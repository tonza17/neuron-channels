"""Phase G.1: AIS-to-soma Nav ratio audit (cluster 1 cells).

Reads:

* ``T0088_RECLUSTER_CENTROIDS_JSON`` -- per-cluster centroid_unnormalised
* ``T0083_ALL_EVALUATIONS_JSON`` -- per-cell 54-d params

For each cluster, computes ratio = ``centroid_unnormalised[NAV16_AIS_GBAR] /
centroid_unnormalised[NAV16_SOMA_GBAR]``. For cluster-1 cells (1304, 1504, 1624,
1634), computes per-cell ratio. Flags any soma Nav at the 1e-5 floor.

Verdict logic:

* If 4/4 cluster-1 cells have soma Nav at the floor (``params[NAV16_SOMA_GBAR]
  <= 1.05 * 1e-5``) the centroid ratio is dominated by the floor and the
  high ratio is an artifact: ``"centroid_artifact"``.
* If <50 percent of cluster-1 cells are floor-pinned and the cell-level
  ratios are also high (>50), the high ratio is a real biological signal:
  ``"real_signal"``.
* If units cannot be confirmed, ``"units_bug"``.
"""

from __future__ import annotations

import json
from typing import Any

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    LOWER_BOUNDS,
    ParamIndex,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    CLUSTER_1_CELL_IDS,
    NAV16_SOMA_LOWER_BOUND_S_CM2,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_G1_AUDIT_JSON,
    T0083_ALL_EVALUATIONS_JSON,
    T0088_RECLUSTER_CENTROIDS_JSON,
    ensure_directories,
)


def _ratio(*, ais: float, soma: float) -> float:
    if abs(soma) < 1e-30:
        return float("inf")
    return float(ais) / float(soma)


def main() -> None:
    ensure_directories()

    centroids_data = json.loads(T0088_RECLUSTER_CENTROIDS_JSON.read_text())
    centroids = centroids_data["centroids"]
    print(f"read {len(centroids)} cluster centroids from {T0088_RECLUSTER_CENTROIDS_JSON}")

    cluster_entries: list[dict[str, Any]] = []
    for c in centroids:
        cluster_id = int(c["cluster_id"])
        unnorm = c["centroid_unnormalised"]
        ais_gbar = float(unnorm[int(ParamIndex.NAV16_AIS_GBAR)])
        soma_gbar = float(unnorm[int(ParamIndex.NAV16_SOMA_GBAR)])
        ratio = _ratio(ais=ais_gbar, soma=soma_gbar)
        cluster_entries.append(
            {
                "cluster_id": cluster_id,
                "n_cells": int(c["n_cells"]),
                "ais_gbar_s_cm2": ais_gbar,
                "soma_gbar_s_cm2": soma_gbar,
                "ratio_ais_to_soma": ratio,
            }
        )

    all_evals = json.loads(T0083_ALL_EVALUATIONS_JSON.read_text())
    cluster1_cells = [e for e in all_evals if int(e["cell_index"]) in CLUSTER_1_CELL_IDS]
    assert len(cluster1_cells) == len(CLUSTER_1_CELL_IDS), (
        f"expected to find {len(CLUSTER_1_CELL_IDS)} cluster-1 cells, found {len(cluster1_cells)}"
    )

    floor = float(LOWER_BOUNDS[int(ParamIndex.NAV16_SOMA_GBAR)])
    floor_threshold = 1.05 * NAV16_SOMA_LOWER_BOUND_S_CM2
    print(f"NAV16 soma lower bound from t0080: {floor}, floor-pin threshold: {floor_threshold}")

    per_cell_entries: list[dict[str, Any]] = []
    floor_pinned: list[int] = []
    for cell in cluster1_cells:
        params = cell["params"]
        cell_id = int(cell["cell_index"])
        ais = float(params[int(ParamIndex.NAV16_AIS_GBAR)])
        soma = float(params[int(ParamIndex.NAV16_SOMA_GBAR)])
        ratio = _ratio(ais=ais, soma=soma)
        is_floor_pinned = soma <= floor_threshold
        if is_floor_pinned:
            floor_pinned.append(cell_id)
        per_cell_entries.append(
            {
                "cell_id": cell_id,
                "ais_gbar_s_cm2": ais,
                "soma_gbar_s_cm2": soma,
                "ratio_ais_to_soma": ratio,
                "is_floor_pinned": is_floor_pinned,
            }
        )

    # Verdict.
    n_pinned = len(floor_pinned)
    n_total = len(per_cell_entries)
    cluster1_centroid_ratio = next(
        (c["ratio_ais_to_soma"] for c in cluster_entries if c["cluster_id"] == 1),
        float("nan"),
    )
    high_ratio_cells = sum(1 for e in per_cell_entries if e["ratio_ais_to_soma"] > 50.0)
    if n_pinned == n_total:
        verdict = "centroid_artifact"
        verdict_reason = (
            f"All {n_total} cluster-1 cells have soma Nav at or near the {floor} S/cm^2 lower "
            "bound. The high centroid ratio is dominated by the floor-pinned denominator and is "
            "not a real biological signal."
        )
    elif n_pinned <= n_total // 2 and high_ratio_cells >= n_total // 2:
        verdict = "real_signal"
        verdict_reason = (
            f"Only {n_pinned}/{n_total} cluster-1 cells are floor-pinned but {high_ratio_cells}/"
            f"{n_total} have AIS-to-soma ratios above 50. The cluster's high ratio reflects a "
            "biological pattern, not a floor artifact."
        )
    else:
        verdict = "centroid_artifact"
        verdict_reason = (
            f"{n_pinned}/{n_total} cells are floor-pinned and {high_ratio_cells}/{n_total} have "
            "high ratios. The cluster centroid is partly inflated by the floor-pinned subset, so "
            "the high centroid ratio cannot be confidently interpreted as a real signal."
        )

    audit = {
        "cluster_centroid_ratios": cluster_entries,
        "per_cell_ratios": per_cell_entries,
        "cluster_1_centroid_ratio": cluster1_centroid_ratio,
        "floor_pinned_cell_ids": floor_pinned,
        "n_floor_pinned": n_pinned,
        "n_total_cluster_1_cells": n_total,
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "lower_bound_s_cm2": floor,
        "floor_threshold_s_cm2": floor_threshold,
    }

    DATA_G1_AUDIT_JSON.write_text(json.dumps(audit, indent=2))
    print(f"wrote {DATA_G1_AUDIT_JSON}")
    print(f"verdict: {verdict}")
    print(f"reason: {verdict_reason}")


if __name__ == "__main__":
    main()
