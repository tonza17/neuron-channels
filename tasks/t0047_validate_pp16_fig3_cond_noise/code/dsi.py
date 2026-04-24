"""DSI helper copied from t0046 (kept inline per t0012-incompat note in the plan).

Source: ``tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:100-124``
(``_mean`` and ``_dsi`` helpers, ~12 lines combined). Copied not imported because the
t0012 ``compute_dsi`` library function requires a 12-angle TuningCurve and we have only
PD vs ND values; constructing a 12-angle curve to satisfy the library would mask intent.
"""

from __future__ import annotations

from collections.abc import Iterable


def _mean(values: Iterable[float]) -> float | None:
    seq: list[float] = list(values)
    if len(seq) == 0:
        return None
    return float(sum(seq) / len(seq))


def compute_dsi_pd_nd(
    *,
    pd_values: list[float],
    nd_values: list[float],
) -> float | None:
    """Compute classic DSI = (PD_mean - ND_mean) / (PD_mean + ND_mean).

    Returns ``None`` when either input is empty. Returns ``0.0`` when the means
    sum to zero (degenerate case, e.g. both means exactly zero).
    """
    pd_mean: float | None = _mean(pd_values)
    nd_mean: float | None = _mean(nd_values)
    if pd_mean is None or nd_mean is None:
        return None
    if pd_mean + nd_mean == 0.0:
        return 0.0
    return float((pd_mean - nd_mean) / (pd_mean + nd_mean))
