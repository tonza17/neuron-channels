"""Tonic bias current (DC plus optional Gaussian white noise) injected at the soma."""

from dataclasses import dataclass
from typing import Any

import numpy as np


@dataclass(frozen=True, slots=True)
class BiasSpec:
    i_bias_pa: float
    sigma_noise_pa: float
    noise_seed: int


@dataclass(slots=True)
class BiasHandles:
    dc_clamp: Any
    noise_clamp: Any | None
    noise_vec: Any | None


def attach_bias(
    *,
    h: Any,
    soma: Any,
    bias: BiasSpec,
    tstop_ms: float,
    dt_ms: float,
) -> BiasHandles:
    """DC IClamp (``i_bias_pa``) for the whole run plus a noise IClamp driven by a Vector."""
    dc = h.IClamp(soma(0.5))
    dc.delay = 0.0
    dc.dur = tstop_ms + 1000.0
    dc.amp = bias.i_bias_pa / 1000.0
    noise_clamp: Any | None = None
    noise_vec: Any | None = None
    if bias.sigma_noise_pa > 0.0:
        n_samples: int = int(np.ceil(tstop_ms / dt_ms)) + 2
        rng = np.random.default_rng(bias.noise_seed)
        samples = rng.normal(loc=0.0, scale=bias.sigma_noise_pa / 1000.0, size=n_samples)
        noise_vec = h.Vector(samples.tolist())
        noise_clamp = h.IClamp(soma(0.5))
        noise_clamp.delay = 0.0
        noise_clamp.dur = tstop_ms + 1000.0
        noise_vec.play(noise_clamp._ref_amp, dt_ms)
    return BiasHandles(dc_clamp=dc, noise_clamp=noise_clamp, noise_vec=noise_vec)


def detach_bias(*, handles: BiasHandles) -> None:
    if handles.noise_vec is not None:
        handles.noise_vec.play_remove()
    handles.dc_clamp.amp = 0.0
    if handles.noise_clamp is not None:
        handles.noise_clamp.amp = 0.0
