"""Multi-mode 12-direction tuning-curve sweep for the t0053 minimal DSGC (spatial GABA gating).

Adapted from t0052's ``run_tuning_curve.py`` per CLAUDE.md rule 3 (cross-task code is copied, not
imported). Differences from t0052:

* ``soma_origin_um=cell.soma_origin_um`` is threaded into ``build_ei_pairs`` so each pair carries
  ``theta_centrifugal_rad``.
* ``schedule_ei_onsets`` no longer accepts ``gaba_mod_theta``; the I-synapse fire decision is per
  pair via the centripetal-gating rule.
* The activation-times CSV gains an ``is_fired`` (0/1) column per (angle, synapse).
* A new CSV ``active_fraction_per_direction.csv`` is written, with the per-direction mean of the
  per-trial ``i_active_fraction`` across the 10 FULL-mode trials.
* The dry-run validation gate adds an ``i_active_fraction in [0.3, 0.7]`` check at theta=0 (one
  point on a roughly symmetric placement should land near 0.5).

Outputs after a full sweep:
* ``tuning_curve_{full,ampa_only,gaba_only}.csv`` (120 rows each)
* ``spike_times_{full,ampa_only,gaba_only}.csv``
* ``voltage_traces_{full,ampa_only,gaba_only}.csv``
* ``activation_times.csv`` (1,200 rows; 12 angles x 100 synapses, with ``is_fired``)
* ``active_fraction_per_direction.csv`` (12 rows)
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tqdm import tqdm

from tasks.t0053_minimal_dsgc_spatial_gaba.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
    summarize_cell,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.constants import (
    ACTIVE_FRACTION_LOWER,
    ACTIVE_FRACTION_UPPER,
    ANGLES_DEG,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_IS_FIRED,
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
from tasks.t0053_minimal_dsgc_spatial_gaba.code.neuron_bootstrap import (
    enable_cvode,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.paths import (
    ACTIVATION_TIMES_CSV,
    ACTIVE_FRACTION_CSV,
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
from tasks.t0053_minimal_dsgc_spatial_gaba.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.synapses import (
    EiPair,
    build_ei_pairs,
)
from tasks.t0053_minimal_dsgc_spatial_gaba.code.trial import (
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
        f"soma_L_um={summary.soma_length_um:.2f} soma_diam_um={summary.soma_diameter_um:.2f} "
        f"soma_origin_um={cell.soma_origin_um}",
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
        soma_origin_um=cell.soma_origin_um,
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
    """Write a long-form (angle, seed, sample_idx, t_ms, voltage_mv) CSV."""
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
    """Write the per-angle, per-synapse onset-time CSV with the ``is_fired`` column.

    Onset time is mode-independent (it depends only on bar geometry); ``is_fired`` for I synapses
    is the per-trial centripetal-gating mask. We read the first FULL-mode trial of each angle.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    seen_angles: set[float] = set()
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_ANGLE_DEG, COL_SYNAPSE_INDEX, COL_ONSET_TIME_MS, COL_IS_FIRED])
        for r in results:
            if r.angle_deg in seen_angles:
                continue
            seen_angles.add(r.angle_deg)
            assert len(r.synapse_onset_times_ms) == len(r.i_fired_mask), (
                "onset_times_ms and i_fired_mask must align"
            )
            for synapse_index, (onset_time_ms, fires) in enumerate(
                zip(r.synapse_onset_times_ms, r.i_fired_mask, strict=True),
            ):
                writer.writerow(
                    [
                        int(r.angle_deg),
                        int(synapse_index),
                        f"{onset_time_ms:.4f}",
                        1 if fires else 0,
                    ],
                )


def _write_active_fraction_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write the per-direction mean active fraction across the 10 FULL-mode trials per angle."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    angles_seen: list[float] = sorted({r.angle_deg for r in results})
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([COL_ANGLE_DEG, COL_ACTIVE_FRACTION])
        for angle_deg in angles_seen:
            fractions: list[float] = [
                r.i_active_fraction for r in results if r.angle_deg == angle_deg
            ]
            assert len(fractions) > 0, f"no trials for angle={angle_deg}"
            mean_af: float = float(np.mean(fractions))
            writer.writerow([int(angle_deg), f"{mean_af:.6f}"])


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

    Per Step 10 of the t0053 plan:
    * AMPA_ONLY at theta=0 must produce a non-zero firing rate.
    * FULL at theta=0 spike count must be <= AMPA_ONLY at theta=0 (inhibition can only suppress).
    * GABA_ONLY at theta=0: per-trial ``i_active_fraction`` must be in [0.3, 0.7].
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
    full_active: float = float(np.mean([r.i_active_fraction for r in full_results]))
    gaba_active: float = float(np.mean([r.i_active_fraction for r in gaba_results]))
    print(
        f"[dry-run] mean firing rate at theta=0: FULL={full_rate:.2f} Hz "
        f"AMPA_ONLY={ampa_rate:.2f} Hz GABA_ONLY={gaba_rate:.2f} Hz",
        flush=True,
    )
    print(
        f"[dry-run] mean i_active_fraction at theta=0: FULL={full_active:.3f} "
        f"GABA_ONLY={gaba_active:.3f}",
        flush=True,
    )

    if ampa_rate <= 0.0:
        first_pair: EiPair = artifacts.pairs[0]
        print(
            f"[dry-run] DEBUG first pair: x_um={first_pair.x_um:.2f} y_um={first_pair.y_um:.2f} "
            f"theta_centrifugal_rad={first_pair.theta_centrifugal_rad:.4f} "
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

    full_spikes: float = float(np.mean([len(r.spike_times_ms) for r in full_results]))
    ampa_spikes: float = float(np.mean([len(r.spike_times_ms) for r in ampa_results]))
    if full_spikes > ampa_spikes + 1e-6:
        raise RuntimeError(
            f"Dry-run gate failed: FULL spike count ({full_spikes:.2f}) exceeds AMPA_ONLY "
            f"({ampa_spikes:.2f}) at theta=0. Inhibition should only suppress.",
        )

    if not (0.3 <= gaba_active <= 0.7):
        raise RuntimeError(
            f"Dry-run gate failed: GABA_ONLY i_active_fraction at theta=0 = {gaba_active:.3f} "
            f"is outside [0.3, 0.7]. Inspect soma_origin_um and theta_centrifugal_rad.",
        )

    print(
        f"[dry-run] gates passed (AMPA spikes>0, FULL<=AMPA, GABA i_active in "
        f"[0.3, 0.7]; soft cross-direction range is "
        f"[{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}]).",
        flush=True,
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

    # Activation times: one row per (angle, synapse), with is_fired -- read from FULL results.
    _write_activation_times_csv(results=full_results, out_path=ACTIVATION_TIMES_CSV)
    print(f"[sweep] wrote activation times -> {ACTIVATION_TIMES_CSV.name}", flush=True)

    # Active fraction per direction: 12 rows.
    _write_active_fraction_csv(results=full_results, out_path=ACTIVE_FRACTION_CSV)
    print(
        f"[sweep] wrote active fraction per direction -> {ACTIVE_FRACTION_CSV.name}",
        flush=True,
    )


if __name__ == "__main__":
    run_full_sweep()
