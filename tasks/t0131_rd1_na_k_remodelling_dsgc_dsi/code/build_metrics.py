"""Step 15: write results/metrics.json (explicit variants), costs.json, remote machines file."""

import json
from typing import Any

import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import ScalingArm
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    COSTS_JSON,
    DSI_RESULTS_CSV,
    METRICS_JSON,
    REMOTE_MACHINES_JSON,
    RESULTS_DIR,
    with_arm_suffix,
)

METRIC_KEY: str = "direction_selectivity_index"
LABELS: dict[str, str] = {
    "wt_like": "WT-like (scale 1.0)",
    "rd1_like": "rd1-like (per-cell fitted scaling)",
    "wt_like_with_bias": "WT-like with tonic bias",
    "rd1_like_with_bias": "rd1-like with tonic bias",
}


def variants_for_arm(*, arm: str) -> list[dict[str, Any]]:
    path = with_arm_suffix(path=DSI_RESULTS_CSV, arm=arm)
    if not path.exists():
        return []
    df = pd.read_csv(path)
    out: list[dict[str, Any]] = []
    for cond, label in LABELS.items():
        sub = df[df.condition == cond]
        if len(sub) == 0:
            continue
        defined = sub.dsi_signed.dropna()
        value: float | None = None if len(defined) == 0 else float(defined.median())
        suffix = "" if arm == str(ScalingArm.SOMA_AIS) else "-dendritic"
        out.append(
            {
                "variant_id": cond.replace("_", "-") + suffix,
                "label": label + ("" if suffix == "" else " (dendritic arm)"),
                "dimensions": {
                    "scaling": "rd1_fitted" if cond.startswith("rd1") else "wt_1.0",
                    "tonic_bias": cond.endswith("bias"),
                    "arm": arm,
                    "n_cells_defined": int(len(defined)),
                    "n_cells_undefined": int(len(sub) - len(defined)),
                },
                "metrics": {METRIC_KEY: value},
            }
        )
    return out


def main() -> None:
    variants: list[dict[str, Any]] = []
    for arm in (str(ScalingArm.SOMA_AIS), str(ScalingArm.SOMA_AIS_DENDRITE)):
        variants += variants_for_arm(arm=arm)
    assert len(variants) >= 4, "at least the four base-arm variants exist"
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    METRICS_JSON.write_text(json.dumps({"variants": variants}, indent=2), encoding="utf-8")
    COSTS_JSON.write_text(
        json.dumps(
            {
                "total_cost_usd": 0,
                "breakdown": {},
                "note": "Local CPU NEURON simulations only; no remote machines or paid APIs.",
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    REMOTE_MACHINES_JSON.write_text("[]\n", encoding="utf-8")
    print(json.dumps({"variants": variants}, indent=1))


if __name__ == "__main__":
    main()
