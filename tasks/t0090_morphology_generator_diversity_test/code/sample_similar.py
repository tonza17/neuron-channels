"""Phase C: 30 very-similar morphologies via +/- 5 percent jitter around BedB base point.

Output: ``data/similar_morphologies/morph_NN.json`` (NN = 00..29).
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    BEDB_BASE_POINT,
    INT_PARAM_NAMES,
    PARAM_BOUNDS,
    PARAM_MORPH_SEED,
    PARAM_NAMES,
    PERTURB_SIMILAR_SEED,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_SIMILAR_DIR,
    ensure_directories,
)

N_SAMPLES: int = 30
JITTER_PCT: float = 0.05


def _jitter_value(
    *,
    name: str,
    base: float | int,
    rng: np.random.Generator,
) -> float | int:
    """Return ``base * (1 + uniform(-pct, +pct))`` clipped to bounds (float) or
    ``base + randint(-1, +1)`` clipped (int)."""
    lo, hi = PARAM_BOUNDS[name]
    if name in INT_PARAM_NAMES:
        if name == PARAM_MORPH_SEED:
            # Sample a fresh seed; perturbing the seed is the only sensible operation.
            return int(rng.integers(0, 2**31 - 1))
        delta = int(rng.integers(-1, 2))
        return int(np.clip(int(base) + delta, lo, hi))
    raw = float(base) * (1.0 + float(rng.uniform(-JITTER_PCT, JITTER_PCT)))
    return float(np.clip(raw, lo, hi))


def sample_similar(
    *, n: int = N_SAMPLES, seed: int = PERTURB_SIMILAR_SEED
) -> list[MorphologyParams]:
    """Generate ``n`` perturbations of the BedB base point and return them."""
    rng = np.random.default_rng(seed)
    out: list[MorphologyParams] = []
    for _ in range(n):
        d: dict[str, float | int] = {}
        for name in PARAM_NAMES:
            d[name] = _jitter_value(name=name, base=BEDB_BASE_POINT[name], rng=rng)
        out.append(MorphologyParams.from_dict(data=d))
    return out


def write_morphologies(
    *,
    morphs: list[MorphologyParams],
    out_dir: Path,
    prefix: str = "morph",
) -> list[Path]:
    paths: list[Path] = []
    for i, m in enumerate(morphs):
        p = out_dir / f"{prefix}_{i:02d}.json"
        p.write_text(json.dumps(m.to_dict(), indent=2, sort_keys=True))
        paths.append(p)
    return paths


def main() -> None:
    ensure_directories()
    morphs = sample_similar()
    paths = write_morphologies(morphs=morphs, out_dir=DATA_SIMILAR_DIR)
    print(f"wrote {len(paths)} similar morphologies to {DATA_SIMILAR_DIR}")
    print(f"first: {paths[0].name}, last: {paths[-1].name}")


if __name__ == "__main__":
    main()
