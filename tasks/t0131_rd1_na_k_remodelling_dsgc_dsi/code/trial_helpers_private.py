"""Private trial helpers copied from the t0080/t0129 ``trial_helpers.py`` (t0024 origin)."""

import numpy as np
from numpy.typing import NDArray

from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24
from tasks.t0024_port_de_rosenroll_2026_dsgc.code.ar2_noise import generate_ar2_batch

RATE_DT_MS: float = 1.0
BAR_SIGMA_MS: float = 30.0
BASE_ACH_PROB: float = 0.5
PREF_GABA_PROB: float = 0.05
NULL_GABA_PROB: float = 0.80
CELL_PREF_DEG: float = 0.0


def gaba_prob_for_direction(*, direction_deg: float) -> float:
    d = abs((direction_deg - CELL_PREF_DEG + 180.0) % 360.0 - 180.0)
    sigmoid_val: float = float(1.0 - 0.98 / (1.0 + np.exp((d - 91.0) / 25.0)))
    return PREF_GABA_PROB + (NULL_GABA_PROB - PREF_GABA_PROB) * sigmoid_val


def bar_arrival_times(
    *,
    syn_xy: NDArray[np.float64],
    origin_xy: tuple[float, float],
    direction_deg: float,
) -> NDArray[np.float64]:
    theta = np.radians(direction_deg)
    ux, uy = float(np.cos(theta)), float(np.sin(theta))
    dx = syn_xy[:, 0] - origin_xy[0]
    dy = syn_xy[:, 1] - origin_xy[1]
    proj = dx * ux + dy * uy
    return C24.BAR_START_TIME_MS + (proj - C24.BAR_X_START_UM) / C24.BAR_VELOCITY_UM_PER_MS


def rates_with_ar2_noise(
    *,
    n_syn: int,
    n_bins: int,
    rate_dt_ms: float,
    arrival_times_ms: NDArray[np.float64],
    rho: float,
    seed: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    t_ms = np.arange(n_bins, dtype=np.float64) * rate_dt_ms
    traces = generate_ar2_batch(
        n_samples=n_bins,
        n_streams=n_syn,
        phi=C24.AR2_PHI,
        rho=rho,
        seed=seed,
        innov_scale=C24.AR2_INNOV_SCALE,
    )
    env = np.exp(-0.5 * ((t_ms[None, :] - arrival_times_ms[:, None]) / BAR_SIGMA_MS) ** 2)
    base = C24.AR2_BASE_RATE_HZ * env
    ach = np.clip(base * (1.0 + traces[:, :, 0]), a_min=0.0, a_max=None)
    gaba = np.clip(base * (1.0 + traces[:, :, 1]), a_min=0.0, a_max=None)
    return ach, gaba


def rates_to_events(
    *,
    rates_hz: NDArray[np.float64],
    release_prob: NDArray[np.float64],
    rate_dt_ms: float,
    rng: np.random.Generator,
) -> list[list[float]]:
    n_syn, n_bins = rates_hz.shape
    lam = rates_hz * (rate_dt_ms / 1000.0) * release_prob[:, None]
    counts = rng.poisson(lam=lam)
    events: list[list[float]] = []
    for s in range(n_syn):
        syn_events: list[float] = []
        for b in range(n_bins):
            k = int(counts[s, b])
            if k == 0:
                continue
            jitter = rng.uniform(0.0, rate_dt_ms, size=k)
            t0 = b * rate_dt_ms
            for j in jitter:
                syn_events.append(float(t0 + j))
        syn_events.sort()
        events.append(syn_events)
    return events


def count_spikes(*, v_trace: NDArray[np.float64], threshold_mv: float) -> int:
    above = v_trace > threshold_mv
    return int(np.sum((~above[:-1]) & above[1:]))


def rates_with_envelope(
    *,
    n_syn: int,
    n_bins: int,
    envelope: NDArray[np.float64],
    rho: float,
    seed: int,
) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
    """Per-synapse rates with a common 1-D envelope (peak 1) and the same AR(2) noise as bars."""
    assert envelope.shape == (n_bins,), "envelope has one value per rate bin"
    traces = generate_ar2_batch(
        n_samples=n_bins,
        n_streams=n_syn,
        phi=C24.AR2_PHI,
        rho=rho,
        seed=seed,
        innov_scale=C24.AR2_INNOV_SCALE,
    )
    base = C24.AR2_BASE_RATE_HZ * envelope[None, :]
    ach = np.clip(base * (1.0 + traces[:, :, 0]), a_min=0.0, a_max=None)
    gaba = np.clip(base * (1.0 + traces[:, :, 1]), a_min=0.0, a_max=None)
    return ach, gaba
