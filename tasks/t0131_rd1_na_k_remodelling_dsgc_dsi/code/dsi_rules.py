"""Pure DSI summarisation rules (no NEURON): signed antipodal DSI with the None guard.

Rule (t0131): DSI is ``None`` when the PD spike count summed over seeds is below
``LOW_COUNT_PD_SPIKES`` (the silence guard) -- never -1.0 and never 0.0. The raw counts are
always returned. ``dsi_unguarded`` is a diagnostic computed whenever PD + ND spikes > 0.
"""

from dataclasses import dataclass

import numpy as np

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    LOW_COUNT_PD_SPIKES,
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
    TSTOP_MS,
)


@dataclass(frozen=True, slots=True)
class TrialCount:
    direction_deg: float
    seed_index: int
    spike_count: int
    peak_mv: float | None
    error: str | None


@dataclass(frozen=True, slots=True)
class ConditionSummary:
    dsi_signed: float | None
    dsi_unguarded: float | None
    pd_spikes: int
    nd_spikes: int
    pd_rate_hz: float | None
    nd_rate_hz: float | None
    low_count: bool
    n_trials: int
    n_errors: int
    mean_counts_per_direction: dict[str, float]


def signed_dsi_from_means(*, mean_pd: float, mean_nd: float) -> float | None:
    denom: float = mean_pd + mean_nd
    if denom <= 0.0:
        return None
    return (mean_pd - mean_nd) / denom


def summarise_counts(*, trials: list[TrialCount]) -> ConditionSummary:
    ok: list[TrialCount] = [t for t in trials if t.error is None]
    n_errors: int = len(trials) - len(ok)
    pd_counts: list[int] = [
        t.spike_count for t in ok if abs(t.direction_deg - PD_DIRECTION_DEG) < 1e-6
    ]
    nd_counts: list[int] = [
        t.spike_count for t in ok if abs(t.direction_deg - ND_DIRECTION_DEG) < 1e-6
    ]
    per_dir: dict[str, list[int]] = {}
    for t in ok:
        per_dir.setdefault(f"{int(round(t.direction_deg))}", []).append(t.spike_count)
    mean_per_dir: dict[str, float] = {k: float(np.mean(v)) for k, v in per_dir.items()}
    if len(pd_counts) == 0 or len(nd_counts) == 0:
        return ConditionSummary(
            dsi_signed=None,
            dsi_unguarded=None,
            pd_spikes=int(sum(pd_counts)),
            nd_spikes=int(sum(nd_counts)),
            pd_rate_hz=None,
            nd_rate_hz=None,
            low_count=True,
            n_trials=len(trials),
            n_errors=n_errors,
            mean_counts_per_direction=mean_per_dir,
        )
    pd_sum: int = int(sum(pd_counts))
    nd_sum: int = int(sum(nd_counts))
    mean_pd: float = float(np.mean(pd_counts))
    mean_nd: float = float(np.mean(nd_counts))
    low_count: bool = pd_sum < LOW_COUNT_PD_SPIKES
    unguarded: float | None = signed_dsi_from_means(mean_pd=mean_pd, mean_nd=mean_nd)
    dsi: float | None = None if low_count else unguarded
    secs: float = TSTOP_MS / 1000.0
    return ConditionSummary(
        dsi_signed=dsi,
        dsi_unguarded=unguarded,
        pd_spikes=pd_sum,
        nd_spikes=nd_sum,
        pd_rate_hz=mean_pd / secs,
        nd_rate_hz=mean_nd / secs,
        low_count=low_count,
        n_trials=len(trials),
        n_errors=n_errors,
        mean_counts_per_direction=mean_per_dir,
    )
