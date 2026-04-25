"""SEClamp simulation wrapper for t0049 channel-isolation conductance re-measurement.

Inserts a NEURON ``SEClamp`` at the soma of the deposited DSGC after applying channel-
isolation overrides, runs the simulation under voltage clamp at -65 mV, and returns the peak
clamp current. The downstream ``compute_metrics.py`` converts current to per-channel somatic-
equivalent conductance via ``g_nS = abs(i_pA) / abs(V_clamp - E_rev)``.

Sign convention: NEURON's SEClamp ``_ref_i`` is positive when current flows from clamp INTO
the cell. At -65 mV with reversal potential 0 mV (NMDA / AMPA), inward synaptic currents
require the clamp to source current (negative ``_ref_i``); we use ``abs()`` so derived
conductance is always positive.

Override pattern: ``simplerun()`` rebinds ``b2gnmda``, ``b2gampa``, and other globals every
call. The only correct way to apply non-canonical conductances is to (a) call
``simplerun()`` to trigger the deposited stimulus generator and ``placeBIP()``, (b) override
the desired globals from Python, (c) re-call ``h("update()")`` and ``h("placeBIP()")``,
(d) attach the SEClamp + recorders, (e) ``finitialize`` + ``continuerun``. Pattern adapted
from t0046 ``run_simplerun.py:135-151``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

# Bootstrap NEURON before any t0046 import that touches HOC.
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import (
    ensure_neuron_importable,
)

ensure_neuron_importable()

from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import (  # noqa: E402
    assert_bip_positions_baseline,
    reset_globals_to_canonical,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import (  # noqa: E402
    PSP_BASELINE_MS,
    TSTOP_MS,
    V_INIT_MV,
    Direction,
    ExperimentType,
)
from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import (  # noqa: E402
    _ensure_cell,
)
from tasks.t0049_seclamp_cond_remeasure.code.constants import (  # noqa: E402
    AMP1_MV,
    B2GNMDA_NS,
    CLAMP_VOLTAGE_TOLERANCE_MV,
    DT_RECORD_MS,
    NA_TO_PA,
    RS_MOHM,
    ChannelIsolation,
)


@dataclass(frozen=True, slots=True)
class SeclampTrialResult:
    """One channel-isolation SEClamp trial output."""

    direction: Direction
    channel_on: ChannelIsolation
    trial_seed: int
    b2gnmda_ns: float
    peak_i_pa: float
    baseline_i_pa: float
    peak_i_minus_baseline_pa: float
    clamp_v_sd_mv: float


def _apply_channel_overrides(*, h: Any, channel_on: ChannelIsolation) -> None:
    """Write the HOC globals that zero specific synaptic channels.

    The deposited bipolarNMDA.mod releases AMPA and NMDA on the same vesicle; ``b2gampa = 0``
    silences only AMPA per-vesicle conductance while NMDA continues, and vice versa.
    ``gabaMOD = 0`` zeroes the SAC inhibitory wave amplitude in ``mulnoise.fill(...)`` and is
    the cleanest "GABA-off" switch.
    """
    if channel_on == ChannelIsolation.ALL:
        return
    if channel_on == ChannelIsolation.AMPA_ONLY:
        h.b2gnmda = 0.0
        h.gabaMOD = 0.0
        return
    if channel_on == ChannelIsolation.NMDA_ONLY:
        h.b2gampa = 0.0
        h.gabaMOD = 0.0
        return
    if channel_on == ChannelIsolation.GABA_ONLY:
        h.b2gnmda = 0.0
        h.b2gampa = 0.0
        return
    raise ValueError(f"Unknown channel isolation: {channel_on}")


def run_seclamp_trial(
    *,
    direction: Direction,
    channel_on: ChannelIsolation,
    trial_seed: int,
) -> SeclampTrialResult:
    """Run one SEClamp trial under the requested channel isolation."""
    h, baseline = _ensure_cell()

    # Set canonical globals + per-trial overrides BEFORE simplerun.
    reset_globals_to_canonical(h=h)
    h.flickerVAR = 0.0
    h.stimnoiseVAR = 0.0
    h.b2gnmda = float(B2GNMDA_NS)
    h.seed2 = int(trial_seed)
    h.SpikesOn = 0
    h.nmdaOn = 1

    # Run simplerun() to trigger the deposited stimulus + placeBIP. This first run is
    # discarded; the recorded run happens after the channel-isolation override + re-placeBIP +
    # SEClamp insertion below.
    h.simplerun(int(ExperimentType.CONTROL), int(direction))

    # Apply channel-isolation overrides AFTER simplerun (which clobbers many globals).
    _apply_channel_overrides(h=h, channel_on=channel_on)

    # Re-place synapses with the now-overridden conductance globals (Lesson Learned 5 from
    # t0046 research-code: simplerun's late writes mean we must re-update + re-placeBIP).
    h("update()")
    h("placeBIP()")

    # Insert the SEClamp at the soma. Keep the Python reference alive for the duration of
    # this trial — releasing the binding would let NEURON GC the clamp object mid-run.
    clamp: Any = h.SEClamp(h.RGC.soma(0.5))
    clamp.dur1 = float(TSTOP_MS)
    clamp.amp1 = float(AMP1_MV)
    clamp.rs = float(RS_MOHM)

    # Attach fresh recorders.
    i_rec: Any = h.Vector()
    i_rec.record(clamp._ref_i, DT_RECORD_MS)
    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v, DT_RECORD_MS)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t, DT_RECORD_MS)

    # Run the recorded simulation under voltage clamp.
    h.finitialize(V_INIT_MV)
    h.continuerun(TSTOP_MS)

    # Sanity: BIP positions did not drift mid-sweep.
    assert_bip_positions_baseline(h=h, baseline=baseline)

    # Convert clamp current from nA -> pA. SEClamp _ref_i units are nA in NEURON.
    i_arr_na: np.ndarray = np.array(list(i_rec), dtype=np.float64)
    v_arr_mv: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr_ms: np.ndarray = np.array(list(t_rec), dtype=np.float64)

    if i_arr_na.size == 0:
        raise RuntimeError("No SEClamp samples recorded; finitialize/continuerun were not run.")

    i_arr_pa: np.ndarray = i_arr_na * NA_TO_PA

    # Baseline mean over the pre-stimulus window.
    baseline_mask: np.ndarray = t_arr_ms < PSP_BASELINE_MS
    if not bool(baseline_mask.any()):
        baseline_i_pa: float = 0.0
    else:
        baseline_i_pa = float(i_arr_pa[baseline_mask].mean())

    # Peak |i - baseline| across the trial.
    i_centered_pa: np.ndarray = i_arr_pa - baseline_i_pa
    peak_signed_pa: float = float(i_centered_pa[np.argmax(np.abs(i_centered_pa))])
    peak_i_minus_baseline_pa: float = float(np.max(np.abs(i_centered_pa)))
    peak_i_pa: float = peak_signed_pa  # signed for diagnostic; abs in compute_metrics.

    # Clamp-quality assertion: soma voltage SD across the trial should be < 0.5 mV.
    clamp_v_sd_mv: float = float(v_arr_mv.std())
    if clamp_v_sd_mv >= CLAMP_VOLTAGE_TOLERANCE_MV:
        print(
            f"[seclamp warn] direction={direction.name} channel={channel_on.value} "
            f"seed={trial_seed} clamp_v_sd_mv={clamp_v_sd_mv:.4f} >= "
            f"{CLAMP_VOLTAGE_TOLERANCE_MV} mV; clamp may be drifting.",
            flush=True,
        )

    return SeclampTrialResult(
        direction=direction,
        channel_on=channel_on,
        trial_seed=trial_seed,
        b2gnmda_ns=float(B2GNMDA_NS),
        peak_i_pa=peak_i_pa,
        baseline_i_pa=baseline_i_pa,
        peak_i_minus_baseline_pa=peak_i_minus_baseline_pa,
        clamp_v_sd_mv=clamp_v_sd_mv,
    )
