"""Count cells across optimisation tasks; identify 68-d (electrophys + morphology) runs."""

from __future__ import annotations

import json
from pathlib import Path

CANDIDATES = [
    "tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/results/data/all_evaluations.json",
    "tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json",
    "tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json",
    "tasks/t0091_morphology_extended_nsga2_v1/results/data/all_evaluations.json",
    "tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed11.json",
    "tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed22.json",
    "tasks/t0099_random_init_pareto_robustness/results/data/all_evaluations_seed33.json",
    "tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed44.json",
    "tasks/t0102_seedscale_n4_gen20/results/data/all_evaluations_seed55.json",
    "tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed44.json",
    "tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/all_evaluations_seed55.json",
]


def _extract_rows(path: Path) -> list[dict]:
    with open(path) as f:
        d = json.load(f)
    if isinstance(d, dict):
        for k in ("evaluations", "rows", "cells", "items"):
            if k in d:
                return d[k]
        return []
    return d


def _vec_field(row: dict) -> str | None:
    for k in row:
        if k.startswith("vector_") or k in ("vector", "x", "parameter_vector", "params"):
            return k
    return None


total_68d = 0
total_other = 0
print(f"{'path':<92} {'rows':>6} {'dim':>5} {'keep?'}")
print("-" * 120)
for relpath in CANDIDATES:
    p = Path(relpath)
    if not p.exists():
        print(f"{relpath:<92}  MISSING")
        continue
    try:
        rows = _extract_rows(path=p)
    except Exception as e:
        print(f"{relpath:<92}  ERROR: {type(e).__name__}: {e}")
        continue
    if not rows:
        print(f"{relpath:<92}  empty")
        continue
    sample = rows[0]
    vec_key = _vec_field(sample)
    if vec_key is None:
        # try to find by length
        print(f"{relpath:<92}  no vector key found; keys={list(sample.keys())}")
        continue
    dim = len(sample[vec_key])
    keep = "yes (68d)" if dim == 68 else "no"
    print(f"{relpath:<92} {len(rows):>6} {dim:>5}  {keep}")
    if dim == 68:
        total_68d += len(rows)
    else:
        total_other += len(rows)

print()
print(f"Total 68-d cells: {total_68d}")
print(f"Total non-68d cells (excluded): {total_other}")

# Now apply filter DSI > 0.1 AND PD > 2 across 68-d files (relaxed primary)
print()
print("With RELAXED filter DSI > 0.1 AND PD > 2 Hz on 68-d files (primary cohort):")
print(f"{'path':<92} {'pass'}")
total_pass = 0
all_pass_vecs: set = set()
for relpath in CANDIDATES:
    p = Path(relpath)
    if not p.exists():
        continue
    rows = _extract_rows(path=p)
    if not rows:
        continue
    sample = rows[0]
    vec_key = _vec_field(sample)
    if vec_key is None or len(sample[vec_key]) != 68:
        continue
    n_pass = 0
    n_pass_unique = 0
    for r in rows:
        if r.get("dsi_vector_sum", 0) > 0.1 and r.get("pd_rate_hz", 0) > 2.0:
            n_pass += 1
            sig = tuple(round(v, 6) for v in r[vec_key])
            if sig not in all_pass_vecs:
                all_pass_vecs.add(sig)
                n_pass_unique += 1
    print(f"{relpath:<92} {n_pass:>6} ({n_pass_unique} new unique vectors)")
    total_pass += n_pass

print()
print(f"Total pass (with duplicates): {total_pass}")
print(f"Total pass (unique 68-d vectors): {len(all_pass_vecs)}")
