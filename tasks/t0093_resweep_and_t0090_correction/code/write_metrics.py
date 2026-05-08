"""Write ``results/metrics.json`` in the explicit-variant format.

Reads ``DATA_POST_FIX_VERIFICATION_JSON``, aggregates DSI per population over
STABLE-and-firing cells (``stability_flag == 'stable' AND pd_rate_hz > 0``),
and emits two variants:

* ``different_set_post_fix``
* ``similar_set_post_fix``

Each variant carries only the registered ``direction_selectivity_index`` metric
key. Missing data (no STABLE-and-firing cells in a population) is recorded as
``null``, never ``0.0``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tasks.t0093_resweep_and_t0090_correction.code.constants import (
    FIELD_DSI,
    FIELD_PD_RATE_HZ,
    FIELD_POPULATION,
    FIELD_STABILITY_FLAG,
    POPULATION_DIFFERENT,
    POPULATION_SIMILAR,
    REGISTERED_METRIC_DSI,
    REPLACEMENT_LIBRARY_ID,
    STABILITY_FLAG_STABLE,
    VARIANT_DIFFERENT_POST_FIX,
    VARIANT_SIMILAR_POST_FIX,
)
from tasks.t0093_resweep_and_t0090_correction.code.paths import (
    DATA_POST_FIX_VERIFICATION_JSON,
    RESULTS_METRICS_JSON,
    ensure_directories,
)


@dataclass(frozen=True, slots=True)
class PopulationDsiSummary:
    population: str
    n_stable_firing: int
    mean_dsi: float | None


def _is_stable_firing(*, row: dict[str, Any]) -> bool:
    if str(row.get(FIELD_STABILITY_FLAG)) != STABILITY_FLAG_STABLE:
        return False
    pd_rate = row.get(FIELD_PD_RATE_HZ)
    if pd_rate is None:
        return False
    return float(pd_rate) > 0.0


def _summarise_population(
    *,
    rows: list[dict[str, Any]],
    population: str,
) -> PopulationDsiSummary:
    pop_rows = [r for r in rows if str(r.get(FIELD_POPULATION)) == population]
    firing_dsis: list[float] = [
        float(r[FIELD_DSI])
        for r in pop_rows
        if _is_stable_firing(row=r) and r.get(FIELD_DSI) is not None
    ]
    mean: float | None = (
        None if len(firing_dsis) == 0 else float(sum(firing_dsis) / len(firing_dsis))
    )
    return PopulationDsiSummary(
        population=population,
        n_stable_firing=int(len(firing_dsis)),
        mean_dsi=mean,
    )


def _build_variant(
    *,
    variant_id: str,
    label: str,
    population: str,
    summary: PopulationDsiSummary,
) -> dict[str, Any]:
    return {
        "variant_id": variant_id,
        "label": label,
        "dimensions": {
            "morphology_population": population,
            "channels": "t0083_best_cell",
            "generator": REPLACEMENT_LIBRARY_ID,
        },
        "metrics": {
            REGISTERED_METRIC_DSI: summary.mean_dsi,
        },
    }


def build_metrics_payload(*, post_fix_path: Path) -> dict[str, Any]:
    raw = json.loads(post_fix_path.read_text())
    assert isinstance(raw, list)
    rows: list[dict[str, Any]] = [r for r in raw if isinstance(r, dict)]

    different_summary = _summarise_population(
        rows=rows,
        population=POPULATION_DIFFERENT,
    )
    similar_summary = _summarise_population(
        rows=rows,
        population=POPULATION_SIMILAR,
    )

    return {
        "variants": [
            _build_variant(
                variant_id=VARIANT_DIFFERENT_POST_FIX,
                label="Different-set 30 morphologies (post-fix)",
                population=POPULATION_DIFFERENT,
                summary=different_summary,
            ),
            _build_variant(
                variant_id=VARIANT_SIMILAR_POST_FIX,
                label="Similar-set 30 morphologies (post-fix)",
                population=POPULATION_SIMILAR,
                summary=similar_summary,
            ),
        ],
    }


def main() -> None:
    ensure_directories()
    payload = build_metrics_payload(post_fix_path=DATA_POST_FIX_VERIFICATION_JSON)
    RESULTS_METRICS_JSON.write_text(json.dumps(payload, indent=2))
    print(f"wrote {RESULTS_METRICS_JSON}")
    for v in payload["variants"]:
        dsi = v["metrics"][REGISTERED_METRIC_DSI]
        print(f"  {v['variant_id']}: {REGISTERED_METRIC_DSI}={dsi}")


if __name__ == "__main__":
    main()
