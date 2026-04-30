"""t0064 — HH current-step diagnostic. IClamp on soma, no synapses."""

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
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0064_hh_current_step_test.code.constants import (
    CURRENT_NA_VALUES,
    DELAY_MS,
    DT_MS,
    DURATION_MS,
    TSTOP_MS,
    V_REST_MV,
)
from tasks.t0064_hh_current_step_test.code.paths import (
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
    current_na: float
    mode: TrialMode
    t_ms: np.ndarray
    v_soma_mv: np.ndarray
    spike_times_ms: list[float]


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


def _setup() -> tuple[Any, CellHandles]:
    ensure_neuron_importable()
    load_stdrun()
    enable_cvode()
    from neuron import h  # noqa: PLC0415

    h.dt = DT_MS
    print(f"[t0064] Building cell from {MORPHOLOGY_SWC_PATH}", flush=True)
    cell: CellHandles = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)
    return h, cell


def _run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    mode: TrialMode,
    current_na: float,
) -> TrialResult:
    iclamp: Any = h.IClamp(cell.soma(0.5))
    iclamp.delay = DELAY_MS
    iclamp.dur = DURATION_MS
    iclamp.amp = current_na  # NEURON IClamp.amp is in nA

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
        if mode == TrialMode.EPSP_PASSIVE:
            snapshot = _save_and_zero_hh(cell=cell)
        h.finitialize(V_REST_MV)
        h.continuerun(TSTOP_MS)
    finally:
        if snapshot is not None:
            _restore_hh(cell=cell, snapshot=snapshot)

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    spike_times_ms: list[float] = [float(s) for s in spike_vec]
    return TrialResult(
        current_na=current_na,
        mode=mode,
        t_ms=t_arr,
        v_soma_mv=v_arr,
        spike_times_ms=spike_times_ms,
    )


def _write_traces(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["current_na", "mode", "sample_idx", "t_ms", "v_soma_mv"])
        for r in results:
            for i in range(len(r.t_ms)):
                writer.writerow(
                    [
                        f"{r.current_na:.6f}",
                        r.mode.value,
                        i,
                        f"{float(r.t_ms[i]):.4f}",
                        f"{float(r.v_soma_mv[i]):.6f}",
                    ],
                )


def _write_summary(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            ["current_na", "mode", "peak_vm_mv", "min_vm_mv", "n_spikes", "n_samples"],
        )
        for r in results:
            writer.writerow(
                [
                    f"{r.current_na:.6f}",
                    r.mode.value,
                    f"{float(np.max(r.v_soma_mv)):.6f}",
                    f"{float(np.min(r.v_soma_mv)):.6f}",
                    len(r.spike_times_ms),
                    len(r.t_ms),
                ],
            )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    h, cell = _setup()

    print(
        f"[t0064] Running {len(CURRENT_NA_VALUES)} currents x 2 modes = "
        f"{len(CURRENT_NA_VALUES) * 2} trials",
        flush=True,
    )
    sweep_t0: float = time.perf_counter()
    results: list[TrialResult] = []
    for current_na in CURRENT_NA_VALUES:
        for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE):
            trial_t0: float = time.perf_counter()
            r: TrialResult = _run_one_trial(
                h=h,
                cell=cell,
                mode=mode,
                current_na=current_na,
            )
            trial_dt: float = time.perf_counter() - trial_t0
            results.append(r)
            print(
                f"[t0064] I={current_na:.2f} nA  mode={mode.value:13s}  "
                f"peak_vm={float(np.max(r.v_soma_mv)):6.2f} mV  "
                f"n_spikes={len(r.spike_times_ms):2d}  dt={trial_dt:.2f} s",
                flush=True,
            )

    sweep_wallclock_s: float = time.perf_counter() - sweep_t0
    _write_traces(results=results, out_path=VOLTAGE_TRACES_CSV)
    _write_summary(results=results, out_path=SUMMARY_CSV)
    WALLCLOCK_JSON.write_text(
        json.dumps(
            {
                "wallclock_seconds": sweep_wallclock_s,
                "n_trials": len(results),
                "tstop_ms": TSTOP_MS,
                "current_na_values": list(CURRENT_NA_VALUES),
                "delay_ms": DELAY_MS,
                "duration_ms": DURATION_MS,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[t0064] Done. wall-clock = {sweep_wallclock_s:.2f} s.", flush=True)


if __name__ == "__main__":
    main()
