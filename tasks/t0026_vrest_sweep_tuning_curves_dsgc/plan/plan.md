---
spec_version: "2"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
date_completed: "2026-04-21"
status: "complete"
---
# Plan: V_rest sweep tuning curves for t0022 and t0024 DSGC ports

## Objective

Produce direction-tuning curves as a function of resting potential for the two most recent DSGC
compartmental-model ports (`modeldb_189347_dsgc_channel_testbed` from t0022 and
`de_rosenroll_2026_dsgc` from t0024) by sweeping V_rest across eight values from -90 mV to -20 mV in
10 mV increments, running the existing 12-angle direction protocol at each holding potential, and
exporting polar tuning curves plus per-V_rest metrics (DSI, peak firing rate, HWHM) so the
researcher can see how each model's tuning morphs with V_rest. Done means: two predictions assets
registered (one per model), 16 individual polar plots plus 2 per-model overlay polar plots plus 2
Cartesian summary plots sitting in `results/images/`, and a `results_detailed.md` that embeds the
plots and tables and answers the five key questions stated in the task description.

## Task Requirement Checklist

The operative task request is quoted verbatim below from `task.json` `name`, `short_description`,
and `task_description.md`.

```text
Name: V_rest sweep tuning curves for t0022 and t0024 DSGC ports
Short: Sweep resting potential -90 to -20 mV in 10 mV steps on the t0022
and t0024 DSGC ports; output polar tuning curves.

Scope (from task_description.md):
* V_rest values: exactly eight, -90, -80, -70, -60, -50, -40, -30, -20 mV.
* Holding strategy: set BOTH V_INIT_MV and ELEAK_MV to the sweep value.
* Model 3 (t0022): 1 trial per angle, 12 angles, 8 V_rest -> 96 trials.
* Model 4 (t0024 correlated rho=0.6): 10 trials per angle, 12 angles,
  8 V_rest -> 960 trials.
* Do not modify either library asset.
* Report data in polar coordinates.
* Deliverables: 2 predictions assets, 16 per-(model, V_rest) polar plots,
  2 overlay polar plots, results_detailed.md with embedded DSI/peak/HWHM
  tables, metrics.json with registered keys (or proposed suggestions).
* Five key questions to answer in results_detailed.md.
```

Concrete requirements (each step that satisfies it is named under `## Step by Step`):

* **REQ-1 — Eight V_rest values (exactly -90, -80, -70, -60, -50, -40, -30, -20 mV):** encoded as
  `V_REST_VALUES_MV` in `code/constants.py`; both sweep drivers iterate this list. Evidence: exactly
  8 distinct `v_rest_mv` values appear in each model's `vrest_sweep_tidy.csv`. (Steps 2, 4, 5.)
* **REQ-2 — Move `v_init` AND `eleak` together at each V_rest:** implemented by a shared helper
  `set_vrest` in `code/vrest_override.py` that sets `h.v_init = v_rest_mv` and then walks
  `h.allsec()` setting `seg.eleak_HHst` on every HHst section and `seg.e_pas` on every pas section.
  Evidence: code review + unit test that inspects `h.v_init`, `eleak_HHst`, and `e_pas` after
  calling `set_vrest(-20)` on a freshly built cell. (Steps 3, 4, 5.)
* **REQ-3 — t0022 sweep at 1 trial/angle, 96 trials total:** `run_vrest_sweep_t0022.py` loops 8
  V_rest × 12 angles × 1 trial using the copied t0022 trial runner. Evidence:
  `data/t0022/vrest_sweep_tidy.csv` has exactly 96 rows. (Step 6.)
* **REQ-4 — t0024 sweep at 10 trials/angle, 960 trials total, correlated rho=0.6:**
  `run_vrest_sweep_t0024.py` loops 8 V_rest × 12 angles × 10 trials using the copied t0024
  correlated AR(2) trial runner. Evidence: `data/t0024/vrest_sweep_tidy.csv` has exactly 960 rows.
  (Step 7.)
* **REQ-5 — Do not modify either library asset:** override lives in this task's `code/`; library
  asset files are read-only. Evidence: `git diff main -- tasks/*/assets/library/` shows no changes
  under those paths. (Steps 3, 4, 5.)
* **REQ-6 — Per-(model, V_rest) metrics: DSI, peak firing rate (Hz), null firing rate (Hz), HWHM
  (deg):** computed in `code/compute_vrest_metrics.py`, using `tuning_curve_loss` library asset for
  DSI and a local HWHM helper. Evidence: `data/<model>/vrest_metrics.csv` with columns
  `v_rest_mv, preferred_deg, dsi, peak_hz, null_hz, hwhm_deg, wall_time_s`. (Step 8.)
* **REQ-7 — 16 per-(model, V_rest) polar plots:** `code/plot_polar_tuning.py` emits
  `results/images/polar_<model>_vrest_<value>.png` for every (model, V_rest) pair. Evidence: 16 PNG
  files exist. (Step 9.)
* **REQ-8 — 2 overlay polar plots (one per model, 8 curves each):** same script emits
  `results/images/polar_overlay_<model>.png`. Evidence: both PNGs exist. (Step 9.)
* **REQ-9 — 2 Cartesian summary plots (`dsi_vs_vrest.png`, `peak_hz_vs_vrest.png`):** same script
  emits both. (Step 9.)
* **REQ-10 — Predictions assets registered (one per model):** Step 11 produces
  `assets/predictions/t0026_vrest_sweep_t0022/` and `assets/predictions/t0026_vrest_sweep_t0024/`
  with `details.json` plus the tidy CSV. (Step 11.)
* **REQ-11 — `metrics.json` registers `dsi_at_vrest_<mv>`, `peak_hz_at_vrest_<mv>`,
  `hwhm_deg_at_vrest_<mv>` for each V_rest and `efficiency_wall_time_per_trial_seconds` per model,
  OR proposes them as suggestions if not registered in `meta/metrics/`:** handled by the reporting
  step; un-registered keys are proposed in `results/suggestions.json`. (Step 10.)
* **REQ-12 — Answer the five key questions in `results_detailed.md`:** each question gets a named
  subsection in the report with numeric evidence and a plot reference. (Orchestrator `/results` step
  consumes `data/*/vrest_metrics.csv` and `results/images/*` produced by steps 8-9.)

## Approach

This is a two-model parameter sweep that reuses the existing deterministic (t0022) and correlated
AR(2) stochastic (t0024) trial runners unchanged except for a holding-potential override. The key
research finding is that both models set `h.v_init = V_INIT_MV` unconditionally inside
`apply_params` (called by every trial), and the leak reversal is exposed as the `eleak_HHst` RANGE
variable on every HHst-bearing section; t0022 additionally uses `pas` with `e_pas` on some sections.
Therefore the V_rest override must run AFTER `apply_params` and BEFORE `h.finitialize`: set
`h.v_init` to the target value, then iterate `h.allsec()` and for each section set `seg.eleak_HHst`
(on HHst sections) and `seg.e_pas` (on pas sections). Without iterating all sections the override
would miss the HOC-initialised per-section values (t0008's `dsgc_model.hoc` sets
`eleak_HHst = RGCepas` and `e_pas = RGCepas` once at build time and Python changes to module-level
`C.ELEAK_MV` do not propagate back into the already-built cell).

The wrapper is deliberately thin. All stochastic state (seeds, AR(2) cross-correlation rho,
spike-detection threshold, tstop, dt, morphology, bar velocity, 12 angles) comes from the respective
task's constants unchanged; only `V_INIT_MV` and the section-wise leak reversal move per sweep step.
Since cross-task imports of library assets ARE allowed (t0022's and t0024's `run_tuning_curve.py`
are not in `assets/library/`, but their library assets are), but code in `tasks/*/code/` is not
importable, the plan is to **copy the necessary trial-runner entry points from each dependency task
into this task's `code/` folder** (immutability rule 5 enforces the copy) and wire them into the
sweep driver. The `tuning_curve_loss` library asset is imported directly because it IS a library
asset.

**Alternative considered:** running each model's existing `run_tuning_curve.py` 8 times with
environment-variable overrides would be simpler but would (a) not satisfy the "do not modify the
library asset" rule because the library's module-level constants are imported once and cached, and
(b) would require 16 separate Python process launches with NEURON cold-start overhead each, adding
an estimated ~2 min of pure startup wall time per model. Rejected in favour of a single-process
driver that builds one cell per V_rest value.

**Task types (from `meta/task_types/`):** `experiment-run` (runs a parametric sweep over a
biophysical model) and `data-analysis` (computes tuning-curve metrics and produces plots). Both are
already in `task.json` `task_types`. Planning Guidelines for `experiment-run` emphasise
pre-registering the exact parameter grid and logging per-run wall time; both are encoded here.
Planning Guidelines for `data-analysis` emphasise naming all charts with the question they answer
and embedding every chart in `results_detailed.md`; both encoded here.

## Cost Estimation

Total cost: **$0**. No paid API calls, no remote compute, no GPU provisioning. All runs execute on
the local Windows workstation using the pre-installed NEURON + Python stack. Electricity cost from
~4-5 hours of CPU-bound NEURON simulation is not charged against the project budget
(`project/budget.json` `total_budget = $1.00`, spent so far = $0, remaining = $1.00). The $1 budget
is therefore untouched after this task.

## Step by Step

1. **Sanity-check the working tree and re-confirm research findings.** Run `git status` in the
   worktree; confirm it is clean at the start of the implementation step. Re-read
   `research/research_code.md` sections "Where the holding potential is set" and "V_rest override
   block" to confirm the planned `set_vrest` helper matches the research findings. No files written.
   Satisfies: (setup; no REQ).

2. **Write `code/constants.py`.** Create a single place for the sweep's parametric values:

   ```python
   V_REST_VALUES_MV: tuple[float, ...] = (
       -90.0, -80.0, -70.0, -60.0, -50.0, -40.0, -30.0, -20.0,
   )
   ANGLES_DEG: tuple[int, ...] = tuple(range(0, 360, 30))
   N_TRIALS_T0022: int = 1
   N_TRIALS_T0024: int = 10
   AR2_RHO_T0024: float = 0.6  # correlated condition, matches t0024 default
   ```

   Plus path constants for `data/t0022/`, `data/t0024/`, `results/images/`. Satisfies REQ-1.

3. **Write `code/vrest_override.py`.** One public function:

   ```python
   def set_vrest(h: object, v_rest_mv: float) -> None:
       """Set v_init and every section's leak reversal to v_rest_mv.

       Must be called AFTER apply_params and BEFORE h.finitialize.
       """
       h.v_init = v_rest_mv
       for sec in h.allsec():
           # HHst sections: eleak is a RANGE variable on HHst
           if h.ismembrane("HHst", sec=sec):
               for seg in sec:
                   seg.eleak_HHst = v_rest_mv
           # pas sections (t0022 only): e_pas is the standard pas reversal
           if h.ismembrane("pas", sec=sec):
               for seg in sec:
                   seg.e_pas = v_rest_mv
   ```

   Satisfies REQ-2, REQ-5.

4. **Copy and adapt t0022's trial runner into `code/trial_runner_t0022.py`.** Copy the relevant
   portions of `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` (imports,
   `run_one_trial` or equivalent, the angle loop helper) into this task's `code/` folder. Modify the
   copied function so it accepts a `v_rest_mv: float` argument and calls `set_vrest(h, v_rest_mv)`
   AFTER `apply_params(h, seed=seed)` and BEFORE `h.finitialize(...)`. Imports from
   `tasks.t0022_modify_dsgc_channel_testbed.assets.library.modeldb_189347_dsgc_channel_testbed` are
   allowed because that path is a registered library asset. Satisfies REQ-2, REQ-5.

5. **Copy and adapt t0024's trial runner into `code/trial_runner_t0024.py`.** Same pattern as step
   4, but copying from `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`. Keep
   `AR2_CROSS_CORR_RHO = 0.6` hard-wired (the correlated condition) and `N_TRIALS_PER_ANGLE` as a
   parameter. Call `set_vrest(h, v_rest_mv)` at the same position as in step 4. Library import from
   `tasks.t0024_port_de_rosenroll_2026_dsgc.assets.library.de_rosenroll_2026_dsgc` is allowed.
   Satisfies REQ-2, REQ-5.

6. **Write `code/run_vrest_sweep_t0022.py`.** Sweep driver for t0022.

   * [CRITICAL] Loops `v_rest_mv in V_REST_VALUES_MV`, then `angle_deg in ANGLES_DEG`, then
     `trial in range(N_TRIALS_T0022)`. Calls `trial_runner_t0022.run_one_trial(...)`. Accumulates
     rows with columns `(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`.
     Writes `data/t0022/vrest_sweep_tidy.csv` and `data/t0022/wall_time_by_vrest.json`.
   * **Validation gate (before committing to the full run):** run with
     `--limit-vrest -60 --limit-trials 1` (single V_rest, 1 trial) and confirm the output CSV has 12
     rows, firing_rate_hz values are all non-negative, and at least one direction's firing_rate_hz
     is within the 5-80 Hz envelope (baseline behaviour reported in t0022's results). If any row is
     NaN, negative, or every row is 0.0 Hz, halt and inspect the individual trial in the NEURON GUI
     before proceeding. Only after the gate passes, run the full sweep.

   Satisfies REQ-3.

7. **Write `code/run_vrest_sweep_t0024.py`.** Sweep driver for t0024.

   * [CRITICAL] Same structure as step 6 but using `trial_runner_t0024` with `N_TRIALS_T0024 = 10`
     and `AR2_RHO = 0.6`. Writes `data/t0024/vrest_sweep_tidy.csv` (960 rows) and
     `data/t0024/wall_time_by_vrest.json`.
   * **Validation gate:** run `--limit-vrest -60 --limit-trials 1` first (12 rows, validate as in
     step 6). Baseline for t0024 at V_rest=-60 is `DSI > 0.3` (per t0024 results); if the
     limited-run DSI is under 0.1, halt and debug. Then run the full sweep.

   Satisfies REQ-4.

8. **Write `code/compute_vrest_metrics.py`.** For each model, reads
   `data/<model>/vrest_sweep_tidy.csv`, groups by `v_rest_mv`, and computes:

   * Preferred direction (argmax firing_rate_hz averaged across trials per angle).
   * DSI using `tuning_curve_loss` library asset's DSI formula (`(pref - null) / (pref + null)` on
     trial-averaged firing rates).
   * Peak firing rate (Hz) at preferred direction.
   * Null firing rate (Hz) at preferred + 180 mod 360.
   * HWHM (degrees), computed on a linearly interpolated tuning curve in degrees.
   * Wall time per V_rest (from the sweep driver's JSON log).

   Writes `data/<model>/vrest_metrics.csv` with columns
   `(v_rest_mv, preferred_deg, dsi, peak_hz, null_hz, hwhm_deg, wall_time_s)`. Satisfies REQ-6.

9. **Write `code/plot_polar_tuning.py`.** Produces the 20 plots in `results/images/`:

   * 16 individual polar plots: `polar_<model>_vrest_<value>.png`.
   * 2 overlay polar plots: `polar_overlay_<model>.png` (8 curves each, perceptually ordered
     colormap such as `viridis`, colour legend labelling each V_rest value).
   * 2 Cartesian summary plots: `dsi_vs_vrest.png` and `peak_hz_vs_vrest.png`, each overlaying both
     models.

   Uses `matplotlib.pyplot.subplot(projection='polar')` for the polar plots. Closes every figure
   after saving to bound memory. Satisfies REQ-7, REQ-8, REQ-9.

10. **Write `code/write_metrics.py`.** Emit `results/metrics.json` only (the orchestrator's
    `/results` step is responsible for `results_detailed.md` and `results_summary.md`; this
    implementation step ends at metrics computation). Produces:

    * `results/metrics.json` keyed by `dsi_at_vrest_<mv>`, `peak_hz_at_vrest_<mv>`,
      `hwhm_deg_at_vrest_<mv>` (per model), plus `efficiency_wall_time_per_trial_seconds` (per
      model). Uses the explicit multi-variant format with variants `"t0022"` and `"t0024"`.

    Orchestrator steps (`/results`, `/suggestions`, `/reporting`) consume the tidy CSVs,
    `vrest_metrics.csv`, and `results/images/` produced earlier to produce the narrative results
    files. Satisfies REQ-11.

11. **Register the two predictions assets.** For each model, create an asset directory at
    `assets/predictions/t0026_vrest_sweep_<model_slug>/` containing:

    * `details.json` following `meta/asset_types/predictions/specification.md` — fields include
      `asset_id`, `task_id`, `model_source`, `schema`, `n_rows`, `n_v_rest_values`, `n_angles`,
      `n_trials_per_angle`, short description, categories, and date.
    * A copy (or symlink — the spec permits symlinks on POSIX) of the tidy CSV written by the
      sweep driver.
    * A short markdown description file `description.md` naming the source library asset.

    Satisfies REQ-10.

12. **Run verificators.** Run
    `uv run python -u -m arf.scripts.verificators.verify_implementation t0026_vrest_sweep_tuning_curves_dsgc`
    and
    `uv run python -u -m arf.scripts.verificators.verify_predictions_assets t0026_vrest_sweep_tuning_curves_dsgc`
    (or the generic asset verificator if a predictions-specific one is not present). Fix any
    reported errors. Satisfies cross-cutting REQ-10 evidence check.

## Remote Machines

None required. The entire sweep runs on the local Windows workstation's CPU inside the existing
`uv`-managed Python environment with NEURON already installed. No vast.ai provisioning.

## Assets Needed

Inputs consumed by this task:

* Library asset `modeldb_189347_dsgc_channel_testbed` from
  `tasks/t0022_modify_dsgc_channel_testbed/assets/library/modeldb_189347_dsgc_channel_testbed/` (HOC
  \+ mod files, Python wrapper).
* Library asset `de_rosenroll_2026_dsgc` from
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/` (HOC + mod +
  Python wrapper).
* Library asset `tuning_curve_loss` from
  `tasks/t0012_port_tuning_curve_loss_from_de_rosenroll_2026/assets/library/tuning_curve_loss/` (DSI
  formula).
* Trial-runner source code to copy (not import) from
  `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` and
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`.

No external datasets, no new paper downloads.

## Expected Assets

* **Predictions asset 1**: `assets/predictions/t0026_vrest_sweep_t0022/` — 96-row tidy CSV of
  t0022 sweep outputs with `details.json` and `description.md`. Columns:
  `(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`.
* **Predictions asset 2**: `assets/predictions/t0026_vrest_sweep_t0024/` — 960-row tidy CSV of
  t0024 sweep outputs with `details.json` and `description.md`. Same columns.

Matches `task.json` `expected_assets = {"predictions": 2}`.

## Time Estimation

* Research: ~20 min (already done in step 6 `research-code`).
* Implementation coding (steps 1-5, writing helpers, copying runners): ~1 h 15 min.
* t0022 sweep execution (96 trials): ~25 min wall time (t0022 baseline: ~15 s/trial on this
  workstation).
* t0024 sweep execution (960 trials): ~4 h 15 min wall time (t0024 baseline: ~16 s/trial for the
  correlated condition on this workstation; 960 × 16 s ≈ 4 h 16 min).
* Analysis (metrics + plots, steps 8-9): ~30 min (CPU time) + ~15 min (coding).
* Asset registration, results drafts, verificators, commits, poststeps: ~45 min.
* Total expected wall time: ~7 h 15 min from start of implementation to end of reporting step.

## Risks & Fallbacks

Pre-mortem: the most likely ways this task could fail are an override that silently doesn't
propagate to every section (producing a false-null result that the tuning curve looks the same
regardless of V_rest), a mid-sweep Python/NEURON crash wasting hours of wall time, and the t0024
correlated-AR(2) driver exhibiting numerical blow-ups at extreme V_rest values (-20 mV and -90 mV
are outside the regime it was validated in).

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| V_rest override misses some sections (HHst or pas) because it ran before `apply_params` | Medium | Blocking (produces garbage) | Step 3 writes `set_vrest` with a positional-argument pattern; step 4/5 call it strictly AFTER `apply_params` and BEFORE `h.finitialize`; step 6/7 validation gate runs a 1-V_rest / 1-trial smoke test first and verifies that firing rate responds to V_rest |
| t0024 sweep crashes halfway (unstable at extreme V_rest) | Medium | Hours of wasted wall time | Sweep driver writes one CSV per (V_rest) as it goes, then concatenates at the end, so partial progress is never lost. Script is re-runnable with `--skip-vrest <csv already on disk>` |
| Depolarization block or hyperpolarization silence at V_rest extremes produces all-zero firing | High for V=-20 and V=-90 | Cosmetic (not a bug) | Expected and documented as a key question answer (Q4). Plotting code handles all-zero rows gracefully (polar plot shrinks radius); metric computation returns `NaN` for DSI when `peak + null == 0` and the reporting step notes this explicitly |
| Wall-time overrun past estimated 4 h 15 min for t0024 | Low | Schedule slip, not a blocker | No hard deadline; worst case overnight run |
| Cross-task import rule violated (e.g. accidentally importing from `tasks.t0022_*.code.*`) | Low | Verificator failure | Step 4 and 5 use `# imports only from assets/library/` comments as review gates; pre-commit mypy + ruff run on every commit |
| Library asset accidentally modified (immutability rule 5) | Low | Pre-merge verificator failure | No edit to any file under `tasks/*/assets/library/`. All adaptation lives in this task's `code/`. Enforced by pre-merge verificator that diffs library paths |

## Verification Criteria

At least three concrete checks, each with an exact command and expected outcome.

* **File existence.** All required output files exist:
  ```bash
  uv run python -c "from pathlib import Path; import sys; \
    base = Path('tasks/t0026_vrest_sweep_tuning_curves_dsgc'); \
    req = [base/'data/t0022/vrest_sweep_tidy.csv', \
           base/'data/t0024/vrest_sweep_tidy.csv', \
           base/'data/t0022/vrest_metrics.csv', \
           base/'data/t0024/vrest_metrics.csv', \
           base/'results/metrics.json']; \
    req += [base/f'results/images/polar_overlay_{m}.png' for m in ['t0022','t0024']]; \
    req += [base/'results/images/dsi_vs_vrest.png', \
            base/'results/images/peak_hz_vs_vrest.png']; \
    missing = [p for p in req if not p.exists()]; \
    print('MISSING:', missing); sys.exit(0 if not missing else 1)"
  ```
  Expected exit 0 and `MISSING: []`. Directly checks REQ-3, REQ-4, REQ-6, REQ-7, REQ-8, REQ-9,
  REQ-11.
* **Row-count integrity on tidy CSVs.** Exactly 96 rows for t0022, 960 for t0024:
  ```bash
  uv run python -c "import pandas as pd; \
    a = pd.read_csv('tasks/t0026_vrest_sweep_tuning_curves_dsgc/data/t0022/vrest_sweep_tidy.csv'); \
    b = pd.read_csv('tasks/t0026_vrest_sweep_tuning_curves_dsgc/data/t0024/vrest_sweep_tidy.csv'); \
    assert len(a) == 96, len(a); assert len(b) == 960, len(b); \
    assert sorted(a['v_rest_mv'].unique().tolist()) == [-90.0,-80.0,-70.0,-60.0,-50.0,-40.0,-30.0,-20.0]; \
    assert sorted(b['v_rest_mv'].unique().tolist()) == [-90.0,-80.0,-70.0,-60.0,-50.0,-40.0,-30.0,-20.0]; \
    print('OK')"
  ```
  Expected output `OK`. Directly checks REQ-1, REQ-3, REQ-4.
* **Individual polar plot count.** 16 per-(model, V_rest) polar plots exist:
  ```bash
  uv run python -c "from pathlib import Path; \
    root = Path('tasks/t0026_vrest_sweep_tuning_curves_dsgc/results/images'); \
    n = len(list(root.glob('polar_t00*_vrest_*.png'))); \
    assert n == 16, n; print('OK', n)"
  ```
  Expected output `OK 16`. Directly checks REQ-7.
* **Library immutability.** No file under `tasks/*/assets/library/` has been modified on this task
  branch:
  ```bash
  git diff main --name-only -- 'tasks/*/assets/library/**' | tee /tmp/libdiff.txt
  test ! -s /tmp/libdiff.txt && echo "OK: no library edits"
  ```
  Expected output `OK: no library edits`. Directly checks REQ-5.
* **Override unit test.** Run a NEURON-in-the-loop test that builds one cell, calls
  `set_vrest(h, -20.0)`, and confirms every section's `eleak_HHst` (and `e_pas` where present) now
  equals -20.0:
  ```bash
  uv run python -u -m tasks.t0026_vrest_sweep_tuning_curves_dsgc.code.vrest_override_smoke
  ```
  Expected output `OK`. Directly checks REQ-2.
* **Predictions asset verificator.**
  ```bash
  uv run python -u -m arf.scripts.verificators.verify_predictions_assets \
    t0026_vrest_sweep_tuning_curves_dsgc
  ```
  Expected exit 0 with no errors. Directly checks REQ-10.
