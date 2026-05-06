"""Build metrics.json for t0086 with one variant per cell.

Each variant records per-cell mean DSI / SD, mean PD / SD, n_pass / 5, and
classification (Genuine / Marginal / Stochastic).
"""

from __future__ import annotations

import json

from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    CELL_CLASSIFICATION_JSON,
    RESULTS_DIR,
    ensure_directories,
)

METRICS_JSON = RESULTS_DIR / "metrics.json"


def main() -> None:
    ensure_directories()
    payload = json.loads(CELL_CLASSIFICATION_JSON.read_text(encoding="utf-8"))
    variants: list[dict[str, object]] = []
    for cell in payload["cells"]:
        cell_id = int(cell["cell_id"])
        variants.append(
            {
                "variant_id": f"cell_{cell_id:04d}",
                "label": (f"Cell {cell_id} ({cell['selection_reason']}, {cell['classification']})"),
                "dimensions": {
                    "cell_id": cell_id,
                    "selection_reason": cell["selection_reason"],
                    "classification": cell["classification"],
                    "n_pass": int(cell["n_pass"]),
                    "n_total": int(cell["n_total"]),
                    "dsi_sd": float(cell["dsi_sd"]),
                    "pd_rate_hz_mean": float(cell["pd_mean"]),
                    "pd_rate_hz_sd": float(cell["pd_sd"]),
                    "robustness_fraction": (
                        float(cell["n_pass"]) / float(cell["n_total"])
                        if int(cell["n_total"]) > 0
                        else None
                    ),
                },
                "metrics": {
                    "direction_selectivity_index": float(cell["dsi_mean"]),
                },
            }
        )
    out = {"variants": variants}
    METRICS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[build_metrics] wrote {METRICS_JSON} with {len(variants)} variants")


if __name__ == "__main__":
    main()
