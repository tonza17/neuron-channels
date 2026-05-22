"""Pool ALL NSGA-II evaluation records across four seeds with NO cohort filter.

This is the one and only methodological change vs t0116: the
`dsi_vector_sum > 0.7 AND pd_rate_hz > 10.0` filter is removed. Every record from every source
is admitted. The dedup-by-rounded-68d-vector convention from t0116 is preserved verbatim.

Branches on file suffix:
    *.json.gz  -> gzipped JSON, structured as {"evaluations": [...]}.
    *.jsonl.gz -> gzipped JSONL, one record per line (t0114 / t0115).

Outputs:
    data/pooled_all_cells.parquet
    results/data/per_seed_pool_counts.csv

Usage:
    uv run python -u -m \
        tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.load_pooled_cells
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pandas as pd

from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.constants import (
    ALL_PARAM_NAMES,
    DEDUP_DECIMALS,
    N_TOTAL_DIMS,
    SOURCES,
)
from tasks.t0117_pooled_pca_cluster_factor_all_cells_4_seeds.code.paths import (
    PER_SEED_POOL_COUNTS_CSV,
    POOLED_ALL_CELLS_PARQUET,
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


def _build_dataframe_for_source(
    *,
    source_task: str,
    seed: int,
    path: Path,
) -> tuple[pd.DataFrame, PerSeedCounts]:
    """Load every record from one source without any cohort filter.

    The single t0117 divergence from t0116 lives here: no DSI/PD threshold gate. Every record
    with a valid 68-d vector is admitted (records with malformed vectors still fail their assert
    as before).
    """
    n_raw: int = 0
    rows: list[dict[str, object]] = []
    for individual_idx, rec in enumerate(_iter_records(path)):
        n_raw += 1
        # NO cohort filter applied — every record is admitted, in deliberate contrast to t0116.
        vec = rec.get("vector_68d")
        assert isinstance(vec, list) and len(vec) == N_TOTAL_DIMS, (
            f"unexpected vector_68d shape in {path} at idx={individual_idx}: "
            f"{None if vec is None else len(vec)!r}"
        )
        dsi_val: object = rec.get(DSI_COLUMN)
        pd_val: object = rec.get(PD_COLUMN)
        assert isinstance(dsi_val, int | float), (
            f"missing or non-numeric dsi_vector_sum in {path} at idx={individual_idx}"
        )
        assert isinstance(pd_val, int | float), (
            f"missing or non-numeric pd_rate_hz in {path} at idx={individual_idx}"
        )
        row: dict[str, object] = {
            SOURCE_TASK_COLUMN: source_task,
            SEED_COLUMN: int(seed),
            GENERATION_COLUMN: int(rec["generation"]),  # type: ignore[arg-type]
            INDIVIDUAL_IDX_COLUMN: int(individual_idx),
            DSI_COLUMN: float(dsi_val),
            PD_COLUMN: float(pd_val),
        }
        for name, val in zip(ALL_PARAM_NAMES, vec, strict=True):
            row[name] = float(val)
        rows.append(row)
    df_raw: pd.DataFrame = pd.DataFrame(rows)
    if n_raw == 0:
        df_unique: pd.DataFrame = df_raw.copy()
    else:
        rounded = df_raw[list(ALL_PARAM_NAMES)].round(DEDUP_DECIMALS)
        dedup_keys = pd.util.hash_pandas_object(rounded, index=False)
        df_raw = df_raw.assign(_dedup_key=dedup_keys.values)
        df_unique = (
            df_raw.drop_duplicates(subset=["_dedup_key"], keep="first")
            .drop(columns=["_dedup_key"])
            .reset_index(drop=True)
        )
    counts = PerSeedCounts(
        source_task=source_task,
        seed=int(seed),
        n_raw=n_raw,
        n_unique=int(len(df_unique)),
    )
    print(
        f"  {source_task} (seed {seed}): n_raw={n_raw}, n_unique={counts.n_unique}",
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
    POOLED_ALL_CELLS_PARQUET.parent.mkdir(parents=True, exist_ok=True)
    PER_SEED_POOL_COUNTS_CSV.parent.mkdir(parents=True, exist_ok=True)

    print(
        f"Pooling ALL records (no DSI/PD filter) from {len(SOURCES)} sources...",
        flush=True,
    )

    frames: list[pd.DataFrame] = []
    counts_rows: list[PerSeedCounts] = []
    first_sample: bool = False
    for source_task, seed, rel_path in SOURCES:
        abs_path: Path = REPO_ROOT / rel_path
        assert abs_path.exists(), f"missing predictions file: {abs_path}"
        df, counts = _build_dataframe_for_source(
            source_task=source_task,
            seed=seed,
            path=abs_path,
        )
        # Validation gate (Step 2 plan, relaxed): t0106 must yield non-zero records and the dedup
        # ratio must be > 0.1 (NSGA-II's converged offspring naturally collapse a lot of duplicates
        # at 6-decimal rounding; t0116's strict cohort dedup ratio was 121/658 = 18%, and t0116
        # also documented this for its own gate). A ratio at or below 0.10 means the rounding
        # decimals are wrong or every cell collapsed to a few canonical points — STOP and inspect.
        if not first_sample and source_task == "t0106_long_pdnd_nsga2_300gen":
            assert counts.n_raw > 0, (
                "VALIDATION GATE FAILED: t0106 returned n_raw=0. Inspect the JSON wrapper."
            )
            assert counts.n_unique > 0.10 * counts.n_raw, (
                f"VALIDATION GATE FAILED: t0106 dedup collapsed pool from "
                f"{counts.n_raw} to {counts.n_unique} (< 10%). Inspect dedup decimals."
            )
            print(
                f"  [validation gate] first 3 loaded rows from {source_task}:",
                flush=True,
            )
            for _, row in df.head(3).iterrows():
                print(
                    f"    gen={int(row[GENERATION_COLUMN])} idx={int(row[INDIVIDUAL_IDX_COLUMN])} "
                    f"DSI={row[DSI_COLUMN]:.4f} PD={row[PD_COLUMN]:.2f} "
                    f"v[0:3]={[round(float(row[n]), 4) for n in ALL_PARAM_NAMES[:3]]}",
                    flush=True,
                )
            first_sample = True
        frames.append(df)
        counts_rows.append(counts)

    pooled: pd.DataFrame = pd.concat(frames, axis=0, ignore_index=True)
    pooled = _typed_dataframe(pooled)
    pooled.to_parquet(POOLED_ALL_CELLS_PARQUET, index=False)
    print(f"\nWrote {POOLED_ALL_CELLS_PARQUET} (n_rows={len(pooled)})", flush=True)

    counts_df: pd.DataFrame = pd.DataFrame(
        [
            {
                "source_task": c.source_task,
                "seed": c.seed,
                "n_raw": c.n_raw,
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
                "n_unique": int(counts_df["n_unique"].sum()),
            }
        ]
    )
    counts_df_out: pd.DataFrame = pd.concat([counts_df, total_row], axis=0, ignore_index=True)
    counts_df_out.to_csv(PER_SEED_POOL_COUNTS_CSV, index=False)
    print(f"Wrote {PER_SEED_POOL_COUNTS_CSV}", flush=True)

    # Sanity check: pooled parquet rows equal the sum of per-seed unique counts.
    assert len(pooled) == int(counts_df["n_unique"].sum()), (
        f"row count mismatch: pooled={len(pooled)}, sum n_unique={counts_df['n_unique'].sum()}"
    )
    print(
        f"\nTotal pooled records: {len(pooled)} "
        f"(sum n_unique = {int(counts_df['n_unique'].sum())})",
        flush=True,
    )


if __name__ == "__main__":
    main()
