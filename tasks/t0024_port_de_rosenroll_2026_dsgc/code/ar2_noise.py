"""AR(2) correlated release-rate noise for paired ACh/GABA channels.

Implements the paper's per-synapse release-rate noise process. Two scalar AR(2)
streams (one for ACh, one for GABA) are driven by a shared Gaussian innovation
plus an independent component to achieve a target cross-channel correlation
``rho``. ``rho = 0.6`` reproduces the paper's correlated condition; ``rho = 0.0``
is the decorrelated / AMB control.

The AR(2) recursion is

    x_{t} = phi_1 * x_{t-1} + phi_2 * x_{t-2} + eps_t

with ``phi = (0.9, -0.1)`` (plan REQ-1). The two streams share the innovation
component ``rho * z_t`` and draw independent residual innovations
``sqrt(1 - rho**2) * z_ach/gaba``.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True, slots=True)
class AR2NoiseParams:
    n_samples: int
    phi: tuple[float, float]
    rho: float
    seed: int
    innov_scale: float = 1.0


def generate_ar2_process(
    *,
    n_samples: int,
    phi: tuple[float, float],
    rho: float,
    seed: int,
    innov_scale: float = 1.0,
) -> NDArray[np.float64]:
    """Generate an (n_samples, 2) array of [ach_rate, gaba_rate] AR(2) traces.

    Each column is an AR(2) process with coefficients ``phi`` and Gaussian
    innovations; the two columns share a fraction ``rho`` of their innovation,
    producing an empirical cross-correlation close to ``rho`` at lag 0.

    Args:
        n_samples: Length of the series (time steps).
        phi: AR(2) coefficients ``(phi_1, phi_2)``.
        rho: Target cross-channel correlation, in ``[-1, 1]``.
        seed: Seed for numpy's ``default_rng``.
        innov_scale: Standard deviation of the Gaussian innovation.
    """
    batch: NDArray[np.float64] = generate_ar2_batch(
        n_samples=n_samples,
        n_streams=1,
        phi=phi,
        rho=rho,
        seed=seed,
        innov_scale=innov_scale,
    )
    out: NDArray[np.float64] = batch[0]
    return out


def generate_ar2_batch(
    *,
    n_samples: int,
    n_streams: int,
    phi: tuple[float, float],
    rho: float,
    seed: int,
    innov_scale: float = 1.0,
) -> NDArray[np.float64]:
    """Vectorised version generating ``n_streams`` independent 2-channel AR(2) traces.

    Returns an ``(n_streams, n_samples, 2)`` array. Each stream has the same
    AR(2) dynamics and cross-channel correlation ``rho`` but independent
    innovations (streams are uncorrelated with each other).
    """
    assert n_samples > 0, "n_samples must be positive"
    assert n_streams > 0, "n_streams must be positive"
    assert -1.0 <= rho <= 1.0, "rho must be in [-1, 1]"
    assert innov_scale > 0.0, "innov_scale must be positive"

    rng = np.random.default_rng(seed)
    # Draw (n_streams, n_samples, 2) innovations.
    z = rng.standard_normal((n_streams, n_samples, 2)) * innov_scale
    residual_factor = float(np.sqrt(max(0.0, 1.0 - rho * rho)))
    # eps_ach = z1; eps_gaba = rho * z1 + sqrt(1 - rho^2) * z2.
    eps_ach = z[:, :, 0]
    eps_gaba = rho * z[:, :, 0] + residual_factor * z[:, :, 1]
    # Stack back; shape (n_streams, n_samples, 2).
    eps = np.stack([eps_ach, eps_gaba], axis=-1)

    trace = np.zeros((n_streams, n_samples, 2), dtype=np.float64)
    phi_1, phi_2 = phi
    # First two samples: prev values are zero.
    trace[:, 0, :] = eps[:, 0, :]
    if n_samples > 1:
        trace[:, 1, :] = phi_1 * trace[:, 0, :] + eps[:, 1, :]
    for t in range(2, n_samples):
        trace[:, t, :] = phi_1 * trace[:, t - 1, :] + phi_2 * trace[:, t - 2, :] + eps[:, t, :]

    return trace


def _self_test() -> int:
    """Empirically validate phi and rho within 0.05 tolerance."""
    n = 100_000
    phi = (0.9, -0.1)
    rho_target = 0.6
    trace = generate_ar2_process(
        n_samples=n,
        phi=phi,
        rho=rho_target,
        seed=42,
    )

    # Cross-correlation at lag 0.
    ach = trace[:, 0]
    gaba = trace[:, 1]
    ach_centered = ach - ach.mean()
    gaba_centered = gaba - gaba.mean()
    cross_corr = float(
        (ach_centered * gaba_centered).sum()
        / np.sqrt((ach_centered**2).sum() * (gaba_centered**2).sum())
    )

    # Lag-1 autocorrelation (for phi_1 sanity).
    ach_lag1 = float((ach_centered[1:] * ach_centered[:-1]).sum() / (ach_centered**2).sum())

    print(f"  target rho = {rho_target:.3f}, empirical = {cross_corr:.3f}")
    print(f"  target lag-1 autocorr ~ {phi[0] / (1 - phi[1]):.3f}, empirical = {ach_lag1:.3f}")

    rho_ok = abs(cross_corr - rho_target) < 0.05
    # For AR(2), lag-1 autocorr equals phi_1 / (1 - phi_2) in the stationary limit.
    autocorr_target = phi[0] / (1 - phi[1])
    autocorr_ok = abs(ach_lag1 - autocorr_target) < 0.05

    if rho_ok and autocorr_ok:
        print("AR(2) self-test PASSED.")
        return 0
    print("AR(2) self-test FAILED.")
    return 1


if __name__ == "__main__":
    import sys

    sys.exit(_self_test())
