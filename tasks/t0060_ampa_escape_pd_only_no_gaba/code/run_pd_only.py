"""t0060 — quick AMPA-escape diagnostic at PD only with GABA = 0.

Imports the t0059 minimal_dsgc_bar_locked_gaba_ampa_sweep library primitives via the registered
library asset's module paths, runs 8 gAMPA values x 2 modes x 1 trial at theta = 0 deg, and
writes a flat CSV of soma V(t) plus a JSON summary. Does NOT touch the t0059 task folder.
"""

from __future__ import annotations

import csv
import json
import time
from pathlib import Path
from typing import Any

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    DT_MS,
    N_PAIRS,
    PLACEMENT_SEED,
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.neuron_bootstrap import (
    enable_cvode,
    ensure_gaba_tonic_compiled,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import MORPHOLOGY_SWC_PATH
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.synapses import (
    EiPair,
    build_ei_pairs,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.trial import (
    TrialResult,
    run_one_trial,
)
from tasks.t0060_ampa_escape_pd_only_no_gaba.code.constants import (
    ANGLE_DEG,
    GABA_BASE_NS,
    GAMPA_NS_VALUES,
    N_TRIALS,
)
from tasks.t0060_ampa_escape_pd_only_no_gaba.code.paths import (
    PLACEMENT_JSON,
    RESULTS_DIR,
    SUMMARY_CSV,
    VOLTAGE_TRACES_CSV,
    WALLCLOCK_JSON,
)


def _setup_cell_and_pairs() -> tuple[Any, CellHandles, list[EiPair]]:
    """Bootstrap NEURON + build cell + sample placement + build pairs.

    Equivalent to t0059's setup_sweep_artifacts but writes the placement JSON to t0060's
    results dir (not t0059's). The placement seed (= 0) is the same as t0059's so the
    sampled locations are bit-identical.
    """
    ensure_neuron_importable()
    load_stdrun()
    ensure_gaba_tonic_compiled()
    enable_cvode()
    from neuron import h  # noqa: PLC0415

    h.dt = DT_MS

    print(f"[t0060] Building cell from {MORPHOLOGY_SWC_PATH}", flush=True)
    cell: CellHandles = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)

    print(f"[t0060] Sampling {N_PAIRS} dendritic locations (seed={PLACEMENT_SEED})", flush=True)
    locations: list[Location] = sample_dendritic_locations(
        cell=cell,
        n_pairs=N_PAIRS,
        seed=PLACEMENT_SEED,
    )
    PLACEMENT_JSON.parent.mkdir(parents=True, exist_ok=True)
    save_placement_json(locations=locations, out_path=PLACEMENT_JSON)
    print(f"[t0060] Wrote placement to {PLACEMENT_JSON}", flush=True)

    pairs: list[EiPair] = build_ei_pairs(
        h=h,
        locations=locations,
        sections=cell.dendrites,
        soma_origin_um=cell.soma_origin_um,
    )
    return h, cell, pairs


def _write_voltage_traces_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write a long-format CSV: one row per (gampa, mode, sample_idx) with t_ms, v_mv."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["gampa_ns", "mode", "sample_idx", "t_ms", "v_soma_mv"])
        for r in results:
            t_arr: np.ndarray = r.t_ms
            v_arr: np.ndarray = r.v_soma_mv
            n: int = len(t_arr)
            for i in range(n):
                writer.writerow(
                    [
                        f"{r.gampa_ns:.6f}",
                        r.mode.value,
                        i,
                        f"{float(t_arr[i]):.4f}",
                        f"{float(v_arr[i]):.6f}",
                    ],
                )


def _write_summary_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Per-(gampa, mode) summary: peak Vm, spike count (FULL only), final Vm."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                "gampa_ns",
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
                    f"{r.gampa_ns:.6f}",
                    r.mode.value,
                    f"{float(np.max(r.v_soma_mv)):.6f}",
                    f"{float(np.min(r.v_soma_mv)):.6f}",
                    len(r.spike_times_ms),
                    len(r.t_ms),
                ],
            )


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    h, cell, pairs = _setup_cell_and_pairs()

    print(
        f"[t0060] Running {len(GAMPA_NS_VALUES)} gAMPA x 2 modes x {N_TRIALS} trial = "
        f"{len(GAMPA_NS_VALUES) * 2 * N_TRIALS} trials at theta = {ANGLE_DEG} deg, GABA = "
        f"{GABA_BASE_NS} nS",
        flush=True,
    )

    sweep_t0: float = time.perf_counter()
    results: list[TrialResult] = []
    for gampa_ns in GAMPA_NS_VALUES:
        for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE):
            for trial_idx in range(N_TRIALS):
                trial_t0: float = time.perf_counter()
                r: TrialResult = run_one_trial(
                    h=h,
                    cell=cell,
                    pairs=pairs,
                    mode=mode,
                    angle_deg=float(ANGLE_DEG),
                    trial_seed=trial_idx,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=GABA_BASE_NS,
                )
                trial_dt: float = time.perf_counter() - trial_t0
                results.append(r)
                print(
                    f"[t0060] gampa={gampa_ns:.2f} nS  mode={mode.value:13s}  "
                    f"trial={trial_idx}  peak_vm={float(np.max(r.v_soma_mv)):6.2f} mV  "
                    f"n_spikes={len(r.spike_times_ms):2d}  dt={trial_dt:.2f} s",
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
                "tstop_ms": 1400.0,
                "gampa_ns_values": list(GAMPA_NS_VALUES),
                "gaba_base_ns": GABA_BASE_NS,
                "angle_deg": ANGLE_DEG,
                "n_trials_per_condition": N_TRIALS,
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"[t0060] Done. wall-clock = {sweep_wallclock_s:.2f} s. Wrote "
        f"{VOLTAGE_TRACES_CSV.name}, {SUMMARY_CSV.name}, {WALLCLOCK_JSON.name}.",
        flush=True,
    )


if __name__ == "__main__":
    main()
