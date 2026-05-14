"""Pool, filter, dedupe per-cell evaluations from the four 68-d NSGA-II lineages.

Implements REQ-1 (pool + dedupe + primary/strict filters) and REQ-3 (silenced-cell
artifact filter on t0091/t0099/t0102). Writes:

* results/data/selected_cells_primary.json
* results/data/selected_cells_strict.json
* results/data/selection_counts.json
"""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from tasks.t0105_cluster_factor_analysis_dsi_pd.code.constants import (
    DEDUP_DECIMALS,
    N_TOTAL_DIMS,
    PRE_GUARD_SOURCE_TASKS,
    PRIMARY_DSI_THRESHOLD,
    PRIMARY_PD_THRESHOLD,
    SILENCE_DSI_THRESHOLD,
    SILENCE_PD_THRESHOLD,
    SOURCE_T0091,
    SOURCE_T0099,
    SOURCE_T0102,
    SOURCE_T0104,
    STRICT_DSI_THRESHOLD,
    STRICT_PD_THRESHOLD,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.paths import (
    RESULTS_DATA_DIR,
    SELECTED_CELLS_PRIMARY_PATH,
    SELECTED_CELLS_STRICT_PATH,
    SELECTION_COUNTS_PATH,
    T0091_EVAL_PATH,
    T0099_SEEDS,
    T0102_SEEDS,
    T0104_SEEDS,
    t0099_seed_path,
    t0102_seed_path,
    t0104_seed_path,
)
from tasks.t0105_cluster_factor_analysis_dsi_pd.code.schemas import CellRecord


def _read_rows(*, path: Path) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as f:
        data: Any = json.load(f)
    rows_obj: Any = data["evaluations"] if isinstance(data, dict) else data
    assert isinstance(rows_obj, list), f"Expected list of evaluations in {path}"
    out: list[dict[str, Any]] = []
    for row in rows_obj:
        assert isinstance(row, dict)
        out.append(row)
    return out


def _build_record(
    *,
    row: dict[str, Any],
    source_task: str,
    seed: int | None,
) -> CellRecord:
    vec_obj: Any = row["vector_68d"]
    assert isinstance(vec_obj, list)
    assert len(vec_obj) == N_TOTAL_DIMS, (
        f"vector_68d in {source_task} has length {len(vec_obj)}, expected {N_TOTAL_DIMS}"
    )
    vec: tuple[float, ...] = tuple(float(v) for v in vec_obj)
    robustness_val: float | None = (
        float(row["robustness"]) if "robustness" in row and row["robustness"] is not None else None
    )
    return CellRecord(
        source_task=source_task,
        seed=seed,
        generation=int(row["generation"]),
        dsi=float(row["dsi_vector_sum"]),
        pd_rate_hz=float(row["pd_rate_hz"]),
        robustness=robustness_val,
        vector_68d=vec,
    )


def _load_lineage(
    *,
    source_task: str,
) -> tuple[list[CellRecord], int]:
    """Return (records, raw_row_count) for one lineage."""
    raw: list[CellRecord] = []
    raw_count: int = 0
    if source_task == SOURCE_T0091:
        rows: list[dict[str, Any]] = _read_rows(path=T0091_EVAL_PATH)
        raw_count += len(rows)
        for r in rows:
            raw.append(_build_record(row=r, source_task=source_task, seed=None))
    elif source_task == SOURCE_T0099:
        for seed in T0099_SEEDS:
            rows = _read_rows(path=t0099_seed_path(seed=seed))
            raw_count += len(rows)
            for r in rows:
                raw.append(_build_record(row=r, source_task=source_task, seed=seed))
    elif source_task == SOURCE_T0102:
        for seed in T0102_SEEDS:
            rows = _read_rows(path=t0102_seed_path(seed=seed))
            raw_count += len(rows)
            for r in rows:
                raw.append(_build_record(row=r, source_task=source_task, seed=seed))
    elif source_task == SOURCE_T0104:
        for seed in T0104_SEEDS:
            rows = _read_rows(path=t0104_seed_path(seed=seed))
            raw_count += len(rows)
            for r in rows:
                raw.append(_build_record(row=r, source_task=source_task, seed=seed))
    else:
        raise ValueError(f"unknown source_task: {source_task}")
    return raw, raw_count


def _apply_silence_filter(
    *,
    records: list[CellRecord],
    source_task: str,
) -> tuple[list[CellRecord], int]:
    """Drop DSI > 0.95 AND PD < 5 from pre-guard lineages. Returns (kept, n_excluded)."""
    if source_task not in PRE_GUARD_SOURCE_TASKS:
        return records, 0
    kept: list[CellRecord] = []
    excluded: int = 0
    for rec in records:
        if rec.dsi > SILENCE_DSI_THRESHOLD and rec.pd_rate_hz < SILENCE_PD_THRESHOLD:
            excluded += 1
            continue
        kept.append(rec)
    return kept, excluded


def _apply_threshold_filter(
    *,
    records: list[CellRecord],
    dsi_threshold: float,
    pd_threshold: float,
) -> list[CellRecord]:
    return [r for r in records if r.dsi > dsi_threshold and r.pd_rate_hz > pd_threshold]


def _dedupe_by_vector(*, records: list[CellRecord]) -> list[CellRecord]:
    """Dedupe by 68-d vector rounded to DEDUP_DECIMALS. Keep first occurrence."""
    seen: set[tuple[float, ...]] = set()
    out: list[CellRecord] = []
    for rec in records:
        sig: tuple[float, ...] = tuple(round(v, DEDUP_DECIMALS) for v in rec.vector_68d)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(rec)
    return out


def _records_to_jsonable(*, records: list[CellRecord]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for rec in records:
        d: dict[str, Any] = asdict(rec)
        d["vector_68d"] = list(rec.vector_68d)
        out.append(d)
    return out


def _per_source_breakdown(*, records: list[CellRecord]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for rec in records:
        counts[rec.source_task] = counts.get(rec.source_task, 0) + 1
    return counts


def main() -> None:
    RESULTS_DATA_DIR.mkdir(parents=True, exist_ok=True)

    sources: tuple[str, ...] = (SOURCE_T0091, SOURCE_T0099, SOURCE_T0102, SOURCE_T0104)

    silence_exclusions: dict[str, int] = {}
    raw_counts: dict[str, int] = {}
    pass_silence: dict[str, int] = {}
    all_post_silence: list[CellRecord] = []

    for source_task in sources:
        records, raw_count = _load_lineage(source_task=source_task)
        raw_counts[source_task] = raw_count
        kept, n_excl = _apply_silence_filter(records=records, source_task=source_task)
        silence_exclusions[source_task] = n_excl
        pass_silence[source_task] = len(kept)
        all_post_silence.extend(kept)

    # Primary filter.
    primary_passing: list[CellRecord] = _apply_threshold_filter(
        records=all_post_silence,
        dsi_threshold=PRIMARY_DSI_THRESHOLD,
        pd_threshold=PRIMARY_PD_THRESHOLD,
    )
    primary_unique: list[CellRecord] = _dedupe_by_vector(records=primary_passing)

    # Strict filter.
    strict_passing: list[CellRecord] = _apply_threshold_filter(
        records=all_post_silence,
        dsi_threshold=STRICT_DSI_THRESHOLD,
        pd_threshold=STRICT_PD_THRESHOLD,
    )
    strict_unique: list[CellRecord] = _dedupe_by_vector(records=strict_passing)

    # Per-source breakdown.
    primary_per_source: dict[str, int] = _per_source_breakdown(records=primary_unique)
    strict_per_source: dict[str, int] = _per_source_breakdown(records=strict_unique)
    primary_passing_per_source: dict[str, int] = _per_source_breakdown(records=primary_passing)
    strict_passing_per_source: dict[str, int] = _per_source_breakdown(records=strict_passing)

    selection_counts: dict[str, Any] = {
        "n_raw_total": sum(raw_counts.values()),
        "n_raw_per_source": raw_counts,
        "n_pass_silence_filter_per_source": pass_silence,
        "silence_artifact_exclusions": silence_exclusions,
        "primary_filter": {
            "dsi_threshold": PRIMARY_DSI_THRESHOLD,
            "pd_threshold": PRIMARY_PD_THRESHOLD,
            "n_passing_total": len(primary_passing),
            "n_passing_per_source": primary_passing_per_source,
            "n_unique_total": len(primary_unique),
            "n_unique_per_source": primary_per_source,
        },
        "strict_filter": {
            "dsi_threshold": STRICT_DSI_THRESHOLD,
            "pd_threshold": STRICT_PD_THRESHOLD,
            "n_passing_total": len(strict_passing),
            "n_passing_per_source": strict_passing_per_source,
            "n_unique_total": len(strict_unique),
            "n_unique_per_source": strict_per_source,
        },
    }

    with open(SELECTION_COUNTS_PATH, "w", encoding="utf-8") as f:
        json.dump(selection_counts, f, indent=2)
    with open(SELECTED_CELLS_PRIMARY_PATH, "w", encoding="utf-8") as f:
        json.dump({"cells": _records_to_jsonable(records=primary_unique)}, f, indent=2)
    with open(SELECTED_CELLS_STRICT_PATH, "w", encoding="utf-8") as f:
        json.dump({"cells": _records_to_jsonable(records=strict_unique)}, f, indent=2)

    print("== Pooled cell counts ==")
    print(f"  Total raw rows: {selection_counts['n_raw_total']}")
    for src in sources:
        print(
            f"    {src}: raw={raw_counts[src]} pass_silence={pass_silence[src]} "
            f"silence_excluded={silence_exclusions[src]}"
        )
    print()
    print("== Primary filter (DSI > 0.1 AND PD > 2.0) ==")
    print(f"  N_passing={len(primary_passing)} N_unique={len(primary_unique)}")
    for src, n in primary_per_source.items():
        print(f"    {src}: unique={n}")
    print()
    print("== Strict filter (DSI > 0.2 AND PD > 3.0) ==")
    print(f"  N_passing={len(strict_passing)} N_unique={len(strict_unique)}")
    for src, n in strict_per_source.items():
        print(f"    {src}: unique={n}")
    print()
    print(f"Wrote: {SELECTION_COUNTS_PATH}")
    print(f"Wrote: {SELECTED_CELLS_PRIMARY_PATH}")
    print(f"Wrote: {SELECTED_CELLS_STRICT_PATH}")


if __name__ == "__main__":
    main()
