# Patched-generator full 60-morph re-sweep + t0090 correction overlay

## Motivation

Task t0092 confirmed the soma `pt3dadd` collapse as the load-bearing root cause of t0090's 0/60
spike rate, and shipped a thin shim `generate_fixed_morphology` that recovered firing for the
BedB-equivalent and 5/5 STABLE-from-t0090 cells under the t0083 best-cell channel set. But the t0092
validation set was small: 1 BedB-equivalent + 5 of t0090's 9 STABLE cells. The remaining 51
NAN_VOLTAGE cells from t0090's diversity sweep were never re-tested with the patch, so the
project-level evidence that the bug is fully fixed is incomplete.

This task closes that gap by re-running t0090's full 60-morph Phase D verification (30 LHS-sampled
"different" + 30 +/-5% "similar") under the patched generator and the unmodified t0083 best-cell
parameter vector, then issuing a correction overlay against t0090's
`procedural_dsgc_morphology_generator` library asset so that downstream consumers (t0091 NSGA-II,
future morph-extended runs, t0086 / t0088 cluster re-score work) see the patched generator as the
canonical entry point. Without the correction, downstream skills walking the library aggregator
would re-import the unpatched generator and re-introduce the bug.

## Scope

### In Scope

* Re-run the t0090 60-morphology Phase D verification (30 different + 30 similar) under the patched
  `generate_fixed_morphology` from t0092, with the unmodified t0083 best-cell parameter vector and
  the same 8-direction bar protocol (1400 ms / direction, HH on, single seed per direction matching
  t0090's protocol).
* Compare per-morph results to t0090's pre-fix `verification_summary.json` and produce a
  side-by-side delta JSON quantifying: how many of the 51 NAN_VOLTAGE cells now reach STABLE, how
  many of the 9 STABLE cells now produce spikes, total fraction of cells producing PD-rate
  > 0 Hz post-fix.
* Visualisations: morphology-grid panel coloured by post-fix stability flag (STABLE-firing /
  STABLE-silent / NAN_VOLTAGE / DIVERGED); paired bar chart of pre-fix vs post-fix spike count per
  cell.
* Issue a `replace` correction overlay against t0090's `procedural_dsgc_morphology_generator`
  library asset pointing consumers at t0092's `procedural_dsgc_morphology_generator_fix`. Verify the
  corrections-aware aggregator output reflects the supersession.
* Document the registered metric `direction_selectivity_index` per population
  (`different_set_post_fix`, `similar_set_post_fix`) in the explicit-variant `metrics.json`.

### Out of Scope

* Modifying t0090's library or any other completed task folder (immutable per ARF rules; the
  correction overlay is the only mechanism).
* Refining the soma area to match t0024's 287 µm² reference (S-0092-02 follow-up).
* Investigating the synapse-XY symmetry residual on the BedB base point (S-0092-04 follow-up).
* Joint 68-d NSGA-II run (deferred to t0091).
* Phase G validation triplet re-runs (deferred until BedB-equivalent DSI > 0.1, addressed by
  S-0092-04).

## Approach

### Phase A — Re-sweep driver (under the patched generator)

Implement `code/resweep_driver.py` modelled on t0090's `verification.py` but importing
`generate_fixed_morphology` from t0092's library asset
(`from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`).
For each of the 60 morphologies in t0090's `data/different_morphologies/` and
`data/similar_morphologies/`, build the patched cell, run the 50 ms no-stim stability check, then
the 8-direction bar protocol with the t0083 best-cell vector. Use the same
`SEED_BASE + int(morph_seed)` trial-seed pattern as t0090 to keep results comparable.

Parallelise on the 64-core EPYC via `ProcessPoolExecutor`. Save 60 results to
`data/post_fix_verification_summary.json` with the same row schema as t0090's
`verification_summary.json` plus a `pre_fix_stability_flag` and `pre_fix_spike_count_total` column
copied from t0090 for easy diffing.

**Validation gate**: run on the first 5 morphologies (limit=5) before scaling to 60. Baseline
expectation: at least 4/5 reach STABLE (vs t0090's 0/5 for the same first-5 cells). If the small-run
reproduces t0090's NAN_VOLTAGE pattern, halt and debug — the patch is not being applied.

**Time**: ~30 min on 64 cores. **Cost**: $0.

### Phase B — Pre-fix vs post-fix delta analysis

Implement `code/delta_analysis.py` reading both t0090's `verification_summary.json` and the new
`post_fix_verification_summary.json`. Produce `data/pre_post_delta.json` with:

* Per-cell delta entries: `morph_id`, `population`, `pre_stability_flag`, `post_stability_flag`,
  `pre_spike_count_total`, `post_spike_count_total`, `transition_label` (e.g.
  `nan_to_stable_firing`, `stable_silent_to_stable_firing`, `unchanged_nan`,
  `regression_stable_to_nan`).
* Aggregate counts: how many cells in each transition class.
* Pass criterion: at least 50/60 cells produce non-zero PD-rate post-fix. Stretch: 55/60.

If pass criterion is not met, surface which cells regressed and why; document but do not halt (the
correction overlay is independent of the pass-criterion outcome — t0091 needs the correction
whether 50 or 55 or 60 cells fire).

### Phase C — Visualisations

* `results/images/post_fix_morphology_grid.png`: 5x6 grid of the 30 different morphologies (or 60 in
  a 6x10 layout) coloured by post-fix stability flag.
* `results/images/pre_vs_post_spike_counts.png`: paired bar chart, one bar pair per cell, pre-fix
  red vs post-fix green, sorted by post-fix spike count descending.
* `results/images/transition_sankey.png` (or stacked bar if Sankey is too heavy): cell-count flow
  from pre-fix-flag to post-fix-flag, showing how many NAN_VOLTAGE cells became STABLE, etc.

### Phase D — Correction overlay against t0090

Write `tasks/t0093_../corrections/library_procedural_dsgc_morphology_generator.json` per
`arf/specifications/corrections_specification.md` with:

* `spec_version: "3"`
* `correction_id: "C-0093-01"`
* `correcting_task: "t0093_patched_morph_generator_resweep_and_t0090_correction"`
* `target_task: "t0090_morphology_generator_diversity_test"`
* `target_kind: "library"`
* `target_id: "procedural_dsgc_morphology_generator"`
* `action: "replace"`
* `changes`: pointer to the replacement asset
  (`tasks/t0092_diagnose_morphology_generator_silence/assets/library/procedural_dsgc_morphology_generator_fix/`)
* `rationale`: cite the post-fix re-sweep results, the t0092 root-cause diagnosis (soma pt3d
  collapse), and the t0091 dependency.

Verify the correction format passes `verify_corrections.py` and the library aggregator's effective
output now lists the t0092 library as the canonical procedural DSGC morphology generator.

### Phase E — Metrics + summary

Read `data/post_fix_verification_summary.json`; aggregate `direction_selectivity_index` per
population (mean over STABLE-and-firing cells only; null if none). Write `results/metrics.json` in
explicit-variant format with two variants (`different_set_post_fix`, `similar_set_post_fix`).

## Pass Criteria

* **At least 50/60 cells produce non-zero PD-rate** post-fix on the full re-sweep (vs 0/60 pre-fix).
* **Stretch: 55/60 cells fire post-fix.**
* The `replace` correction overlay against t0090's `procedural_dsgc_morphology_generator` is written
  and `verify_corrections.py` passes.
* The library aggregator's corrections-aware output lists t0092's
  `procedural_dsgc_morphology_generator_fix` as the canonical entry for the procedural DSGC
  morphology generator after running with the corrections overlay applied.
* `data/post_fix_verification_summary.json` exists with 60 entries; matches t0090's row schema plus
  pre-fix-comparison columns.
* All visualisations under `results/images/` are embedded in `results_detailed.md`.

**Acceptable negative**: if fewer than 50/60 cells fire post-fix, document the breakdown of
remaining failure modes (e.g. asymmetry-knob extreme values that survive the soma fix), record the
per-population pass rate, and still issue the correction overlay — the correction is about
canonicalising the patched generator regardless of how many cells the patch recovers.

## Compute and Budget

* **Local 64-core EPYC** for Phase A. No remote machines required.
* **Total cost**: $0. Single-process NEURON simulations parallelised across 64 cores; ~30 min
  wall-clock for Phase A; visualisations and correction overlay add ~30 min total.

## Time Estimation

* Phase A (re-sweep driver + run): ~45 min including the validation-gate small run.
* Phase B (delta analysis): ~30 min.
* Phase C (visualisations): ~30 min.
* Phase D (correction overlay): ~15 min including verifier.
* Phase E (metrics + summary): ~15 min.
* Plus reporting, results, suggestions, PR + merge.
* **Total wall-clock**: ~3-4 hours.

## Expected Assets

* No new library or answer assets. The deliverables are: the post-fix verification summary, the
  delta analysis, the visualisations, the registered-metric report, and the correction overlay.

## Risks and Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| The validation-gate small run reproduces t0090's NAN_VOLTAGE pattern (patch not being applied) | Low | Bug in import path or fix-shim invocation | Halt at the gate; inspect `cell.soma.L` after `generate_fixed_morphology`; should be ~15 µm not ~1e-9. |
| Post-fix re-sweep has fewer than 50/60 cells firing | Medium | Pass criterion miss | Document the surviving failure modes per `transition_label`; correction overlay is independent. The acceptable-negative branch records the per-population pass rate. |
| ProcessPoolExecutor on Windows has high per-worker NEURON DLL load cost | Medium | Wall-clock blow-out | Single-process serial execution as fallback; ~5 min × 60 = 5 hours, still within the day's budget. |
| Correction-overlay format error | Low | `verify_corrections.py` fails | Read the spec carefully before writing; test on a copy first. |

## Verification Criteria

* `data/post_fix_verification_summary.json` exists with **60 entries**.
* At least 50/60 entries have `pd_rate_hz > 0` (pass criterion).
* `data/pre_post_delta.json` exists with `transition_label` per cell.
* `corrections/library_procedural_dsgc_morphology_generator.json` exists and `verify_corrections.py`
  PASSES.
* `aggregate_libraries.py` (with corrections applied) lists the t0092 library as the canonical
  `procedural_dsgc_morphology_generator` entry.
* `results/metrics.json` uses explicit-variant format with two variants and only registered metric
  keys; `verify_task_metrics.py` PASSES.
* `verify_task_results.py`, `verify_logs.py`, `verify_task_folder.py`, `verify_task_file.py`,
  `verify_suggestions.py` all PASS with 0 errors.

## Cross-References

* **t0024_port_de_rosenroll_2026_dsgc** — original Bed B port for reference comparisons (no
  imports in this task).
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2** — `apply_parameter_vector`,
  `setup_synapses_parametric`, `run_one_trial`, `_compute_nseg`. Used unchanged.
* **t0083_bedb_v3_extend_nsga2_gen8plus** — source of the best-cell parameter vector applied to
  every cell in the re-sweep.
* **t0090_morphology_generator_diversity_test** — source of the 60 morph spec JSONs and the
  pre-fix `verification_summary.json` for delta comparison. **Target of the correction overlay.**
* **t0092_diagnose_morphology_generator_silence** — source of the patched generator
  (`generate_fixed_morphology`) and the diagnosis the correction cites.
* Source suggestion: **S-0092-01** (full 60-morph re-sweep). Also implements **S-0092-03**
  (correction overlay) bundled per the consolidated-task preference.
