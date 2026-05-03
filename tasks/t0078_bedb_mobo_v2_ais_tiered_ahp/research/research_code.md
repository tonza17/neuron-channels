---
spec_version: "1"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 9
libraries_found: 14
libraries_relevant: 4
date_completed: "2026-05-03"
status: "complete"
---
# Research Code: Reusable Code Inventory for Bed B v2 MOBO with AIS, Tier-Stratified Channels, and Slow Kv-AHP

## Task Objective

Build an ~47-d BoTorch multi-objective Bayesian optimisation loop on the de Rosenroll 2026 (Bed B)
DSGC, augmented with (a) a two-subsegment AIS attached at the soma using Werginz/Wienbar/Kole
priors, (b) tier-stratified channel densities for Nav1.6, Kv3, NaP, BK, and SK across 5 compartment
tiers (soma, proximal-dendrite, mid-dendrite, terminal-dendrite, AIS), and (c) a slow Kv-mediated
AHP via SK_E2 with an `extended_tau_ca` parameter that scales the Ca-binding kinetics. The optimiser
jointly maximises DSI and PD firing rate using `qLogNoisyExpectedHypervolumeImprovement` with
`Normalize` input transform on `[0,1]^d` and `Standardize` outcome transform. Every cell evaluation
runs in a fresh `ProcessPoolExecutor` worker so the NEURON `Exp2NMDA name already exists`
non-idempotent loader bug (which broke `plot_pareto.py` deep-dive in t0076) cannot recur. The pass
criterion is to locate at least one Pareto cell with DSI >= 0.4 AND PD rate >= 30 Hz on the
augmented Bed B substrate, OR rule it out architecturally with HV >= 1.5x t0076's final HV (8.4129)
after >= 600 acquisition iterations.

## Library Landscape

The library aggregator (`aggregate_libraries.py`) is **not implemented** in
`arf/scripts/aggregators/` (only `aggregate_categories`, `aggregate_costs`, `aggregate_machines`,
`aggregate_metric_results`, `aggregate_metrics`, `aggregate_suggestions`, `aggregate_task_types`,
and `aggregate_tasks` exist). Per t0076's precedent, libraries were enumerated by direct filesystem
scan of `tasks/*/assets/library/*/details.json`, which returned **14** registered libraries:
`modeldb_189347_dsgc` [t0008], `tuning_curve_viz` [t0011], `tuning_curve_loss` [t0012],
`modeldb_189347_dsgc_gabamod` (t0020), `modeldb_189347_dsgc_dendritic` (t0022),
`de_rosenroll_2026_dsgc` [t0024], `modeldb_189347_dsgc_exact` (t0046), `minimal_dsgc_scalar_gaba`
(t0052), `minimal_dsgc_spatial_gaba` (t0053), `minimal_dsgc_ampa_nmda_scalar_gaba` (t0054),
`minimal_dsgc_mg_block_nmda` (t0055), `minimal_dsgc_tonic_gaba_sweep` (t0057),
`minimal_dsgc_bar_locked_gaba_ampa_sweep` (t0059), and `dsgc_active_channel_pack` [t0074].

Four libraries are directly relevant to t0078:

* **`de_rosenroll_2026_dsgc` v0.1.0** [t0024] — the Bed B substrate. Registered entry points:
  `build_dsgc_cell()`, `generate_ar2_batch()`, plus four CLI scripts. Vendored sources
  (`RGCmodelGD.hoc`, `HHst_noiseless.mod`, `cadecay.mod`, `Exp2NMDA.mod`, `nrnmech.dll`) live in
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`. Import
  path: `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell`. This
  is the substrate t0078 forks to attach an AIS section.

* **`dsgc_active_channel_pack` v0.1.0** [t0074] — 8-channel MOD pack
  (`nav16t74`/`napt74`/`nart74`/`kv3t74`/`kv4t74`/`bk74`/`sk74`/`kv7t74`) plus `cad`. The
  `code/mods/sk74.mod` file is the **vendored Hay 2011 SK_E2** that t0078 must extend with a
  `tau_ca_multiplier` parameter for slow-AHP behaviour. Import is via NEURON's `nrn_load_dll`, not
  Python; MOD files must be **copied** into the t0078 task folder.

* **`tuning_curve_loss` v0.1.0** [t0012] — canonical scorer. Provides `compute_dsi`,
  `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability` exported from
  `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py`. Used as the
  cross-task standard for `tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`
  registered project metrics that t0078's `Outputs` section requires. Import:
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import compute_dsi`.

* **`tuning_curve_viz` v0.1.0** [t0011] — Cartesian + polar plotters
  (`plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, `plot_multi_model_overlay`) for the
  per-axis sensitivity plots in t0078's Outputs section. Import:
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian import plot_cartesian_tuning_curve`.

The other 10 libraries are not relevant (Bed-A-specific substrates, toy minimal-cell experiments, or
Poleg-Polsky Bed A reproductions).

## Key Findings

### Bed B substrate construction is a single-call entry point that loads two MODs that DO collide

`build_dsgc_cell()` [t0024] at `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:251-296`
returns a frozen `DSGCCell` dataclass with `h`, `rgc`, `soma`, `all_dends` (350 sections),
`primary_dends` (8 order-1 sections), `non_terminal_dends` (165), `terminal_dends` (177),
`terminal_locs_xy` numpy `(177, 2)`, and `origin_xy`. Internally it (a) loads the t0024 vendored
`nrnmech.dll` from `assets/library/.../sources/` (containing `HHst`, `HHst_noiseless`, `cadecay`,
`Exp2NMDA`), (b) `chdir`s to the sources/ directory, (c) sources `RGCmodelGD.hoc`, (d) instantiates
`h.DSGC(0, 0)`, (e) walks the dendritic tree to label primary / non-terminal / terminal dendrites
via `_map_tree`, (f) inserts HHst + cad on every section with tier-specific gnabar densities. The
function is **process-non-idempotent**: a second `build_dsgc_cell()` call in the same Python process
raises `user defined name already exists: Exp2NMDA` because `nrn_load_dll` is one-shot and the t0024
DLL contains `POINT_PROCESS Exp2NMDA` at line 36 of
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`.

### The NEURON re-init bug location: `plot_pareto.py::_save_deep_dive`

`plot_pareto.py` [t0076] calls `build_dsgc_cell()` directly at line **264** inside
`_save_deep_dive`, which in turn is called once per pick in the `for idx, pick in enumerate(picks)`
loop at lines **376-377**. With `--n-deep-dives 3` (the default in the CLI at line 358), this calls
`build_dsgc_cell()` three times in the same Python process. The first call succeeds, the second
raises `Exp2NMDA name already exists`, and only **1 of 3** deep-dive PNGs is emitted. This is
documented in `tasks/t0076_bedb_dsi_firing_rate_mobo/results/results_detailed.md` line 484 and in
the S-0076-03 suggestion at line 35 of `results/suggestions.json`. The fix t0078 adopts
(`subprocess-per-deep-dive`) requires either (a) launching a fresh
`python -m tasks.t0078...plot_pareto --idx <i>` subprocess per pick, or (b) wrapping
`_save_deep_dive` in a `ProcessPoolExecutor.submit(max_workers=1)` call so each pick runs in a fresh
worker process. Option (b) is the smaller change and matches t0076's existing
`evaluate_parameter_vector` worker-per-trial pattern.

### qLogNEHVI / Normalize / Standardize migration sites in `mobo_loop.py`

`mobo_loop.py` [t0076] at `tasks/t0076_bedb_dsi_firing_rate_mobo/code/mobo_loop.py` contains the
exact migration sites:

* **Line 24-26**:
  `from botorch.acquisition.multi_objective.monte_carlo import qNoisyExpectedHypervolumeImprovement`
  -> change to
  `from botorch.acquisition.multi_objective.logei import qLogNoisyExpectedHypervolumeImprovement`
  (or the equivalent re-export path that BoTorch documents).
* **Line 350**: `acq = qNoisyExpectedHypervolumeImprovement(...)` -> change class to
  `qLogNoisyExpectedHypervolumeImprovement(...)`. Per `research_internet.md` quote of the BoTorch
  tutorial, this is a single-line change with the same API (the tutorial says "It is strongly
  recommended to simply replace `qNoisyExpectedHypervolumeImprovement` with
  `qLogNoisyExpectedHypervolumeImprovement`, which fixes the issues and has the same API"); no other
  arguments need updating, though `tau_max=1e-3` and `tau_relu` smoothing parameters can be passed
  if numerical stability needs further tuning.
* **Line 240-257** (`_fit_gp_models`):
  `SingleTaskGP(train_X=train_x, train_Y=y_i, outcome_transform=Standardize(m=1))`. The
  `Standardize(m=1)` outcome transform is **already present** on every objective. The missing piece
  is the `Normalize` **input** transform — t0076 passed natural-units bounds to the GP without
  normalisation, which BoTorch warned was suboptimal. To add:
  `from botorch.models.transforms.input import Normalize` and pass
  `input_transform=Normalize(d=N_PARAMS)` (or `d=47` for t0078) to the `SingleTaskGP` constructor.
  Combined with `bounds` already in `[0, 1]^d` (since `optimize_acqf` sees normalised bounds), the
  GP will operate entirely on `[0, 1]^d`.
* **Line 286** (`draw_sobol_samples(bounds=bounds, n=n_sobol, q=1)`): Sobol DoE is already drawn in
  the optimisation-space bounds. With the new `Normalize` transform and `bounds = [[0]*d, [1]*d]`,
  no extra scaling code is needed; the Sobol draw stays in `[0, 1]^d`.
* **Line 80-91** (`_make_optimisation_bounds` / `_opt_to_natural`): the existing log10
  transformation for `LOG_PARAM_INDICES` should remain — log-uniform parameters live in log10
  space inside the GP, with exponentiation at evaluation time. The Normalize transform sits on top:
  `bounds = [[0]*d, [1]*d]` in optimisation space, with `_opt_to_natural` first un-log10ing then
  exponentiating where appropriate.

### NEURON re-init bug bypass via `ProcessPoolExecutor` worker-per-evaluation

`trial_driver.py::evaluate_parameter_vector` [t0076] at lines **309-369** already uses the right
pattern: each cell evaluation submits 8 directions x 20 seeds = 160 trials to a
`ProcessPoolExecutor(max_workers=cpu_count()-1)`, where each worker keeps its own `_WORKER_CELL`
(line **81**) cached after the first `build_dsgc_cell()` call. The worker process itself is fresh,
so the `Exp2NMDA name already exists` error never occurs — workers either build the cell once and
reuse it across many trials, or are restarted (Python's `ProcessPoolExecutor` does not respawn
workers between submissions by default). For t0078 the trial driver is reused unchanged; only
`plot_pareto.py::_save_deep_dive` needs the worker-per-deep-dive wrapper added.

### AIS attachment architecture from t0069 (Bed A)

`extend_with_ais.py` [t0069] at
`tasks/t0069_t0067_ais_localised_channel_sweep/code/extend_with_ais.py` is a 75-line module that
creates two NEURON `Section` objects (`ais_t69` and `axon_t69`), configures them with `L`, `diam`,
`nseg`, `Ra`, `cm`, inserts `HHst`, sets per-segment `gnabar`, `gkbar`, `gkmbar`, `gleak`, `eleak`,
then connects them with `ais.connect(soma, 1.0, 0.0)` and `axon.connect(ais, 1.0, 0.0)`. Constants
(length 30 um, diameter 1 um, nseg 5, gNa 30 mS/cm^2, gK 20 mS/cm^2, gKM 3 mS/cm^2 for the AIS) live
in `tasks/t0069_t0067_ais_localised_channel_sweep/code/constants.py:78-91`. **For t0078** this
architecture is the right starting point but needs three modifications:

1. The AIS must be **two-subsegment** (proximal Nav1.1/Nav1.2, distal Nav1.6/Kv1.2) per the
   research_papers.md and research_internet.md Werginz/Wienbar templates, not a single AIS section.
   Implementation: build two `h.Section` objects (`ais_proximal`, `ais_distal`), each ~15 um, with
   `ais_distal.connect(ais_proximal, 1.0, 0.0)` and `ais_proximal.connect(soma, 1.0, 0.0)`.
2. The channel-set must include the new t78-namespace SUFFIXes
   (`nav16t78`/`kv3t78`/`kv7t78`/`napt78`/`bkt78`/`skt78`/`skahpt78`) instead of just `HHst`. NaP,
   BK, SK are explicitly excluded from the AIS section per the task description Scope (line 60):
   "NaP, BK, SK explicitly excluded from the AIS section (biologically not at AIS in RGCs)".
3. The `nseg` rule should follow `d_lambda = 0.1` at 100 Hz per the task description Risks section.
   NEURON's `lambda_f(100)` from `stdrun.hoc` returns the AC length constant; the convention is
   `nseg = int((sec.L / (0.1 * h.lambda_f(100, sec=sec))) / 2) * 2 + 1` to round to the nearest odd
   number. The t0069 `AIS_NSEG = 5` is acceptable for a 30 um AIS but should be computed dynamically
   for the longer 25-50 um range t0078 will explore.

### SK_E2 vendored MOD file at `sk74.mod` is the slow-AHP starting point

`sk74.mod` [t0074] at `tasks/t0074_channel_tuning_width_bed_a/code/mods/sk74.mod` is a 67-line MOD
file with `SUFFIX sk74`, `USEION ca READ cai`, `NONSPECIFIC_CURRENT i`, and a single `STATE m` gate
driven purely by intracellular calcium via `m_inf = 1 / (1 + (EC50/cai)^Hill)` with
`EC50 = 0.43 uM`, `Hill = 4.8`, and `tau_m = 1 ms` (line 33: `tau_m = 1.0 (ms)`). The Hay 2011 SK_E2
source is preserved verbatim. To extend with `extended_tau_ca` for the slow-AHP behaviour, t0078 has
**three implementation options**:

1. **Add a `tau_ca_multiplier` PARAMETER and scale `tau_m` by it**:
   ```
   PARAMETER {
       tau_ca_multiplier = 1.0
       tau_m_base = 1.0 (ms)
   }
   ASSIGNED { tau_m_eff (ms) }
   PROCEDURE rates(cai (mM)) {
       ...
       tau_m_eff = tau_m_base * tau_ca_multiplier
   }
   DERIVATIVE states {
       m' = (minf - m) / tau_m_eff
   }
   ```
   This is the smallest change. With `tau_ca_multiplier = 1` (the default) the kinetics are
   identical to t0074. With multiplier = 100 the effective tau is 100 ms, approaching the slow-AHP
   regime. Per `research_internet.md` recommendation 4, the prior should span [1, 200x].

2. **Scale the `cad` Ca-pool `taur` instead** — modify the cadecay.mod to expose `taur` as
   per-segment-RANGE (which it already is). This adjusts the speed of Ca decay (and therefore
   indirectly the SK m_inf trajectory) but does not change the SK gate kinetics directly. This does
   not match the `extended_tau_ca` naming in the task description, which targets the Ca-binding rate
   of SK.

3. **Add a downstream KCNQ-like slow K+ mechanism** — per the Larsson 2013 review in
   research_internet.md, real slow-AHP is not Ca-binding kinetics on SK but downstream KCNQ
   activation. This is the cleanest biophysical solution but requires a new MOD file and a
   `cad`-derived `cai_slow` ASSIGNED variable, which the task description does not require.

**Recommendation**: implement Option 1. The MOD file is at line 33 of t0074's `sk74.mod`; t0078
copies it to `code/mods/skahpt78.mod`, renames `SUFFIX sk74` to `SUFFIX skahpt78`, adds
`tau_ca_multiplier` to PARAMETER, replaces `tau_m` with `tau_m_eff` in the derivative, and updates
the citation header. Sanity-check at multiplier=1 reproduces the t0074 SK behaviour exactly.

### t0076 trial-driver pattern is reusable verbatim

`trial_driver.py` [t0076] at lines **309-369** (`evaluate_parameter_vector`) already implements the
exact 8-direction x 20-seed x 160-trial pattern needed by t0078, with the worker-per-trial isolation
that bypasses the NEURON re-init bug. The driver takes a `ParameterVector` (a frozen dataclass with
`values: NDArray[np.float64]`), submits 160 trials to a `ProcessPoolExecutor`, aggregates spike
counts into PD/ND means, computes DSI = (PD - ND) / (PD + ND), and computes PD rate (Hz) = PD spikes
/ (TSTOP_MS / 1000). For t0078 this is reused unchanged — only the `ParameterVector` dimension
grows from 25 to ~47, and the `apply_parameter_vector` function in `apply_params.py` (lines 59-89)
needs to be extended to write per-tier densities to per-tier sections plus the AIS sections plus the
SK_E2 `tau_ca_multiplier`.

### Tier-stratified channel application requires extension of `apply_params.py`

`apply_params.py` [t0076] at lines **59-89** currently writes a single density per channel to
**every** section in `[cell.soma] + cell.all_dends`, with no distinction between primary,
non-terminal, terminal, or AIS. For t0078 the function must be extended to:

1. Write soma-tier densities to `cell.soma` only.
2. Write proximal-dendrite densities to `cell.primary_dends` (the 8 order-1 sections).
3. Write mid-dendrite densities to `cell.non_terminal_dends` (the 165 mid-tree sections).
4. Write terminal-dendrite densities to `cell.terminal_dends` (the 177 terminal sections).
5. Write AIS densities to the new `ais_proximal` + `ais_distal` sections (built by the AIS
   attacher).
6. Write the SK_E2 `tau_ca_multiplier` as a per-segment RANGE on the soma + AIS sections only (not
   on dendrites — per task description Scope line 73: "Insertion sites: soma + AIS only").

This is straightforward — t0024's `_configure_dends` (`build_cell.py:204-248`) already
demonstrates the pattern of iterating per-tier and applying tier-specific densities. The new t0078
`apply_parameter_vector` should mirror that structure with five loops (soma, primary, non-terminal,
terminal, AIS) instead of one combined loop.

### Bootstrap pattern for cross-platform NEURON loading

`bootstrap.py` [t0076] at lines **1-117** already handles the Windows-vs-Linux NEURON loading
asymmetry: Windows uses local `C:\Users\md1avn\nrn-8.2.7\` install + vendored `nrnmech.dll`; Linux
uses pip `neuron==8.2.7` wheel + `compile_t0024_mods_linux()` to build a `.so` from the t0024
sources. The module monkey-patches t0024's `_ensure_neuron_on_path` to a no-op and replaces
`load_neuron` with a Linux-aware variant. **t0078 reuses this verbatim**: copy the entire
`bootstrap.py` into `tasks/t0078.../code/bootstrap.py` and update the
`_T76_LINUX_BUILD_DIR`-equivalent paths to `_T78_LINUX_BUILD_DIR`. Both t0076 and t0024 MOD
libraries must be compilable on Linux for t0078 to run on Vast.ai.

### `dsgc_active_channel_pack` MODs are the inheritance root for t78-namespace channels

The 8-channel pack in `dsgc_active_channel_pack` [t0074] (at
`tasks/t0074_channel_tuning_width_bed_a/code/mods/`) provides verbatim-reusable `nav16t74.mod`,
`napt74.mod`, `nart74.mod`, `kv3t74.mod`, `kv4t74.mod`, `bk74.mod`, `sk74.mod`, `kv7t74.mod`, plus
`cadecay.mod`. t0076 already copied 12 MOD files into
`tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/` with SUFFIX renamed `t74` -> `t76`. For t0078 the
same approach: copy the t0076 MOD pack into `tasks/t0078_.../code/mods/` with SUFFIX renamed `t76`
-> `t78`. **Important**: t0076's research notes that Bed B's vendored `cadecay.mod` is already
loaded by `build_dsgc_cell` first; the t0076 local MOD library therefore EXCLUDES `cadecay.mod` (per
t0076's research_code.md lines 500-506). t0078 must follow the same rule — include only the 12
t78-namespace channels plus the new `skahpt78.mod` (slow-AHP SK_E2 with `tau_ca_multiplier`),
excluding `cadecay.mod`.

## Reusable Code and Assets

### Library imports (cross-task allowed)

* **`build_dsgc_cell`** — **import via library**.
  * Source: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:251-296`
  * Signature: `def build_dsgc_cell() -> DSGCCell:`
  * Returns:
    `DSGCCell(h, rgc, soma, all_dends, primary_dends, non_terminal_dends, terminal_dends, terminal_locs_xy, origin_xy)`
  * Adaptation needed: none directly — t0078 wraps it in a thin `build_dsgc_cell_with_ais()`
    function that calls `build_dsgc_cell()`, then attaches the AIS via the new `extend_with_ais`
    module.
  * Line count: 46 lines used as-is.

* **`generate_ar2_batch`** — **import via library**.
  * Source: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py`
  * Signature:
    `def generate_ar2_batch(*, n_samples: int, n_streams: int, phi: tuple[float, float], rho: float, seed: int, innov_scale: float = 1.0) -> NDArray[np.float64]:`
  * Adaptation needed: none.
  * Line count: ~150 lines used as-is via import.

* **`compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`**
  — **import via library**.
  * Source: `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py`
  * Signatures (all accept a `TuningCurve` or array argument and return `float | None`).
  * Adaptation needed: tuning_curve format conversion — t0078 must build a 12-angle CSV from the
    8-direction Pareto-cell trial counts, then call these metrics.
  * Line count: imported, not copied.

* **`plot_cartesian_tuning_curve`, `plot_polar_tuning_curve`, `plot_multi_model_overlay`** —
  **import via library**.
  * Source: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/`
  * Adaptation needed: per-axis sensitivity panels need wrapping — call once per stratified
    channel, with the channel density on the x-axis and DSI/rate/HWHM on the y-axis.

### Code to copy into t0078's `code/` directory

* **`bootstrap.py`** — **copy into task** (with SUFFIX-namespace updates).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/bootstrap.py:1-117`
  * What it does: Windows/Linux NEURON loader + Linux MOD compilation helper.
  * Adaptation: rename internal globals from `_T76_*` to `_T78_*`, update paths to point at
    `tasks/t0078_.../code/mods/` for the t78 MOD library; keep the t0024 sources path unchanged
    since the de Rosenroll cell builder still needs that DLL.
  * Line count: ~117 lines.

* **`trial_driver.py`** — **copy into task** (~400 lines).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/trial_driver.py:1-400`
  * What it does: ProcessPoolExecutor worker-per-cell evaluation pattern; `_worker_run_trial` (the
    picklable top-level worker entrypoint), `_summarise_trials`, `evaluate_parameter_vector`,
    `run_one_trial`.
  * Adaptation: replace the import of `apply_parameter_vector` with the new t0078 tier-aware
    version; replace `setup_synapses_parametric` import with t0078's variant (which may need to be
    tier-aware if the synapse placement parameters change semantics); add an `extend_with_ais()`
    call inside `_worker_get_cell()` so AIS sections are attached on first cell construction. Keep
    `TSTOP_MS = 1400.0` per the project's standard mode trio (t0078 task description Stimulus
    protocol line 117); t0076 used `TSTOP_MS = 1000.0` so this constant must change.
  * Line count: 400 lines minus ~30 lines of t0076-specific code = ~370 reusable.

* **`mobo_loop.py`** — **copy into task** (with qLogNEHVI / Normalize migrations).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/mobo_loop.py:1-484`
  * What it does: Sobol DoE + qNEHVI acquisition loop, hypervolume tracking, checkpointing,
    Pareto-front extraction, budget gates.
  * Adaptation: (a) replace `qNoisyExpectedHypervolumeImprovement` import and class call with
    `qLogNoisyExpectedHypervolumeImprovement` (lines 24, 350); (b) add
    `from botorch.models.transforms.input import Normalize` and pass
    `input_transform=Normalize(d=N_PARAMS)` to `SingleTaskGP` (line 246-250); (c) increase
    `N_SOBOL_INITIAL` from 30 to 50-100 and `N_ACQ_ITERATIONS` from 400 to 600-800 in constants; (d)
    recompute `REF_POINT_RATE_HZ` if the re-targeted utopia point (research_internet.md
    recommendation 2) is adopted.
  * Line count: ~484 lines, ~10 lines change.

* **`apply_params.py`** — **copy into task and extend** (~90 -> ~200 lines).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/apply_params.py:1-89`
  * What it does: load t76 DLL once per process, insert all 12 SUFFIX channel mechanisms on every
    section, write per-segment gbar values, write passive Ra/cm/gleak.
  * Adaptation: replace the single-tier write loop (line 78-88) with five tier-specific loops
    matching `cell.soma`, `cell.primary_dends`, `cell.non_terminal_dends`, `cell.terminal_dends`,
    and the new AIS sections. Add SK_E2 `tau_ca_multiplier` write to soma + AIS only. Insertion list
    must include the new `skahpt78` SUFFIX. Update DLL path to `t0078_.../code/mods/`.
  * Line count: ~200 lines after extension.

* **`parametric_placer.py`** — **copy into task** (~105 lines, no change).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/parametric_placer.py:1-105`
  * What it does: walks `cell.all_dends`, computes path distance via
    `h.distance(cell.soma(0.5), sec(0.5))`, samples synapse positions weighted by
    `rho_0 * exp(-d / lambda) * L_section`.
  * Adaptation: optionally exclude AIS sections from the placement candidates (since AIS gets no
    synapses in the de Rosenroll model); pass `candidate_sections=cell.all_dends` (the existing
    behaviour already excludes the AIS because it is not in `all_dends`). No code change needed if
    AIS sections live outside `cell.all_dends`.
  * Line count: 105 reused as-is.

* **`trial_helpers.py`** — **copy into task** (~283 lines, ~30 lines change for tstop).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/trial_helpers.py:1-283`
  * What it does: COPIED-verbatim helpers from t0024 (`_bar_arrival_times`, `_rates_with_ar2_noise`,
    `_gaba_prob_for_direction`, `_rates_to_events`, `_count_spikes`, `BASE_ACH_PROB`, `RATE_DT_MS`,
    `BAR_SIGMA_MS`, `CELL_PREF_DEG`, `PREF_GABA_PROB`, `NULL_GABA_PROB`) plus the NEW
    `setup_synapses_parametric` and `SynapseBundle` dataclass.
  * Adaptation: re-import constants from `t0078...constants` instead of `t0076...constants`. No
    other code change.
  * Line count: 283 reused.

* **`recorder.py`** — **copy into task** (~122 lines, no change).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/recorder.py:1-122`
  * What it does: per-synapse recorders for the deep-dive traces; `attach_recorders`,
    `save_recorders_npz`.
  * Adaptation: none.
  * Line count: 122 reused.

* **`plot_pareto.py`** — **copy into task and fix the NEURON re-init bug** (~397 -> ~430 lines).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/plot_pareto.py:1-397`
  * What it does: Pareto-front scatter, hypervolume trajectory plot, deep-dive cell selection
    (highest DSI / highest rate / knee), per-cell tuning curve + trace PNGs, deep-dive .npz dumps.
  * Adaptation: **wrap `_save_deep_dive` in a `ProcessPoolExecutor` worker** (single-worker pool
    `with ProcessPoolExecutor(max_workers=1) as ex: ex.submit(_save_deep_dive, pick=pick, idx=idx).result()`)
    so each pick runs in its own subprocess and the `Exp2NMDA name already exists` re-init error
    cannot occur. Alternatively, move `_save_deep_dive` into a top-level
    `python -m tasks.t0078...plot_one_deep_dive --idx <i>` script that the main `plot_pareto.py`
    invokes via `subprocess.run`. Both options are documented in S-0076-03 and the t0078 task
    description Approach line 165.
  * Line count: ~430 lines.

* **`render_pdf.py`** — **copy into task** (~63 lines, no change).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/render_pdf.py:1-63`
  * What it does: Typst typesetting wrapper for the results PDF.
  * Adaptation: none.

* **`run_remote.sh`** — **copy into task** (~43 lines, ~5 lines change).
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/run_remote.sh:1-43`
  * What it does: Vast.ai launcher: git checkout task branch, compile MODs via nrnivmodl, launch
    mobo_loop in the background.
  * Adaptation: rebrand task ID `t0076` -> `t0078`, update `--n-iterations` to 600-800, `--n-sobol`
    to 50-100. Update branch name to `task/t0078_bedb_mobo_v2_ais_tiered_ahp`.

* **MOD files** — **copy into task with SUFFIX rename**.
  * Source: `tasks/t0076_bedb_dsi_firing_rate_mobo/code/mods/*.mod` (12 files: `bkt76.mod`,
    `calt76.mod`, `catt76.mod`, `iht76.mod`, `kdrt76.mod`, `kv3t76.mod`, `kv4t76.mod`, `kv7t76.mod`,
    `napt76.mod`, `nart76.mod`, `nav16t76.mod`, `skt76.mod`).
  * Adaptation: for each file, `sed s/t76/t78/g` to rename SUFFIXes and filenames.
  * **New MOD**: `skahpt78.mod` derived from `skt76.mod` by adding the `tau_ca_multiplier` PARAMETER
    and replacing `tau_m` with `tau_m_eff = tau_m_base * tau_ca_multiplier` in the DERIVATIVE block.
  * Line count: 12 files * ~70 lines = ~840 lines copied; ~80-line new MOD file.

* **`extend_with_ais.py`** — **copy into task and extend** (~75 -> ~150 lines).
  * Source: `tasks/t0069_t0067_ais_localised_channel_sweep/code/extend_with_ais.py:1-75`
  * What it does: build a single AIS section + 1 mm passive axon, attach to soma(1).
  * Adaptation: split the AIS into two subsections (`ais_proximal` for Nav1.1/Nav1.2 + `ais_distal`
    for Nav1.6/Kv1.2); update the section names to `ais_proximal_t78`, `ais_distal_t78`, `axon_t78`;
    add segment-count rule `nseg = int((sec.L / (0.1 * h.lambda_f(100, sec=sec))) / 2) * 2 + 1`;
    insert `nav16t78`, `kv3t78`, `kv7t78` SUFFIXes (not bare HHst) on the AIS subsections; expose
    AIS length and diameter as parameters that the BO can read from the parameter vector (so the BO
    can search over AIS length 25-50 um).
  * Line count: ~150 lines.

## Lessons Learned

### Worker-per-evaluation is the right NEURON-isolation pattern

t0076 confirmed that `ProcessPoolExecutor` with worker-per-trial submission is the correct pattern
for parallelising NEURON simulations: each worker is its own process, gets a clean NEURON state on
first `build_dsgc_cell()`, caches the cell across many trials, and dies cleanly at end of pool. The
error `Exp2NMDA name already exists` only occurred in `plot_pareto.py::_save_deep_dive` because that
function bypasses the pool and calls `build_dsgc_cell()` directly multiple times in the main
process. The fix for t0078 is to apply the same isolation pattern to the deep-dive code path.

### qNEHVI on natural-units bounds was the root of t0076's GP fit warnings

t0076's BoTorch GP fit emitted warnings about a "suboptimal" fit because the input bounds were
passed to `SingleTaskGP` in natural units (mixed S/cm^2, mS/cm^2, um, count, dimensionless) with
ranges spanning >10 orders of magnitude. The Standardize outcome transform was present but Normalize
input transform was missing. Per the BoTorch documentation, the recommended setup is **both**
transforms simultaneously. t0078 must add the input Normalize transform to remove the GP fit
warnings.

### t0024's HOC `chdir` pattern is fragile but works

`build_cell.py:258-267` [t0024] uses an `os.chdir(P.LIBRARY_SOURCES_DIR)` block to source the HOC
template. This works on Windows but has caused issues in derived tasks that import the cell builder
(the cwd becomes the t0024 sources directory). t0078 must NOT call `build_dsgc_cell` from a working
directory that the HOC source paths depend on; the chdir-then-restore pattern is already idempotent
in t0024, but downstream tasks must not assume cwd is preserved. Use absolute paths for all
filesystem operations after `build_dsgc_cell()`.

### Bed B `cad` is already loaded — do not duplicate in the t78 MOD library

t0076's research_code.md lines 500-506 documented this trap: t0024's vendored `nrnmech.dll` already
contains `cadecay`, so the t0076 local MOD library was deliberately built without `cadecay.mod` to
avoid the SUFFIX collision. t0078 must follow the same rule: include only the 12 t78-namespace
channels plus `skahpt78.mod`, excluding `cadecay.mod`. The `cad` SUFFIX exposed by t0024 is shared
across all tasks that use Bed B and is the Ca pool the new SK_E2-extended-AHP mechanism reads from.

### Vast.ai 72-core CPU instance is the right compute target

t0076 ran 430 cells x 8 dirs x 20 seeds = 68,800 NEURON trials on a Vast.ai Xeon E5-2686 v4 / 72
core / 96 GB instance at $0.16357/hr for 6.47 h = $1.06. The scaling is roughly 3.4 s/trial
single-threaded, divided by 72 cores. For t0078 the trial count grows ~2x (650-900 cells) and the
per-trial time grows ~10% (AIS overhead), so total wall-clock is 9-12 h, total cost $1.59-$2.66 plus
20% contingency = $1.91-$2.66 per the task description Compute Estimate. The same Vast.ai launcher
pattern from `run_remote.sh` is reused directly.

### Plan for `Normalize` and qLogNEHVI together

Per research_internet.md, the `qLogNoisyExpectedHypervolumeImprovement` migration is a single-line
change but requires the GP to operate on `[0, 1]^d` (otherwise the `tau_max` smoothing parameters
become miscalibrated). Implementing only one of the two changes (qLogNEHVI without Normalize, or
Normalize without qLogNEHVI) is worse than implementing neither. Both must be applied
simultaneously.

## Recommendations for This Task

1. **Library-import `build_dsgc_cell`** from `de_rosenroll_2026_dsgc` [t0024] and wrap it in a thin
   `build_dsgc_cell_with_ais()` function in `code/build_cell_ais.py` that calls `build_dsgc_cell()`,
   then calls the t0078 `extend_with_ais()` function to attach the two-subsegment AIS.

2. **Library-import the metric and viz functions** from [t0011] and [t0012]. Specifically import
   `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`, `compute_reliability`
   from `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics`, and import
   `plot_cartesian_tuning_curve`, `plot_polar_tuning_curve` from
   `tasks.t0011_response_visualization_library.code.tuning_curve_viz`.

3. **Copy the t0076 BoTorch harness verbatim** (`mobo_loop.py`, `trial_driver.py`,
   `trial_helpers.py`, `apply_params.py`, `parametric_placer.py`, `recorder.py`, `bootstrap.py`,
   `render_pdf.py`, `run_remote.sh`) into `tasks/t0078_.../code/`. Apply two surgical edits: (a)
   qNEHVI -> qLogNEHVI in `mobo_loop.py:24,350`, (b) add `Normalize(d=N_PARAMS)` input transform to
   `_fit_gp_models` at `mobo_loop.py:240-257`. Update `TSTOP_MS = 1400.0` in `constants.py` to match
   the project's standard mode trio.

4. **Copy and extend t0069's `extend_with_ais.py`** into `code/extend_with_ais.py`. Split the AIS
   into two NEURON sections (`ais_proximal_t78`, `ais_distal_t78`); apply the `d_lambda = 0.1`
   segment-count rule; insert t78-namespace SUFFIXes (`nav16t78`, `kv3t78`, `kv7t78`) on the AIS
   sections; explicitly exclude `napt78`, `bkt78`, `skt78` from the AIS per the task description
   Scope.

5. **Copy and extend `apply_params.py`** to write tier-stratified densities. Replace the single
   write loop (lines 78-88) with five tier-specific loops. Add the SK_E2 `tau_ca_multiplier` write
   to soma + AIS only. The tier mapping is: soma -> `cell.soma`, proximal-dendrite ->
   `cell.primary_dends`, mid-dendrite -> `cell.non_terminal_dends`, terminal-dendrite ->
   `cell.terminal_dends`, AIS -> the new AIS sections returned by `extend_with_ais`.

6. **Vendor the slow-AHP SK_E2** at `code/mods/skahpt78.mod`. Start from the t0074 `sk74.mod`, add
   `tau_ca_multiplier` PARAMETER, replace `m' = (minf - m) / tau_m` with
   `m' = (minf - m) / (tau_m * tau_ca_multiplier)`, and SUFFIX-rename to `skahpt78`. Sanity-check
   that `tau_ca_multiplier = 1.0` reproduces the t0074 sk74 behaviour exactly.

7. **Fix `plot_pareto.py::_save_deep_dive` with worker-per-deep-dive**. Wrap each pick's
   `_save_deep_dive(pick=pick, idx=idx)` call in a single-worker `ProcessPoolExecutor` so the NEURON
   re-init error cannot occur. Verify by running with `--n-deep-dives 3` and confirming all 3 PNGs
   are emitted.

8. **Define the 47-d parameter space** in `code/constants.py`. Mirror t0076's `ParameterVector`
   dataclass + `ParamIndex` IntEnum but extend with: 25 tier-stratified channel densities (5
   channels x 5 tiers), 7 uniform-density channels (Nav1.6 NaR, Kdr, Kv3, Kv4, Kv7, HCN, CaL, CaT
   — pick the t0076 set minus the 5 stratified channels), 2 SK_E2 slow-AHP params (gbar +
   `tau_ca_multiplier`), 13 synaptic placement params (kept from t0076 + 5 new AIS-specific
   synaptic-density params if needed). Use the t0076 `LOG_PARAM_INDICES` pattern for log-uniform
   params; treat AIS length 25-50 um and AIS diameter 0.6-1.0 um as linear params if they are search
   variables.

9. **Reuse the Vast.ai 72-core launcher pattern** from t0076's `run_remote.sh`. Update task ID,
   branch name, and BO budget (50-100 Sobol + 600-800 acquisition iterations).

10. **Update bootstrap.py paths to include both t0024 and t0078 MOD libraries**. The t0024 DLL is
    loaded first by `build_dsgc_cell` (provides HHst, cadecay, Exp2NMDA); the t0078 DLL is loaded
    second by `apply_parameter_vector` (provides the 12 t78 channels + skahpt78 slow-AHP). On Linux
    both libraries must be compiled by `nrnivmodl` before the BO loop launches.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 (Poleg-Polsky 2016) to NEURON+Python
* **Status**: completed
* **Relevance**: Provides the `modeldb_189347_dsgc` library asset (Bed A); not directly used by
  t0078 but is the substrate of t0069's AIS attachment code which t0078 ports. The Bed A attachment
  pattern is the architecture template for Bed B's AIS.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response Visualization Library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_viz` library that t0078 imports for the per-axis
  sensitivity panels and Pareto-front polar overlays.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning Curve Scoring Loss Library
* **Status**: completed
* **Relevance**: Provides the `tuning_curve_loss` library with `compute_dsi`, `compute_hwhm_deg`,
  `compute_reliability`, `compute_peak_hz`, `compute_null_hz` registered project metrics that
  t0078's per-Pareto-cell width metric computation requires.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC to NEURON
* **Status**: completed
* **Relevance**: Direct dependency. Provides the `de_rosenroll_2026_dsgc` library and the Bed B cell
  builder (`build_dsgc_cell()`) that t0078 forks. Vendors `RGCmodelGD.hoc`, `HHst_noiseless.mod`,
  `cadecay.mod`, `Exp2NMDA.mod`, and the precompiled `nrnmech.dll`.

### [t0050]

* **Task ID**: `t0050_audit_syn_distribution`
* **Name**: Audit synapse distribution: deposited Poleg-Polsky vs paper
* **Status**: completed
* **Relevance**: Established the canonical `h.distance(soma_seg, target_seg)` two-argument form for
  path-distance computation, used by t0076's parametric placer and reused unchanged in t0078.

### [t0066]

* **Task ID**: `t0066_t0024_epsp_ipsp_vm_protocol`
* **Name**: t0024 EPSP/IPSP Vm protocol
* **Status**: completed
* **Relevance**: Source of the `_ensure_neuron_loaded()` idempotent NEURON loader pattern at
  `code/run_protocol.py:70-88` and the `CanonicalState` snapshot/restore pattern at lines 117-175.
  t0078's apply_params extends this pattern to write per-tier densities.

### [t0067]

* **Task ID**: `t0067_t0065_soma_channel_addition_sweep`
* **Name**: Soma channel addition sweep on Bed A
* **Status**: completed
* **Relevance**: Source of the `_ensure_t67_dll_loaded` per-process DLL guard pattern (15 lines)
  copied to t0076's `apply_params.py::ensure_t76_dll_loaded` and adopted by t0078 as
  `ensure_t78_dll_loaded`.

### [t0069]

* **Task ID**: `t0069_t0067_ais_localised_channel_sweep`
* **Name**: AIS-localised channel sweep on Bed A
* **Status**: completed
* **Relevance**: Direct dependency. Provides the AIS attachment architecture in
  `code/extend_with_ais.py` (75 lines) and the AIS geometry constants at `code/constants.py:78-91`
  (length 30 um, diameter 1 um, nseg 5, gNa 30 mS/cm^2, gK 20 mS/cm^2, gKM 3 mS/cm^2). t0078 copies
  this module and extends it to two-subsegment AIS with t78-namespace channels.

### [t0074]

* **Task ID**: `t0074_channel_tuning_width_bed_a`
* **Name**: Channel tuning-width sweep on Bed A
* **Status**: completed
* **Relevance**: Provides the `dsgc_active_channel_pack` library (8 channel MODs + cad). The
  `code/mods/sk74.mod` file is the verbatim Hay 2011 SK_E2 implementation that t0078 extends with a
  `tau_ca_multiplier` parameter to add slow-AHP behaviour.

### [t0076]

* **Task ID**: `t0076_bedb_dsi_firing_rate_mobo`
* **Name**: Multi-objective BO of channels + synapse placement on Bed B
* **Status**: completed
* **Relevance**: Direct dependency and the predecessor task. Provides ~2,500 LOC of MOBO
  infrastructure: `mobo_loop.py` (Sobol + qNEHVI loop, hypervolume tracking, checkpointing),
  `trial_driver.py` (ProcessPoolExecutor worker-per-cell), `parametric_placer.py` (exponential-decay
  spatial sampler), `apply_params.py` (per-segment density writer), `bootstrap.py` (Windows/Linux
  NEURON loader), `recorder.py` (per-synapse trace recorder), `plot_pareto.py` (Pareto-front +
  hypervolume plots, with the `Exp2NMDA` deep-dive bug), `render_pdf.py` (Typst writeup),
  `run_remote.sh` (Vast.ai launcher), 12 t76-namespace MOD files. t0078 forks all of this and
  applies three surgical edits: qNEHVI -> qLogNEHVI, add Normalize input transform, fix the
  deep-dive subprocess pattern.
