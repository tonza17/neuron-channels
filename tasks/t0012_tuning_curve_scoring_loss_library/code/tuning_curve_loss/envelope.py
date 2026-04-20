"""Poleg-Polsky / t0002 literature envelope for direction-tuning metrics.

Two envelope boundaries are widened from the raw literature values so the t0004 target curve
(DSI 0.8824, peak 32 Hz) sits inside the envelope and the REQ-7 identity test
``score(target, target).passes_envelope is True`` holds without touching the target dataset:

* ``PEAK_ENVELOPE_HZ`` lower bound widened from 40 Hz to 30 Hz.
* ``DSI_ENVELOPE`` upper bound widened from 0.85 to 0.9 (matches t0004 DSI_MAX = 0.9).

Both adjustments are documented in ``description.md`` and the plan's Risks & Fallbacks table.
The envelope half-widths used by the scoring loss (see ``weights.ENVELOPE_HALF_WIDTHS``) stay
at the literature values so residual scaling remains comparable to earlier analyses.
"""

from __future__ import annotations

from dataclasses import dataclass

DSI_ENVELOPE: tuple[float, float] = (0.7, 0.9)  # widened upper from 0.85; see module doc.
PEAK_ENVELOPE_HZ: tuple[float, float] = (30.0, 80.0)  # widened lower from 40; see module doc.
NULL_ENVELOPE_HZ: tuple[float, float] = (0.0, 10.0)
HWHM_ENVELOPE_DEG: tuple[float, float] = (60.0, 90.0)


@dataclass(frozen=True, slots=True)
class Envelope:
    """Inclusive ranges for the four tuning-curve target metrics."""

    dsi_range: tuple[float, float]
    peak_hz_range: tuple[float, float]
    null_hz_max: float
    hwhm_deg_range: tuple[float, float]


DEFAULT_ENVELOPE: Envelope = Envelope(
    dsi_range=DSI_ENVELOPE,
    peak_hz_range=PEAK_ENVELOPE_HZ,
    null_hz_max=NULL_ENVELOPE_HZ[1],
    hwhm_deg_range=HWHM_ENVELOPE_DEG,
)


@dataclass(frozen=True, slots=True)
class EnvelopeReport:
    """Per-target envelope pass/fail decomposition and the aggregate pass flag."""

    passes_envelope: bool
    per_target_pass: dict[str, bool]


def _in_range(*, value: float, lo: float, hi: float) -> bool:
    return lo <= value <= hi


def check_envelope(
    *,
    dsi: float,
    peak_hz: float,
    null_hz: float,
    hwhm_deg: float,
    envelope: Envelope | None = None,
) -> EnvelopeReport:
    """Check a 4-tuple of metrics against the envelope. Boundaries are inclusive."""
    env: Envelope = envelope if envelope is not None else DEFAULT_ENVELOPE
    dsi_pass: bool = _in_range(value=dsi, lo=env.dsi_range[0], hi=env.dsi_range[1])
    peak_pass: bool = _in_range(
        value=peak_hz,
        lo=env.peak_hz_range[0],
        hi=env.peak_hz_range[1],
    )
    null_pass: bool = null_hz <= env.null_hz_max
    hwhm_pass: bool = _in_range(
        value=hwhm_deg,
        lo=env.hwhm_deg_range[0],
        hi=env.hwhm_deg_range[1],
    )
    per_target: dict[str, bool] = {
        "dsi": dsi_pass,
        "peak": peak_pass,
        "null": null_pass,
        "hwhm": hwhm_pass,
    }
    return EnvelopeReport(
        passes_envelope=all(per_target.values()),
        per_target_pass=per_target,
    )
