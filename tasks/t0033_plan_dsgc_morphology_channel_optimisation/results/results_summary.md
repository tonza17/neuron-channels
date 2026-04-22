# Results Summary: Plan DSGC Morphology + VGC DSI Optimisation on Vast.ai GPU

## Summary

Produced a full feasibility plan and Vast.ai GPU cost envelope for a future joint DSGC morphology
+ top-10 voltage-gated channel DSI-maximisation optimisation. Committed parameter count: **25 free
  parameters tight** (5 Cuntz morphology scalars + 20 per-region channel gbar) with a **45-parameter
  rich** upper-bound envelope. Recommended (strategy × compute mode × GPU tier):
  **Surrogate-NN-assisted GA × Surrogate-NN-GPU × RTX 4090 × tight parameterisation** → central
  estimate **$50.54**, sensitivity band **$23-$119** under 0.5×/1×/2× perturbations to per-sim cost
  and sample count.

## Metrics

* **Parameter count (tight committed)**: **25** free parameters (5 Cuntz morphology + 20 per-region
  VGC gbar); rich upper-bound envelope: **45** parameters.
* **Expected simulation counts**: random baseline **2,000**; CMA-ES **1,300**; Bayesian optimisation
  **500**; surrogate-NN-GA **18,500** (5,000 NEURON training samples + 13,500 GA evaluations on the
  surrogate); grid **10^25** (reported as infeasibility anchor).
* **Per-simulation wall-time (empirical, from t0026)**: **456 s** deterministic, **1,440 s**
  stochastic per full 12-angle × 10-trial protocol (derived from 3.8 s and 12.0 s per (angle, trial)
  respectively).
* **Recommended USD on RTX 4090**: central **$50.54** (Surrogate-NN-GA × Surrogate-NN-GPU × tight);
  sensitivity band **$23-$119** across 3×3 perturbation grid.
* **Cost-floor CPU comparator**: Vast.ai CPU-96 at $0.40/h gives **$32.38** for
  Surrogate-NN-GA-tight — within the recommended GPU sensitivity band but surrenders future scaling
  headroom.

## Verification

* `verify_task_file.py` — target 0 errors on final pass.
* `verify_task_dependencies.py` — PASSED on step 2 (all six dependencies completed).
* `verify_research_papers.py` — PASSED on step 4 (0 errors, 0 warnings).
* `verify_research_code.py` — PASSED on step 6 (0 errors, 0 warnings).
* `verify_plan.py` — PASSED on step 7 (0 errors, 0 warnings).
* `verify_task_metrics.py` — target 0 errors (`metrics.json` is `{}` because no registered project
  metrics apply to a planning/answer-question task).
* `verify_task_results.py` — target 0 errors on final pass.
* `verify_task_folder.py` — target 0 errors on final pass.
* `verify_logs.py` — target 0 errors on final pass.
* Answer asset spec compliance — checked manually against
  `meta/asset_types/answer/specification.md`; all 14 required `details.json` fields present,
  short-answer 3 sentences in 2-5 band, no inline citations in `## Short Answer` / `## Answer`, full
  answer has all 9 mandatory sections.
* `ruff check --fix` and `ruff format` PASSED;
  `mypy -p tasks.t0033_plan_dsgc_morphology_channel_optimisation.code` PASSED with no issues.
