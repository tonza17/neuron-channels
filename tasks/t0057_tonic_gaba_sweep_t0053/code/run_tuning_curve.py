"""Multi-mode 12-direction tuning-curve sweep with outer GABA_BASE_NS loop for t0057.

Adapted from ``tasks/t0053_minimal_dsgc_spatial_gaba/code/run_tuning_curve.py`` with the
[t0055]-style outer-loop pattern: ``GABA_BASE_NS_VALUES`` is a 5-tuple, and each per-mode CSV
gains a leading ``gaba_base_ns`` column. Total: 5 GABA values x 12 angles x 10 trials x 3 modes
= 1,800 trials. Each per-mode CSV ends up with 5 x 12 x 10 = 600 rows.

The sweep harness invokes ``ensure_gaba_tonic_compiled()`` AFTER ``load_stdrun()`` and BEFORE any
``h.gaba_tonic(seg)`` construction so the new POINT_PROCESS is registered before the synapse
builder runs. The dry-run gate at ``gaba_base_ns = 1.0`` validates AMPA_ONLY peak Hz, FULL <=
AMPA_ONLY, and the IPSP-sustained-window check at ``theta = 210 deg`` per REQ-13.

Outputs after a full sweep:
* ``tuning_curve_{full,ampa_only,gaba_only}.csv`` (600 rows each)
* ``spike_times_{full,ampa_only,gaba_only}.csv``
* ``voltage_traces_{full,ampa_only,gaba_only}.csv`` (stride-8 downsampled per [t0055] guidance)
* ``activation_times.csv`` (1 row per (gaba_base_ns, angle, synapse))
* ``active_fraction_per_direction.csv`` (12 rows; conductance-independent)
* ``placement_seed0.json``
* ``wallclock.json``
"""

from __future__ import annotations

import csv
import json
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tqdm import tqdm

from tasks.t0057_tonic_gaba_sweep_t0053.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
    summarize_cell,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    ACTIVE_FRACTION_LOWER,
    ACTIVE_FRACTION_UPPER,
    ANGLES_DEG,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_GABA_BASE_NS,
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
    GABA_BASE_NS_VALUES,
    IPSP_SUSTAINED_RATIO,
    IPSP_SUSTAINED_T_EARLY_MS,
    IPSP_SUSTAINED_T_LATE_MS,
    IPSP_SUSTAINED_THETA_DEG,
    N_PAIRS,
    N_TRIALS_PER_ANGLE,
    PLACEMENT_SEED,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.neuron_bootstrap import (
    enable_cvode,
    ensure_gaba_tonic_compiled,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.paths import (
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
    WALLCLOCK_JSON,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.placement import (
    Location,
    sample_dendritic_locations,
    save_placement_json,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.synapses import (
    EiPair,
    build_ei_pairs,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.trial import (
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
    if mode == TrialMode.AMPA_ONLY:
        return ModeOutputPaths(
            curve=TUNING_CURVE_AMPA_ONLY_CSV,
            spikes=SPIKE_TIMES_AMPA_ONLY_CSV,
            voltages=VOLTAGE_TRACES_AMPA_ONLY_CSV,
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

    This invokes ``ensure_gaba_tonic_compiled()`` after ``load_stdrun`` so that the
    ``gaba_tonic`` POINT_PROCESS is registered with NEURON before ``build_ei_pairs`` constructs
    any ``h.gaba_tonic(seg)`` handles.
    """
    ensure_neuron_importable()
    load_stdrun()
    ensure_gaba_tonic_compiled()
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

    print(f"[setup] Building {len(locations)} co-located E+tonic-I pairs", flush=True)
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
        writer.writerow(
            [COL_GABA_BASE_NS, COL_ANGLE_DEG, COL_TRIAL_SEED, COL_FIRING_RATE_HZ],
        )
        for r in results:
            writer.writerow(
                [
                    f"{r.gaba_base_ns:.6f}",
                    int(r.angle_deg),
                    r.trial_seed,
                    f"{r.firing_rate_hz:.6f}",
                ],
            )


def _write_spikes_csv(*, results: list[TrialResult], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [COL_GABA_BASE_NS, COL_ANGLE_DEG, COL_TRIAL_INDEX, COL_SPIKE_TIME_S],
        )
        for r in results:
            for spike_time_ms in r.spike_times_ms:
                writer.writerow(
                    [
                        f"{r.gaba_base_ns:.6f}",
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
    """Write a long-form (gaba_base_ns, angle, seed, sample_idx, t_ms, voltage_mv) CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_GABA_BASE_NS,
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
                        f"{r.gaba_base_ns:.6f}",
                        int(r.angle_deg),
                        r.trial_seed,
                        int(sample_idx),
                        f"{float(r.t_ms[sample_idx]):.4f}",
                        f"{float(r.v_soma_mv[sample_idx]):.4f}",
                    ],
                )


def _write_activation_times_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write the per-(gaba, angle, synapse) onset-time CSV with the ``is_fired`` column.

    Onset time and is_fired are mode-independent (they depend only on bar geometry and the
    spatial-gating predicate). The first encountered FULL trial for each (gaba_base_ns, angle)
    pair is used.
    """
    out_path.parent.mkdir(parents=True, exist_ok=True)
    seen_keys: set[tuple[float, float]] = set()
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_GABA_BASE_NS,
                COL_ANGLE_DEG,
                COL_SYNAPSE_INDEX,
                COL_ONSET_TIME_MS,
                COL_IS_FIRED,
            ],
        )
        for r in results:
            key: tuple[float, float] = (r.gaba_base_ns, r.angle_deg)
            if key in seen_keys:
                continue
            seen_keys.add(key)
            assert len(r.synapse_onset_times_ms) == len(r.i_fired_mask), (
                "onset_times_ms and i_fired_mask must align"
            )
            for synapse_index, (onset_time_ms, fires) in enumerate(
                zip(r.synapse_onset_times_ms, r.i_fired_mask, strict=True),
            ):
                writer.writerow(
                    [
                        f"{r.gaba_base_ns:.6f}",
                        int(r.angle_deg),
                        int(synapse_index),
                        f"{onset_time_ms:.4f}",
                        1 if fires else 0,
                    ],
                )


def _write_active_fraction_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write the per-direction mean active fraction across all FULL-mode trials per angle.

    The active fraction is conductance-independent (it depends only on the spatial-gating
    predicate, not on the conductance amplitude), so we pool across all GABA values.
    """
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
    gaba_base_ns: float,
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
                gaba_base_ns=gaba_base_ns,
            )
            results.append(result)
            bar.update(1)
    bar.close()
    return results


def _print_summary(*, label: str, results: list[TrialResult]) -> None:
    angles_seen: list[float] = sorted({r.angle_deg for r in results})
    gaba_values_seen: list[float] = sorted({r.gaba_base_ns for r in results})
    print(
        f"[{label}] gaba_base_ns values: {gaba_values_seen}  "
        f"per-(gaba, angle) mean firing rate (Hz):",
        flush=True,
    )
    for gaba_value in gaba_values_seen:
        for angle_deg in angles_seen:
            rates: list[float] = [
                r.firing_rate_hz
                for r in results
                if r.angle_deg == angle_deg and r.gaba_base_ns == gaba_value
            ]
            mean_rate: float = sum(rates) / max(1, len(rates))
            print(
                f"  gaba={gaba_value:.2f}  angle={int(angle_deg):3d} deg  "
                f"mean={mean_rate:6.2f} Hz  (n={len(rates)})",
                flush=True,
            )


def _check_ipsp_sustained(
    *,
    artifacts: SweepArtifacts,
    gaba_base_ns: float,
) -> None:
    """Run one GABA_ONLY trial at theta = 210 and assert IPSP sustained-window.

    Asserts |v(IPSP_SUSTAINED_T_LATE_MS) - V_INIT| >= IPSP_SUSTAINED_RATIO *
    |v(IPSP_SUSTAINED_T_EARLY_MS) - V_INIT|. This is REQ-13: the new tonic mechanism must keep the
    IPSP voltage envelope sustained across the stimulus window, not collapse early like the t0053
    Exp2Syn-event mechanism did.
    """
    from neuron import h  # noqa: PLC0415

    result: TrialResult = run_one_trial(
        h=h,
        cell=artifacts.cell,
        pairs=artifacts.pairs,
        mode=TrialMode.GABA_ONLY,
        angle_deg=float(IPSP_SUSTAINED_THETA_DEG),
        trial_seed=99999,
        gaba_base_ns=gaba_base_ns,
    )
    t_arr: np.ndarray = result.t_ms
    v_arr: np.ndarray = result.v_soma_mv
    early_idx: int = int(np.argmin(np.abs(t_arr - IPSP_SUSTAINED_T_EARLY_MS)))
    late_idx: int = int(np.argmin(np.abs(t_arr - IPSP_SUSTAINED_T_LATE_MS)))
    v_early: float = float(v_arr[early_idx])
    v_late: float = float(v_arr[late_idx])
    delta_early: float = abs(v_early - V_INIT_MV)
    delta_late: float = abs(v_late - V_INIT_MV)
    print(
        f"[dry-run] IPSP-sustained check: theta={IPSP_SUSTAINED_THETA_DEG} deg, "
        f"gaba={gaba_base_ns:.2f} nS, v(t=200ms)={v_early:.4f} mV "
        f"(|delta|={delta_early:.4f}), v(t=1300ms)={v_late:.4f} mV "
        f"(|delta|={delta_late:.4f}), ratio={delta_late / max(delta_early, 1e-9):.4f}",
        flush=True,
    )
    if delta_late < IPSP_SUSTAINED_RATIO * delta_early:
        threshold: float = IPSP_SUSTAINED_RATIO * delta_early
        raise RuntimeError(
            f"IPSP-sustained-window gate failed at theta={IPSP_SUSTAINED_THETA_DEG} deg, "
            f"gaba={gaba_base_ns:.2f}: |v(1300ms) - V_init|={delta_late:.4f} mV is less than "
            f"{IPSP_SUSTAINED_RATIO} * |v(200ms) - V_init|={threshold:.4f} mV. "
            f"The tonic mechanism is not sustaining inhibition through the stimulus window.",
        )


def run_dry_run_validation(*, artifacts: SweepArtifacts, gaba_base_ns: float = 1.0) -> None:
    """1 angle x 2 trials per mode dry-run gate at the specified ``gaba_base_ns``.

    Per Step 9 of the t0057 plan:
    * AMPA_ONLY at theta=0 must produce a non-zero firing rate.
    * FULL at theta=0 spike count must be <= AMPA_ONLY at theta=0 (inhibition can only suppress).
    * GABA_ONLY at theta=0: per-trial ``i_active_fraction`` must be in [0.3, 0.7].
    * IPSP-sustained-window check at theta=210 deg passes.
    """
    print(
        f"[dry-run] Running 1 angle (theta=0) x 2 trials per mode at gaba={gaba_base_ns:.2f}...",
        flush=True,
    )
    dry_angles: tuple[int, ...] = (0,)
    n_dry: int = 2
    full_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.FULL,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gaba_base_ns=gaba_base_ns,
        description=f"dry-run FULL gaba={gaba_base_ns:.2f}",
    )
    ampa_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.AMPA_ONLY,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gaba_base_ns=gaba_base_ns,
        description=f"dry-run AMPA_ONLY gaba={gaba_base_ns:.2f}",
    )
    gaba_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.GABA_ONLY,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gaba_base_ns=gaba_base_ns,
        description=f"dry-run GABA_ONLY gaba={gaba_base_ns:.2f}",
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
            "Aborting before the full sweep.",
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

    # IPSP-sustained-window regression at theta = 210 deg (REQ-13).
    _check_ipsp_sustained(artifacts=artifacts, gaba_base_ns=gaba_base_ns)

    print(
        f"[dry-run] gates passed (AMPA spikes>0, FULL<=AMPA, GABA i_active in "
        f"[0.3, 0.7], IPSP sustained at theta=210; soft cross-direction range is "
        f"[{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}]).",
        flush=True,
    )


def run_full_sweep(*, voltage_sample_stride: int = 8) -> None:
    """End-to-end sweep: setup, dry-run gate, then 5 x 12 x 10 x 3 = 1,800 trials.

    All five GABA_BASE_NS values are appended to a single per-mode CSV (one CSV per mode); each
    CSV ends up with 5 x 12 x 10 = 600 rows.
    """
    artifacts: SweepArtifacts = setup_sweep_artifacts()

    run_dry_run_validation(artifacts=artifacts, gaba_base_ns=1.0)

    angles: tuple[int, ...] = ANGLES_DEG
    n_trials: int = N_TRIALS_PER_ANGLE

    full_results_all: list[TrialResult] = []
    ampa_results_all: list[TrialResult] = []
    gaba_results_all: list[TrialResult] = []

    sweep_t0: float = time.perf_counter()
    for gaba_base_ns in GABA_BASE_NS_VALUES:
        print(f"[sweep] === GABA_BASE_NS = {gaba_base_ns:.2f} nS ===", flush=True)
        full_results_all.extend(
            _run_sweep_for_mode(
                artifacts=artifacts,
                mode=TrialMode.FULL,
                angles_deg=angles,
                n_trials_per_angle=n_trials,
                gaba_base_ns=gaba_base_ns,
                description=f"sweep FULL gaba={gaba_base_ns:.2f}",
            ),
        )
        ampa_results_all.extend(
            _run_sweep_for_mode(
                artifacts=artifacts,
                mode=TrialMode.AMPA_ONLY,
                angles_deg=angles,
                n_trials_per_angle=n_trials,
                gaba_base_ns=gaba_base_ns,
                description=f"sweep AMPA_ONLY gaba={gaba_base_ns:.2f}",
            ),
        )
        gaba_results_all.extend(
            _run_sweep_for_mode(
                artifacts=artifacts,
                mode=TrialMode.GABA_ONLY,
                angles_deg=angles,
                n_trials_per_angle=n_trials,
                gaba_base_ns=gaba_base_ns,
                description=f"sweep GABA_ONLY gaba={gaba_base_ns:.2f}",
            ),
        )

    sweep_wallclock_s: float = time.perf_counter() - sweep_t0

    for label, results in (
        ("FULL", full_results_all),
        ("AMPA_ONLY", ampa_results_all),
        ("GABA_ONLY", gaba_results_all),
    ):
        _print_summary(label=label, results=results)

    # Write per-mode outputs (single CSV per mode with all five gaba values appended).
    for mode, results in (
        (TrialMode.FULL, full_results_all),
        (TrialMode.AMPA_ONLY, ampa_results_all),
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

    # Activation times: one row per (gaba, angle, synapse) -- read from FULL results.
    _write_activation_times_csv(results=full_results_all, out_path=ACTIVATION_TIMES_CSV)
    print(f"[sweep] wrote activation times -> {ACTIVATION_TIMES_CSV.name}", flush=True)

    # Active fraction per direction: 12 rows.
    _write_active_fraction_csv(results=full_results_all, out_path=ACTIVE_FRACTION_CSV)
    print(
        f"[sweep] wrote active fraction per direction -> {ACTIVE_FRACTION_CSV.name}",
        flush=True,
    )

    # Wall-clock log.
    WALLCLOCK_JSON.parent.mkdir(parents=True, exist_ok=True)
    WALLCLOCK_JSON.write_text(
        json.dumps(
            {
                "wallclock_seconds": sweep_wallclock_s,
                "n_trials": (len(full_results_all) + len(ampa_results_all) + len(gaba_results_all)),
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
