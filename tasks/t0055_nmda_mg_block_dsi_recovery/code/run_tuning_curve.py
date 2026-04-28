"""Multi-mode 12-direction tuning-curve sweep with gNMDA outer loop for t0055 minimal DSGC.

Adapted from ``tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/code/run_tuning_curve.py`` with
import-path rewrite and a single new bootstrap call:
``ensure_nmda_mg_block_compiled()`` is invoked AFTER ``ensure_neuron_importable()`` and
``load_stdrun()`` and BEFORE any ``h.NMDA_MgBlock(seg)`` construction. This guarantees the MOD is
built and registered before the synapse builder runs.

The sweep loop, per-trial seed formula (``1000 * angle_idx + trial_idx + 1``), CSV schema, and
dry-run validation gate are unchanged from t0054. Total: 4 gNMDA x 12 angles x 10 trials x 3
modes = 1,440 trials. Each per-mode CSV ends up with 4 x 12 x 10 = 480 rows.
"""

from __future__ import annotations

import csv
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tqdm import tqdm

from tasks.t0055_nmda_mg_block_dsi_recovery.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
    summarize_cell,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.constants import (
    ANGLES_DEG,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_GNMDA_NS,
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
    NMDA_PEAK_NS_VALUES,
    PLACEMENT_SEED,
    TrialMode,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    ensure_nmda_mg_block_compiled,
    load_stdrun,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.paths import (
    ACTIVATION_TIMES_CSV,
    MORPHOLOGY_SWC_PATH,
    PLACEMENT_JSON,
    SPIKE_TIMES_E_ONLY_CSV,
    SPIKE_TIMES_FULL_CSV,
    SPIKE_TIMES_GABA_ONLY_CSV,
    TUNING_CURVE_E_ONLY_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_GABA_ONLY_CSV,
    VOLTAGE_TRACES_E_ONLY_CSV,
    VOLTAGE_TRACES_FULL_CSV,
    VOLTAGE_TRACES_GABA_ONLY_CSV,
    WALLCLOCK_JSON,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.synapses import (
    EiPair,
    build_ei_pairs,
)
from tasks.t0055_nmda_mg_block_dsi_recovery.code.trial import (
    TrialResult,
    run_one_trial,
)


@dataclass(frozen=True, slots=True)
class SweepArtifacts:
    cell: CellHandles
    pairs: list[EiPair]
    locations: list[Location]


@dataclass(frozen=True, slots=True)
class ModeOutputPaths:
    curve: Path
    spikes: Path
    voltages: Path


def _select_paths_for_mode(*, mode: TrialMode) -> ModeOutputPaths:
    if mode == TrialMode.FULL:
        return ModeOutputPaths(
            curve=TUNING_CURVE_FULL_CSV,
            spikes=SPIKE_TIMES_FULL_CSV,
            voltages=VOLTAGE_TRACES_FULL_CSV,
        )
    if mode == TrialMode.E_ONLY:
        return ModeOutputPaths(
            curve=TUNING_CURVE_E_ONLY_CSV,
            spikes=SPIKE_TIMES_E_ONLY_CSV,
            voltages=VOLTAGE_TRACES_E_ONLY_CSV,
        )
    if mode == TrialMode.GABA_ONLY:
        return ModeOutputPaths(
            curve=TUNING_CURVE_GABA_ONLY_CSV,
            spikes=SPIKE_TIMES_GABA_ONLY_CSV,
            voltages=VOLTAGE_TRACES_GABA_ONLY_CSV,
        )
    raise AssertionError(f"Unhandled TrialMode: {mode}")


def setup_sweep_artifacts() -> SweepArtifacts:
    """Build the cell, sample placements, and construct EiPair objects (one-time per process).

    This invokes ``ensure_nmda_mg_block_compiled()`` after ``load_stdrun`` so that the
    ``NMDA_MgBlock`` POINT_PROCESS is registered with NEURON before ``build_ei_pairs`` constructs
    any ``h.NMDA_MgBlock(seg)`` handles.
    """
    ensure_neuron_importable()
    load_stdrun()
    ensure_nmda_mg_block_compiled()
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

    print(f"[setup] Building {len(locations)} co-located E+I+NMDA pairs", flush=True)
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
        writer.writerow([COL_GNMDA_NS, COL_ANGLE_DEG, COL_TRIAL_SEED, COL_FIRING_RATE_HZ])
        for r in results:
            writer.writerow(
                [
                    f"{r.gnmda_ns:.6f}",
                    int(r.angle_deg),
                    r.trial_seed,
                    f"{r.firing_rate_hz:.6f}",
                ],
            )


def _write_spikes_csv(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_GNMDA_NS, COL_ANGLE_DEG, COL_TRIAL_INDEX, COL_SPIKE_TIME_S])
        for r in results:
            for spike_time_ms in r.spike_times_ms:
                writer.writerow(
                    [
                        f"{r.gnmda_ns:.6f}",
                        int(r.angle_deg),
                        r.trial_seed,
                        f"{spike_time_ms / 1000.0:.6f}",
                    ],
                )


def _write_voltage_csv(
    *,
    results: list[TrialResult],
    out_path: Path,
    sample_stride: int,
) -> None:
    """Write a long-form (gnmda_ns, angle, seed, sample_idx, t_ms, voltage_mv) CSV.

    The trace is downsampled by ``sample_stride`` to keep file sizes manageable. With
    ``DT_MS = 0.025`` and ``TSTOP_MS = 1500``, a stride of 8 yields ~7,500 rows per trial -> 480
    trials per mode -> ~3.6 M rows per mode (3 modes -> ~10.8 M rows total), comfortably within
    on-disk limits.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_GNMDA_NS,
                COL_ANGLE_DEG,
                COL_TRIAL_SEED,
                COL_SAMPLE_IDX,
                COL_T_MS,
                COL_VOLTAGE_MV,
            ],
        )
        for r in results:
            stride: int = max(1, sample_stride)
            indices: np.ndarray = np.arange(0, r.t_ms.shape[0], stride)
            for sample_idx in indices:
                writer.writerow(
                    [
                        f"{r.gnmda_ns:.6f}",
                        int(r.angle_deg),
                        r.trial_seed,
                        int(sample_idx),
                        f"{float(r.t_ms[sample_idx]):.4f}",
                        f"{float(r.v_soma_mv[sample_idx]):.4f}",
                    ],
                )


def _write_activation_times_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write the per-(gnmda, angle, synapse) onset-time CSV.

    Onset time is mode-independent and gnmda-independent (it depends only on bar geometry).
    However, we still emit one row per (gnmda_ns, angle, synapse) so downstream analysis can
    group by gnmda_ns symmetrically with the other CSVs. The first encountered (angle, trial)
    for each (gnmda_ns, angle) pair is used.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    seen_keys: set[tuple[float, float]] = set()
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_GNMDA_NS, COL_ANGLE_DEG, COL_SYNAPSE_INDEX, COL_ONSET_TIME_MS])
        for r in results:
            key: tuple[float, float] = (r.gnmda_ns, r.angle_deg)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            for synapse_index, onset_time_ms in enumerate(r.synapse_onset_times_ms):
                writer.writerow(
                    [
                        f"{r.gnmda_ns:.6f}",
                        int(r.angle_deg),
                        int(synapse_index),
                        f"{onset_time_ms:.4f}",
                    ],
                )


def _run_sweep_for_mode(
    *,
    artifacts: SweepArtifacts,
    mode: TrialMode,
    angles_deg: tuple[int, ...],
    n_trials_per_angle: int,
    gnmda_ns: float,
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
                gnmda_ns=gnmda_ns,
            )
            results.append(result)
            bar.update(1)
    bar.close()
    return results


def _print_summary(*, label: str, results: list[TrialResult]) -> None:
    angles_seen: list[float] = sorted({r.angle_deg for r in results})
    gnmda_values_seen: list[float] = sorted({r.gnmda_ns for r in results})
    print(
        f"[{label}] gNMDA values: {gnmda_values_seen}  per-(gNMDA, angle) mean firing rate (Hz):",
        flush=True,
    )
    for gnmda_ns in gnmda_values_seen:
        for angle_deg in angles_seen:
            rates: list[float] = [
                r.firing_rate_hz
                for r in results
                if r.angle_deg == angle_deg and r.gnmda_ns == gnmda_ns
            ]
            mean_rate: float = sum(rates) / max(1, len(rates))
            print(
                f"  gNMDA={gnmda_ns:.2f}  angle={int(angle_deg):3d} deg  "
                f"mean={mean_rate:6.2f} Hz  (n={len(rates)})",
                flush=True,
            )


def run_dry_run_validation(*, artifacts: SweepArtifacts, gnmda_ns: float = 0.0) -> None:
    """1 angle x 2 trials per mode dry-run gate at the specified ``gnmda_ns``.

    At ``gnmda_ns = 0.0``, FULL mode at theta=0 must produce a non-zero firing rate (matches
    t0054's gnmda=0 row at theta=0); otherwise the entire pipeline is broken.
    """
    print(
        f"[dry-run] Running 1 angle (theta=0) x 2 trials per mode at gnmda_ns={gnmda_ns:.2f}...",
        flush=True,
    )
    dry_angles: tuple[int, ...] = (0,)
    n_dry: int = 2
    full_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.FULL,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gnmda_ns=gnmda_ns,
        description=f"dry-run FULL gnmda={gnmda_ns:.2f}",
    )
    e_only_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.E_ONLY,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gnmda_ns=gnmda_ns,
        description=f"dry-run E_ONLY gnmda={gnmda_ns:.2f}",
    )
    gaba_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.GABA_ONLY,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gnmda_ns=gnmda_ns,
        description=f"dry-run GABA_ONLY gnmda={gnmda_ns:.2f}",
    )

    e_only_rate: float = float(np.mean([r.firing_rate_hz for r in e_only_results]))
    full_rate: float = float(np.mean([r.firing_rate_hz for r in full_results]))
    gaba_rate: float = float(np.mean([r.firing_rate_hz for r in gaba_results]))
    print(
        f"[dry-run] mean firing rate at theta=0, gnmda_ns={gnmda_ns:.2f}: "
        f"FULL={full_rate:.2f} Hz E_ONLY={e_only_rate:.2f} Hz GABA_ONLY={gaba_rate:.2f} Hz",
        flush=True,
    )

    if full_rate <= 0.0 and gnmda_ns == 0.0:
        first_pair: EiPair = artifacts.pairs[0]
        print(
            f"[dry-run] DEBUG first pair: x_um={first_pair.x_um:.2f} y_um={first_pair.y_um:.2f} "
            f"ampa_netstim.start={float(first_pair.ampa_netstim.start):.2f} ms "
            f"ampa_netcon.weight[0]={float(first_pair.ampa_netcon.weight[0])} uS "
            f"nmda_netcon.weight[0]={float(first_pair.nmda_netcon.weight[0])} uS",
            flush=True,
        )
        raise RuntimeError(
            "Dry-run gate failed: FULL at theta=0, gnmda_ns=0 produced zero spikes. "
            "Aborting before the full sweep.",
        )


def run_full_sweep(*, voltage_sample_stride: int = 8) -> None:
    """End-to-end sweep: setup, dry-run, then 12 x 10 x 3 x 4 = 1,440 trials.

    All four gNMDA values are appended to a single per-mode CSV (one CSV per mode); each CSV
    ends up with 4 x 12 x 10 = 480 rows.
    """
    artifacts: SweepArtifacts = setup_sweep_artifacts()

    run_dry_run_validation(artifacts=artifacts, gnmda_ns=0.0)

    angles: tuple[int, ...] = ANGLES_DEG
    n_trials: int = N_TRIALS_PER_ANGLE

    full_results_all: list[TrialResult] = []
    e_only_results_all: list[TrialResult] = []
    gaba_results_all: list[TrialResult] = []

    sweep_t0: float = time.perf_counter()
    for gnmda_ns in NMDA_PEAK_NS_VALUES:
        print(f"[sweep] === gNMDA = {gnmda_ns:.2f} nS ===", flush=True)
        full_results_all.extend(
            _run_sweep_for_mode(
                artifacts=artifacts,
                mode=TrialMode.FULL,
                angles_deg=angles,
                n_trials_per_angle=n_trials,
                gnmda_ns=gnmda_ns,
                description=f"sweep FULL gnmda={gnmda_ns:.2f}",
            ),
        )
        e_only_results_all.extend(
            _run_sweep_for_mode(
                artifacts=artifacts,
                mode=TrialMode.E_ONLY,
                angles_deg=angles,
                n_trials_per_angle=n_trials,
                gnmda_ns=gnmda_ns,
                description=f"sweep E_ONLY gnmda={gnmda_ns:.2f}",
            ),
        )
        gaba_results_all.extend(
            _run_sweep_for_mode(
                artifacts=artifacts,
                mode=TrialMode.GABA_ONLY,
                angles_deg=angles,
                n_trials_per_angle=n_trials,
                gnmda_ns=gnmda_ns,
                description=f"sweep GABA_ONLY gnmda={gnmda_ns:.2f}",
            ),
        )

    sweep_wallclock_s: float = time.perf_counter() - sweep_t0

    for label, results in (
        ("FULL", full_results_all),
        ("E_ONLY", e_only_results_all),
        ("GABA_ONLY", gaba_results_all),
    ):
        _print_summary(label=label, results=results)

    # Write per-mode outputs (single CSV per mode with all four gNMDA values appended).
    for mode, results in (
        (TrialMode.FULL, full_results_all),
        (TrialMode.E_ONLY, e_only_results_all),
        (TrialMode.GABA_ONLY, gaba_results_all),
    ):
        out_paths: ModeOutputPaths = _select_paths_for_mode(mode=mode)
        _write_curve_csv(results=results, out_path=out_paths.curve)
        _write_spikes_csv(results=results, out_path=out_paths.spikes)
        _write_voltage_csv(
            results=results,
            out_path=out_paths.voltages,
            sample_stride=voltage_sample_stride,
        )
        print(
            f"[sweep] wrote {out_paths.curve.name} (rows={len(results)}); "
            f"spikes -> {out_paths.spikes.name}; voltages -> {out_paths.voltages.name}",
            flush=True,
        )

    # Activation times: one row per (gnmda, angle, synapse) — read from FULL results.
    _write_activation_times_csv(results=full_results_all, out_path=ACTIVATION_TIMES_CSV)
    print(f"[sweep] wrote activation times -> {ACTIVATION_TIMES_CSV.name}", flush=True)

    # Wall-clock log.
    import json  # noqa: PLC0415

    WALLCLOCK_JSON.parent.mkdir(parents=True, exist_ok=True)
    WALLCLOCK_JSON.write_text(
        json.dumps(
            {
                "wallclock_seconds": sweep_wallclock_s,
                "n_trials": (
                    len(full_results_all) + len(e_only_results_all) + len(gaba_results_all)
                ),
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"[sweep] total wall-clock: {sweep_wallclock_s:.2f} s ({sweep_wallclock_s / 60.0:.2f} min)",
        flush=True,
    )


if __name__ == "__main__":
    run_full_sweep()
