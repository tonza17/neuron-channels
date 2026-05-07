"""Phase D: per-morphology verification simulation.

For each of the 60 morphologies:

1. Build the procedural cell from the morph params (using ``generate_morphology``).
2. Run a 50 ms no-stim stability check at V_rest = -70 mV.
3. If stable, run an 8-direction bar protocol (1 seed per direction) with the
   t0083 best-cell parameter vector via the t0080 trial helpers.
4. Record per-morphology stability flag + DSI + PD-rate.

The driver is ``verify_morphology_file(morph_path, default_params_values)`` which
accepts only picklable arguments (the morph spec JSON path and the 54-d param
array). It is therefore safe to dispatch on a ``ProcessPoolExecutor`` if needed.

For determinism + simplicity we run sequentially by default; the
``--max-workers`` flag enables process-pool parallelism.
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
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_DIFFERENT_DIR,
    DATA_SIMILAR_DIR,
    DATA_VERIFICATION_JSON,
    ensure_directories,
)


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
        "morph_id": r.morph_id,
        "population": r.population,
        "morph_index": r.morph_index,
        "stability_flag": r.stability_flag.value,
        "dsi": r.dsi,
        "pd_rate_hz": r.pd_rate_hz,
        "nd_rate_hz": r.nd_rate_hz,
        "peak_vm_mv": r.peak_vm_mv,
        "n_dendrites": r.n_dendrites,
        "n_terminals": r.n_terminals,
        "elapsed_s": r.elapsed_s,
        "error": r.error,
        "per_direction_spikes": {
            f"{angle:.1f}": int(count) for angle, count in sorted(r.per_direction_spikes.items())
        },
    }


# Module-level list keeps every built cell alive for the duration of the
# verification process; without it, Python may garbage-collect a previous cell
# and re-use its id, causing t0080's _INSERTED_CELLS / _INSERTED_BASELINE_CELLS
# caches to skip channel insertion on a fresh cell.
_LIVE_CELLS: list[Any] = []


def _insert_baseline_channels(*, cell: Any) -> None:
    """Insert HHst + cad on soma + all dendrites of one procedural cell.

    NEURON sections do not error on duplicate ``insert(name)`` calls — they
    silently no-op — so this helper does not need its own idempotency cache.
    """
    sections: list[Any] = [cell.soma] + list(cell.all_dends)
    for sec in sections:
        sec.insert("HHst")
        sec.insert("cad")
    for ais_sec in (cell.ais_proximal, cell.ais_distal):
        ais_sec.insert("HHst")


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
    """Build, stability-check, and 8-direction-protocol one morphology."""
    t0 = time.time()
    try:
        cell = generate_morphology(params=params, morph_seed=int(params.morph_seed))
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

    # Insert HHst + cad on soma + dendrites (apply_parameter_vector assumes these
    # are already present — t0024's build_cell does this in _configure_soma /
    # _configure_dends; our procedural cell omits those calls).
    try:
        _insert_baseline_channels(cell=cell)
        # Sanity: confirm HHst is present on the soma midpoint segment.
        _ = cell.soma(0.5).HHst.gleak
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

    # 50 ms no-stim stability check at V_rest = -70 mV (now with channels installed).
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

    # Build synapses (apply_parameter_vector already wrote channel densities).
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
    # Final NaN check on a longer trial: if any spike count is unrealistically high,
    # something diverged.
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
    """Pickleable worker: build a cell, verify, return result dict."""
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
            "morph_id": Path(morph_path_str).stem,
            "population": population,
            "morph_index": morph_index,
            "stability_flag": StabilityKind.DISCONNECTED.value,
            "dsi": None,
            "pd_rate_hz": None,
            "nd_rate_hz": None,
            "peak_vm_mv": None,
            "n_dendrites": 0,
            "n_terminals": 0,
            "elapsed_s": 0.0,
            "error": traceback.format_exc(limit=3),
            "per_direction_spikes": {},
        }


def collect_morph_paths(*, limit: int | None = None) -> list[tuple[str, int, Path]]:
    """Return ``(population, morph_index, morph_path)`` tuples for all 60 morphs."""
    out: list[tuple[str, int, Path]] = []
    for population, directory in (
        ("different", DATA_DIFFERENT_DIR),
        ("similar", DATA_SIMILAR_DIR),
    ):
        all_paths = sorted(directory.glob("morph_*.json"))
        for i, p in enumerate(all_paths):
            out.append((population, i, p))
    if limit is not None:
        out = out[:limit]
    return out


def run_verification(
    *,
    limit: int | None = None,
    max_workers: int = 1,
) -> list[dict[str, Any]]:
    """Run the verification pipeline; write to ``DATA_VERIFICATION_JSON``."""
    ensure_directories()
    default_params = load_t0083_best_cell_param_vector()
    morph_specs = collect_morph_paths(limit=limit)
    print(f"verifying {len(morph_specs)} morphologies (max_workers={max_workers})")

    results: list[dict[str, Any]] = []
    if max_workers <= 1:
        for population, morph_index, morph_path in tqdm(morph_specs, desc="verify"):
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
                    )
                )
            for f in tqdm(as_completed(futures), total=len(futures), desc="verify"):
                results.append(f.result())

    # Sort for deterministic output.
    results.sort(key=lambda d: (d["population"], d["morph_index"]))

    # Write the summary.
    DATA_VERIFICATION_JSON.write_text(json.dumps(results, indent=2))
    n_stable = sum(1 for r in results if r["stability_flag"] == StabilityKind.STABLE.value)
    print(f"wrote {len(results)} entries to {DATA_VERIFICATION_JSON}")
    print(f"stable: {n_stable}/{len(results)}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit the number of morphologies (validation gate).",
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=1,
        help="Worker process count. Use 1 for sequential debugging.",
    )
    args = parser.parse_args()
    if args.max_workers == 0:
        args.max_workers = max(1, (cpu_count() or 4) - 1)
    run_verification(limit=args.limit, max_workers=int(args.max_workers))


if __name__ == "__main__":
    main()
