"""Sample 10 cells from the t0106 top-50 by joint-corner ranking.

Loads the gzipped all-evaluations JSON produced by the t0106 NSGA-II run,
deduplicates by (round(dsi, 4), round(pd, 2)), ranks the unique cells by the
joint-corner score `min(dsi/0.5, 1) * min(pd/30, 1)` (ties broken by
`dsi + pd/100`, higher is better), takes the top 50, and samples 10 of them
uniformly at random with `numpy.random.default_rng(42)`.

Writes the chosen cells to `code/selected_cells.json` as a JSON object with
the field "cells" mapping to a list of 10 dicts of:
    t0106_rank, t0106_generation, t0106_dsi, t0106_pd_hz, vector_68d.
"""

from __future__ import annotations

import gzip
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from tasks.t0107_t0106_polar_8dir_recheck.code.paths import (
    CODE_DIR,
    REPO_ROOT,
)

T0106_ALL_EVALS_JSON_GZ: Path = (
    REPO_ROOT
    / "tasks"
    / "t0106_long_pdnd_nsga2_300gen"
    / "results"
    / "data"
    / "all_evaluations_seed44.json.gz"
)

SELECTED_CELLS_JSON: Path = CODE_DIR / "selected_cells.json"

# Joint-corner reference scales.
DSI_CORNER_SCALE: float = 0.5
PD_CORNER_SCALE_HZ: float = 30.0

TOP_N: int = 50
SAMPLE_N: int = 10
RANDOM_SEED: int = 42


@dataclass(frozen=True, slots=True)
class T0106Evaluation:
    generation: int
    dsi: float
    pd_hz: float
    vector_68d: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class RankedCell:
    rank: int
    generation: int
    dsi: float
    pd_hz: float
    score: float
    vector_68d: tuple[float, ...]


def _load_evaluations(*, path: Path) -> list[T0106Evaluation]:
    with gzip.open(path, "rt") as f:
        data = json.load(f)
    assert isinstance(data, dict), f"expected dict at top level, got {type(data).__name__}"
    raw: list[dict[str, object]] = data["evaluations"]
    assert isinstance(raw, list) and len(raw) > 0, "evaluations field must be a non-empty list"
    out: list[T0106Evaluation] = []
    for r in raw:
        vec = r["vector_68d"]
        assert isinstance(vec, list) and len(vec) == 68
        out.append(
            T0106Evaluation(
                generation=int(r["generation"]),  # type: ignore[arg-type]
                dsi=float(r["dsi_vector_sum"]),  # type: ignore[arg-type]
                pd_hz=float(r["pd_rate_hz"]),  # type: ignore[arg-type]
                vector_68d=tuple(float(x) for x in vec),
            )
        )
    return out


def _deduplicate(*, evaluations: list[T0106Evaluation]) -> list[T0106Evaluation]:
    seen: set[tuple[float, float]] = set()
    out: list[T0106Evaluation] = []
    for e in evaluations:
        key: tuple[float, float] = (round(e.dsi, 4), round(e.pd_hz, 2))
        if key in seen:
            continue
        seen.add(key)
        out.append(e)
    return out


def _joint_corner_score(*, dsi: float, pd_hz: float) -> float:
    return min(dsi / DSI_CORNER_SCALE, 1.0) * min(pd_hz / PD_CORNER_SCALE_HZ, 1.0)


def _rank_top(*, evaluations: list[T0106Evaluation], top_n: int) -> list[RankedCell]:
    scored: list[tuple[float, float, T0106Evaluation]] = []
    for e in evaluations:
        primary = _joint_corner_score(dsi=e.dsi, pd_hz=e.pd_hz)
        tiebreak = e.dsi + e.pd_hz / 100.0
        scored.append((primary, tiebreak, e))
    # Sort descending by primary then tiebreak.
    scored.sort(key=lambda t: (t[0], t[1]), reverse=True)
    top = scored[:top_n]
    return [
        RankedCell(
            rank=i + 1,
            generation=e.generation,
            dsi=e.dsi,
            pd_hz=e.pd_hz,
            score=primary,
            vector_68d=e.vector_68d,
        )
        for i, (primary, _tb, e) in enumerate(top)
    ]


def _sample_n(*, top: list[RankedCell], n_sample: int, seed: int) -> list[RankedCell]:
    rng = np.random.default_rng(seed)
    chosen_idx: np.ndarray = rng.choice(len(top), n_sample, replace=False)
    out: list[RankedCell] = []
    for i in chosen_idx.tolist():
        out.append(top[int(i)])
    return out


def main() -> None:
    print(f"Reading t0106 evaluations from {T0106_ALL_EVALS_JSON_GZ}")
    evals = _load_evaluations(path=T0106_ALL_EVALS_JSON_GZ)
    print(f"  Loaded {len(evals)} raw evaluations")
    uniq = _deduplicate(evaluations=evals)
    print(f"  After dedup by (round(DSI, 4), round(PD, 2)): {len(uniq)}")
    top = _rank_top(evaluations=uniq, top_n=TOP_N)
    print(f"  Top {len(top)} by joint-corner score (DSI/0.5 * PD/30, ties by dsi+pd/100)")
    print("  Top 10 of the top-50 by score:")
    for r in top[:10]:
        print(
            f"    rank={r.rank:2d}  gen={r.generation:3d}  "
            f"DSI={r.dsi:.4f}  PD={r.pd_hz:6.2f} Hz  score={r.score:.4f}"
        )
    chosen = _sample_n(top=top, n_sample=SAMPLE_N, seed=RANDOM_SEED)
    chosen.sort(key=lambda c: c.rank)
    print(f"\n  Sampled {len(chosen)} cells with numpy.random.default_rng({RANDOM_SEED}):")
    for c in chosen:
        print(f"    rank={c.rank:2d}  gen={c.generation:3d}  DSI={c.dsi:.4f}  PD={c.pd_hz:6.2f} Hz")

    payload: dict[str, object] = {
        "source_path": str(T0106_ALL_EVALS_JSON_GZ),
        "top_n": TOP_N,
        "sample_n": SAMPLE_N,
        "random_seed": RANDOM_SEED,
        "dsi_corner_scale": DSI_CORNER_SCALE,
        "pd_corner_scale_hz": PD_CORNER_SCALE_HZ,
        "cells": [
            {
                "t0106_rank": c.rank,
                "t0106_generation": c.generation,
                "t0106_dsi": c.dsi,
                "t0106_pd_hz": c.pd_hz,
                "joint_corner_score": c.score,
                "vector_68d": list(c.vector_68d),
            }
            for c in chosen
        ],
    }
    SELECTED_CELLS_JSON.write_text(
        json.dumps(payload, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nWrote {SELECTED_CELLS_JSON}")
    # Silence unused-import warnings.
    _ = asdict


if __name__ == "__main__":
    main()
