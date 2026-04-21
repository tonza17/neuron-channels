---
spec_version: "1"
task_id: "t0026_vrest_sweep_tuning_curves_dsgc"
research_stage: "code"
tasks_reviewed: 8
tasks_cited: 7
libraries_found: 6
libraries_relevant: 4
date_completed: "2026-04-21"
status: "complete"
---
# Research Code: V_rest Sweep Tuning Curves (DSGC)

## Task Objective

Sweep the resting potential of the two most recent DSGC compartmental-model ports (t0022 dendritic,
t0024 de Rosenroll) across eight values from -90 mV to -20 mV in 10 mV steps, run the canonical
12-angle direction protocol at each step, and export polar tuning curves. The purpose of this
research is to locate the existing trial-runner code, identify the holding-potential handles
(`v_init`, `eleak_HHst`, `e_pas`) we must override, and list the reusable scoring/plotting utilities
so the implementation stage can focus on the V_rest wrapper rather than reinventing any of these.

## Library Landscape

The project registers six libraries under `assets/library/`. Four are directly relevant here:

* **`modeldb_189347_dsgc`** from [t0008] — the canonical HOC/NMODL DSGC model (Poleg-Polsky &
  Sivyer 2017). Imported indirectly by the two compartmental-model ports. Contains `dsgc_model.hoc`,
  `main.hoc`, and `HHst.mod` with the `eleak_HHst` RANGE variable we need to drive. **Relevant: must
  import via library** (its HOC is the backing model for t0022).
* **`modeldb_189347_dsgc_dendritic`** from [t0022] — metadata-only library that documents the
  dendritic E-I modification of the t0008 model. The executable code lives in t0022's `code/` (not
  in the library tree). **Relevant: copy the trial orchestration from t0022's `code/` into t0026**
  (cross-task code cannot be imported).
* **`de_rosenroll_2026_dsgc`** from [t0024] — the de Rosenroll 2026 port (AR(2)-correlated
  stochastic release). Ships its own HOC/NMODL sources under the library tree. **Relevant: import
  via library** (the mechanisms are compiled into this library) but the Python orchestration must be
  copied from t0024's `code/`.
* **`tuning_curve_loss`** from [t0012] — tuning-curve scoring / DSI / HWHM / reliability /
  smoothing library. **Relevant: import via library** for the analysis step (DSI and HWHM are
  reported per V_rest).

The remaining two libraries are not relevant: `tuning_curve_viz` from [t0011] is a matplotlib
visualization helper designed for Cartesian tuning-curve plots, whereas this task requires polar
plots which are simpler to render directly; `modeldb_189347_dsgc_gabamod` from [t0020] is a
GABA-kinetics variant that neither t0022 nor t0024 depend on.

No corrections overlays apply to these library records.

## Key Findings

### Where the holding potential is set in each model

Both models set `h.v_init` and then call `h.finitialize(V_INIT_MV)` in their per-trial runners. For
a true V_rest shift we must drive three quantities together: `h.v_init`, `eleak_HHst` on every
section that inserts `HHst`, and `e_pas` on the sections that additionally insert `pas`.

* [t0022]
  `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:_run_one_trial_dendritic` calls
  `apply_params(h, seed=trial_seed)` (which sets `h.v_init = V_INIT_MV` = -65.0 mV), then
  `h("update()")`, then `h("placeBIP()")`, then records soma voltage and finally
  `h.finitialize(V_INIT_MV)` → `h.continuerun(TSTOP_MS)`. The V_rest override must land **after**
  `apply_params` and **before** `h.finitialize`, because `apply_params` re-writes `h.v_init` every
  call.
* [t0008] `tasks/t0008_port_modeldb_189347/code/build_cell.py:apply_params` at line 280-316 sets
  `h.v_init = V_INIT_MV = -65.0`. The leak reversal is set in the backing HOC file
  `assets/library/modeldb_189347_dsgc/sources/dsgc_model.hoc` at lines 151 (`RGCepas = -60`), 291
  (`eleak_HHst = RGCepas`), and 301 (`e_pas = RGCepas`). `dsgc_model.hoc` is executed once at cell
  build time, so subsequent V_rest overrides in Python must iterate sections and set the RANGE
  variables directly.
* [t0024] `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` at lines 193-246 inserts
  `HHst` and `cad` (not `pas`) on soma and every dendrite class and sets
  `sec.eleak_HHst = C.ELEAK_MV` (= -60.0 mV). The trial runner at
  `code/run_tuning_curve.py:run_single_trial` sets `h.v_init = C.V_INIT_MV` (= -60.0 mV) at line 307
  then `h.finitialize(C.V_INIT_MV)` at line 309.
* The `HHst.mod` RANGE variable is named `eleak` inside the MOD file, `eleak_HHst` from the outside
  (NEURON's mechanism-suffix convention). Both models use this same RANGE handle.

### Canonical direction protocol

Both trial runners use the 12-angle sweep `tuple(range(0, 360, 30))` as the canonical angle set
(`C.ANGLES_12ANG_DEG` in t0024; identical literal list in t0022). Both use `TSTOP_MS = 1000.0` and
AP detection via upward crossings of `AP_THRESHOLD_MV = -10.0` mV on the somatic voltage. Trial
spike count divided by 1 s gives firing rate in Hz; because tstop = 1 s exactly, spike count and
rate are numerically identical.

### Trial stochasticity model

* [t0022] is **deterministic per dendrite**: once `trial_seed` is passed into
  `apply_params → h("seed2=…")`, the per-dendrite E-I onset schedule is fully determined. This
  is why 1 trial per angle is sufficient — additional trials would repeat the same schedule.
* [t0024] is **AR(2)-correlated stochastic release**: per-synapse release-rate noise is generated in
  Python from a NumPy RNG seeded per-trial at
  `code/run_tuning_curve.py:272: rng = np.random.default_rng(seed + 1_000_003)`. Each trial is
  genuinely different. At the correlated condition (`rho = 0.6`, default for this task), 10 trials
  is the upstream convention [t0024] for retaining trial-to-trial variance without blowing up wall
  time.

### Polar plotting

No existing library produces polar plots. The project's only tuning-curve visualization library is
[t0011] `tuning_curve_viz`, which plots Cartesian direction-vs-rate curves with SEM shading. For
this task, polar plots are simpler to write directly with
`matplotlib.pyplot.subplot(projection='polar')`. Reusing [t0011] would require a parallel Cartesian
API that is not needed for the deliverables.

### Tidy CSV schema

* [t0004] established the canonical tuning-curve CSV schema:
  `(angle_deg, trial_seed, firing_rate_hz)`.
* [t0022] and [t0024] both emit this schema from their main drivers (`TUNING_CURVE_DENDRITIC_CSV`
  and `dsgc_de_rosenroll_tuning.csv` respectively). For this task we extend to
  `(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)` — two extra columns
  (`v_rest_mv`, `peak_mv`) so one CSV per model carries all eight V_rest sweeps.

### Wall-time scaling

[t0022] reports ~12 s per trial × 12 angles = ~2.4 min per angle-sweep at 1 trial/angle, and so a
96-trial V_rest sweep is ~20-25 min. [t0024] reports ~4 h 15 min for 800 trials (correlated
condition), which is ~19 s per trial; a 960-trial sweep is ~5 h on this workstation. These numbers
are consistent with the task-description budget and confirm that local-only execution is feasible
(no remote compute).

## Reusable Code and Assets

### Direct library imports (no copying)

* **`tuning_curve_loss` library from [t0012]** — **import via library**. Import path:
  `from assets.library.tuning_curve_loss.<module> import …` (the exact import path is documented
  in the library's `description.md`; the aggregator view is not available on this branch). Exposes
  `compute_dsi`, `compute_hwhm`, smoothing helpers. We use `compute_dsi` and `compute_hwhm` once per
  V_rest to fill `metrics.json`. Function signatures (from t0012 plan):
  `compute_dsi(rates_per_angle: dict[float, list[float]]) -> float`,
  `compute_hwhm(rates_per_angle: dict[float, list[float]]) -> float`. No adaptation needed.
* **`modeldb_189347_dsgc` library from [t0008]** — **import via library**. Required for t0022
  sweep — the t0022 Python code loads this library's HOC at build time. No changes required; it
  continues to work exactly as [t0022] uses it.
* **`de_rosenroll_2026_dsgc` library from [t0024]** — **import via library**. Required for t0024
  sweep — the t0024 Python code loads this library's compiled NMODL (`run_nrnivmodl.cmd`) at
  startup. No changes required.

### Code to copy into `tasks/t0026_vrest_sweep_tuning_curves_dsgc/code/`

* **t0022 trial orchestration** — **copy into task**. Copy the body of
  `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py:_run_one_trial_dendritic`
  (approximately 80 lines) and rename to `run_one_trial_t0022_vrest`, parameterising on `v_rest_mv`
  and inserting between `apply_params(h, seed=trial_seed)` and `h.finitialize(...)`:

  ```python
  h.v_init = v_rest_mv
  for sec in h.allsec():
      if h.ismembrane("HHst", sec=sec):
          for seg in sec:
              seg.eleak_HHst = v_rest_mv
      if h.ismembrane("pas", sec=sec):
          for seg in sec:
              seg.e_pas = v_rest_mv
  ```

  Then call `h.finitialize(v_rest_mv)`. This is the minimum override surface — the constraints
  analysis in the task description required "move both `v_init` and `eleak`", and `e_pas` is
  included because the backing HOC explicitly sets `e_pas = RGCepas` on passive sections at
  `dsgc_model.hoc:301`. Approx 100 lines once the sweep loop is wrapped around it.

* **t0022 build-cell call** — **copy into task**. Copy the prelude from `_main_full_sweep` in
  `tasks/t0022_modify_dsgc_channel_testbed/code/run_tuning_curve.py` that constructs the cell,
  captures `baseline_coords` and `baseline_gaba_mod`, and sets up the HOC environment. ~60 lines.

* **t0024 trial runner** — **copy into task**. Copy
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:run_single_trial` (approx 120
  lines), inject the same V_rest override block (minus the `e_pas` branch — the t0024 model
  inserts `HHst` + `cad` only, no `pas`), then loop over the 8 V_rest values × 12 angles × 10
  trials. Rename to `run_one_trial_t0024_vrest`.

* **Canonical V_rest values and task-local constants** — **new code** in `code/constants.py`:
  `V_REST_MV_VALUES: tuple[float, ...] = (-90.0, -80.0, -70.0, -60.0, -50.0, -40.0, -30.0, -20.0)`,
  `N_TRIALS_T0022 = 1`, `N_TRIALS_T0024 = 10`, `ANGLES_12ANG_DEG = tuple(range(0, 360, 30))`,
  `AP_THRESHOLD_MV = -10.0`, `TSTOP_MS = 1000.0`.

* **Polar-plot helper** — **new code** in `code/plot_polar_tuning.py`. Minimal matplotlib-polar
  implementation (~40 lines) that takes a per-angle rate dict and writes one PNG. Loops to produce
  16 per-(model, V_rest) plots plus 2 overlay plots (one per model, superimposing all 8 V_rest
  curves). No adaptation from existing code.

### Data-schema constants

* Column names reused from [t0004] / [t0022] / [t0024]: `angle_deg`, `trial_seed`, `firing_rate_hz`.
  New columns for this task: `v_rest_mv`, `trial`, `direction_deg`, `spike_count`, `peak_mv`. Put
  these in `code/constants.py` as string constants, not literals.

## Lessons Learned

* **`apply_params` always rewrites `h.v_init`** [t0008], so any override must come **after** the
  call, not before. We confirmed this by reading the apply_params body (lines 280-316) — it sets
  `h.v_init = V_INIT_MV` unconditionally.
* **`eleak_HHst` is a RANGE variable, not a global** [t0022][t0024] — overriding the Python
  constant `ELEAK_MV` in t0024 `constants.py` would have no effect on already-built sections. Must
  iterate `h.allsec()` and write `seg.eleak_HHst` per segment after cell build.
* **Single-trial determinism in t0022** [t0022] — the upstream deterministic E-I schedule makes
  the 96-trial budget genuinely sufficient; repeated trials at the same angle produce identical
  spike counts by construction.
* **Don't import across tasks** (project rule 9) — [t0022] / [t0024] code must be **copied**, not
  imported, even though the logic is almost identical to what we need.
* **Wall-time overestimates are cheap; underestimates stall the task** — [t0024] completing 800
  trials in 4 h 15 min was the actual reported time; the 960-trial sweep is roughly proportional (5
  h). Plan around 5-6 h for t0024 and 25-30 min for t0022 to leave headroom.
* **Polar tuning-curve plots are not in any library** — writing the ~40-line polar helper in this
  task is faster than threading a polar API through [t0011]. No prior task produced polar plots of
  DSGC tuning so there is no prior art to reuse.

## Recommendations for This Task

1. **Use a V_rest override block** injected between `apply_params(...)` and `h.finitialize(...)` in
   both copied trial runners. The block sets `h.v_init`, iterates `h.allsec()` to set `eleak_HHst`
   on every HHst-bearing segment, and sets `e_pas` on every pas-bearing segment (t0022 only —
   t0024 has no pas).
2. **Copy the t0022 and t0024 trial-runner bodies** into `code/run_vrest_sweep_t0022.py` and
   `code/run_vrest_sweep_t0024.py`. Do not attempt cross-task imports (project rule 9).
3. **Reuse `tuning_curve_loss` for DSI/HWHM analytics** (import via library). Do not reimplement
   scoring in this task.
4. **Write a minimal polar-plot helper** (new ~40 lines). Do not add a polar API to the [t0011]
   library — that is out of scope and a later task can library-ize this if multiple future tasks
   need it.
5. **Emit one tidy CSV per model** with columns
   `(v_rest_mv, trial, direction_deg, spike_count, peak_mv, firing_rate_hz)`, saved to
   `data/vrest_sweep_t0022.csv` and `data/vrest_sweep_t0024.csv`.
6. **Two predictions assets** (one per model), each pointing at its tidy CSV and describing the
   V_rest sweep as the "model" context.
7. **Metric keys**: register `dsi_at_vrest_*_mv` and `peak_hz_at_vrest_*_mv` lazily by first
   checking `meta/metrics/` with `aggregate_metrics`. If absent, report the values in
   `results_summary.md` without filling `metrics.json` to avoid mismatched keys, and raise a
   suggestion in `results/suggestions.json` proposing the registration.
8. **Expect ~5-6 h total wall time** for both sweeps; run them sequentially on the local
   workstation.

## Task Index

### [t0004]

* **Task ID**: `t0004_generate_target_tuning_curve`
* **Name**: Generate target tuning curve
* **Status**: completed
* **Relevance**: established the canonical tuning-curve CSV schema (angle_deg, trial_seed,
  firing_rate_hz) reused by both t0022 and t0024 and extended by this task.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 DSGC
* **Status**: completed
* **Relevance**: source of the `apply_params` function, the `modeldb_189347_dsgc` library (with
  `HHst.mod` defining `eleak_HHst`), and the HOC initialization logic that t0022 inherits.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response visualization library
* **Status**: completed
* **Relevance**: only Cartesian tuning-curve plotting is available; noted here to justify writing a
  separate minimal polar helper rather than extending the existing library.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning curve scoring/loss library
* **Status**: completed
* **Relevance**: provides DSI, HWHM, and reliability helpers used in the analysis step for reporting
  how tuning-curve shape varies with V_rest.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC (GABA-mod variant)
* **Status**: completed
* **Relevance**: cited only in the Library Landscape; the `modeldb_189347_dsgc_gabamod` library is a
  GABA-kinetics variant that neither t0022 nor t0024 depend on, so it is not reused by this task.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC channel testbed
* **Status**: completed
* **Relevance**: source of the dendritic E-I trial runner being adapted, provides
  `_run_one_trial_dendritic` and the `modeldb_189347_dsgc_dendritic` library metadata. One of the
  two models under V_rest sweep.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC
* **Status**: completed
* **Relevance**: source of the AR(2)-correlated trial runner and the `de_rosenroll_2026_dsgc`
  library. The other model under V_rest sweep.
