"""Bar-locked IPSP envelope regression test (REQ-13).

Runs two IPSP_PASSIVE trials at the centre grid cell (gampa_ns=1.0, gaba_base_ns=1.0), one at
``theta=0`` and one at ``theta=90``. Computes the centre of mass of |v(t) - V_INIT_MV| over
each trial, and asserts that the absolute difference between the two centres of mass exceeds
a coarse predicted lower bound derived from the per-synapse onset latencies.

If the t0057 global-window mechanism were used instead of t0059's bar-arrival-locked mechanism,
the IPSP envelope shape would be the same at both directions (only the gating mask would
differ), so the centre-of-mass shift would collapse to ~0 ms. A strictly-positive shift here
indicates the per-synapse window mechanism is wired correctly.
"""

from __future__ import annotations

import math

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import (
    BAR_VELOCITY_UM_PER_MS,
    V_INIT_MV,
    TrialMode,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve import (
    SweepArtifacts,
    setup_sweep_artifacts,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.synapses import (
    _onset_time_ms,
    i_synapse_fires,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.trial import (
    TrialResult,
    run_one_trial,
)


def _ipsp_centre_of_mass_ms(*, result: TrialResult) -> float:
    weights: np.ndarray = np.abs(result.v_soma_mv - V_INIT_MV)
    if float(np.sum(weights)) == 0.0:
        return 0.0
    return float(np.sum(weights * result.t_ms) / np.sum(weights))


def _predicted_lower_bound_ms(*, artifacts: SweepArtifacts) -> float:
    """Coarse lower bound: ``|mean_onset(0) - mean_onset(90)| / 2``.

    Uses the bar-arrival-time formula on the active (firing) subset for each direction.
    """

    def _direction_onset_mean(angle_deg: float) -> float:
        active_onsets: list[float] = []
        for pair in artifacts.pairs:
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

    a: float = _direction_onset_mean(angle_deg=0.0)
    b: float = _direction_onset_mean(angle_deg=90.0)
    return abs(a - b) / 2.0


def test_bar_locked_ipsp_envelope_shifts_with_direction() -> None:
    """The IPSP centre of mass at theta=0 and theta=90 must differ by >= predicted_lower_bound."""
    artifacts: SweepArtifacts = setup_sweep_artifacts()
    from neuron import h  # noqa: PLC0415

    print("[bar-locked-ipsp] Running IPSP_PASSIVE trial at theta=0...", flush=True)
    res_0: TrialResult = run_one_trial(
        h=h,
        cell=artifacts.cell,
        pairs=artifacts.pairs,
        mode=TrialMode.IPSP_PASSIVE,
        angle_deg=0.0,
        trial_seed=1,
        gampa_ns=1.0,
        gaba_base_ns=1.0,
    )
    print("[bar-locked-ipsp] Running IPSP_PASSIVE trial at theta=90...", flush=True)
    res_90: TrialResult = run_one_trial(
        h=h,
        cell=artifacts.cell,
        pairs=artifacts.pairs,
        mode=TrialMode.IPSP_PASSIVE,
        angle_deg=90.0,
        trial_seed=2,
        gampa_ns=1.0,
        gaba_base_ns=1.0,
    )
    com_0: float = _ipsp_centre_of_mass_ms(result=res_0)
    com_90: float = _ipsp_centre_of_mass_ms(result=res_90)
    com_shift: float = abs(com_0 - com_90)
    lower_bound: float = _predicted_lower_bound_ms(artifacts=artifacts)
    print(
        f"[bar-locked-ipsp] COM(theta=0)={com_0:.2f} ms, COM(theta=90)={com_90:.2f} ms, "
        f"|shift|={com_shift:.2f} ms, predicted_lower_bound={lower_bound:.2f} ms",
        flush=True,
    )
    assert com_shift >= lower_bound, (
        f"Bar-locked IPSP envelope test failed: |COM(0) - COM(90)| = {com_shift:.4f} ms < "
        f"predicted lower bound {lower_bound:.4f} ms. The per-synapse bar-arrival-locked "
        f"window mechanism is not producing direction-dependent IPSP timing."
    )


if __name__ == "__main__":
    test_bar_locked_ipsp_envelope_shifts_with_direction()
    print("[bar-locked-ipsp] PASS", flush=True)
