"""Pool DSI > 0.7 ∧ PD > 10 Hz NSGA-II survivors across four seeds.

Branches on file suffix:
    *.json.gz  -> gzipped JSON, structured as {"evaluations": [...]}.
    *.jsonl.gz -> gzipped JSONL, one record per line (t0114 / t0115).

Outputs:
    data/pooled_survivors.parquet
    results/data/per_seed_cohort_counts.csv

Usage:
    uv run python -u -m tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.load_pooled_cells
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.constants import (
    ALL_PARAM_NAMES,
    DEDUP_DECIMALS,
    DSI_THRESHOLD,
    N_TOTAL_DIMS,
    PD_THRESHOLD_HZ,
    SOURCES,
)
from tasks.t0116_pooled_pca_cluster_factor_dsi07_pd10.code.paths import (
    PER_SEED_COHORT_COUNTS_CSV,
    POOLED_SURVIVORS_PARQUET,
    REPO_ROOT,
)

SOURCE_TASK_COLUMN: str = "source_task"
SEED_COLUMN: str = "seed"
GENERATION_COLUMN: str = "generation"
INDIVIDUAL_IDX_COLUMN: str = "individual_idx"
DSI_COLUMN: str = "dsi_vector_sum"
PD_COLUMN: str = "pd_rate_hz"

JSONL_GZ_SUFFIXES: list[str] = [".jsonl", ".gz"]
JSON_GZ_SUFFIXES: list[str] = [".json", ".gz"]


@dataclass(frozen=True, slots=True)
class PerSeedCounts:
    source_task: str
    seed: int
    n_raw: int
    n_passing_filter: int
    n_unique: int


def _iter_records(path: Path) -> Iterator[dict[str, object]]:
    """Yield raw records from either a JSON-wrapper gzip or a JSONL gzip file."""
    suffixes: list[str] = path.suffixes[-2:]
    if suffixes == JSONL_GZ_SUFFIXES:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            for line in fh:
                if line.strip() == "":
                    continue
                yield json.loads(line)
    elif suffixes == JSON_GZ_SUFFIXES:
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            payload = json.load(fh)
        assert isinstance(payload, dict) and "evaluations" in payload, (
            f"expected {{'evaluations': [...]}} wrapper in {path}"
        )
        evals = payload["evaluations"]
        assert isinstance(evals, list)
        yield from evals
    else:
        raise ValueError(f"unsupported file suffixes for {path}: {suffixes}")


def _passes_cohort_filter(*, record: dict[str, object]) -> bool:
    dsi: object = record.get(DSI_COLUMN)
    pd_rate: object = record.get(PD_COLUMN)
    if not isinstance(dsi, int | float) or not isinstance(pd_rate, int | float):
        return False
    return float(dsi) > DSI_THRESHOLD and float(pd_rate) > PD_THRESHOLD_HZ


def _build_dataframe_for_source(
    *,
    source_task: str,
    seed: int,
    path: Path,
) -> tuple[pd.DataFrame, PerSeedCounts]:
    n_raw: int = 0
    passing_rows: list[dict[str, object]] = []
    for individual_idx, rec in enumerate(_iter_records(path)):
        n_raw += 1
        if not _passes_cohort_filter(record=rec):
            continue
        vec = rec.get("vector_68d")
        assert isinstance(vec, list) and len(vec) == N_TOTAL_DIMS, (
            f"unexpected vector_68d shape in {path} at idx={individual_idx}: "
            f"{None if vec is None else len(vec)!r}"
        )
        row: dict[str, object] = {
            SOURCE_TASK_COLUMN: source_task,
            SEED_COLUMN: int(seed),
            GENERATION_COLUMN: int(rec["generation"]),  # type: ignore[arg-type]
            INDIVIDUAL_IDX_COLUMN: int(individual_idx),
            DSI_COLUMN: float(rec[DSI_COLUMN]),  # type: ignore[arg-type]
            PD_COLUMN: float(rec[PD_COLUMN]),  # type: ignore[arg-type]
        }
        for name, val in zip(ALL_PARAM_NAMES, vec, strict=True):
            row[name] = float(val)
        passing_rows.append(row)
    n_passing: int = len(passing_rows)
    df_raw_filtered: pd.DataFrame = pd.DataFrame(passing_rows)
    if n_passing == 0:
        df_unique: pd.DataFrame = df_raw_filtered.copy()
    else:
        rounded = df_raw_filtered[list(ALL_PARAM_NAMES)].round(DEDUP_DECIMALS)
        dedup_keys = pd.util.hash_pandas_object(rounded, index=False)
        df_raw_filtered = df_raw_filtered.assign(_dedup_key=dedup_keys.values)
        df_unique = (
            df_raw_filtered.drop_duplicates(subset=["_dedup_key"], keep="first")
            .drop(columns=["_dedup_key"])
            .reset_index(drop=True)
        )
    counts = PerSeedCounts(
        source_task=source_task,
        seed=int(seed),
        n_raw=n_raw,
        n_passing_filter=n_passing,
        n_unique=int(len(df_unique)),
    )
    print(
        f"  {source_task} (seed {seed}): n_raw={n_raw}, "
        f"n_passing={n_passing}, n_unique={counts.n_unique}",
        flush=True,
    )
    return df_unique, counts


def _typed_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Apply explicit dtypes to the pooled DataFrame."""
    typed: dict[str, str] = {
        SOURCE_TASK_COLUMN: "string",
        SEED_COLUMN: "UInt32",
        GENERATION_COLUMN: "UInt32",
        INDIVIDUAL_IDX_COLUMN: "UInt32",
        DSI_COLUMN: "float64",
        PD_COLUMN: "float64",
    }
    for name in ALL_PARAM_NAMES:
        typed[name] = "float64"
    return df.astype(typed)


def main() -> None:
    POOLED_SURVIVORS_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    PER_SEED_COHORT_COUNTS_CSV.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"Pooling survivors with DSI > {DSI_THRESHOLD} AND PD > {PD_THRESHOLD_HZ} from "
        f"{len(SOURCES)} sources...",
        flush=True,
    )

    frames: list[pd.DataFrame] = []
    counts_rows: list[PerSeedCounts] = []
    first_passing_sample: bool = False
    for source_task, seed, rel_path in SOURCES:
        abs_path: Path = REPO_ROOT / rel_path
        assert abs_path.exists(), f"missing predictions file: {abs_path}"
        df, counts = _build_dataframe_for_source(
            source_task=source_task,
            seed=seed,
            path=abs_path,
        )
        # Validation gate (Step 2 plan): on the first source (t0106), print the first 3 surviving
        # rows verbatim and confirm the filter holds. If t0106 yields zero passing records the
        # filter must be debugged before continuing.
        if not first_passing_sample and source_task == "t0106_long_pdnd_nsga2_300gen":
            assert counts.n_passing_filter > 0, (
                f"VALIDATION GATE FAILED: t0106 post-filter count is 0 with "
                f"DSI>{DSI_THRESHOLD}, PD>{PD_THRESHOLD_HZ}. Inspect raw records."
            )
            print(
                f"  [validation gate] first 3 surviving rows from {source_task}:",
                flush=True,
            )
            for _, row in df.head(3).iterrows():
                assert row[DSI_COLUMN] > DSI_THRESHOLD
                assert row[PD_COLUMN] > PD_THRESHOLD_HZ
                print(
                    f"    gen={int(row[GENERATION_COLUMN])} idx={int(row[INDIVIDUAL_IDX_COLUMN])} "
                    f"DSI={row[DSI_COLUMN]:.4f} PD={row[PD_COLUMN]:.2f} "
                    f"v[0:3]={[round(float(row[n]), 4) for n in ALL_PARAM_NAMES[:3]]}",
                    flush=True,
                )
            first_passing_sample = True
        frames.append(df)
        counts_rows.append(counts)

    pooled: pd.DataFrame = pd.concat(frames, axis=0, ignore_index=True)
    pooled = _typed_dataframe(pooled)
    pooled.to_parquet(POOLED_SURVIVORS_PARQUET, index=False)
    print(f"\nWrote {POOLED_SURVIVORS_PARQUET} (n_rows={len(pooled)})", flush=True)

    counts_df: pd.DataFrame = pd.DataFrame(
        [
            {
                "source_task": c.source_task,
                "seed": c.seed,
                "n_raw": c.n_raw,
                "n_passing_filter": c.n_passing_filter,
                "n_unique": c.n_unique,
            }
            for c in counts_rows
        ]
    )
    total_row: pd.DataFrame = pd.DataFrame(
        [
            {
                "source_task": "TOTAL",
                "seed": -1,
                "n_raw": int(counts_df["n_raw"].sum()),
                "n_passing_filter": int(counts_df["n_passing_filter"].sum()),
                "n_unique": int(counts_df["n_unique"].sum()),
            }
        ]
    )
    counts_df_out: pd.DataFrame = pd.concat([counts_df, total_row], axis=0, ignore_index=True)
    counts_df_out.to_csv(PER_SEED_COHORT_COUNTS_CSV, index=False)
    print(f"Wrote {PER_SEED_COHORT_COUNTS_CSV}", flush=True)

    # Sanity check: pooled parquet rows equal the sum of per-seed unique counts.
    assert len(pooled) == int(counts_df["n_unique"].sum()), (
        f"row count mismatch: pooled={len(pooled)}, sum n_unique={counts_df['n_unique'].sum()}"
    )
    print(
        f"\nTotal pooled survivors: {len(pooled)} "
        f"(sum n_unique = {int(counts_df['n_unique'].sum())})",
        flush=True,
    )


if __name__ == "__main__":
    main()
