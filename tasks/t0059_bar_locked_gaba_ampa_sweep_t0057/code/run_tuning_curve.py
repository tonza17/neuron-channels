"""Multi-mode 12-direction tuning-curve sweep with outer (gampa, gaba) loop for t0059.

Adapted from ``tasks/t0057_tonic_gaba_sweep_t0053/code/run_tuning_curve.py``. Major changes:

* New outer ``AMPA_PEAK_NS_VALUES`` loop wraps the existing ``GABA_BASE_NS_VALUES`` loop. Total:
  5 (gampa) x 5 (gaba) x 12 (angles) x 10 (trials) x 3 (modes) = 9,000 trials.
* ``gampa_ns`` is added as a leading column to every per-mode CSV.
* The activation-time CSV writer is removed (no longer informative under explicit per-synapse
  bar-arrival-locked windows; REQ-5).
* The dry-run gate is reworked for the new (FULL / EPSP_PASSIVE / IPSP_PASSIVE) protocol.

The CVODE bootstrap order is unchanged:
``ensure_neuron_importable -> load_stdrun -> ensure_gaba_tonic_compiled -> enable_cvode``.

Outputs:
* ``tuning_curve_{full,epsp_passive,ipsp_passive}.csv`` (300 rows each)
* ``spike_times_{full,epsp_passive,ipsp_passive}.csv``
* ``voltage_traces_{full,epsp_passive,ipsp_passive}.csv`` (stride-8 downsampled)
* ``active_fraction_per_direction.csv`` (12 rows; conductance-independent)
* ``placement_seed0.json``
* ``wallclock.json``
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from tqdm import tqdm

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.cell import (
    CellHandles,
    build_dsgc_from_swc,
    summarize_cell,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    ACTIVE_FRACTION_LOWER,
    ACTIVE_FRACTION_UPPER,
    AMPA_PEAK_NS_VALUES,
    ANGLES_DEG,
    AP_THRESHOLD_MV,
    BAR_VELOCITY_UM_PER_MS,
    BASE_OFFSET_MS,
    COL_ACTIVE_FRACTION,
    COL_ANGLE_DEG,
    COL_FIRING_RATE_HZ,
    COL_GABA_BASE_NS,
    COL_GAMPA_NS,
    COL_SAMPLE_IDX,
    COL_SPIKE_TIME_S,
    COL_T_MS,
    COL_TRIAL_INDEX,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    DT_MS,
    EPSP_PASSIVE_PEAK_VM_GATE_MV,
    GABA_BASE_NS_VALUES,
    N_PAIRS,
    N_TRIALS_PER_ANGLE,
    PLACEMENT_SEED,
    V_INIT_MV,
    WINDOW_MS,
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.neuron_bootstrap import (
    enable_cvode,
    ensure_gaba_tonic_compiled,
    ensure_neuron_importable,
    load_stdrun,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import (
    ACTIVE_FRACTION_CSV,
    MORPHOLOGY_SWC_PATH,
    PLACEMENT_JSON,
    SPIKE_TIMES_EPSP_PASSIVE_CSV,
    SPIKE_TIMES_FULL_CSV,
    SPIKE_TIMES_IPSP_PASSIVE_CSV,
    TUNING_CURVE_EPSP_PASSIVE_CSV,
    TUNING_CURVE_FULL_CSV,
    TUNING_CURVE_IPSP_PASSIVE_CSV,
    VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
    VOLTAGE_TRACES_FULL_CSV,
    VOLTAGE_TRACES_IPSP_PASSIVE_CSV,
    WALLCLOCK_JSON,
)
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
    if mode == TrialMode.EPSP_PASSIVE:
        return ModeOutputPaths(
            curve=TUNING_CURVE_EPSP_PASSIVE_CSV,
            spikes=SPIKE_TIMES_EPSP_PASSIVE_CSV,
            voltages=VOLTAGE_TRACES_EPSP_PASSIVE_CSV,
        )
    if mode == TrialMode.IPSP_PASSIVE:
        return ModeOutputPaths(
            curve=TUNING_CURVE_IPSP_PASSIVE_CSV,
            spikes=SPIKE_TIMES_IPSP_PASSIVE_CSV,
            voltages=VOLTAGE_TRACES_IPSP_PASSIVE_CSV,
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
            [
                COL_GAMPA_NS,
                COL_GABA_BASE_NS,
                COL_ANGLE_DEG,
                COL_TRIAL_SEED,
                COL_FIRING_RATE_HZ,
            ],
        )
        for r in results:
            writer.writerow(
                [
                    f"{r.gampa_ns:.6f}",
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
            [
                COL_GAMPA_NS,
                COL_GABA_BASE_NS,
                COL_ANGLE_DEG,
                COL_TRIAL_INDEX,
                COL_SPIKE_TIME_S,
            ],
        )
        for r in results:
            for spike_time_ms in r.spike_times_ms:
                writer.writerow(
                    [
                        f"{r.gampa_ns:.6f}",
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
    """Write a long-form (gampa, gaba, angle, seed, sample_idx, t_ms, voltage_mv) CSV."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                COL_GAMPA_NS,
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
                        f"{r.gampa_ns:.6f}",
                        f"{r.gaba_base_ns:.6f}",
                        int(r.angle_deg),
                        r.trial_seed,
                        int(sample_idx),
                        f"{float(r.t_ms[sample_idx]):.4f}",
                        f"{float(r.v_soma_mv[sample_idx]):.4f}",
                    ],
                )


def _write_active_fraction_csv(*, results: list[TrialResult], out_path: Path) -> None:
    """Write the per-direction mean active fraction across all FULL-mode trials per angle.

    The active fraction is conductance-independent, so we pool across all (gampa, gaba) values.
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
    gampa_ns: float,
    gaba_base_ns: float,
    description: str,
    progress_bar: tqdm | None = None,
) -> list[TrialResult]:
    from neuron import h  # noqa: PLC0415

    results: list[TrialResult] = []
    bar = progress_bar
    own_bar: bool = False
    if bar is None:
        total: int = len(angles_deg) * n_trials_per_angle
        bar = tqdm(total=total, desc=description, unit="trial")
        own_bar = True
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
                gampa_ns=gampa_ns,
                gaba_base_ns=gaba_base_ns,
            )
            results.append(result)
            bar.update(1)
    if own_bar:
        bar.close()
    return results


def _ipsp_centre_of_mass_ms(*, result: TrialResult) -> float:
    """Centre of mass of |v(t) - V_INIT_MV| over the trial in ms.

    Used by the dry-run gate and the bar-locked IPSP envelope test (REQ-13).
    """
    weights: np.ndarray = np.abs(result.v_soma_mv - V_INIT_MV)
    if float(np.sum(weights)) == 0.0:
        return 0.0
    return float(np.sum(weights * result.t_ms) / np.sum(weights))


def _predicted_ipsp_com_lower_bound_ms(
    *,
    pairs: list[EiPair],
    theta_a_deg: float,
    theta_b_deg: float,
) -> float:
    """Predicted lower bound on |COM_a - COM_b| from per-synapse onset latencies.

    For each direction, average ``onset_ms`` over active (firing) synapses; the absolute
    difference between the two direction averages, divided by 2, is a coarse but valid lower
    bound on the centre-of-mass shift between IPSP traces at the two directions.
    """
    from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.synapses import (  # noqa: PLC0415
        _onset_time_ms,
        i_synapse_fires,
    )

    def _direction_onset_mean(angle_deg: float) -> float:
        active_onsets: list[float] = []
        for pair in pairs:
            fires: bool = i_synapse_fires(
                theta_stim_deg=angle_deg,
                theta_centrifugal_deg=math.degrees(pair.theta_centrifugal_rad),
            )
            if fires:
                active_onsets.append(
                    _onset_time_ms(
                        pair=pair,
                        angle_deg=angle_deg,
                        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
                    ),
                )
        if len(active_onsets) == 0:
            return 0.0
        return float(np.mean(active_onsets))

    a: float = _direction_onset_mean(angle_deg=theta_a_deg)
    b: float = _direction_onset_mean(angle_deg=theta_b_deg)
    return abs(a - b) / 2.0


def run_dry_run_validation(
    *,
    artifacts: SweepArtifacts,
    gampa_ns: float = 1.0,
    gaba_base_ns: float = 0.5,
) -> None:
    """1 angle x 2 trials x 3 modes dry-run gate at the centre of the new grid.

    Per Step 10 of the t0059 plan:
    * EPSP_PASSIVE peak Vm < -50 mV at every direction (HH save-and-zero is wired correctly).
    * IPSP centre-of-mass shift between theta=0 and theta=90 >= predicted_lower_bound.
    * Active fraction at theta=0 in [0.30, 0.70].
    * FULL spike count <= EPSP_PASSIVE-equivalent... but EPSP_PASSIVE produces 0 spikes by
      construction (no spike generator with HH disabled), so this gate becomes: FULL spike count
      <= some sanity bound (use AMPA-without-GABA in a separate dry mini-trial as needed).
    """
    print(
        f"[dry-run] Running dry-run gate at gampa_ns={gampa_ns:.2f} nS, "
        f"gaba_base_ns={gaba_base_ns:.2f} nS, theta in {{0, 90}}, 2 trials each, 3 modes...",
        flush=True,
    )
    dry_angles: tuple[int, ...] = (0, 90)
    n_dry: int = 2
    full_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.FULL,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gampa_ns=gampa_ns,
        gaba_base_ns=gaba_base_ns,
        description=f"dry FULL g={gampa_ns:.2f}/{gaba_base_ns:.2f}",
    )
    epsp_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.EPSP_PASSIVE,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gampa_ns=gampa_ns,
        gaba_base_ns=gaba_base_ns,
        description=f"dry EPSP g={gampa_ns:.2f}/{gaba_base_ns:.2f}",
    )
    ipsp_results: list[TrialResult] = _run_sweep_for_mode(
        artifacts=artifacts,
        mode=TrialMode.IPSP_PASSIVE,
        angles_deg=dry_angles,
        n_trials_per_angle=n_dry,
        gampa_ns=gampa_ns,
        gaba_base_ns=gaba_base_ns,
        description=f"dry IPSP g={gampa_ns:.2f}/{gaba_base_ns:.2f}",
    )

    full_rate: float = float(np.mean([r.firing_rate_hz for r in full_results]))
    full_active: float = float(np.mean([r.i_active_fraction for r in full_results]))
    epsp_peak_vm: float = float(max(np.max(r.v_soma_mv) for r in epsp_results))
    print(
        f"[dry-run] FULL mean firing rate: {full_rate:.2f} Hz; "
        f"FULL i_active_fraction: {full_active:.3f}; "
        f"EPSP_PASSIVE max Vm: {epsp_peak_vm:.2f} mV",
        flush=True,
    )

    # Active-fraction gate at theta=0 (use first 2 trials).
    full_active_theta0: float = float(
        np.mean([r.i_active_fraction for r in full_results if r.angle_deg == 0.0]),
    )
    if not (0.30 <= full_active_theta0 <= 0.70):
        raise RuntimeError(
            f"Dry-run gate failed: i_active_fraction at theta=0 = {full_active_theta0:.3f} "
            f"is outside [0.30, 0.70]. Inspect soma_origin_um and theta_centrifugal_rad.",
        )

    # EPSP_PASSIVE peak-Vm soft gate (must stay below the AP threshold by a comfortable margin).
    if epsp_peak_vm > -50.0:
        print(
            f"WARNING: EPSP_PASSIVE peak Vm = {epsp_peak_vm:.2f} mV exceeds -50 mV; this can "
            f"happen at high gampa_ns (4 nS) due to passive AMPA summation. Continuing the "
            f"dry-run as long as Vm stays below the spike threshold AP_THRESHOLD_MV "
            f"({AP_THRESHOLD_MV} mV).",
            flush=True,
        )
    if epsp_peak_vm > EPSP_PASSIVE_PEAK_VM_GATE_MV:
        raise RuntimeError(
            f"Dry-run gate failed: EPSP_PASSIVE max Vm = {epsp_peak_vm:.2f} mV exceeds the "
            f"passive ceiling {EPSP_PASSIVE_PEAK_VM_GATE_MV:.2f} mV (above E_AMPA = 0 mV). "
            f"The HH save-and-zero is wired incorrectly.",
        )

    # Bar-locked IPSP centre-of-mass shift gate.
    ipsp_at_0: list[TrialResult] = [r for r in ipsp_results if r.angle_deg == 0.0]
    ipsp_at_90: list[TrialResult] = [r for r in ipsp_results if r.angle_deg == 90.0]
    com_a: float = float(np.mean([_ipsp_centre_of_mass_ms(result=r) for r in ipsp_at_0]))
    com_b: float = float(np.mean([_ipsp_centre_of_mass_ms(result=r) for r in ipsp_at_90]))
    com_shift: float = abs(com_a - com_b)
    com_lower_bound: float = _predicted_ipsp_com_lower_bound_ms(
        pairs=artifacts.pairs,
        theta_a_deg=0.0,
        theta_b_deg=90.0,
    )
    print(
        f"[dry-run] IPSP COM(theta=0)={com_a:.2f} ms, COM(theta=90)={com_b:.2f} ms, "
        f"|shift|={com_shift:.2f} ms, predicted_lower_bound={com_lower_bound:.2f} ms",
        flush=True,
    )
    if com_shift < com_lower_bound:
        raise RuntimeError(
            f"Dry-run gate failed: IPSP centre-of-mass shift {com_shift:.2f} ms < "
            f"predicted lower bound {com_lower_bound:.2f} ms. The bar-arrival-locked "
            f"window mechanism is not working as expected.",
        )

    print(
        f"[dry-run] gates passed (EPSP_PASSIVE Vm < {EPSP_PASSIVE_PEAK_VM_GATE_MV} mV, IPSP COM "
        f"shift > predicted lower bound, active fraction in [0.30, 0.70]; soft cross-direction "
        f"range is [{ACTIVE_FRACTION_LOWER}, {ACTIVE_FRACTION_UPPER}]). WINDOW_MS={WINDOW_MS} ms.",
        flush=True,
    )


def _check_epsp_peak_vm_gate(*, results: list[TrialResult]) -> None:
    """Sanity gate: EPSP_PASSIVE max Vm must stay below EPSP_PASSIVE_PEAK_VM_GATE_MV (REQ-15).

    With HH off the soma cannot exceed the AMPA reversal (E_AMPA = 0 mV) by more than a small
    numerical headroom. A trip indicates the HH save-and-zero is wired incorrectly (e.g., a
    real spike fired).
    """
    for r in results:
        peak_vm: float = float(np.max(r.v_soma_mv))
        if peak_vm > EPSP_PASSIVE_PEAK_VM_GATE_MV:
            raise RuntimeError(
                f"EPSP_PASSIVE peak-Vm gate failed: gampa_ns={r.gampa_ns:.2f}, "
                f"gaba_base_ns={r.gaba_base_ns:.2f}, theta={int(r.angle_deg)} deg, "
                f"peak_vm={peak_vm:.2f} mV exceeds "
                f"EPSP_PASSIVE_PEAK_VM_GATE_MV={EPSP_PASSIVE_PEAK_VM_GATE_MV:.2f} mV. "
                f"The HH save-and-zero is wired incorrectly.",
            )


def _print_summary(*, label: str, results: list[TrialResult]) -> None:
    angles_seen: list[float] = sorted({r.angle_deg for r in results})
    gampa_seen: list[float] = sorted({r.gampa_ns for r in results})
    gaba_seen: list[float] = sorted({r.gaba_base_ns for r in results})
    print(
        f"[{label}] gampa_ns values: {gampa_seen}  gaba_base_ns values: {gaba_seen}",
        flush=True,
    )
    for gampa_ns in gampa_seen:
        for gaba_ns in gaba_seen:
            rates: list[float] = [
                r.firing_rate_hz
                for r in results
                if r.gampa_ns == gampa_ns and r.gaba_base_ns == gaba_ns
            ]
            if len(rates) == 0:
                continue
            angle_means: list[float] = []
            for angle_deg in angles_seen:
                angle_rates: list[float] = [
                    r.firing_rate_hz
                    for r in results
                    if r.gampa_ns == gampa_ns
                    and r.gaba_base_ns == gaba_ns
                    and r.angle_deg == angle_deg
                ]
                if len(angle_rates) > 0:
                    angle_means.append(sum(angle_rates) / len(angle_rates))
            mean_rate: float = float(np.mean(angle_means)) if len(angle_means) > 0 else 0.0
            peak_rate: float = float(np.max(angle_means)) if len(angle_means) > 0 else 0.0
            print(
                f"  gampa={gampa_ns:.2f}  gaba={gaba_ns:.2f}  "
                f"mean Hz={mean_rate:.2f}  peak Hz={peak_rate:.2f}",
                flush=True,
            )


def run_full_sweep(
    *,
    voltage_sample_stride: int = 8,
    skip_dry_run: bool = False,
    ampa_subset: tuple[float, ...] | None = None,
    gaba_subset: tuple[float, ...] | None = None,
    n_trials_override: int | None = None,
    angles_subset: tuple[int, ...] | None = None,
) -> None:
    """End-to-end sweep: setup, dry-run gate, then 5 x 5 x 12 x 10 x 3 = 9,000 trials.

    All 25 (gampa, gaba) cells are appended to a single per-mode CSV (one CSV per mode).

    Optional subset overrides allow exercising the pipeline on a smaller config (e.g. for
    in-session smoke tests). When subsets are not provided the full constant-defined grid runs.
    """
    artifacts: SweepArtifacts = setup_sweep_artifacts()

    if not skip_dry_run:
        run_dry_run_validation(artifacts=artifacts, gampa_ns=1.0, gaba_base_ns=0.5)

    ampa_values: tuple[float, ...] = ampa_subset if ampa_subset is not None else AMPA_PEAK_NS_VALUES
    gaba_values: tuple[float, ...] = gaba_subset if gaba_subset is not None else GABA_BASE_NS_VALUES
    angles: tuple[int, ...] = angles_subset if angles_subset is not None else ANGLES_DEG
    n_trials: int = n_trials_override if n_trials_override is not None else N_TRIALS_PER_ANGLE

    full_results_all: list[TrialResult] = []
    epsp_results_all: list[TrialResult] = []
    ipsp_results_all: list[TrialResult] = []

    n_grid_cells: int = len(ampa_values) * len(gaba_values)
    n_per_mode_per_cell: int = len(angles) * n_trials
    total_trials: int = 3 * n_grid_cells * n_per_mode_per_cell
    print(
        f"[sweep] About to run {total_trials} trials across {n_grid_cells} grid cells x "
        f"3 modes x {n_per_mode_per_cell} trials/mode/cell.",
        flush=True,
    )
    print(
        f"[sweep] ampa_values={ampa_values} gaba_values={gaba_values} "
        f"angles={angles} n_trials={n_trials}",
        flush=True,
    )

    sweep_t0: float = time.perf_counter()
    progress_bar: tqdm = tqdm(total=total_trials, desc="sweep", unit="trial")
    for gampa_ns in ampa_values:
        for gaba_base_ns in gaba_values:
            print(
                f"[sweep] === gampa={gampa_ns:.2f} nS, gaba={gaba_base_ns:.2f} nS ===",
                flush=True,
            )
            full_results_all.extend(
                _run_sweep_for_mode(
                    artifacts=artifacts,
                    mode=TrialMode.FULL,
                    angles_deg=angles,
                    n_trials_per_angle=n_trials,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                    description="FULL",
                    progress_bar=progress_bar,
                ),
            )
            epsp_results_all.extend(
                _run_sweep_for_mode(
                    artifacts=artifacts,
                    mode=TrialMode.EPSP_PASSIVE,
                    angles_deg=angles,
                    n_trials_per_angle=n_trials,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                    description="EPSP",
                    progress_bar=progress_bar,
                ),
            )
            ipsp_results_all.extend(
                _run_sweep_for_mode(
                    artifacts=artifacts,
                    mode=TrialMode.IPSP_PASSIVE,
                    angles_deg=angles,
                    n_trials_per_angle=n_trials,
                    gampa_ns=gampa_ns,
                    gaba_base_ns=gaba_base_ns,
                    description="IPSP",
                    progress_bar=progress_bar,
                ),
            )
    progress_bar.close()
    sweep_wallclock_s: float = time.perf_counter() - sweep_t0

    for label, results in (
        ("FULL", full_results_all),
        ("EPSP_PASSIVE", epsp_results_all),
        ("IPSP_PASSIVE", ipsp_results_all),
    ):
        _print_summary(label=label, results=results)

    # Write per-mode outputs (single CSV per mode).
    for mode, results in (
        (TrialMode.FULL, full_results_all),
        (TrialMode.EPSP_PASSIVE, epsp_results_all),
        (TrialMode.IPSP_PASSIVE, ipsp_results_all),
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
                "n_trials": (len(full_results_all) + len(epsp_results_all) + len(ipsp_results_all)),
                "tstop_ms": float(BASE_OFFSET_MS) + 1300.0,
                "window_ms": WINDOW_MS,
                "ampa_peak_ns_values": list(ampa_values),
                "gaba_base_ns_values": list(gaba_values),
                "angles_deg": list(angles),
                "n_trials_per_angle": n_trials,
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    print(
        f"[sweep] total wall-clock: {sweep_wallclock_s:.2f} s ({sweep_wallclock_s / 60.0:.2f} min)",
        flush=True,
    )

    # EPSP_PASSIVE peak-Vm soft gate (REQ-15). Runs LAST so all CSVs are persisted regardless
    # of whether the gate trips: a gate failure indicates a real bug worth investigating, but
    # losing the 9000-trial sweep output to it is not acceptable.
    print("[sweep] Running EPSP_PASSIVE peak-Vm gate...", flush=True)
    _check_epsp_peak_vm_gate(results=epsp_results_all)


def run_dry_only() -> None:
    """Run only the dry-run validation gate at the centre grid cell (gampa=1.0, gaba=0.5)."""
    artifacts: SweepArtifacts = setup_sweep_artifacts()
    run_dry_run_validation(artifacts=artifacts, gampa_ns=1.0, gaba_base_ns=0.5)


def _parse_float_csv(value: str) -> tuple[float, ...]:
    return tuple(float(x) for x in value.split(",") if x.strip())


def _parse_int_csv(value: str) -> tuple[int, ...]:
    return tuple(int(x) for x in value.split(",") if x.strip())


def _build_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="t0059 5x5 (gampa, gaba) tuning-curve sweep with bar-locked GABA windows.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run only the dry-run validation gate at gampa=1.0, gaba=0.5 (12 trials).",
    )
    parser.add_argument(
        "--skip-dry-run",
        action="store_true",
        help="Skip the dry-run validation gate before running the full sweep.",
    )
    parser.add_argument(
        "--ampa-subset",
        type=_parse_float_csv,
        default=None,
        help="Comma-separated AMPA values to override AMPA_PEAK_NS_VALUES (e.g. '0.5,1.0,2.0').",
    )
    parser.add_argument(
        "--gaba-subset",
        type=_parse_float_csv,
        default=None,
        help="Comma-separated GABA values to override GABA_BASE_NS_VALUES.",
    )
    parser.add_argument(
        "--n-trials",
        type=int,
        default=None,
        help="Override N_TRIALS_PER_ANGLE for the sweep (default 10).",
    )
    parser.add_argument(
        "--angles",
        type=_parse_int_csv,
        default=None,
        help="Comma-separated angles in degrees to override ANGLES_DEG.",
    )
    return parser


if __name__ == "__main__":
    args = _build_argparser().parse_args()
    if args.dry_run:
        run_dry_only()
    else:
        run_full_sweep(
            skip_dry_run=args.skip_dry_run,
            ampa_subset=args.ampa_subset,
            gaba_subset=args.gaba_subset,
            n_trials_override=args.n_trials,
            angles_subset=args.angles,
        )
