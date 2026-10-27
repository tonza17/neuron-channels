"""Panel D toy model: Naka-Rushton static nonlinearity plus a leaky rate integrator.

``f(u) = b + r_max * u^n / (u^n + k^n)``; ``tau dr/dt = -r + f(u_ref * s(t))`` where ``s(t)`` is the
three-Gaussian input (peak 1). The relative signal is ``r(t) / f(u_ref)`` (the saturated steady
state of the same cell type), an assumption: panel D does not state its normalisation.
"""

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.panel_d_metrics import input_signal


@dataclass(frozen=True, slots=True)
class ToyParams:
    b: float
    r_max: float
    k: float
    n: float
    tau_ms: float


def rate_static(*, u: NDArray[np.float64] | float, params: ToyParams) -> NDArray[np.float64]:
    uu = np.asarray(u, dtype=np.float64)
    un = np.power(np.maximum(uu, 0.0), params.n)
    out: NDArray[np.float64] = params.b + params.r_max * un / (un + params.k**params.n)
    return out


@dataclass(frozen=True, slots=True)
class PulseTrace:
    t_ms: NDArray[np.float64]
    rate: NDArray[np.float64]
    relative: NDArray[np.float64]


def simulate_pulse_response(
    *,
    params: ToyParams,
    u_ref: float,
    tstop_ms: float,
    dt_ms: float,
) -> PulseTrace:
    t = np.arange(0.0, tstop_ms, dt_ms, dtype=np.float64)
    drive = rate_static(u=u_ref * input_signal(t_ms=t), params=params)
    r = np.zeros_like(t)
    r[0] = float(rate_static(u=0.0, params=params))
    alpha = dt_ms / params.tau_ms
    for i in range(1, len(t)):
        r[i] = r[i - 1] + alpha * (drive[i - 1] - r[i - 1])
    norm = float(rate_static(u=u_ref, params=params))
    return PulseTrace(t_ms=t, rate=r, relative=r / norm)
