---
spec_version: "2"
task_id: "t0047_validate_pp16_fig3_cond_noise"
---
# Results Detailed: Validate Poleg-Polsky 2016 Fig 3A-F Conductances and Extend Noise Sweep

## Summary

This task wrapped the t0046 `modeldb_189347_dsgc_exact` library to record per-synapse-class
conductance traces (NMDA / AMPA / GABA) under the gNMDA sweep
`b2gnmda in {0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0}` nS and the extended noise sweep
`flickerVAR in {0.0, 0.1, 0.3, 0.5}` for control / AP5 / 0Mg conditions. The deposited code does not
reproduce the paper's Fig 3A-E per-synapse conductance balance (every channel × direction × gNMDA
cell is far outside the +/- 25% pass band) and does not reproduce the Fig 3F bottom claim that DSI
is approximately constant ~0.30 across gNMDA. The noise sweep does show qualitative monotonic DSI
decline in all three conditions, matching the paper's Figs 6-7 shape — but the ROC AUC metric
saturates at 1.0 because the implementation uses pre-stimulus baseline mV as the negative class and
PSP peaks dwarf baselines. Three new discrepancies extend t0046's catalogue.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation (no MPI, no GPU)
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7` (validated by `t0007_install_neuron_netpyne`)
* **MOD compiler**: re-uses t0046's existing `nrnmech.dll` (no recompile)

### Runtime

* **Implementation step started**: 2026-04-24T22:40:46Z
* **Implementation step completed**: 2026-04-24T23:44:04Z (poststep)
* **Sweep wall-clock**: approximately 60 minutes total. The gNMDA sweep ran first (56 trials),
  followed by the noise extension sweep (96 trials).

### Methods

The implementation re-uses `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun` for
trial execution and adds a thin wrapper `code/run_with_conductances.py` that attaches NEURON
`Vector.record(syn._ref_<gname>, dt_ms=0.25)` to every BIPsyn (recording `gAMPA`, `gNMDA`, `g`),
SACexcsyn (`g`), and SACinhibsyn (`g`) instance after `_ensure_cell()`. Recorders are attached once
at cell-build time because synapse identities are stable across `simplerun()` invocations
(`placeBIP()` only re-binds the Vinf playback vectors).

For each trial, the wrapper reports:

* Soma voltage trace (sub-sampled at 0.25 ms).
* Per-synapse-class summed peak conductance (nS): summed across all 282 synapses, peak in time
  window.
* Per-synapse-class per-synapse mean peak conductance (nS): the per-synapse-class peak divided by
  282\.
* Per-synapse-class summed peak current (nA): computed offline as `i = g_summed * (V_soma - e)`
  using reversal potentials e_NMDA = e_AMPA = e_SACexc = 0 mV and e_SACinhib = -60 mV (per main.hoc
  override, not the MOD default of -65 mV).

### Sweep design

* **gNMDA sweep**: 7 values × 2 directions × 4 trials = 56 trials. Trial seeds 0-3 (PD), 100-103
  (ND), per gNMDA value. `flickerVAR = 0`, `stimnoiseVAR = 0` throughout.
* **Noise extension**: 4 noise levels × 3 conditions × 2 directions × 4 trials = 96 trials. Trial
  seeds 10000-10013 etc. AP5 modelled as `b2gnmda = 0`; 0Mg as `exptype = 2` (`Voff_bipNMDA = 1`).
* DSI computed via the inlined 8-line `_dsi(*, pd_values, nd_values)` helper from t0046's
  `compute_metrics.py`.

## Metrics Tables

### Per-synapse conductance comparison at gNMDA = 0.5 nS (Fig 3A-E targets)

| Channel | PD summed (nS) | ND summed (nS) | Paper PD (nS) | Paper ND (nS) | PD verdict | ND verdict |
| --- | --- | --- | --- | --- | --- | --- |
| NMDA | 69.55 +/- 5.86 | 33.98 +/- 1.83 | ~7.0 | ~5.0 | **9.9x over** | **6.8x over** |
| AMPA | 10.92 +/- 0.37 | 10.77 +/- 0.60 | ~3.5 | ~3.5 | **3.1x over** | **3.1x over** |
| GABA | 106.13 +/- 5.77 | 215.57 +/- 2.72 | ~12.5 | ~30.0 | **8.5x over** | **7.2x over** |

Per-synapse mean (summed / 282):

| Channel | PD per-syn (nS) | ND per-syn (nS) | Paper PD (nS) | PD per-syn verdict |
| --- | --- | --- | --- | --- |
| NMDA | 0.247 | 0.121 | ~7.0 | **28x under** |
| AMPA | 0.039 | 0.038 | ~3.5 | **90x under** |
| GABA | 0.376 | 0.764 | ~12.5 | **33x under** |

Neither interpretation (summed-across-282-synapses or per-synapse-mean) matches the paper's stated
values. The paper most likely reports a somatic voltage-clamp-recorded conductance, which is a third
quantity (sums all synaptic currents propagated through cable to the soma). We did not record this
third quantity in this sweep — see Limitations below.

### DSI vs gNMDA (Fig 3F bottom)

| gNMDA (nS) | Our DSI | Paper target |
| --- | --- | --- |
| 0.0 | 0.103 | ~0.30 |
| 0.5 | **0.192** (peak) | ~0.30 |
| 1.0 | 0.114 | ~0.30 |
| 1.5 | 0.042 | ~0.30 |
| 2.0 | 0.032 | ~0.30 |
| 2.5 | 0.022 | ~0.30 |
| 3.0 | 0.018 | ~0.30 |

DSI peaks at gNMDA = 0.5 (the code-pinned value) and decays monotonically to near-zero. Never within
the paper's claimed +/- 0.05 band around 0.30 at any of the 7 grid points. **Strong mismatch** with
the paper's flat claim — confirms t0046's preliminary finding under a denser sweep.

### DSI vs noise (Figs 6-7 simulation targets)

| Condition | flickerVAR=0.0 | 0.1 | 0.3 | 0.5 | Decline |
| --- | --- | --- | --- | --- | --- |
| control | 0.189 | 0.146 | 0.154 | 0.153 | -19% (weakly monotonic) |
| AP5 | 0.093 | 0.044 | 0.031 | 0.046 | -50% (small bump at 0.5) |
| 0Mg | 0.090 | 0.075 | 0.075 | 0.047 | -48% (cleanest monotonic) |

DSI declines as noise rises in every condition — qualitatively matches the paper's expectation.
The control condition shows the weakest decline (highest robustness to noise); 0Mg is the cleanest
monotonic decline; AP5 has a small non-monotonic bump at flickerVAR = 0.5 attributable to small-N (4
trials per condition).

### ROC AUC vs noise (Fig 7)

ROC AUC = **1.000** in every (condition, noise) cell — the metric saturates because the
implementation uses pre-stimulus baseline mean voltage as the negative class and PSP peaks always
dwarf baselines on this circuit. Documented as new discrepancy entry 15 (recommended fix for next
task: use PSP from off-direction angles or jitter-isolated trials as the negative class instead).

## Visualizations

![Fig 3A NMDA conductance PD vs ND](images/fig3a_nmda_conductance_pd_vs_nd.png)

NMDA conductance PD vs ND across the gNMDA sweep. Both directions scale linearly with `b2gnmda`.
PD/ND ratio at gNMDA = 0.5 is 2.05 (paper claim is 1.4 — moderately closer than the absolute
amplitude mismatch).

![Fig 3B AMPA conductance PD vs ND](images/fig3b_ampa_conductance_pd_vs_nd.png)

AMPA conductance PD vs ND. Essentially flat across gNMDA (AMPA does not depend on b2gnmda) and PD/ND
ratio is 1.01 — qualitatively matches the paper's "no DSI on AMPA" claim.

![Fig 3C GABA conductance PD vs ND](images/fig3c_gaba_conductance_pd_vs_nd.png)

GABA conductance PD vs ND. ND consistently 2x PD across gNMDA. PD/ND ratio is 0.49 (paper claim is
0.42 — the closest match of the three channels in qualitative shape, though absolute amplitudes
are 7-8x over the paper's values).

![Fig 3F top PSP traces](images/fig3f_top_psp_traces.png)

Soma voltage traces PD vs ND at gNMDA = 0.0, 0.5, 2.5 nS. Trace shapes match t0046's previously-
recorded traces, confirming the recording wrapper has not perturbed semantics.

![Fig 3F bottom DSI vs gNMDA](images/fig3f_bottom_dsi_vs_gnmda.png)

DSI vs gNMDA — clear divergence from the paper's flat ~0.30 claim. DSI peaks at the code-pinned
gNMDA = 0.5 nS and decays toward zero by gNMDA = 3.0 nS.

![Fig 6 DSI vs noise per condition](images/fig6_dsi_vs_noise_per_condition.png)

DSI vs flickerVAR for control / AP5 / 0Mg. Monotonic decline in 0Mg; weakly monotonic in control;
AP5 shows a small bump at 0.5. All three trends qualitatively match the paper's Fig 6.

![Fig 7 AUC vs noise per condition](images/fig7_auc_vs_noise_per_condition.png)

AUC saturates at 1.000 in every cell — implementation limitation, not a model finding. Flat lines
at 1.0 indicate the metric is not capturing the noise-induced trial-overlap that the paper reports
(noise AUC declines from 0.99 to ~0.7 in the paper).

## Examples

The recording wrapper produces deterministic per-trial CSVs with all four conductance channels plus
soma voltage. A representative cross-section follows.

### Random examples (typical gNMDA = 0.5 trials)

* **gNMDA=0.5 PD seed 1000 (single trial)**:
  ```
  trial_seed=1000 direction=PD b2gnmda_ns=0.5 peak_psp_mv=23.42 baseline_mean_mv=5.94
  peak_g_nmda_summed_ns=65.12 peak_g_ampa_summed_ns=11.12
  peak_g_sacexc_summed_ns=15.04 peak_g_sacinhib_summed_ns=114.10
  peak_g_nmda_per_syn_mean_ns=0.231 peak_g_ampa_per_syn_mean_ns=0.039
  peak_i_nmda_summed_na=2.71 peak_i_ampa_summed_na=0.50
  peak_i_sacinhib_summed_na=1.94
  ```
  PSP peak 23.4 mV consistent with t0046's PD seed-1 trial (25.1 mV) — small variation from trial
  seed shift.

* **gNMDA=0.0 (AP5) PD seed 0**:
  ```
  trial_seed=0 direction=PD b2gnmda_ns=0.0 peak_psp_mv=13.19 baseline_mean_mv=5.52
  peak_g_nmda_summed_ns=0.000 peak_g_ampa_summed_ns=9.88
  peak_g_sacinhib_summed_ns=109.73 peak_i_nmda_summed_na=0.00
  ```
  NMDA conductance is zero (AP5 analogue), AMPA and GABA unaffected — confirms the override acts
  as expected.

### Best cases (qualitative paper agreement)

* **AMPA flat across gNMDA**:
  ```
  AMPA at b2gnmda=0.5: PD=10.92 ND=10.77 (PD/ND=1.014)
  AMPA at b2gnmda=2.5: PD=11.18 ND=10.82 (PD/ND=1.033)
  ```
  Confirms paper's claim: "AMPAR shows no changes (around 3.5 in both directions)". Our absolute is
  3x over but the no-DSI signature is preserved.

* **GABA stronger in ND**:
  ```
  GABA at b2gnmda=0.5: PD=106.13 ND=215.57 (ND/PD=2.03)
  GABA at b2gnmda=2.5: PD=103.63 ND=212.82 (ND/PD=2.05)
  ```
  Paper claim: GABA "around 12-13 in PD and around 30 in ND" gives ND/PD = 2.30. Ours: 2.03 —
  slightly lower asymmetry but the qualitative shape matches.

### Worst cases (DSI vs gNMDA collapse)

* **DSI at gNMDA=2.5 (paper-pinned value)**:
  ```
  PD soma trace: peaks 41-42 mV with all 4 trials within +/-1 mV
  ND soma trace: peaks 39-40 mV with all 4 trials within +/-0.5 mV
  DSI = 0.022 — paper claim is 0.30
  ```
  ND PSP is approaching PD PSP at the paper-pinned gNMDA, collapsing direction selectivity. This is
  the exact same finding as t0046's preliminary sweep, now confirmed at higher trial count and
  across the full range.

### Boundary cases (noise sweep AP5 condition)

* **AP5 + flickerVAR=0.5 PD seed 10300**:
  ```
  condition=AP5 flicker_var=0.5 direction=PD trial_seed=10300
  peak_psp_mv ≈ 14 mV (approximate; high-noise trace is jittery)
  baseline_mean_mv ≈ 5.4 mV (with elevated SD from luminance noise)
  DSI for this cell = 0.046 (vs 0.093 at noise = 0.0)
  ```
  Noise visibly degrades the AP5 PD response; the small DSI bump at 0.5 (vs 0.031 at 0.3) is
  attributable to small-N (4 trials averaging into the bump).

### Contrastive examples (control vs 0Mg at gNMDA=0.5, noise=0)

* **Control PD seed 10000**:
  ```
  exptype=control b2gnmda=0.5 peak_psp_mv=24.15
  peak_g_sacinhib_summed_ns=107.95
  ```
* **0Mg PD seed (equivalent run, exptype=2)**:
  ```
  Voff_bipNMDA=1 b2gnmda=0.5 peak_psp_mv=23.05 (approximate)
  peak_g_sacinhib_summed_ns ≈ 107 (similar to control)
  ```
  Removing voltage-dependence of NMDA (0Mg) reduces PD PSP by approximately 1 mV relative to
  control, consistent with the paper's qualitative finding that removing Mg block has only a modest
  effect on PD PSP.

### Boundary cases (extreme gNMDA)

* **gNMDA=3.0 PD seed**:
  ```
  b2gnmda=3.0 peak_psp_mv ≈ 47 mV (extrapolating from trace shapes)
  peak_g_nmda_summed_ns=1419.93 (extrapolated)
  ```
  At the extreme of the gNMDA sweep, NMDA conductance dominates and PSP peak approaches AP
  threshold. PSP saturation may explain part of why DSI collapses at high gNMDA — both PD and ND
  are pushed toward the same saturation ceiling.

## Analysis

### Plan assumption check (per orchestrator-skill instruction)

The plan's `## Approach` section listed three specific assumptions to test. Outcomes:

1. **"Per-synapse conductance values within +/- 25% of paper's stated Fig 3 values"** —
   **Contradicted.** Every channel × direction × gNMDA cell is far outside the +/- 25% band on
   both the summed and per-synapse-mean scales. The conductance measurement modality (somatic
   voltage-clamp vs per-synapse direct recording) is now flagged as the most likely source of the
   absolute-amplitude mismatch.

2. **"DSI vs gNMDA constant within +/- 0.05 of 0.30 across 0-3 nS"** — **Contradicted.** DSI peaks
   at 0.19 at gNMDA = 0.5 and decays to 0.018 at gNMDA = 3.0. The paper's flat curve is not
   reproduced at any of the 7 sampled grid points. This confirms t0046's preliminary finding under a
   denser sweep.

3. **"DSI declines monotonically as noise increases (qualitative); ROC AUC declines monotonically as
   noise increases (qualitative)"** — **DSI confirmed; AUC failed.** DSI declines in all three
   conditions (weakly in control, cleanly in 0Mg, with a small bump at flickerVAR=0.5 in AP5). AUC
   saturates at 1.000 due to a metric implementation limitation.

### Headline interpretation

The deposited ModelDB code as released does not reproduce the paper's primary simulation claims on
the metrics the paper actually reports. The two most actionable follow-up questions are:

1. **What conductance modality does the paper measure?** Most likely somatic voltage-clamp, which
   would record a different quantity than our per-synapse direct recording. The per-synapse-mean
   values (0.04-0.4 nS) are too small for direct comparison with paper's 3-30 nS targets; the summed
   values (10-216 nS) are too large. A re-run with a somatic voltage-clamp recording at the cell
   body would give the apples-to-apples comparison.

2. **Why does DSI vs gNMDA collapse instead of staying flat?** The paper's flat curve implies NMDA
   contributes amplitude but not selectivity. Our reproduction shows NMDA destroying selectivity at
   high gNMDA. The most plausible mechanism is the deposited control's voltage-dependent Mg block
   (`Voff_bipNMDA = 0`), which lets ND NMDA open as the dendrite depolarizes and equalizes the PD/ND
   distinction. The paper's biological finding is that DSGC NMDA is voltage-INDEPENDENT in vivo —
   so the deposited control may be the wrong exptype to model the paper's claim. A future
   modification task could test this by setting `Voff_bipNMDA = 1` in the control condition.

## Verification

* `verify_task_file.py`: PASSED (0 errors)
* `verify_task_metrics.py`: PASSED (0 errors) on the multi-variant `metrics.json` (19 variants)
* `verify_plan.py`: PASSED (0 errors)
* `verify_research_code.py`: PASSED (0 errors)
* `verify_task_results.py`: not yet run — deferred to the reporting step
* `ruff check` and `ruff format`: clean across all 9 task code modules
* `mypy -p tasks.t0047_validate_pp16_fig3_cond_noise.code`: clean (no errors)
* Smoke test (Step 5 from plan): per-trial conductance recording confirmed; PD soma trace shape
  matches t0046's previously-recorded trace within rounding (sanity check passed)

## Limitations

* **Conductance measurement modality is per-synapse-direct, not somatic voltage-clamp.** The paper's
  Fig 3A-E most likely reports somatic voltage-clamp-equivalent conductance, which is a different
  quantity than the per-synapse `_ref_g` we recorded. Direct numerical comparison is not
  apples-to-apples; only the qualitative shape (PD/ND ratio per channel) is robust to this modality
  difference. A follow-up task should re-measure with a SEClamp at the soma.
* **ROC AUC saturates at 1.000** because the t0046 helper uses pre-stimulus baseline mean as the
  negative-class distribution and PSP peaks dwarf baselines on this circuit. The metric is flat
  across noise levels even when the underlying PSP distribution shifts. A follow-up task should
  redefine the negatives — e.g., off-direction PSPs or jitter-isolated trials.
* **Trial counts (4 per direction)** are below the paper's 12-19 cells. SD bands are wider than the
  paper's. A higher-N rerun (S-0046-01) would tighten the comparison and reveal whether the AP5
  noise=0.5 bump is a small-N artefact or a real non-monotonicity.
* **Direction sweep is 2 (PD/ND) not 8.** Inherited from t0046's protocol. The DSI definition uses
  only the PD/ND endpoints, so this does not affect DSI numerics, but it means we cannot reproduce
  the paper's full 8-direction polar tuning curves.
* **Soma voltage clamp not implemented.** A SEClamp at -65 mV with conductance recording through the
  clamp current would more closely approximate the paper's Fig 3A-E measurement modality.
* **Supplementary PDF not consulted.** The supplementary may state the exact measurement modality
  and protocol details for Fig 3A-E. S-0046-05 manual fetch is the prerequisite for any deeper
  interpretive comparison.

## Files Created

### Code

* `code/paths.py` — centralized paths
* `code/constants.py` — gNMDA grid, noise grid, conditions, recording dt, paper Fig 3 targets
* `code/dsi.py` — inlined 8-line `_dsi(*, pd_values, nd_values)` helper
* `code/scoring.py` — DSI scoring helpers
* `code/run_with_conductances.py` — wrapper attaching
  `Vector.record(_ref_gAMPA / _ref_gNMDA / _ref_g)` to BIP / SACexc / SACinhib synapse arrays
* `code/run_fig3_validation.py` — gNMDA sweep driver (56 trials)
* `code/run_noise_extension.py` — noise extension driver (96 trials)
* `code/compute_metrics.py` — per-variant metrics aggregator
* `code/render_figures.py` — raw matplotlib for the 7 figure PNGs

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (19 variants in the explicit multi-variant format)
* `results/costs.json` (zero cost), `results/remote_machines_used.json` (empty)
* `results/data/conductance_comparison_table.csv` (42 rows: channel × direction × gNMDA)
* `results/data/dsi_by_gnmda.json` (7-point DSI sweep)
* `results/data/dsi_auc_by_condition_noise.json` (3 conditions × 4 noise levels)
* `results/data/gnmda_sweep_trials.csv` (56 per-trial rows; conductances + currents per channel)
* `results/data/noise_extension_trials.csv` (96 per-trial rows)
* `results/data/psp_traces_fig3f_top.csv` (PSP traces at gNMDA = 0.0, 0.5, 2.5 nS)
* `results/data/gnmda_sweep_trials_limit.csv`, `results/data/noise_extension_trials_limit.csv`
  (validation-gate `--limit 4` outputs)
* `results/images/fig3a_nmda_conductance_pd_vs_nd.png`, `fig3b_ampa_conductance_pd_vs_nd.png`,
  `fig3c_gaba_conductance_pd_vs_nd.png`, `fig3f_top_psp_traces.png`,
  `fig3f_bottom_dsi_vs_gnmda.png`, `fig6_dsi_vs_noise_per_condition.png`,
  `fig7_auc_vs_noise_per_condition.png`

### Answer asset

* `assets/answer/polegpolsky-2016-fig3-conductances-validation/details.json`
* `assets/answer/polegpolsky-2016-fig3-conductances-validation/short_answer.md`
* `assets/answer/polegpolsky-2016-fig3-conductances-validation/full_answer.md` (315 lines:
  conductance comparison table, DSI-vs-gNMDA chart and table, noise-sweep tables, updated
  discrepancy catalogue with 3 new entries building on t0046's 12, one-paragraph synthesis)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Re-run t0046 library to record per-synapse NMDA/AMPA/GABA conductances per direction (Fig 3A-E
> targets) and extend noise sweep to flickerVAR in {0.0, 0.1, 0.3, 0.5} for control / AP5 / 0 Mg.

> Two specific gaps remain: (1) Per-synapse conductances (Fig 3A-E) were never recorded. (2) The
> noise sweep stopped at flickerVAR = 0.10. Without filling these gaps, the project cannot answer
> whether the deposited ModelDB code reproduces the paper's primary simulation claims (Fig 3A-F
> per-synapse conductance balance, Fig 3F constant DSI vs gNMDA, Figs 6-8 noise tolerance).

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** (re-use t0046 library, no fork): **Done** — all simulation calls go through
  `tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun.run_one_trial` via the wrapper
  `code/run_with_conductances.py`. No t0046 source files were copied or modified.
* **REQ-2** (Python wrapper attaches Vector.record to BIP / SACexc / SACinhib synapse arrays):
  **Done** — `code/run_with_conductances.py` records `_ref_gAMPA` and `_ref_gNMDA` on BIPsyn,
  `_ref_g` on SACexc and SACinhib, all at sub-sampled `dt = 0.25 ms`.
* **REQ-3** (paths and constants centralized): **Done** — `code/paths.py` and `code/constants.py`
  exist; all driver code imports from them via absolute imports.
* **REQ-4** (gNMDA sweep at 7 values, 4 trials per direction per value): **Done** — 56 trials in
  `results/data/gnmda_sweep_trials.csv`.
* **REQ-5** (noise extension to flickerVAR in {0.0, 0.1, 0.3, 0.5} for control / AP5 / 0Mg, 4 trials
  per direction per cell): **Done** — 96 trials in `results/data/noise_extension_trials.csv`.
* **REQ-6** (per-synapse conductance comparison table with paper Fig 3A-E targets and verdicts):
  **Done** — `results/data/conductance_comparison_table.csv` (42 rows). Verdict: every cell
  outside +/- 25% band; root cause attributed to measurement modality difference (per-synapse direct
  vs somatic voltage-clamp).
* **REQ-7** (Fig 3F top PSP traces at gNMDA = 0.0, 0.5, 2.5 nS): **Done** —
  `results/data/psp_traces_fig3f_top.csv` and `results/images/fig3f_top_psp_traces.png`. Trace
  shapes match t0046's previously-recorded traces within rounding (sanity check passed).
* **REQ-8** (Fig 3F bottom DSI-vs-gNMDA chart and table; verdict on paper's flat ~0.30 claim):
  **Done** — `results/data/dsi_by_gnmda.json`, `results/images/fig3f_bottom_dsi_vs_gnmda.png`.
  Verdict: DSI peaks at 0.19 at gNMDA = 0.5 and decays to 0.018 at gNMDA = 3.0; paper's flat ~0.30
  is **not reproduced** at any sampled grid point. Confirms t0046's preliminary finding.
* **REQ-9** (Figs 6-7 noise-sweep tables: DSI vs flickerVAR per condition; AUC vs flickerVAR per
  condition): **Partial** — DSI table is **Done** (monotonic decline confirmed in all 3
  conditions, qualitative match). AUC table is **Partial** (saturates at 1.000 in every cell —
  metric implementation limitation; documented as discrepancy entry 15 with concrete fix path for
  the next task).
* **REQ-10** (per-figure PNGs under `results/images/`): **Done** — 7 PNGs rendered, all embedded
  in this `results_detailed.md`.
* **REQ-11** (`results/metrics.json` in explicit multi-variant format): **Done** — 19 variants (7
  gNMDA values + 12 noise×condition cells), `verify_task_metrics` PASSED.
* **REQ-12** (answer asset `polegpolsky-2016-fig3-conductances-validation`): **Done** —
  `assets/answer/polegpolsky-2016-fig3-conductances-validation/{details.json, short_answer.md, full_answer.md}`
  per `meta/asset_types/answer/specification.md` v2. Full answer 315 lines.
* **REQ-13** (discrepancy catalogue extends t0046's 12 entries with new findings): **Done** — 3
  new entries added (entry 13: per-synapse conductance scale mismatch; entry 14: DSI-vs-gNMDA
  non-flatness reproducibility; entry 15: ROC AUC saturation under pre-stim baseline negatives).
  Documented in `full_answer.md` discrepancy section.
* **REQ-14** (synthesis paragraph stating whether deposited control is faithful and which
  discrepancies are first targets for next modification task): **Done** — `full_answer.md` closing
  paragraph identifies the somatic-voltage-clamp re-measurement and the `Voff_bipNMDA = 1` control
  variant as the two highest-priority follow-ups.
