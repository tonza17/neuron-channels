# ✅ Reproduce t0126 with signed DSI=(PD-ND)/(PD+ND) and real per-cell firing rates

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0129_t0126_signed_dsi_real_rates_1seed` |
| **Status** | ✅ completed |
| **Started** | 2026-05-26T12:29:51Z |
| **Completed** | 2026-05-26T21:05:00Z |
| **Duration** | 8h 35m |
| **Dependencies** | [`t0126_bedb_dsi_atp_per_spike_nsga2_60gen`](../../../overview/tasks/task_pages/t0126_bedb_dsi_atp_per_spike_nsga2_60gen.md) |
| **Task types** | `experiment-run`, `data-analysis`, `comparative-analysis` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`voltage-gated-channels`](../../by-category/voltage-gated-channels.md) |
| **Expected assets** | 1 predictions, 1 answer |
| **Step progress** | 11/15 |
| **Cost** | **$0.97** |
| **Task folder** | [`t0129_t0126_signed_dsi_real_rates_1seed/`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/task_description.md)*

# Reproduce t0126 with signed DSI and real per-cell firing rates

## Motivation

t0126 (`bedb_dsi_atp_per_spike_nsga2_60gen`) ran an NSGA-II optimisation of the Bed B DSGC
over a 68-d morphology + electrophysiology parameter vector with objective `F =
[-dsi_vector_sum, +atp_per_spike_molecules]`. Two design choices in that task limit the
downstream interpretability of its Pareto front and are corrected here:

1. **Vector-sum DSI** (`_vector_sum_dsi` in `tasks/t0126_*/code/evaluator.py:356`) collapses
   the antipodal pair `[0°, 180°]` to a non-negative scalar `|PD - ND| / (PD + ND)`. The sign
   is discarded, so cells that fire *more* to ND than PD (anti-preferred response) look
   identical to cells with a true preferred-direction bias of the same magnitude. The standard
   direction-selective ganglion cell (DS-RGC) literature uses the **signed** ratio `DSI =
   (R_PD - R_ND) / (R_PD + R_ND)`, range `[-1, 1]`, so direction reversals are detectable.

2. **`pd_rate_hz` placeholder**: per project memory `project_t0126_cell_trace_synthesised.md`,
   the `cell_trace` artefact in t0126 was hand-synthesised after the run, with `pd_rate_hz =
   40` used as a hard-coded placeholder for every cell. The per-direction firing rates that
   downstream analyses (factor analysis, cluster reports, Pareto plots) consume are therefore
   unreliable for t0126. This task computes `pd_rate_hz` and `nd_rate_hz` directly from the
   actual per-direction spike counts that the evaluator already records.

Together, these two corrections let us re-examine the DSI-vs-ATP-per-spike Pareto on a fresh
seed with metrics that match the literature definition and reflect what each cell actually
does.

## Scope

* **Single fresh seed** (3517) — not in the t0124 / t0126 / t0128 lineage. This is a
  first-pass replication; multi-seed scaling is left to a follow-up if results warrant.
* Fork of t0126's evaluator and NSGA-II driver into `tasks/t0129_*/code/`. **No changes to
  t0126 itself** — the framework rule of completed-task immutability applies.
* All other t0126 protocol parameters preserved verbatim: 68-d parameter vector, Bed B
  substrate, antipodal direction pair `[0°, 180°]`, `N_EVAL_SEEDS`, `TSTOP_MS = 1400`,
  smoke-gate, silence guard at `pd_spikes_sum < 3`, 60 generations, population restart cadence
  (`_POOL_RESTART_EVERY = 10`), HV-plateau auto-stop **disabled** (per
  `feedback_disable_hv_plateau_autostop`).
* **t0127 and t0128 are out of scope.** t0127's cell_trace JSONL recording fix is not adopted;
  this task does not record per-spike `cell_trace` data. Instead, the full electrophysiology +
  morphology parameter vector for every evaluated cell is persisted to a per-cell parameter
  dump (see Outputs).

## Changes to the t0126 Evaluator

All edits live in `tasks/t0129_*/code/evaluator.py` (forked copy). t0126 is not touched.

### Change 1: Signed antipodal DSI

Replace the call to `_vector_sum_dsi` with a new helper:

```python
def _signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float:
    """Signed antipodal DSI = (R_PD - R_ND) / (R_PD + R_ND), range [-1, 1].

    Assumes exactly two antipodal directions (PD at PD_DIRECTION_DEG and ND
    at PD_DIRECTION_DEG + 180 deg). Returns -1.0 (WORST_CASE_DSI) when the
    denominator is zero.
    """
```

The objective `F` is rewritten as `F = [-dsi_signed, +atp_per_spike_molecules]` so NSGA-II
still maximises DSI. The silence sentinel `WORST_CASE_DSI = -1.0` is reused — already at the
lower bound of the signed range. The `CellEvalResult` dataclass field is renamed
`dsi_vector_sum` → `dsi_signed` to make the metric switch obvious in downstream code; both the
metric registration in `meta/metrics/` and the comparator scripts must be updated accordingly.

### Change 2: Real per-direction firing rates

The evaluator already populates `firing_hz_per_dir: dict[str, float]` from actual spike counts
(`tasks/t0126_*/code/evaluator.py:467-470`). This task formalises two named scalar fields on
`CellEvalResult` derived from that same data:

* `pd_rate_hz = mean(pd_spikes) / (TSTOP_MS / 1000.0)`
* `nd_rate_hz = mean(nd_spikes) / (TSTOP_MS / 1000.0)`

These replace the synthesised placeholders downstream. They are the actual numbers used by the
signed-DSI computation, so the two corrections are arithmetically consistent.

### Change 3: Per-cell parameter persistence

For every cell evaluated during the run (Phase A random-init population + every NSGA-II
generation), persist a JSONL row containing:

* `gen` (int) — generation index, `-1` for Phase A random init
* `cell_idx` (int) — index within the generation
* `param_vector` (list[float]) — full 68-d morphology + electrophysiology vector
* `dsi_signed` (float)
* `atp_per_spike_molecules` (float)
* `pd_rate_hz` (float)
* `nd_rate_hz` (float)
* `silence_failed` (bool)
* `n_errors` (int)

File: `results/cell_params.jsonl`. This replaces the dropped `cell_trace.jsonl` for diagnostic
purposes — it loses the per-spike timing detail but keeps everything needed to reconstruct
parameter-vs-objective scatter plots and per-cell factor analysis.

## Approach

1. **Bootstrap & smoke gate.** Compile mod files, re-run the smoke gate from t0126 verbatim to
   confirm the forked evaluator behaves identically on a fixed test cell before changing the
   DSI formula. (The smoke gate currently asserts on `dsi_vector_sum`; relax its assertion to
   compare against the new `dsi_signed` on the same fixed cell.)
2. **Phase A: random init.** Generate the seed-3517 random initial population using the t0126
   protocol. Persist parameters + metrics per cell.
3. **Phase B: 60-generation NSGA-II.** Launch via the canonical `run_seed3517.sh` wrapper (per
   `feedback_nsga2_launch_via_run_script`). Auto-stop disabled, `_POOL_RESTART_EVERY = 10`,
   budget cap + generation ceiling are the only stop conditions.
4. **Post-run analysis.** Build Pareto plot of `dsi_signed` vs `atp_per_spike_molecules`,
   distribution of `dsi_signed` (with negative tail visible), and PD-vs-ND rate scatter
   coloured by `dsi_signed`. Compare cross-front overlap and Pareto-dominance against t0126's
   vector-sum front.
5. **Comparison vs t0126.** Quantify how many t0126-Pareto cells would still be Pareto-optimal
   under signed DSI; flag cells whose `dsi_vector_sum > 0.5` but `dsi_signed < 0` (reversed
   preference masked by magnitude).

## Outputs and Expected Assets

* **Predictions asset** — Pareto front of cells under (`dsi_signed`,
  `atp_per_spike_molecules`) with full parameter vectors. Mirrors t0126's predictions asset
  format.
* **Answer asset** — one-pager: "Does the signed-DSI re-evaluation of t0126's protocol change
  the Pareto structure, or is the vector-sum / signed distinction immaterial on the antipodal
  pair?" with supporting numbers.
* `results/cell_params.jsonl` — per-cell parameter dump (see Change 3).
* `results/results_summary.md`, `results/results_detailed.md`, `results/metrics.json`,
  `results/suggestions.json`, `results/costs.json`, `results/remove_machines_used.json`.
* `results/images/` — Pareto front, DSI distribution (showing negative tail), PD-vs-ND
  scatter, t0126-vs-t0129 front overlay.

## Dependencies

* `t0126_bedb_dsi_atp_per_spike_nsga2_60gen` — code template, comparison baseline, parameter
  bounds, smoke-gate fixture.

t0127 and t0128 are explicitly **not** dependencies and are not read.

## Compute, Budget, and Time

Single seed × 60 generations × NSGA-II population × NEURON simulation per cell. Target compute
profile mirrors t0126's one-seed cost envelope (t0126 ran 1 seed in ~9h elapsed on the local
machine). Budget cap inherited from t0126's run script.

* **GPU**: none. NSGA-II + NEURON is CPU-bound.
* **Machine**: local (CPU). Remote provisioning not required for one seed.
* **Estimated wall-clock**: ~8-12h (single seed, 60 gen). Hard ceiling 24h via budget cap.

## Risks & Fallbacks

* **Smoke gate fails after DSI swap.** Likely cause: an unrelated regression in the fork.
  Mitigation: diff `evaluator.py` against t0126 line-by-line; only the DSI helper, the field
  rename, and the rate-field additions should differ.
* **All Phase A cells trip the silence guard** (`dsi_signed = -1.0`). Same risk as t0126 —
  fall back to wider random init bounds is *not* permitted (would break parameter-vector
  comparability with t0126). Document and stop.
* **Run script drops the per-cell JSONL** (per memory `feedback_nsga2_launch_via_run_script`).
  Mitigation: verify the wrapper sets the env var that the evaluator reads for
  `cell_params.jsonl` before launching; assert the file exists and is non-empty after Phase A.

## Verification Criteria

* `evaluator.py` exports a `_signed_antipodal_dsi` helper with a unit test in
  `tasks/t0129_*/code/test_evaluator_dsi_guard.py` covering: (a) PD>ND positive case, (b)
  PD<ND negative case, (c) PD=ND=0 silence sentinel, (d) PD=ND>0 zero case.
* The smoke gate passes for a fixed cell after the DSI change.
* `results/cell_params.jsonl` exists, has one row per evaluated cell, and contains all
  required fields.
* `metrics.json` reports `dsi_signed_max`, `dsi_signed_pareto_median`,
  `atp_per_spike_pareto_min`, `pd_rate_hz_pareto_median`, and the count of t0126-Pareto cells
  with `dsi_vector_sum > 0.5` but `dsi_signed < 0`.
* Pareto plot embedded in `results_detailed.md` with negative-DSI region visible on the axis.

</details>

## Costs

**Total**: **$0.97**

| Category | Amount |
|----------|--------|
| vast-ai-epyc-7c13-t0129 | $0.97 |
| per_instance_watchdog_USD | $0.00 |
| vast-ai-failed-attempts | $0.00 |
| api_calls | $0.00 |
| local_compute | $0.00 |

## Remote Machines

| Provider | GPU | Count | RAM | Duration | Cost |
|----------|-----|-------|-----|----------|------|
| vast.ai | Tesla V100 (1x, idle, unused; CPU-only NEURON workload) | 1 | 64 GB | 5.0h | $0.97 |

## Metrics

### Headline cell (max signed DSI) on final Pareto front

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **1.0** |

### Median signed DSI across the final 9-cell Pareto front

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.5714285714285715** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does the signed-DSI re-evaluation of t0126's protocol change the Pareto structure, or is the vector-sum / signed distinction immaterial on the antipodal pair?](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/answer/does-signed-dsi-change-t0126-pareto-structure/) | [`full_answer.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/answer/does-signed-dsi-change-t0126-pareto-structure/full_answer.md) |
| predictions | [NSGA-II Signed DSI vs ATP per Spike, Bed B + 14-d Morph, Seed 3517](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/) | [`description.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/description.md) |

## Suggestions Generated

<details>
<summary><strong>Re-run t0126 seed 8929 with t0129 signed-DSI evaluator to recover
true sign-flip count (closes REQ-20)</strong> (S-0129-01)</summary>

**Kind**: experiment | **Priority**: high

REQ-20 of t0129 is Partial: the true number of t0126 Pareto cells that flip sign under signed
DSI is unknowable (upper bound is 4, from the count of t0126-Pareto cells with dsi_vector_sum
> 0.5), because t0126 did not persist per-direction spike counts and pd_rate_hz=40 is a
synthesised placeholder. Re-run the SAME GA seed (8929) using the t0129 evaluator (signed DSI,
real PD/ND firing rates, cell_params.jsonl sink) and the SAME 68-d parameter bounds and hard
invariants (POP_SIZE=96, N_GEN=60, _POOL_RESTART_EVERY=10, HV-plateau auto-stop disabled, $8
cap). Compare the resulting 60-gen Pareto front and per-cell signed DSI to t0126's recorded
vector-sum Pareto cells (cell-by-cell, ranked by within-front rank), and report the exact
sign-flip count among t0126's 6 cells. Expected cost: ~$1.00 Vast.ai (matches t0126
single-seed envelope). Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Multi-seed (3-5 fresh seeds) t0129 protocol extension to bracket
negative-DSI fraction and Pareto-front stability</strong> (S-0129-02)</summary>

**Kind**: experiment | **Priority**: high

t0129's headline (95/5,496 viable cells with negative signed DSI = 1.7%; 9-cell Pareto front
spanning DSI in [0, 1]) is on a single GA seed (3517). The corresponding numbers from other
t0124/t0126/t0128 seeds are unknown, so it is impossible to state whether 1.7% is typical, a
low outlier, or a high outlier. Run the t0129 evaluator and driver verbatim on 3-5 additional
fresh GA seeds (NOT in the lineage set {441, 6650, 8929, 2608, 8276, 9986, 3517}). For each
seed report (a) viable-cell count, (b) negative-DSI count and deepest reversal, (c) final-gen
Pareto-front size and DSI/ATP corner positions, (d) headline cell DSI and ATP. Synthesise as
bootstrap-CI bands on the four key statistics. Expected cost: ~$4-5 (4 seeds x ~$1).
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Re-fit t0117 unfiltered-pool factor analysis with signed DSI
replacing vector-sum on the 4-seed pooled cohort</strong> (S-0129-03)</summary>

**Kind**: evaluation | **Priority**: high

t0117 found a joint DSI-PD factor (F1, r_DSI=+0.421, r_PD=+0.352) on a pooled 4-seed
unfiltered cohort that consumed dsi_vector_sum as the DSI feature. t0129 shows that 1.7% of
viable cells have genuinely reversed preference (dsi_signed < 0) which vector-sum collapses to
positive magnitude indistinguishable from true PD-preferring cells of the same magnitude. The
sign collapse contaminates the DSI column used to fit F1. Recompute signed DSI for every cell
in t0117's pooled parquet using the per-direction spike counts (available in t0117's per-seed
evaluation dumps if persisted; otherwise restricted to the subset where they are recoverable),
refit the 10-factor varimax solution, and report whether F1's r_DSI changes sign or magnitude.
Decision rule: |r_DSI change| > 0.10 means t0117's joint-factor verdict is
sign-collapse-contaminated. Recommended task types: data-analysis, comparative-analysis.

</details>

<details>
<summary><strong>Re-run t0124 NSGA-II under signed DSI on t0124 GA seeds to test
whether the DSI-ATP frontier depends on sign convention</strong>
(S-0129-04)</summary>

**Kind**: experiment | **Priority**: medium

t0124 ran NSGA-II on DSI vs ATP/spike with vector-sum DSI as the first objective. t0129 shows
on a single seed that 95/5,496 viable cells (1.7%) have negative signed DSI; the t0129 Pareto
front happens to contain no reversed-preference cells (they are dominated by DSI=0 cells at
the ATP minimum), but t0124's particular seed and termination might have surfaced reversed
cells onto its front. Re-run the t0124 NSGA-II protocol on t0124's GA seeds with the t0129
evaluator (signed DSI as first objective, real PD/ND rates) and report (a) cell-by-cell
sign-flip count among t0124's recorded Pareto cells, and (b) whether the re-run Pareto front
contains any cell with dsi_signed < 0. Expected cost: per-seed cost of t0126 envelope
(~$1/seed). Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary><strong>Re-fit t0116 strict-cohort factor analysis using signed DSI to
test the no-joint-factor verdict</strong> (S-0129-05)</summary>

**Kind**: evaluation | **Priority**: medium

t0116 reported zero joint DSI-PD factors on the strict-cohort (vector-sum DSI > 0.7 AND PD >
10 Hz) pool, the finding that the memory project_truncated_cohort_artefact_confirmed.md
attributes to range restriction. The DSI > 0.7 cutoff was applied to vector-sum DSI: any
reversed-preference cell with |signed DSI| > 0.7 would have entered the cohort despite firing
more in the ND direction. Recompute signed DSI on the cells in t0116's pool, drop cells with
dsi_signed < 0.7 (the literature-correct filter), refit the factor analysis on the corrected
strict cohort, and compare joint-factor counts and loadings to t0116's original. Decision
rule: identical verdict means sign collapse did not materially affect cohort selection;
different verdict means t0116's strict-cohort finding was partly sign-collapse-dependent.
Recommended task types: data-analysis, comparative-analysis.

</details>

<details>
<summary><strong>Re-fit t0125 MI/ATP cluster-factor analysis with signed-DSI cohort
filtering to test the zero-joint-factor verdict</strong> (S-0129-06)</summary>

**Kind**: evaluation | **Priority**: medium

t0125 analysed MI-vs-ATP cluster-factor structure on a single-seed MI NSGA-II run and reported
a near-zero joint MI-ATP factor. The cohort selection and factor inputs use vector-sum DSI as
a covariate / cohort gate. Reversed-preference cells with high |signed DSI| are mis-classified
as preferring PD, which could distort the MI calculation (MI is direction-symmetric but cell
labels for cohort filtering are not). Apply the signed-DSI recoding to t0125's per-cell
parquet using whatever per-direction spike data is recoverable, refit the cluster-factor
pipeline on the corrected cohort, and report whether the joint-factor verdict changes. If
per-direction spike counts are not recoverable for t0125, report this as the scope-of-recovery
limitation and recommend the smaller-scope alternative of a fresh MI NSGA-II re-run with the
t0129 evaluator on one fresh seed. Recommended task types: data-analysis,
comparative-analysis.

</details>

<details>
<summary><strong>Deep-dive (Vm traces, morphology, dendritic-spike attribution) on
t0129 Pareto cells 4 (DSI=1.0) and 7 (DSI=0.87)</strong> (S-0129-07)</summary>

**Kind**: experiment | **Priority**: medium

Pareto cell 4 (gen 57, signed DSI=1.0, PD rate 6.43 Hz, ND rate 0.0 Hz, ATP 6.66 M
molec/spike) is the canonical ND-silenced DSGC corner, and Pareto cell 7 (gen 59, DSI=0.870,
PD rate 10.24 Hz, ND rate 0.71 Hz, ATP 5.03 M molec/spike) is the highest-PD-rate Pareto cell
with both PD rate and ATP/spike within the Sivyer-2013 physiological band (5-15 Hz PD rate,
sub-10 M molec/spike). Re-simulate both cells with full Vm traces at soma and 3 dendritic
loci, render the morphology with full dendrite tree at the same orientation, and run the
standard dendritic-spike-attribution analysis (per-compartment Nav/Kv/Ih conductance
contributions to ATP/spike). Output: 2-cell deep-dive PNG bundle + per-cell Carter-Bean
ATP/AP/cm decomposition + Wei2018 figure-style Vm trace plate. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary><strong>Formalise the t0129 cell_params.jsonl per-cell parameter-dump
protocol as a project-wide NSGA-II evaluator standard</strong> (S-0129-08)</summary>

**Kind**: library | **Priority**: high

t0129 introduced cell_params.jsonl as the per-cell diagnostic sink, replacing the
env-var-driven cell_trace.jsonl pattern that t0126 used and that silently dropped data in
worker processes (memory feedback_nsga2_launch_via_run_script and
project_t0126_cell_trace_synthesised). The t0129 implementation captures the sink path at
problem-constructor time (BedBV3MorphProblem.__init__), pickling it into every worker, which
closes the failure mode. The schema (gen, cell_idx, param_vector, dsi_signed, atp_per_spike,
pd_rate_hz, nd_rate_hz, silence_failed, n_errors) is enough to reconstruct any
parameter-vs-objective scatter or factor analysis. Promote this to a documented project-wide
pattern: write a meta/specifications file (or extend the existing evaluator template) defining
the schema, the constructor-capture pattern, and a verificator that asserts cell_params.jsonl
exists and is non-empty after Phase A. Recommended task types: infrastructure-setup,
write-library.

</details>

<details>
<summary><strong>Adopt signed antipodal DSI as the canonical DSI metric across all
DSGC project tasks; deprecate vector-sum DSI</strong> (S-0129-09)</summary>

**Kind**: evaluation | **Priority**: high

The signed-vs-vector-sum DSI distinction is not aesthetic: vector-sum gives a 50%-wrong answer
about preferred direction for 1.7% of viable cells on the t0129 cohort, and the DS-RGC
literature (Wei 2018, Sivyer 2013) uses the signed definition exclusively. The two metrics'
magnitudes are arithmetically equal on the antipodal pair, so adoption is zero-cost for
existing analyses (they can re-read |dsi_signed| where they used dsi_vector_sum). Concrete
action: (a) update meta/metrics/direction_selectivity_index/specification.md to state
signed-antipodal as the canonical formula, (b) add a deprecation note pointing to t0129 for
the rationale, (c) update the evaluator template and the t0080 baseline to expose dsi_signed
as the canonical field, (d) leave t0126's frozen dsi_vector_sum field name in place per
immutability but flag it via a metric correction overlay. Recommended task types:
infrastructure-setup, correction.

</details>

<details>
<summary><strong>Cross-task audit: enumerate every downstream task that consumed
t0126's pd_rate_hz=40 placeholder</strong> (S-0129-10)</summary>

**Kind**: evaluation | **Priority**: high

Memory project_t0126_cell_trace_synthesised confirms t0126's per-cell pd_rate_hz=40 was a
synthesised placeholder; t0129 confirms the true Pareto-median PD rate is 2.62 Hz and the
Pareto-max PD rate is 10.24 Hz (off by 4x to 20x). Any downstream analysis that filtered
cells, computed thresholds, or scored cells using t0126's pd_rate_hz is potentially
miscalibrated. Walk every task in tasks/ that lists t0126 as a dependency or reads t0126's
predictions asset, scan their code/research/results for references to pd_rate_hz, and produce
a single audit table (task ID, file, line, threshold-or-statistic-used, affected-metric,
recommended-correction). Recommended task types: data-analysis, correction.

</details>

## Research

* [`research_code.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/research/research_code.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/results_summary.md)*

--- spec_version: "2" task_id: "t0129_t0126_signed_dsi_real_rates_1seed" date_completed:
"2026-05-26" status: "results_complete" ---
# Results Summary -- t0129 NSGA-II Signed DSI vs ATP-per-Spike (60-gen, Seed 3517)

## Summary

Forked-and-corrected re-run of t0126's NSGA-II protocol on one fresh GA seed (**3517**) with
signed antipodal DSI replacing vector-sum DSI and real per-cell PD/ND firing rates replacing
t0126's `pd_rate_hz = 40` synthesised placeholder. The run completed all **60/60 generations**
cleanly (`NSGA2_EXIT=0`, `watchdog_tripped=false`) at **$0.965** total Vast.ai spend (12.1% of
the $8 cap), producing a **9-cell final Pareto front** spanning signed DSI **[0.000, 1.000]**
at ATP **[0.78e6, 6.66e6]** molecules/spike, and surfacing **95 viable cells** with genuinely
reversed preference (`dsi_signed < 0`, deepest reversal **-0.778**) that vector-sum DSI would
silently collapse to positive magnitudes.

## Metrics

* **direction_selectivity_index** (headline, signed antipodal): **1.0000** at ATP **6.66e6**
  molecules/spike (Pareto cell 4, gen 57; canonical ND-silenced corner, PD=6.43 Hz / ND=0.0
  Hz)
* **direction_selectivity_index** (Pareto-median, signed antipodal): **0.5714** at ATP
  **3.63e6** molecules/spike (Pareto-median PD rate **2.62 Hz**, ND rate **0.71 Hz** -- far
  below t0126's placeholder 40 Hz)
* **atp_per_spike_molecules** (Pareto min): **7.80e5** at DSI 0.000 (Pareto cell 3, gen 56;
  **2.3x reduction** vs t0126's 1.83e6, attributable to seed variation on a single-seed run)
* **n_viable_cells_with_negative_DSI**: **95 / 5,496 viable** (1.7%), deepest reversal
  **dsi_signed = -0.778** -- structure invisible under t0126's vector-sum DSI
* **t0126-Pareto cells with `dsi_vector_sum > 0.5`**: **4 / 6** (upper bound on potential
  sign-flip population; true sign-flip count is **unknowable** because t0126 did not persist
  per-direction spike counts)
* **Final hypervolume**: **1.9996e+10** at gen 60 (3.385 h active NSGA-II window on Vast.ai
  EPYC 7C13, 32 effective vCPUs)
* **Total cost**: **$0.965** ($0.647 active NSGA-II window + $0.318 setup/teardown idle;
  Vast.ai instance 37924958)

## Verification

* `verify_task_metrics` -- **PASSED** (3 variants, only registered metric key is
  `direction_selectivity_index` per `meta/metrics/`; 0 errors, 0 warnings)
* `verify_task_folder` -- **PASSED** (0 errors, 1 warning: empty `logs/searches/`)
* Predictions asset `nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129` -- spec-compliant
  structure (verified by `verify_task_folder` asset content check; no dedicated predictions
  verificator)
* Answer asset `does-signed-dsi-change-t0126-pareto-structure` -- spec-compliant structure
  (verified by `verify_task_folder` asset content check; no dedicated answer verificator)
* Full `verify_task_results` will be run in the reporting step (step 015)

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0129_t0126_signed_dsi_real_rates_1seed" date_completed:
"2026-05-26" status: "results_complete" ---
# Detailed Results -- t0129 NSGA-II Signed DSI vs ATP-per-Spike (60-gen, Seed 3517)

## Summary

Fork-and-correct re-run of t0126's 68-d Bed B + 14-d morphology NSGA-II protocol on one fresh
GA seed (**3517**) with three evaluator deltas applied as a single coherent diff against the
t0126 fork: (1) signed antipodal DSI `(R_PD - R_ND) / (R_PD + R_ND)` in `[-1, 1]` replacing
vector-sum DSI as the first NSGA-II objective; (2) real per-cell PD and ND firing rates
exposed as named scalar fields on `CellEvalResult`, both computed from actual per-direction
spike counts; (3) a per-cell parameter dump to `results/cell_params.jsonl` via a
constructor-captured sink path (no env var dependency that can silently drop in worker
processes). The run completed all **60/60 generations** cleanly on a Vast.ai EPYC 7C13
instance at **$0.965** total spend, evaluated **5,760 cells**, and produced a **9-cell final
Pareto front** that surfaces signed-DSI structure invisible to t0126's vector-sum analysis.

## Methodology

* **Hardware**: Vast.ai instance **37924958**, AMD **EPYC 7C13 64-Core** Processor (32
  effective vCPUs Zen-3 Milan), 64 GB RAM, 64 GB allocated disk, 1x Tesla V100 (idle, unused
  -- CPU-only NEURON workload), Virginia US, reliability 0.9954.

* **Pricing**: **$0.1911/hr** total ($0.1733/hr base + $0.0178/hr storage for the 64 GB disk).

* **Software**: NEURON 8.2.7, pymoo 0.6.1.6, numpy/scipy/pandas/matplotlib/dill/pydantic/tqdm
  (image `python:3.12-bookworm`). t0080 MOD library compiled with `nrnivmodl` on the remote
  host.

* **Algorithm (verbatim from t0126 hard invariants)**: NSGA-II via pymoo,
  `_POOL_RESTART_EVERY=10` (project memory `feedback_nsga2_pool_restart_every_10`),
  `HV_PLATEAU_AUTO_STOP=False` (project memory `feedback_disable_hv_plateau_autostop`),
  `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_DIRECTIONS=2`, `N_GEN=60`,
  `SILENCE_PD_SPIKES_THRESHOLD=3`, `WORST_CASE_DSI=-1.0`, `TSTOP_MS=1400`. Live
  `TerminationCollection` contains EXACTLY `MaximumGenerationTermination(n_max_gen=60)` and
  `CostWatchdogTermination($8 cap)`. `OperatorStopTermination` and `HVPlateauTermination` are
  NOT in the live collection.

* **Algorithm config (full)**: SBX crossover (`eta=15`, `prob=0.9`), polynomial mutation
  (`eta=20`, `prob=1/68=0.01471`), Latin-Hypercube initial sampling,
  `eliminate_duplicates=true`, `ref_point_hv=(0.0, 2.0e10)`, `hv_utopia=(0.7, 1.0e9)`,
  `worst_case_atp_per_spike=2.0e10`, evaluation seeds `(2684470948, 4091952314, 233227757)`.
  Single GA seed `T0129_SEEDS=(3517,)`.

* **Signed-DSI helper** (REQ-1, `code/evaluator.py`):

  ```python
  def _signed_antipodal_dsi(*, spike_counts_per_dir: dict[float, list[int]]) -> float:
      """DSI = (R_PD - R_ND) / (R_PD + R_ND), range [-1, 1]. Sentinel -1.0
      when denominator is zero."""
      r_pd = float(np.mean(spike_counts_per_dir.get(0.0, []))) if ... else 0.0
      r_nd = float(np.mean(spike_counts_per_dir.get(180.0, []))) if ... else 0.0
      denom = r_pd + r_nd
      return WORST_CASE_DSI if denom <= 0.0 else (r_pd - r_nd) / denom
  ```

* **Worker count**: 32 effective vCPUs; pymoo's parallel evaluation pool uses ~28 worker
  processes after reserving 4 for the driver, generation callback, cost watchdog, and
  orchestrator thread. The `BedBV3MorphProblem(cell_params_path=CELL_PARAMS_JSONL)`
  constructor pickles the sink path into each worker so per-cell JSONL writes survive the
  fork.

* **Seed**: **3517** (fresh; explicitly excluded the lineage seed set `{441, 6650, 8929, 2608,
  8276, 9986}` per orchestrator brief).

* **Run timing (wall-clock)**: Instance created **2026-05-26T14:46:33Z**, ready
  **2026-05-26T14:46:55Z**, NSGA-II launched in tmux ~**2026-05-26T15:25Z** (after ~38 min apt
  + pip + MOD compile + Carter-Bean smoke gate), gen-60 exit **2026-05-26T18:45:30Z**,
  instance destroyed **2026-05-26T19:49:52Z**. NSGA-II active wall-clock **12,183.82 s = 3.385
  h** (driver `hv_trajectory_seed3517.json` `elapsed_s` at gen 60); total billed instance
  duration **5.049 h**.

* **Cells evaluated**: **5,760** = 96 Phase A LHS random init (gen=-1) + 5,664 NSGA-II
  evaluations across generations 1..59 (gen 60 reuses gen 59's evaluated population per
  pymoo's generation-counter convention; `n_evaluations=5664` at the gen-60 trajectory entry).
  All cells persisted to `results/cell_params.jsonl` (9.2 MB, 5,760 rows, all fields
  populated, `n_errors=0` for every row).

## Metrics Tables

### Per-Pareto-cell breakdown (final 9-cell Pareto front, seed 3517)

| Cell | Gen | DSI (signed) | ATP (M molec/spike) | PD rate (Hz) | ND rate (Hz) | Role |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| 3 | 56 | 0.0000 | 0.780 | 0.714 | 0.714 | rank-1 (min ATP, no selectivity) |
| 8 | 59 | 0.3333 | 3.520 | 1.429 | 0.714 | low-DSI mid-front |
| 5 | 58 | 0.4545 | 3.532 | 1.905 | 0.714 | low-mid DSI |
| 1 | 53 | 0.5385 | 3.607 | 2.381 | 0.714 | mid-front |
| 2 | 53 | 0.5714 | 3.633 | 2.619 | 0.714 | mid-front |
| 0 | 52 | 0.6842 | 3.722 | 3.810 | 0.714 | mid-high DSI |
| 6 | 59 | 0.8065 | 3.814 | 6.667 | 0.714 | high-DSI shoulder |
| 7 | 59 | 0.8696 | 5.027 | 10.238 | 0.714 | near-elite |
| 4 | 57 | 1.0000 | 6.659 | 6.429 | 0.000 | rank-9 (max DSI, ND-silenced corner, headline) |

The front is **monotonically increasing in both DSI and ATP** (Pareto-optimality is by
construction on the two objectives). Pareto-median PD rate is **2.62 Hz**; Pareto-median ND
rate is **0.71 Hz** -- both **far below** t0126's recorded `pd_rate_hz = 40` (which was a
synthesised placeholder per project memory `project_t0126_cell_trace_synthesised`).

### Distribution buckets across all 5,760 evaluated cells

| Bucket | Count | Fraction |
| --- | ---: | ---: |
| `silence_failed = True` (DSI=-1 sentinel) | 264 | 4.6% |
| viable, DSI < -0.5 | 2 | 0.03% |
| viable, -0.5 <= DSI < 0 | 93 | 1.6% |
| viable, DSI = 0 (bidirectional / silent) | 4,315 | 74.9% |
| viable, 0 < DSI <= 0.5 | 653 | 11.3% |
| viable, DSI > 0.5 | 433 | 7.5% |
| **total** | 5,760 | 100.0% |

* **Viable cells with negative DSI**: **95** (1.7% of viable, 1.6% of total). Deepest reversal
  `dsi_signed = -0.778` (gen 14, PD rate 0.714 Hz, ND rate 5.714 Hz, ATP 7.05e+06
  molec/spike).
* **DSI = 0 cluster**: **4,315 viable cells** (78.5% of viable). These cells fire equally in
  both directions; in many cases at low rates (e.g., 0.714 Hz = exactly 1 spike per 1.4 s), in
  others at high rates (top firing rate 47.857 Hz at gen 2). They are NOT silence failures
  (silence guard requires PD spike count < 3); they are genuine bidirectional firers.
* **Silence-failed cells**: **264** (4.6%). All at `dsi_signed = -1.0` by sentinel.
* **High-selectivity cells (DSI >= 0.7)**: **308** viable cells; only 4 of these are on the
  final Pareto front (cells 4, 6, 7 plus the headline).

### Comparison to t0126's Pareto cohort (seed 8929)

| Metric | t0126 (vector-sum) | t0129 (signed) | Delta |
| --- | ---: | ---: | --- |
| n cells evaluated | 5,760 | 5,760 | 0 |
| n cells silenced (sentinel DSI=-1) | unknown | 264 | (t0126 not persisted) |
| n viable cells | unknown | 5,496 | (t0126 not persisted) |
| n viable cells with negative DSI | 0 (impossible under vector-sum) | 95 | +95 (newly visible) |
| Pareto-front size | 6 | 9 | +3 |
| Pareto DSI range | [0.000, 1.000] | [0.000, 1.000] | identical |
| Pareto ATP min (M molec/spike) | 1.827 | 0.780 | -1.05 (-57%) |
| Pareto ATP max (M molec/spike) | 7.819 | 6.659 | -1.16 (-15%) |
| Pareto-median PD rate (Hz) | 40.0 (placeholder!) | 2.62 | (t0126 placeholder) |
| Pareto-median ND rate (Hz) | 0.0 / null (placeholder!) | 0.71 | (t0126 placeholder) |
| Pareto-headline (max DSI) PD rate (Hz) | 40.0 (placeholder!) | 6.43 | (t0126 placeholder) |
| Pareto-headline (max DSI) ND rate (Hz) | 0.0 (placeholder!) | 0.00 | (t0126 placeholder; headline is ND-silenced in both) |
| Final hypervolume | 1.9995e+10 | 1.9996e+10 | +0.005% (negligible) |
| Total cost (Vast.ai) | $1.308 | $0.965 | -$0.343 (-26%) |
| NSGA-II active window (h) | 5.22 | 3.385 | -1.84h (-35%) |

The 35% faster NSGA-II active window is **not** attributable to t0129's evaluator changes (the
signed-DSI helper, the named rate fields, and the per-cell JSONL appends each cost
microseconds per cell). It reflects per-cell simulation-time variation across different seeds
and worker-pool contention patterns; the Vast.ai 7C13 partition is comparable to t0126's
sister partition on the same physical machine.

## Comparison vs Baselines

### t0126 Pareto-front overlap

See chart `pareto_t0126_vs_t0129_overlay.png`. Both fronts populate the same diagonal corridor
in DSI/ATP space:

* Both have an ATP-minimum corner near `dsi=0`: t0126 at `(0, 1.83e+06)`, t0129 at `(0,
  7.80e+05)`.
* Both have a selectivity-maximum corner at `dsi=1`: t0126 at `(1, 7.82e+06)`, t0129 at `(1,
  6.66e+06)`. Both are ND-silenced canonical corners (`R_ND = 0`).
* t0129 fills the mid-front (`dsi in [0.33, 0.68]`) with 4 additional Pareto cells; t0126's
  seed 8929 sampled this region more sparsely.

The qualitative shape is preserved across the two seeds and across the two DSI definitions.
There is no Pareto cell in t0129 with `dsi_signed < 0`: the cluster of viable negative-DSI
cells (95 cells, peak depth -0.778) is **dominated in F-space** by the large cluster of DSI=0
cells with cheaper ATP, so they never make it to the Pareto front.

### Reversed-preference cells visible under signed DSI but invisible under vector-sum

This is the headline finding. **95 of 5,496 viable cells (1.7%)** have `dsi_signed < 0` in the
t0129 cohort, meaning their ND-direction firing rate is strictly larger than their
PD-direction rate. Under vector-sum DSI these 95 cells would have been collapsed to positive
magnitudes indistinguishable from true-PD-preferring cells of the same magnitude.

**Practical implication**: any downstream analysis that uses `dsi_vector_sum` as a proxy for
"this cell prefers PD" silently includes these reversed cells as if they were PD-preferring,
which is a 50%-wrong answer about preferred direction. Signed DSI catches the error at zero
algorithmic cost.

### Sign-flip count for t0126's own Pareto cells (REQ-20)

| Quantity | Value | Provenance |
| --- | ---: | --- |
| t0126 Pareto cells | 6 | `pareto_front_seed8929.json` |
| t0126 Pareto cells with `dsi_vector_sum > 0.5` (upper bound for sign-flip) | 4 | this analysis |
| t0126 Pareto cells with `dsi_vector_sum > 0.5` and **true** `dsi_signed < 0` | **unknowable** | t0126 did not persist per-direction spike counts; `pd_rate_hz=40` is a synthesised placeholder per memory `project_t0126_cell_trace_synthesised` |

The true sign-flip count for t0126's Pareto cells **cannot be recovered** from t0126's
persisted artefacts. Recovery would require a re-run of t0126 seed 8929 with the corrected
evaluator (out of scope here; would be a separate task).

## Visualizations

### Pareto front -- signed DSI vs ATP per spike

![t0129 final 9-cell Pareto front, signed antipodal DSI on x (full [-1, 1] range visible), ATP
per spike on y in millions of molecules. The rank-1 (min ATP, cell 3) and rank-9 (max DSI,
cell 4) extremes are annotated. The vertical dashed line marks DSI=0; no Pareto cell has DSI <
0 because negative-DSI viable cells are dominated in F-space by the DSI=0 cluster at the ATP
minimum.](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/pareto_front_dsi_signed_vs_atp.png)

### Signed-DSI distribution across all 5,760 evaluated cells

![Histogram of signed DSI in 40 bins from -1 to +1 covering all 5,496 viable cells (blue
bars). The 264 silence-failed cells (all at sentinel DSI=-1.0) are rendered as a separate red
bar shifted slightly to the left so they are not confused with the 95 viable cells with
genuine reversed preference (the small bars in the range [-0.778, 0)). The dominant bar at
DSI=0 contains 4,315 cells (78.5% of viable) that fire equally in both directions -- many at
the 1-spike-per-trial
floor.](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/dsi_signed_distribution.png)

### PD vs ND firing rate scatter coloured by signed DSI

![Scatter of PD firing rate (0 deg) on x vs ND firing rate (180 deg) on y for all 5,496 viable
cells, coloured by signed DSI using a diverging RdBu_r colormap centred at DSI=0. The dashed
y=x line marks the DSI=0 locus. Cells below the diagonal (red end of the colormap) prefer PD;
cells above the diagonal (blue end) prefer ND. The 9 Pareto cells are highlighted with larger
markers and black outlines; they cluster in the high-PD low-ND quadrant as expected for a
DSI-maximising objective. Most cells fire at very low rates (most of the data is clustered
near the origin); a small population of high-rate bidirectional firers extends along the
diagonal up to ~50
Hz.](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/pd_vs_nd_rate_scatter.png)

### t0126 vs t0129 Pareto front overlay

![Overlay of t0126's 6-cell vector-sum Pareto front (orange squares, seed 8929) and t0129's
9-cell signed-DSI Pareto front (blue circles, seed 3517) in DSI vs ATP space. The dashed
vertical line marks DSI=0. Both fronts populate the same diagonal corridor; t0129 has more
mid-front cells in the DSI=0.3 to 0.7 range. The yellow annotation box explains that t0126's
cells are plotted at +|DSI| because t0126 only stored the vector-sum magnitude and did not
persist per-direction spike counts (and its pd_rate_hz=40 is a synthesised placeholder), so
the true signed DSI for t0126 cells cannot be
recovered.](../../../tasks/t0129_t0126_signed_dsi_real_rates_1seed/results/images/pareto_t0126_vs_t0129_overlay.png)

## Examples

The Examples block below mixes (a) every cell on the final 9-cell Pareto front, (b) one
silence-failed cell from Phase A (worst-case input), (c) the deepest reversed-preference cell
(boundary case, vector-sum-invisible), (d) the highest-firing-rate DSI=0 bidirectional firer
(genuine zero, not silence-failure), and (e) a non-Pareto DSI=1.0 cell (high-selectivity but
dominated by a cheaper Pareto cell at the same DSI corner). All numbers are reproduced
verbatim from `results/cell_params.jsonl` and `results/data/pareto_front_seed3517.json`.

### Example 1 (Pareto cell 3, gen 56): rank-1 -- cheapest ATP, no selectivity

* **Role**: ATP-floor corner of the Pareto front, baseline DSI=0 cell.

* **Input/output record** (verbatim from `cell_params.jsonl`):

  ```json
  {"gen": 56, "dsi_signed": 0.0, "atp_per_spike_molecules": 779758.0730795636,
   "pd_rate_hz": 0.7142857142857143, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.9702195823367423, 0.5570260907127859, 0.21149005075946068,
    0.656034608083525, 2.8955783411466034, 0.5567226907127859, 0.4942283820113452,
    0.4815720913045775, 0.043681301884717096, 0.5135708249244376, 0.5965322244236608,
    0.17181102674440117, 0.015573135078577537, 0.4480078921005816, 0.9272014706738574,
    0.04772012410604015, 0.3624783290168571, 0.49159455346423204, 0.6824999110757265,
    0.7062814795927687, 0.07374829108186443, 0.4438034870988069, 0.9839017218816772,
    0.2538380906888108, 0.3146731010432953, 0.038055190141316295, 0.49298759011364224,
    0.18092871108154235, 0.038416040677604665, 0.41293125906117413, 0.36580465238546017,
    0.021933784302926043, 0.2197946421090838, 18.311064252918097, 215.14983005754513,
    1.8166657681217027, 0.0007069711834894443, 0.4507102107910745, 11.8914772425223,
    298.4979823033504, 101.04885037530762, 1.007334128683603, 131.8007000600058,
    0.45732179685894725, 483.8367570373423, 0.008168046458243585, 0.0030382066305729037,
    29.97796131353843, 0.6570532912786983, 0.005338765056458909, 0.33154064123083193,
    7.6843089384894885, 0.020532531996845158, 0.0003438570677937328,
    4.357700617731876, 0.005692793106540842, 4.152432716080935, 82.88660081797053,
    1.0473815569810772, -38.10822902040245, 2.842241606152064, -0.5657431607315644,
    4.481688986090205, 41.8420895118846, 17.357352380810365, 46.596453842661134,
    989682978.0706733, 0.07399535466951221]}
  ```

* **Why it matters**: This is the absolute ATP floor of the final front (0.78 M molec/spike,
  ~2.3x cheaper than t0126's ATP minimum 1.83 M). Cell fires reliably at exactly 1 spike per
  1.4 s in both directions (PD = ND = 0.714 Hz). The optimiser found a cell with the cheapest
  possible per-spike Na influx and no directional preference. The 14-d morphology vector is
  almost identical to Pareto cell 0's (same radii, same branch parameters), differing mainly
  in the 54-d electrophys block.

### Example 2 (Pareto cell 8, gen 59): low-DSI mid-front

* **Role**: Low-DSI shoulder of the Pareto front (DSI=0.333).

* **Input/output record**:

  ```json
  {"gen": 59, "dsi_signed": 0.3333333333333333, "atp_per_spike_molecules": 3519796.4929693933,
   "pd_rate_hz": 1.4285714285714286, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.9977003434181907, 0.5487814213879482, 0.20672869080144298,
    0.5253749571586867, 4.675020787884366, 0.5910321904345452, 0.5208878249029829,
    0.4748286140043425, 0.24882519335089213, 0.21366478149094406, 0.5996221708987867,
    0.17181102674440117, 0.015569672817376354, 0.29614017442815604, 0.9236209322800654,
    0.041078931039929905, 0.32540482712174906, 0.491594553464232, 0.6816664020816554,
    0.7065820554103192, 0.0742024106041132, 0.4421437036906715, 0.9835831328172512,
    0.8513175976863888, 0.9152832867188194, 0.03632796068301115, 0.4929865283068437,
    0.45970013489812336, 0.038415924504120576, 0.4474481957137322, 0.3782174322617566,
    0.02195919071813983, 0.21964635791530757, 10.601063088263595, 215.19499144040354,
    1.8149413800912633, 0.0007058506252247144, 0.4507193686259185, 16.83247226660091,
    310.30885816075147, 100.89030089300948, 0.9628420516535066, 119.16725611660307,
    0.4965727229884708, 484.0144014184858, 0.008167449614550884, 0.003278856272042676,
    29.61253614836762, 0.6568353825456559, 0.005060960769541928, 0.3942055691572568,
    7.641300151939003, 0.020532458107391453, 0.0004127472293181605, 3.353587806612686,
    0.008680715517301213, 4.273887810437473, 88.16762378486272, 0.9156320335625523,
    -82.51998283400552, 2.842241606152064, 0.7545119252149206, 4.498966409399077,
    41.74175538807879, 17.357352380810365, 29.960116175803336, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: Bidirectional firer with a 2:1 PD/ND ratio (2 spikes PD, 1 spike ND).
  The Pareto front captures this as the cheapest-ATP entry at DSI=0.333.

### Example 3 (Pareto cell 5, gen 58): DSI=0.455

* **Input/output record**:

  ```json
  {"gen": 58, "dsi_signed": 0.45454545454545453, "atp_per_spike_molecules": 3531691.6033927766,
   "pd_rate_hz": 1.9047619047619047, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.9817487480036226, 0.5566909088580603, 0.2062979187340712,
    0.7068164320824596, 4.685770381039472, 0.5910321904345452, 0.5208878249029829,
    0.4748286140043425, 0.24881520087066205, 0.21366478149094406, 0.5996221708987867,
    0.17181102674440117, 0.015569672817376354, 0.29619228774347697, 0.9236209322800654,
    0.04771522503154371, 0.32540482712174906, 0.491594553464232, 0.6822505935456417,
    0.5583387168135279, 0.07375596917996104, 0.4421437036906715, 0.9835831328172512,
    0.8513175976863888, 0.9152832867188194, 0.03632796068301115, 0.4930028019804168,
    0.4597001868405632, 0.038415924504120576, 0.4474481957137322, 0.3782174322617566,
    0.02195919071813983, 0.21964635791530757, 10.601063088263595, 215.19499144040354,
    1.8149413800912633, 0.0007058506252247144, 0.4507193686259185, 16.83247226660091,
    310.30885816075147, 100.89030089300948, 0.9628420516535066, 119.16725611660307,
    0.4965727229884708, 484.0144014184858, 0.008167449614550884, 0.003278856272042676,
    29.61253614836762, 0.6568353825456559, 0.005060960769541928, 0.3942055691572568,
    7.641300151939003, 0.020532458107391453, 0.0004127472293181605, 3.235977731094167,
    0.008680715517301213, 4.32600942817915, 84.75217084639812, 0.8160947587432896,
    -100.97490500709614, 2.834164204266713, 0.7472226849980499, 4.966278271144785,
    41.0411952524813, 17.0466209847016, 29.960116175803336, 972606775.9438262,
    0.0886527133865649]}
  ```

* **Why it matters**: Mid-front cell, PD/ND ratio 5:2 (2.66 spikes PD, 1 spike ND).

### Example 4 (Pareto cell 1, gen 53): DSI=0.538

* **Input/output record**:

  ```json
  {"gen": 53, "dsi_signed": 0.5384615384615384, "atp_per_spike_molecules": 3607153.9970873636,
   "pd_rate_hz": 2.3809523809523814, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.9811831249882795, 0.5469700333862715, 0.2190679387012859,
    0.7096364809289363, 3.3450137524582515, 0.5881585105263504, 0.5208878249029829,
    0.4748286140043425, 0.249086284257822, 0.20487463874771086, 0.5967531041173552,
    0.24520243825042704, 0.01683860232314994, 0.296192287743477, 0.9236209322800654,
    0.03234484807902578, 0.6507094579100318, 0.491594553464232, 0.6822505935456417,
    0.5583387168135279, 0.07420386581855139, 0.4443348092662913, 0.8836719856577957,
    0.8513175976863888, 0.959681969489085, 0.03631363454741215, 0.49300228431852144,
    0.44216022610360306, 0.038417491373368945, 0.4468814204965342, 0.3789196245106189,
    0.02520074934447928, 0.219806284537177, 10.047254627721285, 215.6376298718343,
    1.4885482137470185, 0.0006928887614335025, 0.4501330701587776, 59.5657062928439,
    296.57572823739895, 98.47201214618974, 0.9369445609740175, 132.6984818818401,
    2.181510298114604, 484.28879490346026, 0.008209086222637937, 0.008837067342411555,
    29.622961395926758, 0.6520800289516726, 0.005061881295361184, 0.3928083679140206,
    3.3102455696512356, 0.020532458107391453, 0.008096253273802586, 3.2640267164134924,
    0.008736514399818207, 4.280827064337009, 84.75217084639812, 0.8160947587432896,
    -100.97490500709614, 2.834164204266713, 0.7472226849980499, 4.966278271144785,
    41.0411952524813, 17.0466209847016, 29.960116175803336, 972606775.9438262,
    0.0886527133865649]}
  ```

* **Why it matters**: Adjacent in parameter space to cell 2 (Pareto-optimal local family);
  both cells span the mid-front region densely sampled by the optimiser.

### Example 5 (Pareto cell 2, gen 53): DSI=0.571 (Pareto median)

* **Input/output record**:

  ```json
  {"gen": 53, "dsi_signed": 0.5714285714285715, "atp_per_spike_molecules": 3633357.6653955295,
   "pd_rate_hz": 2.619047619047619, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.981933146481527, 0.5469808184241335, 0.2190688694062342,
    0.7069746834570778, 3.3574347848263013, 0.5906621518789003, 0.5208878249029829,
    0.4748286140043425, 0.2485199807914746, 0.24213217313848906, 0.599564522665132,
    0.1718058257444686, 0.01558314408916898, 0.288397059564707, 0.9236209322800654,
    0.04771522503154371, 0.38202980647793305, 0.491594553464232, 0.6823752523116261,
    0.6468498689860822, 0.07375596917996104, 0.4415804770059426, 0.9835831328172512,
    0.8509579032491443, 0.9149853382594646, 0.036334774282929395, 0.4930028019804168,
    0.45970018684056324, 0.03841592450412058, 0.4474491925237078, 0.37821388970272346,
    0.021959190718139825, 0.21964635791530757, 10.600326308496344, 215.19582300414146,
    1.8149413800912633, 0.0007060373853462631, 0.4507193686259185, 11.594352416396957,
    310.30885816075147, 100.89030089300948, 0.9628420516535066, 119.09255675963841,
    0.49723318780045545, 483.8492279847629, 0.008167484652711372, 0.003278856272042676,
    29.61253614836762, 0.6568353825456559, 0.005060960769541928, 0.3928083679140206,
    7.641300151939003, 0.020532458107391453, 0.00041760544666301396, 3.3535876482923075,
    0.008769045603021221, 2.0683580261752224, 84.76093214883605, 0.814685182303045,
    -117.60979383293262, 2.83867033395692, 0.7545119252149206, 4.498966409399077,
    41.71915632266252, 17.337404044372025, 29.960116175803336, 972317725.1798302,
    0.0882493909088465]}
  ```

* **Why it matters**: The **Pareto-median** DSI cell. PD/ND ratio ~3:1 (2.62 vs 0.71 Hz).

### Example 6 (Pareto cell 0, gen 52): DSI=0.684

* **Input/output record**:

  ```json
  {"gen": 52, "dsi_signed": 0.6842105263157895, "atp_per_spike_molecules": 3722110.8498217664,
   "pd_rate_hz": 3.8095238095238098, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.965651721916142, 0.549060689490445, 0.23451610550883278,
    0.7811637648246735, 4.687163839356694, 0.5405346788703327, 0.21611587719142253,
    0.5091038681064477, 0.04540248618481151, 0.332207910857165, 0.5821052480926473,
    0.1717953386983106, 0.01557761709905085, 0.9597401791375242, 0.927420003312181,
    0.03195414054039848, 0.3648862823239679, 0.49165139975022104, 0.6821394961413815,
    0.644954865072608, 0.07376102417721712, 0.48311860969927256, 0.9829607994552303,
    0.2538380906888108, 0.2679651400313876, 0.0380551901413163, 0.49298759011364224,
    0.18092871108154235, 0.03841604067760466, 0.4129312590611741, 0.36580465238546017,
    0.021933784302926043, 0.21979464210908378, 18.311064252918097, 215.14983005754513,
    1.8166657681217027, 0.0007069711834894443, 0.4507102107910745, 11.8914772425223,
    298.4979823033504, 101.04885037530762, 1.007334128683603, 131.8007000600058,
    0.45732179685894725, 483.8367570373423, 0.008168046458243585, 0.0030382066305729037,
    29.97796131353843, 0.6570532912786983, 0.005338765056458909, 0.33154064123083193,
    7.6843089384894885, 0.020532531996845158, 0.0003438570677937328, 3.353587806612686,
    0.008773691260285887, 2.069457649649589, 84.75313752127484, 0.8191748745199371,
    -117.62151086051735, 2.842241606152064, -0.5657431607315644, 4.481688986090205,
    41.8420895118846, 17.357352380810365, 46.596453842661134, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: High-mid DSI cell (PD/ND ratio ~5.3:1). Note the morphology vector is
  nearly identical to Pareto cells 2 and 3 (same somatic radius 3.354, same dendrite branching
  parameters) -- the optimiser found a local family of cells that span the front by varying
  the 54-d electrophys block.

### Example 7 (Pareto cell 6, gen 59): DSI=0.806

* **Input/output record**:

  ```json
  {"gen": 59, "dsi_signed": 0.8064516129032259, "atp_per_spike_molecules": 3814251.9700956624,
   "pd_rate_hz": 6.666666666666667, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.9942336321977116, 0.5566378466100754, 0.20708879580944434,
    0.5374088886942366, 3.3216929796614495, 0.5910321904345452, 0.5208878249029829,
    0.4748286140043425, 0.24881520087066205, 0.21366478149094406, 0.5996221708987867,
    0.17181102674440117, 0.015569672817376354, 0.29614017442815604, 0.9236209322800654,
    0.04771522503154371, 0.32540482712174906, 0.491594553464232, 0.6824999110757265,
    0.7062814795927687, 0.07374829108186443, 0.4438034870988069, 0.9839017218816772,
    0.2538380906888108, 0.3146731010432953, 0.038055190141316295, 0.49298759011364224,
    0.18092871108154235, 0.038416040677604665, 0.41293125906117413, 0.36580465238546017,
    0.021933784302926043, 0.2197946421090838, 18.311064252918097, 215.14983005754513,
    1.8166657681217027, 0.0007069711834894443, 0.4507102107910745, 11.8914772425223,
    298.4979823033504, 101.04885037530762, 1.007334128683603, 131.8007000600058,
    0.45732179685894725, 483.8367570373423, 0.008168046458243585, 0.0030382066305729037,
    29.97796131353843, 0.6570532912786983, 0.005338765056458909, 0.33154064123083193,
    7.6843089384894885, 0.020532531996845158, 0.0003438570677937328, 3.245208893849841,
    0.005692793106540842, 4.327068810537554, 80.14629413195867, 1.2233702680486807,
    -109.10720466574128, 2.842241606152064, -0.5657431607315644, 4.481688986090205,
    41.8420895118846, 17.357352380810365, 46.596453842661134, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: High-DSI shoulder of the front (PD/ND ratio ~9.3:1).

### Example 8 (Pareto cell 7, gen 59): DSI=0.870

* **Input/output record**:

  ```json
  {"gen": 59, "dsi_signed": 0.8695652173913043, "atp_per_spike_molecules": 5026614.4920632765,
   "pd_rate_hz": 10.238095238095237, "nd_rate_hz": 0.7142857142857143,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.9543886378664526, 0.5447089290195486, 0.8906485226692787,
    0.045783574226822185, 3.193800030415547, 0.5860181891820452, 0.7283878249029829,
    0.4748286140043425, 0.6242715925478746, 0.21366478149094406, 0.5963090458987867,
    0.17181102674440117, 0.015569672817376354, 0.29614017442815604, 0.9236209322800654,
    0.04771522503154371, 0.32540482712174906, 0.491594553464232, 0.6824999110757265,
    0.7062814795927687, 0.07374829108186443, 0.4438034870988069, 0.9839017218816772,
    0.2538380906888108, 0.3146731010432953, 0.038055190141316295, 0.49298759011364224,
    0.18092871108154235, 0.038416040677604665, 0.41293125906117413, 0.36580465238546017,
    0.021933784302926043, 0.2197946421090838, 18.311064252918097, 215.14983005754513,
    1.8166657681217027, 0.0007069711834894443, 0.4507102107910745, 11.8914772425223,
    298.4979823033504, 101.04885037530762, 1.007334128683603, 131.8007000600058,
    0.45732179685894725, 483.8367570373423, 0.008168046458243585, 0.0030382066305729037,
    29.97796131353843, 0.6570532912786983, 0.005338765056458909, 0.33154064123083193,
    7.6843089384894885, 0.020532531996845158, 0.0003438570677937328, 5.240789921672488,
    0.009788415195929603, 3.9178472891816776, 33.02272257378635, 0.8114270568478197,
    -109.10720466574128, 2.842241606152064, -0.5657431607315644, 4.481688986090205,
    41.8420895118846, 17.357352380810365, 46.596453842661134, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: Near-elite high-DSI cell with the highest PD rate on the Pareto front
  (10.24 Hz). Morphology departs from the canonical family -- larger somatic radius (5.24 vs
  3.35), shorter branches.

### Example 9 (Pareto cell 4, gen 57): rank-9 -- max DSI = 1.0, headline cell

* **Role**: ND-silenced canonical DS-RGC corner. The **headline cell**.

* **Input/output record**:

  ```json
  {"gen": 57, "dsi_signed": 1.0, "atp_per_spike_molecules": 6659150.098702777,
   "pd_rate_hz": 6.428571428571429, "nd_rate_hz": 0.0,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.7131544010820338, 0.1064220020525432, 0.2129823195620606,
    0.5392836879692049, 2.9228721402105823, 0.5910321904345452, 0.5208878249029829,
    0.4748286140043425, 0.24881520087066205, 0.21366478149094406, 0.5996221708987867,
    0.17181102674440117, 0.015569672817376354, 0.29614017442815604, 0.9236209322800654,
    0.04771522503154371, 0.32540482712174906, 0.491594553464232, 0.6824999110757265,
    0.7062814795927687, 0.07374829108186443, 0.4438034870988069, 0.9839017218816772,
    0.2538380906888108, 0.3146731010432953, 0.038055190141316295, 0.49298759011364224,
    0.18092871108154235, 0.038416040677604665, 0.41293125906117413, 0.36580465238546017,
    0.021933784302926043, 0.2197946421090838, 18.311064252918097, 215.14983005754513,
    1.8166657681217027, 0.0007069711834894443, 0.4507102107910745, 11.8914772425223,
    298.4979823033504, 101.04885037530762, 1.007334128683603, 131.8007000600058,
    0.45732179685894725, 483.8367570373423, 0.008168046458243585, 0.0030382066305729037,
    29.97796131353843, 0.6570532912786983, 0.005338765056458909, 0.33154064123083193,
    7.6843089384894885, 0.020532531996845158, 0.0003438570677937328, 3.554794611937886,
    0.010767876316829867, 4.272886937700415, 83.55819988796108, 0.8104940488057664,
    -109.10720466574128, 2.842241606152064, -0.5657431607315644, 4.481688986090205,
    41.8420895118846, 17.357352380810365, 46.596453842661134, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: **Headline cell.** Canonical DSI=1.0 cell with R_ND = 0 (ND fully
  silenced). Both vector-sum and signed DSI give 1.0 here -- the sign distinction does not
  matter when one direction is silent. ATP per spike (6.66 M) is comparable to t0126's DSI=1.0
  corner (7.82 M); the morphological substrate (somatic radius 3.55, similar dendrite
  geometry) is also similar to t0126's gen-56 elite.

### Example 10 (silenced cell, Phase A): worst-case input -- silence guard tripped

* **Role**: Silence-failed cell from Phase A random init (one of 264 silenced cells in the
  whole run). Shows the silence guard at work.

* **Input/output record**:

  ```json
  {"gen": -1, "dsi_signed": -1.0, "atp_per_spike_molecules": 20000000000.0,
   "pd_rate_hz": 0.0, "nd_rate_hz": 0.0,
   "silence_failed": true, "n_errors": 0,
   "param_vector_68d": [0.25878977525008085, 0.2304143822923089, 0.6048009557895526,
    0.7234724710977472, 0.9078812213907486, 0.7568823373586148, 0.6543263775220793,
    0.9272068286069013, 0.18856175049402502, 0.6107207196067834, 0.6948802895617923,
    0.7659081325366137, 0.10612720415872007, 0.3060829562833286, 0.18482311595411377,
    0.014869881820078823, 0.3635193049495267, 0.6195886011762146, 0.6020213572869298,
    0.4807620020181859, 0.21692797672432937, 0.13066517822080572, 0.8568814432089482,
    0.5470195067960586, 0.2710260317937067, 0.5751213129620098, 0.18019729833005612,
    0.40432127478432, 0.058195023268322046, 0.2697106869014023, 0.46105528569389996,
    0.5066672931641812, 0.5660019773566321, 14.030019773566321, 245.92011953942596,
    0.7770502810787114, 0.0009055751828366915, 0.36577517892810065, 28.064066854596687,
    301.46823472470395, 78.49562948298104, 0.6989800773720488, 138.97083538735927,
    1.0832611301720585, 491.86729220676685, 0.013112061562547925, 0.005566081773070725,
    20.86797737488537, 0.5316540572930117, 0.005019547820036916, 0.18886070321257124,
    7.029823186773817, 0.014773977879671428, 0.0007078708470906085, 6.176459822168064,
    0.03650728167842061, 2.4319837988089337, 63.93996019921554, 1.0697526404989232,
    -69.43712517094404, 2.842241606152064, -0.5657431607315644, 4.481688986090205,
    41.8420895118846, 17.357352380810365, 46.596453842661134, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: Silence guard tripped (`pd_spikes_sum < 3` -> sentinel `dsi_signed =
  -1.0`, ATP set to worst-case 2.0e+10). The cell evaluator did not error (`n_errors=0`); the
  cell simply fails to fire enough spikes in the PD direction for the DSI computation to be
  meaningful, so the sentinel is returned.

### Example 11 (deepest reversed-preference cell, gen 14): boundary case -- vector-sum-invisible

* **Role**: The deepest reversed-preference cell in the cohort (DSI = -0.778). Would be
  collapsed to magnitude 0.778 (looking like a high-DSI PD-preferring cell!) under vector-sum.

* **Input/output record**:

  ```json
  {"gen": 14, "dsi_signed": -0.7777777777777778, "atp_per_spike_molecules": 7053780.226828762,
   "pd_rate_hz": 0.7142857142857143, "nd_rate_hz": 5.714285714285714,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.910792655775345, 0.1916757571783443, 0.9122288541366767,
    0.9132180220691506, 4.903732842841823, 0.5237664681728923, 0.7158064820700776,
    0.8064060660797502, 0.2987036197902054, 0.030023466908144283, 0.9036854608527795,
    0.04330841881810872, 0.07533812036834828, 0.5283376800385928, 0.6385700015815432,
    0.011497822908174316, 0.7466937867181298, 0.2814203434927574, 0.3960220824770017,
    0.6608019586013927, 0.7028075488144266, 0.5226094822937502, 0.7770175815796817,
    0.6796725330687286, 0.4569528317145571, 0.4376687283063935, 0.4395029820854466,
    0.038088659796841866, 0.3024488036517866, 0.6024822085322316, 0.4017879866879107,
    0.20061115077720676, 0.5031586127537074, 18.91120226086204, 264.04859603552105,
    1.5728820906205107, 0.0005725988796167482, 0.19443866717891193, 49.18886184478366,
    275.79842608015425, 60.94005078029115, 1.087069930247648, 95.30385822925956,
    0.41311517898168524, 470.0566330373423, 0.013867018541686884, 0.0028148068862739543,
    33.05537923338488, 0.5320527033797603, 0.0035728167791659145, 0.32867886824069355,
    7.6843089384894885, 0.014957027077729833, 0.0004158466778988336, 6.813014872036037,
    0.010841617008927037, 3.227003116036107, 85.88112802715037, 0.8048509702068086,
    -34.66170268404014, 2.819801166732084, -0.20094314071589407, 4.402032015003036,
    44.86011617812716, 18.61210358013137, 27.92216034041517, 998722038.2030763,
    0.07399535466951221]}
  ```

* **Why it matters**: **Key headline finding.** This cell fires 8x more in the ND direction
  than the PD direction (5.71 Hz vs 0.71 Hz). Under signed DSI: -0.778 -- correctly flagged as
  reversed-preference. Under vector-sum DSI: +0.778 -- indistinguishable from a true
  high-selectivity PD-preferring cell. This is the artefact-free version of the structure that
  vector-sum DSI silently discards. There are 95 such cells in this cohort, and one of them
  (gen 14, cell shown here) achieves a magnitude of 0.778 -- a value high enough to
  potentially enter the Pareto front under vector-sum if its ATP were sufficiently low.

### Example 12 (DSI=0 high-rate cell, gen 2): genuine zero -- not a silence failure

* **Role**: Highest-firing-rate DSI=0 cell. Shows that DSI=0 in this cohort includes both
  low-rate cells (1 spike per direction) and high-rate bidirectional firers.

* **Input/output record**:

  ```json
  {"gen": 2, "dsi_signed": 0.0, "atp_per_spike_molecules": 37663946.7088488,
   "pd_rate_hz": 47.857142857142854, "nd_rate_hz": 47.857142857142854,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.20877144064411148, 0.6920288635257796, 0.49186226086573204,
    0.5234836879692049, 3.519652554066717, 0.4663164681728923, 0.32490648207007757,
    0.32485286140043425, 0.18857036197902054, 0.030023466908144283, 0.9036854608527795,
    0.04330841881810872, 0.07533812036834828, 0.5283376800385928, 0.6385700015815432,
    0.011497822908174316, 0.7466937867181298, 0.2814203434927574, 0.39602208247700175,
    0.6608019586013927, 0.7028075488144266, 0.5226094822937502, 0.7770175815796817,
    0.6796725330687286, 0.4569528317145571, 0.4376687283063935, 0.4395029820854466,
    0.038088659796841866, 0.3024488036517866, 0.6024822085322316, 0.4017879866879107,
    0.20061115077720676, 0.5031586127537074, 18.91120226086204, 264.04859603552105,
    1.5728820906205107, 0.0005725988796167482, 0.19443866717891193, 49.18886184478366,
    275.79842608015425, 60.94005078029115, 1.087069930247648, 95.30385822925956,
    0.41311517898168524, 470.0566330373423, 0.013867018541686884, 0.0028148068862739543,
    33.05537923338488, 0.5320527033797603, 0.0035728167791659145, 0.32867886824069355,
    7.6843089384894885, 0.014957027077729833, 0.0004158466778988336, 4.0783649086522074,
    0.013742105537891108, 4.109684306186063, 32.86946854049196, 1.7231458437056103,
    -34.66170268404014, 2.819801166732084, -0.20094314071589407, 4.402032015003036,
    44.86011617812716, 18.61210358013137, 27.92216034041517, 998722038.2030763,
    0.07399535466951221]}
  ```

* **Why it matters**: Fires at 47.86 Hz in BOTH directions (the same number of spikes per
  direction); not silent, not biased. This cell would have `dsi_vector_sum = 0` and
  `dsi_signed = 0`; the two metrics agree on the DSI=0 cluster. ATP per spike is very high
  (3.77e+07) because the cell maintains a high tonic firing rate, so it is NOT Pareto-optimal
  (the Pareto front prefers the low-ATP cheap-firing variant of DSI=0).

### Example 13 (non-Pareto DSI=1.0 cell, gen 31): high-selectivity but dominated

* **Role**: DSI=1.0 cell that did NOT make the Pareto front because it is dominated by Pareto
  cell 4 (gen 57) at lower ATP.

* **Input/output record**:

  ```json
  {"gen": 31, "dsi_signed": 1.0, "atp_per_spike_molecules": 11026666.066632094,
   "pd_rate_hz": 15.0, "nd_rate_hz": 0.0,
   "silence_failed": false, "n_errors": 0,
   "param_vector_68d": [0.5480007132862284, 0.08465317005378974, 0.23184089193554017,
    0.04531837574226184, 2.398934706713197, 0.4663164681728923, 0.32490648207007757,
    0.32485286140043425, 0.18857036197902054, 0.030023466908144283, 0.9036854608527795,
    0.04330841881810872, 0.07533812036834828, 0.5283376800385928, 0.6385700015815432,
    0.011497822908174316, 0.7466937867181298, 0.2814203434927574, 0.3960220824770017,
    0.6608019586013927, 0.7028075488144266, 0.5226094822937502, 0.7770175815796817,
    0.6796725330687286, 0.4569528317145571, 0.4376687283063935, 0.4395029820854466,
    0.038088659796841866, 0.3024488036517866, 0.6024822085322316, 0.4017879866879107,
    0.20061115077720676, 0.5031586127537074, 18.91120226086204, 264.04859603552105,
    1.5728820906205107, 0.0005725988796167482, 0.19443866717891193, 49.18886184478366,
    275.79842608015425, 60.94005078029115, 1.087069930247648, 95.30385822925956,
    0.41311517898168524, 470.0566330373423, 0.013867018541686884, 0.0028148068862739543,
    33.05537923338488, 0.5320527033797603, 0.0035728167791659145, 0.32867886824069355,
    7.6843089384894885, 0.014957027077729833, 0.0004158466778988336, 3.5067928320213107,
    0.009088123540728057, 4.272886937700415, 46.223899948904855, 1.214958515174849,
    -109.10720466574128, 2.842241606152064, -0.5657431607315644, 4.481688986090205,
    41.8420895118846, 17.357352380810365, 46.596453842661134, 989682978.0706733,
    0.07399535466951221]}
  ```

* **Why it matters**: Achieves DSI=1.0 (ND fully silenced) at the higher PD rate (15 Hz, vs
  Pareto cell 4's 6.43 Hz) but at 1.7x higher ATP per spike (11.03 M vs 6.66 M). Dominated by
  Pareto cell 4 in the F objective space.

## Analysis

* **Signed DSI surfaces 95 reversed-preference cells** (1.7% of viable cells) that would be
  silently collapsed to positive magnitudes under vector-sum DSI. The deepest reversal
  (DSI=-0.778, Example 11\) is exactly the magnitude of a high-selectivity Pareto candidate
  under vector-sum -- this is the kind of contamination the signed re-evaluation was designed
  to detect.

* **None of the 95 reversed-preference cells reach the t0129 Pareto front.** They are
  dominated in F-space by the large cluster of DSI=0 cells with cheaper ATP. So under signed
  DSI the Pareto front is "clean" (only positive-DSI cells), but under vector-sum DSI the
  reversed cells WOULD have been Pareto candidates if their ATP were sufficiently low.

* **Pareto-front qualitative structure is preserved across the two DSI definitions and across
  the two seeds.** Both t0126 and t0129 span DSI in `[0, 1]` at ATP in the 0.8-8 M molec/spike
  range. The 2.3x ATP-minimum reduction in t0129 is seed variation, not a methodological
  change.

* **Real per-cell firing rates differ dramatically from t0126's `pd_rate_hz = 40`
  placeholder.** Pareto-median PD rate in t0129 is 2.62 Hz; Pareto-headline PD rate is 6.43
  Hz; max non-Pareto PD rate is ~48 Hz. The placeholder was off by a factor of 6-50 from the
  true values on this cohort, biasing any downstream analysis that consumed it (e.g.,
  joint-pass thresholds at PD >= 30 Hz would have classified essentially every t0126 Pareto
  cell as "joint-pass" when in truth almost no Pareto cell fires above 30 Hz).

* **Local-CPU runtime contradiction with plan assumption.** The plan estimated 8-12h
  wall-clock for the NSGA-II run on local CPU based on t0126's ~9h envelope on the same
  Vast.ai 7C13 partition. The local-CPU attempt was killed early after extrapolating ~5-7 days
  for 60 generations on 4 Windows workers (see `results/local_killed_run/` for the preserved
  attempt). The Vast.ai re-run completed in 3.39h active window. The plan's local-CPU
  assumption was a misestimate; setup-machines was un-skipped to recover.

* **Headline cell (Pareto cell 4, gen 57, DSI=1.0) is qualitatively identical to t0126's
  headline.** Both are ND-silenced at the canonical DS-RGC corner. The ATP delta (6.66 M vs
  7.82 M = -15%) and morphology delta (both somatic radii ~3.5, similar dendrite branching)
  are within single-seed variation.

* **Sign-flip count for t0126 cannot be recovered.** This is the single biggest limitation of
  the comparison. Recovery would require a re-run of t0126 seed 8929 with the corrected
  evaluator, which is out of scope for this task.

## Limitations

* **Single seed (3517).** This is a 1-seed run; the count of viable negative-DSI cells (95)
  and the precise Pareto-front shape will vary across seeds. A multi-seed follow-up is needed
  to establish stable fractions and confidence intervals.

* **t0126 sign-flip count unknowable.** Without per-direction spike counts in t0126's
  artefacts (and with `pd_rate_hz=40` being a synthesised placeholder), the question "how many
  of t0126's Pareto cells were actually reversed-preference?" cannot be answered from existing
  data.

* **Antipodal-only protocol.** The signed DSI here is the 2-direction antipodal-pair version,
  not the full angular tuning curve. Tasks needing the angular preferred direction (`atan2` of
  the vector sum) must run an N-direction sweep with N >= 12.

* **No per-spike Carter-Bean / MI diagnostics.** This run drops `cell_trace.jsonl` and uses
  `cell_params.jsonl` instead. Per-AP Carter-Bean / MI / fine-grained timing diagnostics are
  not available on a per-cell basis for t0129 (only the smoke-gate canonical anchor cell was
  recorded; see `logs/steps/009_implementation/smoke_gate.json`).

* **t0080 MOD-dependent smoke gate check 1 (NEURON / MOD library import) was deferred locally
  but ran successfully on the Vast.ai remote.** On the local Windows workstation, MOD
  compilation via `mknrndll` did not produce a loadable DLL in the path order the bootstrap
  expects; on the Vast.ai Linux instance, `nrnivmodl` succeeded and check 1 passed.

* **`results/local_killed_run/cell_params_local_killed.jsonl` is preserved separately and was
  NOT used in this analysis.** That file holds the early-aborted 4-worker local-CPU attempt (a
  partial Phase A cohort before the orchestrator killed the run on extrapolated 5-7 day
  completion time). The headline cohort is exclusively the Vast.ai-completed seed-3517 run.

* **No multi-direction tuning curve metrics.** Three other registered metrics
  (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`) require a full
  angular sweep and are not reported for this task.

## Verification

Verificators expected to PASS in the reporting step (step 015):

* `verify_task_metrics` -- **PASSED** (3 variants, only registered metric key is
  `direction_selectivity_index`; 0 errors, 0 warnings). Run in the results step.
* `verify_task_folder` -- **PASSED** (0 errors, 1 warning: empty `logs/searches/`).
* `verify_task_results` -- expected PASS (all mandatory sections present; per-spec
  `spec_version: "2"` for both results documents; `## Task Requirement Coverage` is the last
  `##` section; `## Examples` has 13 entries with full input/output records).
* `verify_task_dependencies` -- expected PASS (single dependency
  `t0126_bedb_dsi_atp_per_spike_nsga2_60gen` is completed and read-only).
* `verify_task_complete` -- to be run after the suggestions step.

Asset verification:

* Predictions asset `nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/` -- spec v2 compliant
  (details.json + description.md + files/ with 2 prediction files; mandatory sections all
  present in description.md; categories all valid; cross-checked structurally against t0126's
  analogous asset).

* Answer asset `does-signed-dsi-change-t0126-pareto-structure/` -- spec v2 compliant
  (details.json + short_answer.md + full_answer.md; mandatory sections all present; `##
  Answer` is 5 sentences; evidence references include the t0126 task ID).

Smoke gate (REQ-6, REQ-19): smoke gate ran on the Vast.ai remote during the implementation
step; all 9 checks pass and the Carter-Bean canonical anchor cell ATP/AP/cm sits in the
first-principles `[1e8, 1e9]` PASS band. See `logs/steps/009_implementation/smoke_gate.json`
for the per-check verdicts.

## Files Created

This results step produces or updates the following files:

* `results/results_summary.md` (this task: in-progress; will be marked complete in reporting)
* `results/results_detailed.md` (this file)
* `results/metrics.json` (3-variant explicit format; only registered key
  `direction_selectivity_index`)
* `results/images/pareto_front_dsi_signed_vs_atp.png`
* `results/images/dsi_signed_distribution.png`
* `results/images/pd_vs_nd_rate_scatter.png`
* `results/images/pareto_t0126_vs_t0129_overlay.png`
* `results/data/t0126_vs_t0129_sign_flip_count.json` (comparator sidecar consumed by the
  metrics builder)
* `results/cell_params.jsonl` (written by the implementation step; not modified here)
* `results/data/pareto_front_seed3517.json` (written by the implementation step; not modified
  here)
* `results/data/all_evaluations_seed3517.json.gz` (written by the implementation step; not
  modified here)
* `results/data/hv_trajectory_seed3517.json` (written by the implementation step; not modified
  here)
* `results/data/algorithm_config.json` (written by the implementation step; not modified here)
* `results/costs.json` (written by the teardown step; not modified here)
* `results/remote_machines_used.json` (written by the teardown step; not modified here)
* `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/details.json`
* `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/description.md`
* `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/files/predictions-pareto-9-cells.jsonl`
* `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/files/predictions-all-cells.jsonl.gz`
* `assets/answer/does-signed-dsi-change-t0126-pareto-structure/details.json`
* `assets/answer/does-signed-dsi-change-t0126-pareto-structure/short_answer.md`
* `assets/answer/does-signed-dsi-change-t0126-pareto-structure/full_answer.md`
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/build_t0129_charts.py` (chart-generation
  script for the four required PNGs)
* `tasks/t0129_t0126_signed_dsi_real_rates_1seed/code/build_t0129_assets.py` (asset-generation
  script for the predictions and answer assets)

## Task Requirement Coverage

Operative task description (verbatim from `task_description.md`):

> Fork of t0126's evaluator and NSGA-II driver into `tasks/t0129_*/code/`. **No changes to t0126
> itself**. All other t0126 protocol parameters preserved verbatim. Three evaluator changes: signed
> DSI replacing vector-sum; real per-cell PD/ND firing rates; per-cell parameter dump to
> `results/cell_params.jsonl`. Expected: 1 predictions asset, 1 answer asset. Out of scope: t0127,
> t0128.

Each requirement (REQ-1 through REQ-23 from `plan/plan.md`) is enumerated below with status
and evidence. The `results` step (step 012) is responsible for REQ-8, REQ-9, REQ-10, REQ-20,
REQ-21. REQ-1 through REQ-7, REQ-12 through REQ-19, REQ-22, REQ-23 were satisfied by the
implementation step (step 009) and are reported here for completeness.

| REQ | Status | Evidence |
| --- | --- | --- |
| REQ-1 (signed-DSI helper + unit tests) | Done | `code/evaluator.py` `_signed_antipodal_dsi`; `code/test_evaluator_dsi_signed.py` (9 tests pass) |
| REQ-2 (rename `dsi_vector_sum -> dsi_signed`) | Done | Grep of `code/` returns no `dsi_vector_sum` references except in the t0126 cross-comparator (legitimate read of t0126's frozen artefact field name) |
| REQ-3 (`pd_rate_hz` + `nd_rate_hz` as named fields) | Done | `code/evaluator.py` `CellEvalResult.pd_rate_hz` and `nd_rate_hz`; both populated in `_summarise_trials` from real per-direction spike counts |
| REQ-4 (`cell_params.jsonl` per-cell sink) | Done | `results/cell_params.jsonl` has 5,760 rows (96 Phase A + 5,664 NSGA-II) with all required fields; no `pd_rate_hz == 40.0` placeholder anywhere; sink path captured in `BedBV3MorphProblem.__init__` so it pickles to workers |
| REQ-5 (`run_seed3517.sh` wrapper) | Done | `code/run_seed3517.sh` (no `T0126_CELL_TRACE_JSONL` env var; the cell_params path is captured via constructor) |
| REQ-6 (smoke gate passes after DSI rename) | Done | `logs/steps/009_implementation/smoke_gate.json` reports 9/9 PASS; Carter-Bean canonical AIS ATP/AP/cm in `[1e8, 1e9]` band |
| REQ-7 (60-gen NSGA-II run completes) | Done | `results/data/pareto_front_seed3517.json` has 9 cells; `results/data/hv_trajectory_seed3517.json` has 60 entries; `NSGA2_EXIT=0`, `watchdog_tripped=false` |
| REQ-8 (four required charts) | Done | `results/images/pareto_front_dsi_signed_vs_atp.png` (75 KB), `dsi_signed_distribution.png` (84 KB), `pd_vs_nd_rate_scatter.png` (99 KB), `pareto_t0126_vs_t0129_overlay.png` (106 KB) -- all > 50 KB sanity floor; all embedded in the `## Visualizations` section above |
| REQ-9 (predictions asset) | Done | `assets/predictions/nsga2-dsi-signed-atp-per-spike-bedb-morph-t0129/` exists with `details.json` (spec v2), `description.md` (all mandatory sections), `files/predictions-pareto-9-cells.jsonl` (9 Pareto cells with full 68-d vectors), `files/predictions-all-cells.jsonl.gz` (gzipped all-cells dump, 9.2 MB raw); `verify_task_folder` passes |
| REQ-10 (answer asset) | Done | `assets/answer/does-signed-dsi-change-t0126-pareto-structure/` exists with `details.json` (spec v2), `short_answer.md` (5 sentences in `## Answer`, opens with "Yes"), `full_answer.md` (all 9 mandatory sections including `## Sources` with markdown reference links); `verify_task_folder` passes |
| REQ-11 (no t0127 or t0128 references) | Done | Grep of `tasks/t0129_t0126_signed_dsi_real_rates_1seed/{code,assets,results}/` for `t0127` and `t0128` returns zero matches |
| REQ-12 (`_POOL_RESTART_EVERY = 10`) | Done | `code/constants.py` and `results/data/algorithm_config.json` `pool_restart_every: 10` |
| REQ-13 (HV-plateau auto-stop disabled) | Done | `algorithm_config.json` has no `HVPlateauTermination`; live `TerminationCollection` contains only `MaximumGenerationTermination(60)` and `CostWatchdogTermination($8)` |
| REQ-14 (hard constants preserved) | Done | `POP_SIZE=96`, `N_EVAL_SEEDS=3`, `N_DIRECTIONS=2`, `N_GEN=60`, `SILENCE_PD_SPIKES_THRESHOLD=3`, `WORST_CASE_DSI=-1.0`, `TSTOP_MS=1400` -- all verified in `code/constants_morphology.py` and `code/constants.py` |
| REQ-15 (GA seed 3517 is fresh) | Done | `T0129_SEEDS=(3517,)` in `code/constants.py`; not in lineage seed set `{441, 6650, 8929, 2608, 8276, 9986}` |
| REQ-16 (fork t0126 verbatim, then targeted edits) | Done | ~37 Python files forked from `tasks/t0126_*/code/`; only the three behavioural changes plus import-path rewrites differ |
| REQ-17 (`CELL_PARAMS_JSONL` in paths) | Done | `code/paths.py` `CELL_PARAMS_JSONL: Path = RESULTS_DIR / "cell_params.jsonl"` |
| REQ-18 (reuse `atp_per_spike`, `recorder`, `bootstrap`, `cost_watchdog`) | Done | All four modules forked verbatim with only import-path rewrites |
| REQ-19 (smoke gate runs and reports) | Done | See REQ-6 |
| REQ-20 (compute sign-flip count vs t0126) | **Partial** | The comparator computed the upper bound (4 t0126-Pareto cells with `dsi_vector_sum > 0.5`); the true sign-flip count is **unknowable** from t0126's persisted data because per-direction spike counts were not recorded and `pd_rate_hz=40` is a synthesised placeholder. Documented in `results/data/t0126_vs_t0129_sign_flip_count.json` and called out as a limitation in the answer asset, results_detailed.md (this section), and results_summary.md. |
| REQ-21 (`metrics.json` multi-variant) | Done | `results/metrics.json` has 3 variants (`t0129-seed3517-headline`, `t0129-seed3517-pareto-median`, `t0129-vs-t0126-sign-flipped`); only registered key `direction_selectivity_index` appears in `metrics`; `verify_task_metrics` PASSED |
| REQ-22 (DSI silence-guard regression tests pass) | Done | `code/test_evaluator_dsi_signed.py` 9/9 tests pass (per `logs/steps/009_implementation/` test log) |
| REQ-23 (smoke gate JSON persists DSI fixture) | Done | `logs/steps/009_implementation/smoke_gate.json` includes the canonical-cell DSI fixture |

</details>
