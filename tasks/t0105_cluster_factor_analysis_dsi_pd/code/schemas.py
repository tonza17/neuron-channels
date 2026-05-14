"""Frozen dataclasses for t0105 per-cell records and analysis outputs."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CellRecord:
    """One deduped cell from the pooled 68-d optimisation evaluations."""

    source_task: str
    seed: int | None
    generation: int
    dsi: float
    pd_rate_hz: float
    robustness: float | None
    vector_68d: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class LineageCounts:
    """Per-lineage counts for one filter threshold."""

    n_raw: int
    n_pass_silence_filter: int
    n_pass_primary_filter: int
    n_pass_strict_filter: int
    n_silence_artifact_excluded: int


@dataclass(frozen=True, slots=True)
class CohortCounts:
    """Top-level cohort statistics for one filter."""

    n_passing_total: int
    n_unique: int
    per_source_unique: dict[str, int]
