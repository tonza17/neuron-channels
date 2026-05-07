"""Phase B: 30 very-different morphologies via Latin Hypercube over the 14-d space.

Output: ``data/different_morphologies/morph_NN.json`` (NN = 00..29).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from scipy.stats import qmc  # type: ignore[import-untyped]

from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    INT_PARAM_NAMES,
    LHS_DIFFERENT_SEED,
    PARAM_BOUNDS,
    PARAM_MORPH_SEED,
    PARAM_NAMES,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_DIFFERENT_DIR,
    ensure_directories,
)

N_SAMPLES: int = 30
N_DIMS: int = 14


def _scale_lhs_row(*, row: np.ndarray) -> dict[str, float | int]:
    """Map one [0, 1)^14 LHS row to natural-units parameter values.

    Integer parameters are rounded to the nearest int and clipped to bounds.
    """
    out: dict[str, float | int] = {}
    for col, name in enumerate(PARAM_NAMES):
        lo, hi = PARAM_BOUNDS[name]
        scaled = float(lo + (hi - lo) * row[col])
        if name in INT_PARAM_NAMES:
            out[name] = int(np.clip(round(scaled), lo, hi))
        else:
            out[name] = scaled
    return out


def sample_different(
    *, n: int = N_SAMPLES, seed: int = LHS_DIFFERENT_SEED
) -> list[MorphologyParams]:
    """Generate ``n`` LHS samples and return ``n`` ``MorphologyParams`` objects."""
    sampler = qmc.LatinHypercube(d=N_DIMS, optimization="random-cd", seed=seed)
    raw = sampler.random(n=n)
    assert raw.shape == (n, N_DIMS), f"unexpected LHS shape {raw.shape}"

    # Override morph_seed column with deterministic distinct integer seeds.
    seed_rng = np.random.default_rng(seed)
    morph_seeds: np.ndarray = seed_rng.integers(low=0, high=2**31 - 1, size=n)

    out: list[MorphologyParams] = []
    seed_col = PARAM_NAMES.index(PARAM_MORPH_SEED)
    for i in range(n):
        d = _scale_lhs_row(row=raw[i, :])
        d[PARAM_MORPH_SEED] = int(morph_seeds[i])
        # Ensure the seed_col raw value is preserved (we just override the int).
        del seed_col
        seed_col = PARAM_NAMES.index(PARAM_MORPH_SEED)  # noqa: F841 (kept for clarity)
        out.append(MorphologyParams.from_dict(data=d))
    return out


def write_morphologies(
    *,
    morphs: list[MorphologyParams],
    out_dir: Path,
    prefix: str = "morph",
) -> list[Path]:
    """Write each morphology spec to ``<out_dir>/<prefix>_NN.json`` and return paths."""
    paths: list[Path] = []
    for i, m in enumerate(morphs):
        p = out_dir / f"{prefix}_{i:02d}.json"
        p.write_text(json.dumps(m.to_dict(), indent=2, sort_keys=True))
        paths.append(p)
    return paths


def main() -> None:
    ensure_directories()
    morphs = sample_different()
    paths = write_morphologies(morphs=morphs, out_dir=DATA_DIFFERENT_DIR)
    print(f"wrote {len(paths)} different morphologies to {DATA_DIFFERENT_DIR}")
    print(f"first: {paths[0].name}, last: {paths[-1].name}")


if __name__ == "__main__":
    main()
