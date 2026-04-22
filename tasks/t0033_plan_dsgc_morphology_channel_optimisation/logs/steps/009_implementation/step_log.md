---
spec_version: "3"
task_id: "t0033_plan_dsgc_morphology_channel_optimisation"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-04-22T14:54:43Z"
completed_at: "2026-04-22T16:16:00Z"
---
## Summary

Spawned an implementation subagent that produced the full feasibility plan and Vast.ai GPU cost
estimate for a future joint DSGC morphology + top-10 voltage-gated channel DSI-maximisation
optimisation. Committed parameter count is 25 free parameters (tight: 5 Cuntz morphology + 20 VGC
gbar) with a 45-parameter rich envelope. Recommendation: **Surrogate-NN-assisted GA × Surrogate-NN-
GPU × RTX 4090 × tight parameterisation → $50.54 central, $23-$119 sensitivity band**. All 11
requirements from `plan/plan.md` are `done`.

## Actions Taken

1. Spawned a general-purpose subagent with the `/implementation` skill instructions and a prompt
   covering all 6 deliverables (code, data, charts, answer asset, asset verification, REQ
   checklist).
2. Subagent wrote `code/paths.py`, `code/constants.py`, `code/enumerate_params.py`,
   `code/search_space.py`, `code/wall_time.py`, `code/pricing.py`, `code/cost_model.py`,
   `code/make_charts.py` — all conforming to the project Python style guide (dataclasses, keyword
   args, absolute imports, pathlib, explicit dtypes). Code passes `ruff check` and `mypy` clean.
3. Subagent ran the scripts to generate the data tables in `data/`: `parameter_summary.json`,
   `morphology_params.json`, `channel_params_hhst.json`, `top10_vgcs.json`,
   `search_space_table.csv`, `sim_wall_time.csv`, `per_tier_wall_time.csv`,
   `vastai_pricing_snapshot.json`, `cost_envelope.csv` (70 rows), `sensitivity_grid.csv` (630 rows),
   `cost_model_summary.json`.
4. Subagent rendered three charts to `results/images/`: `parameter_count_breakdown.png`,
   `cost_by_strategy_and_tier.png`, `sensitivity_heatmap.png`.
5. Subagent produced the answer asset at
   `assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/` with
   `details.json`, `short_answer.md` (2-5 sentences), and `full_answer.md` (all 9 mandatory
   sections).
6. `verify_answer_asset` is not present in the project's verificator directory; the subagent
   performed a manual specification check against `meta/asset_types/answer/specification.md` (all 14
   required `details.json` fields present, short answer has 3 sentences in the 2-5 band, no inline
   citations in `## Short Answer` / `## Answer`, full answer has all 9 mandatory sections).

## Outputs

* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/code/` (8 Python files)
* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/data/` (11 files: JSON + CSV)
* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/results/images/` (3 PNG charts)
* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/assets/answer/vastai-cost-of-joint-dsgc-morphology-channel-dsi-optimisation/`
  (3 files)
* `tasks/t0033_plan_dsgc_morphology_channel_optimisation/logs/commands/...` (run_with_logs entries)

## Issues

`verify_answer_asset.py` is referenced in the orchestrator skill (Phase 6 reporting step) but is not
present in `arf/scripts/verificators/`. Substituted with a manual specification check against
`meta/asset_types/answer/specification.md`. Framework gap should be flagged in a downstream
infrastructure PR.

Documented assumptions that extend beyond the downloaded paper corpus: (a) CoreNEURON CPU→GPU
speedup = 5× vs stock NEURON CPU; (b) surrogate-NN training sample cost = 5000 full NEURON
simulations; (c) surrogate-NN inference speedup = 100× vs full simulation. Each assumption is stated
explicitly in the full answer's `## Limitations` section, and the 3×3 sensitivity grid bounds the
effect.
