"""Scoring helper: one-sided ROC AUC of PD peaks vs trial baselines.

Source: ``tasks/t0046_reproduce_poleg_polsky_2016_exact/code/compute_metrics.py:142-158``
(``_roc_auc_pd_vs_baseline``, ~17 lines). Copied not imported because t0046's helper is
private (single leading underscore) and not part of any registered library.
"""

from __future__ import annotations


def compute_roc_auc_pd_vs_baseline(
    *,
    pd_values: list[float],
    baselines: list[float],
) -> float | None:
    """One-sided ROC AUC: P(PD peak > baseline mean), averaged over all PD x baseline pairs.

    Sklearn-style: positives = PD peaks, negatives = baseline means. AUC range is [0, 1].
    Returns ``None`` when either input is empty.
    """
    n_pos: int = len(pd_values)
    n_neg: int = len(baselines)
    if n_pos == 0 or n_neg == 0:
        return None
    correct: int = 0
    for p in pd_values:
        for b in baselines:
            if p > b:
                correct += 1
            # Ties contribute 0 (per t0046 convention; halving is omitted for stability).
    return float(correct) / float(n_pos * n_neg)
