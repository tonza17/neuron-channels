---
spec_version: "1"
task_id: "t0107_t0106_polar_8dir_recheck"
date_created: "2026-05-18"
---
# Research Code: Reuse t0106 Evaluator at 8-Direction Protocol

## Task Objective

Identify the minimum code path to re-evaluate a single cell's 68-d parameter vector at an arbitrary
direction set, reusing the existing t0106 evaluator without re-implementing the NEURON / pymoo
machinery. Produce the per-direction firing rates needed for polar tuning-curve plots on 10 cells
from the t0106 top 50.

## Library Landscape

The only directly relevant in-project library is the t0106 evaluator stack. No external library
matches the t0106 evaluator's interface (NEURON 8.2.7 + custom Bed B / morphology generator + DSI
silence guard). Re-implementing from scratch would be far more work than reusing t0106's code.

Within the project: t0099 / t0102 / t0104 evaluators are earlier sibling versions of the same
evaluator; t0091's evaluator predates the 14-d morphology fix. The t0106 version is the canonical
one because it incorporates S-0102-01 (silence guard), C-0093-01 (morphology generator patch), and
the 2-direction ratio-DSI mode.

## Key Findings

* `evaluate_68d_vector(vector_68d, n_directions, eval_seeds)` already accepts `n_directions = 8` via
  `ANGLES_8DIR_DEG`. No algorithm patch needed for the direction count itself.
* The public return value of `evaluate_68d_vector` exposes aggregate DSI and PD-rate but does NOT
  expose per-direction firing rates. For polar plots we need per-direction rates, so a small patch
  adds `per_direction_rates_hz` (length-`n_directions` array) to the return dataclass.
* The t0106 mod compilation (`code/mods/`) is reusable: the same NEURON shared library can run both
  2-direction and 8-direction protocols since the angle is a per-trial parameter, not a compiled
  constant.
* Cell selection from `tasks/t0106_*/results/data/all_evaluations_seed44.json.gz`: 3,744
  evaluations, dedup by (DSI, PD), joint-corner-rank, top 50. Sample 10 deterministically with numpy
  seed 42.
* Local execution is feasible: 10 cells x 8 dirs x 3 trials = 240 NEURON sims at ~0.3 s each = ~75 s
  wall clock. No Vast.ai needed.

## Reusable Code and Assets

| Source file (t0106) | Action | Destination (t0107) |
| --- | --- | --- |
| `code/evaluator.py` | copy + small patch to expose `per_direction_rates_hz` | `code/evaluator.py` |
| `code/constants_electrophys.py` | copy verbatim | `code/constants_electrophys.py` |
| `code/constants_morphology.py` | copy verbatim | `code/constants_morphology.py` |
| `code/constants.py` | copy verbatim | `code/constants.py` |
| `code/paths.py` | copy + rename task slug t0106 -> t0107 | `code/paths.py` |
| `code/generator_wrapper.py` | copy verbatim | `code/generator_wrapper.py` |
| `code/recorder.py` | copy verbatim | `code/recorder.py` |
| `code/trial_helpers.py` | copy verbatim | `code/trial_helpers.py` |
| `code/build_cell_ais.py` | copy verbatim | `code/build_cell_ais.py` |
| `code/apply_params.py` | copy verbatim | `code/apply_params.py` |
| `code/extend_with_ais.py` | copy verbatim | `code/extend_with_ais.py` |
| `code/parametric_placer.py` | copy verbatim | `code/parametric_placer.py` |
| `code/mods/` | copy verbatim (the .o / .so / nrnmech.dll already compiled) | `code/mods/` |

New files unique to t0107:

* `code/sample_top10.py` — load t0106 evaluations, dedup, joint-corner-rank, sample 10 with numpy
  seed 42, write `selected_cells.json`.
* `code/eval_polar.py` — for each selected cell, call
  `evaluate_68d_vector(vec, n_directions=8, eval_seeds=[...])`, collect per-direction rates, write
  `per_cell_polar.json`.
* `code/plot_polar.py` — render the 10-cell polar grid into
  `results/images/polar_tuning_curves_top10.png`.

## Lessons Learned

The 2-direction reformulation in t0106 was lucky in that the evaluator's
`evaluate_68d_vector(n_directions=N)` was already direction-count-parameterised even when t0099 /
t0102 / t0104 only ever invoked it with N = 16. The 2-direction case was always a one-argument
change away from working. That same flexibility now makes t0107 cheap to build: zero algorithm work,
just data plumbing.

## Recommendations for This Task

1. Copy 13 files verbatim from t0106; patch only `evaluator.py` to surface per-direction rates.
2. Write the 3 new scripts described above. Keep them simple and stateless.
3. Run locally; no Vast.ai. Use the t0106 nrnmech.dll cached at
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/build/` (per the t0106 smoke gate
   precedent).
4. Save the per-direction firing-rate matrix as part of the predictions asset so any downstream task
   can re-plot or re-analyse without re-running NEURON.

## Task Index

* `t0106_long_pdnd_nsga2_300gen` — source of the top-50 cells and the canonical evaluator
* `t0102_seedscale_n4_gen20` — sibling evaluator with the same silence-guard inheritance pattern
* `t0093_resweep_and_t0090_correction` — morphology generator patch (transitively inherited via
  t0106)
* `t0024_port_de_rosenroll_2026_dsgc` — Bed B substrate
* `t0080_bedb_mobo_v3_dendritic_spike_nsga2` — MOD library (reused .so / .dll)
