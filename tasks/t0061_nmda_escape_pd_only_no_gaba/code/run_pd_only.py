"""t0061 — NMDA-only PD diagnostic; mirror of t0060 with AMPA replaced by Mg-block NMDA."""

from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    AP_THRESHOLD_MV,
    BAR_VELOCITY_UM_PER_MS,
    BASE_OFFSET_MS,
    DT_MS,
    N_PAIRS,
    PLACEMENT_SEED,
    TSTOP_MS,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)
from tasks.t0061_nmda_escape_pd_only_no_gaba.code.constants import (
    ANGLE_DEG,
    GNMDA_NS_VALUES,
    N_TRIALS,
)
from tasks.t0061_nmda_escape_pd_only_no_gaba.code.nmda_bootstrap import (
    ensure_nmda_compiled,
    get_h,
)
from tasks.t0061_nmda_escape_pd_only_no_gaba.code.nmda_synapse import (
    NmdaPair,
    build_nmda_pairs,
    schedule_nmda_onsets,
)
from tasks.t0061_nmda_escape_pd_only_no_gaba.code.paths import (
    PLACEMENT_JSON,
    RESULTS_DIR,
    SUMMARY_CSV,
    VOLTAGE_TRACES_CSV,
    WALLCLOCK_JSON,
)


@dataclass(frozen=True, slots=True)
class HhSnapshot:
    soma_gnabar: list[float]
    soma_gkbar: list[float]
    ais_gnabar: list[float]
    ais_gkbar: list[float]


@dataclass(frozen=True, slots=True)
class TrialResult:
    gnmda_ns: float
    mode: TrialMode
    t_ms: np.ndarray
    v_soma_mv: np.ndarray
    n_spikes: int


def _save_and_zero_hh(*, cell: CellHandles) -> HhSnapshot:
    soma_gnabar: list[float] = []
    soma_gkbar: list[float] = []
    for seg in cell.soma:
        soma_gnabar.append(float(seg.hh.gnabar))
        soma_gkbar.append(float(seg.hh.gkbar))
        seg.hh.gnabar = 0.0
        seg.hh.gkbar = 0.0
    ais_gnabar: list[float] = []
    ais_gkbar: list[float] = []
    for seg in cell.axon_initial_segment:
        ais_gnabar.append(float(seg.hh.gnabar))
        ais_gkbar.append(float(seg.hh.gkbar))
        seg.hh.gnabar = 0.0
        seg.hh.gkbar = 0.0
    return HhSnapshot(
        soma_gnabar=soma_gnabar,
        soma_gkbar=soma_gkbar,
        ais_gnabar=ais_gnabar,
        ais_gkbar=ais_gkbar,
    )


def _restore_hh(*, cell: CellHandles, snapshot: HhSnapshot) -> None:
    for seg, gnabar, gkbar in zip(
        cell.soma,
        snapshot.soma_gnabar,
        snapshot.soma_gkbar,
        strict=True,
    ):
        seg.hh.gnabar = gnabar
        seg.hh.gkbar = gkbar
    for seg, gnabar, gkbar in zip(
        cell.axon_initial_segment,
        snapshot.ais_gnabar,
        snapshot.ais_gkbar,
        strict=True,
    ):
        seg.hh.gnabar = gnabar
        seg.hh.gkbar = gkbar


def _setup() -> tuple[Any, CellHandles, list[NmdaPair]]:
    ensure_neuron_importable()
    load_stdrun()
    ensure_nmda_compiled()
    enable_cvode()
    h: Any = get_h()
    h.dt = DT_MS

    print(f"[t0061] Building cell from {MORPHOLOGY_SWC_PATH}", flush=True)
    cell: CellHandles = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)

    print(f"[t0061] Sampling {N_PAIRS} dendritic locations (seed={PLACEMENT_SEED})", flush=True)
    locations: list[Location] = sample_dendritic_locations(
        cell=cell,
        n_pairs=N_PAIRS,
        seed=PLACEMENT_SEED,
    )
    PLACEMENT_JSON.parent.mkdir(parents=True, exist_ok=True)
    save_placement_json(locations=locations, out_path=PLACEMENT_JSON)
    print(f"[t0061] Wrote placement to {PLACEMENT_JSON}", flush=True)

    pairs: list[NmdaPair] = build_nmda_pairs(
        h=h,
        locations=locations,
        sections=cell.dendrites,
        soma_origin_um=cell.soma_origin_um,
    )
    print(f"[t0061] Built {len(pairs)} NMDA-only synapses", flush=True)
    return h, cell, pairs


def _run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    pairs: list[NmdaPair],
    mode: TrialMode,
    angle_deg: float,
    gnmda_ns: float,
) -> TrialResult:
    schedule_nmda_onsets(
        pairs=pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        base_offset_ms=BASE_OFFSET_MS,
        gnmda_ns=gnmda_ns,
    )

    v_rec: Any = h.Vector()
    v_rec.record(cell.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)
    spike_vec: Any = h.Vector()
    netcon: Any = h.NetCon(cell.soma(0.5)._ref_v, None, sec=cell.soma)
    netcon.threshold = AP_THRESHOLD_MV
    netcon.record(spike_vec)

    snapshot: HhSnapshot | None = None
    try:
        if mode in {TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE}:
            snapshot = _save_and_zero_hh(cell=cell)
        h.finitialize(V_INIT_MV)
        h.continuerun(TSTOP_MS)
    finally:
        if snapshot is not None:
            _restore_hh(cell=cell, snapshot=snapshot)

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    n_spikes: int = len(list(spike_vec))
    return TrialResult(
        gnmda_ns=gnmda_ns,
        mode=mode,
        t_ms=t_arr,
        v_soma_mv=v_arr,
        n_spikes=n_spikes,
    )


def _write_voltage_traces_csv(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["gnmda_ns", "mode", "sample_idx", "t_ms", "v_soma_mv"])
        for r in results:
            for i in range(len(r.t_ms)):
                writer.writerow(
                    [
                        f"{r.gnmda_ns:.6f}",
                        r.mode.value,
                        i,
                        f"{float(r.t_ms[i]):.4f}",
                        f"{float(r.v_soma_mv[i]):.6f}",
                    ],
                )


def _write_summary_csv(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "gnmda_ns",
                "mode",
                "peak_vm_mv",
                "min_vm_mv",
                "n_spikes",
                "n_samples",
            ],
        )
        for r in results:
            writer.writerow(
                [
                    f"{r.gnmda_ns:.6f}",
                    r.mode.value,
                    f"{float(np.max(r.v_soma_mv)):.6f}",
                    f"{float(np.min(r.v_soma_mv)):.6f}",
                    r.n_spikes,
                    len(r.t_ms),
                ],
            )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    h, cell, pairs = _setup()

    print(
        f"[t0061] Running {len(GNMDA_NS_VALUES)} gNMDA x 2 modes x {N_TRIALS} trial = "
        f"{len(GNMDA_NS_VALUES) * 2 * N_TRIALS} trials at theta = {ANGLE_DEG} deg, GABA = 0, "
        f"AMPA = 0 (NMDA-only)",
        flush=True,
    )

    sweep_t0: float = time.perf_counter()
    results: list[TrialResult] = []
    for gnmda_ns in GNMDA_NS_VALUES:
        for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE):
            for trial_idx in range(N_TRIALS):
                _ = trial_idx
                trial_t0: float = time.perf_counter()
                r: TrialResult = _run_one_trial(
                    h=h,
                    cell=cell,
                    pairs=pairs,
                    mode=mode,
                    angle_deg=float(ANGLE_DEG),
                    gnmda_ns=gnmda_ns,
                )
                trial_dt: float = time.perf_counter() - trial_t0
                results.append(r)
                print(
                    f"[t0061] gnmda={gnmda_ns:.2f} nS  mode={mode.value:13s}  "
                    f"peak_vm={float(np.max(r.v_soma_mv)):6.2f} mV  "
                    f"n_spikes={r.n_spikes:2d}  dt={trial_dt:.2f} s",
                    flush=True,
                )

    sweep_wallclock_s: float = time.perf_counter() - sweep_t0

    _write_voltage_traces_csv(results=results, out_path=VOLTAGE_TRACES_CSV)
    _write_summary_csv(results=results, out_path=SUMMARY_CSV)

    WALLCLOCK_JSON.write_text(
        json.dumps(
            {
                "wallclock_seconds": sweep_wallclock_s,
                "n_trials": len(results),
                "tstop_ms": TSTOP_MS,
                "gnmda_ns_values": list(GNMDA_NS_VALUES),
                "gaba_base_ns": 0.0,
                "ampa_peak_ns": 0.0,
                "angle_deg": ANGLE_DEG,
                "n_trials_per_condition": N_TRIALS,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"[t0061] Done. wall-clock = {sweep_wallclock_s:.2f} s.",
        flush=True,
    )


if __name__ == "__main__":
    main()
