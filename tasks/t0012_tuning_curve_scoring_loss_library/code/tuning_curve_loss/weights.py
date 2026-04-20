"""Default weights and half-widths for the weighted-Euclidean loss.

Default weights are 0.25 each across the four axes. Half-widths normalise each residual to a
fraction of the envelope half-width, so that a residual at the envelope boundary contributes
~1.0 per-axis before weighting.
"""

from __future__ import annotations

import json
from pathlib import Path

WEIGHT_KEYS: frozenset[str] = frozenset({"dsi", "peak", "null", "hwhm"})


DEFAULT_WEIGHTS: dict[str, float] = {
    "dsi": 0.25,
    "peak": 0.25,
    "null": 0.25,
    "hwhm": 0.25,
}


# Envelope half-widths used by scoring to normalise each residual.
# Kept at literature values even though PEAK_ENVELOPE_HZ was widened to (30, 80);
# the half-width keeps the scalar comparable to earlier analyses.
ENVELOPE_HALF_WIDTHS: dict[str, float] = {
    "dsi": 0.075,
    "peak": 20.0,
    "null": 5.0,
    "hwhm": 15.0,
}


def validate_weights(*, weights: dict[str, float]) -> None:
    """Validate a weights dict. Raises ``ValueError`` on any structural problem.

    Rules:
    1. Keys must exactly equal ``{"dsi", "peak", "null", "hwhm"}``.
    2. No value may be negative.
    3. Sum must be > 0.

    The sum is intentionally NOT required to equal 1.0 — callers often feed in raw relative
    weights; the scoring function does not need a unit-sum assumption.
    """
    key_set: frozenset[str] = frozenset(weights.keys())
    if key_set != WEIGHT_KEYS:
        raise ValueError(
            f"weights keys must be exactly {sorted(WEIGHT_KEYS)!r}; got {sorted(key_set)!r}"
        )
    for key, value in weights.items():
        if value < 0:
            raise ValueError(f"weights[{key!r}] = {value!r} is negative; must be >= 0")
    total: float = sum(weights.values())
    if total == 0.0:
        raise ValueError(f"weights sum to zero: {weights!r}; at least one weight must be positive")


def load_weights_from_json(*, json_path: Path) -> dict[str, float]:
    """Load and validate a weights dict from a JSON file."""
    raw: str = json_path.read_text(encoding="utf-8")
    data: object = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError(f"weights JSON must be an object; got {type(data).__name__}")
    # Cast to dict[str, float] after validation.
    weights: dict[str, float] = {}
    for key, value in data.items():
        if not isinstance(key, str):
            raise ValueError(f"weights JSON keys must be strings; got {type(key).__name__}")
        if not isinstance(value, int | float):
            raise ValueError(f"weights[{key!r}] must be numeric; got {type(value).__name__}")
        weights[key] = float(value)
    validate_weights(weights=weights)
    return weights
