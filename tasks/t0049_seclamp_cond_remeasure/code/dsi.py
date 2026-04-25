"""DSI helper copied verbatim from t0047.

Source: ``tasks/t0047_validate_pp16_fig3_cond_noise/code/dsi.py``. t0047 is NOT a registered
library, so the project cross-task copy rule applies (rule from the implementation skill).
The function ``compute_dsi_pd_nd`` is the only API used by t0049's ``compute_metrics.py``.
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

    Returns ``None`` when either input is empty. Returns ``0.0`` when the means sum to zero
    (degenerate case, e.g. both means exactly zero).
    """
    pd_mean: float | None = _mean(pd_values)
    nd_mean: float | None = _mean(nd_values)
    if pd_mean is None or nd_mean is None:
        return None
    if pd_mean + nd_mean == 0.0:
        return 0.0
    return float((pd_mean - nd_mean) / (pd_mean + nd_mean))
