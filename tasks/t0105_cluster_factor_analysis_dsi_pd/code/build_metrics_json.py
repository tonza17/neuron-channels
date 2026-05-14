"""Write results/metrics.json in explicit multi-variant format.

Implements REQ-14. Two variants: primary_cohort and strict_cohort. Records the
four registered metric keys; only direction_selectivity_index has a measured
value (median DSI). The other three are null with documented reasons in
results_detailed.md.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
from numpy.typing import NDArray

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    METRIC_DIRECTION_SELECTIVITY_INDEX,
    METRIC_TUNING_CURVE_HWHM_DEG,
    METRIC_TUNING_CURVE_RELIABILITY,
    METRIC_TUNING_CURVE_RMSE,
    PRIMARY_DSI_THRESHOLD,
    PRIMARY_PD_THRESHOLD,
    STRICT_DSI_THRESHOLD,
    STRICT_PD_THRESHOLD,
    VARIANT_PRIMARY_COHORT,
    VARIANT_STRICT_COHORT,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    METRICS_PATH,
    RESULTS_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
    SELECTED_CELLS_STRICT_PATH,
)


def _load_dsi(*, path: Path) -> NDArray[np.float64]:
    with open(path, encoding="utf-8") as f:
        data: dict[str, Any] = json.load(f)
    cells_obj: Any = data["cells"]
    assert isinstance(cells_obj, list)
    return np.array([float(c["dsi"]) for c in cells_obj], dtype=np.float64)


def _build_variant(
    *,
    variant_id: str,
    label: str,
    dsi_threshold: float,
    pd_threshold: float,
    dsi_values: NDArray[np.float64],
) -> dict[str, Any]:
    median_dsi: float = float(np.median(dsi_values)) if dsi_values.size > 0 else 0.0
    return {
        "variant_id": variant_id,
        "label": label,
        "dimensions": {
            "filter_dsi_min": dsi_threshold,
            "filter_pd_hz_min": pd_threshold,
            "n_cells": int(dsi_values.size),
        },
        "metrics": {
            METRIC_DIRECTION_SELECTIVITY_INDEX: median_dsi,
            METRIC_TUNING_CURVE_HWHM_DEG: None,
            METRIC_TUNING_CURVE_RELIABILITY: None,
            METRIC_TUNING_CURVE_RMSE: None,
        },
    }


def main() -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    primary_dsi: NDArray[np.float64] = _load_dsi(path=SELECTED_CELLS_PRIMARY_PATH)
    strict_dsi: NDArray[np.float64] = _load_dsi(path=SELECTED_CELLS_STRICT_PATH)

    primary_variant: dict[str, Any] = _build_variant(
        variant_id=VARIANT_PRIMARY_COHORT,
        label="Primary cohort (DSI > 0.1 AND PD > 2.0)",
        dsi_threshold=PRIMARY_DSI_THRESHOLD,
        pd_threshold=PRIMARY_PD_THRESHOLD,
        dsi_values=primary_dsi,
    )
    strict_variant: dict[str, Any] = _build_variant(
        variant_id=VARIANT_STRICT_COHORT,
        label="Strict cohort (DSI > 0.2 AND PD > 3.0)",
        dsi_threshold=STRICT_DSI_THRESHOLD,
        pd_threshold=STRICT_PD_THRESHOLD,
        dsi_values=strict_dsi,
    )

    payload: dict[str, Any] = {"variants": [primary_variant, strict_variant]}
    with open(METRICS_PATH, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"Wrote {METRICS_PATH}")
    print(
        f"  primary cohort N={primary_dsi.size} median_dsi="
        f"{primary_variant['metrics'][METRIC_DIRECTION_SELECTIVITY_INDEX]:.4f}"
    )
    print(
        f"  strict cohort  N={strict_dsi.size} median_dsi="
        f"{strict_variant['metrics'][METRIC_DIRECTION_SELECTIVITY_INDEX]:.4f}"
    )


if __name__ == "__main__":
    main()
