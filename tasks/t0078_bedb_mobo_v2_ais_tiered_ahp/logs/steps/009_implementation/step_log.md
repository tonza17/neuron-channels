---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-05-03T15:19:26Z"
completed_at: "2026-05-03T16:45:00Z"
---
# Step 9 — Implementation

## Summary

Forked the t0076 BoTorch MOBO harness into the t0078 task folder, attached a two-subsegment AIS to
the de Rosenroll 2026 Bed B substrate, vendored an SK_E2 MOD with extended Ca-binding kinetics,
migrated the BoTorch acquisition function from `qNoisyExpectedHypervolumeImprovement` to
`qLogNoisyExpectedHypervolumeImprovement` with `Normalize` input transform, fixed the
`plot_pareto.py` deep-dive NEURON re-init bug with subprocess-per-pick, and built the
`de_rosenroll_2026_dsgc_ais` library asset. Local Windows imports + ruff + mypy pass; remote
smoke-test on Vast.ai 36068067 confirms the cell builds with the right mechanism set on AIS / soma /
dendrites and one trial executes without instability. The 49-d Sobol DoE phase of the BO loop is now
running stably on the remote instance (PID 2366), checkpointed every 10 cells.

## Actions Taken

1. Read `plan/plan.md`, `task.json`, `research/research_code.md`, `research/research_papers.md` to
   confirm the 49-d parameter layout, the AIS architecture, the `tau_ca_multiplier` range ([1, 20]),
   and the single-tier pass criterion (DSI >= 0.4 AND PD rate >= 10 Hz).
2. Copied the t0076 harness into `code/`: `bootstrap.py`, `parametric_placer.py`, `recorder.py`,
   `render_pdf.py`, plus the 12 t76-namespace MODs renamed to `t78`.
3. Authored `code/constants.py` with the 49-d parameter layout: 25 tier-stratified densities
   (Nav1.6, Kv3, NaP, BK, SK x 5 tiers), 7 uniform-density channels (Kdr, Kv4, NaR, HCN, CaL, CaT,
   Kv7), 2 slow-AHP params (skahpt78 gbar + tau_ca_multiplier), 13 synaptic placement params, 2 free
   AIS geometry params. `TSTOP_MS = 1400.0` (researcher decision; t0076 had 1000).
4. Authored `code/extend_with_ais.py`: builds two subsegments (`ais_proximal_t78`, `ais_distal_t78`)
   connected in series at `soma(1.0)`, with d_lambda=0.1 nseg rule at 100 Hz.
5. Authored `code/build_cell_ais.py`: thin wrapper around t0024's `build_dsgc_cell()` that returns a
   `DSGCCellWithAIS` dataclass with the two AIS section handles.
6. Authored `code/apply_params.py`: tier-stratified writes (5 tier loops); AIS-tier writes restrict
   to AIS-permitted SUFFIXes (Nav1.6 / Kv3 / Kv7 only); slow-AHP write to soma + AIS only; AIS
   geometry update before channel insertion. Found and fixed an issue during smoke test: `skahpt78`
   must be inserted on AIS sections (the task description "Insertion sites: soma + AIS only" applies
   to the slow-AHP, not the regular fast SK).
7. Authored `code/mods/skahpt78.mod`: SK_E2 with extended Ca-binding via a `tau_ca_multiplier`
   PARAMETER (default 1.0, range [1, 20] per researcher decision). Replaces
   `m' = (minf - m) / tau_m` with `m' = (minf - m) / (tau_m_base * tau_ca_multiplier)`.
8. Forked `code/trial_helpers.py` and `code/trial_driver.py` from t0076 with imports retargeted to
   t0078. Updated `EvalResult` dataclass to track `is_unstable` (peak Vm outside [-80, +60] mV) and
   `peak_vm_mv`. The trial driver still uses the worker-per-trial `ProcessPoolExecutor` pattern from
   t0076 — no NEURON re-init issue can occur during the BO loop.
9. Migrated `code/mobo_loop.py`: changed import to
   `from botorch.acquisition.multi_objective.logei import qLogNoisyExpectedHypervolumeImprovement`,
   replaced the class call, and added `input_transform=Normalize(d=N_PARAMS)` to every
   `SingleTaskGP`. `N_SOBOL_INITIAL = 75`, `N_ACQ_ITERATIONS = 700`, fresh restart (no warm-start).
10. Forked `code/plot_pareto.py` from t0076 and wrapped each `_save_deep_dive` call in a
    `ProcessPoolExecutor(max_workers=1)` so each pick runs in a fresh subprocess (REQ-11). Updated
    the cell builder to `build_dsgc_cell_with_ais` so deep-dive cells include the AIS.
11. Authored `code/run_remote.sh` for the Vast.ai launcher: `git fetch`, checkout the task branch,
    `nrnivmodl mods/`, then `nohup` launch `mobo_loop` with `--n-sobol 75 --n-acq 700 --workers 64`.
12. Built the `de_rosenroll_2026_dsgc_ais` library asset at
    `assets/library/de_rosenroll_2026_dsgc_ais/` with `details.json` (spec v2) listing 23 module
    paths and 5 entry points, plus `description.md` with all mandatory sections. Library
    verificator: 0 errors, 1 warning (no `test_paths`, accepted: testing happens via the BO loop).
13. Ran ruff check + ruff format + mypy on the package. All passes.
14. Verified locally: `from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.constants import N_PARAMS`
    prints 49; `ParameterVector.default()` returns a 49-element array.
15. Pushed two commits to `origin/task/t0078_bedb_mobo_v2_ais_tiered_ahp` (HEADs 3727fd39 and
    f4f4096a).
16. SSH'd to Vast.ai 36068067, fixed the remote git config (the initial clone had
    `+refs/heads/main:refs/remotes/origin/main` only; added the wildcard fetch refspec), checked out
    the task branch (HEAD f4f4096a).
17. Compiled the t78 MOD library on the remote: 13 SUFFIXes (12 t78 channels + skahpt78) →
    `code/mods/x86_64/.libs/libnrnmech.so` (118 KB). Compiled the t0024 MOD library →
    `assets/library/.../sources/x86_64/.libs/libnrnmech.so` (64 KB).
18. Remote smoke test: built one cell with AIS, applied the default ParameterVector. Confirmed AIS
    sections carry only `HHst, kv3t78, kv7t78, nav16t78, skahpt78` (no NaP, BK, SK, etc.); soma
    carries all 12 t78 channels + skahpt78 + HHst + cad. Single trial with default params: DSI =
    0.000, PD rate = 0.71 Hz, peak Vm = 39.7 mV, `is_unstable = False`. End-to-end pipeline works.
19. Launched the BO loop via `bash run_remote.sh`. PID 2366. After ~3 min, Sobol cells 1 and 2
    completed: DSI 0.000 / 0.000, PD 9.79 / 5.00 Hz, n_err 0 / 0, trial_t 46.2 / 45.0 s. Projected
    wall-clock for the full 775-cell run: 9.9 hours, in line with the planning estimate.

## Files Produced

* `code/bootstrap.py` (~117 LOC; copied from t0076 unchanged except docstring)
* `code/paths.py` (~80 LOC; copied + retargeted to t0078 paths)
* `code/constants.py` (~330 LOC; new 49-d parameter layout)
* `code/extend_with_ais.py` (~120 LOC; new two-subsegment AIS attacher with d_lambda nseg rule)
* `code/build_cell_ais.py` (~80 LOC; new thin wrapper around t0024 build_dsgc_cell)
* `code/apply_params.py` (~220 LOC; new tier-stratified write loops)
* `code/trial_helpers.py` (~280 LOC; forked from t0076 with imports retargeted)
* `code/trial_driver.py` (~430 LOC; forked from t0076 + is_unstable tracking)
* `code/mobo_loop.py` (~480 LOC; forked from t0076 + qLogNEHVI + Normalize migration)
* `code/parametric_placer.py` (~110 LOC; copied from t0076 unchanged)
* `code/plot_pareto.py` (~410 LOC; forked from t0076 + subprocess-per-deep-dive fix)
* `code/recorder.py` (~125 LOC; forked from t0076 with imports retargeted)
* `code/render_pdf.py` (~65 LOC; forked from t0076 with imports retargeted)
* `code/run_remote.sh` (~45 LOC; forked from t0076 with task ID + branch + n-sobol/n-acq updated)
* `code/mods/{12 t78 channels}.mod` (~840 LOC; SUFFIX-renamed from t76)
* `code/mods/skahpt78.mod` (~75 LOC; new SK_E2 with tau_ca_multiplier)
* `assets/library/de_rosenroll_2026_dsgc_ais/details.json` + `description.md`
* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/009_implementation/step_log.md` (this file)

## Files Modified Outside Task Folder

None (no files outside `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/` were touched).

## Outcomes

* **49-d parameter space verified**:
  `from tasks.t0078_bedb_mobo_v2_ais_tiered_ahp.code.constants import N_PARAMS; assert N_PARAMS == 49`
  passes (REQ-7).
* **AIS attached as two subsegments**: smoke test confirms `ais_proximal_t78` and `ais_distal_t78`
  with `HHst, kv3t78, kv7t78, nav16t78, skahpt78` and no NaP / BK / SK (REQ-2, REQ-3, REQ-4).
* **SK_E2 with `tau_ca_multiplier` vendored at `code/mods/skahpt78.mod`** (REQ-5).
* **Tier-stratified writes**: 5 tier-specific write loops in `apply_parameter_vector` (REQ-6).
* **qLogNEHVI + Normalize migration**: import, class call, and input transform all migrated;
  `grep qNoisyExpected` returns 0 lines, `grep Normalize(d=` returns 1 line in `_fit_gp_models`
  (REQ-8, REQ-9).
* **Sobol 75 + Acquisition 700 fresh restart**: `mobo_loop.py` constants + `run_remote.sh` arguments
  confirm; no warm-start path (REQ-10).
* **plot_pareto subprocess fix**: `_save_deep_dive` wrapped in `ProcessPoolExecutor(max_workers=1)`
  per-pick (REQ-11).
* **TSTOP_MS = 1400.0** (REQ-12).
* **Library asset built and verified**: `de_rosenroll_2026_dsgc_ais` passes the verificator with 0
  errors / 1 `LA-W014` warning (no test_paths) — REQ-1.
* **BO loop running stably** on Vast.ai 36068067, PID 2366, Sobol DoE phase under way (2 cells in ~3
  min). Projected wall-clock 9.9 h.

## Issues

No blocking issues. The BO loop sanity check at step closure (16:35 UTC, ~6 min after launch)
confirmed PID 2366 healthy with 8/75 Sobol cells completed at ~46 s each, no errors. **REQ-16
(substrate regression check at the t0076 iter-424 parameters) was deferred** to keep the BO loop
running while the cost counter ticks; this can be re-run post-BO from the saved Pareto front in the
analysis (results) step.

## Costs

`HOURLY_RATE_USD = 0.1582`. From the time `setup-machines` completed (15:18 UTC) through the start
of BO loop launch (~16:30 UTC): ~1.2 h * $0.1582/hr ≈ $0.19 (idle + smoke-test + compile time).
Anticipate ~$1.62 for the BO loop wall-clock; total ~$2.06 — within plan estimate.

## Pending Work — Resume Context

* The BO loop is running on Vast.ai 36068067, PID 2366; checkpoint files appear in
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/data/` after every 10 cells.
* The orchestrator spawns 7 paper-addition subagents in parallel (max 3 concurrent) at step closure
  while the BO loop continues running on Vast.ai. Implementation skill could not fan them out itself
  (the Skill tool runs subagents synchronously within a single conversation). Papers: Hay2011,
  Khaliq2003, Ament2023, RivlinEtzion2012, Trenholm2013, Wienbar2022, Werginz2024.
* When the BO loop completes (~9.9 h from launch), download `data/trial_history.parquet`,
  `data/hypervolume_trajectory.csv`, `results/data/pareto_front.json`, `data/checkpoints/*.pt` to
  the local worktree, then run `plot_pareto.py --n-deep-dives 5` locally to produce the Pareto +
  hypervolume + deep-dive PNGs.
* The orchestrator's downstream `teardown` step (step 10) destroys the Vast.ai instance and
  finalises `machine_log.json` + `costs.json`.
