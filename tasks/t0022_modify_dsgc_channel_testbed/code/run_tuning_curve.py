"""Run the 12-angle x 10-trial per-dendrite E-I moving-bar sweep.

Inherits the t0008 HOC cell (``RGCmodel.hoc`` + ``dsgc_model.hoc``) via the
registered library ``modeldb_189347_dsgc``, adds an extra HOC overlay
(``dsgc_channel_partition.hoc``) that exposes five channel-modular
SectionLists, and drives the per-trial firing via a new
``run_one_trial_dendritic`` function that inserts one AMPA and one GABA_A
Exp2Syn per ON-dendrite and schedules their onsets as a function of
bar direction.

Key differences from t0008:

* **No BIP synapse-coordinate rotation.** BIP/SAC coordinates stay at their
  baseline snapshot; only the per-EiPair NetStim start times change per
  angle.
* **No gabaMOD scalar swap.** ``h.gabaMOD`` is held at its baseline value
  (0.33). A per-trial assertion verifies this and that BIP coordinates
  remain at their baseline (guards against the t0008 rotation logic or a
  t0020 gabaMOD swap silently re-engaging).
* **Per-dendrite E-I pairs.** On each ON-dendrite section, an AMPA
  ``Exp2Syn`` at ``sec(0.9)`` and a GABA_A ``Exp2Syn`` at ``sec(0.3)`` are
  created once during cell build. Each is driven by a dedicated NetStim
  running in burst mode (``number=N_SYN_EVENTS``, ``noise=0``,
  ``interval=SYN_EVENT_INTERVAL_MS``, ``start`` set per trial).

The CSV schema is the canonical t0004/t0012 format:
``(angle_deg, trial_seed, firing_rate_hz)``. One row per (angle, trial).

Per-trial seed: ``seed = 1000 * angle_idx + trial_idx + 1``. This is a
deterministic 3-tuple analogue for the Random123 convention used by
NEURON's native noise streams.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from dataclasses import dataclass
from typing import Any

from tasks.t0022_modify_dsgc_channel_testbed.code.neuron_bootstrap import (
    ensure_neuron_importable,
)

ensure_neuron_importable()


# ruff: noqa: E402  -- deferred imports; NEURON bootstrap must run first.
from tqdm import tqdm

from tasks.t0008_port_modeldb_189347.code import build_cell as _t0008_build_cell
from tasks.t0008_port_modeldb_189347.code.build_cell import (
    SynapseCoords,
    apply_params,
    build_dsgc,
    get_cell_summary,
    read_synapse_coords,
)
from tasks.t0022_modify_dsgc_channel_testbed.code.constants import (
    AMPA_CONDUCTANCE_NS,
    AMPA_REVERSAL_MV,
    AMPA_SEG_LOCATION,
    AMPA_TAU1_MS,
    AMPA_TAU2_MS,
    ANGLE_STEP_DEG,
    AP_THRESHOLD_MV,
    BAR_BASE_ONSET_MS,
    BAR_VELOCITY_UM_PER_MS,
    CSV_COLUMN_ANGLE_DEG,
    CSV_COLUMN_FIRING_RATE_HZ,
    CSV_COLUMN_TRIAL_SEED,
    EI_OFFSET_NULL_MS,
    EI_OFFSET_PREFERRED_MS,
    GABA_CONDUCTANCE_NULL_NS,
    GABA_CONDUCTANCE_PREFERRED_NS,
    GABA_REVERSAL_MV,
    GABA_SEG_LOCATION,
    GABA_TAU1_MS,
    GABA_TAU2_MS,
    N_ANGLES,
    N_SYN_EVENTS,
    N_TRIALS,
    PREFLIGHT_ANGLES_DEG,
    PREFLIGHT_N_TRIALS,
    SYN_EVENT_INTERVAL_MS,
    TSTOP_MS,
    V_INIT_MV,
)
from tasks.t0022_modify_dsgc_channel_testbed.code.paths import (
    CHANNEL_PARTITION_HOC,
    CHANNEL_PARTITION_HOC_SAFE,
    MODELDB_NRNMECH_DLL,
    PREFLIGHT_CURVE_CSV,
    PREFLIGHT_DIR,
    PREFLIGHT_ONSETS_JSON,
    TUNING_CURVE_DENDRITIC_CSV,
    TUNING_CURVES_DIR,
)


@dataclass(frozen=True, slots=True)
class EiPair:
    """Per-dendrite excitation-inhibition synapse pair with azimuth tag.

    NetStim-based burst scheduler: each synapse is driven by a NetStim
    point process configured with ``number=N_SYN_EVENTS, noise=0``,
    ``interval=SYN_EVENT_INTERVAL_MS``, and a ``start`` time set per
    trial. The short regular burst approximates the BIPsyn's continuous
    drive across the bar-sweep window. Using NetStim (rather than
    VecStim) avoids a dependency on the optional ``vecevent.mod`` that
    is not bundled with the Windows NEURON install at this workstation.
    """

    dendrite_index: int
    ampa_syn: Any
    gaba_syn: Any
    ampa_netstim: Any
    gaba_netstim: Any
    ampa_netcon: Any
    gaba_netcon: Any
    x_mid_um: float
    y_mid_um: float
    azimuth_deg: float


@dataclass(frozen=True, slots=True)
class TrialResult:
    """Firing-rate outcome of one (angle, seed) trial."""

    angle_deg: float
    trial_seed: int
    firing_rate_hz: float


def _preload_nrnmech_dll() -> None:
    """Preload the t0022-compiled nrnmech.dll and bypass t0008's lookup.

    t0008's ``load_neuron`` looks for ``nrnmech.dll`` in its own
    ``MODELDB_BUILD_DIR``. Because this worktree builds the DLL under
    t0022's ``build/modeldb_189347/``, we manually call
    ``h.nrn_load_dll`` on our DLL, source ``stdrun.hoc``, and set the
    internal ``_loaded`` sentinel so t0008's ``load_neuron`` becomes a
    no-op re-entry and does not try to load a non-existent t0008 DLL.
    """
    if not MODELDB_NRNMECH_DLL.exists():
        raise FileNotFoundError(
            f"nrnmech.dll missing at {MODELDB_NRNMECH_DLL}. "
            "Run ``nrnivmodl`` on the t0008 bundled MOD sources into "
            f"{MODELDB_NRNMECH_DLL.parent}.",
        )
    # Ensure NEURONHOME env + DLL directory are already set by
    # ensure_neuron_importable(); we are safe to import neuron now.
    from neuron import h  # noqa: PLC0415

    if getattr(_t0008_build_cell.load_neuron, "_loaded", False):
        return
    loaded: float = h.nrn_load_dll(str(MODELDB_NRNMECH_DLL))
    assert loaded == 1.0, f"h.nrn_load_dll failed for {MODELDB_NRNMECH_DLL}"
    loaded_std: float = h.load_file("stdrun.hoc")
    assert loaded_std == 1.0, "h.load_file('stdrun.hoc') failed"
    _t0008_build_cell.load_neuron._loaded = True  # type: ignore[attr-defined]


def _source_channel_partition_hoc(*, h: Any) -> None:
    """Source the channel-modular HOC overlay.

    Must be called after ``build_dsgc()`` so ``RGC.soma``/``RGC.dends`` are
    defined. HOC path literals on Windows must use forward slashes.
    """
    if not CHANNEL_PARTITION_HOC.exists():
        raise FileNotFoundError(
            f"dsgc_channel_partition.hoc missing at {CHANNEL_PARTITION_HOC}",
        )
    loaded: float = h.load_file(1, CHANNEL_PARTITION_HOC_SAFE)
    assert loaded == 1.0, f"h.load_file({CHANNEL_PARTITION_HOC_SAFE}) failed"


def _section_midpoint(*, sec: Any) -> tuple[float, float]:
    """Return (x_mid, y_mid) in micrometres for a NEURON section.

    Uses ``x3d(i)`` / ``y3d(i)`` calls, averaging over the 3D points that
    define the section's shape. Falls back to (0, 0) if the section has
    no 3D points (not expected for the bundled morphology).
    """
    n_points: int = int(sec.n3d())
    if n_points == 0:
        return (0.0, 0.0)
    x_sum: float = 0.0
    y_sum: float = 0.0
    for i in range(n_points):
        x_sum += float(sec.x3d(i))
        y_sum += float(sec.y3d(i))
    return (x_sum / n_points, y_sum / n_points)


def build_ei_pairs(*, h: Any) -> list[EiPair]:
    """Build per-ON-dendrite AMPA/GABA_A Exp2Syn pairs with NetStim drivers.

    One AMPA synapse at ``sec(AMPA_SEG_LOCATION)`` (distal, 0.9) and one
    GABA_A synapse at ``sec(GABA_SEG_LOCATION)`` (proximal, 0.3) per
    section in ``h.RGC.ON``. Each synapse owns its own NetStim and NetCon
    so the per-angle onset scheduling does not spill across pairs.
    """
    pairs: list[EiPair] = []
    # ``h.RGC.ON`` is a NEURON SectionList. Iterate by asking HOC to walk
    # it into a Python list of section names; this is the same pattern
    # used by t0008's build_cell when counting ``countON``.
    # Using sec.push() + h.pop_section() pattern here to be explicit.
    for dendrite_index, sec in enumerate(h.RGC.ON):
        x_mid_um, y_mid_um = _section_midpoint(sec=sec)
        azimuth_rad: float = math.atan2(y_mid_um, x_mid_um)
        azimuth_deg: float = math.degrees(azimuth_rad)

        ampa_syn: Any = h.Exp2Syn(sec(AMPA_SEG_LOCATION))
        ampa_syn.tau1 = AMPA_TAU1_MS
        ampa_syn.tau2 = AMPA_TAU2_MS
        ampa_syn.e = AMPA_REVERSAL_MV

        gaba_syn: Any = h.Exp2Syn(sec(GABA_SEG_LOCATION))
        gaba_syn.tau1 = GABA_TAU1_MS
        gaba_syn.tau2 = GABA_TAU2_MS
        gaba_syn.e = GABA_REVERSAL_MV

        ampa_netstim: Any = h.NetStim()
        ampa_netstim.number = N_SYN_EVENTS
        ampa_netstim.noise = 0.0
        ampa_netstim.interval = SYN_EVENT_INTERVAL_MS

        gaba_netstim: Any = h.NetStim()
        gaba_netstim.number = N_SYN_EVENTS
        gaba_netstim.noise = 0.0
        gaba_netstim.interval = SYN_EVENT_INTERVAL_MS

        ampa_netcon: Any = h.NetCon(ampa_netstim, ampa_syn)
        ampa_netcon.delay = 0.0
        ampa_netcon.weight[0] = AMPA_CONDUCTANCE_NS * 1e-3

        gaba_netcon: Any = h.NetCon(gaba_netstim, gaba_syn)
        gaba_netcon.delay = 0.0
        gaba_netcon.weight[0] = GABA_CONDUCTANCE_PREFERRED_NS * 1e-3

        pairs.append(
            EiPair(
                dendrite_index=dendrite_index,
                ampa_syn=ampa_syn,
                gaba_syn=gaba_syn,
                ampa_netstim=ampa_netstim,
                gaba_netstim=gaba_netstim,
                ampa_netcon=ampa_netcon,
                gaba_netcon=gaba_netcon,
                x_mid_um=x_mid_um,
                y_mid_um=y_mid_um,
                azimuth_deg=azimuth_deg,
            ),
        )

    return pairs


def _angular_delta_deg(*, azimuth_deg: float, bar_direction_deg: float) -> float:
    """Signed minimum angular difference in degrees, in [-180, 180]."""
    delta: float = (bar_direction_deg - azimuth_deg + 540.0) % 360.0 - 180.0
    return delta


def _is_preferred(*, delta_deg: float) -> bool:
    """A pair is on the 'preferred side' if |delta| < 90 deg."""
    return abs(delta_deg) < 90.0


def _compute_onset_times_ms(
    *,
    pair: EiPair,
    angle_deg: float,
    velocity_um_per_ms: float,
) -> tuple[float, float]:
    """Return (ampa_onset_ms, gaba_onset_ms) for this pair at this angle.

    The bar's leading edge reaches each synapse at
    ``t_bar = (x * cos theta + y * sin theta) / velocity + base_offset``.
    base_offset shifts all onsets to positive simulation times.

    In the preferred half (|delta| < 90), AMPA precedes GABA by
    ``EI_OFFSET_PREFERRED_MS``. In the null half, GABA precedes AMPA by
    the same magnitude (``EI_OFFSET_NULL_MS`` is negative).
    """
    theta_rad: float = math.radians(angle_deg)
    t_bar_ms: float = (
        pair.x_mid_um * math.cos(theta_rad) + pair.y_mid_um * math.sin(theta_rad)
    ) / velocity_um_per_ms + BAR_BASE_ONSET_MS

    delta_deg: float = _angular_delta_deg(
        azimuth_deg=pair.azimuth_deg,
        bar_direction_deg=angle_deg,
    )
    if _is_preferred(delta_deg=delta_deg):
        ampa_onset_ms: float = t_bar_ms
        gaba_onset_ms: float = t_bar_ms + EI_OFFSET_PREFERRED_MS
    else:
        # Null half: GABA arrives first, AMPA lags by |EI_OFFSET_NULL_MS|.
        gaba_onset_ms = t_bar_ms
        ampa_onset_ms = t_bar_ms + abs(EI_OFFSET_NULL_MS)
    return (ampa_onset_ms, gaba_onset_ms)


def schedule_ei_onsets(
    *,
    h: Any,  # noqa: ARG001  -- reserved for future Random-seeded jitter
    pairs: list[EiPair],
    angle_deg: float,
    velocity_um_per_ms: float,
    gaba_null_pref_ratio: float,
    trial_seed: int,  # noqa: ARG001  -- reserved for future jitter injection
) -> list[dict[str, float]]:
    """Set per-pair NetStim.start times and GABA NetCon weights.

    Returns a list of debug dicts (one per pair) suitable for dumping to
    ``logs/preflight/onsets.json`` for visual inspection.
    """
    debug_rows: list[dict[str, float]] = []
    preferred_weight_us: float = GABA_CONDUCTANCE_PREFERRED_NS * 1e-3
    null_weight_us: float = GABA_CONDUCTANCE_PREFERRED_NS * gaba_null_pref_ratio * 1e-3
    # Guard: ensure null_weight_us matches GABA_CONDUCTANCE_NULL_NS.
    expected_null_us: float = GABA_CONDUCTANCE_NULL_NS * 1e-3
    assert abs(null_weight_us - expected_null_us) < 1e-9, (
        f"null GABA weight mismatch: {null_weight_us} vs {expected_null_us}"
    )

    for pair in pairs:
        ampa_onset_ms, gaba_onset_ms = _compute_onset_times_ms(
            pair=pair,
            angle_deg=angle_deg,
            velocity_um_per_ms=velocity_um_per_ms,
        )

        delta_deg: float = _angular_delta_deg(
            azimuth_deg=pair.azimuth_deg,
            bar_direction_deg=angle_deg,
        )
        is_preferred: bool = _is_preferred(delta_deg=delta_deg)
        pair.gaba_netcon.weight[0] = preferred_weight_us if is_preferred else null_weight_us

        pair.ampa_netstim.start = ampa_onset_ms
        pair.gaba_netstim.start = gaba_onset_ms

        debug_rows.append(
            {
                "dendrite_index": pair.dendrite_index,
                "x_mid_um": pair.x_mid_um,
                "y_mid_um": pair.y_mid_um,
                "azimuth_deg": pair.azimuth_deg,
                "delta_deg": delta_deg,
                "is_preferred": 1.0 if is_preferred else 0.0,
                "ampa_onset_ms": ampa_onset_ms,
                "gaba_onset_ms": gaba_onset_ms,
                "gaba_weight_us": pair.gaba_netcon.weight[0],
            },
        )
    return debug_rows


def _assert_bip_and_gabamod_baseline(
    *,
    h: Any,
    baseline_coords: list[SynapseCoords],
    baseline_gaba_mod: float,
) -> None:
    """Fire if gabaMOD or any BIPsyn coord drifted from baseline."""
    assert h.gabaMOD == baseline_gaba_mod, (
        f"h.gabaMOD = {h.gabaMOD} != baseline {baseline_gaba_mod}; gabaMOD swap re-engaged?"
    )
    for s in baseline_coords:
        assert h.RGC.BIPsyn[s.index].locx == s.bip_locx_um, (
            f"BIPsyn[{s.index}].locx = {h.RGC.BIPsyn[s.index].locx} "
            f"!= baseline {s.bip_locx_um}; rotation logic re-engaged?"
        )
        assert h.RGC.BIPsyn[s.index].locy == s.bip_locy_um, (
            f"BIPsyn[{s.index}].locy = {h.RGC.BIPsyn[s.index].locy} "
            f"!= baseline {s.bip_locy_um}; rotation logic re-engaged?"
        )


def _count_threshold_crossings(*, samples: list[float], threshold_mv: float) -> int:
    """Count upward crossings of ``threshold_mv`` in ``samples``."""
    if len(samples) == 0:
        return 0
    spike_count: int = 0
    above: bool = samples[0] >= threshold_mv
    for val in samples[1:]:
        now_above: bool = val >= threshold_mv
        if now_above and not above:
            spike_count += 1
        above = now_above
    return spike_count


def _silence_baseline_hoc_synapses(*, h: Any) -> None:
    """Zero out t0008's bundled BIP/SAC synaptic conductances.

    The t0008 ``apply_params`` sets ``h.b2gampa``, ``h.b2gnmda``,
    ``h.s2ggaba``, ``h.s2gach`` and the ACh/GABA modulation scalars to
    their Poleg-Polsky defaults, which on their own drive 13-15 Hz
    spiking even with no moving bar. For the t0022 per-dendrite E-I
    driver we want firing to be produced exclusively by the NetStim-
    driven AMPA/GABA_A pairs we insert ourselves, so we zero the
    bundled synaptic conductances after ``apply_params`` each trial.

    Calls ``update()`` + ``placeBIP()`` so the scalar zeros propagate
    to the per-synapse BIPsyn/SACinhibsyn/SACexcsyn instances. Without
    these HOC procs the scalars sit in globals but the synapse objects
    retain the Poleg-Polsky defaults.
    """
    h.b2gampa = 0.0
    h.b2gnmda = 0.0
    h.s2ggaba = 0.0
    h.s2gach = 0.0
    h("update()")
    h("placeBIP()")


def run_one_trial_dendritic(
    *,
    h: Any,
    pairs: list[EiPair],
    angle_deg: float,
    trial_seed: int,
    baseline_coords: list[SynapseCoords],
    baseline_gaba_mod: float,
) -> float:
    """Run one per-dendrite E-I trial and return firing rate in Hz."""
    apply_params(h, seed=trial_seed)
    _silence_baseline_hoc_synapses(h=h)
    _assert_bip_and_gabamod_baseline(
        h=h,
        baseline_coords=baseline_coords,
        baseline_gaba_mod=baseline_gaba_mod,
    )

    schedule_ei_onsets(
        h=h,
        pairs=pairs,
        angle_deg=angle_deg,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS,
        trial_seed=trial_seed,
    )

    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)

    h.finitialize(V_INIT_MV)
    h.continuerun(TSTOP_MS)

    samples: list[float] = [float(v) for v in v_rec]
    spike_count: int = _count_threshold_crossings(
        samples=samples,
        threshold_mv=AP_THRESHOLD_MV,
    )
    tstop_s: float = TSTOP_MS / 1000.0
    return float(spike_count) / tstop_s


def _run_sweep(
    *,
    h: Any,
    pairs: list[EiPair],
    baseline_coords: list[SynapseCoords],
    baseline_gaba_mod: float,
    angles_deg: tuple[float, ...],
    n_trials: int,
    label: str,
) -> list[TrialResult]:
    """Execute (angles x trials) trials and return per-trial firing rates."""
    results: list[TrialResult] = []
    total_trials: int = len(angles_deg) * n_trials
    bar = tqdm(total=total_trials, desc=label, unit="trial")
    for angle_idx, angle_deg in enumerate(angles_deg):
        for trial_idx in range(n_trials):
            trial_seed: int = 1000 * angle_idx + trial_idx + 1
            rate_hz: float = run_one_trial_dendritic(
                h=h,
                pairs=pairs,
                angle_deg=angle_deg,
                trial_seed=trial_seed,
                baseline_coords=baseline_coords,
                baseline_gaba_mod=baseline_gaba_mod,
            )
            results.append(
                TrialResult(
                    angle_deg=angle_deg,
                    trial_seed=trial_seed,
                    firing_rate_hz=rate_hz,
                ),
            )
            bar.update(1)
    bar.close()
    return results


def _write_csv(*, results: list[TrialResult], out_path: Any) -> None:
    """Write per-trial firing rates to the canonical CSV schema."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [
                CSV_COLUMN_ANGLE_DEG,
                CSV_COLUMN_TRIAL_SEED,
                CSV_COLUMN_FIRING_RATE_HZ,
            ],
        )
        for r in results:
            writer.writerow(
                [int(r.angle_deg), r.trial_seed, f"{r.firing_rate_hz:.6f}"],
            )


def _print_per_angle_summary(*, results: list[TrialResult]) -> None:
    """Print mean firing rate per angle (for quick eyeballing)."""
    angles_seen: list[float] = sorted({r.angle_deg for r in results})
    print("", flush=True)
    for angle_deg in angles_seen:
        rates_at_angle: list[float] = [
            r.firing_rate_hz for r in results if r.angle_deg == angle_deg
        ]
        mean_rate: float = sum(rates_at_angle) / len(rates_at_angle)
        print(
            f"  angle={int(angle_deg):3d} deg  mean={mean_rate:6.2f} Hz  (n={len(rates_at_angle)})",
            flush=True,
        )


def _main_dry_run() -> int:
    """Build the cell, source the partition HOC, build E-I pairs; no run."""
    print("Dry run: preloading nrnmech.dll...", flush=True)
    _preload_nrnmech_dll()
    print("Dry run: building DSGC cell...", flush=True)
    h = build_dsgc()
    summary = get_cell_summary(h=h)
    print(
        f"  countON={summary.num_on_sections} numsyn={summary.num_synapses}",
        flush=True,
    )

    print("Sourcing channel-partition HOC overlay...", flush=True)
    _source_channel_partition_hoc(h=h)

    print("Building per-dendrite E-I pairs...", flush=True)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    print(f"  Built {len(pairs)} EiPair objects", flush=True)

    assert len(pairs) >= 200, (
        f"Expected >=200 EiPair objects (ON-dendrite count ~282); got {len(pairs)}"
    )
    print("Dry run succeeded.", flush=True)
    return 0


def _main_preflight() -> int:
    """Run the 4-angle x 2-trial validation gate."""
    print("Preflight: preloading nrnmech.dll...", flush=True)
    _preload_nrnmech_dll()
    print("Preflight: building DSGC cell...", flush=True)
    h = build_dsgc()
    _source_channel_partition_hoc(h=h)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    baseline_gaba_mod: float = float(h.gabaMOD)
    print(
        f"  EiPair count = {len(pairs)}, gabaMOD baseline = {baseline_gaba_mod}",
        flush=True,
    )

    PREFLIGHT_DIR.mkdir(parents=True, exist_ok=True)

    # Dump debug onsets for angle 0 (preferred) and 180 (null) before the run.
    debug_0: list[dict[str, float]] = schedule_ei_onsets(
        h=h,
        pairs=pairs,
        angle_deg=0.0,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS,
        trial_seed=1,
    )
    debug_180: list[dict[str, float]] = schedule_ei_onsets(
        h=h,
        pairs=pairs,
        angle_deg=180.0,
        velocity_um_per_ms=BAR_VELOCITY_UM_PER_MS,
        gaba_null_pref_ratio=GABA_CONDUCTANCE_NULL_NS / GABA_CONDUCTANCE_PREFERRED_NS,
        trial_seed=1,
    )
    PREFLIGHT_ONSETS_JSON.write_text(
        json.dumps(
            {"angle_0": debug_0, "angle_180": debug_180},
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"  wrote debug onsets to {PREFLIGHT_ONSETS_JSON}", flush=True)

    results: list[TrialResult] = _run_sweep(
        h=h,
        pairs=pairs,
        baseline_coords=baseline_coords,
        baseline_gaba_mod=baseline_gaba_mod,
        angles_deg=PREFLIGHT_ANGLES_DEG,
        n_trials=PREFLIGHT_N_TRIALS,
        label="preflight",
    )
    _write_csv(results=results, out_path=PREFLIGHT_CURVE_CSV)
    _print_per_angle_summary(results=results)
    print(f"\nWrote {PREFLIGHT_CURVE_CSV}", flush=True)
    return 0


def _main_full_sweep() -> int:
    """[CRITICAL] Run the full 12-angle x N_TRIALS sweep."""
    print("Preloading nrnmech.dll...", flush=True)
    _preload_nrnmech_dll()
    print("Building DSGC cell for full sweep...", flush=True)
    h = build_dsgc()
    _source_channel_partition_hoc(h=h)
    pairs: list[EiPair] = build_ei_pairs(h=h)
    baseline_coords: list[SynapseCoords] = read_synapse_coords(h=h)
    baseline_gaba_mod: float = float(h.gabaMOD)
    print(
        f"  EiPair count = {len(pairs)}, gabaMOD baseline = {baseline_gaba_mod}",
        flush=True,
    )

    angles_deg: tuple[float, ...] = tuple(float(i) * ANGLE_STEP_DEG for i in range(N_ANGLES))
    TUNING_CURVES_DIR.mkdir(parents=True, exist_ok=True)
    results: list[TrialResult] = _run_sweep(
        h=h,
        pairs=pairs,
        baseline_coords=baseline_coords,
        baseline_gaba_mod=baseline_gaba_mod,
        angles_deg=angles_deg,
        n_trials=N_TRIALS,
        label="sweep",
    )
    _write_csv(results=results, out_path=TUNING_CURVE_DENDRITIC_CSV)
    _print_per_angle_summary(results=results)
    print(f"\nWrote {TUNING_CURVE_DENDRITIC_CSV}", flush=True)
    return 0


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the t0022 per-dendrite E-I moving-bar sweep. "
            "Default: 12 angles x 10 trials (full sweep)."
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build cell + source partition HOC + build EiPairs; do not run.",
    )
    parser.add_argument(
        "--preflight",
        action="store_true",
        help="Run 4 angles x 2 trials preflight validation (no full sweep).",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    if args.dry_run:
        return _main_dry_run()
    if args.preflight:
        return _main_preflight()
    return _main_full_sweep()


if __name__ == "__main__":
    sys.exit(main())
