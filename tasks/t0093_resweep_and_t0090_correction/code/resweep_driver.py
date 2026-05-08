"""Re-sweep driver: re-run t0090's full 60-morphology Phase D verification under
t0092's patched ``generate_fixed_morphology``.

Adapted verbatim from
``tasks/t0090_morphology_generator_diversity_test/code/verification.py`` with
two surgical changes:

1. Build-cell call site swapped from ``generate_morphology`` to
   ``generate_fixed_morphology``.
2. Inline ``_insert_baseline_channels`` replaced with the registered library
   helper ``insert_baseline_channels`` from t0092.

Two new columns are appended to the output JSON: ``pre_fix_stability_flag`` and
``pre_fix_spike_count_total``. Both are populated by reading t0090's
pre-fix ``verification_summary.json`` once at driver start and looking up
``(population, morph_id)``. All other code is reused unchanged so any per-cell
delta between t0090's pre-fix JSON and the post-fix JSON is attributable to the
soma-area patch and nothing else.
"""

from __future__ import annotations

import argparse
import json
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from dataclasses import dataclass, field
from os import cpu_count
from pathlib import Path
from typing import Any, cast

import numpy as np
from numpy.typing import NDArray
from tqdm import tqdm

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import (
    DSGCCellWithAIS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    CELSIUS_DEG_C,
    DT_MS,
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
    SEED_BASE,
    STEPS_PER_MS,
    TSTOP_MS,
    ParameterVector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    run_one_trial,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    ANGLES_8DIR_DEG,
    VERIFY_NO_STIM_MS,
    VERIFY_V_INIT_MV,
    VERIFY_V_NAN_THRESHOLD_MV,
    StabilityKind,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0093_resweep_and_t0090_correction.code.constants import (
    FIELD_DSI,
    FIELD_ELAPSED_S,
    FIELD_ERROR,
    FIELD_MORPH_ID,
    FIELD_MORPH_INDEX,
    FIELD_N_DENDRITES,
    FIELD_N_TERMINALS,
    FIELD_ND_RATE_HZ,
    FIELD_PD_RATE_HZ,
    FIELD_PEAK_VM_MV,
    FIELD_PER_DIRECTION_SPIKES,
    FIELD_POPULATION,
    FIELD_PRE_FIX_SPIKE_COUNT_TOTAL,
    FIELD_PRE_FIX_STABILITY_FLAG,
    FIELD_STABILITY_FLAG,
    POPULATION_DIFFERENT,
    POPULATION_SIMILAR,
)
from tasks.t0093_resweep_and_t0090_correction.code.paths import (
    DATA_POST_FIX_VERIFICATION_JSON,
    T0090_DIFFERENT_DIR,
    T0090_SIMILAR_DIR,
    T0090_VERIFICATION_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class PreFixRow:
    """Pre-fix row data needed to populate the new comparison columns."""

    stability_flag: str
    spike_count_total: int


@dataclass(frozen=True, slots=True)
class VerificationResult:
    morph_id: str
    population: str  # "different" or "similar"
    morph_index: int
    stability_flag: StabilityKind
    dsi: float | None
    pd_rate_hz: float | None
    nd_rate_hz: float | None
    peak_vm_mv: float | None
    n_dendrites: int
    n_terminals: int
    elapsed_s: float
    error: str | None = None
    per_direction_spikes: dict[float, int] = field(default_factory=dict)


def _to_dict(*, r: VerificationResult) -> dict[str, Any]:
    return {
        FIELD_MORPH_ID: r.morph_id,
        FIELD_POPULATION: r.population,
        FIELD_MORPH_INDEX: r.morph_index,
        FIELD_STABILITY_FLAG: r.stability_flag.value,
        FIELD_DSI: r.dsi,
        FIELD_PD_RATE_HZ: r.pd_rate_hz,
        FIELD_ND_RATE_HZ: r.nd_rate_hz,
        FIELD_PEAK_VM_MV: r.peak_vm_mv,
        FIELD_N_DENDRITES: r.n_dendrites,
        FIELD_N_TERMINALS: r.n_terminals,
        FIELD_ELAPSED_S: r.elapsed_s,
        FIELD_ERROR: r.error,
        FIELD_PER_DIRECTION_SPIKES: {
            f"{angle:.1f}": int(count) for angle, count in sorted(r.per_direction_spikes.items())
        },
    }


# Module-level list keeps every built cell alive for the duration of the
# verification process; without it, Python may garbage-collect a previous cell
# and re-use its id, causing t0080's _INSERTED_CELLS / _INSERTED_BASELINE_CELLS
# caches to skip channel insertion on a fresh cell.
_LIVE_CELLS: list[Any] = []


def _stability_check_no_stim(
    *,
    h: Any,
    soma_sec: Any,
    duration_ms: float,
) -> tuple[StabilityKind, float]:
    """Run a brief no-stim simulation; return (StabilityKind, peak_vm_mv)."""
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.steps_per_ms = STEPS_PER_MS
    h.v_init = VERIFY_V_INIT_MV
    h.tstop = float(duration_ms)

    v_vec = h.Vector()
    v_vec.record(soma_sec(0.5)._ref_v)
    h.finitialize(VERIFY_V_INIT_MV)
    try:
        h.run()
    except (RuntimeError, ValueError, ArithmeticError):
        return StabilityKind.DIVERGED, float("nan")
    v_arr: NDArray[np.float64] = np.asarray(v_vec.to_python(), dtype=np.float64)
    if v_arr.size == 0:
        return StabilityKind.DISCONNECTED, float("nan")
    if not np.all(np.isfinite(v_arr)):
        return StabilityKind.NAN_VOLTAGE, float("nan")
    peak = float(v_arr.max())
    if abs(peak) > VERIFY_V_NAN_THRESHOLD_MV:
        return StabilityKind.DIVERGED, peak
    return StabilityKind.STABLE, peak


def _run_8direction_protocol(
    *,
    cell: Any,
    bundle: Any,
    angles_deg: tuple[int, ...],
    seed_base: int,
) -> dict[float, int]:
    """Run one trial per direction; return per-direction spike counts."""
    spikes_by_angle: dict[float, int] = {}
    for angle in angles_deg:
        seed = seed_base + int(angle) * 13
        result = run_one_trial(
            cell=cell,
            bundle=bundle,
            direction_deg=float(angle),
            seed=seed,
        )
        spikes_by_angle[float(angle)] = int(result.spike_count)
    return spikes_by_angle


def verify_one_morphology(
    *,
    morph_id: str,
    population: str,
    morph_index: int,
    params: MorphologyParams,
    default_params: ParameterVector,
) -> VerificationResult:
    """Build (with patched generator), stability-check, 8-direction-protocol one cell."""
    t0 = time.time()
    try:
        cell = generate_fixed_morphology(params=params, morph_seed=int(params.morph_seed))
        _LIVE_CELLS.append(cell)
    except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
        return VerificationResult(
            morph_id=morph_id,
            population=population,
            morph_index=morph_index,
            stability_flag=StabilityKind.DISCONNECTED,
            dsi=None,
            pd_rate_hz=None,
            nd_rate_hz=None,
            peak_vm_mv=None,
            n_dendrites=0,
            n_terminals=0,
            elapsed_s=time.time() - t0,
            error=f"build_failed: {type(exc).__name__}: {exc}",
        )

    n_dendrites = len(cell.all_dends)
    n_terminals = len(cell.terminal_dends)

    # Insert HHst + cad on soma + dendrites + AIS using t0092's library helper.
    try:
        insert_baseline_channels(h=cell.h, cell=cell)
        _ = cell.soma(0.5).HHst.gleak  # sanity: confirm HHst is present.
        apply_parameter_vector(cell=cast(DSGCCellWithAIS, cell), params=default_params)
    except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
        return VerificationResult(
            morph_id=morph_id,
            population=population,
            morph_index=morph_index,
            stability_flag=StabilityKind.DIVERGED,
            dsi=None,
            pd_rate_hz=None,
            nd_rate_hz=None,
            peak_vm_mv=None,
            n_dendrites=n_dendrites,
            n_terminals=n_terminals,
            elapsed_s=time.time() - t0,
            error=f"apply_params_failed: {type(exc).__name__}: {exc}",
        )

    # 50 ms no-stim stability check at V_rest = -70 mV (with channels installed).
    stability, peak = _stability_check_no_stim(
        h=cell.h,
        soma_sec=cell.soma,
        duration_ms=VERIFY_NO_STIM_MS,
    )
    if stability is not StabilityKind.STABLE:
        return VerificationResult(
            morph_id=morph_id,
            population=population,
            morph_index=morph_index,
            stability_flag=stability,
            dsi=None,
            pd_rate_hz=None,
            nd_rate_hz=None,
            peak_vm_mv=peak if np.isfinite(peak) else None,
            n_dendrites=n_dendrites,
            n_terminals=n_terminals,
            elapsed_s=time.time() - t0,
            error=None,
        )

    # Build synapses.
    placer_seed = SEED_BASE + (int(hash(default_params.values.tobytes())) & 0xFFFF)
    try:
        bundle = setup_synapses_parametric(
            cell=cast(DSGCCellWithAIS, cell),
            n_ach=default_params.n_ach,
            n_gaba=default_params.n_gaba,
            rho_0_ach=default_params.rho0_ach,
            lambda_ach_um=default_params.lambda_ach_um,
            rho_0_gaba=default_params.rho0_gaba,
            lambda_gaba_um=default_params.lambda_gaba_um,
            w_ach_us=default_params.w_ach_us,
            w_gaba_us=default_params.w_gaba_us,
            placer_seed=placer_seed,
            gnmda_dend=default_params.gnmda_dend,
            mg_conc_mm=default_params.mg_conc_mm,
            voff_nmda=default_params.voff_nmda,
        )
    except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
        return VerificationResult(
            morph_id=morph_id,
            population=population,
            morph_index=morph_index,
            stability_flag=StabilityKind.DIVERGED,
            dsi=None,
            pd_rate_hz=None,
            nd_rate_hz=None,
            peak_vm_mv=peak,
            n_dendrites=n_dendrites,
            n_terminals=n_terminals,
            elapsed_s=time.time() - t0,
            error=f"setup_synapses_failed: {type(exc).__name__}: {exc}",
        )

    spikes_by_angle = _run_8direction_protocol(
        cell=cell,
        bundle=bundle,
        angles_deg=ANGLES_8DIR_DEG,
        seed_base=SEED_BASE + int(params.morph_seed),
    )

    pd_count = spikes_by_angle.get(PD_DIRECTION_DEG, 0)
    nd_count = spikes_by_angle.get(ND_DIRECTION_DEG, 0)
    pd_rate = pd_count / (TSTOP_MS / 1000.0)
    nd_rate = nd_count / (TSTOP_MS / 1000.0)
    denom = pd_count + nd_count
    dsi = float((pd_count - nd_count) / denom) if denom > 0 else 0.0
    max_spikes = max(spikes_by_angle.values()) if len(spikes_by_angle) > 0 else 0
    if max_spikes > 5000:
        return VerificationResult(
            morph_id=morph_id,
            population=population,
            morph_index=morph_index,
            stability_flag=StabilityKind.DIVERGED,
            dsi=None,
            pd_rate_hz=None,
            nd_rate_hz=None,
            peak_vm_mv=peak,
            n_dendrites=n_dendrites,
            n_terminals=n_terminals,
            elapsed_s=time.time() - t0,
            error=f"runaway_spiking: max={max_spikes}",
            per_direction_spikes=spikes_by_angle,
        )

    return VerificationResult(
        morph_id=morph_id,
        population=population,
        morph_index=morph_index,
        stability_flag=StabilityKind.STABLE,
        dsi=float(dsi),
        pd_rate_hz=float(pd_rate),
        nd_rate_hz=float(nd_rate),
        peak_vm_mv=peak,
        n_dendrites=n_dendrites,
        n_terminals=n_terminals,
        elapsed_s=time.time() - t0,
        error=None,
        per_direction_spikes=spikes_by_angle,
    )


# ---------------------------------------------------------------------------
# Worker entrypoint (top-level so it pickles cleanly).
# ---------------------------------------------------------------------------


def _worker_verify(
    *,
    morph_path_str: str,
    default_params_values: NDArray[np.float64],
    population: str,
    morph_index: int,
) -> dict[str, Any]:
    """Pickleable worker: build a cell with patched generator, verify, return dict."""
    try:
        morph_path = Path(morph_path_str)
        data = json.loads(morph_path.read_text())
        params = MorphologyParams.from_dict(data=data)
        default_params = ParameterVector(values=default_params_values)
        result = verify_one_morphology(
            morph_id=morph_path.stem,
            population=population,
            morph_index=morph_index,
            params=params,
            default_params=default_params,
        )
        return _to_dict(r=result)
    except (RuntimeError, ValueError, ArithmeticError, AssertionError):
        return {
            FIELD_MORPH_ID: Path(morph_path_str).stem,
            FIELD_POPULATION: population,
            FIELD_MORPH_INDEX: morph_index,
            FIELD_STABILITY_FLAG: StabilityKind.DISCONNECTED.value,
            FIELD_DSI: None,
            FIELD_PD_RATE_HZ: None,
            FIELD_ND_RATE_HZ: None,
            FIELD_PEAK_VM_MV: None,
            FIELD_N_DENDRITES: 0,
            FIELD_N_TERMINALS: 0,
            FIELD_ELAPSED_S: 0.0,
            FIELD_ERROR: traceback.format_exc(limit=3),
            FIELD_PER_DIRECTION_SPIKES: {},
        }


def collect_morph_paths(
    *,
    limit: int | None = None,
    per_population: bool = True,
) -> list[tuple[str, int, Path]]:
    """Return ``(population, morph_index, morph_path)`` tuples.

    ``limit`` caps the per-population count when ``per_population=True``, else the total.
    """
    out: list[tuple[str, int, Path]] = []
    for population, directory in (
        (POPULATION_DIFFERENT, T0090_DIFFERENT_DIR),
        (POPULATION_SIMILAR, T0090_SIMILAR_DIR),
    ):
        all_paths = sorted(directory.glob("morph_*.json"))
        if limit is not None and per_population:
            all_paths = all_paths[:limit]
        for i, p in enumerate(all_paths):
            out.append((population, i, p))
    if limit is not None and not per_population:
        out = out[:limit]
    return out


def _load_pre_fix_lookup(*, path: Path) -> dict[tuple[str, str], PreFixRow]:
    """Read t0090's pre-fix verification_summary.json into a (pop, morph_id) lookup."""
    if not path.exists():
        return {}
    raw = json.loads(path.read_text())
    assert isinstance(raw, list), f"expected list, got {type(raw).__name__}"
    out: dict[tuple[str, str], PreFixRow] = {}
    for row in raw:
        assert isinstance(row, dict)
        per_dir: dict[str, int] = row.get(FIELD_PER_DIRECTION_SPIKES, {}) or {}
        spike_count_total: int = int(sum(int(v) for v in per_dir.values()))
        out[(str(row[FIELD_POPULATION]), str(row[FIELD_MORPH_ID]))] = PreFixRow(
            stability_flag=str(row[FIELD_STABILITY_FLAG]),
            spike_count_total=spike_count_total,
        )
    return out


def _augment_with_pre_fix(
    *,
    rows: list[dict[str, Any]],
    pre_fix_lookup: dict[tuple[str, str], PreFixRow],
) -> list[dict[str, Any]]:
    """Append the two pre-fix-comparison columns to each row in place + return."""
    for row in rows:
        key = (str(row[FIELD_POPULATION]), str(row[FIELD_MORPH_ID]))
        pre = pre_fix_lookup.get(key)
        if pre is None:
            row[FIELD_PRE_FIX_STABILITY_FLAG] = None
            row[FIELD_PRE_FIX_SPIKE_COUNT_TOTAL] = 0
        else:
            row[FIELD_PRE_FIX_STABILITY_FLAG] = pre.stability_flag
            row[FIELD_PRE_FIX_SPIKE_COUNT_TOTAL] = int(pre.spike_count_total)
    return rows


def run_resweep(
    *,
    limit: int | None = None,
    max_workers: int = 1,
) -> list[dict[str, Any]]:
    """Run the patched-generator re-sweep; write to ``DATA_POST_FIX_VERIFICATION_JSON``."""
    ensure_directories()
    default_params = load_t0083_best_cell_param_vector()
    morph_specs = collect_morph_paths(limit=limit)
    pre_fix_lookup = _load_pre_fix_lookup(path=T0090_VERIFICATION_JSON)
    print(
        f"resweep: {len(morph_specs)} morphologies, max_workers={max_workers}, "
        f"pre_fix_lookup_size={len(pre_fix_lookup)}",
    )

    results: list[dict[str, Any]] = []
    if max_workers <= 1:
        for population, morph_index, morph_path in tqdm(morph_specs, desc="resweep"):
            d = _worker_verify(
                morph_path_str=str(morph_path),
                default_params_values=default_params.values,
                population=population,
                morph_index=morph_index,
            )
            results.append(d)
    else:
        with ProcessPoolExecutor(max_workers=max_workers) as ex:
            futures = []
            for population, morph_index, morph_path in morph_specs:
                futures.append(
                    ex.submit(
                        _worker_verify,
                        morph_path_str=str(morph_path),
                        default_params_values=default_params.values,
                        population=population,
                        morph_index=morph_index,
                    ),
                )
            for f in tqdm(as_completed(futures), total=len(futures), desc="resweep"):
                results.append(f.result())

    # Sort for deterministic output.
    results.sort(key=lambda d: (str(d[FIELD_POPULATION]), int(d[FIELD_MORPH_INDEX])))

    augmented = _augment_with_pre_fix(rows=results, pre_fix_lookup=pre_fix_lookup)

    # Write the summary.
    DATA_POST_FIX_VERIFICATION_JSON.write_text(json.dumps(augmented, indent=2))
    n_stable = sum(1 for r in augmented if r[FIELD_STABILITY_FLAG] == StabilityKind.STABLE.value)
    n_firing = sum(
        1 for r in augmented if r[FIELD_PD_RATE_HZ] is not None and float(r[FIELD_PD_RATE_HZ]) > 0.0
    )
    print(f"wrote {len(augmented)} entries to {DATA_POST_FIX_VERIFICATION_JSON}")
    print(f"stable: {n_stable}/{len(augmented)}; pd_rate>0: {n_firing}/{len(augmented)}")
    return augmented


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit per-population morph count (validation gate runs --limit 5).",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=1,
        help="Worker process count; 0 = autodetect (cpu_count - 1); 1 = sequential.",
    )
    args = parser.parse_args()
    if args.max_workers == 0:
        args.max_workers = max(1, (cpu_count() or 4) - 1)
    run_resweep(limit=args.limit, max_workers=int(args.max_workers))


if __name__ == "__main__":
    main()
