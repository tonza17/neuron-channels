---
spec_version: "2"
task_id: "t0091_morphology_extended_nsga2_v1"
date_completed: "2026-05-08"
status: "complete"
---
# Plan: First Joint 68-d NSGA-II With Morphology In The Evaluation Loop

## Objective

Run the project's first joint 68-d NSGA-II (54-d v3 electrophys + 14-d procedural DSGC morphology)
on a Vast.ai EPYC 7B13 64-core instance, with the t0092-patched procedural morphology generator
(`generate_fixed_morphology`, canonicalised by correction overlay `C-0093-01`) called inside the
per-cell evaluation loop. Population size is 96, with a hard 8-generation cap, an adaptive
HV-plateau stop (1% growth threshold across a 2-generation window after a 4-generation warm-up), and
a $4.00 hard cost watchdog reading the per-instance hourly rate from the setup-machines
`machine_log.json`. The warm-start population is built from 5 morphology anchors (Bed-B-like,
symmetric, PD-asymmetric, ND-asymmetric, alternative-topology) each cloned with ~19 t0083 gen-17
Pareto electrophys variants, plus 1 random fill, totalling 96 cells. Outputs: a 68-d Pareto-front
predictions asset, an answer asset on whether morphology variation reaches biologically-plausible
joint-pass cells, an extended biological scorecard (9 electrophys priors plus 4 new morphology
priors), and an anchor-tracking analysis with bootstrap-significance p-values over PD-asymmetric vs
ND-asymmetric preservation.

**Done** when: a 68-d Pareto front of >=8 cells exists, the extended biological scorecard has been
applied to every Pareto cell, the anchor-tracking table with bootstrap CIs is present, the answer
asset and the predictions asset both pass their verificators, `verify_plan.py`,
`verify_research_*.py`, `verify_assets.py`, and `verify_costs.py` all pass with 0 errors, and remote
spend is at or below the $4.00 cap.

## Task Requirement Checklist

> **Task name**: First joint 68-d NSGA-II with morphology in eval loop, 5-anchor warm-start.
>
> **Short description**: First joint 68-d NSGA-II (54-d electrophys + 14-d morphology) with
> t0092-patched generator in eval loop; pop 96, <=8 gens, 5-anchor warm-start.
>
> **Long description (operative excerpts from `task_description.md`)**:
>
> * Scope (in): 68-d NSGA-II with the t0092 patched generator (`generate_fixed_morphology`,
>   canonicalised by C-0093-01); pop 96, up to 8 generations, adaptive HV-plateau stop, cost
>   watchdog; 5-anchor warm-start population (Bed-B-like + symmetric + PD-asymmetric + ND-asymmetric
>   \+ alt-topology) each cloned with ~19 t0083 Pareto electrophys variants; Pareto-front analysis
>   with biological-plausibility scoring per t0086 / t0088 framework extended to 68-d;
>   anchor-tracking analysis (PD- vs ND-asymmetric preservation); one answer asset on biological
>   plausibility under morphology variation; one predictions asset (68-d Pareto cells with DSI / PD
>   / robustness / morphology / electrophys).
> * NSGA-II settings: pop 96, up to 8 generations, SBX eta=15, polynomial mutation eta=20 with
>   prob=1/68, mixed integer-real handling for `num_primary_branches` and `max_strahler_depth`.
> * Cost watchdog: $4.00 hard cap; 5 evaluation seeds per cell; bar-rotation simulation at 16
>   directions; objectives = (DSI vector-sum, PD firing rate, robustness across seeds).
> * Pass criteria: Phase B converges within budget without NaN propagation; Phase C produces a 68-d
>   Pareto front of >=8 cells; Phase D produces an anchor-tracking table with bootstrap-significance
>   p-values; Phase E lands a definitive yes/no on whether morphology extension reaches biologically
>   plausible cells.
> * Cross-references / corrections: t0091 imports the t0092 patched generator only; t0090's
>   unpatched `generate_morphology` MUST NOT be called.

| REQ | Description | Step(s) | Evidence |
| --- | --- | --- | --- |
| REQ-1 | Use t0092 `generate_fixed_morphology` only (canonical per `C-0093-01`); never call t0090 `generate_morphology` directly | Steps 3, 6 | `code/generator_wrapper.py` imports t0092; static grep shows zero t0090.generator imports |
| REQ-2 | 14-d morphology + 54-d electrophys = 68-d joint search space; integer dims handled via mixed-variable GA or real-then-round | Steps 5, 7 | `code/constants.py` `LOWER_BOUNDS_68` / `UPPER_BOUNDS_68`; `code/evaluator.py` declares `n_var=68` |
| REQ-3 | Pop 96 = 5 anchors x ~19 t0083 Pareto electrophys clones + 1 random sample | Step 5 | `code/warmstart.py`; `results/data/warm_start_population.json` shape (96, 68) |
| REQ-4 | 5 anchors: Bed-B-like; symmetric; PD-asymmetric (soma offset +100 um, field elongated 2x along PD, branches biased toward PD); ND-asymmetric (mirror of PD-asym); alt-topology (more primary branches, deeper Strahler depth, smaller field) | Step 4 | `code/anchor_definitions.py`; `results/data/anchor_definitions.json` |
| REQ-5 | NSGA-II via pymoo with SBX eta=15, PM eta=20, mut prob=1/68, eliminate_duplicates=True | Step 7 | `code/nsga2_driver.py`; `results/data/algorithm_config.json` |
| REQ-6 | Up to 8 generations; adaptive HV-plateau stop (<1% HV growth across 2-gen window after 4-gen warm-up) | Step 7 | `code/hv_plateau_watchdog.py`; `results/data/hv_trajectory.json` |
| REQ-7 | $4.00 hard cost watchdog reading per-instance hourly rate from `machine_log.json` `selected_offer.price_per_hour`; trip writes intervention file | Steps 2, 7 | `code/cost_watchdog.py`; `costs.json` `breakdown.vast_ai.actual_rate_usd_per_hour`; `intervention/budget_overrun.md` if tripped |
| REQ-8 | 5 evaluation seeds per cell; 16 directions per seed; objectives = DSI vector-sum, PD firing rate, robustness | Step 6 | `code/evaluator.py`; per-cell `EvalResult` schema |
| REQ-9 | Smoke gate before remote launch: re-evaluate the 5 anchors with the t0083 best-cell electrophys vector and confirm DSI / PD within tolerance vs the t0093 60-cell post-fix fingerprint | Step 6 | `code/smoke_gate.py`; `logs/steps/<smoke-gate>/smoke_gate_report.json` |
| REQ-10 | Pareto front extracted with >=8 cells | Step 8 | `results/data/pareto_front.json` |
| REQ-11 | Biological scorecard extended to 68-d: keep 9 t0086/t0088 electrophys priors AND add >=4 new morphology priors (`soma_offset_pd_um`, `field_elongation_pd`, `branch_density_gradient_pd`, `primary_branch_pd_concentration`) | Step 9 | `code/biological_priors.py`; `results/data/biological_priors_68d.json`; `results/data/biological_scorecard_68d.json` |
| REQ-12 | Per-Pareto-cell plausibility verdict (plausible / stretched / exotic) under the corrected NMDA prior (Sivyer 2013 corrected units from t0090 Phase G.2) | Step 9 | `biological_scorecard_68d.json` per-cell `verdict` field; heatmap at `results/images/biological_plausibility_heatmap_68d.png` |
| REQ-13 | Anchor-tracking analysis: classify each Pareto cell to its nearest of 5 anchors in 14-d normalised morphology space; tabulate counts; bootstrap 95% CIs (1000 resamples); compute p-value for PD-asymmetric vs ND-asymmetric preservation | Step 10 | `code/anchor_tracking.py`; `results/data/anchor_tracking.json`; `results/images/anchor_tracking_bar.png` |
| REQ-14 | Cable-theoretic v_opt = 2 * lambda / tau_m sanity check tabulated for every Pareto cell | Step 10 | `anchor_tracking.json` per-cell `v_opt_um_per_s` field |
| REQ-15 | Hausselt 2007 length-vs-DSI sanity check: scatter DSI vs effective dendritic length for the Pareto | Step 11 | `results/images/dsi_vs_length.png`; `results/data/length_dsi_correlation.json` |
| REQ-16 | One predictions asset (`pareto-front-68d-morphology-extended-bedb-v3`) with per-cell DSI / PD / robustness / 14-d morphology / 54-d electrophys vectors | Step 11 | `assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/{details.json, description.md, files/pareto_cells.jsonl}` |
| REQ-17 | One answer asset (`morphology-extension-biological-plausibility`) addressing: did morphology extension open biologically-plausible joint-pass regions; which anchors were preserved; PD-asymmetric vs ND-asymmetric direction; biological-plausibility ceiling; follow-ups | Step 12 | `assets/answer/morphology-extension-biological-plausibility/{details.json, short_answer.md, full_answer.md}` |
| REQ-18 | Worker cell cache is morphology-aware: rebuild on morphology vector change, reuse on electrophys-only change; `_LIVE_CELLS` GC defense list per t0093 | Step 6 | `code/trial_driver.py` worker-cache key includes morph hash; module-level `_LIVE_CELLS` |
| REQ-19 | All Vast.ai script invocations from PowerShell set `$env:PYTHONIOENCODING="utf-8"`; aggregator and flowmark runs use the same | Steps 2, 7-12 | `logs/steps/*/exec.json` shows env propagation |
| REQ-20 | Vast.ai EPYC 7B13 64-core instance acquired at <$0.35/hr if available, fallback any 36+ core EPYC <$0.40/hr | Step 2 | `logs/steps/<setup-machines>/machine_log.json` |
| REQ-21 | Outer evaluation seeds recorded deterministically (e.g. `np.random.SeedSequence(42).spawn(5)`) for reproducibility | Step 6 | `results/data/evaluation_seeds.json` |
| REQ-22 | Biological scorecard explicitly notes that the GABA spatial-gradient prior applies to classical-RF SAC-mediated DS only (not Riccitelli 2025 glycinergic extraclassical pathway) | Step 9 | `biological_priors.py` docstring + scorecard report `notes` field |

## Approach

The task is the first NSGA-II run that calls the procedural morphology generator inside the per-cell
evaluation loop. All prior NSGA-II tasks (t0078, t0080, t0081, t0083, t0086) ran on a fixed Bed-B
substrate with 54-d electrophys parameters only; t0091 promotes the 14 morphology knobs from t0090
to first-class optimisation variables, producing a 68-d joint search space.

**Cross-task code reuse rule**. Per the ARF cross-task rule and `research_code.md`, the build path
imports from exactly two task code trees via library assets: t0090 (`MorphologyParams`,
`MorphologyResult`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`, `PARAM_NAMES`, `INT_PARAM_NAMES`,
`StabilityKind`) and t0092 (`generate_fixed_morphology`, `insert_baseline_channels`). All other
reusable code from t0080 / t0081 / t0083 / t0086 / t0088 is **copied** into `tasks/t0091/code/`. The
total copied-and-adapted footprint is ~2491 lines (`apply_params.py` 228, `bootstrap.py` 117,
`build_cell_ais.py` 79, `extend_with_ais.py` 127, `parametric_placer.py` 105, `recorder.py` 122,
`trial_helpers.py` 311, `trial_driver.py` 427, `hv_plateau_watchdog.py` 118, `cost_watchdog.py` 132,
`biological_priors.py` 179, `biological_scorecard.py` 201, `smoke_gate.py` 145), plus ~1600-2200 new
lines (`paths.py`, `constants.py`, `generator_wrapper.py`, `anchor_definitions.py`, `warmstart.py`,
`evaluator.py`, `nsga2_driver.py`, `pareto_analysis.py`, `anchor_tracking.py`).

**NSGA-II configuration**. pymoo `NSGA2` with population 96, SBX crossover eta=15 prob=0.9,
polynomial mutation eta=20 prob=1/68=0.0147 (matching `[Lopez-Camacho-2022]`'s default for
moderate-d MOEA and `[Pymoo-NSGA2-Docs]`), `eliminate_duplicates=True`. Termination is composed via
`TerminationCollection` of `MaximumGenerationTermination(n_max_gen=8)`, a custom
`HVPlateauTermination` (window=2 generations, relative threshold=0.01 after 4-gen warm-up) copied
from t0083, and a custom `CostWatchdogTermination` reading the cumulative spend after each
generation from the same hourly rate that t0086's `cost_watchdog` resolves from the setup-machines
`machine_log.json`. Mixed integer-real handling: 5 integer dims (`num_primary_branches`,
`max_strahler_depth`, `morph_seed`, `n_ach`, `n_gaba`) declared as `Real` and rounded to int at
apply time — matching t0080's existing pattern for its 2 integer electrophys dims (this is the
incumbent project pattern; pymoo's `MixedVariableGA` was a candidate alternative considered and
rejected, see below).

**5-anchor warm-start construction**. Five 14-d morphology anchors (defined verbatim from the
brainstorm 18 task_description.md table — Bed-B-like / symmetric / PD-asymmetric / ND-asymmetric /
alt-topology) each cloned with 19 electrophys vectors sampled from t0083's gen-17 Pareto archive (18
cells in `pareto_front.json`; if 18 < 19 needed per anchor we expand from `all_evaluations.json`
filtered by `t0086/cell_classification.json` Genuine + Marginal class), plus 1 random LHS sample =
96 cells. The warm-start array is passed to pymoo via `sampling=` as a `(96, 68)` numpy array per
`[Pymoo-Initialization-Docs]`; pymoo applies first-generation rank
+ crowding-distance selection to the warm-start, so dominated cells may be filtered — we frontload
  known-dominant cells (the t0083 Pareto-front cells are by construction non-dominated in the
  electrophys subspace).

**Per-cell evaluation**. The worker process keeps a `_WORKER_CELL` cache; the cache key incorporates
a hash of the 14-d morphology vector AND the 54-d electrophys vector. On morphology hash change the
cell is rebuilt by calling
`generate_fixed_morphology(params=morph_params, morph_seed=fixed_per_anchor_or_propagated)` followed
by `insert_baseline_channels` (HHst + cad); on electrophys-only change the cached cell is reused and
`apply_parameter_vector` rewrites the 54-d densities. A module-level `_LIVE_CELLS` list retains
references to all built cells per t0093's GC-defense pattern (cell-id reuse after garbage collection
caused silent channel-skip failures in early dev). 16 directions x 5 evaluation seeds per cell,
parallelised over `cpu_count() - 1` workers via `ProcessPoolExecutor`. Objectives: vector-sum DSI;
PD firing rate (Hz); robustness as the inverse coefficient of variation of DSI across the 5 seeds.
NaN propagation is caught and produces a penalty objective so NSGA-II's selection is well-defined.

**Smoke gate**. Re-evaluate the 5 anchors with the t0083 best-cell electrophys vector under the
patched generator and confirm DSI within 0.05 and PD-rate within 1 Hz of the t0093 60-cell post-fix
fingerprint for the BedB-equivalent point (anchor 1 -- expected PD-rate ~43.6 Hz). The smoke gate is
the first remote step after setup-machines; it MUST pass before the 14-16 hour NSGA-II run is
launched.

**Biological scorecard (68-d extension)**. t0086/t0088's 9 electrophys priors copy verbatim (AIS
Nav, distal Nav1.6, distal NaP, NMDA per-synapse with the corrected-units Sivyer 2013 prior from
t0090 Phase G.2, NMDA voff, GABA rho0, GABA lambda, GABA spatial gradient, AIS-to-soma Nav ratio).
Four NEW morphology priors are added with explicit paper IDs: `soma_offset_pd_um` (mean=0, sigma=50
um, citing Schachter 2010 / Trenholm 2013 displacement bounds); `field_elongation_pd` (mean=1.0,
sigma=0.3, citing Briggman 2011 dendritic field aspect ratios); `branch_density_gradient_pd`
(mean=0, sigma=0.3, anatomical-symmetry prior from Vaney 2012); `primary_branch_pd_concentration`
(mean=0, sigma=0.3, anatomical-symmetry prior from Vaney 2012). Per-cell scoring uses (centroid -
mean) / sigma classified as plausible (<2 sigma), stretched (2-5 sigma), or exotic (>5 sigma);
per-cell verdict is the worst-case prior class. The scorecard output is one row per Pareto cell
rather than t0086/t0088's per-cluster aggregation.

**Anchor-tracking analysis**. For each Pareto cell, compute its 14-d morphology vector's nearest
anchor in min-max-normalised morphology space (skipping `morph_seed` which is non-causal in this
distance metric). Tabulate counts per anchor; bootstrap 1000 resamples for 95% CIs; compute a
p-value for "anchor 3 (PD-asymmetric) over-represented vs anchor 4 (ND-asymmetric)" via a one-sided
exact test. Per `[Briggman2011]`'s 12.8:1 effect-size precedent, t0091 needs at least a 5:1
over-representation to claim the soma-displacement-toward-PD asymmetry direction is functional given
pop 96 / 5 anchors / ~19 cells per anchor.

**Cable-theoretic sanity check**. Compute v_opt = 2 * lambda / tau_m for every Pareto cell where
lambda is derived from the cell's effective dendritic length and tau_m from the membrane RC time
constant per `[Anderson1999]`'s methodology. Report v_opt distribution alongside DSI / PD; cells
whose v_opt is far from `[Trenholm2013]`'s 600 um/s preferred bar velocity are flagged
"DSI-by-cable-mismatch" exotic.

**Hausselt length-vs-DSI test**. Plot Pareto-cell DSI vs effective dendritic length; report the
Spearman correlation. A monotonically positive correlation confirms the `[Hausselt2007]` mechanism
(DSI scales with dendritic length 50-200 um) is operative; a flat or inverted correlation indicates
the Pareto found DSI through the channel-mechanism (the v3 substrate's existing attractor) and not
the morphology mechanism.

**Alternatives considered**:

* **`MixedVariableGA` from pymoo** (recommended in `research_internet.md`): rejected for now to keep
  the structural change minimal and consistent with the t0080-t0083 pattern. The integer dims at
  issue (`num_primary_branches`, `max_strahler_depth`, `n_ach`, `n_gaba`, `morph_seed`) are 5 of 68
  dims; the real-with-round pattern has been validated across 5 prior task runs (t0080-t0086) with
  no observed integer-grid clustering pathology. If HV stalls and individual- parameter analysis
  indicates integer-grid clustering is the cause, the fallback is documented in Risks & Fallbacks.
* **NSGA-III** (k > 3 algorithm): rejected because t0091 has 3 objectives, exactly the design regime
  NSGA-II was made for `[Lopez-Camacho-2022, Pymoo-NSGA3-Docs]`.
* **BoTorch qLogNEHVI** at d=68: rejected per t0078's O(N^3) GP-scaling blowup at d=49 and the
  project's standing preference (NSGA-II for d > 40, BoTorch only for d <= 40).
* **Pop 80 instead of pop 96** (saving ~17% wall-clock): rejected because at d=68 pop 80 gives fewer
  than 16 cells per anchor, which weakens bootstrap power for the anchor-tracking hypothesis test.
  Pop 96 keeps ~19 cells per anchor; if cost overshoot looks likely, the cost watchdog drops to a
  6-gen cap (acceptable degradation; documented as a fallback).
* **Reducing `morph_seed` from optimised to fixed-per-anchor**: documented as a follow-up rather
  than implemented in t0091. The brainstorm specifies all 14 morphology dims as part of the joint
  vector, so `morph_seed` stays in the parameter space with high mutation eta (eta=80) so PM rarely
  changes it across generations.

**Task types**: `experiment-run` (Phase B NSGA-II), `data-analysis` (Phase C/D Pareto + anchor-
tracking), `answer-question` (Phase E). All three present in `task.json`.

## Cost Estimation

Itemised costs:

* **Vast.ai EPYC 7B13 64-core CPU** for Phase B remote NSGA-II:
  * Best case (HV-plateau fires at gen 5): ~10 hours x $0.32/hr = **$3.20**.
  * Worst case (8-gen cap, no plateau): ~14-16 hours x $0.32/hr = $4.50-$5.10 — but the cost
    watchdog at $4.00 hard cap will trigger termination first, capping spend at **<= $4.00**.
  * Realistic central estimate (HV-plateau fires at gen 6-7): **$3.00-$3.50**.
* **Smoke-gate run** (5 anchors x 1 electrophys vector x 5 seeds x 16 directions): ~10 minutes on
  the same Vast.ai instance = ~$0.05 (rolled into the Phase B total above).
* **Phases A, C, D, E** (warm-start construction, Pareto analysis, anchor-tracking, answer asset):
  local 64-core CPU, **$0**.

**Total estimated cost: $3.00-$3.50 (central), <= $4.00 (hard cap)**.

**Project budget context**: $4.45 USD remaining of the $20.00 USD project budget after t0093. A
$4.00 cap leaves a $0.45 buffer for any post-t0091 cleanup; if the watchdog trips, the partial
Pareto is still publishable and the answer asset can land an "acceptable negative" verdict per the
brainstorm's pass-criteria. The S-0090-03 NMDA-calibration follow-up is explicitly held out of t0091
(researcher confirmed in brainstorm 19) so it does NOT compete for this $4.00 envelope.

## Step by Step

**Milestone 1 — Setup & Smoke Gate (Steps 1-3)**

1. **Initialise task code structure.** Create `code/__init__.py`, `code/paths.py`, and
   `code/constants.py`. `paths.py` exposes `RESULTS_DATA_DIR`, `IMAGES_DIR`, `INTERVENTION_DIR`,
   plus the upstream artifact paths (`T0083_PARETO_FRONT_JSON`, `T0083_ALL_EVALUATIONS_JSON`,
   `T0086_CELL_CLASSIFICATION_JSON`, `T0093_POST_FIX_VERIFICATION_SUMMARY_JSON`, `MACHINE_LOG_JSON`)
   and predicted outputs (`PARETO_FRONT_JSON`, `ALL_EVALUATIONS_JSON`, `HV_TRAJECTORY_JSON`,
   `WARM_START_POPULATION_JSON`, `ANCHOR_TRACKING_JSON`, `BIOLOGICAL_SCORECARD_68D_JSON`,
   `BIOLOGICAL_PRIORS_68D_JSON`, `BUDGET_OVERRUN_MD`). `constants.py` defines
   `LOWER_BOUNDS_68 = np.concatenate([LOWER_BOUNDS_54_FROM_T0080, MORPHOLOGY_LOWER_BOUNDS_FROM_T0090])`,
   `UPPER_BOUNDS_68` similarly, `INT_PARAM_INDICES_68` (5 indices), `POP_SIZE = 96`, `N_GEN = 8`,
   `SBX_ETA = 15`, `PM_ETA = 20`, `PM_PROB = 1.0/68`, `T0091_HARD_BUDGET_USD = 4.00`,
   `HV_PLATEAU_REL_THRESHOLD = 0.01`, `HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_MIN_HV_HISTORY = 4`,
   `N_EVAL_SEEDS = 5`, `N_DIRECTIONS = 16`,
   `ANCHOR_NAMES = ("bedb_like", "symmetric", "pd_asymmetric", "nd_asymmetric", "alt_topology")`.
   Satisfies REQ-2, REQ-19.

2. **[CRITICAL] Provision Vast.ai instance via setup-machines orchestrator step.** Search for AMD
   EPYC 7B13 64-core with `cpu_ram>=300 GB`, `disk_space>=40 GB`, `reliability>=0.995`, ordered by
   `dph` ascending. Pick the lowest-rate offer with rate `< $0.35/hr`. Fallback: any 36+ core EPYC
   at `< $0.40/hr` (matches t0086 fallback). Provision via `vastai create instance`. Record full
   `machine_log.json` with `selected_offer.price_per_hour`. Verify SSH connectivity. Set
   `$env:PYTHONIOENCODING="utf-8"` for every PowerShell call. Satisfies REQ-7, REQ-19, REQ-20.

3. **Copy and adapt support modules into `code/`.** Copy from prior tasks per the cross-task reuse
   rule:
   * `code/bootstrap.py` from `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/bootstrap.py`
     (117 lines, no adaptation).
   * `code/build_cell_ais.py` from t0080 (79 lines, update imports to t0091 modules).
   * `code/extend_with_ais.py` from t0080 (127 lines, no adaptation).
   * `code/apply_params.py` from t0080 (228 lines; adapt `_T80_DLL_LOADED` -> `_T91_DLL_LOADED`,
     `resolve_t80_mod_library` -> `resolve_t91_mod_library`, all `tasks.t0080_...` import paths ->
     `tasks.t0091_morphology_extended_nsga2_v1.code...`).
   * `code/parametric_placer.py` from t0080 (105 lines, no adaptation).
   * `code/recorder.py` from t0080 (122 lines, no adaptation).
   * `code/trial_helpers.py` from t0080 (311 lines, no adaptation — `setup_synapses_parametric`
     consumes `DSGCCellWithAIS`-shaped cells, and the t0090/t0092 `MorphologyResult` is duck-typed
     compatible).
   * `code/cost_watchdog.py` from t0086 (132 lines; set `T0091_HARD_BUDGET_USD = 4.00` and rename
     `patch_t0080_loop_rate` -> `patch_t91_loop_rate`).
   * `code/hv_plateau_watchdog.py` from t0083 (118 lines; set `HV_PLATEAU_REL_THRESHOLD = 0.01`,
     `HV_PLATEAU_WINDOW = 2`, `HV_PLATEAU_MIN_HV_HISTORY = 4`).
   * `code/biological_priors.py` from t0086 (179 lines; keep all 9 electrophys priors verbatim; ADD
     4 morphology priors targeting indices 54-67 with explicit `paper_id` references and the prior
     parameters listed in REQ-11). Add a docstring noting that the GABA spatial-gradient prior
     applies to classical-RF SAC-mediated DS only per REQ-22.
   * `code/biological_scorecard.py` from t0088 (198 lines, the corrected-NMDA variant; rename
     `score_clusters` -> `score_pareto_cells` and feed per-Pareto-cell 68-d vectors as
     pseudo-centroids). Copy step satisfies REQ-1 (no t0090.generator imports), REQ-11, REQ-22.

4. **Define the 5 morphology anchors.** Write `code/anchor_definitions.py` with one
   `MorphologyParams` instance per anchor, derived from `BEDB_BASE_POINT` plus the per-anchor
   deviations from the brainstorm 18 table:
   * `bedb_like` = `BEDB_BASE_POINT` (anchor 1).
   * `symmetric` = base with `soma_offset_pd_um=0.0`, `field_elongation_pd=1.0`,
     `branch_density_gradient_pd=0.0`, `primary_branch_pd_concentration=0.0` (anchor 2).
   * `pd_asymmetric` = base with `soma_offset_pd_um=+100.0`, `field_elongation_pd=2.0`,
     `branch_density_gradient_pd=+0.5`, `primary_branch_pd_concentration=+0.5` (anchor 3).
   * `nd_asymmetric` = exact mirror of anchor 3: `soma_offset_pd_um=-100.0`,
     `field_elongation_pd=2.0`, `branch_density_gradient_pd=-0.5`,
     `primary_branch_pd_concentration=-0.5` (anchor 4).
   * `alt_topology` = base with `num_primary_branches=7`, `max_strahler_depth=5`, smaller field
     radius (anchor 5). Save `results/data/anchor_definitions.json` with the 14-d vector per anchor
     for downstream nearest-anchor classification. Expected output: 5-row JSON file. Satisfies
     REQ-4.

**Milestone 2 — Warm-Start Population & Smoke Gate (Steps 5-6)**

5. **Build the 5-anchor x 19-electrophys-clone warm-start population.** Write `code/warmstart.py`.
   Read t0083 `pareto_front.json` (18 cells); read t0086 `cell_classification.json` (Genuine +
   Marginal labels per cell). For each anchor's 14-d morphology vector, sample 19 electrophys
   vectors from the t0083 Pareto preferring Genuine then Marginal cells; if 18 < 19 needed, expand
   from `all_evaluations.json` filtered to non-dominated + Genuine-or-Marginal. Project each
   electrophys vector against `LOWER_BOUNDS_54` / `UPPER_BOUNDS_54` (clamp into bounds). Concatenate
   the 14-d morphology vector with the 54-d electrophys vector for each (anchor, clone) pair to
   produce a 68-d row. Add 1 random LHS sample drawn against the 68-d bounds (last cell). Pack into
   a `(96, 68)` numpy array. Save `results/data/warm_start_population.json` with shape, anchor index
   per row, and source electrophys cell ID per row. Expected output: file with 96 rows, anchor index
   distribution `{0: 19, 1: 19, 2: 19, 3: 19, 4: 19, "random": 1}`. Satisfies REQ-3, REQ-4.

6. **Write per-cell evaluator and smoke-gate. [CRITICAL]** Write `code/generator_wrapper.py` that
   imports
   `from tasks.t0092_diagnose_morphology_generator_silence.code.morphology_generator_fix import generate_fixed_morphology`
   and
   `from tasks.t0092_diagnose_morphology_generator_silence.code.baseline_channels import insert_baseline_channels`,
   plus the t0093 `_LIVE_CELLS` GC-defense list. Write `code/evaluator.py` defining
   `BedBV3MorphProblem(n_var=68, n_obj=3, n_ieq_constr=1)` with `xl=LOWER_BOUNDS_68`,
   `xu=UPPER_BOUNDS_68`. The `_evaluate` method splits the 68-d vector into 14-d morphology + 54-d
   electrophys, looks up the worker-cached cell by morphology hash, rebuilds via
   `generate_fixed_morphology` + `insert_baseline_channels` if hash changed, applies electrophys via
   `apply_parameter_vector`, runs 16 directions x `N_EVAL_SEEDS=5` seeds via `code/trial_driver.py`
   (copied from t0080, line 427, ADAPTED so the worker cache key incorporates a hash of the 14-d
   morph vector — `_worker_prepare(*, params_68d, morph_params, placer_seed)` with
   `_WORKER_MORPH_HASH` global). Outer evaluation seeds are derived deterministically:
   `seeds = list(np.random.SeedSequence(42).spawn(5))`, recorded to
   `results/data/evaluation_seeds.json`. Write `code/smoke_gate.py` (copy from
   `tasks/t0081/code/smoke_gate.py` 145 lines and adapt to evaluate the 5 anchors with the t0083
   best-cell electrophys vector; tolerance DSI <= 0.05, PD-rate <= 1 Hz vs the t0093 60-cell
   post-fix verification fingerprint at the BedB-equivalent point). Run the smoke gate on the
   Vast.ai instance. Expected output: smoke-gate report with all 5 anchors passing or a detailed
   mismatch table for any that fail. **Validation gate**: trivial baseline = anchor 1 (Bed-B-like)
   MUST reproduce the t0093 fingerprint of PD-rate ~43.6 Hz within 1 Hz; if it fails, halt and
   inspect whether `apply_parameter_vector` is wiring the densities to the patched-generator section
   list correctly before launching the 14-16 hour run. Satisfies REQ-1, REQ-8, REQ-9, REQ-18,
   REQ-21.

**Milestone 3 — Joint NSGA-II Run (Step 7)**

7. **[CRITICAL] Run joint 68-d NSGA-II on Vast.ai.** Write `code/nsga2_driver.py` mirroring t0080's
   `nsga2_loop.py` (394 lines):
   ```python
   from pymoo.algorithms.moo.nsga2 import NSGA2
   from pymoo.operators.crossover.sbx import SBX
   from pymoo.operators.mutation.pm import PM
   from pymoo.termination.collection import TerminationCollection
   from pymoo.termination.max_gen import MaximumGenerationTermination

   algorithm = NSGA2(
       pop_size=POP_SIZE,
       sampling=warm_start_array,
       crossover=SBX(eta=SBX_ETA, prob=0.9),
       mutation=PM(eta=PM_ETA, prob=PM_PROB),
       eliminate_duplicates=True,
   )
   termination = TerminationCollection(
       MaximumGenerationTermination(n_max_gen=N_GEN),
       HVPlateauTermination(window=HV_PLATEAU_WINDOW, tol=HV_PLATEAU_REL_THRESHOLD,
                            min_history=HV_PLATEAU_MIN_HV_HISTORY),
       CostWatchdogTermination(max_cost_usd=T0091_HARD_BUDGET_USD),
   )
   result = minimize(problem, algorithm, termination, seed=42, verbose=True)
   ```
   At the start of the run, `make_watchdog_from_machine_log(MACHINE_LOG_JSON)` resolves the actual
   hourly rate and patches `nsga2_driver._HOURLY_RATE_USD`. After every generation the driver writes
   `results/data/hv_trajectory.json`, `results/data/all_evaluations.json` (union pattern from
   t0083), and a per-generation cumulative-spend record (consumed by the orchestrator's cost log).
   `CostWatchdogTermination` evaluates after each generation, never per-cell, to avoid
   mid-generation Pareto corruption. **Validation gate**: after generation 1 completes, inspect the
   HV value and confirm it is >= the warm-start seed HV (no regression) AND that at least 50 of the
   96 cells have feasible `is_unstable=False` evaluations; if either fails, halt before gen 2 and
   inspect 5 individual cell outputs (DSI, PD, stability) before proceeding. Expected final state:
   `result.X` shape `(N_pareto, 68)` with `N_pareto >= 8`, `result.F` shape `(N_pareto, 3)`.
   Satisfies REQ-2, REQ-5, REQ-6, REQ-7, REQ-10.

**Milestone 4 — Pareto + Bio Scorecard (Steps 8-9)**

8. **Extract Pareto front + write final archive.** Write `code/pareto_analysis.py`. Read
   `all_evaluations.json`; extract the non-dominated set across all generations using
   `pymoo.indicators.indicator_factory.NonDominatedSorting().do(F, only_non_dominated_front=True)`
   on the (DSI, PD, robustness) objectives. Write `results/data/pareto_front.json` with per-cell
   68-d parameter vector, 3 objectives, and source-generation index. Expected output: file with
   > =8 rows. Satisfies REQ-10.

9. **Run extended biological scorecard on every Pareto cell.** Use the copied-and-extended
   `code/biological_priors.py` and `code/biological_scorecard.py`:
   ```bash
   $env:PYTHONIOENCODING="utf-8"
   uv run python -u -m arf.scripts.utils.run_with_logs uv run python -u -m \
     tasks.t0091_morphology_extended_nsga2_v1.code.biological_scorecard \
     --pareto results/data/pareto_front.json \
     --priors results/data/biological_priors_68d.json \
     --output results/data/biological_scorecard_68d.json
   ```
   For each Pareto cell, compute (centroid - mean) / sigma per prior, classify as plausible /
   stretched / exotic, aggregate per-cell verdict as worst-case across the 13 priors (9 electrophys
   \+ 4 morphology). Render the heatmap to `results/images/biological_plausibility_heatmap_68d.png`.
   Expected output: per-cell plausibility table; expected `verdict` distribution if no Pareto cell
   reaches biological plausibility (the brainstorm's "acceptable negative" outcome): all rows show
   `verdict="exotic"` driven by NMDA / NaP / GABA priors. Satisfies REQ-11, REQ-12, REQ-22.

**Milestone 5 — Anchor Tracking + Sanity Checks (Steps 10-11)**

10. **Anchor-tracking analysis + cable-theoretic sanity check.** Write `code/anchor_tracking.py`.
    For each Pareto cell:
    * Normalise the 14-d morphology vector via min-max against `MORPHOLOGY_LOWER_BOUNDS` /
      `MORPHOLOGY_UPPER_BOUNDS` (skipping `morph_seed` from the distance computation).
    * Compute Euclidean distance to each of the 5 anchors' normalised 14-d vectors; assign the cell
      to the nearest.
    * Compute v_opt = 2 * lambda_um / tau_m_s for each cell from the cell's electrotonic length and
      membrane time constant (extracted from the morphology + electrophys vectors as in
      `[Anderson1999]`). Tabulate per-anchor counts, total Pareto count, and bootstrap 95% CIs (1000
      resamples sampling each Pareto cell with replacement). Compute one-sided p-value for the
      hypothesis "anchor 3 (pd_asymmetric) over-represented vs anchor 4 (nd_asymmetric)" via exact
      permutation test. Save `results/data/anchor_tracking.json` (counts + CIs + p-value + per-cell
      `nearest_anchor`, `v_opt_um_per_s`). Render `results/images/anchor_tracking_bar.png` (bar
      chart with 95% CI error bars). Satisfies REQ-13, REQ-14.

11. **Hausselt length-vs-DSI test + predictions asset.** Write `code/length_dsi_test.py` to plot
    Pareto-cell DSI vs effective dendritic length and compute Spearman correlation; save
    `results/images/dsi_vs_length.png` and `results/data/length_dsi_correlation.json`. Then create
    the predictions asset:
    `assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/{details.json, description.md, files/pareto_cells.jsonl}`.
    The JSONL has one line per Pareto cell with fields: `cell_id`, `dsi_vector_sum`, `pd_rate_hz`,
    `robustness`, `morphology_vector_14d` (dict of 14 named morphology params),
    `electrophys_vector_54d` (dict of 54 named electrophys params), `nearest_anchor`,
    `verdict_biological`, `v_opt_um_per_s`, `effective_dendritic_length_um`. The `details.json`
    follows the predictions asset spec v2 (`spec_version="2"`, `predictions_id`, `description_path`,
    source task IDs, etc.). Satisfies REQ-15, REQ-16.

**Milestone 6 — Answer Asset + Metrics (Step 12)**

12. **Create answer asset + metrics.json.** Create
    `assets/answer/morphology-extension-biological-plausibility/{details.json, short_answer.md, full_answer.md}`
    per the answer asset spec v2. The question text is verbatim from the brainstorm: "Did enabling
    the 14-d procedural morphology variation as an optimisation axis open biologically-plausible
    joint-pass regions of parameter space that the fixed-Bed-B substrate of t0080-t0088 could not
    reach?". The short answer is 2-5 sentences with a "Yes", "No", or "Partial" lead, no inline
    citations. The full answer is a mini-paper with sections `## Short Answer`, `## Method`,
    `## Evidence from Code or Experiments`, `## Evidence from Papers`,
    `## Evidence from Internet Sources`, `## Conclusion`, `## Limitations`, `## Sources` (with
    markdown reference link definitions for every cited paper / task). `details.json` lists
    `source_paper_ids` (Schachter2010, Briggman2011, Trenholm2013, Sivyer2013, Hausselt2007,
    Tukker2004, Wu2023, Hay2011, Cuntz2010, Anderson1999, Ezra-Tsur2021, Vaney2012, Goethals2020,
    PolegPolsky2016, Sethuramanujam2017, Aldor2024, Ament2023, Riccitelli2025, Ankri2024JPhysiol,
    Roy2024JNeurosci, MullerEgorov2024) and `source_task_ids` (t0078, t0080, t0081, t0083, t0086,
    t0088, t0090, t0092, t0093). Write `results/metrics.json` using the explicit multi-variant
    format with one variant per anchor + one for the full Pareto:
    ```json
    {
      "spec_version": "2",
      "task_id": "t0091_morphology_extended_nsga2_v1",
      "format": "explicit_variants",
      "variants": [
        {"name": "anchor_1_bedb_like", "metric_results": [
            {"metric_key": "direction_selectivity_index", "value": 0.42},
            {"metric_key": "tuning_curve_reliability", "value": 0.83},
            ...
        ]},
        ...
      ]
    }
    ```
    Use only registered metric keys: `direction_selectivity_index` (per-anchor mean DSI),
    `tuning_curve_hwhm_deg` (per-anchor mean HWHM), `tuning_curve_reliability` (per-anchor inverse
    CV across seeds), `tuning_curve_rmse` (mean across Pareto). Other registered `efficiency_*`
    metrics: `efficiency_inference_time_per_item_seconds` is omitted with an explicit comment
    because t0091 does not run inference over a benchmark dataset; the NSGA-II evaluation latency is
    instead saved to `results/data/evaluation_latency.json` for downstream orchestrator consumption.
    `efficiency_training_time_seconds` is omitted because no model is trained. **Validation gate**:
    before computing the per-anchor metric variants, confirm the Pareto front has at least 1 cell
    per anchor; if any anchor has 0 cells in the Pareto, mark its variant with `"value": null` per
    the project style guide ("None for missing data, never zero"). Satisfies REQ-17.

## Remote Machines

Vast.ai EPYC 7B13 64-core CPU instance is required for Phase B (Step 7) and the smoke-gate preflight
(Step 6 final substep). Provisioning criteria (REQ-20): `machine_type=cpu`, `cores>=64`,
`cpu_ram>=300 GB`, `disk_space>=40 GB`, `reliability>=0.995`, `cpu=AMD EPYC 7B13`, order by `dph`
ascending, target rate `< $0.35/hr`. Fallback (matching t0086 pattern): any 36+ core EPYC at
`< $0.40/hr` if no 7B13 available at the target rate within 30 minutes. Image: same Ubuntu 22.04 +
uv image as t0086 / t0093 to keep the NEURON / pymoo stack identical. The instance is destroyed via
the orchestrator's teardown step after Step 7 completes; Phases A, C, D, E (Steps 1, 4, 5, 8-12) run
locally on the developer's 64-core CPU at $0. The cost watchdog reads the actual rate from the
`setup-machines` step's `machine_log.json` `selected_offer.price_per_hour` and patches
`_HOURLY_RATE_USD` per t0086.

## Assets Needed

* **Library asset `procedural_dsgc_morphology_generator`** (from t0090, superseded by C-0093-01 but
  provides `MorphologyParams`, `MorphologyResult`, `BEDB_BASE_POINT`, `PARAM_BOUNDS`, `PARAM_NAMES`,
  `INT_PARAM_NAMES`, `StabilityKind` constants).
* **Library asset `procedural_dsgc_morphology_generator_fix`** (from t0092 --
  `generate_fixed_morphology`, `insert_baseline_channels`; canonical entry point per `C-0093-01`).
* **t0083 Pareto archive**
  (`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/results/data/pareto_front.json`,
  `all_evaluations.json`).
* **t0086 cell classification**
  (`tasks/t0086_robustness_cluster_bio_comparison/results/data/cell_classification.json`).
* **t0093 post-fix verification fingerprint**
  (`tasks/t0093_resweep_and_t0090_correction/results/data/post_fix_verification_summary.json`).
* **t0024 vendored MOD library** (transitively via t0080's `bootstrap.py`).
* **Vast.ai paid compute** (Phase B remote NSGA-II), $3.00-$3.50 expected, $4.00 hard cap.
* **Project budget**: $4.45 USD remaining; t0091 consumes <= $4.00 leaving >= $0.45 buffer.

## Expected Assets

* **Predictions asset** (1, matches `task.json` `expected_assets.predictions=1`):
  `assets/predictions/pareto-front-68d-morphology-extended-bedb-v3/` with `details.json`
  (spec_version 2), `description.md`, and `files/pareto_cells.jsonl` containing per-cell DSI /
  PD-rate / robustness / 14-d morphology / 54-d electrophys / nearest-anchor / biological-verdict /
  v_opt / effective dendritic length. >=8 rows.
* **Answer asset** (1, matches `task.json` `expected_assets.answer=1`):
  `assets/answer/morphology-extension-biological-plausibility/` with `details.json` (spec_version
  2), `short_answer.md`, `full_answer.md`. The question is "Did enabling the 14-d procedural
  morphology variation as an optimisation axis open biologically-plausible joint-pass regions that
  the fixed-Bed-B substrate of t0080-t0088 could not reach?". `answer_methods` includes
  `code-experiment` and `papers`.

## Time Estimation

* **Step 1 (initialise paths/constants)**: ~30 minutes local.
* **Step 2 (provision Vast.ai)**: ~30 minutes including offer search.
* **Step 3 (copy + adapt support modules)**: ~3-4 hours local (mostly mechanical).
* **Step 4 (define anchors)**: ~30 minutes local.
* **Step 5 (build warm-start)**: ~1 hour local.
* **Step 6 (evaluator + smoke gate)**: ~3 hours local + ~10 minutes remote smoke run.
* **Step 7 (NSGA-II remote run)**: ~10-16 hours remote wall-clock (cost watchdog will cap at ~12
  hours = $4.00; HV-plateau may fire earlier at gen 5-7).
* **Step 8 (Pareto extraction)**: ~30 minutes local.
* **Step 9 (biological scorecard)**: ~1 hour local.
* **Step 10 (anchor tracking + v_opt)**: ~2 hours local.
* **Step 11 (length-vs-DSI + predictions asset)**: ~1 hour local.
* **Step 12 (answer asset + metrics.json)**: ~2 hours local.

**Total wall-clock**: ~24-30 hours, dominated by Step 7 remote NSGA-II.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Cost watchdog trips before 8 generations complete (HV not plateaued) | Medium | Partial Pareto only; <8 gens | Document partial Pareto; the brainstorm's "acceptable negative" outcome remains publishable; follow-up suggestion to extend at lower dimensionality (d<=45) per `[Lopez-Camacho-2022]` |
| HV growth stalls at gen 4-5 below 1% threshold (premature plateau before convergence) | Medium | Pareto under-converged; misleading anchor-tracking | Per `[Lopez-Camacho-2022]` auto-config, lowering `eta_m` from 20 to 12-15 widens mutation spread; documented as conditional fallback (DO NOT change without inspecting individual gen-5 cells first) |
| Patched generator instability under NSGA-II mutation extremes | Low | NaN evaluations in Pareto | Penalty objective (large positive) returned for any cell whose simulation NaNs out; t0093's 60/60 STABLE result implies tail-only failures; live-cell GC defense (`_LIVE_CELLS`) prevents the t0080 cell-id-reuse class of bug |
| Smoke gate fails (anchor 1 BedB-like does not reproduce t0093 PD-rate ~43.6 Hz) | Low | Run blocked before launch | Halt; inspect `apply_parameter_vector` against the patched-generator section list; verify `insert_baseline_channels` was called before `apply_parameter_vector`; re-run smoke gate; do NOT launch the remote NSGA-II until anchor 1 reproduces within tolerance |
| Vast.ai EPYC 7B13 unavailable at <$0.35/hr | Low | Fallback EPYC at <$0.40/hr | Documented offer-search fallback; cost estimate already includes the upper-rate scenario in the $4.00 cap |
| Anchor 4 ND-asymmetric warm-start cells unstable (mirror-image cell silent) | Low | Anchor-tracking bias against ND-asymmetric | Smoke gate evaluates ALL 5 anchors; if anchor 4 fails, replace with a near-symmetric variant for the warm-start and document the substitution in the answer asset |
| Project budget exhausted by t0091 ($4.00 of $4.45 = 90%) | Low | No buffer for follow-ups | Cost watchdog hard cap is $4.00; expected central is $3.00-$3.50 leaving ~$1.00; if exceeded, post-t0091 follow-ups defer until budget refresh |
| Worker cache morphology-hash collision causes cell reuse with wrong morphology | Low | Silent wrong-cell evaluation | Hash both 14-d morphology AND 54-d electrophys; smoke gate's known-good fingerprint catches collisions; assert hash uniqueness across worker for first 96 evaluations |
| Windows `cp1252` codec breaks on `≥` Unicode in aggregator output | High | Pre-commit / verificator fails locally | Set `$env:PYTHONIOENCODING="utf-8"` for every `uv run` call; documented in REQ-19 |

## Verification Criteria

* **Plan file structure**: run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0091_morphology_extended_nsga2_v1` and
  confirm exit code 0 with 0 errors.
* **Research files exist and pass spec checks**: run
  `uv run python -u -m arf.scripts.verificators.verify_research_papers t0091_morphology_extended_nsga2_v1`,
  `verify_research_internet`, and `verify_research_code` and confirm 0 errors each.
* **Answer asset passes verification**: run
  `uv run python -u -m arf.scripts.verificators.verify_answer_asset t0091_morphology_extended_nsga2_v1`
  and confirm 0 errors. The asset must exist at
  `tasks/t0091_morphology_extended_nsga2_v1/assets/answer/morphology-extension-biological-plausibility/`
  with `details.json` (spec_version 2), `short_answer.md`, and `full_answer.md`.
* **Predictions asset passes verification**: run
  `uv run python -u -m arf.scripts.verificators.verify_predictions_asset t0091_morphology_extended_nsga2_v1`
  and confirm 0 errors. The JSONL must have >=8 rows and per-row keys `cell_id`, `dsi_vector_sum`,
  `pd_rate_hz`, `robustness`, `morphology_vector_14d`, `electrophys_vector_54d`, `nearest_anchor`,
  `verdict_biological`, `v_opt_um_per_s`, `effective_dendritic_length_um`.
* **Pareto front size**: run
  `python -c "import json; print(len(json.load(open('tasks/t0091_morphology_extended_nsga2_v1/results/data/pareto_front.json'))['cells']))"`
  and confirm output `>=8`.
* **Cost compliance**: run
  `uv run python -u -m arf.scripts.aggregators.aggregate_costs --task-ids t0091_morphology_extended_nsga2_v1`
  and confirm `cost_usd <= 4.00`.
* **Cost-rate provenance**: confirm `results/costs.json`
  `breakdown.vast_ai.actual_rate_usd_per_hour` matches the resolved `selected_offer.price_per_hour`
  from the setup-machines `machine_log.json`.
* **REQ coverage**: run
  `python -c "import re; p=open('tasks/t0091_morphology_extended_nsga2_v1/plan/plan.md').read(); print(sum(1 for _ in re.finditer(r'^\| REQ-\d+', p, re.M)))"`
  and confirm output `>=22`. Cross-check that every REQ-id appears at least once in
  `## Step by Step` section's `Satisfies` annotations.
* **No t0090 generator import**: run
  `grep -r "from tasks.t0090.*import generate_morphology" tasks/t0091_morphology_extended_nsga2_v1/code/`
  and confirm zero matches (REQ-1).
* **Smoke gate result**: confirm
  `tasks/t0091_morphology_extended_nsga2_v1/logs/steps/<smoke-gate>/smoke_gate_report.json` has
  `anchor_1.dsi_within_tolerance=true` and `anchor_1.pd_within_tolerance=true`.
* **Anchor-tracking bootstrap**: confirm `results/data/anchor_tracking.json` has fields
  `bootstrap_n_resamples=1000`, `pd_vs_nd_p_value` (float), and per-anchor `count_ci95_lo`,
  `count_ci95_hi`.
* **Metrics format**: confirm `results/metrics.json` `format == "explicit_variants"` and every
  `metric_key` is one of `direction_selectivity_index`, `tuning_curve_hwhm_deg`,
  `tuning_curve_reliability`, `tuning_curve_rmse`.
