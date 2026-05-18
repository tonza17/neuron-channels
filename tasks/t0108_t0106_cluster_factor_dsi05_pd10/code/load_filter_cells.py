"""Load t0106 evaluations, apply strict filter, dedupe by 68-d vector.

Output: results/data/filtered_cells.json with one record per unique cell.

Usage:
    uv run python -m tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.load_filter_cells
"""

from __future__ import annotations

import gzip
import json
from dataclasses import asdict, dataclass
from pathlib import Path

from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.constants import (
    DEDUP_DECIMALS,
    DSI_THRESHOLD,
    N_TOTAL_DIMS,
    PD_THRESHOLD_HZ,
    SOURCE_SEED,
    SOURCE_TASK,
)
from tasks.t0108_t0106_cluster_factor_dsi05_pd10.code.paths import (
    FILTERED_CELLS_JSON,
    T0106_EVALUATIONS_GZ,
)


@dataclass(frozen=True, slots=True)
class FilteredCell:
    cell_index: int
    source_task: str
    source_seed: int
    generation: int
    dsi: float
    pd_rate_hz: float
    vector_68d: list[float]


@dataclass(frozen=True, slots=True)
class FilterReport:
    n_raw: int
    n_passing_raw: int
    n_unique: int
    dsi_threshold: float
    pd_threshold_hz: float
    source_task: str
    source_seed: int


def _load_evaluations(path: Path) -> list[dict]:
    with gzip.open(path, "rt", encoding="utf-8") as f:
        payload = json.load(f)
    assert isinstance(payload, dict), "expected top-level dict"
    assert "evaluations" in payload, "expected 'evaluations' key"
    evaluations: list[dict] = payload["evaluations"]
    return evaluations


def _passes_filter(evaluation: dict) -> bool:
    return (
        evaluation["dsi_vector_sum"] > DSI_THRESHOLD and evaluation["pd_rate_hz"] > PD_THRESHOLD_HZ
    )


def _vector_key(vector_68d: list[float]) -> tuple[float, ...]:
    return tuple(round(x, DEDUP_DECIMALS) for x in vector_68d)


def _dedupe_cells(passing: list[dict]) -> list[FilteredCell]:
    seen: dict[tuple[float, ...], FilteredCell] = {}
    for idx, evaluation in enumerate(passing):
        vector_68d: list[float] = list(evaluation["vector_68d"])
        assert len(vector_68d) == N_TOTAL_DIMS, "expected 68-d vector"
        key: tuple[float, ...] = _vector_key(vector_68d)
        if key in seen:
            continue
        cell = FilteredCell(
            cell_index=idx,
            source_task=SOURCE_TASK,
            source_seed=SOURCE_SEED,
            generation=int(evaluation["generation"]),
            dsi=float(evaluation["dsi_vector_sum"]),
            pd_rate_hz=float(evaluation["pd_rate_hz"]),
            vector_68d=vector_68d,
        )
        seen[key] = cell
    return list(seen.values())


def load_and_filter() -> tuple[list[FilteredCell], FilterReport]:
    evaluations: list[dict] = _load_evaluations(path=T0106_EVALUATIONS_GZ)
    passing: list[dict] = [e for e in evaluations if _passes_filter(evaluation=e)]
    unique: list[FilteredCell] = _dedupe_cells(passing=passing)
    report = FilterReport(
        n_raw=len(evaluations),
        n_passing_raw=len(passing),
        n_unique=len(unique),
        dsi_threshold=DSI_THRESHOLD,
        pd_threshold_hz=PD_THRESHOLD_HZ,
        source_task=SOURCE_TASK,
        source_seed=SOURCE_SEED,
    )
    return unique, report


def _save_filtered_cells(
    *,
    cells: list[FilteredCell],
    report: FilterReport,
    output_path: Path,
) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload: dict[str, object] = {
        "report": asdict(report),
        "cells": [asdict(c) for c in cells],
    }
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    cells, report = load_and_filter()
    print(f"N_raw evaluations:  {report.n_raw}")
    print(f"N passing filter:   {report.n_passing_raw}")
    print(f"N unique (deduped): {report.n_unique}")
    print(f"Source: {report.source_task} seed {report.source_seed}")
    print(f"Filter: DSI > {report.dsi_threshold} AND PD > {report.pd_threshold_hz} Hz")
    _save_filtered_cells(
        cells=cells,
        report=report,
        output_path=FILTERED_CELLS_JSON,
    )
    print(f"Wrote {FILTERED_CELLS_JSON}")


if __name__ == "__main__":
    main()
