"""Phase B: synapse-placement comparison (REQ-2).

Places ACh + GABA synapses on both cells using the t0083 best-cell synaptic
parameters and the same ``placer_seed=42``. Records per-synapse XY plus the
PD-direction bar arrival times under ``BAR_X_START_UM=-40``,
``BAR_VELOCITY_UM_PER_MS=1.0``, ``TSTOP_MS=1400`` and the t0024
``BAR_START_TIME_MS=0.0`` constants used by the trial driver.

Per-cell summary fields: synapse-XY centroid, bounding box, distribution of
arrival times (min, max, mean, fraction-within-window).
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    PD_DIRECTION_DEG,
    TSTOP_MS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    SynapseBundle,
    _bar_arrival_times,
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.build_cells import (
    TwoCells,
    build_both_cells,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.constants import (
    PLACER_SEED,
    SPEC_VERSION_SYNAPSE,
)
from tasks.t0092_diagnose_morphology_generator_silence.code.paths import (
    SYNAPSE_COMPARISON_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class CellSynapseSummary:
    cell_kind: str
    n_ach_placed: int
    n_gaba_placed: int
    syn_centroid_xy: tuple[float, float]
    syn_bbox_min_xy: tuple[float, float]
    syn_bbox_max_xy: tuple[float, float]
    pd_arrival_min_ms: float
    pd_arrival_max_ms: float
    pd_arrival_mean_ms: float
    pd_arrival_fraction_in_window: float


def _bbox(xy: NDArray[np.float64]) -> tuple[tuple[float, float], tuple[float, float]]:
    if xy.shape[0] == 0:
        return ((0.0, 0.0), (0.0, 0.0))
    mn = (float(xy[:, 0].min()), float(xy[:, 1].min()))
    mx = (float(xy[:, 0].max()), float(xy[:, 1].max()))
    return (mn, mx)


def _centroid(xy: NDArray[np.float64]) -> tuple[float, float]:
    if xy.shape[0] == 0:
        return (0.0, 0.0)
    return (float(xy[:, 0].mean()), float(xy[:, 1].mean()))


def _arrival_stats(
    *,
    syn_xy: NDArray[np.float64],
    origin_xy: tuple[float, float],
) -> tuple[float, float, float, float]:
    if syn_xy.shape[0] == 0:
        return (0.0, 0.0, 0.0, 0.0)
    arrivals = _bar_arrival_times(
        syn_xy=syn_xy,
        origin_xy=origin_xy,
        direction_deg=float(PD_DIRECTION_DEG),
    )
    in_window = (arrivals >= 0.0) & (arrivals < float(TSTOP_MS))
    frac = float(np.sum(in_window)) / float(arrivals.shape[0])
    return (
        float(arrivals.min()),
        float(arrivals.max()),
        float(arrivals.mean()),
        frac,
    )


def _summarise_cell(
    *,
    cell_kind: str,
    bundle: SynapseBundle,
    origin_xy: tuple[float, float],
) -> CellSynapseSummary:
    all_xy = np.concatenate([bundle.syn_xy_ach, bundle.syn_xy_gaba], axis=0)
    bbox_min, bbox_max = _bbox(all_xy)
    centroid = _centroid(all_xy)
    arr_min, arr_max, arr_mean, arr_frac = _arrival_stats(
        syn_xy=all_xy,
        origin_xy=origin_xy,
    )
    return CellSynapseSummary(
        cell_kind=cell_kind,
        n_ach_placed=int(bundle.syn_xy_ach.shape[0]),
        n_gaba_placed=int(bundle.syn_xy_gaba.shape[0]),
        syn_centroid_xy=centroid,
        syn_bbox_min_xy=bbox_min,
        syn_bbox_max_xy=bbox_max,
        pd_arrival_min_ms=arr_min,
        pd_arrival_max_ms=arr_max,
        pd_arrival_mean_ms=arr_mean,
        pd_arrival_fraction_in_window=arr_frac,
    )


def _summary_to_dict(*, s: CellSynapseSummary) -> dict[str, Any]:
    return {
        "cell_kind": s.cell_kind,
        "n_ach_placed": s.n_ach_placed,
        "n_gaba_placed": s.n_gaba_placed,
        "syn_centroid_xy": list(s.syn_centroid_xy),
        "syn_bbox_min_xy": list(s.syn_bbox_min_xy),
        "syn_bbox_max_xy": list(s.syn_bbox_max_xy),
        "pd_arrival_min_ms": s.pd_arrival_min_ms,
        "pd_arrival_max_ms": s.pd_arrival_max_ms,
        "pd_arrival_mean_ms": s.pd_arrival_mean_ms,
        "pd_arrival_fraction_in_window": s.pd_arrival_fraction_in_window,
    }


def run_synapse_dump(*, two: TwoCells) -> dict[str, Any]:
    pv = load_t0083_best_cell_param_vector()

    bundle_proc: SynapseBundle = setup_synapses_parametric(
        cell=two.procedural_bedb,
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
    bundle_hand: SynapseBundle = setup_synapses_parametric(
        cell=two.handcoded_bedb,
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

    proc_origin = (
        float(two.procedural_bedb.origin_xy[0]),
        float(two.procedural_bedb.origin_xy[1]),
    )
    hand_origin = (
        float(two.handcoded_bedb.origin_xy[0]),
        float(two.handcoded_bedb.origin_xy[1]),
    )
    proc_summary = _summarise_cell(
        cell_kind="procedural_bedb",
        bundle=bundle_proc,
        origin_xy=proc_origin,
    )
    hand_summary = _summarise_cell(
        cell_kind="handcoded_bedb",
        bundle=bundle_hand,
        origin_xy=hand_origin,
    )

    return (
        {
            "spec_version": SPEC_VERSION_SYNAPSE,
            "n_ach_target": int(pv.n_ach),
            "n_gaba_target": int(pv.n_gaba),
            "placer_seed": int(PLACER_SEED),
            "procedural_bedb": _summary_to_dict(s=proc_summary),
            "handcoded_bedb": _summary_to_dict(s=hand_summary),
        },
        bundle_proc,
        bundle_hand,
    )


def main() -> int:
    ensure_directories()
    two = build_both_cells()
    payload, _, _ = run_synapse_dump(two=two)
    SYNAPSE_COMPARISON_JSON.write_text(json.dumps(payload, indent=2))
    print(f"wrote {SYNAPSE_COMPARISON_JSON}")
    print(
        "procedural arrival fraction in [0, 1400] ms: "
        f"{payload['procedural_bedb']['pd_arrival_fraction_in_window']:.3f}"
    )
    print(
        "handcoded arrival fraction in [0, 1400] ms: "
        f"{payload['handcoded_bedb']['pd_arrival_fraction_in_window']:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
