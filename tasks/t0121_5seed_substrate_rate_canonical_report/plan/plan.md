---
spec_version: "2"
task_id: "t0121_5seed_substrate_rate_canonical_report"
date_completed: "2026-05-24"
status: "complete"
---
# Plan: Canonical 5-Seed Substrate-Rate Report (S-0112-01 Batch Closed)

## Objective

Produce one canonical, self-contained write-up that consolidates the five separate-task LEGIT
joint-pass acceptance-rate measurements from the S-0112-01 substrate-rate confirmation batch (t0106
seed 44, t0112 seed 77, t0113 seed 2247, t0114 seed 7755, t0115 seed 9354) on the 68-d Bed B
electrophysiology + 14-d morphology NSGA-II substrate. Re-load each source task's raw NSGA-II
evaluation dump, recompute every per-seed acceptance rate under the canonical t0115 LEGIT-only
convention (`n_legit_joint_pass_unique / n_total_evals * 100`, where LEGIT means
`DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999`), surface a convention-drift reconciliation table
that exposes the silence-guard-included numbers historically published by t0113 and t0114, compute
the 5-seed mean / sample SD / sample SE plus 95% confidence intervals using both the
normal-approximation and a fixed-seed bootstrap (`numpy.random.default_rng(seed=42)`, `B=10000`,
2.5/97.5 percentiles), document the HV-plateau auto-stop and pool-restart-cadence protocol drift
across the five source tasks, and place the headline rate side by side with Hay 2011 (0.40% full
envelope, 0.0104% perisomatic-only bottleneck), Druckmann 2007 (0.10% baseline), and Mohacsi 2024
(20-60 gen convergence band). Produce three CSVs, one pooled parquet, three charts, and one answer
asset answering the canonical substrate-rate question. **Done** means: (1) every per-seed acceptance
rate produced by the new code matches the t0115 `substrate_rate_5seed.csv` headline numbers within
rounding (seed 44 = 3.2318%, seed 77 = 0.3472%, seed 2247 = 0.0000%, seed 7755 = 8.1317%, seed 9354
= 1.1932%); (2) the 5-seed mean / SE reproduces 2.58% / 1.50% within rounding; (3) the
convention-drift table prints the silence-guard-included headline numbers from t0114's
`joint_pass_summary_4seeds.csv` next to the canonical LEGIT-only numbers for the three impacted
seeds (44, 2247, 7755); (4) the three charts and the pooled parquet are saved with the file names
listed in `## Expected Assets`; (5) one answer asset is written under
`assets/answer/substrate-rate-5seed-canonical/` with both `short_answer.md` and `full_answer.md`
files and passes the answer-asset verificator. The task ends with chart and CSV production; the
orchestrator handles `results_summary.md`, `results_detailed.md`, `compare_literature.md`,
`suggestions.json`, `costs.json`, and reporting steps.

* * *

## Task Requirement Checklist

Operative task text from `tasks/t0121_5seed_substrate_rate_canonical_report/task.json` and the
resolved long description at
`tasks/t0121_5seed_substrate_rate_canonical_report/task_description.md`:

```text
Name: Canonical 5-seed substrate-rate report (S-0112-01 batch closed)

Short description: Pure write-up consolidating t0106 / t0112 / t0113 / t0114 / t0115 5-seed
LEGIT joint-pass acceptance rate into one canonical document with harmonised conventions and
Hay 2011 / Druckmann 2007 comparisons.

Dependencies: t0106_long_pdnd_nsga2_300gen, t0112_t0106_seed77_replicate,
t0113_t0106_seed2247_replicate, t0114_seed7755_no_autostop, t0115_seed9354_no_autostop,
t0119_brainstorm_results_23.
Expected assets: 1 answer.
Task types: data-analysis, comparative-analysis, answer-question.
Source suggestion: S-0115-02.

Long description (excerpts):

* Pure write-up. No new simulation, no new NSGA-II runs. Re-read the 5 source tasks' results
  parquets and produce one consolidated canonical document plus one answer asset.
* Re-read source data: load each of the 5 tasks' pareto_front_seed*.json (or equivalent) and
  all_evaluations_seed*.json if available. Verify total evaluation counts match the per-seed
  reports (3744, 2016, 1344, 5952, 5280).
* Harmonise conventions: re-compute LEGIT joint-pass count per seed using the canonical
  definition (DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999). Cross-check against each
  task's reported number; flag and document any discrepancies.
* Compute 5-seed statistics: per-seed acceptance rate, 5-seed mean, sample SD, sample SE,
  95% CI (normal approx), 95% CI (bootstrap with B=10000), and counts of seeds beating Hay
  envelope.
* Comparison table: harmonise with Hay 2011's 0.40% upper envelope and 0.0104% perisomatic
  bottleneck, and with Druckmann 2007's 0.10% baseline.
* Per-seed convergence-trajectory comparison: HV trajectory, plateau generation, total
  evaluations, wall-clock per generation.
* Charts: (a) per-seed acceptance rate bar chart with Hay/Druckmann reference lines,
  (b) 5-seed HV-trajectory overlay (one trace per seed), (c) DSI-vs-PD scatter for the
  pooled LEGIT joint-pass cells colored by seed.
* Answer asset: write one answer asset answering "What is the LEGIT joint-pass acceptance
  rate on the 68-d Bed B + 14-d morphology substrate, estimated from a 5-seed random-init
  NSGA-II batch, and how does it compare to Hay 2011 and Druckmann 2007?"
* Expected outputs: per_seed_substrate_rate_5seed.csv, pooled_legit_jointpass_cells.parquet,
  per_seed_acceptance_bar.png, hv_trajectory_5seed_overlay.png,
  dsi_pd_scatter_5seed_pooled.png, assets/answer/substrate-rate-5seed-canonical/.
* Budget: Local CPU only, no remote machines. Estimate <$0.20.
* Verification criteria: All 5 per-seed acceptance rates match the source task reports within
  rounding. 5-seed mean and SE match the brainstorm-session-23 summary (2.58% +/- 1.50%)
  within rounding. Charts saved and embedded in results_detailed.md. Answer asset passes
  verify_answer_asset (or local fallback).
```

Concrete requirements decomposed into stable `REQ-*` items:

* **REQ-1**: Re-load each of the 5 source tasks' raw NSGA-II evaluation dumps. Verify the per-task
  total-evaluation counts equal **3744 (t0106 seed 44), 2016 (t0112 seed 77), 1344 (t0113 seed
  2247), 5952 (t0114 seed 7755), 5280 (t0115 seed 9354)**. Satisfied by Step 5. Evidence: stdout
  print of `n_total_evals` per seed; assertion in `code/main.py` halts the run on mismatch.

* **REQ-2**: Re-compute per-seed LEGIT joint-pass count using the canonical predicate
  `DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999` (the t0115 convention; the LEGIT ceiling
  excludes silence-guard / single-spike evaluator artefacts at `DSI = 1.0`). Satisfied by Step 6.
  Evidence: per-seed `n_legit_unique` printed to stdout and written to
  `results/data/per_seed_substrate_rate_5seed.csv`.

* **REQ-3**: Cross-check the recomputed per-seed numbers against each source task's reported number;
  flag and document the convention drift between (a) t0113 / t0114's `joint_pass_summary_*seeds.csv`
  headline numbers (silence-guard included) and (b) t0115's canonical LEGIT-only numbers. Satisfied
  by Step 7. Evidence: `results/data/convention_drift_5seed.csv` with columns `seed`, `task_id`,
  `legacy_joint_pass_pct`, `canonical_legit_pct`, `delta_pct`, `convention`.

* **REQ-4**: Compute 5-seed mean, sample SD, sample SE, 95% CI (normal approximation), and 95% CI
  (bootstrap with `B=10000`, fixed seed `numpy.random.default_rng(seed=42)`, 2.5/97.5 percentile).
  Verify mean and SE reproduce 2.58% / 1.50% within rounding. Satisfied by Step 8. Evidence:
  `results/data/substrate_stats_5seed.csv` with columns `metric`, `value`, `normal_approx_lo`,
  `normal_approx_hi`, `bootstrap_lo`, `bootstrap_hi`.

* **REQ-5**: Count how many of the five seeds individually beat the Hay 2011 envelope upper bound
  (0.40%). Satisfied by Step 8. Evidence: `n_seeds_above_hay_envelope` row in
  `results/data/substrate_stats_5seed.csv` (expected value: 3 — seeds 44, 7755, 9354).

* **REQ-6**: Build a literature-comparison table positioning the 5-seed mean against Hay 2011 (0.40%
  full envelope, 0.0104% perisomatic-only bottleneck), Druckmann 2007 (0.10% baseline), and Mohacsi
  2024 (20-60 gen convergence band). Satisfied by Step 9. Evidence:
  `results/data/literature_comparison_5seed.csv` with columns `study`, `rate_pct`, `substrate_d`,
  `notes`, `cite_paper_id`.

* **REQ-7**: Per-seed convergence-trajectory comparison covering HV trajectory, plateau generation,
  total evaluations, and wall-clock per generation. Satisfied by Steps 5 and 10. Evidence:
  `results/data/per_seed_convergence_5seed.csv` (one row per seed: `n_generations_completed`,
  `final_hypervolume`, `stop_trigger`, `wall_clock_per_gen_s`, `pool_restart_every`,
  `hv_plateau_autostop`) and the HV-trajectory overlay chart from Step 11.

* **REQ-8**: Document the HV-plateau auto-stop and pool-restart-cadence protocol drift across the
  five source tasks: t0106 ran with `_POOL_RESTART_EVERY = 25` and auto-stop enabled; t0112 used
  cadence 10 with auto-stop enabled; t0113 used cadence 10 with auto-stop enabled and the detector
  fired prematurely at gen 14; t0114 and t0115 used cadence 10 with auto-stop disabled. Satisfied by
  Step 7. Evidence: `convention` column in `convention_drift_5seed.csv` and dedicated
  `protocol_drift_notes` column in `per_seed_convergence_5seed.csv`.

* **REQ-9**: Produce chart `results/images/per_seed_acceptance_bar.png` — per-seed acceptance-rate
  bar chart with Hay 2011 (0.40%) and Druckmann 2007 (0.10%) reference lines and both normal-approx
  SE and bootstrap-CI error bars on the 5-seed mean bar. Satisfied by Step 11. Evidence: file
  exists; file size > 5 KB.

* **REQ-10**: Produce chart `results/images/hv_trajectory_5seed_overlay.png` — 5-seed
  HV-trajectory overlay (one trace per seed) with pool-restart-cadence annotations using the
  canonical t0115 `SEED_COLORS`, `SEED_MARKERS`, `SEED_LABELS` visual key. Satisfied by Step 11.
  Evidence: file exists; file size > 5 KB.

* **REQ-11**: Produce chart `results/images/dsi_pd_scatter_5seed_pooled.png` — pooled DSI-vs-PD
  scatter of the LEGIT joint-pass cells across all five seeds, colored by seed. Satisfied by Step
  11\. Evidence: file exists; file size > 5 KB.

* **REQ-12**: Write `results/data/pooled_legit_jointpass_cells.parquet` — one row per LEGIT
  joint-pass cell across all five seeds with columns `seed`, `source_task_id`, `generation`, `dsi`,
  `pd_rate_hz`, `cell_id`. Satisfied by Step 6. Evidence: file exists; row count equals
  `121 + 7 + 0 + 484 + 63 = 675`.

* **REQ-13**: Write one answer asset at `assets/answer/substrate-rate-5seed-canonical/` with
  `details.json`, `short_answer.md`, and `full_answer.md`, answering "What is the LEGIT joint-pass
  acceptance rate on the 68-d Bed B + 14-d morphology substrate, estimated from a 5-seed random-init
  NSGA-II batch, and how does it compare to Hay 2011 and Druckmann 2007?" with confidence `medium`.
  Satisfied by Step 12. Evidence: three files exist; answer-asset verificator passes with zero
  errors.

* **REQ-14**: Cite the t0106 `t0106-joint-pass-recovery-2dir` answer asset in the new answer's
  `source_task_ids` as the 1-seed predecessor that this 5-seed batch supersedes. Satisfied by Step
  12\. Evidence: presence of `t0106_long_pdnd_nsga2_300gen` in the new answer's `source_task_ids`,
  plus an explicit prose reference in `full_answer.md`.

* **REQ-15**: Document the t0113 zero-LEGIT censoring caveat (premature HV-plateau auto-stop at gen
  14 below the Mohacsi 2024 20-60 convergence band) as the dominant uncertainty in the lower tail of
  the 5-seed mean. Satisfied by Step 12 (inside `full_answer.md` `## Limitations`). Evidence:
  explicit "censoring artefact" language in the answer's `## Limitations` section.

* **REQ-16**: Local CPU only. No remote machines. Total estimated cost below **$0.20**. Satisfied by
  the entire plan; cost recorded in `## Cost Estimation` and confirmed at orchestrator's
  `costs.json` step (out of scope for this plan).

* * *

## Approach

### Technical approach

The work decomposes into three layers. The **data layer** re-reads each of the five source tasks'
raw NSGA-II evaluation dumps (`all_evaluations_seed<N>.json[.gz]`, `hv_trajectory_seed<N>.json`,
`pareto_front_seed<N>.json`) using a single suffix-branching loader that handles both gzipped JSON
(t0106 / t0112 / t0113) and plain JSON (t0114 / t0115). The **statistics layer** applies the
canonical LEGIT predicate per cell, deduplicates by `cell_id`, counts per-seed unique LEGIT
joint-pass cells, then computes the 5-seed mean / sample SD / sample SE / normal-approximation 95%
CI / bootstrap 95% CI. The **presentation layer** emits four CSVs, one parquet, three PNG charts,
and one answer asset that wraps the canonical numbers in a literature-grounded narrative.

The single most important transform is the **convention harmonisation**. t0113's
`joint_pass_summary_3seeds.csv` and t0114's `joint_pass_summary_4seeds.csv` published the acceptance
rate as `n_joint_pass_unique / n_total_evals * 100`, which **includes silence-guard ceiling cells at
`DSI = 1.0`** (the single-spike evaluator artefact). t0115 switched to
`n_legit_joint_pass_unique / n_total_evals * 100` (LEGIT-only, the convention required by this
task). The drift is consequential: under the silence-guard-included convention, t0114 reported seed
7755 at **12.95%** (771 / 5952); under the canonical LEGIT-only convention, it is **8.13%** (484 /
5952). The plan exposes this drift in `convention_drift_5seed.csv` so the canonical reporting cannot
be misread.

### Key research findings that ground the approach

* **Result-data layout is uniform across all 5 source tasks** (per code-research finding #1) — one
  loader handles all five. The `_load_evaluations` / `_load_hv` / `_load_pareto_cells` helpers in
  `tasks/t0115_seed9354_no_autostop/code/build_results.py:222-240` are battle-tested and copyable.

* **t0106 and t0113 evaluations live under `assets/predictions/`** (per code-research finding #2),
  not under `results/data/`. The path resolver must consult t0115's `T0106_EVALS` / `T0113_EVALS`
  constants (`build_results.py:54-76`) rather than glob `results/data/`.

* **t0115 LEGIT-only convention is canonical** (per code-research finding #3 and project memory note
  "Adopt the t0115 LEGIT convention as the canonical definition"). The LEGIT predicate
  `DSI >= 0.5 AND PD-rate >= 30 Hz AND DSI < 0.9999` is encapsulated in t0115's
  `_is_legit_joint_pass` (`build_results.py:261-266`).

* **The five canonical per-seed numbers are pinned**: 121 / 3744 = 3.2318% (seed 44), 7 / 2016 =
  0.3472% (seed 77), 0 / 1344 = 0.0000% (seed 2247), 484 / 5952 = 8.1317% (seed 7755), 63 / 5280 =
  1.1932% (seed 9354). 5-seed mean = 2.5808%, sample SD = 3.3471%, sample SE = 1.4969%. Normal-
  approx 95% CI = (-0.36%, +5.52%). These are the verification anchors for REQ-1, REQ-2, REQ-4.

* **Bootstrap-CI helper is new code** (per code-research finding #9). No reusable helper exists in
  the project; the implementation is approximately five lines of `numpy`:
  `rng = np.random.default_rng(seed=42); samples = rng.choice(rates, size=(10000, 5), replace=True).mean(axis=1); lo, hi = np.percentile(samples, [2.5, 97.5])`.

* **Literature numbers are already pinned** in t0114's and t0115's `compare_literature.md`: Hay 2011
  = 0.40% full envelope (~2000 accepted / 500,000 evals on 22-d L5b pyramidal cell;
  `[Hay2011, p. 4]`), 0.0104% perisomatic-only bottleneck (52 / 500,000; `[Hay2011, p. 6]`);
  Druckmann 2007 = 0.10% baseline (300 / 300,000 on 12-d cortical interneuron;
  `[Druckmann2007, Fig 3 + Methods]`); Mohacsi 2024 = 20-60 gen convergence band on 3-12 param
  problems (`[Mohacsi2024, Fig 4]`). Paper assets are at
  `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`,
  `tasks/t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/`, and
  `tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/`.

* **Code reuse strategy**: copy approximately 500-600 lines from t0115's `build_results.py` (1,514
  lines total) into focused t0121 modules (`paths.py`, `constants.py`, `seed_metadata.py`,
  `loaders.py`, `stats.py`, `csv_writers.py`, `charts.py`, `main.py`) rather than recreate the
  monolith. No library asset is registered — per project convention, cross-task code reuse for
  this task is **copy-and-rewrite-imports**.

### Alternatives considered and rejected

1. **Import t0115's `build_results.py` directly without copying.** Rejected: the project has no
   registered library asset wrapping t0115's code; cross-task imports outside `arf/` are forbidden
   per the project's task-isolation rule. The only legitimate cross-task reuse path is copy-
   and-adapt.

2. **Single-file `build_results.py` monolith inheriting t0115's structure verbatim.** Rejected:
   t0114 (1,674 lines) and t0115 (1,514 lines) both became unwieldy single-file monoliths mixing
   loaders, CSV writers, chart builders, and asset writers. The code-research lesson explicitly
   recommends splitting into focused modules (`paths.py` / `loaders.py` / `stats.py` /
   `csv_writers.py` / `charts.py`). Estimated reduction: ~600 lines split across 5 modules vs the
   upstream 1,514-line monolith.

3. **Skip the bootstrap CI and report only the normal-approximation CI as t0115 did.** Rejected: the
   task description explicitly requires both, and with `n = 5` the normal approximation under-covers
   heavily skewed empirical distributions (one zero, one large value at 8.13%). The bootstrap CI is
   a robustness check that the report explicitly needs to publish.

4. **Recompute everything from the strict-Pareto `pareto_front_seed<N>.json` files instead of the
   full evaluation dumps.** Rejected: per-seed denominators (`n_total_evals`) must come from the
   full evaluation dump, not the Pareto subset. The Pareto JSON is appropriate only for the DSI-PD
   scatter (cross-check) and is not the canonical input.

### Recommended task types

Per `task.json` the recommended task types are already set: `data-analysis`, `comparative-analysis`,
`answer-question`. All three apply:

* **data-analysis** drives the per-seed acceptance-rate recompute, the convention-drift table, and
  the chart suite. Its Planning Guidelines (define questions upfront, list metrics and chart types,
  decide statistical tests during planning) shaped REQ-1 through REQ-12.

* **comparative-analysis** drives the literature-comparison table and the side-by-side Hay 2011 /
  Druckmann 2007 / Mohacsi 2024 framing. Its Planning Guidelines (define comparison dimensions
  upfront, fair-comparison criteria, structured comparison tables) shaped REQ-6 and the
  literature-comparison CSV schema. No new training or inference is performed, so the `efficiency_*`
  registered metrics do not apply.

* **answer-question** drives the single answer asset. Its Planning Guidelines (one answer per
  question, name the answer ID upfront, identify evidence channels, define stopping criterion)
  shaped REQ-13 through REQ-15 and the `## Expected Assets` answer specification.

### Registered metrics applicability

Per Phase 1 step 7, the registered metrics are `direction_selectivity_index`,
`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`. **None of the four
applies** to this task because the task performs no new simulation — it re-reads pre-computed
NSGA-II evaluations whose DSI and PD-rate fields are already finalised in the source-task
predictions assets and are aggregated here as a percentage rather than reported per-cell. The LEGIT
joint-pass acceptance rate is the central quantity of this report but is **not** a registered
project metric. No metric measurement step is included; this omission is deliberate.

* * *

## Cost Estimation

* LLM API calls: **$0.00** — no API calls are made by the implementation scripts.
* Remote compute: **$0.00** — all loading, statistics, and chart generation runs on local CPU.
  Estimated wall-clock for the full pipeline is under 5 minutes (largest single input is t0114's
  `all_evaluations_seed7755.json` at ~30 MB plain JSON).
* Storage: **$0.00** — outputs total approximately 5-10 MB (three PNGs + four small CSVs + one
  small parquet).
* Total estimated cost: **$0.00** in third-party fees. The task description ceiling of **<$0.20** is
  preserved as an upper bound for unforeseen utility costs (none expected).

Project budget context: `project/budget.json` declares a total project budget of $100.00 with a
per-task default limit of $8.00. This task consumes none of that. Well below both limits.

* * *

## Step by Step

### Milestone 1: Code scaffolding (Steps 1-4)

1. **Create the per-task `paths.py`.** Create `code/paths.py` defining the absolute path constants
   for the source-task evaluation dumps and the t0121 outputs. Resolve the repository root via the
   idiom `_THIS_FILE = Path(__file__).resolve()`, `TASK_ROOT = _THIS_FILE.parent.parent`,
   `REPO_ROOT = TASK_ROOT.parent.parent` (copy from
   `tasks/t0115_seed9354_no_autostop/code/paths.py:14-16`). Define input constants per code-
   research finding #2 (use `assets/predictions/` paths for t0106 and t0113; use `results/data/`
   paths for t0112, t0114, t0115):
   `T0106_EVALS = REPO_ROOT / "tasks/t0106_long_pdnd_nsga2_300gen/assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz"`,
   `T0112_EVALS`,
   `T0113_EVALS = REPO_ROOT / "tasks/t0113_t0106_seed2247_replicate/assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz"`,
   `T0114_EVALS`, `T0115_EVALS` (mirror t0115's `build_results.py:54-95`). Define output constants:
   `OUT_DATA_DIR = TASK_ROOT / "results/data"`, `OUT_IMAGES_DIR = TASK_ROOT / "results/images"`,
   `CSV_PER_SEED = OUT_DATA_DIR / "per_seed_substrate_rate_5seed.csv"`,
   `CSV_CONVENTION_DRIFT = OUT_DATA_DIR / "convention_drift_5seed.csv"`,
   `CSV_STATS = OUT_DATA_DIR / "substrate_stats_5seed.csv"`,
   `CSV_CONVERGENCE = OUT_DATA_DIR / "per_seed_convergence_5seed.csv"`,
   `CSV_LITERATURE = OUT_DATA_DIR / "literature_comparison_5seed.csv"`,
   `PARQUET_POOLED = OUT_DATA_DIR / "pooled_legit_jointpass_cells.parquet"`,
   `CHART_ACCEPTANCE_BAR = OUT_IMAGES_DIR / "per_seed_acceptance_bar.png"`,
   `CHART_HV_OVERLAY = OUT_IMAGES_DIR / "hv_trajectory_5seed_overlay.png"`,
   `CHART_DSI_PD_SCATTER = OUT_IMAGES_DIR / "dsi_pd_scatter_5seed_pooled.png"`. Expected observable:
   `code/paths.py` exists and
   `uv run python -c "from tasks.t0121_5seed_substrate_rate_canonical_report.code.paths import CSV_PER_SEED; print(CSV_PER_SEED)"`
   prints the absolute path with no `ImportError`. Satisfies the path-centralisation precondition
   for every subsequent step.

2. **Create the per-task `constants.py`.** Create `code/constants.py` by copying the threshold and
   literature constants from `tasks/t0115_seed9354_no_autostop/code/build_results.py:98-107`:
   `DSI_THRESHOLD = 0.5`, `PD_RATE_THRESHOLD_HZ = 30.0`, `LEGIT_DSI_CEILING = 0.9999`,
   `SILENCE_GUARD_DSI = 1.0`, `HAY_2011_RATE_PCT = 0.40`, `DRUCKMANN_2007_RATE_PCT = 0.10`. Add the
   new constant `HAY_2011_PERISOMATIC_RATE_PCT = 0.0104` (cited but not pinned in t0115). Add the
   bootstrap constants `BOOTSTRAP_B = 10000`, `BOOTSTRAP_SEED = 42`,
   `BOOTSTRAP_PERCENTILES = (2.5, 97.5)`. Add the canonical 5-seed verification anchors as
   constants:
   `EXPECTED_N_EVALS = {"seed_44": 3744, "seed_77": 2016, "seed_2247": 1344, "seed_7755": 5952, "seed_9354": 5280}`,
   `EXPECTED_LEGIT_COUNT = {"seed_44": 121, "seed_77": 7, "seed_2247": 0, "seed_7755": 484, "seed_9354": 63}`.
   Expected observable: import succeeds; the six rate constants print correctly. Satisfies REQ-2
   precondition.

3. **Create `code/seed_metadata.py`.** Copy the canonical visual key and per-seed metadata block
   from `tasks/t0115_seed9354_no_autostop/code/build_results.py:109-182` verbatim: `SEED_COLORS`,
   `SEED_MARKERS`, `SEED_LABELS`, `POOL_RESTART_CADENCE`, `ALL_SEED_KEYS`, `ASSET_DECLARED`. Verify
   the `POOL_RESTART_CADENCE` dict captures the **drift**:
   `{"seed_44": 25, "seed_77": 10, "seed_2247": 10, "seed_7755": 10, "seed_9354": 10}`. Add a
   parallel `HV_AUTOSTOP_ENABLED` dict capturing the auto-stop convention:
   `{"seed_44": True, "seed_77": True, "seed_2247": True, "seed_7755": False, "seed_9354": False}`
   (per code-research finding #6). Expected observable: import succeeds; `ALL_SEED_KEYS` contains
   all five canonical keys. Satisfies REQ-8 precondition.

4. **Create `code/loaders.py`.** Copy the four loader helpers from
   `tasks/t0115_seed9354_no_autostop/code/build_results.py:222-266` into `code/loaders.py`:
   `_load_evaluations(*, path: Path) -> list[dict]` (with suffix-branch on `.gz`),
   `_load_hv(*, path: Path) -> list[dict]`, `_load_pareto_cells(*, path: Path) -> list[dict]`, and
   the `_is_legit_joint_pass(*, dsi: float, pd_rate_hz: float) -> bool` predicate. Adapt all imports
   to use the new t0121 namespace. Add explicit type aliases at module top:
   `type EvalRecord = dict[str, Any]`, `type HvRecord = dict[str, Any]`. Expected observable:
   `uv run python -c "from tasks.t0121_5seed_substrate_rate_canonical_report.code.loaders import _load_evaluations, _is_legit_joint_pass; print('ok')"`
   prints `ok`. Satisfies REQ-1 and REQ-2 preconditions.

### Milestone 2: Recompute per-seed numbers and reconcile conventions (Steps 5-7)

5. **Implement `code/per_seed.py` (per-seed acceptance recompute).** Create `code/per_seed.py` that
   defines `@dataclass(frozen=True, slots=True) PerSeedSummary` with fields `seed_key: str`,
   `task_id: str`, `n_total_evals: int`, `n_legit_unique: int`, `acceptance_rate_pct: float`,
   `n_generations_completed: int`, `final_hypervolume: float`, `stop_trigger: str`,
   `wall_clock_per_gen_s: float | None`. Implement
   `summarize_seed(*, seed_key: str, eval_path: Path, hv_path: Path, task_id: str) -> PerSeedSummary`
   that loads evaluations + HV trajectory, deduplicates evaluations by `cell_id`, counts unique
   LEGIT joint-pass cells using `_is_legit_joint_pass`, computes
   `acceptance_rate_pct = n_legit_unique / n_total_evals * 100`, derives `n_generations_completed`
   and `final_hypervolume` from the last HV record, `wall_clock_per_gen_s` from
   `(last_elapsed_s - first_elapsed_s) / (n_gen - 1)` when at least 2 HV records exist (`None`
   otherwise — never `0.0`), and the `stop_trigger` from the last HV record's metadata if present
   (else infer from `HV_AUTOSTOP_ENABLED` and the gen count). After computing each `PerSeedSummary`,
   **assert** `summary.n_total_evals == EXPECTED_N_EVALS[seed_key]` and
   `summary.n_legit_unique == EXPECTED_LEGIT_COUNT[seed_key]` with a positive assertion message
   ("seed_44 total evals is 3744"). The asserts implement REQ-1 verification. Expected observable:
   each per-seed summary prints to stdout in the format
   `seed_44 t0106_long_pdnd_nsga2_300gen 3744 evals 121 LEGIT 3.2318%`. Satisfies REQ-1, REQ-2,
   REQ-7.

6. **Implement `code/pool.py` (pooled LEGIT cells parquet writer).** Create `code/pool.py` that
   defines
   `build_pooled_legit_cells(*, eval_paths: dict[str, Path], task_ids: dict[str, str]) -> pd.DataFrame`
   which iterates the 5 seeds, loads each evaluation dump via `_load_evaluations`, filters with
   `_is_legit_joint_pass`, deduplicates by `cell_id`, and returns a DataFrame with explicit dtypes
   `{"seed": pd.StringDtype(), "source_task_id": pd.StringDtype(), "generation": pd.Int64Dtype(), "dsi": np.dtype("float64"), "pd_rate_hz": np.dtype("float64"), "cell_id": pd.StringDtype()}`.
   Use `pandas.DataFrame.to_parquet(path, index=False)` to write `PARQUET_POOLED`. After write,
   **assert** `len(df) == sum(EXPECTED_LEGIT_COUNT.values()) == 675`. Expected observable:
   `PARQUET_POOLED` exists with 675 rows; stdout prints
   `pooled_legit_jointpass_cells.parquet: 675 rows written`. Satisfies REQ-12.

7. **Implement `code/convention_drift.py` (convention-drift reconciliation table).** Create
   `code/convention_drift.py` that builds `convention_drift_5seed.csv` with one row per seed.
   Columns: `seed`, `task_id`, `legacy_joint_pass_pct`, `legacy_convention`, `canonical_legit_pct`,
   `delta_pct`, `protocol_notes`. The **legacy numbers come from the pinned task-published
   headlines** (do not recompute the legacy numbers — they are the historical artefacts being
   reconciled). Hardcoded as a module-level constant
   `LEGACY_REPORTED_PCT = {"seed_44": 3.2318, "seed_77": 0.3472, "seed_2247": 0.1488, "seed_7755": 12.9536, "seed_9354": 1.1932}`
   with source
   `LEGACY_SOURCE = {"seed_44": "t0114 joint_pass_summary_4seeds.csv (LEGIT)", "seed_77": "t0114 joint_pass_summary_4seeds.csv (LEGIT)", "seed_2247": "t0114 joint_pass_summary_4seeds.csv (silence-guard included)", "seed_7755": "t0114 joint_pass_summary_4seeds.csv (silence-guard included)", "seed_9354": "t0115 substrate_rate_5seed.csv (canonical LEGIT)"}`
   (per code- research finding #3; t0106 / t0112 already happen to match the LEGIT convention
   because their silence-guard cells contributed nothing, so `delta_pct = 0` for those two). The
   `protocol_notes` column carries the auto-stop and pool-restart-cadence drift narrative per seed
   (e.g., seed_2247: "HV-plateau auto-stop fired prematurely at gen 14, below the Mohacsi 2024 20-60
   convergence band; t0114 / t0115 disabled auto-stop in response per S-0113-03"). Expected
   observable: `CSV_CONVENTION_DRIFT` exists with 5 data rows; the printed table shows
   `delta_pct = -4.82` for seed 7755 (canonical 8.13% minus legacy 12.95%) and `delta_pct = -0.15`
   for seed 2247. Satisfies REQ-3, REQ-8.

### Milestone 3: Statistics and literature comparison (Steps 8-9)

8. **Implement `code/stats.py` (5-seed statistics and bootstrap CI).** Create `code/stats.py` that
   defines `@dataclass(frozen=True, slots=True) SubstrateStats` with fields `mean_pct: float`,
   `sample_sd_pct: float`, `sample_se_pct: float`, `normal_approx_ci_lo_pct: float`,
   `normal_approx_ci_hi_pct: float`, `bootstrap_ci_lo_pct: float`, `bootstrap_ci_hi_pct: float`,
   `n_seeds_above_hay_envelope: int`. Implement
   `compute_substrate_stats(*, summaries: dict[str, PerSeedSummary]) -> SubstrateStats` that
   collects the five `acceptance_rate_pct` values, computes mean via `np.mean`, sample SD via
   `np.std(rates, ddof=1)`, sample SE via `sd / sqrt(5)`, normal-approx 95% CI as
   `mean +/- 1.96 * se`, bootstrap CI via
   `rng = np.random.default_rng(seed=BOOTSTRAP_SEED); samples = rng.choice(rates, size=(BOOTSTRAP_B, 5), replace=True).mean(axis=1); lo, hi = np.percentile(samples, BOOTSTRAP_PERCENTILES)`,
   and `n_seeds_above_hay_envelope = sum(1 for r in rates if r > HAY_2011_RATE_PCT)`. After
   computing, **assert** `abs(stats.mean_pct - 2.58) < 0.01` and
   `abs(stats.sample_se_pct - 1.50) < 0.01` (verifies REQ-4 against the brainstorm-session-23
   anchor) and `stats.n_seeds_above_hay_envelope == 3` (verifies REQ-5). Write
   `substrate_stats_5seed.csv` with one row per metric. Expected observable: stdout prints
   `5-seed mean = 2.58 +/- SE 1.50; normal-approx 95% CI = (-0.36, 5.52); bootstrap 95% CI = (...) ; n_seeds > Hay = 3`.
   Satisfies REQ-4, REQ-5.

   **Note on validation gates**: This task performs no inference, no model training, no paid API
   calls, and processes far fewer than 100 items (the largest single dataset is ~6 K evaluation
   records). Validation gates per the planning skill's expensive-operation rule do not apply. The
   assert-against-anchor pattern in Step 5 and Step 8 provides equivalent end-to-end verification:
   if the recomputed per-seed counts or the 5-seed mean / SE deviate from the pinned canonical
   numbers, the script halts with a clear AssertionError before any chart or answer asset is
   written.

9. **Implement `code/literature.py` (literature comparison table).** Create `code/literature.py`
   that writes `literature_comparison_5seed.csv` with one row per literature reference plus one row
   for the 5-seed canonical estimate. Hardcoded rows (per code-research finding #7 and the project
   memory note pinning Hay 2011 0.40% envelope, 0.0104% perisomatic bottleneck, Druckmann 2007
   0.10%, and Mohacsi 2024 20-60 gen numbers from the prior t0114 and t0115 literature-comparison
   documents):

   * `study="Hay 2011 full envelope", rate_pct=0.40, substrate_d=22, notes="500K evals on L5b pyramidal cell; full perisomatic + back-propagating AP fits", cite_paper_id="10.1371_journal.pcbi.1002107"`
   * `study="Hay 2011 perisomatic-only", rate_pct=0.0104, substrate_d=22, notes="52 accepted / 500K evals; substrate-limited counterexample", cite_paper_id="10.1371_journal.pcbi.1002107"`
   * `study="Druckmann 2007 baseline", rate_pct=0.10, substrate_d=12, notes="300 accepted / 300K evals on cortical interneuron", cite_paper_id="10.3389_neuro.01.1.1.001.2007"`
   * `study="Mohacsi 2024 convergence band", rate_pct=null, substrate_d=null, notes="NSGA-II asymptotes 20-60 gen on 3-12 param problems", cite_paper_id="10.1371_journal.pcbi.1012039"`
   * `study="This work 5-seed mean", rate_pct=<stats.mean_pct>, substrate_d=68, notes="t0106/t0112/t0113/t0114/t0115 5-seed LEGIT; normal-approx 95% CI inserted", cite_paper_id=null`

   Use `None` (rendered as null JSON / blank CSV cell) for missing rate / substrate-d values, never
   `0.0` (per project style guide). Expected observable: `CSV_LITERATURE` exists with 5 data rows.
   Satisfies REQ-6.

### Milestone 4: Charts (Steps 10-11)

10. **Implement `code/convergence.py` (per-seed convergence-trajectory CSV).** Create
    `code/convergence.py` that builds `per_seed_convergence_5seed.csv` with one row per seed.
    Columns: `seed`, `task_id`, `n_generations_completed`, `n_total_evals`, `final_hypervolume`,
    `stop_trigger`, `wall_clock_per_gen_s`, `pool_restart_every`, `hv_plateau_autostop`,
    `protocol_drift_notes`. Pull values from each `PerSeedSummary` and from `POOL_RESTART_CADENCE` /
    `HV_AUTOSTOP_ENABLED` in `seed_metadata.py`. The `protocol_drift_notes` column carries the
    per-seed protocol narrative (e.g., seed_44: "Legacy cadence 25; auto-stop fired at gen 39 with
    hypervolume plateau"; seed_2247: "Cadence 10; auto-stop fired prematurely at gen 14 below
    Mohacsi convergence band — zero LEGIT plausibly censoring artefact"; seed_7755: "Cadence 10;
    auto-stop DISABLED; operator stop at gen 62 after visible plateau"). Expected observable:
    `CSV_CONVERGENCE` exists with 5 data rows; printed table shows `pool_restart_every` flips from
    25 (seed_44) to 10 (others) and `hv_plateau_autostop` flips from True (44/77/2247) to False
    (7755/9354). Satisfies REQ-7, REQ-8.

11. **Implement `code/charts.py` (three required charts).** Create `code/charts.py` with three chart
    functions. All three must set `matplotlib.use("Agg")` before importing `matplotlib.pyplot` (per
    code-research finding "Common Patterns") and use the canonical visual key from
    `seed_metadata.py` (`SEED_COLORS`, `SEED_MARKERS`, `SEED_LABELS`).

    * `chart_per_seed_acceptance_bar(*, summaries: dict[str, PerSeedSummary], stats: SubstrateStats) -> Path`:
      per-seed bar chart with seeds on the x-axis and acceptance-rate percent on the y-axis. Add a
      horizontal dashed red line at `HAY_2011_RATE_PCT = 0.40` labelled "Hay 2011 envelope (0.40%)"
      and a horizontal dashed orange line at `DRUCKMANN_2007_RATE_PCT = 0.10` labelled "Druckmann
      2007 (0.10%)". Add a 6th bar at the right for the 5-seed mean with **two error bars** — one
      normal-approx (caps at `stats.normal_approx_ci_lo_pct` / `stats.normal_approx_ci_hi_pct`)
      drawn in black, and one bootstrap (caps at `stats.bootstrap_ci_lo_pct` /
      `stats.bootstrap_ci_hi_pct`) drawn in slate-grey, with a legend disambiguating them. Title:
      "5-seed LEGIT joint-pass acceptance rate vs Hay 2011 and Druckmann 2007". Save to
      `CHART_ACCEPTANCE_BAR`. Adapted from t0115's `chart_substrate_rate_5seed_with_literature`
      (`build_results.py:826-891`); the delta is the additional bootstrap error bar (the upstream
      chart has only the normal-approx SE bar). Satisfies REQ-9.

    * `chart_hv_trajectory_5seed_overlay(*, hv_traces: dict[str, list[dict]]) -> Path`: 5-seed HV
      trajectory overlay with generation on the x-axis and hypervolume on the y-axis, one line per
      seed using `SEED_COLORS` / `SEED_MARKERS` / `SEED_LABELS`. Annotate pool-restart events as
      faint dotted vertical lines (every 25 generations for seed_44, every 10 generations for the
      other four seeds, per `POOL_RESTART_CADENCE`). Mark the auto-stop / operator-stop point for
      each seed with an `X` marker. Add a faint shaded vertical band from x=20 to x=60 labelled
      "Mohacsi 2024 convergence band". Title: "5-seed HV trajectory overlay (t0106 / t0112 / t0113 /
      t0114 / t0115)". Save to `CHART_HV_OVERLAY`. Adapted from t0115's `chart_hv_vs_gen_5seeds`
      (`build_results.py:702-740`). Satisfies REQ-10.

    * `chart_dsi_pd_scatter_5seed_pooled(*, pooled_df: pd.DataFrame) -> Path`: scatter plot of the
      pooled LEGIT-joint-pass cells with PD-rate (Hz) on the x-axis and DSI on the y-axis, colored
      by `seed` (5 colors from `SEED_COLORS`), marker shape from `SEED_MARKERS`. Add a horizontal
      dashed black line at `DSI_THRESHOLD = 0.5` labelled "DSI threshold (0.5)" and a vertical
      dashed black line at `PD_RATE_THRESHOLD_HZ = 30.0` labelled "PD-rate threshold (30 Hz)". Add a
      horizontal dashed grey line at `LEGIT_DSI_CEILING = 0.9999` labelled "LEGIT ceiling". Title:
      "Pooled LEGIT joint-pass cells (DSI vs PD-rate), 5-seed canonical batch". Save to
      `CHART_DSI_PD_SCATTER`. New chart (not in t0115); the scatter is broader than t0115's
      `chart_pareto_front_5seeds` because it shows all LEGIT cells, not just the strict Pareto
      front. Satisfies REQ-11.

    Expected observable: all three PNG files exist; each is > 5 KB. Charts visually pass the
    description above (operator review).

### Milestone 5: Answer asset (Step 12)

12. **Implement `code/answer_asset.py` (write the substrate-rate canonical answer asset).** Create
    `code/answer_asset.py` that materialises `assets/answer/substrate-rate-5seed-canonical/` with
    three files conforming to `meta/asset_types/answer/specification.md` v2:

    * `details.json`: `spec_version: "2"`, `answer_id: "substrate-rate-5seed-canonical"`,
      `question: "What is the LEGIT joint-pass acceptance rate on the 68-d Bed B + 14-d morphology NSGA-II substrate, estimated from a 5-seed random-init batch, and how does it compare to Hay 2011 and Druckmann 2007?"`,
      `short_title: "5-seed substrate-rate canonical estimate"`,
      `short_answer_path: "short_answer.md"`, `full_answer_path: "full_answer.md"`,
      `categories: ["direction-selectivity", "compartmental-modeling"]`,
      `answer_methods: ["code-experiment", "papers"]`,
      `source_paper_ids: ["10.1371_journal.pcbi.1002107", "10.3389_neuro.01.1.1.001.2007", "10.1371_journal.pcbi.1012039"]`,
      `source_urls: []`,
      `source_task_ids: ["t0106_long_pdnd_nsga2_300gen", "t0112_t0106_seed77_replicate", "t0113_t0106_seed2247_replicate", "t0114_seed7755_no_autostop", "t0115_seed9354_no_autostop", "t0078_bedb_mobo_v2_ais_tiered_ahp", "t0097_multi_obj_optim", "t0102_seedscale_n4_gen20"]`,
      `confidence: "medium"`, `created_by_task: "t0121_5seed_substrate_rate_canonical_report"`,
      `date_created: "2026-05-24"`. The `medium` confidence reflects the small sample (n=5), the
      wide CI that brackets both literature baselines and zero, and the t0113 censoring caveat.
      Satisfies REQ-13, REQ-14.

    * `short_answer.md`: YAML frontmatter per spec, then `## Question` (verbatim from
      `details.json`), then `## Answer` (2-5 sentences, direct, no inline citations, no hedging
      beyond what the data demands; state the 2.58% point estimate with normal-approx and bootstrap
      CIs, the 3-of-5-seeds-above-Hay finding, and that the CI cannot rule out the Hay or Druckmann
      baselines), then `## Sources` (bulleted list of the three paper IDs and the eight task IDs
      from `details.json`). Satisfies REQ-13.

    * `full_answer.md`: YAML frontmatter per spec (`confidence: "medium"`), then `## Question`
      (verbatim), `## Short Answer` (matches the short answer's `## Answer` verbatim, citation-
      free), `## Research Process` (describe re-loading the five source-task evaluation dumps,
      applying the LEGIT predicate, recomputing per-seed acceptance under the canonical convention,
      computing the 5-seed statistics with both normal-approx and bootstrap CIs, assembling the
      literature comparison), `## Evidence from Papers` (cite `[Hay2011]`, `[Druckmann2007]`,
      `[Mohacsi2024]` inline with the canonical numbers from each),
      `## Evidence from Internet Sources` (state explicitly that the internet method was not used
      — all evidence is from project papers and code experiments),
      `## Evidence from Code or Experiments` (cite `[t0106]`, `[t0112]`, `[t0113]`, `[t0114]`,
      `[t0115]` inline with the per-seed numbers, and reference `[t0106_joint_pass_recovery]` as the
      1-seed predecessor this 5-seed batch supersedes — satisfies REQ-14), `## Synthesis` (the
      point estimate is 6.5x Hay and 25.8x Druckmann but the CI cannot reject either baseline; three
      of five seeds individually beat the Hay envelope; the convention-drift reconciliation matters
      because t0114's pre-correction headline of 12.95% for seed 7755 is a silence-guard artefact
      under the historical convention), `## Limitations` (the t0113 zero is plausibly a censoring
      artefact from premature HV-plateau auto-stop at gen 14, below the Mohacsi 2024 20-60
      convergence band — satisfies REQ-15; n=5 is small; the S-0113-03 detector reparameterisation
      `(W*, T*) = (3, 0.015)` was computed offline but never adopted in production), `## Sources`
      (bulleted list of paper IDs and task IDs, followed by markdown reference link definitions:
      `[Hay2011]: ../../../t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/summary.md`,
      `[Druckmann2007]: ../../../t0097_multi_obj_optim/assets/paper/10.3389_neuro.01.1.1.001.2007/summary.md`,
      `[Mohacsi2024]: ../../../t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/summary.md`,
      `[t0106_joint_pass_recovery]: ../../../t0106_long_pdnd_nsga2_300gen/assets/answer/t0106-joint-pass-recovery-2dir/`,
      plus relative `[tNNNN]` links to each of the five source-task folders). Satisfies REQ-13,
      REQ-14, REQ-15.

    Expected observable: three files exist; running
    `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.verificators.verify_answer_asset t0121_5seed_substrate_rate_canonical_report`
    prints zero errors.

### Milestone 6: Top-level orchestrator (Step 13)

13. **Implement `code/main.py` (orchestrator).** Create `code/main.py` whose `main()` function runs
    the pipeline in dependency order: Step 5 (compute the five `PerSeedSummary`), Step 6 (build and
    write pooled parquet), Step 7 (write convention-drift CSV), Step 10 (write convergence CSV),
    Step 8 (compute and write stats CSV), Step 9 (write literature CSV), Step 11 (build the three
    charts), Step 12 (write the answer asset). Wrap the top-level in `if __name__ == "__main__":`
    and parse no command-line arguments (no `--limit` is required since the task has no
    expensive-operation step). Print a one-line completion summary
    `wrote 5 CSVs, 1 parquet, 3 charts, 1 answer asset to tasks/t0121_5seed_substrate_rate_canonical_report/`.
    Run via
    `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0121_5seed_substrate_rate_canonical_report -- uv run python -u -m tasks.t0121_5seed_substrate_rate_canonical_report.code.main`.
    Expected observable: the completion line prints; all 9 output files exist; the per-seed asserts
    in Step 5 and the stats asserts in Step 8 all pass. Satisfies the end-to-end integration of
    REQ-1 through REQ-13.

* * *

## Remote Machines

None required. The task is a pure write-up; all computation runs on local CPU in under 5 minutes.
Largest single input file is t0114's `all_evaluations_seed7755.json` at ~30 MB plain JSON. No GPU,
no large-memory worker, no remote provisioning. Reasoning: total runtime is bounded by reading five
JSON dumps (total ~80 MB across all five), applying a vectorisable LEGIT predicate, computing
5-element statistics, and rendering three matplotlib PNGs — all trivially CPU-local.

* * *

## Assets Needed

* **t0106_long_pdnd_nsga2_300gen** — provides seed 44 NSGA-II evaluation dump under
  `assets/predictions/nsga2-seed44-bedb-morph-2dir-300gen/files/all_evaluations_seed44.json.gz` plus
  `results/data/hv_trajectory_seed44.json` and `results/data/pareto_front_seed44.json`. Also
  provides the predecessor answer asset `t0106-joint-pass-recovery-2dir` cited as REQ-14 evidence.

* **t0112_t0106_seed77_replicate** — provides seed 77 NSGA-II evaluation dump under
  `results/data/all_evaluations_seed77.json.gz` plus the matching HV and Pareto JSONs.

* **t0113_t0106_seed2247_replicate** — provides seed 2247 NSGA-II evaluation dump under
  `assets/predictions/t0113-bedb-morph-nsga2-seed2247/files/all_evaluations_seed2247.json.gz` plus
  the matching HV and Pareto JSONs.

* **t0114_seed7755_no_autostop** — provides seed 7755 NSGA-II evaluation dump under
  `results/data/all_evaluations_seed7755.json` plus the matching HV and Pareto JSONs.

* **t0115_seed9354_no_autostop** — provides seed 9354 NSGA-II evaluation dump under
  `results/data/all_evaluations_seed9354.json` plus the matching HV and Pareto JSONs. Also provides
  the canonical `build_results.py` (1,514 lines) from which approximately 500-600 lines of loaders,
  summariser, stats, CSV writers, and chart builders are copied into the new t0121 modules.

* **t0078_bedb_mobo_v2_ais_tiered_ahp** — hosts the Hay 2011 paper asset
  (`assets/paper/10.1371_journal.pcbi.1002107/`) cited via relative path in the answer asset.

* **t0097_multi_obj_optim** — hosts the Druckmann 2007 paper asset
  (`assets/paper/10.3389_neuro.01.1.1.001.2007/`) cited via relative path in the answer asset.

* **t0102_seedscale_n4_gen20** — hosts the Mohacsi 2024 paper asset
  (`assets/paper/10.1371_journal.pcbi.1012039/`) cited via relative path in the answer asset.

* **t0119_brainstorm_results_23** — commissioned this task via suggestion S-0115-02; provides the
  5-seed mean / SE anchor (2.58% +/- 1.50%) that the Step 8 assert reproduces.

No external URLs, no new datasets, no remote machines needed.

* * *

## Expected Assets

* **1 answer asset** (matches `task.json` `expected_assets.answer = 1`):
  `assets/answer/substrate-rate-5seed-canonical/` — contains `details.json`, `short_answer.md`,
  `full_answer.md`. Answers the canonical substrate-rate question for the 68-d Bed B + 14-d
  morphology NSGA-II substrate based on the 5-seed S-0112-01 batch, with the 2.58% point estimate in
  context of Hay 2011 (0.40% envelope, 0.0104% perisomatic bottleneck) and Druckmann 2007 (0.10%
  baseline). Confidence: medium (n=5, wide CI, t0113 censoring caveat). Two evidence methods:
  `code-experiment` (the recompute and statistics pipeline in this task) and `papers` (the three
  literature baselines).

No new datasets, libraries, models, predictions, or papers. The task is a pure write-up; the single
asset deliverable is the answer asset.

In addition to the answer asset, the task writes the following non-asset outputs to `results/data/`
and `results/images/` (these are not registered asset types but are required by the task description
and the verification criteria):

* `results/data/per_seed_substrate_rate_5seed.csv` — per-seed acceptance rates and totals.
* `results/data/convention_drift_5seed.csv` — legacy-vs-canonical reconciliation table.
* `results/data/substrate_stats_5seed.csv` — 5-seed mean / SD / SE / both 95% CIs.
* `results/data/per_seed_convergence_5seed.csv` — per-seed convergence trajectory summary.
* `results/data/literature_comparison_5seed.csv` — Hay / Druckmann / Mohacsi side-by-side table.
* `results/data/pooled_legit_jointpass_cells.parquet` — 675-row pooled LEGIT cells parquet.
* `results/images/per_seed_acceptance_bar.png` — per-seed bar chart with literature reference
  lines.
* `results/images/hv_trajectory_5seed_overlay.png` — 5-seed HV overlay with cadence annotations.
* `results/images/dsi_pd_scatter_5seed_pooled.png` — pooled LEGIT-cell DSI-vs-PD scatter.

* * *

## Time Estimation

* Research stages (papers / internet / code): **already complete**.
* Planning (this step): **completed at this commit**.
* Implementation:
  * Steps 1-4 (scaffolding `paths.py`, `constants.py`, `seed_metadata.py`, `loaders.py`): ~15
    minutes.
  * Steps 5-7 (per-seed recompute, pooled parquet, convention-drift CSV): ~25 minutes.
  * Steps 8-10 (stats CSV, literature CSV, convergence CSV): ~20 minutes.
  * Step 11 (three charts): ~30 minutes.
  * Step 12 (answer asset): ~30 minutes.
  * Step 13 (orchestrator + end-to-end run): ~10 minutes.
  * **Implementation total**: approximately 130 minutes (~2 hours 10 minutes).
* Remote compute: **none**.
* Verification (verificators + asset checks): ~10 minutes.
* Orchestrator-managed downstream steps (results writing, compare-literature, suggestions,
  reporting): out of scope for this plan — handled by execute-task.

**Total wall-clock from planning end to implementation end**: approximately 2 hours 20 minutes.

* * *

## Risks & Fallbacks

Pre-mortem: imagine the task has failed. What went wrong?

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| The per-seed `n_total_evals` recomputed from each source dump does not equal the pinned headline number (3744, 2016, 1344, 5952, 5280), indicating a path-resolution bug or a dedup-by-cell_id miscount | Low | Blocking | Step 5 asserts `n_total_evals == EXPECTED_N_EVALS[seed_key]` per seed with positive message ("seed_44 total evals is 3744"). If the assert trips, halt and diagnose by (a) printing the file path being read, (b) comparing the live `len(evaluations_dedup)` against the source task's `n_cells_total` field in its `details.json` predictions metadata. If a true mismatch is found, write an intervention file documenting the source-dump corruption. |
| The per-seed `n_legit_unique` recomputed under the LEGIT predicate does not match the pinned canonical headline (121 / 7 / 0 / 484 / 63), indicating a threshold drift between the copied `_is_legit_joint_pass` and the upstream t0115 version | Low | Blocking | Step 5 asserts `n_legit_unique == EXPECTED_LEGIT_COUNT[seed_key]` per seed. If the assert trips, halt and diff the t0121 `_is_legit_joint_pass` against `tasks/t0115_seed9354_no_autostop/code/build_results.py:261-266` byte for byte. The thresholds `DSI_THRESHOLD = 0.5`, `PD_RATE_THRESHOLD_HZ = 30.0`, `LEGIT_DSI_CEILING = 0.9999` are also asserted to equal the pinned values at module import time. |
| The 5-seed mean or SE recomputed in Step 8 does not match the brainstorm-session-23 anchor (2.58% / 1.50%) within rounding | Low | Blocking | Step 8 asserts `abs(stats.mean_pct - 2.58) < 0.01` and `abs(stats.sample_se_pct - 1.50) < 0.01`. If the assert trips, halt and inspect the five per-seed rates that fed the computation; the most likely cause is an off-by-one in the `ddof` argument to `np.std`. |
| The convention-drift table mislabels a seed's legacy convention (e.g., claims t0106 was silence-guard-included when it was actually LEGIT-by-coincidence because no silence-guard cells appeared) | Medium | Documentation error | The legacy numbers are hardcoded from the source task CSVs (t0114's `joint_pass_summary_4seeds.csv` for seeds 44, 77, 2247, 7755; t0115's `substrate_rate_5seed.csv` for seed 9354). The `legacy_convention` column is documented per cell. Mitigation: cross-check the t0114 CSV directly before hardcoding the values; if any legacy number differs from the canonical recompute by less than 0.001%, mark the convention as "LEGIT-by-coincidence" rather than asserting silence-guard inclusion. |
| The pooled parquet has the wrong row count (not equal to 675 = 121+7+0+484+63), indicating a dedup or filter mismatch between the per-seed counter (Step 5) and the pooled builder (Step 6) | Medium | Blocking | Step 6 asserts `len(df) == sum(EXPECTED_LEGIT_COUNT.values()) == 675` post-write. The per-seed counter and the pooled builder share the same `_is_legit_joint_pass` predicate and the same dedup-by-`cell_id` rule; a divergence is most likely caused by a per-seed file-path bug. If the assert trips, halt and emit per-seed row counts from the pooled DataFrame to localise the mismatch. |
| The answer asset fails the `verify_answer_asset` verificator (missing section, malformed details.json, broken reference link) | Medium | Blocking | Step 12 explicitly enumerates every mandatory section per `meta/asset_types/answer/specification.md` v2. After writing, run the verificator and iterate until zero errors. The most common failure mode in prior tasks has been the `## Sources` reference-link block missing one of the relative paths — the plan lists all required `[Xxxx]:` definitions in Step 12. |
| A source-task evaluation dump path resolved by `paths.py` does not exist (e.g., t0106's gzipped predictions file was moved or never existed at the stated path) | Low | Blocking | At module import time, `paths.py` does not stat the files (no eager IO); but Step 4's `_load_evaluations` raises a clear `FileNotFoundError` with the full absolute path. If raised, halt and cross-check against `tasks/t0115_seed9354_no_autostop/code/build_results.py:54-95` for the canonical path constants. The historical t0106 / t0113 paths under `assets/predictions/...` are confirmed extant in the code-research file. |
| The bootstrap CI implementation has a bug (wrong axis, wrong percentile, non-reproducible due to unfixed seed) | Low | Subtle quality issue | The bootstrap helper uses an explicit `numpy.random.default_rng(seed=42)` (constant `BOOTSTRAP_SEED = 42`), a single named call to `rng.choice(rates, size=(10000, 5), replace=True).mean(axis=1)`, and `np.percentile(samples, (2.5, 97.5))`. Mitigation: the same seed and size produce a deterministic CI; if a future re-run produces a different number, the bug is in the helper, not the data. |
| Charts saved successfully but the visual key drifts from the canonical t0115 colors / markers (so the canonical report is visually inconsistent with the upstream per-seed reports) | Medium | Cosmetic / interpretability | Step 3 copies `SEED_COLORS`, `SEED_MARKERS`, `SEED_LABELS` from t0115 verbatim and Step 11 imports them from `seed_metadata.py`. The visual key is centralised; no chart hardcodes per-seed colors locally. |

* * *

## Verification Criteria

* **VC-1 (file existence + counts; covers REQ-1, REQ-2, REQ-4, REQ-9, REQ-10, REQ-11, REQ-12,
  REQ-13)**: Run the end-to-end pipeline via
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0121_5seed_substrate_rate_canonical_report -- uv run python -u -m tasks.t0121_5seed_substrate_rate_canonical_report.code.main`
  and confirm the completion line
  `wrote 5 CSVs, 1 parquet, 3 charts, 1 answer asset to tasks/t0121_5seed_substrate_rate_canonical_report/`
  appears on stdout. Then confirm all of the following files exist with non-empty contents (>0
  bytes): `results/data/per_seed_substrate_rate_5seed.csv`,
  `results/data/convention_drift_5seed.csv`, `results/data/substrate_stats_5seed.csv`,
  `results/data/per_seed_convergence_5seed.csv`, `results/data/literature_comparison_5seed.csv`,
  `results/data/pooled_legit_jointpass_cells.parquet`, `results/images/per_seed_acceptance_bar.png`,
  `results/images/hv_trajectory_5seed_overlay.png`,
  `results/images/dsi_pd_scatter_5seed_pooled.png`,
  `assets/answer/substrate-rate-5seed-canonical/details.json`,
  `assets/answer/substrate-rate-5seed-canonical/short_answer.md`,
  `assets/answer/substrate-rate-5seed-canonical/full_answer.md`. Each PNG > 5 KB; the parquet has
  exactly 675 rows.

* **VC-2 (canonical-number reproduction; covers REQ-1, REQ-2, REQ-4, REQ-5)**: Run the end-to-end
  pipeline from VC-1 and confirm stdout contains the per-seed lines
  `seed_44 t0106_long_pdnd_nsga2_300gen 3744 evals 121 LEGIT 3.2318%`,
  `seed_77 t0112_t0106_seed77_replicate 2016 evals 7 LEGIT 0.3472%`,
  `seed_2247 t0113_t0106_seed2247_replicate 1344 evals 0 LEGIT 0.0000%`,
  `seed_7755 t0114_seed7755_no_autostop 5952 evals 484 LEGIT 8.1317%`,
  `seed_9354 t0115_seed9354_no_autostop 5280 evals 63 LEGIT 1.1932%`, and the summary line
  `5-seed mean = 2.58 +/- SE 1.50; ...; n_seeds > Hay = 3`. All five per-seed asserts
  (`n_total_evals == EXPECTED_N_EVALS[k]`, `n_legit_unique == EXPECTED_LEGIT_COUNT[k]`) and both
  stats asserts (`abs(mean - 2.58) < 0.01`, `abs(se - 1.50) < 0.01`,
  `n_seeds_above_hay_envelope == 3`) must pass.

* **VC-3 (plan-verificator pass)**: Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0121_5seed_substrate_rate_canonical_report -- uv run python -m arf.scripts.verificators.verify_plan t0121_5seed_substrate_rate_canonical_report`
  and confirm zero errors. Warnings about word counts are tolerable but must be reviewed.

* **VC-4 (answer-asset verificator pass; covers REQ-13)**: Run
  `PYTHONIOENCODING=utf-8 uv run python -m arf.scripts.utils.run_with_logs --task-id t0121_5seed_substrate_rate_canonical_report -- uv run python -m arf.scripts.verificators.verify_answer_asset t0121_5seed_substrate_rate_canonical_report`
  (or the local-fallback equivalent if the dedicated verificator does not exist on this branch) and
  confirm zero errors against the single answer asset `substrate-rate-5seed-canonical/`. Confirm
  `details.json` lists `t0106_long_pdnd_nsga2_300gen` in `source_task_ids` (REQ-14 evidence) and the
  three paper IDs `10.1371_journal.pcbi.1002107`, `10.3389_neuro.01.1.1.001.2007`,
  `10.1371_journal.pcbi.1012039` in `source_paper_ids`.

* **VC-5 (requirement-coverage check; covers REQ-1 through REQ-16)**: Open `plan/plan.md` and
  confirm every `REQ-*` item listed in `## Task Requirement Checklist` is referenced by at least one
  step in `## Step by Step`. Then open each output file from VC-1 and confirm the schema matches the
  description in the step that produces it (e.g., `convention_drift_5seed.csv` has the columns
  `seed`, `task_id`, `legacy_joint_pass_pct`, `legacy_convention`, `canonical_legit_pct`,
  `delta_pct`, `protocol_notes`; `substrate_stats_5seed.csv` has rows for `mean_pct`,
  `sample_sd_pct`, `sample_se_pct`, `normal_approx_ci_lo_pct`, `normal_approx_ci_hi_pct`,
  `bootstrap_ci_lo_pct`, `bootstrap_ci_hi_pct`, `n_seeds_above_hay_envelope`).

* **VC-6 (Python style + type check; covers all implementation steps)**: Run
  `PYTHONIOENCODING=utf-8 uv run ruff check tasks/t0121_5seed_substrate_rate_canonical_report/code`,
  `PYTHONIOENCODING=utf-8 uv run ruff format --check tasks/t0121_5seed_substrate_rate_canonical_report/code`,
  and `PYTHONIOENCODING=utf-8 uv run mypy tasks/t0121_5seed_substrate_rate_canonical_report/code`
  and confirm zero errors.

* **VC-7 (Markdown style; covers `plan.md` and the answer asset markdown files)**: Run
  `PYTHONIOENCODING=utf-8 uv run flowmark --inplace --nobackup tasks/t0121_5seed_substrate_rate_canonical_report/plan/plan.md`
  and the equivalent commands for `short_answer.md` and `full_answer.md`. Confirm no unexpected
  rewraps remain.
