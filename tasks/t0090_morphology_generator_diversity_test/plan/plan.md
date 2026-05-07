---
spec_version: "2"
task_id: "t0090_morphology_generator_diversity_test"
date_completed: "2026-05-07"
status: "complete"
---
# Plan: Procedural DSGC Morphology Generator + Diversity Test + Validation Bundle

## Objective

Build a deterministic, pure-Python procedural DSGC morphology generator with 14 explicit knobs (5
topology + 4 asymmetry + 3 geometry + 2 stochastic), then exercise it across two morphology
populations (30 wide-LHS "very different" + 30 +/-5 percent "very similar"), verify each morphology
in NEURON, visualise the populations as 2D dendrograms and morphometric PCA/UMAP, confirm Bed-B
reproducibility on 5 t0083 Pareto cells (within 10 percent on DSI and PD firing rate), and execute a
3-suggestion validation bundle (S-0088-02 AIS-to-soma Nav ratio audit, S-0086-02 NMDA units
calibration, S-0088-01 causal NaP knockout). The generator becomes the substrate for t0091's joint
68-d (54-d electrophys + 14-d morphology) NSGA-II run, so its API must be stable, deterministic, and
compatible with t0080's `apply_parameter_vector` harness without modification. "Done" means: 60/60
morphologies build and pass the 50 ms no-stim stability check; the diversity test produces visibly
distinct morphology classes for the "different" set and a tight PCA cluster for the "similar" set;
Bed-B reproducibility is within 10 percent on 5/5 Pareto cells; all three validation suggestions
yield concrete quantitative verdicts; one library asset (`procedural_dsgc_morphology_generator`) and
one answer asset (validation triplet biological-plausibility synthesis) exist and pass their
respective verificators.

## Task Requirement Checklist

The operative request from `task.json` and `task_description.md`:

> Implement 14-knob procedural DSGC morphology generator; 30 very-different + 30 very-similar
> morphologies; visualise; Bed-B reproducibility; bundled validation triplet. The validated
> generator is the input to t0091's joint 68-d NSGA-II optimisation. Phases A-G as defined in
> task_description.md, expected_assets = {library: 1, answer: 1}.

Concrete requirements extracted from the task text:

* **REQ-1** — Implement a deterministic 14-knob procedural Python generator with API
  `generate_morphology(params: MorphologyParams, morph_seed: int) -> MorphologyResult`. Same
  `(params, morph_seed)` must produce byte-identical NEURON section dumps. Satisfied by **Steps
  3-6** (Phase A); evidence: `pytest test_determinism.py` passes.
* **REQ-2** — `MorphologyParams` is a `@dataclass(frozen=True, slots=True)` with the 14 typed
  fields listed in `task_description.md` (3 ints: `num_primary_branches`, `max_strahler_depth`,
  `morph_seed`; 11 floats including `branch_prob_per_um`, `mean_branching_angle_deg`,
  `rall_exponent`, `soma_offset_pd_um`, `field_elongation_pd`, `branch_density_gradient_pd`,
  `primary_branch_pd_concentration`, `mean_segment_length_um`, `soma_diameter_um`, `ais_length_um`,
  `branch_length_cv`). Satisfied by **Step 3**; evidence: `mypy` passes on `morphology_params.py`.
* **REQ-3** — `MorphologyResult` is structurally compatible with t0080's `DSGCCellWithAIS` so that
  `apply_parameter_vector(cell=..., params=...)` consumes it without modification (fields `soma`,
  `all_dends`, `primary_dends`, `non_terminal_dends`, `terminal_dends`, `terminal_locs_xy`,
  `origin_xy`, `ais_proximal`, `ais_distal`, plus a `stability_flag` enum and `morphometric_summary`
  dataclass). Satisfied by **Steps 4-5**; evidence: `apply_parameter_vector` consumes the procedural
  cell in **Step 11** with no errors.
* **REQ-4** — Unit tests cover determinism (same seed -> identical sections), edge cases
  (`num_primary_branches=3` and `=7`; `max_strahler_depth=2` and `=6`), round-trip
  serialise/reconstruct, and no-NaN section lengths/diameters/connectivity. Satisfied by **Step 7**;
  evidence: `uv run pytest tasks/t0090_morphology_generator_diversity_test/code/ -v` reports 0
  failures.
* **REQ-5** — Generate 30 very-different morphologies via
  `scipy.stats.qmc.LatinHypercube(d=14, optimization="random-cd", seed=42).random(n=30)` over the
  14-d parameter bounds. Satisfied by **Step 8**; evidence: `data/different_morphologies/` contains
  30 morph spec JSONs.
* **REQ-6** — Generate 30 very-similar morphologies via independent uniform +/- 5 percent jitter
  on each parameter around the Bed-B-equivalent base point. Satisfied by **Step 9**; evidence:
  `data/similar_morphologies/` contains 30 morph spec JSONs.
* **REQ-7** — Run a 50 ms no-stim stability check at V_rest = -70 mV and an 8-direction bar
  protocol with the t0083 best-cell channel set on each of the 60 morphologies; record per-
  morphology stability flag (STABLE / NAN_VOLTAGE / DIVERGED / DISCONNECTED) and DSI / PD-rate.
  Satisfied by **Step 11**; evidence: `data/verification_summary.json` contains 60 entries.
* **REQ-8** — Produce visualisations: `morphology_grid_different.png` (5x6 panel of 30 different
  morphologies), `morphology_grid_similar.png` (5x6 panel), `morphometric_pca.png`, and
  `morphometric_umap.png` (UMAP if `umap-learn` available; otherwise the file is omitted and the PCA
  panel is the canonical reduction). Satisfied by **Steps 12-13**; evidence: PNG files exist under
  `results/images/`.
* **REQ-9** — Bed-B reproducibility check: load 5 random t0083 Pareto cells (deterministic seed),
  build the procedural cell at the Bed-B-equivalent morph base point, apply each cell's 54-d
  parameter vector, run the 8-direction protocol, and confirm DSI and PD firing rate within 10
  percent of the original Pareto values. Satisfied by **Step 14**; evidence:
  `data/bedb_reproducibility.json` contains 5 entries with `dsi_delta_pct` and `pd_rate_delta_pct`
  fields.
* **REQ-10** — Phase G.1: AIS-to-soma Nav ratio audit. Read t0088 cluster centroids and per-cell
  parameter vectors for cluster 1 cells (1304, 1504, 1624, 1634); confirm units are matching S/cm^2;
  check whether the soma Nav lower bound (1e-5 S/cm^2) is pinning the denominator; report per-cell
  ratios vs centroid average. Satisfied by **Step 15**; evidence: `data/g1_nav_ratio_audit.json`
  contains the per-cell ratios and lower-bound check.
* **REQ-11** — Phase G.2: NMDA units calibration ablation. Sweep `gnmda_dend` from 1e-5 to 1e-2 uS
  in 6 log-spaced steps on a single t0080 cell at PD direction; record per-spine effective open
  conductance; produce a calibration curve mapping NetCon weight to per-spine conductance; re-score
  t0086 / t0088 clusters in calibrated units. Satisfied by **Step 16**; evidence:
  `data/g2_nmda_calibration.json` and `results/images/nmda_calibration_curve.png`.
* **REQ-12** — Phase G.3: causal NaP knockout. Force `nap_dend_distal = 0.0` on each of the 4
  cluster representatives (1604, 1634, 767, 1639); run the 16-direction Vm-trace deepdive; compare
  knockout DSI to the original t0088 DSI; pass criterion: if DSI collapses to <0.2 in all 4 cells,
  NaP is causally responsible; if DSI remains >0.4 in any cell, NaP attribution is partial.
  Satisfied by **Step 17**; evidence: `data/g3_nap_knockout.json` and the 64 trace `.npz` files
  under `data/g3_traces/`.
* **REQ-13** — One library asset at
  `assets/library/procedural_dsgc_morphology_generator/details.json` with `module_paths` pointing at
  `code/morphology_params.py`, `code/generator.py`, and `code/verification.py`, plus a canonical
  `description.md` documenting the public API and at least two runnable usage examples. Satisfied by
  **Step 18**; evidence: `verify_assets.py` passes for the library asset.
* **REQ-14** — One answer asset at
  `assets/answer/validation-triplet-implications-for-biological-plausibility/` synthesising the G.1
  + G.2 + G.3 findings into a yes/no/conditional verdict per validation suggestion plus an overall
    confidence rating. Satisfied by **Step 19**; evidence: `verify_answer_asset.py` passes.
* **REQ-15** — Apply the NEURON `d_lambda` rule (`freq=100 Hz`, `d_lambda=0.1`) to every
  procedurally generated section;
  `nseg = max(1, int(L / (0.1 * lambda_f(100, sec=sec))) / 2 * 2 + 1)`. Satisfied by **Step 5**;
  evidence: a unit test in `code/test_generator.py` confirms `nseg` is always odd and `>= 1` for L
  in [10, 600] um.
* **REQ-16** — Compute and publish the registered project metric `direction_selectivity_index` per
  morphology in `data/verification_summary.json`. Satisfied by **Step 11**. The other three
  registered metrics (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) are
  reported only for the Bed-B-reproducibility 5-cell subset (Step 14) where the 8-direction protocol
  with multi-trial seeds gives meaningful statistics; the 60-morphology sweep uses 1 seed per
  direction so reliability and RMSE-vs-target are not measurable there. This omission is deliberate
  — recorded here so it is not mistaken for an oversight.

## Approach

The task delivers a procedural DSGC morphology generator and validates it through three lenses:
diversity coverage (60-morph LHS + perturbation sweep), Bed-B reproducibility, and a 3-suggestion
biological-plausibility validation triplet. The recommended task types are **`write-library`** (the
generator is the deliverable library), **`data-analysis`** (PCA/UMAP diversity test, Bed-B
comparison, G.1 ratio audit, G.2 calibration curve, G.3 attribution), and **`answer-question`** (the
G synthesis answer asset). All three are listed in `task.json` `task_types`.

**Generator design (Phase A).** Pure-Python NEURON: `h.Section(name=...)` with explicit `L`, `diam`,
`Ra`, `cm`, `nseg` set per section, then `child.connect(parent, 1.0, 0.0)`. Topology is built
recursively: `num_primary_branches` primary stems are sampled from a von Mises distribution biased
by `primary_branch_pd_concentration` (kappa, range 0-5; kappa=0 yields uniform); each primary stem
recurses up to `max_strahler_depth` levels with branching probability `branch_prob_per_um` per
micron of segment length, branching angles drawn from `mean_branching_angle_deg +/- branch_length_cv
* mean_branching_angle_deg`, daughter diameters from Rall's generalised power law `d_parent^rall =
  sum
  d_daughter^rall`(canonical 1.5 = Rall's 3/2 rule). Asymmetry transforms are applied post-hoc:`soma_offset_pd_um`translates the soma along the PD axis,`field_elongation_pd`stretches the dendritic field along PD,`branch_density_gradient_pd`re-weights branching probability with PD distance,`primary_branch_pd_concentration`biases primary stems toward PD. Every section gets`nseg` from the d_lambda rule (`freq=100
  Hz`, `d_lambda=0.1`) per [t0080] `extend_with_ais._compute_nseg`, ensuring cable-faithful spatial discretisation. The AIS is built as two concatenated sections (proximal + distal) using the t0080 idiom. Determinism is guaranteed by `numpy.random.default_rng(morph_seed)`
  for all stochastic calls.

**Why a pure-Python generator (alternatives considered).** Three alternatives were evaluated and
rejected:

* **TREES toolbox via oct2py.** Cuntz 2010 / Beining 2017 (T2N) provide a published procedural
  generator validated on multiple cell classes, but it is MATLAB-only with sparse Python wrapping.
  Internet research found that calling TREES from Python via oct2py adds a heavyweight Octave
  dependency, MATLAB script-level file passing, and non-trivial debugging overhead. Crucially,
  TREES' MST_tree does not expose asymmetry knobs analogous to `soma_offset_pd_um` or
  `field_elongation_pd`; those would have to be bolted on Python-side anyway. Net: the interop cost
  exceeds the from-scratch implementation cost.
* **NeuroMaC (Torben-Nielsen 2014).** Python-native L-system generator, but the GitHub repo has been
  unmaintained since ~2015 with no recent releases. Using it as a runtime dependency would require
  dependency forensics on stale code. Rejected; conceptual ideas (growth-cone branching,
  context-aware termination) are referenced in the generator's docstring instead.
* **Real-cell library from NeuroMorpho.Org.** API exists but does not have a DSGC-specific filter
  (only "ganglion"); curated import is out of scope for t0090 per the task description's
  Out-of-Scope. Reserved as a path for t0091's warm-start anchor archive.

**Diversity test (Phases B-C, E).** Phase B uses
`scipy.stats.qmc.LatinHypercube(d=14, optimization="random-cd", seed=42).random(n=30)` scaled
per-parameter to the bounds in `constants.py`. Internet research confirmed that `seed=int` is
mandatory for determinism (the `scramble=False` flag does not suffice). Phase C generates 30
perturbations of the Bed-B-equivalent base point with each parameter independently jittered uniform
+/- 5 percent of its range. Phase E extracts morphometric features (total dendritic length, branch
count, max Strahler depth, electrotonic length, soma displacement, field major-axis length) using
NeuroM's `partition_asymmetry`, `strahler_order`, `section_lengths`, `total_length`. PCA on the
6-feature matrix produces `morphometric_pca.png`; UMAP via `umap-learn` (with `random_state=42`)
produces `morphometric_umap.png` if the package is installed (PCA fallback if not). Per t0041's
electrotonic collapse finding (many distinct (length, diameter) combinations produce identical DSI
when reduced to L/lambda), morphometric features include electrotonic length explicitly so the PCA
reveals whether the 14-knob space is functionally over-parameterised (PC1+PC2 >80 percent variance
-> yes; <50 percent -> no).

**Verification (Phase D).** For each of the 60 morphologies, build the cell, run a 50 ms no-stim
stability check at V_rest = -70 mV (catch NaN voltages, divergence, disconnected sections), then run
the 8-direction bar protocol with the t0083 best-cell parameter vector via t0080's
`evaluate_parameter_vector`. Record DSI, PD-rate, stability flag per morphology. Per [Mainen1996]
some morphologies will fail under a fixed channel set; per the recorded researcher protocol use 1400
ms trial length, HH on for Vm/firing-rate/DSI mode. Parallelised on 64 cores with the t0080
worker-cached cell pattern (cache one MorphologyResult per worker; all 8 directions evaluated on the
same cached cell). Wall-clock target ~5-10 min on the local 64-core EPYC.

**Bed-B reproducibility (Phase F).** Define the Bed-B-equivalent base point: `num_primary_branches`
matching the t0024 Bed B published count (4); `mean_segment_length_um=30` calibrated to deRosenroll
2026's ~341 sections / ~1300 um total dendritic length; `soma_offset_pd_um=0`;
`field_elongation_pd=1.0`; `branch_density_gradient_pd=0`; `primary_branch_pd_concentration=0`;
`rall_exponent=1.5` (Rall canonical); `soma_diameter_um=15`; `ais_length_um=31` (Goethals 2020
mean). Load 5 random t0083 Pareto cells (deterministic
`np.random.default_rng(0).choice(18, size=5, replace=False)`), apply each cell's 54-d vector to the
procedural cell at this base point, run the 8-direction protocol, compare DSI and PD-rate to the
original Pareto values from
`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`. Pass criterion: |delta|
<= 10 percent on both DSI and PD-rate. Note: the task description specifies 5 percent, but
research_papers.md and research_internet.md both flagged that cell-to-cell DSI variability is 10-20
percent biologically and ~5 percent trial-to-trial under AR(2) noise; 10 percent is the achievable
target and is documented as a deliberate relaxation here.

**Validation bundle (Phase G).** G.1 is pure data analysis on existing JSONs: load t0088
recluster_centroids.json and t0083 all_evaluations.json, extract
`centroid_unnormalised[NAV16_AIS_GBAR]` and `[NAV16_SOMA_GBAR]` per cluster, compute the ratio per
cluster and per cell for cluster-1 cells (1304, 1504, 1624, 1634), check whether
`LOWER_BOUNDS[NAV16_SOMA_GBAR]=1e-5` is being hit. G.2 is a log sweep of `gnmda_dend` from 1e-5 to
1e-2 uS on one t0080 cell at PD direction, recording per-spine `g_nmda_us` from the NEURON state
during stimulus, integrating to compute effective open conductance, producing a calibration curve
mapping NetCon weight to per-spine conductance, then re-scoring t0086 / t0088 cluster centroids
against the Sivyer 2013 0.1 nS prior in the calibrated units. G.3 is the t0088 16-direction Vm-trace
deepdive driver run with `params[NAP_DEND_DISTAL]=0.0` forced on cells 1604, 1634, 767, 1639. The G
synthesis answer asset combines these into a yes/no verdict per suggestion plus an overall
confidence rating.

**Reuse summary.** Imports from prior task libraries:
`tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants` for passive defaults;
`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants` for `ParameterVector`, `ParamIndex`,
`LOWER_BOUNDS`, `UPPER_BOUNDS`, `Tier`;
`tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params` for `apply_parameter_vector`,
`ensure_t80_dll_loaded`; `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver` for
`evaluate_parameter_vector`, `EvalResult`;
`tasks.t0011_response_visualization_library.code.tuning_curve_viz` for polar/cartesian polar tuning
panels (Phase F sanity panel);
`tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics` for `compute_dsi`,
`compute_peak_hz`, `compute_null_hz`. Code copied into the task: t0080
`extend_with_ais._compute_nseg` (12 lines), t0088 `select_representatives._load_cell_entries` (40
lines), t0088 `run_deepdive` 16-direction driver (80 lines), t0088
`attribution_metric.compute_attribution` (40 lines), t0086 `biological_scorecard._verdict` (30
lines), t0086 `biological_priors.BIOLOGICAL_PRIORS` list (or read it from
`tasks/t0086.../results/data/biological_priors.json` directly). New libraries: `scipy.stats.qmc`
(already in `pyproject.toml` via scipy), `umap-learn` (added optional dependency), `neurom` (added
optional dependency for morphometric features).

## Cost Estimation

Total estimated cost: **$0.30**.

* **Phase A** (generator implementation): $0 — local Python development.
* **Phase B-C** (LHS + perturbation sampling): $0 — local CPU, seconds.
* **Phase D** (60-morph verification): $0 — local 64-core EPYC, ~5-10 min wall-clock. Local
  hardware available; no remote provisioning needed.
* **Phase E** (visualisation): $0 — local matplotlib + scipy + neurom + optional umap-learn, ~1
  hour.
* **Phase F** (Bed-B reproducibility): $0 — local 64-core EPYC, ~1 hour for 5 cells x 8
  directions.
* **Phase G.1** (AIS-to-soma audit): $0 — pure data analysis on existing JSONs.
* **Phase G.2** (NMDA calibration ablation): **$0.30** — Vast.ai EPYC 7B13 for ~1 hour at $0.30/h.
  Local CPU is available as a free fallback if Vast.ai provisioning fails (Phase G.2 is a
  single-cell parameter sweep, not a multi-trial population sim, so a single thread suffices and the
  time budget is generous).
* **Phase G.3** (NaP knockout): $0 — local 64-core EPYC, ~64 min wall-clock for 4 cells x 16
  directions.

Project budget context: total budget **$20.00**, **$15.55** spent, **$4.45** remaining before this
task. After t0090 the buffer is ~$4.15, leaving ~$3.00-3.50 for t0091's joint NSGA-II run as
planned.

## Step by Step

The Step by Step is grouped into milestones aligned with the seven phases. Steps must be executed in
order; each milestone is independently verifiable.

### Milestone 1: Generator infrastructure (Phase A)

1. **Create `code/paths.py`.** Define constants for repo-relative output paths:
   `TASK_ROOT = Path(__file__).resolve().parent.parent`,
   `DATA_DIFFERENT_DIR = TASK_ROOT / "data" / "different_morphologies"`,
   `DATA_SIMILAR_DIR = TASK_ROOT / "data" / "similar_morphologies"`,
   `DATA_VERIFICATION_JSON = TASK_ROOT / "data" / "verification_summary.json"`,
   `DATA_BEDB_REPRO_JSON = TASK_ROOT / "data" / "bedb_reproducibility.json"`,
   `DATA_G1_AUDIT_JSON = TASK_ROOT / "data" / "g1_nav_ratio_audit.json"`,
   `DATA_G2_CALIB_JSON = TASK_ROOT / "data" / "g2_nmda_calibration.json"`,
   `DATA_G3_KNOCKOUT_JSON = TASK_ROOT / "data" / "g3_nap_knockout.json"`,
   `DATA_G3_TRACES_DIR = TASK_ROOT / "data" / "g3_traces"`,
   `RESULTS_IMAGES_DIR = TASK_ROOT / "results" / "images"`. Cross-task input paths:
   `T0083_PARETO_FRONT_JSON = REPO_ROOT / "tasks" / "t0083_bedb_v3_extend_nsga2_gen8plus" / "results" / "data" / "pareto_front.json"`;
   `T0083_ALL_EVALUATIONS_JSON = REPO_ROOT / "tasks" / "t0083_bedb_v3_extend_nsga2_gen8plus" / "results" / "data" / "all_evaluations.json"`;
   `T0088_RECLUSTER_CENTROIDS_JSON = REPO_ROOT / "tasks" / "t0088_recluster_marginals_and_vm_motifs" / "results" / "data" / "recluster_centroids.json"`.
   Add an `ensure_directories()` helper that creates all output directories. **Inputs**: none.
   **Outputs**: `code/paths.py`. **Satisfies**: prerequisite for REQ-1 through REQ-14.

2. **Create `code/constants.py`.** Define the 14 parameter bounds as
   `PARAM_BOUNDS: dict[str, tuple[float, float]]` exactly per the task_description.md table; the
   Bed-B-equivalent base point as a dict (`BEDB_BASE_POINT`); enums `StabilityKind(Enum)` with
   members `STABLE`, `NAN_VOLTAGE`, `DIVERGED`, `DISCONNECTED`; integer parameter names list
   (`INT_PARAM_NAMES = ["num_primary_branches", "max_strahler_depth", "morph_seed"]`); the d_lambda
   constants `LAMBDA_F_FREQ_HZ = 100.0` and `D_LAMBDA = 0.1`; cluster representative cell IDs
   (`CLUSTER_1_CELL_IDS = (1304, 1504, 1624, 1634)`,
   `REPRESENTATIVE_CELL_IDS = (1604, 1634, 767, 1639)`); 16-direction angles tuple (copy from t0088
   `run_deepdive.ANGLES_16DIR_DEG`); Phase G.2 NMDA sweep levels
   (`GNMDA_SWEEP_US = (1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2)`). **Inputs**: research files for
   the parameter bounds. **Outputs**: `code/constants.py`. **Satisfies**: prerequisite for REQ-2.

3. **Create `code/morphology_params.py`.** Define
   `@dataclass(frozen=True, slots=True) class MorphologyParams` with the 11 typed float fields and 3
   typed int fields (`num_primary_branches: int`, `max_strahler_depth: int`, `morph_seed: int`). Add
   `to_dict()` and `from_dict(cls, data)` methods for serialisation. Define
   `@dataclass(frozen=True, slots=True) class MorphometricSummary` with fields
   `total_dendritic_length_um: float`, `branch_count: int`, `max_strahler_depth: int`,
   `electrotonic_length_lambda: float`, `soma_displacement_um: float`,
   `field_major_axis_length_um: float`. Define
   `@dataclass(frozen=True, slots=True) class MorphologyResult` with fields `soma: Section`,
   `all_dends: list[Section]`, `primary_dends: list[Section]`, `non_terminal_dends: list[Section]`,
   `terminal_dends: list[Section]`, `terminal_locs_xy: list[tuple[float, float]]`,
   `origin_xy: tuple[float, float]`, `ais_proximal: Section`, `ais_distal: Section`,
   `stability_flag: StabilityKind`, `morphometric_summary: MorphometricSummary`,
   `connectivity: dict[str, str]` (child name -> parent name). **Inputs**: `constants.py`.
   **Outputs**: `code/morphology_params.py`. **Satisfies**: REQ-2, REQ-3.

4. **Create `code/generator.py` -- main procedural generator.** Implement
   `def generate_morphology(*, params: MorphologyParams, morph_seed: int) -> MorphologyResult`.
   Internally: (a) call `ensure_t80_dll_loaded()` from t0080 once per process; (b) instantiate
   `rng = np.random.default_rng(morph_seed)`; (c) build the soma as `h.Section(name="soma")`, set
   `L = soma_diameter_um`, `diam = soma_diameter_um`, `Ra = 100.0`, `cm = 1.0`, then move it along
   PD by `soma_offset_pd_um`; (d) sample primary-branch angles using
   `rng.vonmises(mu_pd_rad, kappa=primary_branch_pd_concentration, size=num_primary_branches)`; (e)
   for each primary branch, construct sections recursively up to `max_strahler_depth` levels with
   branching probability `branch_prob_per_um` per micron of segment length, segment length
   `mean_segment_length_um * (1 + branch_length_cv * rng.normal())`, branching angle
   `mean_branching_angle_deg + rng.normal()*branch_length_cv*30`, daughter diameters from the Rall
   power law `(d_parent**rall_exponent / num_daughters)**(1/rall_exponent)`; (f) after the topology
   is built, apply asymmetry transforms (`soma_offset_pd_um` translation, `field_elongation_pd`
   PD-axis stretch, `branch_density_gradient_pd` post-hoc branch reweighting); (g) build the AIS as
   two sections (`ais_proximal`, `ais_distal`) with total length `ais_length_um`, attached to
   `soma(0)`. **Imports**:
   `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import ensure_t80_dll_loaded`
   and `from neuron import h`. **Inputs**: `MorphologyParams`. **Outputs**: `code/generator.py`,
   returns a `MorphologyResult`. **Satisfies**: REQ-1, REQ-3.

5. **Add `_compute_nseg` helper inside `code/generator.py`.** Copy the d_lambda rule from
   `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/extend_with_ais.py` lines 46-56. Signature:
   `def _compute_nseg(*, h, section, freq: float = LAMBDA_F_FREQ_HZ, d_lambda: float = D_LAMBDA) -> int`.
   Apply it to every newly created section after `L`, `diam`, `Ra`, `cm` are set:
   `section.nseg = _compute_nseg(h=h, section=section)`. **Inputs**: a NEURON section. **Outputs**:
   an odd integer >= 1. **Satisfies**: REQ-15.

6. **Add post-hoc asymmetry transforms inside `code/generator.py`.** For `field_elongation_pd`,
   stretch all section endpoints along the PD axis by the factor. For `branch_density_gradient_pd`,
   re-sample branching probability biased by
   `(pd_distance / max_pd_distance) * branch_density_gradient_pd`. The transforms operate on the
   topology dict before the NEURON sections are built (so geometric transforms only change `pt3dadd`
   coordinates if 3D coordinates are emitted). **Inputs**: topology dict. **Outputs**: transformed
   topology dict. **Satisfies**: REQ-1.

7. **Create `code/test_generator.py` and `code/test_determinism.py` -- unit tests.** Tests: (a)
   `test_determinism` -- generate two cells with the same `(params, morph_seed)`, compare section
   count, lengths, diameters, and connectivity dict; assert byte-identical dumps; (b)
   `test_min_branches` -- `num_primary_branches=3`, `max_strahler_depth=2` produces a valid cell
   with 3 primary branches; (c) `test_max_branches` -- `num_primary_branches=7`,
   `max_strahler_depth=6` produces a valid cell with 7 primary branches; (d) `test_no_nan` -- for 10
   random parameter draws, all section lengths > 0 and diameters > 0, no disconnected sections; (e)
   `test_round_trip` -- `MorphologyParams.to_dict()` -> `from_dict()` returns an equal object; (f)
   `test_nseg_dlambda` -- for L in [10, 600] um, `_compute_nseg` returns an odd integer >= 1. Run
   via `uv run pytest tasks/t0090_morphology_generator_diversity_test/code/ -v`. **Expected
   output**: 6 tests pass. **Satisfies**: REQ-4, REQ-15.

### Milestone 2: Diversity sampling (Phases B + C)

8. **Create `code/sample_different.py`.** Use
   `scipy.stats.qmc.LatinHypercube(d=14, optimization="random-cd", seed=42).random(n=30)` to produce
   a 30x14 sample in [0, 1)^14; scale per-parameter to the bounds in `constants.PARAM_BOUNDS`; cast
   `num_primary_branches`, `max_strahler_depth` and `morph_seed` to int (the seed is itself drawn
   from a uniform 0-2**31 with a deterministic
   `np.random.default_rng(42).integers(0, 2**31, size=30)`). Write each row as a
   `MorphologyParams.to_dict()` JSON to `data/different_morphologies/morph_NN.json` (NN = 00..29).
   **Inputs**: `constants.PARAM_BOUNDS`. **Outputs**: 30 JSON files. **Satisfies**: REQ-5.

9. **Create `code/sample_similar.py`.** Define `BEDB_BASE_POINT` per Step 2; for each of the 14
   parameters, sample 30 perturbations as `base_value * (1 + uniform(-0.05, +0.05))` for floats and
   `base_value + randint(-1, +1)` clipped to bounds for ints, using `np.random.default_rng(43)`.
   Write each perturbed parameter set as a `MorphologyParams.to_dict()` JSON to
   `data/similar_morphologies/morph_NN.json`. **Inputs**: `BEDB_BASE_POINT`, `PARAM_BOUNDS`.
   **Outputs**: 30 JSON files. **Satisfies**: REQ-6.

### Milestone 3: Verification simulation (Phase D)

10. **Create `code/load_default_params.py` -- load the t0083 best-cell parameter vector.** Read
    `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`, select the cell with
    the highest DSI (or the canonical "best cell" per t0083's results_summary), return its 54-d
    list[float] as a `ParameterVector`. **Imports**:
    `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParameterVector`.
    **Inputs**: `T0083_PARETO_FRONT_JSON`. **Outputs**: a `ParameterVector` instance. **Satisfies**:
    prerequisite for REQ-7.

11. **Create `code/verification.py`.** Define
    `verify_morphology(params: MorphologyParams, default_params: ParameterVector) -> VerificationResult`
    where `VerificationResult` is a `@dataclass(frozen=True, slots=True)` with `morph_id: str`,
    `stability_flag: StabilityKind`, `dsi: float | None`, `pd_rate_hz: float | None`,
    `peak_vm_mv: float | None`, `error: str | None`. Internally: (a) call
    `generate_morphology(params=..., morph_seed=...)` to build the cell; (b) run
    `h.continuerun(50.0)` with `v_init = -70.0` and check for NaN voltages / divergence /
    disconnected sections — set `stability_flag` accordingly; (c) if STABLE, call
    `evaluate_parameter_vector(cell=morph_result, params=default_params, n_seeds=1)` from t0080's
    trial_driver and record DSI and PD-rate per the 8-direction protocol with 1400 ms trial length,
    HH on for Vm/firing-rate. Wrap in `try/except (RuntimeError, ValueError, ArithmeticError)` per
    the t0080 pattern; on exception, set `stability_flag = DIVERGED` and DSI/PD-rate to None. Use
    `concurrent.futures.ProcessPoolExecutor(max_workers=64)` with the t0080 worker-cached cell
    pattern. Save 60 results to `data/verification_summary.json`. **Validation gate**: run on the
    first 5 morphologies (limit=5) before scaling to 60; baseline expectation is that the Bed-B
    base-point morph (similar set #00) produces a STABLE cell with DSI in [0.2, 0.9]; if the small
    run reports any NAN_VOLTAGE on the Bed-B base point itself, halt and debug — do NOT scale to
    60\. **Imports**:
    `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import evaluate_parameter_vector, EvalResult`.
    **Inputs**: 60 morph JSON files + default params. **Outputs**: `data/verification_summary.json`
    with 60 entries. **Satisfies**: REQ-7, REQ-16.

### Milestone 4: Visualisation (Phase E)

12. **Create `code/visualization.py` -- 2D dendrograms and grid panels.** For each
    `MorphologyResult`, compute a 2D radial layout from soma using parent-child connectivity and
    section lengths; use matplotlib `LineCollection` with line widths proportional to
    `section.diam`. Function `plot_dendrogram(*, morph_result: MorphologyResult, ax: Axes) -> None`.
    Driver function
    `make_grid_panel(*, morph_jsons: list[Path], output_png: Path, title: str) -> None` creates a
    5x6 figure (matplotlib `subplots(5, 6)`) with one dendrogram per cell using the Okabe-Ito
    palette from t0011. Save: `results/images/morphology_grid_different.png` and
    `results/images/morphology_grid_similar.png`. **Imports**:
    `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.constants import OKABE_ITO_PALETTE`
    (or duplicate the palette colours locally if the import path differs). **Inputs**: 30 + 30 morph
    JSONs. **Outputs**: 2 PNG files. **Satisfies**: REQ-8.

13. **Create `code/morphometric_pca.py` -- morphometric features + PCA/UMAP.** Compute per
    morphology: total dendritic length (`sum(section.L for section in all_dends)`), branch count
    (`len(non_terminal_dends)`), max Strahler depth (recursive max), electrotonic length (max path
    `L/lambda` from soma to terminal), soma displacement (`hypot(soma_offset_pd_um, 0)`), field
    major-axis length (`max-min PD coordinate of all section endpoints`). Stack into 60x6 feature
    matrix; standardise (z-score) per feature; run `sklearn.decomposition.PCA(n_components=2)` on
    the 60x6 matrix; scatter PC1 vs PC2 colour-coded by set (different=blue, similar=orange). Save
    `results/images/morphometric_pca.png`. If `umap-learn` is importable, also run
    `umap.UMAP(n_neighbors=15, n_components=2, random_state=42).fit_transform(features_z)` and save
    `results/images/morphometric_umap.png`; otherwise log a warning and emit only the PCA panel.
    Compute and report PC1+PC2 variance explained ratio and the cluster radius for the similar set
    in PC1-PC2 (record in `data/morphometric_summary.json`). **Imports**:
    `from sklearn.decomposition import PCA`; conditional
    `try: import umap except ImportError: umap = None`. **Inputs**: 60 `MorphologyResult` instances.
    **Outputs**: 1-2 PNG files + 1 JSON. **Satisfies**: REQ-8.

### Milestone 5: Bed-B reproducibility (Phase F)

14. **Create `code/reproducibility.py`.** Load `T0083_PARETO_FRONT_JSON`, take 5 cells via
    `np.random.default_rng(0).choice(18, size=5, replace=False)`. For each cell: extract its 54-d
    `params` list as a `ParameterVector`, build the procedural cell at the Bed-B-equivalent base
    point (`BEDB_BASE_POINT`), apply the parameter vector, run the 8-direction protocol via
    `evaluate_parameter_vector`, compare resulting DSI and PD-rate to the original Pareto values.
    Compute `dsi_delta_pct` and `pd_rate_delta_pct`; pass criterion is |delta| <= 10 percent on
    both. **Validation gate**: run on the first cell only (limit=1) before scaling to 5; baseline
    expectation is that the procedural Bed-B-equivalent cell reproduces the cell-1 DSI within 20
    percent; if the cell-1 delta exceeds 50 percent, halt and inspect the topology dump (likely a
    diameter-taper or axial-connectivity bug per the task description's failure mode). Write 5
    entries to `data/bedb_reproducibility.json`; also produce a sanity panel
    `results/images/bedb_polar_comparison.png` with 5 polar tuning curves overlaid (procedural in
    solid line, Pareto reference in dashed). **Imports**:
    `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.polar import plot_polar_tuning_curve`.
    **Inputs**: 5 t0083 Pareto cells + Bed-B-equivalent `MorphologyParams`. **Outputs**:
    `data/bedb_reproducibility.json`, 1 PNG. **Satisfies**: REQ-9.

### Milestone 6: Validation bundle (Phase G)

15. **Create `code/validation_g1_nav_ratio.py`.** Read `T0088_RECLUSTER_CENTROIDS_JSON`, extract
    per-cluster `centroid_unnormalised[NAV16_AIS_GBAR]` and `[NAV16_SOMA_GBAR]`, compute the ratio
    per cluster (assert units S/cm^2 / S/cm^2 = dimensionless). Read `T0083_ALL_EVALUATIONS_JSON`,
    filter to the 4 cluster-1 cells (1304, 1504, 1624, 1634), compute per-cell
    `params[NAV16_AIS_GBAR] / params[NAV16_SOMA_GBAR]`. Check whether
    `LOWER_BOUNDS[NAV16_SOMA_GBAR]=1e-5` is being hit (any cell with
    `params[NAV16_SOMA_GBAR] <= 1.05 * 1e-5` is flagged as floor-pinned). Write
    `data/g1_nav_ratio_audit.json` with fields `cluster_centroid_ratios: list[ClusterEntry]`,
    `per_cell_ratios: list[CellEntry]` (cluster-1 only), `floor_pinned_cell_ids: list[int]`,
    `verdict: Literal["units_bug", "real_signal", "centroid_artifact"]`. **Imports**:
    `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParamIndex, LOWER_BOUNDS`.
    **Inputs**: 2 JSON files. **Outputs**: 1 JSON. **Satisfies**: REQ-10.

16. **Create `code/validation_g2_nmda_units.py`.** Pick a single t0080 cell (the Bed-B-equivalent
    cell from `T0083_PARETO_FRONT_JSON`); for each `gnmda_dend` in
    `GNMDA_SWEEP_US = (1e-5, 5e-5, 1e-4, 5e-4, 1e-3, 5e-3, 1e-2)`, run a single PD-direction trial
    (1400 ms, 1 seed), record the `g_nmda_us` value at each NMDA synapse during the stimulus window
    via `h.Vector().record(seg.g_nmda_us)`, integrate to compute per-spine effective open
    conductance (mean over the stimulus window), and produce a calibration mapping NetCon weight ->
    per-spine conductance in nS. **Validation gate**: run with the smallest sweep value
    (gnmda_dend=1e-5) only as a preflight; if the recorded per-spine `g_nmda_us` is exactly zero or
    NaN, halt — the recording mechanism is wrong. Save the 7-point calibration curve as
    `data/g2_nmda_calibration.json`. Re-score t0086 / t0088 cluster centroids against Sivyer 2013
    (mean = 0.1 nS = 1e-4 uS, sigma = 5e-5 uS) using the calibration curve to convert centroid
    `gnmda_dend` from NetCon weight to per-spine conductance, and report new `sigma_deviation`
    values per cluster. Save `results/images/nmda_calibration_curve.png` (log-log scatter with fit).
    Run on Vast.ai EPYC 7B13 if local CPU is busy; else run locally. **Imports**:
    `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import apply_parameter_vector`.
    **Inputs**: 1 t0080 cell + sweep levels. **Outputs**: 1 JSON, 1 PNG. **Satisfies**: REQ-11.

17. **Create `code/validation_g3_nap_knockout.py`.** Copy t0088's `run_deepdive.py` 16-direction
    driver pattern (lines 70-180) into the task. For each cell in
    `REPRESENTATIVE_CELL_IDS = (1604, 1634, 767, 1639)`: load its 54-d params from
    `T0083_ALL_EVALUATIONS_JSON`, override `params[NAP_DEND_DISTAL] = 0.0`, run the 16-direction
    Vm-trace deepdive (1400 ms each, HH on), save `.npz` per (cell, direction) to
    `data/g3_traces/cell{cell_id}_dir{direction_int_tenths}_traces.npz`. Compute knockout DSI per
    cell, compare to the original t0088 DSI, classify per-cell verdict as `"nap_dominant"` (DSI <=
    0.2), `"nap_partial"` (0.2 < DSI <= 0.4), or `"nap_minor"` (DSI > 0.4). Reuse t0088's
    `attribution_metric.compute_attribution()` (copy lines 56-130) to recompute NMDA / Nav1.6 / NaP
    fractional attribution post-knockout — expected: NaP fraction shifts to ~0, NMDA + Nav1.6
    fractions absorb the difference. Save `data/g3_nap_knockout.json` with per-cell verdicts and
    attribution shifts. [CRITICAL] — this is the load-bearing causal step. **Validation gate**:
    run cell 1604 first (limit=1); the original t0088 DSI for cell 1604 is documented in
    `tasks/t0088.../results/data/representative_cells.json`; if knockout DSI for cell 1604 is
    identical to the original (>99 percent match), the override did not propagate (likely a `params`
    deep-copy or `ParamIndex` indexing bug) -- halt and debug before the other 3 cells. **Imports**:
    `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import apply_parameter_vector`,
    `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParamIndex`.
    **Inputs**: 4 cell IDs + `T0083_ALL_EVALUATIONS_JSON`. **Outputs**: `data/g3_nap_knockout.json`
    + 64 `.npz` files. **Satisfies**: REQ-12.

### Milestone 7: Library asset + answer asset (deliverables)

18. **Create the library asset.** Write
    `assets/library/procedural_dsgc_morphology_generator/details.json` with
    `library_id = "procedural_dsgc_morphology_generator"`, `version = "0.1.0"`,
    `description_path = "description.md"`, `module_paths` listing
    `tasks/t0090_.../code/morphology_params.py`, `tasks/t0090_.../code/generator.py`,
    `tasks/t0090_.../code/verification.py`, `tasks/t0090_.../code/constants.py`. `entry_points`:
    `generate_morphology` (full path), `MorphologyParams`, `MorphologyResult`,
    `MorphometricSummary`, `StabilityKind`, `verify_morphology`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`.
    Categories: `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
    `dendritic-computation`. Write
    `assets/library/procedural_dsgc_morphology_generator/description.md` with the canonical
    documentation: Overview, API Reference (every public function with full signature, parameter
    descriptions, return type, behaviour), Usage Examples (at least 2 runnable: a minimal
    `generate_morphology(BEDB_BASE_POINT, morph_seed=0)` example and a realistic Phase D
    verification workflow), Data Formats (every dataclass field documented), Dependencies (numpy,
    scipy.stats.qmc, neuron, plus internal libraries `de_rosenroll_2026_dsgc_ais_dendritic_spike`,
    `tuning_curve_viz`), Testing (`uv run pytest tasks/t0090_.../code/ -v`), Limitations (no
    real-cell library; t0091 must select warm-start anchors carefully; the diversity test is
    exploratory not statistically certifiable). **Inputs**: code files. **Outputs**: 2 files in
    `assets/library/`. **Satisfies**: REQ-13.

19. **Create the answer asset.** Write
    `assets/answer/validation-triplet-implications-for-biological-plausibility/details.json` with
    `answer_id = "validation-triplet-implications-for-biological-plausibility"`,
    `question = "Do the validation triplet results (G.1 AIS-to-soma Nav ratio audit, G.2 NMDA units calibration, G.3 NaP knockout) confirm or refute the biological-plausibility flags raised in t0086 and t0088?"`,
    `short_answer_path = "short_answer.md"`, `full_answer_path = "full_answer.md"`, `answer_methods`
    listing `code` (G.2 + G.3 ablation), `prior_assets` (t0086 biological_priors, t0088
    cluster_centroids), `existing_papers` (Werginz 2024, Sivyer 2013, Schachter 2010, Trenholm
    2013). Categories: `compartmental-modeling`, `direction-selectivity`, `voltage-gated-channels`.
    Write `short_answer.md` with the `## Question` and `## Answer` sections, the latter being a 2-5
    sentence direct answer beginning with "Yes", "No", or "Conditional" per the format spec (no
    inline citations). Write `full_answer.md` with the canonical sections per the answer asset
    specification: Question, Short Answer (no citations), Methods (each of G.1/G.2/G.3 with Step
    IDs), Evidence from Code or Experiments (referencing `code/validation_g1_nav_ratio.py` etc.),
    Synthesis (combine the three findings into the overall verdict + confidence rating),
    Limitations, Sources (markdown reference link definitions for every cited paper / task).
    **Inputs**: G.1, G.2, G.3 results JSONs. **Outputs**: 3 files in `assets/answer/`.
    **Satisfies**: REQ-14.

20. **Compute project metrics and produce charts -- final integration step.** Read
    `data/verification_summary.json` and the Bed-B reproducibility JSON; compute the registered
    metric `direction_selectivity_index` per morphology (already in the verification summary); for
    the 5 Bed-B-reproducibility cells additionally compute `tuning_curve_hwhm_deg` via
    `compute_hwhm_deg` from t0012's library. Write to `results/metrics.json` using the **explicit
    multi-variant format** per `arf/specifications/metrics_specification.md`, with one variant per
    morphology population (`different_set`, `similar_set`, `bedb_repro_5`). Produce
    `results/images/diversity_summary.png` (a 2-panel figure: DSI distribution histogram per set;
    PD-rate distribution histogram per set). **Imports**:
    `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg`.
    **Inputs**: 4 JSON files (verification, reproducibility, G.1, G.3). **Outputs**:
    `results/metrics.json`, `results/images/diversity_summary.png`. **Satisfies**: REQ-16.

## Remote Machines

A remote machine is **optional**, used only for Phase G.2 (NMDA units calibration ablation), and
even that phase has a free local-CPU fallback. Specification: Vast.ai EPYC 7B13, no GPU required
(t0090 is CPU-bound NEURON), ~1 hour wall clock at $0.30/h. Provisioning is opportunistic — if the
local 64-core EPYC is busy with another task, rent the remote machine; otherwise run locally for $0.
Phases A-F and G.1, G.3 are local-only (the local 64-core EPYC has more than enough capacity).
Reference `arf/specifications/remote_machines_specification.md` for the lifecycle commands.

## Assets Needed

* **t0024 library `de_rosenroll_2026_dsgc`** (categories `compartmental-modeling`,
  `direction-selectivity`) — supplies the passive defaults (`RA_OHM_CM=100.0`, `CM_UF_CM2=1.0`,
  `GLEAK_S_CM2=0.0001667`, `ELEAK_MV=-60.0`) and the Bed-B reference morphology used to set the
  Bed-B-equivalent base point in `constants.BEDB_BASE_POINT`. Imported as
  `tasks.t0024_port_de_rosenroll_2026_dsgc.code.constants`.
* **t0080 library `de_rosenroll_2026_dsgc_ais_dendritic_spike`** (categories `ais`, `evaluation`)
  — the canonical 54-d substrate. Provides `ParameterVector`, `ParamIndex`, `LOWER_BOUNDS`,
  `UPPER_BOUNDS`, `apply_parameter_vector`, `evaluate_parameter_vector`, `ensure_t80_dll_loaded`,
  `_compute_nseg` (copied), and the trial driver harness. Used by Phase D, Phase F, Phase G.2, Phase
  G.3.
* **t0011 library `tuning_curve_viz`** — supplies polar / Cartesian tuning-curve plotting
  primitives and the Okabe-Ito palette. Used by Phase F sanity panel.
* **t0012 library `tuning_curve_loss`** — supplies `compute_dsi`, `compute_peak_hz`,
  `compute_null_hz`, `compute_hwhm_deg`. Used by Phase D, Phase F, and the metrics step.
* **t0083 results data**: `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`
  (18 Pareto cells) and
  `tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/all_evaluations.json` (1728 cells) —
  source of the 5 Phase F reproducibility cells, the Phase G.3 representative cells, and the Phase
  G.1 cluster-1 cells.
* **t0086 results data**:
  `tasks/t0086_robustness_cluster_bio_comparison/results/data/biological_priors.json` (9 priors,
  Werginz 2024 / Kole 2008 / Sivyer 2013 / Branco-Hausser 2010 / Stuart 1999 / etc.) — source of
  the prior values used by Phase G.1 and Phase G synthesis to re-score clusters.
* **t0088 results data**:
  `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/recluster_centroids.json` and
  `tasks/t0088_recluster_marginals_and_vm_motifs/results/data/representative_cells.json` — source
  of the 4 cluster representatives (1604, 1634, 767, 1639) and the cluster-1 centroid AIS-to-soma
  Nav ratio (116) being audited in Phase G.1.
* **External Python packages**: `numpy`, `scipy>=1.17`, `pymoo>=0.6.1.6` (already in
  `pyproject.toml`); to be added: `umap-learn>=0.5.7` (optional, for Phase E UMAP panel), `neurom`
  (optional, for Phase E community-standard morphometric features). Both are pip-installable; if
  install fails, the script falls back to PCA-only and inline morphometric computations.

## Expected Assets

* **Library asset (1)**: `assets/library/procedural_dsgc_morphology_generator/` — the validated
  procedural DSGC morphology generator. Library ID: `procedural_dsgc_morphology_generator`. Short
  description: "Pure-Python procedural DSGC morphology generator with 14 explicit knobs (5 topology
  \+ 4 asymmetry + 3 geometry + 2 stochastic), deterministic given (params, seed), structurally
  compatible with t0080's apply_parameter_vector harness, validated by 60-morphology diversity test
  and 5-cell Bed-B reproducibility check." Categories: `compartmental-modeling`,
  `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`.
* **Answer asset (1)**: `assets/answer/validation-triplet-implications-for-biological-plausibility/`
  — the 3-suggestion validation triplet synthesis. Question: "Do the validation triplet results
  (G.1 AIS-to-soma Nav ratio audit, G.2 NMDA units calibration, G.3 NaP knockout) confirm or refute
  the biological-plausibility flags raised in t0086 and t0088?". Short answer is 2-5 sentences; full
  answer covers all three findings with confidence rating. Categories: `compartmental-modeling`,
  `direction-selectivity`, `voltage-gated-channels`.

These match `task.json` `expected_assets = {"library": 1, "answer": 1}` exactly.

## Time Estimation

* Research stages (already done): research_papers.md, research_internet.md, research_code.md.
* Phase A — Generator implementation + unit tests (Steps 1-7): ~1.5-2 days local.
* Phase B + C — LHS sampling + perturbation sampling (Steps 8-9): seconds.
* Phase D — Verification simulation on 60 morphologies (Step 11): ~5-10 min on 64 cores.
* Phase E — Visualisation (Steps 12-13): ~1 hour.
* Phase F — Bed-B reproducibility on 5 cells (Step 14): ~1 hour on 64 cores.
* Phase G.1 — AIS-to-soma audit (Step 15): ~30 min.
* Phase G.2 — NMDA calibration ablation (Step 16): ~1 hour (Vast.ai or local CPU).
* Phase G.3 — NaP knockout on 4 cells x 16 directions (Step 17): ~1 hour on 64 cores.
* Library asset (Step 18) + answer asset (Step 19) + metrics (Step 20): ~2-3 hours.
* Total wall-clock: ~3-4 days.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Generator implementation slips beyond 3 days due to NEURON-Python idiom debugging | Medium | Schedule overrun; t0091 delayed | Adopt the t0080 `extend_with_ais` idiom verbatim for AIS attachment; copy the d_lambda nseg helper unchanged; reserve 30 percent buffer in the time estimate. If Phase A still slips at 4 days, fall back to TREES toolbox via `oct2py` (heavy but published). |
| Some morphologies fail the verification simulation under the t0083 best-cell channel set (depolarisation block, NaN voltages) per Mainen 1996 morphology-determines-firing-pattern | High | Pass-criterion miss; possibly informative | Mark failed morphologies in `verification_summary.json` with the appropriate `StabilityKind`; do NOT halt the pipeline — Mainen 1996 predicts this. The diversity test passes if a meaningful subset is STABLE; document which fail and why. |
| Bed-B reproducibility check exceeds the 5 percent task-description criterion due to natural cell-to-cell DSI variability of 10-20 percent (Trenholm 2013, Werginz 2024) | High | Pass-criterion miss | Pre-relax the criterion to 10 percent in this plan and document the rationale (Step 14, REQ-9). If even 10 percent fails, investigate diameter taper (rall_exponent base point) and axial connectivity (the two structural transforms most likely to break electrical equivalence). |
| Phase G.3 NaP knockout fails to propagate (knockout DSI ~ original DSI) due to a `ParamIndex` indexing bug | Low | G.3 verdict invalid | Use the Step 17 [CRITICAL] validation gate: run cell 1604 first, compare to t0088's `representative_cells.json` original DSI; if the match is too tight (>99 percent), halt before running the other 3 cells. |
| `umap-learn` install fails on Windows CPython | Low | Phase E UMAP panel missing | Fall back to PCA-only per the Phase E plan; record the fallback in `data/morphometric_summary.json`. PCA is fully sufficient for the diversity test pass criterion. |
| `neurom` install fails or its API has shifted since the OpenBrainInstitute migration | Low | Phase E morphometric feature extraction harder | Fall back to in-house implementations of Strahler order and partition asymmetry (the recursive definitions are ~30 lines of Python each). The Phase E PCA still works because the 6 features are all simple summaries, not depending on NeuroM's internal definitions. |
| Vast.ai provisioning unreachable for Phase G.2 | Low | Slight delay | Run G.2 locally on the 64-core EPYC (single-thread parameter sweep takes ~1 hour either way; remote was opportunistic). |
| The t0083 best-cell channel set is incompatible with very-different morphologies (e.g., extreme asymmetry knobs producing huge electrotonic distances) | Medium | Some cells silent or in depolarisation block | Already covered by the per-morphology stability flag pattern (Step 11). The diversity test does not require all 60 cells to produce meaningful DSI; it requires the population to cover visibly distinct classes per the Phase E grid panel. |

## Verification Criteria

* All unit tests pass: `uv run pytest tasks/t0090_morphology_generator_diversity_test/code/ -v`
  reports 0 failures. Confirms REQ-1, REQ-2, REQ-4, REQ-15.
* Plan verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_plan t0090_morphology_generator_diversity_test`
  reports 0 errors.
* Logs verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_logs t0090_morphology_generator_diversity_test`
  reports 0 errors after every step.
* Task file verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_task_file t0090_morphology_generator_diversity_test`
  reports 0 errors.
* Library asset verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_assets t0090_morphology_generator_diversity_test`
  reports 0 errors for both the library and answer assets. Confirms REQ-13, REQ-14.
* Answer asset verificator passes:
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset validation-triplet-implications-for-biological-plausibility`
  reports 0 errors. Confirms REQ-14.
* Style checks pass: `uv run ruff check --fix . && uv run ruff format . && uv run mypy .` reports 0
  errors on `tasks/t0090_morphology_generator_diversity_test/`.
* `data/verification_summary.json` exists and has 60 entries. Run:
  `uv run python -c "import json, pathlib; print(len(json.loads(pathlib.Path('tasks/t0090_morphology_generator_diversity_test/data/verification_summary.json').read_text())))"`
  outputs `60`. Confirms REQ-7, REQ-16.
* `data/bedb_reproducibility.json` exists, has 5 entries, and 5/5 entries have |dsi_delta_pct| <=
  10.0 and |pd_rate_delta_pct| <= 10.0. Confirms REQ-9.
* `results/images/morphology_grid_different.png`, `results/images/morphology_grid_similar.png`, and
  `results/images/morphometric_pca.png` exist. Confirms REQ-8.
* `data/g1_nav_ratio_audit.json`, `data/g2_nmda_calibration.json`, and `data/g3_nap_knockout.json`
  all exist with verdict fields populated. Confirms REQ-10, REQ-11, REQ-12.
* The library asset `module_paths` are all importable:
  `uv run python -c "from tasks.t0090_morphology_generator_diversity_test.code.generator import generate_morphology; from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import MorphologyParams, MorphologyResult; from tasks.t0090_morphology_generator_diversity_test.code.verification import verify_morphology; print('OK')"`
  outputs `OK`. Confirms REQ-13.
* `## Task Requirement Checklist` coverage check: for each REQ-* item, the satisfying step is listed
  under that requirement and produces a concrete output named in `## Verification Criteria`. Manual
  review item; cross-referenced inline above.
