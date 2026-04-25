"""Compute DSI per gNMDA value, the H0 / H1 / H2 verdict, and the metrics.json file.

Inputs:
    * ``GNMDA_TRIALS_VOFF1_CSV`` — 56-row CSV produced by ``run_voff1_sweep.py``.
    * ``T0047_GNMDA_TRIALS_CSV`` — 56-row baseline CSV produced by t0047 (Voff = 0).

Outputs:
    * ``DSI_BY_GNMDA_VOFF1_JSON``           — DSI per gNMDA from this task's CSV.
    * ``DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON`` — DSI per gNMDA recomputed from t0047's CSV.
    * ``VERDICT_VOFF1_JSON``                — H0 / H1 / H2 verdict and the two
      numerical tests (range and slope) per REQ-12.
    * ``METRICS_JSON`` — explicit multi-variant ``metrics.json`` with one variant per
      gNMDA value, each carrying ``direction_selectivity_index``.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd

from tasks.t0048_voff_nmda1_dsi_test.code.constants import (
    B2GNMDA_GRID_NS,
    COL_DIRECTION,
    COL_PEAK_PSP_MV,
    DIRECTION_ND_LABEL,
    DIRECTION_PD_LABEL,
    DSI_RANGE_FLAT_THRESHOLD,
    DSI_SLOPE_FLAT_THRESHOLD,
    METRIC_KEY_DSI,
    T0047_DSI_RANGE_REFERENCE,
    T0047_DSI_SLOPE_REFERENCE_PER_NS,
)
from tasks.t0048_voff_nmda1_dsi_test.code.dsi import compute_dsi_pd_nd
from tasks.t0048_voff_nmda1_dsi_test.code.paths import (
    DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON,
    DSI_BY_GNMDA_VOFF1_JSON,
    GNMDA_TRIALS_VOFF1_CSV,
    METRICS_JSON,
    RESULTS_DATA_DIR,
    T0047_GNMDA_TRIALS_CSV,
    VERDICT_VOFF1_JSON,
)


@dataclass(frozen=True, slots=True)
class FlatnessVerdict:
    """Numerical tests for the H0 / H1 / H2 verdict."""

    dsi_max_minus_min: float
    dsi_slope_per_ns: float
    range_test_label: str  # "H0" | "H1" | "H2"
    slope_test_label: str  # "H0" | "H1" | "H2"
    overall_label: str  # combined verdict (H1 only if both tests agree on H1)


def _gnmda_to_variant_id(b2gnmda_ns: float) -> str:
    """Format e.g. 0.5 -> 'voff1_gnmda_0p5ns', 1.0 -> 'voff1_gnmda_1p0ns'."""
    return f"voff1_gnmda_{b2gnmda_ns:.1f}ns".replace(".", "p")


def _compute_dsi_by_gnmda(*, df: pd.DataFrame) -> dict[str, float | None]:
    """Compute DSI per gNMDA grid value from the trial CSV."""
    out: dict[str, float | None] = {}
    for b2gnmda_ns in B2GNMDA_GRID_NS:
        cell: pd.DataFrame = df[df["b2gnmda_ns"].round(6) == round(float(b2gnmda_ns), 6)]
        pd_psp: list[float] = (
            cell[cell[COL_DIRECTION] == DIRECTION_PD_LABEL][COL_PEAK_PSP_MV].astype(float).tolist()
        )
        nd_psp: list[float] = (
            cell[cell[COL_DIRECTION] == DIRECTION_ND_LABEL][COL_PEAK_PSP_MV].astype(float).tolist()
        )
        dsi: float | None = compute_dsi_pd_nd(pd_values=pd_psp, nd_values=nd_psp)
        out[f"{b2gnmda_ns:.2f}"] = dsi
    return out


def _classify_range(*, dsi_range: float) -> str:
    """REQ-12 range test: H1 if range <= threshold; H2 if < t0047 reference; else H0."""
    if dsi_range <= DSI_RANGE_FLAT_THRESHOLD:
        return "H1"
    if dsi_range < T0047_DSI_RANGE_REFERENCE:
        return "H2"
    return "H0"


def _classify_slope(*, slope_per_ns: float) -> str:
    """REQ-12 slope test: H1 if |slope| < threshold; H2 if |slope| < |t0047|; else H0."""
    abs_slope: float = abs(slope_per_ns)
    if abs_slope < DSI_SLOPE_FLAT_THRESHOLD:
        return "H1"
    if abs_slope < abs(T0047_DSI_SLOPE_REFERENCE_PER_NS):
        return "H2"
    return "H0"


def _combine_labels(*, range_label: str, slope_label: str) -> str:
    """Conservative combination: H1 only when both tests pass; H2 when either is H2."""
    if range_label == "H1" and slope_label == "H1":
        return "H1"
    if "H2" in (range_label, slope_label) and "H0" not in (range_label, slope_label):
        return "H2"
    if range_label == "H0" and slope_label == "H0":
        return "H0"
    # Mixed (e.g., one H0 / one H2 / one H1): take the worse of the two.
    if "H0" in (range_label, slope_label):
        return "H0"
    return "H2"


def _compute_verdict(*, dsi_by_gnmda: dict[str, float | None]) -> FlatnessVerdict:
    """Compute the two numerical tests (REQ-12) and the combined verdict label."""
    grid_array: np.ndarray = np.array(list(B2GNMDA_GRID_NS), dtype=np.float64)
    dsi_list: list[float] = []
    grid_kept: list[float] = []
    for b2gnmda_ns in B2GNMDA_GRID_NS:
        value: float | None = dsi_by_gnmda.get(f"{b2gnmda_ns:.2f}")
        assert value is not None, f"DSI is None at gnmda={b2gnmda_ns}; cannot compute verdict"
        dsi_list.append(float(value))
        grid_kept.append(float(b2gnmda_ns))
    dsi_array: np.ndarray = np.array(dsi_list, dtype=np.float64)
    grid_kept_array: np.ndarray = np.array(grid_kept, dtype=np.float64)
    assert grid_kept_array.size == grid_array.size, "DSI grid size disagrees with B2GNMDA_GRID_NS"

    dsi_range: float = float(dsi_array.max() - dsi_array.min())
    slope_per_ns, _intercept = np.polyfit(grid_kept_array, dsi_array, deg=1)
    slope_per_ns_f: float = float(slope_per_ns)

    range_label: str = _classify_range(dsi_range=dsi_range)
    slope_label: str = _classify_slope(slope_per_ns=slope_per_ns_f)
    overall: str = _combine_labels(range_label=range_label, slope_label=slope_label)

    return FlatnessVerdict(
        dsi_max_minus_min=dsi_range,
        dsi_slope_per_ns=slope_per_ns_f,
        range_test_label=range_label,
        slope_test_label=slope_label,
        overall_label=overall,
    )


def _build_metrics_json(*, dsi_by_gnmda: dict[str, float | None]) -> dict[str, Any]:
    variants: list[dict[str, Any]] = []
    for b2gnmda_ns in B2GNMDA_GRID_NS:
        variant_id: str = _gnmda_to_variant_id(float(b2gnmda_ns))
        dsi_value: float | None = dsi_by_gnmda.get(f"{b2gnmda_ns:.2f}")
        variants.append(
            {
                "variant_id": variant_id,
                "label": (f"Voff_bipNMDA = 1, gNMDA = {b2gnmda_ns:.2f} nS, 4 trials per direction"),
                "dimensions": {
                    "sweep": "gnmda",
                    "b2gnmda_ns": float(b2gnmda_ns),
                    "voff_bipnmda": 1,
                    "exptype": "ZERO_MG",
                },
                "metrics": {METRIC_KEY_DSI: dsi_value},
            },
        )
    return {"variants": variants}


def main() -> int:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    df_voff1: pd.DataFrame = pd.read_csv(GNMDA_TRIALS_VOFF1_CSV)
    df_voff0: pd.DataFrame = pd.read_csv(T0047_GNMDA_TRIALS_CSV)

    expected_voff1_rows: int = len(B2GNMDA_GRID_NS) * 2 * 4  # 7 gnmda x 2 dir x 4 trials
    assert len(df_voff1) == expected_voff1_rows, (
        f"Expected {expected_voff1_rows} rows in {GNMDA_TRIALS_VOFF1_CSV}, got {len(df_voff1)}"
    )
    expected_voff0_rows: int = expected_voff1_rows
    assert len(df_voff0) == expected_voff0_rows, (
        f"Expected {expected_voff0_rows} rows in {T0047_GNMDA_TRIALS_CSV}, got {len(df_voff0)}"
    )

    dsi_voff1: dict[str, float | None] = _compute_dsi_by_gnmda(df=df_voff1)
    dsi_voff0: dict[str, float | None] = _compute_dsi_by_gnmda(df=df_voff0)

    DSI_BY_GNMDA_VOFF1_JSON.write_text(
        json.dumps(dsi_voff1, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"[compute_metrics] DSI Voff=1: {dsi_voff1}", flush=True)

    DSI_BY_GNMDA_VOFF0_FROM_T0047_JSON.write_text(
        json.dumps(dsi_voff0, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    print(f"[compute_metrics] DSI Voff=0 (recomputed from t0047): {dsi_voff0}", flush=True)

    verdict: FlatnessVerdict = _compute_verdict(dsi_by_gnmda=dsi_voff1)
    verdict_payload: dict[str, Any] = {
        "dsi_max_minus_min": verdict.dsi_max_minus_min,
        "dsi_slope_per_ns": verdict.dsi_slope_per_ns,
        "range_test_threshold": DSI_RANGE_FLAT_THRESHOLD,
        "slope_test_threshold_per_ns": DSI_SLOPE_FLAT_THRESHOLD,
        "t0047_range_reference": T0047_DSI_RANGE_REFERENCE,
        "t0047_slope_reference_per_ns": T0047_DSI_SLOPE_REFERENCE_PER_NS,
        "range_test_label": verdict.range_test_label,
        "slope_test_label": verdict.slope_test_label,
        "overall_label": verdict.overall_label,
    }
    VERDICT_VOFF1_JSON.write_text(
        json.dumps(verdict_payload, indent=2),
        encoding="utf-8",
    )
    print(
        f"[compute_metrics] verdict range={verdict.dsi_max_minus_min:.4f} "
        f"slope={verdict.dsi_slope_per_ns:.4f}/nS "
        f"range_label={verdict.range_test_label} "
        f"slope_label={verdict.slope_test_label} "
        f"overall={verdict.overall_label}",
        flush=True,
    )

    metrics_payload: dict[str, Any] = _build_metrics_json(dsi_by_gnmda=dsi_voff1)
    METRICS_JSON.write_text(
        json.dumps(metrics_payload, indent=2),
        encoding="utf-8",
    )
    print(
        f"[compute_metrics] wrote {len(metrics_payload['variants'])} variants to {METRICS_JSON}",
        flush=True,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
