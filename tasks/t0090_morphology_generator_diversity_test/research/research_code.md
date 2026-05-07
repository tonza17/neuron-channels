---
spec_version: "1"
task_id: "t0090_morphology_generator_diversity_test"
research_stage: "code"
tasks_reviewed: 17
tasks_cited: 14
libraries_found: 16
libraries_relevant: 5
date_completed: "2026-05-07"
status: "complete"
---
# Research Code -- Procedural DSGC Morphology Generator + Diversity Test + Validation Bundle

## Task Objective

t0090 implements a procedural DSGC morphology generator with 14 explicit knobs (5 topology + 4
asymmetry + 3 geometry + 2 stochastic), generates 30 maximally different (Latin Hypercube) and 30
maximally similar (+/- 5 percent perturbation) morphologies, runs verification simulations, produces
visualisations (2D dendrograms + morphometric PCA / UMAP), performs a Bed-B reproducibility check on
5 t0083 Pareto cells, and bundles three validation suggestions in Phase G (S-0088-02 AIS-to-soma Nav
ratio audit, S-0086-02 NMDA units calibration, S-0088-01 causal NaP-knockout per cluster
representative). Outputs are one library asset (the generator) and one answer asset
(validation-triplet biological-plausibility synthesis). The validated generator is the substrate for
t0091's joint 68-d (54-d electrophys + 14-d morphology) NSGA-II run. This file surveys the project's
libraries, prior tasks, and answer assets to identify reusable infrastructure for the 7 phases
(A-G).

## Library Landscape

The project contains 16 registered libraries. Five are directly relevant to t0090:

* **`de_rosenroll_2026_dsgc`** (`v0.1.0`, created by `t0024_port_de_rosenroll_2026_dsgc`, categories
  `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `dendritic-computation`). The Bed B reference port. Vendors `RGCmodelGD.hoc` (a 350-section
  hand-coded morphology with `numDends=350` and explicit `connect` statements) under
  `assets/library/de_rosenroll_2026_dsgc/sources/`. Provides `build_dsgc_cell()` returning a
  `DSGCCell` dataclass with `soma`, `all_dends`, `primary_dends`, `non_terminal_dends`,
  `terminal_dends`, `terminal_locs_xy`, and `origin_xy` fields. This is the de facto Bed B input to
  Phase F reproducibility. Import path:
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell.build_dsgc_cell`.
* **`de_rosenroll_2026_dsgc_ais`** (`v0.1.0`, created by `t0078_bedb_mobo_v2_ais_tiered_ahp`,
  categories `compartmental-modeling`, `voltage-gated-channels`, `direction-selectivity`,
  `retinal-ganglion-cell`). The 49-d v2 substrate that adds a two-subsegment AIS (proximal HHst
  basal Na+K, distal Nav1.6 + Kv3 + Kv7) on top of the t0024 cell. Superseded for t0090 by the v3
  substrate, but exposes the fork pattern (`AISExtension` dataclass, `_compute_nseg` d_lambda rule,
  `extend_with_ais()`). Not directly imported.
* **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** (`v0.1.0`, created by
  `t0080_bedb_mobo_v3_dendritic_spike_nsga2`, categories `ais`, `evaluation`). The 54-d v3 substrate
  that t0083 / t0086 / t0088 all use. Provides `ParameterVector` (54-d frozen dataclass with
  `@property` accessors for all 5 dendritic-spike knobs), `BedBV3Problem` pymoo Problem,
  `apply_parameter_vector()`, `evaluate_parameter_vector()`, and `build_dsgc_cell_with_ais()`. This
  is the canonical harness t0090 must call from inside Phase D verification simulations and Phase F
  Bed-B reproducibility. Import paths under
  `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.{constants,apply_params,build_cell_ais, trial_driver}`.
* **`tuning_curve_viz`** (`v0.1.0`, created by `t0011_response_visualization_library`, category
  `direction-selectivity`). Matplotlib library that turns tuning-curve CSVs into Cartesian, polar,
  multi-model overlay, and per-angle raster+PSTH PNGs. `plot_polar_tuning_curve()` and
  `plot_cartesian_tuning_curve()` are the de facto rendering primitives reused across t0024 [t0024],
  t0046, t0080, etc. Phase E side-by-side panels can adopt the Okabe-Ito palette and dashed-target
  overlay style. Import path:
  `tasks.t0011_response_visualization_library.code.tuning_curve_viz.{cartesian,polar,overlay}`.
* **`tuning_curve_loss`** (`v0.1.0`, created by `t0012_tuning_curve_scoring_loss_library`,
  categories `direction-selectivity`, `retinal-ganglion-cell`). Canonical scorer for 12-angle tuning
  curves. Provides `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`,
  `compute_reliability`, and `score()` returning a `ScoreReport` with loss, residuals, and envelope
  pass/fail. Phase D and Phase F both need DSI / PD-rate computation; this library is the canonical
  source. Import path:
  `tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics.{compute_dsi, compute_peak_hz}`.

The other 11 libraries are not relevant: `modeldb_189347_dsgc` and its variants
(`modeldb_189347_dsgc_gabamod`, `modeldb_189347_dsgc_dendritic`, `modeldb_189347_dsgc_exact`) are
the older Poleg-Polsky 2016 lineage superseded by Bed B; `dsgc_active_channel_pack` (t0074) is a Bed
A channel pack not used at Bed B; the `minimal_dsgc_*` family (t0052-t0059) are toy-cell scalar-GABA
/ spatial-GABA / NMDA / mg-block / tonic-GABA / bar-locked sweep libraries on a 3-section reduced
cell. None of those expose morphology-construction primitives that t0090 needs.

## Architecture Overview

The reusable infrastructure stack for t0090 is layered:

* **Bottom**: t0024's `build_dsgc_cell()` instantiates the Bed B HOC template via
  `h.load_file("RGCmodelGD.hoc")` then `h.DSGC(0, 0)`, yielding ~350 sections with hand-coded
  topology. t0090's procedural generator REPLACES this layer -- instead of sourcing a HOC file, the
  generator creates `h.Section()` objects programmatically and connects them via
  `child.connect(parent, 1.0, 0.0)` (the same idiom RGCmodelGD.hoc uses internally).
* **Middle**: t0080's `extend_with_ais()` shows the canonical pattern for adding sections to a
  pre-built cell (`h.Section()` + `Ra/cm/nseg` + `insert("HHst")` + `connect(soma, 1.0, 0.0)`).
  t0090 must use the same idioms when building the procedural arbour. The `_compute_nseg` function
  (d_lambda=0.1 rule at 100 Hz) is the canonical way to set `nseg` for new sections.
* **Top**: t0080's `apply_parameter_vector()` + `trial_driver.evaluate_parameter_vector()` are the
  simulation harness. Both consume a `DSGCCellWithAIS` dataclass (h, soma, all_dends, primary_dends,
  non_terminal_dends, terminal_dends, ais_proximal, ais_distal). t0090 must produce a structurally
  compatible dataclass from the procedural generator so Phase D (8-direction bar protocol) and Phase
  F (Bed-B reproducibility) can call `evaluate_parameter_vector` directly with no harness changes.
* **Side**: t0086's `biological_priors.py` and `biological_scorecard.py` provide the canonical
  9-prior bio-comparison framework (Kole 2008, Werginz 2024, Sivyer 2013, Branco-Hausser 2010, Oesch
  2005, Stuart 1999, plus AIS-to-soma Nav ratio derived prior). Phase G.1 audit and Phase G
  synthesis answer asset reuse this scorecard logic.

## Key Findings

### Bed B Morphology Construction Is HOC-Native, Not Programmatic

The Bed B reference morphology in `RGCmodelGD.hoc` is a hand-coded NEURON template with
`begintemplate DSGC ... endtemplate` semantics. It declares `create soma, dend[350]` and lists 350
explicit `connect` statements between dendrite indices [t0024]. There are no procedural generation
primitives -- the 350 sections are instantiated en bloc and the topology is hard-coded. Section
diameters and lengths come from `pt3dadd` calls embedded in HOC `proc shape3d_1()` / `shape3d_2()`
blocks that t0090 cannot easily reuse for procedural generation. Instead, the generator must build
sections programmatically using Python's NEURON API (`h.Section(name=...)` followed by `section.L`,
`section.diam`, `section.connect(parent, 1.0, 0.0)`, `section.insert(...)`).

The pattern `extend_with_ais.py` in t0080 demonstrates this idiom on a single section pair (ais
proximal + ais distal); the procedural generator extends the same idiom to all dendritic sections.
Section count: t0024's Bed B has 350 dendrite sections + 1 soma = 351 sections, with one AIS pair
(t0080 [t0080]) bringing the total to 353 [t0024]. t0090's procedural generator with
`num_primary_branches=3-7` and `max_strahler_depth=2-6` will produce far fewer sections (estimated
~50-300 depending on knob settings) -- the verification simulation must therefore handle smaller
arbours efficiently.

### t0080's `ParameterVector` Provides the 54-d Substrate; t0090 Must Carry It Through Unchanged

t0080's `ParameterVector` is a frozen 54-d dataclass under `constants.py` (see lines 322-495) with
explicit `ParamIndex` IntEnum positions [t0080]. The 5 v3 dendritic-spike additions are at indices
49-53: `GNMDA_DEND` (log-uniform [1e-5, 1e-2] uS NetCon weight for `Exp2NMDA`), `MG_CONC_MM` (linear
[0.1, 0.5] /mM written to `Exp2NMDA.n`), `VOFF_NMDA` (linear [-10, 10] mV), `NAV16_DEND_DISTAL`
(log-uniform [1e-5, 0.05] S/cm^2), and `NAP_DEND_DISTAL` (log-uniform [1e-5, 0.01] S/cm^2). The 25
tier-stratified densities are at indices 0-24 in channel-major order (Nav1.6, Kv3, NaP, BK, SK) x
(soma, primary, mid, terminal, AIS). `LOWER_BOUNDS` and `UPPER_BOUNDS` arrays expose the per-index
ranges; `LOG_PARAM_INDICES` lists the 39 log-parameter indices. The AIS Nav1.6 lower bound is
hard-pinned at 0.25 S/cm^2 (Kole 2008) and the upper at 5.0 S/cm^2 [t0080].

For Phase F Bed-B reproducibility, t0090 loads 5 t0083 Pareto cells from
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json` (which is the canonical
Pareto archive containing 18 non-dominated cells [t0083]). Each `pareto_front.json` cell has fields
`cell_index`, `generation`, `params` (54-d list[float]), `dsi`, `pd_rate_hz`, `is_unstable`,
`peak_vm_mv`. The same 54-d vector is also stored in `all_evaluations.json` (1728 records across
t0081 + t0083). Phase F passes each 54-d vector through the procedural generator at the Bed-B-
equivalent morph point (no separate normalisation needed: `params` are already in natural units in
the Pareto JSON; only the NSGA-II loop sees normalised values internally).

### v3 Simulation Harness Has a Worker-Cached Cell Pattern That t0090 Must Adapt

`trial_driver.py` in t0080 keeps a per-worker cached cell (`_WORKER_CELL`) and synapse bundle
(`_WORKER_BUNDLE`) so that `evaluate_parameter_vector` only rebuilds the cell once per worker
process and only rebuilds synapses when the parameter hash changes [t0080]. This is critical: NEURON
cell construction takes ~30 s, so caching across the 192 (8 dirs x 20 seeds + 32) trials per
parameter vector saves ~95 percent of total wall-clock time.

For t0090's Phase D verification (60 morphologies x 8 directions x 1 seed = 480 trials), the cache
pattern must be inverted: instead of caching one cell across many parameter vectors, t0090 needs to
cache N morphologies across one fixed parameter vector (the t0083 best cell). The same global
worker-state pattern applies; only the cache key changes. The trial driver's
`try/except RuntimeError` envelope (lines 242-249, returning a `TrialResult` with `error` field) is
the right template for Phase D's per-morphology stability flag.

### Cluster Representatives for Phase G.3 Are Cells 1604, 1634, 767, 1639

t0088 picked these 4 cells as the 4-cluster representatives via closest-to-centroid Euclidean
distance in the 54-d normalised parameter space [t0088]. Their parameter vectors are stored in
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` keyed by `cell_index`.
Each is a 54-d list[float] in NATURAL units (i.e., not normalised by LOWER_BOUNDS / UPPER_BOUNDS).
t0088's `select_representatives.py` shows the canonical loader pattern
(`json.loads (T0083_ALL_EVALUATIONS_JSON.read_text())` then filter on
`cell_index in TARGET_CELL_IDS` -- representatives are recorded in `representative_cells.json` after
Phase A clustering [t0088]). For Phase G.3, t0090 must reload each representative cell's 54-d
vector, set `params[NAP_DEND_DISTAL] = 0`, then re-run the 16-direction Vm-trace deepdive (driver
pattern from `run_deepdive.py`).

### t0088's 16-Direction Vm-Trace Deepdive Is Phase G.3's Direct Template

`run_deepdive.py` in t0088 runs `ANGLES_16DIR_DEG = (0, 22.5, 45, ..., 337.5)` for each
representative cell, recording soma + distal-dendrite Vm and per-channel `i_nav16_ma_cm2`,
`i_nap_ma_cm2`, `g_nmda_us` traces [t0088]. Output is one `.npz` per (cell, direction) saved as
`cell{cell_id}_dir{direction_int_tenths}_traces.npz` (where the direction is encoded as tenths of a
degree, e.g. `cell767_dir1800_traces.npz` for 180 deg). For Phase G.3, t0090 calls the same driver
with 4 cells x 16 directions = 64 simulations after `nap_dend_distal=0` is forced; the attribution
metric (PD-minus-ND integrated current per channel, normalised by total) is then recomputed via
`attribution_metric.compute_attribution()`. The expected falsifiable outcome: if NaP is causally
responsible, knocking it out collapses DSI to <0.2 in all 4 cells; if NMDA + Nav1.6
+ GABA also contribute, DSI is partially preserved.

### t0086's Biological Scorecard Is Reusable for Phase G.1 and Phase G Synthesis

t0086's `biological_scorecard.py` computes deviation = (centroid_value - mean) / sigma per (cluster,
prior) pair and assigns verdicts plausible (|d|<=2), stretched (2<|d|<=5), or exotic (|d|>5)
[t0086]. The 9 priors include the AIS-to-soma Nav ratio (Werginz 2024 mean=17.3, sigma=3), Kole 2008
AIS Nav (mean=0.375 +/- 0.125), Sivyer 2013 NMDA (mean=1e-4, sigma=5e-5), and Branco-Hausser 2010
NMDA voff (mean=0, sigma=5). For Phase G.1 (audit cluster-1 ratio of 116), the key checks are: (a)
`centroid_unnormalised[NAV16_AIS_GBAR] / centroid_unnormalised[NAV16_SOMA_GBAR]` in matching units
(S/cm^2 / S/cm^2 = dimensionless), (b) soma Nav lower bound is not pinning the denominator -- if
`LOWER_BOUNDS[NAV16_SOMA_GBAR] = 1e-5` and the centroid hits that floor, the ratio inflates to 1e3+
artifactually, (c) per-cell ratios (cells 1304, 1504, 1624, 1634) versus centroid average (the
centroid may average across heterogeneous values). Phase G.1 reads `recluster_centroids.json`
[t0088] (or equivalently t0086's `cluster_centroids.json`) and the 13-cell-wise breakdown from the
all_evaluations + representative_cells JSONs.

### Cable Theory and Electrotonic Length Constrain the Rall Exponent Knob

t0041 demonstrated that the t0034 distal-length sweep and the t0035 distal-diameter sweep COLLAPSE
onto a single DSI-vs-L/lambda curve under Rall's cable theory [t0041]. This is the canonical project
finding that morphology, when reduced to electrotonic length L/lambda, is 1-dimensional in DSI
space. The implication for t0090 is that the 14 knobs over-parameterise the DSI-relevant morphology
space; many knob combinations will lie on the same L/lambda contour and produce identical DSI. The
Phase E PCA panel should reveal this: parameter-space diversity (high 14-d variance) does NOT
guarantee electrotonic-space diversity. The diversity test must therefore also report total
dendritic length (um), max electrotonic length (max-L/lambda integrated path), and Strahler depth as
morphometric features -- not just the 14 raw knobs.

### Existing One-Axis Morphology Sensitivity Tests Inform Knob Ranges

t0034 swept distal-dendrite length 50-300 um on the t0024 Bed B cell and found DSI varied
non-monotonically (peaks at intermediate lengths) [t0034]. t0035 swept distal-dendrite diameter
0.1-2.0 um and found a similar non-monotonic profile [t0035]. t0009 calibrated dendritic diameters
to ~0.5 um typical, ~0.125 um placeholder upper [t0009]. These three tasks anchor the geometry
ranges in t0090's task description: `mean_segment_length_um=10-60` is conservative versus t0034's
50-300 range (t0024's mean segment length is ~30 um per de Rosenroll 2026 morphometric data); the
proposed `branch_prob_per_um=0.005-0.05` aligns with t0024's Sholl-like density. The
`rall_exponent =0.5-2.0` knob is wider than the canonical Rall's law exponent 1.5, but this is
intentional -- many real neurons depart from the strict 3/2 power law.

## Reusable Code and Assets

### Library Imports (cross-task)

* **`from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`**
  -- import via library `de_rosenroll_2026_dsgc`. Required for Phase F to load the reference Bed B
  morphology and compare DSI against. The `DSGCCell` dataclass exposes `terminal_locs_xy`,
  `origin_xy`, `primary_dends`, `non_terminal_dends`, `terminal_dends` -- Phase F uses these to
  compute Bed B morphometric features. Source:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` (333 lines).
* **`from tasks.t0024_port_de_rosenroll_2026_dsgc.code import constants as C24`** -- import via
  library `de_rosenroll_2026_dsgc`. Provides `RA_OHM_CM=100.0`, `CM_UF_CM2=1.0`,
  `GLEAK_S_CM2=0.0001667`, `ELEAK_MV=-60.0`, `CELSIUS_DEG_C=36.9`, `DT_MS=0.1`, `STEPS_PER_MS=10.0`.
  The Bed-B-equivalent base point in Phase C must reuse these passive defaults so Phase F's
  reproducibility check is fair.
* **`from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParameterVector, ParamIndex, LOWER_BOUNDS, UPPER_BOUNDS, N_PARAMS, Tier`**
  -- import via library `de_rosenroll_2026_dsgc_ais_dendritic_spike`. Required for Phase D
  (verification simulation using default t0083 best-cell channels) and Phase F (5-cell
  reproducibility) and Phase G.3 (NaP-knockout). Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py` (547 lines).
* **`from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import apply_parameter_vector, ensure_t80_dll_loaded`**
  -- import via library `de_rosenroll_2026_dsgc_ais_dendritic_spike`. Writes the 54-d parameter
  vector to a cell with AIS, including all 25 tier densities, 7 uniform densities, slow-AHP,
  synaptic placement, AIS geometry, and 5 v3 dendritic-spike knobs. Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/apply_params.py` (228 lines).
* **`from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import evaluate_parameter_vector, EvalResult, _worker_run_trial`**
  -- import via library `de_rosenroll_2026_dsgc_ais_dendritic_spike`. The simulation harness API.
  Returns DSI, PD firing rate Hz, stability flag. t0090 wraps this in a per-morphology adapter.
  Signatures:
  `evaluate_parameter_vector(params: ParameterVector, *, n_seeds: int = 20) -> EvalResult` and
  `EvalResult(dsi: float, pd_rate_hz: float, n_trials: int, n_errors: int, elapsed_s: float, is_unstable: bool, peak_vm_mv: float)`.
  Source: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/trial_driver.py` (427 lines).
* **`from tasks.t0011_response_visualization_library.code.tuning_curve_viz import plot_polar_tuning_curve, plot_cartesian_tuning_curve`**
  -- import via library `tuning_curve_viz`. Phase E side panels overlay 30+30 morphologies; reuse
  the Okabe-Ito palette and dashed-target style for consistency with t0024 / t0046 / t0080 plots.
  Source: `tasks/t0011_response_visualization_library/code/tuning_curve_viz/{cartesian,polar}.py`.
* **`from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg`**
  -- import via library `tuning_curve_loss`. The DSI / peak / null formulas are the canonical
  project definitions; Phase D and Phase F use them on the 8-direction protocol output. Signature:
  `compute_dsi(rates: NDArray) -> float` returning `(peak - null) / (peak + null)` with 0.0 fallback
  on zero-sum denominator. Source:
  `tasks/t0012_tuning_curve_scoring_loss_library/code/tuning_curve_loss/metrics.py`.

### Code to Copy Into Task

* **`extend_with_ais._compute_nseg(*, h, section)` (~12 lines)** -- copy into task. The d_lambda
  rule at 100 Hz: `nseg = max(1, int(section.L / (0.1 * lambda_f(100, sec=section))) / 2 * 2 + 1)`.
  t0090's procedural generator must call this on every newly created `h.Section()` to ensure
  cable-faithful spatial discretisation. Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/extend_with_ais.py` lines 46-56. Adapt by
  importing `AIS_LAMBDA_F_FREQ_HZ=100.0` and `AIS_D_LAMBDA=0.1` constants from t0080.constants
  (already importable via the library).
* **t0088 `select_representatives._load_cell_entries()` pattern (~40 lines)** -- copy into task.
  Demonstrates loading the canonical t0083 Pareto archive:
  `json.loads( T0083_ALL_EVALUATIONS_JSON.read_text())` -> filter by `cell_index in TARGET_CELL_IDS`
  -> build `CellEntry` with `params: list[float]`. Phase F adapts this to load 5 random Pareto cells
  from `pareto_front.json`; Phase G.3 reuses it verbatim for cells 1604, 1634, 767, 1639. Source:
  `tasks/t0088_recluster_marginals_and_vm_motifs/code/select_representatives.py` lines 85-122.
* **t0088 `run_deepdive.py` 16-direction driver loop (~80 lines)** -- copy into task. The
  `for cell in representative_cells: for direction in ANGLES_16DIR_DEG: simulate -> save .npz`
  pattern is exactly Phase G.3's structure. Adapt by adding the `nap_dend_distal=0` override before
  `apply_parameter_vector()` call. Source:
  `tasks/t0088_recluster_marginals_and_vm_motifs/code/run_deepdive.py` lines 70-180.
* **t0088 `attribution_metric.compute_attribution()` (~40 lines)** -- copy into task. Computes
  PD-minus-ND integrated current per channel and the fractional contribution. Phase G.3 reruns this
  on the NaP-knockout traces to confirm DSI collapse correlates with NMDA / Nav1.6 attribution
  redistribution. Source: `tasks/t0088_recluster_marginals_and_vm_motifs/code/attribution_metric.py`
  lines 56-130.
* **t0086 `biological_scorecard._verdict()` and `_centroid_value()` (~30 lines)** -- copy into task.
  Phase G.1 audit calls `_centroid_value(centroid_unnormalised, param_index=-1)` for the AIS-to-soma
  Nav ratio (the `param_index=-1` sentinel triggers ratio computation). Phase G synthesis answer
  asset re-runs the full scorecard logic on the recomputed (NMDA-recalibrated) cluster centroids.
  Source: `tasks/t0086_robustness_cluster_bio_comparison/code/biological_scorecard.py` lines 41-68.
  Adapt by also copying the `BIOLOGICAL_PRIORS` list from `biological_priors.py` lines 44-180 (or
  better: read `tasks/t0086.../results/data/biological_priors.json` directly).
* **NEURON `h.Section()` programmatic construction idiom (~20 lines)** -- copy into task. From
  `extend_with_ais.extend_with_ais()` lines 80-103: `sec = h.Section(name=...)`, `sec.L = ...`,
  `sec.diam = ...`, `sec.Ra = ...`, `sec.cm = ...`, `sec.nseg = _compute_nseg(...)`,
  `sec.insert("HHst")`, `sec.connect(parent, 1.0, 0.0)`. The procedural generator's main loop
  follows this pattern recursively for each Strahler-depth level. Source:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/extend_with_ais.py` lines 80-103.

## Common Patterns

### Path Centralisation in `paths.py`

Every relevant prior task ([t0024], [t0080], [t0083], [t0086], [t0088]) defines a `paths.py` with
all output paths as module-level constants and an `ensure_directories()` helper. t0090 must follow
the same pattern. Cross-task input paths are constructed via
`REPO_ROOT / "tasks" / "t0083_bedb_v3_extend_nsga2_gen8plus" / "results" / "data" / "all_evaluations.json"`
-- never `Path("../t0083_.../...")`.

### Frozen Dataclasses for All Structured Data

`@dataclass(frozen=True, slots=True)` is the canonical structured-data idiom across the project
(`ParameterVector` [t0080], `CellEvaluation` [t0080], `CellEntry` [t0088], `DirectionResult`
[t0088], `AttributionResult` [t0088], `BiologicalPrior` [t0086], `DSGCCell` [t0024]). t0090's
`MorphologyParams` (14 knobs + seed) and `MorphologyResult` (sections, connectivity, morphometric
features) follow the same idiom.

### Parameter Vector Loading Pattern

The canonical pattern across [t0086] and [t0088] is:
`raw_evals = json.loads( T0083_ALL_EVALUATIONS_JSON.read_text(encoding="utf-8"))` then iterate over
records picking up `record["cell_index"]` and `record["params"]` (54-d list[float]). t0090's Phase F
(5 random Pareto cells) and Phase G.3 (cells 1604, 1634, 767, 1639) both use this pattern.

### NEURON DLL Loading via `ensure_t80_dll_loaded`

t0080's `apply_params.ensure_t80_dll_loaded()` (lines 45-53) is the canonical idempotent DLL loader
for the 13 t80 MOD mechanisms. Worker processes call it once per process; subsequent calls no-op.
t0090 must call this before any `h.Section().insert("nav16t80")` to avoid the silent "mechanism not
found" failure mode that bites cross-process NEURON code.

## Lessons Learned

* **The Bed-B 5 percent reproducibility criterion is too tight given known cell-to-cell DSI
  variability**: t0083's 18 Pareto-front cells have DSI spanning 0.42 to 0.86; even with identical
  parameter vectors, AR(2) noise injection across 20 seeds produces DSI variability of ~5 percent
  trial-to-trial [t0083]. Phase F should relax to 10 percent (per `research_internet.md` Gap 5
  finding) and document the choice.
* **Worker-process caching is essential for NEURON throughput**: t0080's `_WORKER_CELL` /
  `_WORKER_BUNDLE` global pattern saved ~95 percent of cell-build time (~30 s per build x 192 trials
  = ~96 minutes per parameter vector reduced to ~30 s) [t0080]. Phase D MUST adopt this pattern;
  otherwise 60 morphologies x 8 directions on 64 cores will blow past the 5-10 minute wall-clock
  estimate.
* **Channel mechanism non-finite values cause silent test failures**: t0080's trial driver wraps
  each `h.run()` in a try/except for `RuntimeError`, `ValueError`, `ArithmeticError` and returns a
  `WORST_CASE_DSI=-1.0` sentinel on failure (lines 242-249) [t0080]. t0090's Phase D verification
  must use the same pattern; some morphology knob combinations (e.g.,
  `branch_density_gradient_pd=+1` with `field_elongation_pd=3.0`) will produce arbours where the
  default t0083 channel densities cause depolarisation block, NaN voltages, or numerical divergence
  -- all expected per Mainen 1996's morphology-determines-firing-pattern finding (see
  research_papers.md).
* **Morphological diversity does not guarantee functional diversity**: t0041's electrotonic collapse
  finding [t0041] proves that many distinct (length, diameter) combinations produce identical DSI
  when reduced to L/lambda. Phase E PCA must include electrotonic length and total dendritic length
  as morphometric features, not just the 14 raw knobs, to detect this collapse in the diversity
  test.
* **The t0024 HOC template is a fork barrier**: t0024's `build_dsgc_cell()` requires sourcing
  `RGCmodelGD.hoc` from the library asset's `sources/` directory and instantiating `h.DSGC(0, 0)`
  [t0024]. t0090's procedural generator cannot reuse this -- it must build sections programmatically
  in pure Python. Phase F's reproducibility is therefore not an apples-to-apples test (the
  procedural cell will be a structurally different object even at the Bed-B-equivalent point).
* **NMDA exotic verdict in t0086 likely reflects a units mismatch**: t0086 reported the cluster-NMDA
  Sivyer 2013 verdict at >=85 sigma -- so extreme it is more parsimonious to suspect a per-spine vs
  per-NetCon-weight unit mismatch [t0086]. Phase G.2 calibration is the right intervention: the
  t0080 `gnmda_dend` is a NetCon weight in uS, while Sivyer's 0.1 nS is a per-spine voltage-clamp
  measurement; the calibration ablation maps NetCon weight to per-spine conductance via NEURON state
  recording during a single trial.
* **Cluster centroids can be misleading on heterogeneous cells**: t0088 noted that the 4-cluster
  centroid AIS-to-soma Nav ratio of 116x [t0088] may be averaging across heterogeneous cells with
  individual ratios both below and above 116. Phase G.1 must check per-cell ratios (cells 1304,
  1504, 1624, 1634) against the centroid before declaring it the most extreme prior violation.
* **Use aggregators, not file-system walks**: per CLAUDE.md rule 9, t0090 must call
  `aggregate_libraries`, `aggregate_answers`, `aggregate_tasks` for cross-task discovery.
  Aggregators apply corrections overlays; raw `find tasks/` walks miss them. (Note: this project has
  aggregator scripts only for `categories`, `costs`, `machines`, `metric_results`, `metrics`,
  `suggestions`, `task_types`, `tasks`; `aggregate_libraries` and `aggregate_answers` were not yet
  found in `arf/scripts/aggregators/` and were enumerated via `Glob` on
  `tasks/*/assets/library/*/details.json` and `tasks/*/assets/answer/*/details.json` for this
  research stage.)

## Recommendations for This Task

1. **Build `code/morphology_generator.py` as the procedural generator** -- pure Python NEURON,
   following the t0080 `extend_with_ais` idiom. Use `h.Section(name=f"dend_{i}")`, set L / diam / Ra
   / cm / nseg via the d_lambda rule (copy `_compute_nseg` from t0080), call
   `child.connect(parent, 1.0, 0.0)`. Return a dataclass-compatible `MorphologyResult` with `soma`,
   `all_dends`, `primary_dends`, `non_terminal_dends`, `terminal_dends`, `terminal_locs_xy`,
   `origin_xy`, `ais_proximal`, `ais_distal` fields so that `apply_parameter_vector` consumes it
   without modification.

2. **Make `MorphologyResult` structurally compatible with `DSGCCellWithAIS`** -- keep the same field
   names so `apply_params.apply_parameter_vector(cell=morph_result, params=p)` Just Works. The
   procedural cell and the t0024 reference cell then share the same channel-write code path.

3. **Use `ProcessPoolExecutor` with the `_WORKER_CELL` global cache pattern for Phase D** -- t0080's
   pattern in `trial_driver._worker_prepare()` is the template. Cache one MorphologyResult per
   worker, evaluate 8 directions per worker, return per-direction `TrialResult`. 60 morphologies x 8
   directions / 64 cores = ~7-8 trials per worker, each ~10 s = ~80 s total wall clock -- well
   within the 5-10 minute budget.

4. **Phase F: load 5 random t0083 Pareto cells** -- read
   `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`, take 5 with
   deterministic seed (e.g., `np.random.default_rng(0).choice(18, size=5, replace=False)`), build
   the procedural cell at the Bed-B-equivalent morph point, apply each cell's 54-d vector, run the
   8-direction protocol, compare DSI / PD-rate to the original Pareto values. Relax the pass
   criterion to 10 percent (per research_internet.md Gap 5 finding).

5. **Phase G.1: data-only audit in `code/audit_ais_soma_nav_ratio.py`** -- read
   `tasks/t0088.../results/data/recluster_centroids.json` (or t0086's equivalent), extract
   `centroid_unnormalised[NAV16_AIS_GBAR]` and `[NAV16_SOMA_GBAR]` per cluster, compute ratio per
   cluster, then per-cell using the 4 cluster-1 cell IDs (1304, 1504, 1624, 1634) loaded from t0083
   `all_evaluations.json`. Check whether `LOWER_BOUNDS[NAV16_SOMA_GBAR]=1e-5` is being hit by any of
   those 4 cells (if so, the ratio is a floor artefact, not a biological signal).

6. **Phase G.2: NMDA calibration ablation in `code/calibrate_nmda_units.py`** -- pick one t0080
   cell, sweep `gnmda_dend` from 1e-5 to 1e-2 uS in 6 log-spaced steps, run a single
   correlated-rho=0.6 trial at PD direction, record per-spine `i_nmda(t)` from the NEURON state via
   `seg.i_nmda` reference (or by recording `g_nmda_us * (v - e_nmda)`), integrate to compute
   per-spine effective open conductance, and produce a calibration curve. Then re-score t0086 /
   t0088 clusters against Sivyer 2013 in the corrected units.

7. **Phase G.3: causal NaP-knockout in `code/run_nap_knockout.py`** -- copy t0088's
   `run_deepdive.py` driver, hardcode `params[NAP_DEND_DISTAL] = 0.0` before
   `apply_parameter_vector()`, run cells 1604 / 1634 / 767 / 1639 at 16 directions on local CPU.
   Reuse `attribution_metric.compute_attribution()` to confirm the post-knockout NMDA + Nav1.6
   attribution shifts predicted by t0088.

8. **Reuse `tuning_curve_loss.compute_dsi` and `compute_peak_hz`** -- do NOT reimplement these. The
   library is the canonical project source.

9. **Visualisation in Phase E** -- use `plot_polar_tuning_curve` only for the Phase F
   reproducibility-comparison sanity panels; for the dendrogram grid (5x6 panel of 30 morphologies)
   and morphometric PCA, write task-local matplotlib code (the existing tuning_curve_viz library
   does NOT include dendrogram primitives). Match the Okabe-Ito palette of t0011 for consistency.

10. **Document the d_lambda nseg rule explicitly** -- in plan.md, state that every section receives
    `nseg = max(1, int(L / (0.1 * lambda_f(100, sec=sec))) / 2 * 2 + 1)` per [t0080]
    `extend_with_ais._compute_nseg`. This is non-trivial because procedural generation can produce
    arbitrarily long sections; without the rule, simulations diverge.

11. **Use frozen-dataclass pattern for all 14 MorphologyParams + MorphologyResult containers** --
    aligns with the project-wide convention used by [t0080] `ParameterVector`, [t0088] `CellEntry`,
    [t0024] `DSGCCell`. mypy / ruff will not complain.

12. **Match the project's `verify_research_code` requirements exactly** -- this file already follows
    the spec (frontmatter, 7 mandatory sections, by-topic Key Findings, Reusable Code with explicit
    "import via library" / "copy into task" labels, citations for every [tXXXX] in Task Index). Run
    the verificator wrapped in `run_with_logs.py` after writing.

## Task Index

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Provides the literature-derived diameter taper for the t0005 baseline (placeholder
  0.125 um -> calibrated). Anchors t0090's `mean_segment_length_um` and Rall-tapering knob ranges.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Created the `tuning_curve_viz` library reused for Phase F polar / Cartesian
  reproducibility-comparison panels; sets the Okabe-Ito palette convention for Phase E plots.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Provides the canonical `compute_dsi` / `compute_peak_hz` / `compute_null_hz` /
  `compute_hwhm_deg` implementations used in Phase D and Phase F.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Direct dependency. Provides the Bed B reference morphology (350-section HOC
  template), the `build_dsgc_cell()` builder, and the canonical passive constants
  (`RA_OHM_CM=100.0`, `CM_UF_CM2=1.0`, `GLEAK_S_CM2=0.0001667`). Phase F reproducibility is measured
  against this port.

### [t0027]

* **Task ID**: `t0027_literature_survey_morphology_ds_modeling`
* **Name**: Literature survey: modeling effect of cell morphology on direction selectivity
* **Status**: completed
* **Relevance**: Produced the morphology-DS-modeling synthesis answer (~20 papers cited) that
  motivates t0090's 14 knobs. Validates the asymmetry knobs (soma offset, field elongation) as
  literature-anchored.

### [t0034]

* **Task ID**: `t0034_distal_dendrite_length_sweep_t0024`
* **Name**: Distal-dendrite length sweep on t0024 DSGC
* **Status**: completed
* **Relevance**: One-axis morphology sensitivity test on the Bed B port. Anchors t0090's
  `mean_segment_length_um` knob range; precedent for Phase D's per-morphology DSI evaluation.

### [t0035]

* **Task ID**: `t0035_distal_dendrite_diameter_sweep_t0024`
* **Name**: Distal-dendrite diameter sweep on t0024 DSGC
* **Status**: completed
* **Relevance**: One-axis morphology sensitivity test. Anchors t0090's Rall-exponent / soma-
  diameter knob ranges.

### [t0041]

* **Task ID**: `t0041_electrotonic_length_collapse_t0034_t0035`
* **Name**: Electrotonic-length collapse analysis of t0034 and t0035
* **Status**: completed
* **Relevance**: Demonstrates that t0034 + t0035 collapse onto a single L/lambda DSI curve -- the
  canonical project finding that DSI-relevant morphology is 1-d in cable-theory units. Critical for
  Phase E PCA design.

### [t0078]

* **Task ID**: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* **Name**: Bed B v2 MOBO with AIS, tier-stratified channels, slow Kv-AHP
* **Status**: completed
* **Relevance**: Direct dependency. Created the AIS-extension pattern (`extend_with_ais()`, d_lambda
  nseg rule) that t0090's procedural generator copies for AIS attachment. The 49-d v2 precursor to
  the 54-d v3 substrate.

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B MOBO v3 with dendritic-spike machinery
* **Status**: completed
* **Relevance**: Direct dependency. Created the v3 54-d substrate library used by Phase D / F / G.3.
  Provides `ParameterVector`, `apply_parameter_vector`, `evaluate_parameter_vector`,
  `build_dsgc_cell_with_ais` -- the canonical simulation harness t0090 calls.

### [t0081]

* **Task ID**: `t0081_bedb_v3_warmstart_nsga2`
* **Name**: Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start
* **Status**: completed
* **Relevance**: Direct dependency. Produced cell 767 (the first joint-pass cell) and the gen-7
  population reloaded by t0083. Cell 767 is one of t0088's 4 cluster representatives; Phase G.3
  knocks out NaP on it.

### [t0083]

* **Task ID**: `t0083_bedb_v3_extend_nsga2_gen8plus`
* **Name**: Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau stop
* **Status**: completed
* **Relevance**: Direct dependency. Produced 1728 evaluations, 18 Pareto cells, and the
  authoritative `pareto_front.json` + `all_evaluations.json` consumed by Phase F (5 random Pareto
  cells) and Phase G.3 (cluster representatives).

### [t0086]

* **Task ID**: `t0086_robustness_cluster_bio_comparison`
* **Name**: Robustness + cluster + bio-comparison of t0081/t0083 joint-pass cells
* **Status**: completed
* **Relevance**: Direct dependency. Created `biological_priors.py` and `biological_scorecard.py`
  (the 9-prior bio-comparison framework) consumed by Phase G.1, G.2, G synthesis. Reported the
  cluster-NMDA exotic verdict (>=85 sigma) that motivates Phase G.2.

### [t0088]

* **Task ID**: `t0088_recluster_marginals_and_vm_motifs`
* **Name**: Re-cluster t0086 13 cells and per-cluster Vm-trace deep-dive
* **Status**: completed
* **Relevance**: Direct dependency. Produced the 4 cluster representatives (1604, 1634, 767, 1639)
  used by Phase G.3, the 16-direction Vm-deepdive driver template, and the
  `attribution_metric.compute_attribution()` PD-minus-ND fractional-channel-contribution metric.
  Reported the cluster-1 AIS-to-soma Nav ratio of 116x that motivates Phase G.1.
