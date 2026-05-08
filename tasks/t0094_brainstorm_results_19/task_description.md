# Brainstorm Results Session 19

Nineteenth strategic brainstorm, run on 2026-05-08 immediately after t0093
(`resweep_and_t0090_correction`) merged to main. The full 60-cell re-sweep under the t0092 patched
generator landed at 60/60 STABLE-firing (vs 0/60 pre-fix), 56/60 cells with PD-rate>0, mean DSI 0.32
(different) / 0.35 (similar), 21/60 cells with DSI > 0.5, and 0 regressions. The `replace`
correction overlay `C-0093-01` is in place, redirecting the canonical procedural DSGC morphology
generator to t0092's `generate_fixed_morphology`.

The researcher's directive for this session was simple: **launch the morphology-extended NSGA-II
optimisation now**. The session's only outstanding work was to make t0091 actually launchable —
its dependencies and import paths still pointed at t0090's unpatched generator.

## Decisions

1. **Update t0091 in place** (allowed because it is `not_started`):

   * Add `t0092_diagnose_morphology_generator_silence` and `t0093_resweep_and_t0090_correction` to
     the dependencies list.
   * Replace the import-path reference in `task_description.md` Phase B per-cell evaluation from
     "t0090 generator" to
     `tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix.generate_fixed_morphology`.
   * Update the Bed-B-like anchor (Phase A anchor #1) source from "t0090 Phase F validated point" to
     "t0093 patched-generator Bed-B reproducibility (43.6 Hz PD-rate post-fix)".
   * Add t0092, t0093, and t0094 to Cross-References.
   * Refresh the generator-instability risk to reflect t0093's 60/60 STABLE evidence.
   * Refresh the short_description to reference the patched generator.

2. **Reject S-0092-03** (issue a correction overlay against t0090's generator). t0093 has already
   committed the `replace` correction overlay `C-0093-01` and `verify_corrections.py` PASSES. The
   suggestion is fully covered.

3. **Reject S-0090-04** (tighten t0091 LHS bounds using the 9 STABLE cells from the t0090 diversity
   sweep). t0093's patched-generator re-sweep made 60/60 cells STABLE-firing — the original "9
   STABLE" pool was an artefact of the soma-pt3d collapse bug. The premise that "51/60 morphologies
   failed NAN_VOLTAGE" no longer holds, so the tightening rationale is invalidated.

4. **Keep S-0090-02 active** (NaP-knockout sweep at scale on local 64-core EPYC). The fix unblocks
   it; the sweep is partially superseded by t0091 but still useful as an isolated mechanism test.

5. **Keep S-0090-03 active** (G.2 NMDA units calibration). Researcher chose to keep it as a
   post-t0091 task instead of folding it into t0091 as a Phase A.5 prerequisite, on the grounds that
   t0091 launch should stay simple and re-scoring after calibration is acceptable.

6. **Keep S-0086-01, S-0070-01, S-0067-01, S-0074-01/02/03, S-0076-04, S-0093-01 active.** S-0093-01
   is operationally fulfilled by this brainstorm (the t0091 update is exactly what it asks for) but
   kept active as a status marker until the next brainstorm session sweeps it.

7. **Cost-watchdog cap for t0091 stays at $4.00**, matching the existing plan; gives NSGA-II room to
   hit 8 generations and leaves $0.45 buffer against the $4.45 budget cap.

## Why these decisions

* The morphology pivot is the project's committed strategic direction (set in brainstorm 18); the
  generator pipeline is now fully validated at scale; budget remaining ($4.45) just covers t0091's
  $3.00–3.50 plan estimate. This is the right window to launch.
* S-0092-03 and S-0090-04 are both falsified by the t0093 outcome — keeping them active wastes
  reviewer attention.
* Folding S-0090-03 NMDA calibration into t0091 was tempting (it's local-only, $0 incremental) but
  adds wall-clock and complexity ahead of an already-tight remote run. Researcher preferred to keep
  the launch surface minimal.

## Cross-references

* **t0089_brainstorm_results_18** — committed the morphology-extension pivot; commissioned t0090
  and t0091.
* **t0090_morphology_generator_diversity_test** — generator with the soma-pt3d collapse bug.
* **t0092_diagnose_morphology_generator_silence** — root cause + `generate_fixed_morphology` shim.
* **t0093_resweep_and_t0090_correction** — patched-generator re-sweep + correction overlay.
* **t0091_morphology_extended_nsga2_v1** — updated by this session; ready for execute-task.
