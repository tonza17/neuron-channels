"""IPSP-sustained-window regression test (REQ-13).

Loads ``results/voltage_traces_gaba_only.csv``, pivots by (gaba_base_ns, angle_deg, sample_idx) to
get the mean voltage, and for the most-active direction (theta = 210 deg per t0053's spatial-
gating polar) asserts for each of the 5 conductance values:

    abs(v_at_1300_ms - V_INIT_MV) >= 0.5 * abs(v_at_200_ms - V_INIT_MV)

This is the headline t0057 quality gate: without it, the new tonic mechanism could silently
degrade back to the t0053 Exp2Syn-event-decay behaviour. The test runs as a pytest module after
the full sweep is complete; if no GABA_ONLY voltage CSV is present the test is skipped.
"""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from tasks.t0057_tonic_gaba_sweep_t0053.code.constants import (
    COL_ANGLE_DEG,
    COL_GABA_BASE_NS,
    COL_SAMPLE_IDX,
    COL_T_MS,
    COL_TRIAL_SEED,
    COL_VOLTAGE_MV,
    GABA_BASE_NS_VALUES,
    IPSP_SUSTAINED_RATIO,
    IPSP_SUSTAINED_T_EARLY_MS,
    IPSP_SUSTAINED_T_LATE_MS,
    IPSP_SUSTAINED_THETA_DEG,
    V_INIT_MV,
)
from tasks.t0057_tonic_gaba_sweep_t0053.code.paths import VOLTAGE_TRACES_GABA_ONLY_CSV


def _voltage_pivot_per_angle_gaba(
    *,
    df: pd.DataFrame,
    angle_deg: int,
    gaba_base_ns: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (t_ms, mean_v) arrays for the given (angle, gaba_base_ns)."""
    sub: pd.DataFrame = df[
        (df[COL_ANGLE_DEG] == angle_deg)
        & (np.isclose(df[COL_GABA_BASE_NS], gaba_base_ns, atol=1e-6))
    ]
    if len(sub) == 0:
        return (np.zeros(0), np.zeros(0))
    pivot: pd.DataFrame = sub.pivot_table(
        index=COL_SAMPLE_IDX,
        columns=COL_TRIAL_SEED,
        values=COL_VOLTAGE_MV,
    )
    pivot = pivot.dropna(axis=0, how="any")
    sample_indices: np.ndarray = pivot.index.to_numpy(dtype=np.int64)
    voltage_matrix: np.ndarray = pivot.to_numpy(dtype=np.float64)
    mean_v: np.ndarray = voltage_matrix.mean(axis=1)
    representative_seed = pivot.columns[0]
    t_lookup: pd.DataFrame = sub[sub[COL_TRIAL_SEED] == representative_seed][
        [COL_SAMPLE_IDX, COL_T_MS]
    ].drop_duplicates(subset=COL_SAMPLE_IDX)
    t_lookup = t_lookup.set_index(COL_SAMPLE_IDX).reindex(sample_indices)
    t_ms: np.ndarray = t_lookup[COL_T_MS].to_numpy(dtype=np.float64)
    return (t_ms, mean_v)


@pytest.mark.parametrize("gaba_base_ns", GABA_BASE_NS_VALUES)
def test_ipsp_sustained_window(gaba_base_ns: float) -> None:
    """For the most-active direction, IPSP voltage at t=1300 ms is at least 50% of t=200 ms."""
    if not VOLTAGE_TRACES_GABA_ONLY_CSV.exists():
        pytest.skip(f"GABA_ONLY voltage trace CSV not found at {VOLTAGE_TRACES_GABA_ONLY_CSV}")

    df: pd.DataFrame = pd.read_csv(filepath_or_buffer=VOLTAGE_TRACES_GABA_ONLY_CSV)
    t_ms, mean_v = _voltage_pivot_per_angle_gaba(
        df=df,
        angle_deg=IPSP_SUSTAINED_THETA_DEG,
        gaba_base_ns=gaba_base_ns,
    )
    assert len(t_ms) > 0, (
        f"No voltage data found for theta={IPSP_SUSTAINED_THETA_DEG} deg, "
        f"gaba_base_ns={gaba_base_ns:.4f}"
    )
    early_idx: int = int(np.argmin(np.abs(t_ms - IPSP_SUSTAINED_T_EARLY_MS)))
    late_idx: int = int(np.argmin(np.abs(t_ms - IPSP_SUSTAINED_T_LATE_MS)))
    v_early: float = float(mean_v[early_idx])
    v_late: float = float(mean_v[late_idx])
    delta_early: float = abs(v_early - V_INIT_MV)
    delta_late: float = abs(v_late - V_INIT_MV)
    print(
        f"[envelope] gaba={gaba_base_ns:.2f} theta={IPSP_SUSTAINED_THETA_DEG} "
        f"v(200ms)={v_early:.4f} (|delta|={delta_early:.4f}) "
        f"v(1300ms)={v_late:.4f} (|delta|={delta_late:.4f}) "
        f"ratio={delta_late / max(delta_early, 1e-9):.4f}",
        flush=True,
    )
    threshold: float = IPSP_SUSTAINED_RATIO * delta_early
    assert delta_late >= threshold, (
        f"IPSP-sustained-window regression failed at gaba={gaba_base_ns:.2f}, "
        f"theta={IPSP_SUSTAINED_THETA_DEG}: |v(1300ms) - V_init|={delta_late:.4f} mV "
        f"is less than {IPSP_SUSTAINED_RATIO} * |v(200ms) - V_init|={threshold:.4f} mV"
    )


if __name__ == "__main__":
    for gaba_value in GABA_BASE_NS_VALUES:
        test_ipsp_sustained_window(gaba_value)
    print("[envelope] PASS", flush=True)
