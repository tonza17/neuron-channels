---
spec_version: "1"
task_id: "t0039_distal_dendrite_diameter_sweep_t0022_gaba4"
---
# Plan: 7-Diameter Sweep on t0022 at GABA=4 nS

## Objective

Rerun t0030's 7-diameter sweep (0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0 × baseline distal diameter) on
the t0022 testbed with `GABA_CONDUCTANCE_NULL_NS = 4.0 nS` — the operational sweet spot discovered
by t0037 — to measure the DSI-vs-diameter slope and classify the mechanism (Schachter2010 active
amplification vs passive cable filtering vs flat).

## Approach

Merge t0030's diameter override (mutates `seg.diam` on distal sections at each trial) with t0037's
runtime GABA patch (monkey-patches `tasks.t0022.constants.GABA_CONDUCTANCE_NULL_NS` then lazily
re-reads it in the trial runner). Run all 840 trials in a single process locally. Use t0030's
analysis pipeline byte-identical so the slope fit is directly comparable across the two GABA regimes
(12 nS pinned vs 4 nS unpinned).

## Cost Estimation

$0.00. No API calls, no remote compute, no paid services.

## Step by Step

1. Copy t0030's code as base; copy t0037's `gaba_override.py`; bulk-rename module paths.
2. Edit `trial_runner_diameter.py` to apply `set_null_gaba_ns(GABA_NULL_NS_VALUE=4.0)` then
   lazy-re-read the patched value before computing `gaba_null_pref_ratio`.
3. Add `set_null_gaba_ns(4.0)` belt-and-braces call at the top of `run_sweep.main()`.
4. Preflight 3 × 3 × 2 = 18 trials; confirm firing rates are DSGC-like (peak 10-20 Hz, null below
   peak) and GABA override is logged at every trial.
5. Full sweep: 7 × 12 × 10 = 840 trials. Estimated ~40 min.
6. Run `analyse_sweep.py` → per-diameter metrics CSV + metrics.json.
7. Run `classify_slope.py` → slope fit + mechanism classification.
8. Run `plot_sweep.py` → 4 charts (DSI vs diameter, vector-sum DSI, peak Hz, polar overlay).
9. Write results_summary.md, results_detailed.md, compare_literature.md, suggestions.json.

## Remote Machines

None. Local Windows workstation only.

## Assets Needed

* t0022 testbed (dependency task, completed).
* t0030 code (for copying).
* t0037 gaba_override (for copying).
* Bundled nrnmech.dll from `t0022/build/modeldb_189347/` — copied from the t0030 worktree into
  this worktree to avoid rebuilding MOD files.

## Expected Assets

None beyond CSV / JSON / PNG output in `results/`. Task type: `experiment-run`.

## Time Estimation

* Code merge: ~20 min.
* Preflight: ~2 min.
* Full sweep: ~40 min.
* Analysis + plots: ~1 min.
* Writeups: ~30 min.
* Verificators + PR + merge: ~10 min.
* Total: ~100 min.

## Risks & Fallbacks

* **Risk**: Diameter override and GABA patch interact in an unexpected way. **Mitigation**:
  preflight with 18 trials; compare firing rates against t0037's baseline-diameter values at 4 nS
  (peak=15, null=6). If they differ substantially, diagnose.
* **Risk**: Long sweep hits a silent pre-commit-hook conflict while writing CSV. **Mitigation**:
  exclude results/data/ from git adds while the sweep is running; commit data only after sweep
  completion.
* **Fallback**: If slope is flat (|slope| < MIN_SLOPE_MAGNITUDE = 0.05) and DSI range is narrow,
  report `mechanism_label = flat` and note the task's discriminator value is limited.

## Verification Criteria

1. 840 trials complete (841-line tidy CSV).
2. 7 per-diameter tuning curve CSVs written.
3. `analyse_sweep.py`, `classify_slope.py`, `plot_sweep.py` all exit 0.
4. `metrics.json` has `direction_selectivity_index` values for all 7 multipliers.
5. `slope_classification.json` records a mechanism label with numeric slope and p-value.
6. `compare_literature.md` passes `verify_compare_literature`.
7. `results/suggestions.json` passes `verify_suggestions`.
8. All standard verificators PASS with zero errors.
