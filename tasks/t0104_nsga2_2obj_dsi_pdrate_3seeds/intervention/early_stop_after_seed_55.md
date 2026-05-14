---
type: scope-change
decided_by: researcher
decided_at: "2026-05-13T21:55:00Z"
affected_reqs: ["REQ-9", "REQ-10", "REQ-12"]
---
# Early Stop After Seed 55: Skip Seed 66

## Decision

The researcher (mailto:a.nikolaev@sheffield.ac.uk) explicitly directed at 2026-05-13 ~21:55 UTC ("I
don't think we need the third seed. Finish the second and wrap up") to terminate the implementation
step after seed 55 completes, rather than continuing to seed 66 as originally planned.

## Context at Time of Decision

* **Seed 44**: COMPLETE — 12 gens (watchdog tripped before gen 13), 1,152 cells evaluated, final
  HV = 2.85, final per-seed cost $4.69. Pareto front exhibits the t0102 L-shape: max DSI = 0.41, max
  PD = 75 Hz, but zero joint-pass cells.

* **Seed 55**: IN PROGRESS at gen 10 — 864 cells evaluated through gen 9, gen 10 actively running
  on remote workers (about 2 h wall-clock into the generation, normal for late-gen NEURON memory
  accumulation). Current best cell: DSI = 0.4192 at PD = 15.00 Hz (gen 8, also preserved at gen 9
  with a sibling at DSI = 0.4045 / PD = 11.43 Hz). HV = 6.90. No joint-pass cells yet.

* **Seed 66**: queued via the `t0104_launcher` tmux session, waiting for seed 55's pareto file to
  appear before auto-starting.

* **Instance cost**: $8.61 / $15.00 hard task cap at the time of decision; $7.97 productive, $0.64
  idle/setup.

## Rationale (Researcher's Reading)

Two seeds with independent random-init LHS have now converged to the same qualitative answer to Key
Question 1:

> Q1: Does dropping the robustness objective recover joint-pass cells (DSI >= 0.5 AND PD >= 30 Hz)
> on the 68-d Bed B + morphology substrate at random init?

A: **No, with high confidence on the substrate-empty side.**

* Seed 44 reached max DSI = 0.41 on the silenced-firing branch and max PD = 75 Hz on the null-DSI
  branch, with zero joint-pass cells across 1,152 evaluations.
* Seed 55 reached max DSI = 0.42 / PD = 15 Hz (its joint-corner-closest cell), with zero joint-pass
  cells across 864 evaluations and the same characteristic L-shape Pareto.
* Both seeds explored the substrate from two genuinely independent random-init LHS samples. A third
  seed would cost another ~$4 and is highly unlikely to break the L-shape — the signal is already
  saturated.

The marginal information from seed 66 is judged not worth the additional ~$4 of Vast.ai compute when
the two-seed result is already publishable as a definitive negative.

## Effect on Requirements

* **REQ-9** (run NSGA-II at seeds 44, 55, 66): **Partial** — only seeds 44 and 55 will be run.
  Seed 66's launcher tmux session has been killed to prevent auto-start once seed 55's pareto file
  appears.
* **REQ-10** (3 predictions assets each pass `verify_predictions_asset`): **Partial** — only 2
  predictions assets will be produced (one for seed 44, one for seed 55).
* **REQ-12** (1 answer asset addressing joint-pass recovery): unchanged — the answer is now
  delivered on a 2-seed basis. The answer asset will note this scope reduction and the rationale.

## Actions Taken at Decision Time

1. Killed the `t0104_launcher` tmux session on Vast.ai instance 36645796 at 2026-05-13T21:56 UTC to
   prevent seed 66 from auto-starting when seed 55 completes.
2. Wrote this intervention file to document the scope change.
3. Will let seed 55 run to its natural watchdog trip (estimated gen 12-13).
4. Will tear down the Vast.ai instance immediately after seed 55 writes its pareto file.
5. Will proceed with the remaining task steps (teardown, creative-thinking, results,
   compare-literature, suggestions, reporting) on 2-seed data.

## Files Affected

* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/task.json` — `expected_assets` will be updated to
  `{"predictions": 2, "answer": 1}` at the reporting step.
* `tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/plan/plan.md` — REQ-9 / REQ-10 will be re-classified
  in `results_detailed.md` `## Task Requirement Coverage`.

## Cost Recovery

Killing the launcher saves the projected ~$4 of seed 66 compute. Final task cost is now projected at
~$10-11 instead of the earlier $14-15 estimate.
