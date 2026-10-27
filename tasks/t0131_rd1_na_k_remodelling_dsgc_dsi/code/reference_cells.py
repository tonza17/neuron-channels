"""Rebuild the 675-cell LEGIT table (with 68-d vectors) and draw the reference cells."""

import gzip
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import (
    ALL_SEED_KEYS,
    EXPECTED_POOLED_ROWS,
    EXPECTED_STRATUM_COUNTS,
    LEGIT_DSI_CEILING,
    LEGIT_DSI_MIN,
    LEGIT_PD_RATE_MIN_HZ,
    RNG_SEED,
    SEED_TASK_IDS,
    STRATUM_DRAW_COUNTS,
    STRATUM_DRAW_ORDER,
)
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import (
    EVAL_DUMP_PATHS,
    T0121_PARQUET,
)


@dataclass(frozen=True, slots=True)
class LegitCell:
    cell_id: str
    seed_label: str
    source_task_id: str
    generation: int
    dsi_vector_sum: float
    pd_rate_hz: float
    vector_68d: list[float]


def load_evaluations(*, path: Path) -> list[dict[str, Any]]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as f:
            data: object = json.load(f)
    else:
        data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        evals: object = data["evaluations"]
        assert isinstance(evals, list), "evaluations payload is a list"
        return evals
    assert isinstance(data, list), "top-level payload is a list"
    return data


def is_legit_joint_pass(*, dsi: float, pd_rate_hz: float) -> bool:
    return dsi >= LEGIT_DSI_MIN and pd_rate_hz >= LEGIT_PD_RATE_MIN_HZ and dsi < LEGIT_DSI_CEILING


def build_legit_table() -> list[LegitCell]:
    cells: list[LegitCell] = []
    for key in ALL_SEED_KEYS:
        path: Path = EVAL_DUMP_PATHS[key]
        evals = load_evaluations(path=path)
        seen: set[tuple[float, ...]] = set()
        seq: int = 0
        for rec in evals:
            dsi = float(rec["dsi_vector_sum"])
            pd_rate = float(rec["pd_rate_hz"])
            if not is_legit_joint_pass(dsi=dsi, pd_rate_hz=pd_rate):
                continue
            vec_key = tuple(rec["vector_68d"])
            if vec_key in seen:
                continue
            seen.add(vec_key)
            cells.append(
                LegitCell(
                    cell_id=f"{key}_{seq:04d}",
                    seed_label=key,
                    source_task_id=SEED_TASK_IDS[key],
                    generation=int(rec["generation"]),
                    dsi_vector_sum=dsi,
                    pd_rate_hz=pd_rate,
                    vector_68d=[float(x) for x in rec["vector_68d"]],
                )
            )
            seq += 1
    return cells


def assert_matches_parquet(*, cells: list[LegitCell]) -> dict[str, int]:
    df: pd.DataFrame = pd.read_parquet(T0121_PARQUET)
    assert len(df) == EXPECTED_POOLED_ROWS, "parquet has 675 rows"
    assert len(cells) == EXPECTED_POOLED_ROWS, "rebuilt table has 675 rows"
    by_id: dict[str, LegitCell] = {c.cell_id: c for c in cells}
    assert len(by_id) == len(cells), "cell ids are unique"
    mismatches: int = 0
    for row in df.itertuples(index=False):
        cell = by_id.get(str(row.cell_id))
        if cell is None or abs(cell.dsi_vector_sum - float(row.dsi)) > 1e-12:
            mismatches += 1
    assert mismatches == 0, "all parquet cell ids and dsi values match the rebuilt table"
    counts: dict[str, int] = {}
    for c in cells:
        counts[c.seed_label] = counts.get(c.seed_label, 0) + 1
    assert counts == EXPECTED_STRATUM_COUNTS, "stratum counts match"
    return counts


def candidate_order(*, cells: list[LegitCell]) -> dict[str, list[LegitCell]]:
    """Seeded random permutation of every stratum (fixed seed, stratum order fixed)."""
    rng = np.random.default_rng(RNG_SEED)
    out: dict[str, list[LegitCell]] = {}
    for stratum in STRATUM_DRAW_ORDER:
        pool: list[LegitCell] = [c for c in cells if c.seed_label == stratum]
        perm: list[int] = [int(i) for i in rng.permutation(len(pool))]
        out[stratum] = [pool[i] for i in perm]
    return out


def stratum_quota(*, stratum: str) -> int:
    return STRATUM_DRAW_COUNTS[stratum]
