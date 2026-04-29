"""t0063 — HH voltage-step diagnostic. SEClamp on soma, no synapses."""

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
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import TrialMode
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0063_hh_voltage_step_test.code.constants import (
    DT_MS,
    DUR1_MS,
    DUR2_MS,
    DUR3_MS,
    HOLD_MV,
    RS_MOHM,
    TARGET_MV_VALUES,
    TSTOP_MS,
)
from tasks.t0063_hh_voltage_step_test.code.paths import (
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
    target_mv: float
    mode: TrialMode
    t_ms: np.ndarray
    v_soma_mv: np.ndarray
    i_clamp_na: np.ndarray


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
    print(f"[t0063] Building cell from {MORPHOLOGY_SWC_PATH}", flush=True)
    cell: CellHandles = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)
    return h, cell


def _run_one_trial(
    *,
    h: Any,
    cell: CellHandles,
    mode: TrialMode,
    target_mv: float,
) -> TrialResult:
    seclamp: Any = h.SEClamp(cell.soma(0.5))
    seclamp.dur1 = DUR1_MS
    seclamp.amp1 = HOLD_MV
    seclamp.dur2 = DUR2_MS
    seclamp.amp2 = target_mv
    seclamp.dur3 = DUR3_MS
    seclamp.amp3 = HOLD_MV
    seclamp.rs = RS_MOHM

    v_rec: Any = h.Vector()
    v_rec.record(cell.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)
    i_rec: Any = h.Vector()
    i_rec.record(seclamp._ref_i)

    snapshot: HhSnapshot | None = None
    try:
        if mode == TrialMode.EPSP_PASSIVE:
            snapshot = _save_and_zero_hh(cell=cell)
        h.finitialize(HOLD_MV)
        h.continuerun(TSTOP_MS)
    finally:
        if snapshot is not None:
            _restore_hh(cell=cell, snapshot=snapshot)

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    i_arr: np.ndarray = np.array(list(i_rec), dtype=np.float64)
    return TrialResult(
        target_mv=target_mv,
        mode=mode,
        t_ms=t_arr,
        v_soma_mv=v_arr,
        i_clamp_na=i_arr,
    )


def _write_traces(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["target_mv", "mode", "sample_idx", "t_ms", "v_soma_mv", "i_clamp_na"])
        for r in results:
            for i in range(len(r.t_ms)):
                writer.writerow(
                    [
                        f"{r.target_mv:.2f}",
                        r.mode.value,
                        i,
                        f"{float(r.t_ms[i]):.4f}",
                        f"{float(r.v_soma_mv[i]):.6f}",
                        f"{float(r.i_clamp_na[i]):.6f}",
                    ],
                )


def _write_summary(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "target_mv",
                "mode",
                "step_steady_vm_mv",
                "step_peak_inward_i_na",
                "step_steady_i_na",
                "n_samples",
            ],
        )
        # Sample the steady-state at t = DUR1 + DUR2 - 1 ms (just before step ends).
        t_step_steady: float = DUR1_MS + DUR2_MS - 1.0
        # Look for peak inward (most negative) clamp current during the step.
        t_step_start: float = DUR1_MS
        t_step_end: float = DUR1_MS + DUR2_MS
        for r in results:
            mask: np.ndarray = (r.t_ms >= t_step_start) & (r.t_ms <= t_step_end)
            i_during_step: np.ndarray = r.i_clamp_na[mask]
            v_during_step: np.ndarray = r.v_soma_mv[mask]
            steady_idx: int = int(np.argmin(np.abs(r.t_ms - t_step_steady)))
            writer.writerow(
                [
                    f"{r.target_mv:.2f}",
                    r.mode.value,
                    f"{float(r.v_soma_mv[steady_idx]):.6f}",
                    f"{float(np.min(i_during_step)):.6f}",
                    f"{float(np.mean(i_during_step[-50:])):.6f}",
                    len(r.t_ms),
                ],
            )
            _ = v_during_step  # not directly emitted but kept for readability


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    h, cell = _setup()

    print(
        f"[t0063] Running {len(TARGET_MV_VALUES)} target voltages x 2 modes = "
        f"{len(TARGET_MV_VALUES) * 2} trials",
        flush=True,
    )
    sweep_t0: float = time.perf_counter()
    results: list[TrialResult] = []
    for target_mv in TARGET_MV_VALUES:
        for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE):
            trial_t0: float = time.perf_counter()
            r: TrialResult = _run_one_trial(
                h=h,
                cell=cell,
                mode=mode,
                target_mv=target_mv,
            )
            trial_dt: float = time.perf_counter() - trial_t0
            results.append(r)
            print(
                f"[t0063] target={target_mv:6.1f} mV  mode={mode.value:13s}  "
                f"peak_iclamp={float(np.min(r.i_clamp_na)):8.3f} nA  "
                f"steady_iclamp={float(np.mean(r.i_clamp_na[-200:])):8.3f} nA  "
                f"dt={trial_dt:.2f} s",
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
                "target_mv_values": list(TARGET_MV_VALUES),
                "hold_mv": HOLD_MV,
                "dur1_ms": DUR1_MS,
                "dur2_ms": DUR2_MS,
                "dur3_ms": DUR3_MS,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(f"[t0063] Done. wall-clock = {sweep_wallclock_s:.2f} s.", flush=True)


if __name__ == "__main__":
    main()
