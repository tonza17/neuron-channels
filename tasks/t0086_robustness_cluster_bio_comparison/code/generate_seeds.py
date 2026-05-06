"""Generate 5 deterministic outer RNG seeds from SeedSequence(42).spawn(5).

Writes results/data/replication_seeds.json with the parent seed and the
spawned seeds. Same parent seed across all 20 cells; same 5 seeds applied
to each cell so per-cell variance is comparable.
"""

from __future__ import annotations

import json

import numpy as np

from tasks.t0086_robustness_cluster_bio_comparison.code.paths import (
    REPLICATION_SEEDS_JSON,
    ensure_directories,
)

PARENT_SEED: int = 42
N_REPLICATIONS: int = 5


def generate_seeds() -> dict[str, object]:
    # SeedSequence.spawn() returns children whose entropy field equals the
    # parent's entropy (the spawn key differentiates them). We need to call
    # generate_state(1) on each to extract a 32-bit seed.
    seq = np.random.SeedSequence(PARENT_SEED)
    children = seq.spawn(N_REPLICATIONS)
    seeds: list[int] = [int(c.generate_state(1, dtype=np.uint32)[0]) for c in children]
    assert len(seeds) == N_REPLICATIONS, f"expected {N_REPLICATIONS}, got {len(seeds)}"
    assert len(set(seeds)) == N_REPLICATIONS, "seeds are not distinct"
    assert all(s > 0 for s in seeds), "expected all positive seeds"
    return {
        "parent_seed": PARENT_SEED,
        "n_replications": N_REPLICATIONS,
        "seeds": seeds,
    }


def main() -> None:
    ensure_directories()
    out = generate_seeds()
    REPLICATION_SEEDS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[generate_seeds] wrote {REPLICATION_SEEDS_JSON} with seeds={out['seeds']}")


if __name__ == "__main__":
    main()
