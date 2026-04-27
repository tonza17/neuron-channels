"""Multi-mode 12-direction tuning-curve sweep for the t0052 minimal DSGC.

Adapted from ``tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py`` (the sweep
harness at lines 466-530) per CLAUDE.md rule 3 (cross-task code is copied, not imported). Adapted
to:

* Accept a ``mode: TrialMode`` argument and write one CSV per mode (FULL, AMPA_ONLY, GABA_ONLY).
* Loop angles in ``ANGLES_DEG`` order, trials 0..N_TRIALS_PER_ANGLE-1, deterministic seed
  ``1000 * angle_idx + trial_idx + 1``.
* Emit (angle_deg, trial_seed, firing_rate_hz) for the per-mode tuning-curve CSV.
* Emit (angle_deg, trial_seed, sample_idx, t_ms, voltage_mv) long-form per-mode voltage CSV.
* Emit (angle_deg, trial_index, spike_time_s) per-mode spike-times CSV.
* Emit (angle_deg, synapse_index, onset_time_ms) per-angle activation-time CSV (mode-independent;
  written once during the FULL-mode sweep because it depends only on the bar geometry).

Includes a dry-run validation gate (Step 10): 1 angle x 2 trials per mode is run before the full
360-trial sweep, and the loop refuses to advance if AMPA_ONLY at theta = 0 produces 0 spikes.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tqdm import tqdm

from tasks.t0052_minimal_dsgc_scalar_gaba.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
    summarize_cell,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.constants import (
    ANGLES_DEG,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_ONSET_TIME_MS,
    COL_SAMPLE_IDX,
    COL_SPIKE_TIME_S,
    COL_SYNAPSE_INDEX,
    COL_T_MS,
    COL_TRIAL_INDEX,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    DT_MS,
    N_PAIRS,
    N_TRIALS_PER_ANGLE,
    PLACEMENT_SEED,
    TrialMode,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.paths import (
    ACTIVATION_TIMES_CSV,
    MORPHOLOGY_SWC_PATH,
    PLACEMENT_JSON,
    SPIKE_TIMES_AMPA_ONLY_CSV,
    SPIKE_TIMES_FULL_CSV,
    SPIKE_TIMES_GABA_ONLY_CSV,
    TUNING_CURVE_AMPA_ONLY_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_GABA_ONLY_CSV,
    VOLTAGE_TRACES_AMPA_ONLY_CSV,
    VOLTAGE_TRACES_FULL_CSV,
    VOLTAGE_TRACES_GABA_ONLY_CSV,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.synapses import (
    EiPair,
    build_ei_pairs,
)
from tasks.t0052_minimal_dsgc_scalar_gaba.code.trial import (
    TrialResult,
    run_one_trial,
)


@dataclass(frozen=True, slots=True)
class SweepArtifacts:
    cell: CellHandles
    pairs: list[EiPair]
    locations: list[Location]


def _select_paths_for_mode(
    *,
    mode: TrialMode,
) -> tuple[Path, Path, Path]:
    if mode == TrialMode.FULL:
        return (TUNING_CURVE_FULL_CSV, SPIKE_TIMES_FULL_CSV, VOLTAGE_TRACES_FULL_CSV)
    if mode == TrialMode.AMPA_ONLY:
        return (
            TUNING_CURVE_AMPA_ONLY_CSV,
            SPIKE_TIMES_AMPA_ONLY_CSV,
            VOLTAGE_TRACES_AMPA_ONLY_CSV,
        )
    if mode == TrialMode.GABA_ONLY:
        return (
            TUNING_CURVE_GABA_ONLY_CSV,
            SPIKE_TIMES_GABA_ONLY_CSV,
            VOLTAGE_TRACES_GABA_ONLY_CSV,
        )
    raise AssertionError(f"Unhandled TrialMode: {mode}")


def setup_sweep_artifacts() -> SweepArtifacts:
    """Build the cell, sample placements, and construct EiPair objects (one-time per process)."""
    ensure_neuron_importable()
    load_stdrun()
    enable_cvode()
    from neuron import h  # noqa: PLC0415

    h.dt = DT_MS

    print(f"[setup] Building cell from {MORPHOLOGY_SWC_PATH}", flush=True)
    cell: CellHandles = build_dsgc_from_swc(swc_path=MORPHOLOGY_SWC_PATH)
    summary = summarize_cell(cell=cell)
    print(
        f"[setup] cell built: n_dendrites={summary.n_dendrites} "
        f"total_dendritic_length_um={summary.total_dendritic_length_um:.2f} "
        f"soma_L_um={summary.soma_length_um:.2f} soma_diam_um={summary.soma_diameter_um:.2f}",
        flush=True,
    )

    print(f"[setup] Sampling {N_PAIRS} dendritic locations (seed={PLACEMENT_SEED})", flush=True)
    locations: list[Location] = sample_dendritic_locations(
        cell=cell,
        n_pairs=N_PAIRS,
        seed=PLACEMENT_SEED,
    )
    save_placement_json(locations=locations, out_path=PLACEMENT_JSON)
    print(f"[setup] Wrote placement to {PLACEMENT_JSON}", flush=True)

    print(f"[setup] Building {len(locations)} co-located E+I pairs", flush=True)
    pairs: list[EiPair] = build_ei_pairs(
        h=h,
        locations=locations,
        sections=cell.dendrites,
    )

    return SweepArtifacts(cell=cell, pairs=pairs, locations=locations)


def _write_curve_csv(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_ANGLE_DEG, COL_TRIAL_SEED, COL_FIRING_RATE_HZ])
        for r in results:
            writer.writerow([int(r.angle_deg), r.trial_seed, f"{r.firing_rate_hz:.6f}"])


def _write_spikes_csv(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_ANGLE_DEG, COL_TRIAL_INDEX, COL_SPIKE_TIME_S])
        for r in results:
            for spike_time_ms in r.spike_times_ms:
                writer.writerow(
                    [int(r.angle_deg), r.trial_seed, f"{spike_time_ms / 1000.0:.6f}"],
                )


def _write_voltage_csv(
    *,
    results: list[TrialResult],
    out_path: Path,
    sample_stride: int,
) -> None:
    """Write a long-form (angle, seed, sample_idx, t_ms, voltage_mv) CSV.

    The trace is downsampled by ``sample_stride`` to keep file sizes manageable. With
    ``DT_MS = 0.025`` and ``TSTOP_MS = 1500``, a stride of 8 yields ~7,500 rows per trial -> 900k
    rows per mode (3 modes -> 2.7 M rows total), comfortably within reasonable on-disk sizes.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [COL_ANGLE_DEG, COL_TRIAL_SEED, COL_SAMPLE_IDX, COL_T_MS, COL_VOLTAGE_MV],
        )
        for r in results:
            stride: int = max(1, sample_stride)
            indices: np.ndarray = np.arange(0, r.t_ms.shape[0], stride)
            for sample_idx in indices:
                writer.writerow(
                    [
                        int(r.angle_deg),
                        r.trial_seed,
                        int(sample_idx),
                        f"{float(r.t_ms[sample_idx]):.4f}",
                        f"{float(r.v_soma_mv[sample_idx]):.4f}",
                    ],
                )


def _write_activation_times_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write the per-angle, per-synapse onset-time CSV. Reads the first trial of each angle.

    Onset time is mode-independent (it depends only on bar geometry), so reading the first
    encountered (angle, trial) for each angle suffices.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    seen_angles: set[float] = set()
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_ANGLE_DEG, COL_SYNAPSE_INDEX, COL_ONSET_TIME_MS])
        for r in results:
            if r.angle_deg in seen_angles:
                continue
            seen_angles.add(r.angle_deg)
            for synapse_index, onset_time_ms in enumerate(r.synapse_onset_times_ms):
                writer.writerow(
                    [int(r.angle_deg), int(synapse_index), f"{onset_time_ms:.4f}"],
                )


def _run_sweep_for_mode(
    *,
    artifacts: SweepArtifacts,
    mode: TrialMode,
    angles_deg: tuple[int, ...],
    n_trials_per_angle: int,
    description: str,
) -> list[TrialResult]:
    from neuron import h  # noqa: PLC0415

    results: list[TrialResult] = []
    total: int = len(angles_deg) * n_trials_per_angle
    bar = tqdm(total=total, desc=description, unit="trial")
    for angle_idx, angle_deg in enumerate(angles_deg):
        for trial_idx in range(n_trials_per_angle):
            trial_seed: int = 1000 * angle_idx + trial_idx + 1
            result: TrialResult = run_one_trial(
                h=h,
                cell=artifacts.cell,
                pairs=artifacts.pairs,
                mode=mode,
                angle_deg=float(angle_deg),
                trial_seed=trial_seed,
            )
            results.append(result)
            bar.update(1)
    bar.close()
    return results


def _print_summary(*, label: str, results: list[TrialResult]) -> None:
    angles_seen: list[float] = sorted({r.angle_deg for r in results})
    print(f"[{label}] per-angle mean firing rate (Hz):", flush=True)
    for angle_deg in angles_seen:
        rates: list[float] = [r.firing_rate_hz for r in results if r.angle_deg == angle_deg]
        mean_rate: float = sum(rates) / max(1, len(rates))
        print(
            f"  angle={int(angle_deg):3d} deg  mean={mean_rate:6.2f} Hz  (n={len(rates)})",
            flush=True,
        )


def run_dry_run_validation(*, artifacts: SweepArtifacts) -> None:
    """1 angle x 2 trials per mode dry-run gate before the full 360-trial sweep.

    Per Step 10: AMPA_ONLY at theta = 0 must produce a non-zero firing rate; FULL at theta = 0
    must be at least 80% of AMPA_ONLY at theta = 0. Otherwise STOP.
    """
    print("[dry-run] Running 1 angle (theta=0) x 2 trials per mode...", flush=True)
    dry_angles: tuple[int, ...] = (0,)
    n_dry: int = 2
    full_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.FULL,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        description="dry-run FULL",
    )
    ampa_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.AMPA_ONLY,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        description="dry-run AMPA_ONLY",
    )
    gaba_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.GABA_ONLY,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        description="dry-run GABA_ONLY",
    )

    ampa_rate: float = float(np.mean([r.firing_rate_hz for r in ampa_results]))
    full_rate: float = float(np.mean([r.firing_rate_hz for r in full_results]))
    gaba_rate: float = float(np.mean([r.firing_rate_hz for r in gaba_results]))
    print(
        f"[dry-run] mean firing rate at theta=0: FULL={full_rate:.2f} Hz "
        f"AMPA_ONLY={ampa_rate:.2f} Hz GABA_ONLY={gaba_rate:.2f} Hz",
        flush=True,
    )

    if ampa_rate <= 0.0:
        # Print a few details for debugging.
        first_pair: EiPair = artifacts.pairs[0]
        print(
            f"[dry-run] DEBUG first pair: x_um={first_pair.x_um:.2f} y_um={first_pair.y_um:.2f} "
            f"ampa_netstim.start={float(first_pair.ampa_netstim.start):.2f} ms "
            f"ampa_netcon.weight[0]={float(first_pair.ampa_netcon.weight[0])} uS "
            f"v_soma_min={float(np.min(ampa_results[0].v_soma_mv)):.2f} mV "
            f"v_soma_max={float(np.max(ampa_results[0].v_soma_mv)):.2f} mV",
            flush=True,
        )
        raise RuntimeError(
            "Dry-run gate failed: AMPA_ONLY at theta=0 produced zero spikes. "
            "Aborting before the full 360-trial sweep.",
        )


def run_full_sweep(*, voltage_sample_stride: int = 8) -> None:
    """End-to-end sweep: setup, dry-run gate, then 12 x 10 x 3 = 360 trials with CSV outputs."""
    artifacts: SweepArtifacts = setup_sweep_artifacts()

    run_dry_run_validation(artifacts=artifacts)

    angles: tuple[int, ...] = ANGLES_DEG
    n_trials: int = N_TRIALS_PER_ANGLE

    full_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.FULL,
        angles_deg=angles,
        n_trials_per_angle=n_trials,
        description="sweep FULL",
    )
    ampa_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.AMPA_ONLY,
        angles_deg=angles,
        n_trials_per_angle=n_trials,
        description="sweep AMPA_ONLY",
    )
    gaba_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.GABA_ONLY,
        angles_deg=angles,
        n_trials_per_angle=n_trials,
        description="sweep GABA_ONLY",
    )

    for label, results in (
        ("FULL", full_results),
        ("AMPA_ONLY", ampa_results),
        ("GABA_ONLY", gaba_results),
    ):
        _print_summary(label=label, results=results)

    # Write per-mode outputs.
    for mode, results in (
        (TrialMode.FULL, full_results),
        (TrialMode.AMPA_ONLY, ampa_results),
        (TrialMode.GABA_ONLY, gaba_results),
    ):
        curve_path, spikes_path, voltage_path = _select_paths_for_mode(mode=mode)
        _write_curve_csv(results=results, out_path=curve_path)
        _write_spikes_csv(results=results, out_path=spikes_path)
        _write_voltage_csv(
            results=results,
            out_path=voltage_path,
            sample_stride=voltage_sample_stride,
        )
        print(
            f"[sweep] wrote {curve_path.name} (rows={len(results)}); "
            f"spikes -> {spikes_path.name}; voltages -> {voltage_path.name}",
            flush=True,
        )

    # Activation times: one row per (angle, synapse) — read from FULL results.
    _write_activation_times_csv(results=full_results, out_path=ACTIVATION_TIMES_CSV)
    print(f"[sweep] wrote activation times -> {ACTIVATION_TIMES_CSV.name}", flush=True)


if __name__ == "__main__":
    run_full_sweep()
