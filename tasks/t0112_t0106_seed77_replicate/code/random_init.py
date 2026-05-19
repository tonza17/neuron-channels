"""Phase A: random-init NSGA-II population builder.

Replaces t0091's 5-anchor warm-start with a Latin Hypercube Sample over the
68-d parameter space, drawn from ``np.random.SeedSequence(seed)`` for each of
the three RNG seeds 11/22/33. Each row of the (96, 68) matrix is a uniform
sample in [LOWER_BOUNDS_68, UPPER_BOUNDS_68] using ``LatinHypercubeSampling``
from pymoo (with explicit seeding for reproducibility).
"""

from __future__ import annotations

import json

import numpy as np
from numpy.typing import NDArray
from pymoo.operators.sampling.lhs import LatinHypercubeSampling

from tasks.t0112_t0106_seed77_replicate.code.constants import (
    LOWER_BOUNDS_68,
    POP_SIZE,
    T0112_SEEDS,
    UPPER_BOUNDS_68,
)
from tasks.t0112_t0106_seed77_replicate.code.paths import (
    ensure_directories,
    init_pop_json,
)


class _LHSProblem:
    """Minimal Problem-like object satisfying pymoo's LHS sampler API.

    pymoo `LatinHypercubeSampling._do` calls ``problem.bounds()`` and reads
    ``problem.n_var``. The sampler also reads ``problem.xl`` / ``problem.xu``
    in some code paths, so we expose all of them.
    """

    def __init__(self) -> None:
        self.n_var: int = 68
        self.xl: NDArray[np.float64] = LOWER_BOUNDS_68
        self.xu: NDArray[np.float64] = UPPER_BOUNDS_68

    def bounds(self) -> tuple[NDArray[np.float64], NDArray[np.float64]]:
        return self.xl, self.xu


def build_random_init_population(*, seed: int) -> NDArray[np.float64]:
    """Build a (POP_SIZE, 68) LHS sample uniformly in [LOWER_BOUNDS_68, UPPER_BOUNDS_68].

    Uses ``pymoo.operators.sampling.lhs.LatinHypercubeSampling`` with an
    explicit ``np.random.RandomState`` derived from ``np.random.SeedSequence(seed)``
    so that each of the 3 task seeds produces a deterministic but distinct sample
    that is reproducible across re-runs.
    """
    sampler = LatinHypercubeSampling()
    rng_seed_arr = np.random.SeedSequence(seed).generate_state(1)
    rng_seed = int(rng_seed_arr[0]) % (2**31 - 1)
    problem = _LHSProblem()
    random_state = np.random.RandomState(rng_seed)
    raw = sampler._do(problem, POP_SIZE, random_state=random_state)  # type: ignore[arg-type]
    # `raw` may be a numpy array (n_samples, n_var) OR a Population with .X
    # depending on pymoo version. Handle both.
    if hasattr(raw, "get"):
        x_unit = np.asarray(raw.get("X"), dtype=np.float64)
    else:
        x_unit = np.asarray(raw, dtype=np.float64)
    assert x_unit.shape == (POP_SIZE, 68), f"unexpected LHS shape {x_unit.shape}"

    # If the sampler returned [0, 1] normalised samples, map through bounds;
    # if it already mapped, clip for safety.
    if (x_unit.min() >= 0.0 - 1e-9) and (x_unit.max() <= 1.0 + 1e-9):
        sample = LOWER_BOUNDS_68 + x_unit * (UPPER_BOUNDS_68 - LOWER_BOUNDS_68)
    else:
        sample = x_unit
    sample = np.clip(sample, LOWER_BOUNDS_68, UPPER_BOUNDS_68)
    assert sample.shape == (POP_SIZE, 68)
    return sample


def write_init_population(*, seed: int) -> NDArray[np.float64]:
    ensure_directories()
    matrix = build_random_init_population(seed=seed)
    out: dict[str, object] = {
        "seed": int(seed),
        "method": "pymoo.operators.sampling.lhs.LatinHypercubeSampling",
        "shape": list(matrix.shape),
        "matrix": matrix.tolist(),
    }
    out_path = init_pop_json(seed=seed)
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[random_init] seed={seed} wrote {out_path} shape={matrix.shape}")
    return matrix


def main() -> None:
    for seed in T0112_SEEDS:
        write_init_population(seed=seed)


if __name__ == "__main__":
    main()
