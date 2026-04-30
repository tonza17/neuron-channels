"""EPSP_PASSIVE / IPSP_PASSIVE / FULL trial-mode protocol on the de Rosenroll DSGC.

Builds the t0024 cell once per trial, applies per-mode synaptic and HH-channel
overrides, runs a single moving-bar trial, and captures the somatic Vm trace.
6 cells (3 modes x 2 directions) x 20 trials = 120 trials. Outputs:

* ``data/voltage_traces.csv`` (long-format mode/direction/trial/t_ms/v_mv)
* ``data/per_trial_metrics.json`` (per-trial scalar dump)
* ``results/metrics.json`` (registered direction_selectivity_index)
"""

from __future__ import annotations

import argparse
import csv
import json
import time
from dataclasses import dataclass
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import build_cell as _t0024_build_cell
from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import (
    DSGCCell,
    build_dsgc_cell,
)
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.run_tuning_curve import (
    BASE_ACH_PROB,
    RATE_DT_MS,
    SynapseBundle,
    _bar_arrival_times,
    _count_spikes,
    _gaba_prob_for_direction,
    _rates_to_events,
    _rates_with_ar2_noise,
    _setup_synapses,
)
from tasks.t0066_t0024_epsp_ipsp_vm_protocol.code.constants import (
    BASELINE_V_MV_KEY,
    BASELINE_WINDOW_MS,
    CSV_COLUMNS,
    CSV_SUBSAMPLE_STRIDE,
    DIRECTION_ND_DEG,
    DIRECTION_PD_DEG,
    METRIC_KEY_DSI,
    N_SAMPLES_KEY,
    N_TRIALS_PER_CELL,
    PEAK_MINUS_BASELINE_KEY,
    PEAK_V_MV_KEY,
    RHO_CORRELATED,
    SEED_BASE,
    SPIKE_COUNT_KEY,
    Condition,
    TrialMode,
)
from tasks.t0066_t0024_epsp_ipsp_vm_protocol.code.paths import (
    DATA_DIR,
    METRICS_JSON,
    PER_TRIAL_METRICS_JSON,
    RESULTS_DIR,
    VOLTAGE_TRACES_CSV,
)

_NEURON_LOADED: bool = False


def _ensure_neuron_loaded() -> None:
    """Idempotent NEURON loader: load_neuron() can only be called once per process.

    The t0024 cell builder calls ``load_neuron()`` (which calls ``nrn_load_dll``)
    inside ``build_dsgc_cell()``. Re-calling fails with "user defined name already
    exists: Exp2NMDA". We patch ``t0024.code.build_cell.load_neuron`` to be
    idempotent: first call delegates; subsequent calls return the cached ``h``.
    """
    global _NEURON_LOADED
    if _NEURON_LOADED:
        return
    h = _t0024_build_cell.load_neuron()
    _NEURON_LOADED = True
    _orig_load = _t0024_build_cell.load_neuron

    def _cached_load_neuron() -> Any:
        return h

    _t0024_build_cell.load_neuron = _cached_load_neuron  # type: ignore[assignment]
    _ = _orig_load


@dataclass(frozen=True, slots=True)
class TrialKey:
    mode: TrialMode
    direction: Condition
    trial_index: int


@dataclass(frozen=True, slots=True)
class TrialOutput:
    key: TrialKey
    v_trace_mv: NDArray[np.float64]
    t_trace_ms: NDArray[np.float64]
    peak_v_mv: float
    baseline_v_mv: float
    peak_minus_baseline_mv: float
    spike_count: int | None
    n_samples: int


def _direction_deg(*, condition: Condition) -> float:
    if condition == Condition.PD:
        return DIRECTION_PD_DEG
    return DIRECTION_ND_DEG


@dataclass(frozen=True, slots=True)
class CanonicalState:
    """Snapshot of cell defaults so we can restore them per trial."""

    ach_weights: list[float]
    gaba_weights: list[float]
    hh_gnabar_per_section: list[list[float]]
    hh_gkbar_per_section: list[list[float]]
    hh_gkmbar_per_section: list[list[float]]
    sections: list[Any]


def _snapshot_canonical_state(*, cell: DSGCCell, bundle: SynapseBundle) -> CanonicalState:
    """Capture canonical synapse weights and HHst conductances for later restore."""
    sections: list[Any] = [cell.soma]
    sections.extend(cell.all_dends)
    hh_gnabar: list[list[float]] = []
    hh_gkbar: list[list[float]] = []
    hh_gkmbar: list[list[float]] = []
    for sec in sections:
        seg_gnabar: list[float] = []
        seg_gkbar: list[float] = []
        seg_gkmbar: list[float] = []
        for seg in sec:
            seg_gnabar.append(float(seg.HHst.gnabar))
            seg_gkbar.append(float(seg.HHst.gkbar))
            seg_gkmbar.append(float(seg.HHst.gkmbar))
        hh_gnabar.append(seg_gnabar)
        hh_gkbar.append(seg_gkbar)
        hh_gkmbar.append(seg_gkmbar)
    return CanonicalState(
        ach_weights=[float(nc.weight[0]) for nc in bundle.ncs_ach],
        gaba_weights=[float(nc.weight[0]) for nc in bundle.ncs_gaba],
        hh_gnabar_per_section=hh_gnabar,
        hh_gkbar_per_section=hh_gkbar,
        hh_gkmbar_per_section=hh_gkmbar,
        sections=sections,
    )


def _restore_canonical_state(*, bundle: SynapseBundle, state: CanonicalState) -> None:
    """Restore canonical synapse weights and HHst conductances."""
    for nc, w in zip(bundle.ncs_ach, state.ach_weights, strict=True):
        nc.weight[0] = w
    for nc, w in zip(bundle.ncs_gaba, state.gaba_weights, strict=True):
        nc.weight[0] = w
    for sec, gnabar_list, gkbar_list, gkmbar_list in zip(
        state.sections,
        state.hh_gnabar_per_section,
        state.hh_gkbar_per_section,
        state.hh_gkmbar_per_section,
        strict=True,
    ):
        for seg, gnabar, gkbar, gkmbar in zip(
            sec, gnabar_list, gkbar_list, gkmbar_list, strict=True
        ):
            seg.HHst.gnabar = gnabar
            seg.HHst.gkbar = gkbar
            seg.HHst.gkmbar = gkmbar


def _apply_mode_overrides(*, cell: DSGCCell, bundle: SynapseBundle, mode: TrialMode) -> None:
    """Apply per-mode silencing on top of the just-restored canonical state."""
    if mode == TrialMode.EPSP_PASSIVE:
        for nc in bundle.ncs_gaba:
            nc.weight[0] = 0.0
    elif mode == TrialMode.IPSP_PASSIVE:
        for nc in bundle.ncs_ach:
            nc.weight[0] = 0.0
    if mode == TrialMode.FULL:
        return
    sections: list[Any] = [cell.soma]
    sections.extend(cell.all_dends)
    for sec in sections:
        for seg in sec:
            seg.HHst.gnabar = 0.0
            seg.HHst.gkbar = 0.0
            seg.HHst.gkmbar = 0.0


def _baseline_v_mv(*, t_ms: NDArray[np.float64], v_mv: NDArray[np.float64]) -> float:
    """Mean Vm over the first BASELINE_WINDOW_MS of the trial."""
    mask = t_ms < BASELINE_WINDOW_MS
    if not mask.any():
        return float("nan")
    return float(np.mean(v_mv[mask]))


def _run_one_trial(
    *,
    cell: DSGCCell,
    bundle: SynapseBundle,
    state: CanonicalState,
    key: TrialKey,
) -> TrialOutput:
    """Reset cell to canonical state, apply mode overrides, run, capture trace."""
    h = cell.h
    _restore_canonical_state(bundle=bundle, state=state)
    _apply_mode_overrides(cell=cell, bundle=bundle, mode=key.mode)

    direction_deg = _direction_deg(condition=key.direction)
    seed = SEED_BASE + key.trial_index
    n_syn = len(cell.terminal_dends)
    n_bins = int(np.ceil(C24.TSTOP_MS / RATE_DT_MS))

    arrival = _bar_arrival_times(
        syn_xy=cell.terminal_locs_xy,
        origin_xy=cell.origin_xy,
        direction_deg=direction_deg,
    )
    ach_rates, gaba_rates = _rates_with_ar2_noise(
        n_syn=n_syn,
        n_bins=n_bins,
        rate_dt_ms=RATE_DT_MS,
        arrival_times_ms=arrival,
        rho=RHO_CORRELATED,
        seed=seed,
    )
    gaba_prob = _gaba_prob_for_direction(direction_deg)
    ach_probs = np.full(n_syn, BASE_ACH_PROB, dtype=np.float64)
    gaba_probs = np.full(n_syn, gaba_prob, dtype=np.float64)

    rng = np.random.default_rng(seed + 1_000_003)
    ach_events = _rates_to_events(
        rates_hz=ach_rates,
        release_prob=ach_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )
    gaba_events = _rates_to_events(
        rates_hz=gaba_rates,
        release_prob=gaba_probs,
        rate_dt_ms=RATE_DT_MS,
        rng=rng,
    )

    def _queue() -> None:
        for i, nc in enumerate(bundle.ncs_ach):
            for t in ach_events[i]:
                if t < C24.TSTOP_MS:
                    nc.event(t)
        for i, nc in enumerate(bundle.ncs_gaba):
            for t in gaba_events[i]:
                if t < C24.TSTOP_MS:
                    nc.event(t)

    fih = h.FInitializeHandler(_queue)

    v_vec = h.Vector()
    t_vec = h.Vector()
    v_vec.record(cell.soma(0.5)._ref_v)
    t_vec.record(h._ref_t)

    h.celsius = C24.CELSIUS_DEG_C
    h.dt = C24.DT_MS
    h.steps_per_ms = C24.STEPS_PER_MS
    h.v_init = C24.V_INIT_MV
    h.tstop = C24.TSTOP_MS
    h.finitialize(C24.V_INIT_MV)
    _ = fih
    h.run()

    v = np.array(v_vec.to_python(), dtype=np.float64)
    t = np.array(t_vec.to_python(), dtype=np.float64)

    peak_v = float(v.max()) if v.size else float("nan")
    baseline_v = _baseline_v_mv(t_ms=t, v_mv=v)
    peak_minus_baseline = peak_v - baseline_v
    spike_count: int | None = (
        _count_spikes(v, C24.AP_THRESHOLD_MV) if key.mode == TrialMode.FULL else None
    )

    return TrialOutput(
        key=key,
        v_trace_mv=v,
        t_trace_ms=t,
        peak_v_mv=peak_v,
        baseline_v_mv=baseline_v,
        peak_minus_baseline_mv=peak_minus_baseline,
        spike_count=spike_count,
        n_samples=int(v.size),
    )


def _enumerate_trial_keys(*, n_trials_per_cell: int) -> list[TrialKey]:
    keys: list[TrialKey] = []
    for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE):
        for direction in (Condition.PD, Condition.ND):
            for trial_index in range(n_trials_per_cell):
                keys.append(TrialKey(mode=mode, direction=direction, trial_index=trial_index))
    return keys


def _append_trace_rows(
    *,
    csv_path: str,
    output: TrialOutput,
) -> None:
    """Append one trial's per-sample rows to the long-format CSV.

    Subsamples by ``CSV_SUBSAMPLE_STRIDE`` (default 10 → 1 ms resolution from
    the 0.1 ms simulation dt) so the committed CSV stays under the 5 MB
    pre-merge gate. Per-trial scalars (peak Vm, baseline Vm, spike count) are
    computed from the FULL trace before subsampling, so subsampling does not
    affect ``per_trial_metrics.json``.
    """
    with open(file=csv_path, mode="a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        t_sub = output.t_trace_ms[::CSV_SUBSAMPLE_STRIDE]
        v_sub = output.v_trace_mv[::CSV_SUBSAMPLE_STRIDE]
        for t_ms, v_mv in zip(t_sub, v_sub, strict=True):
            writer.writerow(
                [
                    output.key.mode.value,
                    output.key.direction.value,
                    output.key.trial_index,
                    f"{t_ms:.4f}",
                    f"{v_mv:.6f}",
                ]
            )


def _trial_metric_dict(*, output: TrialOutput) -> dict[str, Any]:
    return {
        "mode": output.key.mode.value,
        "direction": output.key.direction.value,
        "trial": output.key.trial_index,
        PEAK_V_MV_KEY: output.peak_v_mv,
        BASELINE_V_MV_KEY: output.baseline_v_mv,
        PEAK_MINUS_BASELINE_KEY: output.peak_minus_baseline_mv,
        SPIKE_COUNT_KEY: output.spike_count,
        N_SAMPLES_KEY: output.n_samples,
    }


def _compute_dsi_from_full_trials(*, trial_metrics: list[dict[str, Any]]) -> float:
    """Compute DSI = (R_PD - R_ND) / (R_PD + R_ND) from FULL-mode trial means."""
    pd_spikes = [
        d[SPIKE_COUNT_KEY]
        for d in trial_metrics
        if d["mode"] == TrialMode.FULL.value
        and d["direction"] == Condition.PD.value
        and d[SPIKE_COUNT_KEY] is not None
    ]
    nd_spikes = [
        d[SPIKE_COUNT_KEY]
        for d in trial_metrics
        if d["mode"] == TrialMode.FULL.value
        and d["direction"] == Condition.ND.value
        and d[SPIKE_COUNT_KEY] is not None
    ]
    pd_mean = float(np.mean(pd_spikes)) if len(pd_spikes) > 0 else 0.0
    nd_mean = float(np.mean(nd_spikes)) if len(nd_spikes) > 0 else 0.0
    denom = pd_mean + nd_mean
    if denom == 0.0:
        return 0.0
    return float((pd_mean - nd_mean) / denom)


def main() -> None:
    parser = argparse.ArgumentParser(description="t0066 EPSP/IPSP/FULL sweep on de Rosenroll DSGC")
    parser.add_argument(
        "--n-trials-per-cell",
        type=int,
        default=N_TRIALS_PER_CELL,
        help=f"Trials per (mode, direction) cell (default: {N_TRIALS_PER_CELL}).",
    )
    parser.add_argument(
        "--smoke",
        action="store_true",
        help="Smoke test: 1 trial per cell (6 trials total).",
    )
    args = parser.parse_args()
    n_trials_per_cell = 1 if args.smoke else int(args.n_trials_per_cell)

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    csv_path = str(VOLTAGE_TRACES_CSV)

    with open(file=csv_path, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)

    _ensure_neuron_loaded()
    keys = _enumerate_trial_keys(n_trials_per_cell=n_trials_per_cell)
    print(f"Total trials to run: {len(keys)} (n_trials_per_cell={n_trials_per_cell})")

    print("Building cell + synapses (one-shot)...")
    cell = build_dsgc_cell()
    bundle = _setup_synapses(cell=cell, gaba_weight_scale=1.0)
    state = _snapshot_canonical_state(cell=cell, bundle=bundle)
    print(
        f"Cell ready: {len(cell.terminal_dends)} terminal dendrites, "
        f"{len(bundle.ncs_ach)} ACh + {len(bundle.ncs_gaba)} GABA NetCons."
    )

    trial_metrics: list[dict[str, Any]] = []
    sweep_t0 = time.perf_counter()
    for trial_idx, key in enumerate(keys, start=1):
        t0 = time.perf_counter()
        output = _run_one_trial(cell=cell, bundle=bundle, state=state, key=key)
        dt_s = time.perf_counter() - t0
        _append_trace_rows(csv_path=csv_path, output=output)
        metric = _trial_metric_dict(output=output)
        trial_metrics.append(metric)
        spike_str = (
            f"spikes={output.spike_count}" if output.spike_count is not None else "spikes=n/a"
        )
        print(
            f"[{trial_idx:3d}/{len(keys)}] "
            f"{key.mode.value:13s} {key.direction.value} trial={key.trial_index:2d} "
            f"peak={output.peak_v_mv:+7.2f} mV  base={output.baseline_v_mv:+7.2f} mV  "
            f"{spike_str}  [{dt_s:5.1f}s]"
        )
        # Write per-trial metrics incrementally so a crash mid-sweep preserves data.
        with open(file=PER_TRIAL_METRICS_JSON, mode="w", encoding="utf-8") as f:
            json.dump({"trials": trial_metrics}, f, indent=2)

    sweep_dt = time.perf_counter() - sweep_t0
    dsi = _compute_dsi_from_full_trials(trial_metrics=trial_metrics)
    metrics_payload: dict[str, Any] = {METRIC_KEY_DSI: dsi}
    with open(file=METRICS_JSON, mode="w", encoding="utf-8") as f:
        json.dump(metrics_payload, f, indent=2)

    print(
        f"\nSweep complete: {len(keys)} trials in {sweep_dt:.1f}s "
        f"(mean {sweep_dt / len(keys):.2f}s/trial)"
    )
    print(f"FULL DSI = {dsi:.4f}")


if __name__ == "__main__":
    main()
