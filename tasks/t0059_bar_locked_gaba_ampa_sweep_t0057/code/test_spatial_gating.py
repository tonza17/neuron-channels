"""Unit tests for the t0059 spatial centripetal-gating I-synapse rule.

Copied bit-for-bit from ``tasks/t0057_tonic_gaba_sweep_t0053/code/test_spatial_gating.py`` per
CLAUDE.md rule 3. Only the import prefix is rewritten; the spatial-gating predicate is unchanged
between t0057 and t0059.
"""

from __future__ import annotations

import math

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.synapses import i_synapse_fires


def test_pd_side_does_not_fire() -> None:
    """At theta_stim = theta_centrifugal (cos = +1), the gate is silent."""
    fired: bool = i_synapse_fires(theta_stim_deg=0.0, theta_centrifugal_deg=0.0)
    assert fired is False, (
        f"Expected silent gate at theta_stim=0, theta_centrifugal=0; got fired={fired}"
    )


def test_nd_side_fires() -> None:
    """At theta_stim - theta_centrifugal = 180 (cos = -1), the gate fires."""
    fired: bool = i_synapse_fires(theta_stim_deg=180.0, theta_centrifugal_deg=0.0)
    assert fired is True, (
        f"Expected fired gate at theta_stim=180, theta_centrifugal=0; got fired={fired}"
    )


def test_perpendicular_does_not_fire() -> None:
    """Strict inequality cos < 0; at exactly 90 deg cos = 0 so the gate is silent."""
    fired: bool = i_synapse_fires(theta_stim_deg=90.0, theta_centrifugal_deg=0.0)
    assert fired is False, (
        f"Expected silent gate at theta_stim=90, theta_centrifugal=0; got fired={fired}"
    )


def test_uniform_random_active_fraction_near_half() -> None:
    """Place 1,000 synapses with uniform-random centrifugal angles; ~50% should fire at theta=0."""
    rng: np.random.Generator = np.random.default_rng(seed=42)
    n_synapses: int = 1000
    centrifugal_angles_rad: np.ndarray = rng.uniform(low=0.0, high=2.0 * math.pi, size=n_synapses)
    centrifugal_angles_deg: np.ndarray = np.rad2deg(centrifugal_angles_rad)
    n_fired: int = 0
    for theta_centrifugal_deg in centrifugal_angles_deg:
        if i_synapse_fires(theta_stim_deg=0.0, theta_centrifugal_deg=float(theta_centrifugal_deg)):
            n_fired += 1
    active_fraction: float = float(n_fired) / float(n_synapses)
    print(
        f"[spatial_gating] uniform-random active fraction at theta_stim=0: "
        f"{active_fraction:.4f} (n={n_synapses})",
        flush=True,
    )
    assert 0.45 <= active_fraction <= 0.55, (
        f"Active fraction {active_fraction:.4f} not within 0.5 +/- 0.05 for uniform-random "
        f"centrifugal angles at theta_stim=0"
    )


if __name__ == "__main__":
    test_pd_side_does_not_fire()
    test_nd_side_fires()
    test_perpendicular_does_not_fire()
    test_uniform_random_active_fraction_near_half()
    print("[spatial_gating] PASS", flush=True)
