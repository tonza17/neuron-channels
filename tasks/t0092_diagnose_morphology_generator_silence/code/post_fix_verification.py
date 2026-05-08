"""Phase F: post-fix 8-direction bar protocol (REQ-8, REQ-9, REQ-12).

Required block: re-run the BedB-equivalent procedural cell with the soma fix
under the t0083 best-cell channel set and check PD-rate > 0 Hz AND DSI > 0.1.

Stretch block: re-run the 5 STABLE-but-silent cells from t0090 verification
(``different/morph_00``, ``13``, ``14``, ``15``, ``19``) and report DSI per
cell.

Outputs:

* ``data/post_fix_verification.json`` — one block per cell
* ``results/images/post_fix_polar_tuning.png`` — six polar tuning curves
* ``results/metrics.json`` — explicit-variant format with the
  ``direction_selectivity_index`` registered metric for the pre-fix and
  post-fix BedB-equivalent variants
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    PD_DIRECTION_DEG,
    SEED_BASE,
    TSTOP_MS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    SynapseBundle,
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    _get_neuron_h,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
    MorphologyResult,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import (
    insert_baseline_channels,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.build_cells import (
    keep_alive,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.constants import (
    ANGLES_8DIR_DEG,
    DSI_PASS_THRESHOLD,
    MORPH_SEED,
    PLACER_SEED,
    SPEC_VERSION_POST_FIX,
    STABLE_T0090_CELLS,
    VARIANT_POST_FIX_BEDB,
    VARIANT_PRE_FIX_BEDB,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import (
    generate_fixed_morphology,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.paths import (
    POST_FIX_POLAR_TUNING_PNG,
    POST_FIX_VERIFICATION_JSON,
    RESULTS_METRICS_JSON,
    T0090_DIFFERENT_DIR,
    ensure_directories,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.trial_with_trace import (
    run_one_trial_with_trace,
)


@dataclass(frozen=True, slots=True)
class CellResult:
    cell_label: str
    spikes_per_direction: dict[float, int]
    pd_rate_hz: float
    nd_rate_hz: float
    dsi: float | None
    peak_vm_pd_mv: float
    error: str | None


def _spikes_to_rate_hz(*, spikes: int, tstop_ms: float) -> float:
    return float(spikes) * 1000.0 / float(tstop_ms)


def _compute_dsi(*, pd_rate: float, nd_rate: float) -> float | None:
    denom = pd_rate + nd_rate
    if denom <= 0.0:
        return None
    return float(pd_rate - nd_rate) / float(denom)


def _run_8dir(
    *,
    cell: MorphologyResult,
    bundle: SynapseBundle,
    cell_label: str,
) -> CellResult:
    spikes_by_angle: dict[float, int] = {}
    pd_peak: float = float("nan")
    last_error: str | None = None
    for angle in ANGLES_8DIR_DEG:
        result = run_one_trial_with_trace(
            cell=cell,
            bundle=bundle,
            direction_deg=float(angle),
            seed=int(SEED_BASE),
        )
        spikes_by_angle[float(angle)] = int(result.spike_count)
        if abs(float(angle) - float(PD_DIRECTION_DEG)) < 1e-6:
            pd_peak = float(result.peak_mv) if np.isfinite(result.peak_mv) else float("nan")
        if result.error is not None:
            last_error = result.error
    pd_rate = _spikes_to_rate_hz(
        spikes=spikes_by_angle.get(float(PD_DIRECTION_DEG), 0),
        tstop_ms=float(TSTOP_MS),
    )
    nd_rate = _spikes_to_rate_hz(
        spikes=spikes_by_angle.get(180.0, 0),
        tstop_ms=float(TSTOP_MS),
    )
    dsi = _compute_dsi(pd_rate=pd_rate, nd_rate=nd_rate)
    return CellResult(
        cell_label=cell_label,
        spikes_per_direction=spikes_by_angle,
        pd_rate_hz=pd_rate,
        nd_rate_hz=nd_rate,
        dsi=dsi,
        peak_vm_pd_mv=pd_peak,
        error=last_error,
    )


def _make_bundle(*, cell: MorphologyResult, pv: Any) -> SynapseBundle:
    return setup_synapses_parametric(
        cell=cell,
        n_ach=pv.n_ach,
        n_gaba=pv.n_gaba,
        rho_0_ach=pv.rho0_ach,
        lambda_ach_um=pv.lambda_ach_um,
        rho_0_gaba=pv.rho0_gaba,
        lambda_gaba_um=pv.lambda_gaba_um,
        w_ach_us=pv.w_ach_us,
        w_gaba_us=pv.w_gaba_us,
        placer_seed=PLACER_SEED,
        gnmda_dend=pv.gnmda_dend,
        mg_conc_mm=pv.mg_conc_mm,
        voff_nmda=pv.voff_nmda,
    )


def _result_to_dict(*, result: CellResult) -> dict[str, Any]:
    spikes_sorted: dict[str, int] = {
        f"{angle:.1f}": int(count) for angle, count in sorted(result.spikes_per_direction.items())
    }
    peak_vm: float | None = (
        float(result.peak_vm_pd_mv) if np.isfinite(result.peak_vm_pd_mv) else None
    )
    return {
        "cell_label": result.cell_label,
        "spikes_per_direction": spikes_sorted,
        "pd_rate_hz": float(result.pd_rate_hz),
        "nd_rate_hz": float(result.nd_rate_hz),
        "dsi": result.dsi if result.dsi is None else float(result.dsi),
        "peak_vm_pd_mv": peak_vm,
        "error": result.error,
    }


def _load_stable_morph_params(*, cell_label: str) -> MorphologyParams:
    """Load a STABLE-from-t0090 cell's MorphologyParams from its diversity-grid file."""
    population, morph_id = cell_label.split("/")
    if population != "different":
        raise ValueError(f"only 'different/' cells supported; got {cell_label}")
    json_path: Path = T0090_DIFFERENT_DIR / f"{morph_id}.json"
    raw = json.loads(json_path.read_text())
    return MorphologyParams.from_dict(data=raw)


def _plot_polar(*, results: list[CellResult], out_png: Path) -> None:
    fig, axes = plt.subplots(
        nrows=2,
        ncols=3,
        subplot_kw={"projection": "polar"},
        figsize=(12, 8),
    )
    flat_axes = list(axes.flat)
    for ax, res in zip(flat_axes, results, strict=False):
        angles = np.array(sorted(res.spikes_per_direction.keys()), dtype=np.float64)
        counts = np.array([res.spikes_per_direction[a] for a in angles], dtype=np.float64)
        rates = counts * 1000.0 / float(TSTOP_MS)
        # Close the polygon
        theta = np.deg2rad(np.append(angles, angles[0]))
        r = np.append(rates, rates[0])
        ax.plot(theta, r, marker="o", linewidth=1.5)
        ax.fill(theta, r, alpha=0.2)
        ax.set_title(
            f"{res.cell_label}\nDSI={res.dsi:.3f}, PD={res.pd_rate_hz:.1f} Hz"
            if res.dsi is not None
            else f"{res.cell_label}\nDSI=N/A, PD={res.pd_rate_hz:.1f} Hz",
            fontsize=9,
        )
    # Hide any extra axes if results < 6
    for ax in flat_axes[len(results) :]:
        ax.set_visible(False)
    fig.suptitle("Post-fix 8-direction polar tuning curves", fontsize=12)
    fig.tight_layout()
    fig.savefig(str(out_png), dpi=150)
    plt.close(fig)


def _build_metrics(
    *,
    pre_fix_dsi: float | None,
    pre_fix_pd_rate: float,
    post_fix_dsi: float | None,
    post_fix_pd_rate: float,
) -> dict[str, Any]:
    """Return metrics.json payload using the explicit-variant format."""
    return {
        "variants": [
            {
                "variant_id": VARIANT_PRE_FIX_BEDB,
                "label": "Pre-fix procedural BedB-equivalent",
                "dimensions": {
                    "morphology": "procedural_bedb_unpatched",
                    "channels": "t0083_best_cell",
                },
                "metrics": {
                    "direction_selectivity_index": pre_fix_dsi,
                },
            },
            {
                "variant_id": VARIANT_POST_FIX_BEDB,
                "label": "Post-fix procedural BedB-equivalent",
                "dimensions": {
                    "morphology": "procedural_bedb_t0092_fixed",
                    "channels": "t0083_best_cell",
                },
                "metrics": {
                    "direction_selectivity_index": post_fix_dsi,
                },
            },
        ]
    }


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Phase F post-fix 8-direction verification")
    parser.add_argument(
        "--skip-stretch",
        action="store_true",
        help="Skip the stretch block (5 STABLE-from-t0090 cells). The BedB-equivalent block alone "
        "satisfies REQ-8 if PD-rate > 0 Hz.",
    )
    parser.add_argument(
        "--max-stretch-cells",
        type=int,
        default=len(STABLE_T0090_CELLS),
        help="Limit the stretch block to N cells (default: all 5).",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    ensure_directories()

    # Load t0083 best-cell vector once.
    pv = load_t0083_best_cell_param_vector()

    # 1. Required block — patched BedB-equivalent.
    h = _get_neuron_h()
    fixed_bedb = generate_fixed_morphology(
        params=MorphologyParams.from_bedb_base_point(),
        morph_seed=MORPH_SEED,
    )
    keep_alive(fixed_bedb)
    insert_baseline_channels(h=h, cell=fixed_bedb)
    apply_parameter_vector(cell=fixed_bedb, params=pv)  # type: ignore[arg-type]
    bundle_bedb = _make_bundle(cell=fixed_bedb, pv=pv)

    bedb_result = _run_8dir(
        cell=fixed_bedb,
        bundle=bundle_bedb,
        cell_label="bedb_fixed",
    )

    # Validation gate: halt-after-3-cells if BedB-equivalent fails.
    bedb_passes = bedb_result.pd_rate_hz > 0.0 and (
        bedb_result.dsi is not None and bedb_result.dsi > DSI_PASS_THRESHOLD
    )
    # PD-rate > 0 alone is sufficient to demonstrate the silence fix; we run
    # the stretch cells whenever PD-rate is non-zero so the panel exists even
    # when the DSI tightening goal misses.
    bedb_silence_resolved = bedb_result.pd_rate_hz > 0.0

    # 2. Stretch block — 5 STABLE-from-t0090 cells (or fewer if requested).
    stretch_results: list[CellResult] = []
    cells_to_run: tuple[str, ...] = (
        () if args.skip_stretch else STABLE_T0090_CELLS[: int(args.max_stretch_cells)]
    )
    if bedb_silence_resolved and len(cells_to_run) > 0:
        for cell_label in cells_to_run:
            try:
                params = _load_stable_morph_params(cell_label=cell_label)
                cell = generate_fixed_morphology(
                    params=params,
                    morph_seed=int(params.morph_seed),
                )
                keep_alive(cell)
                insert_baseline_channels(h=h, cell=cell)
                apply_parameter_vector(cell=cell, params=pv)  # type: ignore[arg-type]
                bundle = _make_bundle(cell=cell, pv=pv)
                res = _run_8dir(
                    cell=cell,
                    bundle=bundle,
                    cell_label=cell_label,
                )
                stretch_results.append(res)
            except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
                stretch_results.append(
                    CellResult(
                        cell_label=cell_label,
                        spikes_per_direction={float(a): 0 for a in ANGLES_8DIR_DEG},
                        pd_rate_hz=0.0,
                        nd_rate_hz=0.0,
                        dsi=None,
                        peak_vm_pd_mv=float("nan"),
                        error=f"{type(exc).__name__}: {exc}",
                    )
                )
    elif not bedb_silence_resolved:
        print("WARNING: BedB-equivalent had zero PD spikes; skipping stretch cells.")
    else:
        print("Skipping stretch block (--skip-stretch or --max-stretch-cells=0).")

    # Plot the polar tuning panel.
    polar_results = [bedb_result] + stretch_results
    if len(polar_results) > 0:
        _plot_polar(results=polar_results, out_png=POST_FIX_POLAR_TUNING_PNG)

    # Pre-fix DSI from Phase C: procedural cell had non-finite voltage and 0
    # spikes -> DSI is None (no rate to compute, denominator zero).
    pre_fix_dsi: float | None = None
    pre_fix_pd_rate: float = 0.0

    payload: dict[str, Any] = {
        "spec_version": SPEC_VERSION_POST_FIX,
        "morph_seed": int(MORPH_SEED),
        "placer_seed": int(PLACER_SEED),
        "trial_seed": int(SEED_BASE),
        "tstop_ms": float(TSTOP_MS),
        "procedural_bedb_fixed": _result_to_dict(result=bedb_result),
        "stretch_stable_cells": [_result_to_dict(result=r) for r in stretch_results],
        "pass_criterion": {
            "pd_rate_hz_strictly_positive": bedb_result.pd_rate_hz > 0.0,
            "dsi_above_threshold": (
                bedb_result.dsi is not None and bedb_result.dsi > DSI_PASS_THRESHOLD
            ),
            "passed": bedb_passes,
            "dsi_threshold": float(DSI_PASS_THRESHOLD),
        },
        "stretch_summary": {
            "n_cells": len(stretch_results),
            "n_with_pd_spikes": sum(1 for r in stretch_results if r.pd_rate_hz > 0.0),
            "stretch_target_n_with_pd_spikes": 3,
        },
    }
    POST_FIX_VERIFICATION_JSON.write_text(json.dumps(payload, indent=2))

    metrics_payload = _build_metrics(
        pre_fix_dsi=pre_fix_dsi,
        pre_fix_pd_rate=pre_fix_pd_rate,
        post_fix_dsi=bedb_result.dsi,
        post_fix_pd_rate=bedb_result.pd_rate_hz,
    )
    RESULTS_METRICS_JSON.write_text(json.dumps(metrics_payload, indent=2))

    print(f"BedB-fixed: PD-rate={bedb_result.pd_rate_hz:.2f} Hz, DSI={bedb_result.dsi}")
    for r in stretch_results:
        print(f"  {r.cell_label}: PD-rate={r.pd_rate_hz:.2f} Hz, DSI={r.dsi}")
    print(f"pass: {bedb_passes}")
    print(f"wrote {POST_FIX_VERIFICATION_JSON}")
    print(f"wrote {POST_FIX_POLAR_TUNING_PNG}")
    print(f"wrote {RESULTS_METRICS_JSON}")
    return 0 if bedb_passes else 0  # do not exit non-zero — orchestrator owns lifecycle


if __name__ == "__main__":
    raise SystemExit(main())
