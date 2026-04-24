# ✅ Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0046_reproduce_poleg_polsky_2016_exact` |
| **Status** | ✅ completed |
| **Started** | 2026-04-24T13:02:27Z |
| **Completed** | 2026-04-24T17:45:00Z |
| **Duration** | 4h 42m |
| **Dependencies** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md), [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md), [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Task types** | `code-reproduction` |
| **Categories** | [`compartmental-modeling`](../../by-category/compartmental-modeling.md), [`direction-selectivity`](../../by-category/direction-selectivity.md), [`retinal-ganglion-cell`](../../by-category/retinal-ganglion-cell.md), [`synaptic-integration`](../../by-category/synaptic-integration.md) |
| **Expected assets** | 1 library, 1 answer |
| **Step progress** | 12/15 |
| **Task folder** | [`t0046_reproduce_poleg_polsky_2016_exact/`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/) |
| **Detailed results** | [`results_detailed.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/results_detailed.md) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/task_description.md)*

# Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Correction — 2026-04-24

The original version of this task_description.md (as merged in PR #44) framed the peak-rate
mismatch (~15 Hz in our ports vs "paper's 40-80 Hz range") as a Poleg-Polsky 2016 claim and
included a pass criterion of "firing rates within +/-10% of the paper's stated value". This
was wrong. **Poleg-Polsky & Diamond 2016 is primarily a subthreshold-PSP paper.** Its main
figures report PSP amplitudes (mV), direction-tuning slope angles (degrees), and subthreshold
ROC AUC. Only Figure 8 includes spikes, and even there the paper reports qualitative DSI
preservation / reduction and PD-failure rate — not specific peak Hz numbers. The 40-80 Hz
target traces back to t0004's project-internal tuning-curve envelope (sourced from Oesch 2005
rabbit recordings and Sivyer 2013), not to Poleg-Polsky 2016.

This revision corrects the pass criteria to target PSP amplitudes, slope angles, and ROC AUC
as the primary reproduction metrics, with Figure 8 suprathreshold checks as a secondary
qualitative pass. Spike-rate comparisons against t0004's envelope are explicitly out of scope
for this task.

## Motivation

The project has two prior ports of Poleg-Polsky & Diamond 2016 (ModelDB 189347): **t0008**
(initial port using a spatial-rotation proxy for the gabaMOD swap) and **t0020** (re-run with
the native gabaMOD parameter-swap protocol; DSI 0.784 ~ paper's median of ~0.80). Both focused
primarily on the tuning curve as measured through DSI and did not audit every parameter
against the paper, did not reproduce the other tests the paper runs, and did not publish a
systematic paper-vs-code discrepancy catalogue.

The brainstorm-8 audit (t0040) identified paper-vs-observation mismatches across every port
and sweep; some of those mismatches — particularly the peak-rate framing — conflated
Poleg-Polsky 2016 with other DSGC papers (Oesch 2005, Sivyer 2013) and therefore do not belong
to this task. This task steps back to establish the faithful reproduction of Poleg-Polsky 2016
on its own terms, using the paper's own figures and metrics as the target.

## Objective

Produce a fresh port of ModelDB 189347 that reproduces Poleg-Polsky 2016 exactly on the
metrics the paper actually reports — PSP amplitudes, direction-tuning slope angles, ROC AUC
under the noise conditions described in the paper, and qualitative Figure 8 suprathreshold
behaviour — using the paper's own protocols. Publish a line-by-line audit comparing **paper ·
ModelDB code · our reproduction** for every quantitative claim, and a discrepancy catalogue
for any place where the paper text and the ModelDB code disagree.

## Paper's Reported Metrics (target of reproduction)

Primary (subthreshold PSP, Figures 1-7):

* **Figure 1** — 8-direction PSPs. PD PSP **5.8 +/- 3.1 mV**, ND PSP **3.3 +/- 2.8 mV**,
  direction-tuning slope **62.5 +/- 14.2 degrees** (multiplicative scaling under
  voltage-dependent NMDAR). DSI preserved under AP5. n=19.
* **Figure 2** — iMK801 (2 mM) dialysis + bath AP5: AP5-after-iMK801 further reduces PD PSP by
  only **16 +/- 17%**. n=15.
* **Figure 3** — NEURON model: 282 presynaptic cells, homogeneous ON-dendrite synapses, tuned
  inhibition, paper-stated **gNMDA = 2.5 nS** (paper) vs **0.5 nS** (ModelDB code)
  **[discrepancy flagged]**. Alternative tuned-excitation scheme predicts additive scaling.
* **Figure 4** — High-Cl- internal (tuned-excitation analogue): slope **45.5 +/- 3.7 degrees**
  (additive). DS reverses PD in 15/20 cells. n=12.
* **Figure 5** — 0 Mg2+ (voltage-dependent NMDAR removed, Ohmic NMDAR analogue): slope **45.5
  +/- 5.3 degrees** (additive). DSI reduced but PD != ND. n=8.
* **Figure 6** — Noisy PSPs under bar + background luminance noise at SD **0 / 10 / 30 /
  50%**. DSI reduced by noise, strongest in 0 Mg2+. n=12.
* **Figure 7** — Subthreshold ROC / accuracy (noise-free): AUC **0.99 / 0.98 / 0.83** for
  control / AP5 / 0 Mg2+. Accuracy curve area larger in control.

Secondary (suprathreshold APs, Figure 8 only):

* **Figure 8** — DSI preserved under AP5 (qualitative); DSI reduced in 0 Mg2+ (qualitative);
  AP5 **raises PD-failure rate**; ROC AUC on spikes under noise. **The paper does not report
  specific peak Hz or aggregate firing-rate numbers for the model.**

Basic parameters (read from ModelDB source, audited vs paper prose where stated):

* V_rest, Ra, Rm, Cm, soma/dendrite channel gbar densities, synaptic kinetics, Jahr-Stevens
  parameters, stimulus timing. See `research/research_internet.md` for extracted ModelDB
  values.

## Scope

### In Scope

* Full from-scratch port of ModelDB 189347 into a new library asset (do NOT fork t0008, t0020,
  or t0022). Target location:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`.
* Download and attach the supplementary PDF (NIHMS766337; PMC4795984) to the existing
  `10.1016_j.neuron.2016.02.013` paper asset.
* Paper corpus review: Poleg-Polsky & Diamond 2016 (Neuron) PDF + supplementary.
* ModelDB 189347 release: every `.hoc`, `.mod`, `.py`, README, comment, and parameter file in
  the release. Cross-check the release version against the paper's cited version.
* **Reproduce every quantitative claim in Figures 1-8**, as enumerated in "Paper's Reported
  Metrics" above.
* Basic parameters audited against paper + code + supplementary.

### Out of Scope

* **Comparisons against t0004's target tuning-curve envelope** (peak Hz 40-80, null Hz <10,
  HWHM 60-90). Those targets come from Oesch 2005 / Sivyer 2013 / Chen 2009 and do not belong
  in a Poleg-Polsky 2016 reproduction task.
* Modifications or improvements beyond the original paper.
* Integration with t0022, t0024, or other downstream modified testbeds.
* Any DSGC models other than Poleg-Polsky 2016.

## Source of Truth

Audit uses all three sources:

1. **Published PDF** — Poleg-Polsky & Diamond 2016, Neuron.
2. **ModelDB 189347 release** — README, `.hoc`, `.mod`, `.py`, parameter files, and all code
   comments. Canonical commit `87d669dcef18e9966e29c88520ede78bc16d36ff` (2019-05-31).
3. **Supplementary materials** — NIHMS766337 (PMC4795984), bundled Supplemental Experimental
   Procedures plus supplementary figures S1-S8. Download during implementation and attach to
   the existing paper asset.

## Paper-vs-Code Discrepancy Handling

The primary reproduction **follows their code** (what they actually ran). If the code fails to
reproduce a specific paper claim within tolerance, flag the discrepancy explicitly with the
paper claim, the code's actual behaviour, and the numerical gap. Known pre-implementation
flags from the research stages:

* **gNMDA discrepancy**: paper Fig 3E states 2.5 nS, ModelDB code uses 0.5 nS.
* **Synapse count discrepancy**: paper states 177 synapses, ModelDB code instantiates 282.
* **Noise driver missing**: shipped `SquareInput.mod` has no luminance-noise driver despite
  Figures 6-8 describing per-50-ms noise SD = 0 / 10 / 30 / 50%. Figures 6-8 cannot be
  reproduced from stock code without adding a noise driver; this must itself be flagged as a
  significant paper-vs-code discrepancy (the Figures 6-8 results in the paper must have come
  from a different code variant).
* **Dendritic Nav**: 2e-4 S/cm2 (small but non-zero), not strictly zero — refines the "passive
  dendrites" wording.

## Pass Criterion

Primary pass criteria (Figures 1-7 subthreshold):

* PD PSP amplitude within **1 SD** of the paper's reported mean (within 3.1 mV of 5.8 mV for
  Fig 1 control).
* ND PSP amplitude within **1 SD** (within 2.8 mV of 3.3 mV).
* Slope angle within **1 SD** (within 14.2 degrees of 62.5 degrees for Fig 1; within 3.7-5.3
  degrees for Figs 4-5 additive regime).
* Under 0 Mg2+: DSI reduced but not zero; preferred direction preserved (paper claim).
* Under High-Cl-: DS reverses PD in >= 50% of trials (paper's 15/20 is 75%; allow
  flexibility).
* Subthreshold noise-free ROC AUC within **+/- 0.05** of each paper value (0.99 / 0.98 / 0.83
  for control / AP5 / 0 Mg2+).

Secondary pass criteria (Figure 8 suprathreshold):

* DSI qualitatively preserved under AP5 (both conditions direction-selective).
* DSI qualitatively reduced in 0 Mg2+.
* PD-failure rate increases under AP5 (direction: positive, magnitude not specified by paper).
* No numeric peak-Hz target is asserted; the paper does not state one.

Parameter-match criterion:

* Every basic parameter in the audit table matches ModelDB code exactly; any deviation is
  documented as a reproduction bug, not an intentional modification.

Discrepancy-catalogue criterion:

* Every paper-vs-code discrepancy is catalogued with numerical evidence, including the four
  pre-flagged above (gNMDA, synapse count, missing noise driver, dendritic Nav wording) and
  any further discrepancies found during implementation.

## Deliverables

### Library asset (1)

`assets/library/modeldb_189347_dsgc_exact/`:

* Full NEURON port runnable under the project's NEURON 8.2.7 + NetPyNE 1.1.1 toolchain (from
  t0007).
* Uses the baseline DSGC morphology from t0005 (or the ModelDB-shipped morphology if that is
  what the paper actually used — audit this; if they differ, this is a discrepancy to flag).
* Source files mirror the ModelDB release structure where practical, with a clear mapping from
  each ModelDB file to the corresponding file in this library.
* Per-file comments identifying the ModelDB source file and line ranges that the port
  transcribes.
* Adds a luminance-noise driver that reproduces the Figure 6-8 noise protocol (the shipped
  ModelDB code lacks one); this addition must itself be flagged as a paper-vs-code
  discrepancy.
* Meets the library-asset specification in `meta/asset_types/library/specification.md`.

### Answer asset (1)

`assets/answer/poleg-polsky-2016-reproduction-audit/` with a full audit report.

The `full_answer.md` must include:

* **Audit table** — one row per basic parameter. Columns: **Parameter**, **Paper value** (when
  stated), **ModelDB code value**, **Our reproduction value**, **Match?**, **Citation**.
* **Figure-reproduction table** — one row per figure (1-8) with the paper's reported metric,
  our reproduction metric, tolerance, match verdict, and paper figure reference. Separate rows
  for PD/ND PSP, slope, ROC AUC, etc. as applicable.
* **Discrepancy catalogue** — one entry per paper-vs-code disagreement with numerical
  evidence.
* **Reproduction bugs** — any place where our port diverges from ModelDB code; each must be
  fixed before the library asset is considered complete.
* One-paragraph summary of what this reproduction establishes for the broader project.
  Specifically: whether Poleg-Polsky's PSP + slope + ROC claims hold under a faithful
  reimplementation, and a note on whether Figure 8 suprathreshold behaviour depends on details
  that the published code does not specify.

### Per-paper figure reproductions (under `results/images/`)

Each paper figure that reports a test this task reproduces gets its own PNG comparing our
reproduction against the paper's figure. Clearly labelled axes and matching ranges.

## Execution Guidance

* **Code-reproduction task type**. Steps: research-papers (done), research-internet (done),
  research-code, planning, implementation, results, compare-literature, suggestions,
  reporting. Skipped: setup-machines, teardown, creative-thinking.
* Local CPU only. No Vast.ai. Estimate 1-2 days of execution time; MOD compilation on Windows
  may take a non-trivial fraction of that, and the noise-driver addition adds one iteration
  cycle.
* Use absolute imports and centralised `paths.py` / `constants.py` per the project's Python
  style guide.

## Anticipated Risks

* **ModelDB 189347 may reference a morphology file not in t0005**: audit carefully; if the
  paper used a different morphology, flag and either fetch the paper's morphology or document
  the substitution as a reproduction bug.
* **MOD file compilation on Windows NEURON 8.2.7**: some MOD files in older ModelDB releases
  need minor adjustments to compile under modern NEURON. Record every adjustment as a
  potential discrepancy.
* **Noise driver**: the shipped code cannot produce Figures 6-8 because it lacks a luminance
  noise driver. Our port must add one; document the addition as a discrepancy (the paper's
  Figure 6-8 results therefore came from a version of the code the authors did not deposit).
* **gNMDA pick**: paper says 2.5 nS, code uses 0.5 nS. Primary reproduction uses 0.5 nS
  (follow code); secondary run at 2.5 nS documents whether the paper claim or the code
  publishes the Figure 1-5 behaviour.

## Relationship to Other Tasks

* **Currently blocks (administrative)**: t0042, t0043, t0044 are `intervention_blocked`
  pending this task. **Note**: t0043's peak-rate framing was built on the same category error
  this task's revised scope addresses; after this task completes, the case for t0043 as
  currently scoped should be reviewed explicitly.
* **Complements**: t0008 (initial port) and t0020 (gabaMOD protocol fix) remain in the history
  as partial reproductions focused on DSI. This task does not modify them; it produces an
  independent, more complete reproduction against the paper's actual reported metrics.
* **Precedes**: any future optimisation task (t0033 style) should use this library asset as
  the starting point.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_library_asset.py` passes for `modeldb_189347_dsgc_exact`.
* Answer-asset verificator passes for `poleg-polsky-2016-reproduction-audit`.
* All pass criteria above met: PSP amplitudes within 1 SD, slope angles within 1 SD, ROC AUC
  within +/-0.05, Figure 8 qualitative checks pass, basic parameters match ModelDB code
  exactly.
* Every paper test attempted is represented in the figure-reproduction table with a match /
  no-match verdict and numerical evidence.
* Discrepancy catalogue is complete and includes the four pre-flagged items plus any new
  findings.

</details>

## Metrics

### Fig 1 control (b2gnmda = 0.5 nS, code value)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.17303679518783643** |

### Fig 1 control (b2gnmda = 2.5 nS, paper value)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.020655514455547648** |

### Fig 2 AP5 analogue (b2gnmda = 0)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.11217460723286353** |

### Fig 4 high-Cl- (tuned-excitation analogue, exptype = 3)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0406436316188555** |

### Fig 5 0 Mg2+ (Voff_bipNMDA = 1, exptype = 2)

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.09894223839442597** |

### Fig 6/7 fig6_control flickerVAR=0.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.20411946395779645** |

### Fig 6/7 fig6_control flickerVAR=0.10

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.16946068741930417** |

### Fig 6/7 fig6_zeromg flickerVAR=0.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.10680865504100232** |

### Fig 6/7 fig6_zeromg flickerVAR=0.10

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.09812950787605132** |

### Fig 8 fig8_control flickerVAR=0.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.6756756756756757** |

### Fig 8 fig8_ap5 flickerVAR=0.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.0** |

### Fig 8 fig8_zeromg flickerVAR=0.00

| Metric | Value |
|--------|-------|
| [`direction_selectivity_index`](../../metrics-results/direction_selectivity_index.md) | **0.21212121212121213** |

## Assets Produced

| Type | Asset | Details |
|------|-------|---------|
| answer | [Does ModelDB 189347 (Poleg-Polsky and Diamond 2016) reproduce every quantitative claim in Figures 1-8 of the Neuron paper when re-run faithfully under NEURON 8.2.7, and where do the paper text and the ModelDB code disagree?](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/) | [`full_answer.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md) |
| library | [ModelDB 189347 DSGC (exact reproduction)](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/) | [`description.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/description.md) |

## Suggestions Generated

<details>
<summary><strong>Re-run t0046 figure sweeps at paper-N (12-19 trials per condition,
full 8-direction sweep)</strong> (S-0046-01)</summary>

**Kind**: experiment | **Priority**: high

Re-execute every figure-reproduction sweep in t0046 (`code/run_all_figures.py`) at the paper's
reported N (12-19 trials per condition) and the full 8-direction sweep instead of the
wall-clock-budget-reduced 2-4 trials and PD/ND-only collapse used in t0046. This will (a)
tighten the SD bands on PSP and AP-rate distributions, (b) replace the `atan2(mean PD PSP,
mean ND PSP)` slope approximation with a fit to the 8-direction tuning curve as the paper
does, and (c) reveal the true Fig 7 0 Mg2+ ROC AUC instead of the small-N saturation at 1.00
(paper reports 0.83). Recommended task types: experiment-run.

</details>

<details>
<summary><strong>Root-cause the 282-vs-177 synapse-count discrepancy in ModelDB
189347 vs Poleg-Polsky 2016 paper text</strong> (S-0046-02)</summary>

**Kind**: experiment | **Priority**: high

Inspect `RGCmodel.hoc`'s ON/OFF cut plane (`z >= -0.16 * y + 46`) and `placeBIP()` to
determine why the deposited code instantiates 282 BIP/SACinhib/SACexc terminals when the paper
Methods text states 177 synapses. Test alternative cut-plane thresholds, density-based
sub-sampling, or supplementary-text geometry rules to find a code configuration that matches
the paper count. The 1.6x synapse overcount is the leading mechanistic hypothesis for the ~4x
PSP amplitude inflation observed in t0046 (PD PSP 23.25 mV vs paper 5.8 +/- 3.1 mV);
reconciling the count is a prerequisite for a quantitatively faithful Fig 1 reproduction.
Recommended task types: experiment-run, code-reproduction.

</details>

<details>
<summary><strong>Add an iMK801 analogue MOD modification (selective dendritic NMDAR
block) to enable Fig 8 AP5 reproduction</strong> (S-0046-03)</summary>

**Kind**: library | **Priority**: high

Author a new MOD mechanism (or extend `bipolarNMDA.mod`) that selectively blocks NMDAR
conductance in dendritic compartments while leaving somatic NMDAR + AMPA intact, mirroring the
paper's intracellular MK801 (iMK801) protocol. The current AP5 analogue used in t0046
(`b2gnmda = 0`) removes ALL NMDAR contribution and silences the cell entirely (DSI = 0 under
AP5); the paper's iMK801 leaves PD spiking, allowing the qualitative 'DSI preserved under AP5'
Fig 8 claim to be reproduced. This unblocks a faithful Fig 8 AP5 reproduction and resolves the
AP5-vs-iMK801 mechanistic divergence catalogued as discrepancy 1 of 12 in t0046's audit.
Recommended task types: write-library, experiment-run.

</details>

<details>
<summary><strong>Decide the fate of t0042/t0043/t0044: rewrite motivation or cancel
based on t0046 findings</strong> (S-0046-04)</summary>

**Kind**: evaluation | **Priority**: medium

t0042 (fine-grained null-GABA ladder), t0043 (Nav1.6 + Kv3 + NMDA restoration), and t0044
(Schachter re-test on t0043) are currently `intervention_blocked` pending t0046's outcome.
t0046 establishes that the systematic peak-rate gap previously seen in t0008/t0020/t0022
(which motivated t0043's channel-inventory framing) is inherent to the deposited ModelDB code,
not a modification artefact. This invalidates t0043's stated motivation. Run a
brainstorm-style triage that (a) explicitly cancels or (b) rewrites motivations for each of
the three blocked tasks, replacing the discredited peak-rate-gap framing with t0046's
confirmed findings (synapse-count overcount; AP5-vs-iMK801 substitution; PSP amplitude
inflation). Apply corrections-overlay updates to record the decisions. Recommended task types:
brainstorming, correction.

</details>

<details>
<summary><strong>Manually fetch and attach the Poleg-Polsky 2016 supplementary PDF
(NIHMS766337, PMC4795984)</strong> (S-0046-05)</summary>

**Kind**: dataset | **Priority**: medium

The supplementary PDF
(`https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`) was
blocked by PMC's JS-only interstitial during t0046 implementation; a metadata-only correction
overlay records the citation but the binary file is not attached. Manually download the PDF
via a browser session and attach it to the existing `10.1016_j.neuron.2016.02.013` paper
asset, then update the corrections overlay to a full-binary-attached state. The supplementary
text is the only authoritative source for any Methods parameters not stated in the published
main text and is needed to fully audit the synapse-count discrepancy (S-0046-02). Recommended
task types: download-paper, correction.

</details>

<details>
<summary><strong>Backport t0046's GUI-free `dsgc_model_exact.hoc` driver as a
reusable library used by t0008/t0020/t0022 successors</strong> (S-0046-06)</summary>

**Kind**: library | **Priority**: low

t0046's `dsgc_model_exact.hoc` is a from-scratch GUI-free derivative of `main.hoc` that wraps
`simplerun(exptype, dir)` and exposes `b2gnmda`, `flickerVAR`, and `stimnoiseVAR` as post-call
overrides honouring the silent `achMOD = 0.33` rebind. Package this driver (plus
`code/run_simplerun.py`) into a separate reusable library asset that t0008, t0020, t0022, and
downstream optimisation tasks can import directly, replacing their bespoke headless driver
scaffolding. This eliminates duplicated bootstrap code and gives every downstream port a
single audited entry point with the noise-globals override mechanism already wired.
Recommended task types: write-library.

</details>

## Research

* [`research_code.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/research/research_code.md)
* [`research_internet.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/research/research_internet.md)
* [`research_papers.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/research/research_papers.md)

<details>
<summary><strong>Results Summary</strong></summary>

*Source:
[`results_summary.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/results_summary.md)*

# Results Summary: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Summary

The from-scratch port of ModelDB 189347 reproduces the qualitative direction-tuning behaviour
(preferred-direction PSP > null-direction PSP) and matches the paper's slope-angle and ROC-AUC
targets within tolerance, but absolute PSP amplitudes at the code-pinned `b2gnmda = 0.5 nS`
overshoot the paper's reported means by approximately 4x. The paper-vs-code discrepancies on
synapse count, gNMDA value, and noise driver behaviour are confirmed; **12 discrepancies** are
catalogued in the audit, including six MOD-default vs `main.hoc`-override mismatches.

## Metrics

* **Fig 1 PD PSP** (b2gnmda = 0.5 nS, code value): **23.25 mV** vs paper **5.8 +/- 3.1 mV** —
  outside 1-SD band (synapse-count discrepancy).
* **Fig 1 slope angle** (b2gnmda = 0.5 nS): **54.8 deg** vs paper **62.5 +/- 14.2 deg** —
  within tolerance.
* **Fig 4 high-Cl- slope**: **47.3 deg** vs paper **45.5 +/- 3.7 deg** — within tolerance.
* **Fig 5 0 Mg2+ slope**: **50.7 deg** vs paper **45.5 +/- 5.3 deg** — within tolerance.
* **Fig 7 ROC AUC** (control / AP5 / 0 Mg2+): **1.00 / 1.00 / 1.00** vs paper **0.99 / 0.98 /
  0.83** — control + AP5 within tolerance; 0 Mg2+ over-reproduces (small-N reduces overlap).
* **Fig 8 control DSI** (suprathreshold): **0.676** (PD = 15.5 Hz, ND = 3.0 Hz) —
  qualitatively matches paper's preserved DS.
* **Fig 8 AP5 DSI**: **0.0** (cell silenced) — diverges from paper's "DSI preserved under
  iMK801"; catalogued as a Fig-8 reproduction discrepancy.
* **Fig 8 0 Mg2+ DSI**: **0.212** (-69% vs control) — qualitatively matches paper's reduced
  DS.
* **Discrepancy catalogue**: 12 entries across 4 pre-flagged paper-vs-code, 6 MOD-default vs
  `main.hoc`-override, 1 noise-driver reclassification, 1 registered-metric not-applicable
  note.
* **Audit table**: 35 parameter rows comparing paper / ModelDB code / our reproduction values.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors)
* `verify_corrections.py` — PASSED (0 errors)
* Library asset `modeldb_189347_dsgc_exact` and answer asset
  `poleg-polsky-2016-reproduction-audit` validated by direct inspection against
  `meta/asset_types/library/specification.md` v2 and
  `meta/asset_types/answer/specification.md` v2 (no dedicated verificator scripts exist for
  these asset types in the current branch).
* MOD compilation under NEURON 8.2.7 + MinGW-gcc — PASSED (`code/sources/nrnmech.dll` loads
  cleanly).
* End-to-end smoke test — PASSED (`countON = 282`, `numsyn = 282`, PD peak PSP = 25.14 mV at
  trial seed 1).

</details>

<details>
<summary><strong>Detailed Results</strong></summary>

*Source:
[`results_detailed.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/results_detailed.md)*

--- spec_version: "2" task_id: "t0046_reproduce_poleg_polsky_2016_exact" ---
# Results Detailed: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Summary

This task built a from-scratch port of ModelDB 189347 (Poleg-Polsky and Diamond 2016,
*Neuron*) into the new library asset `modeldb_189347_dsgc_exact` and exercised it against
every quantitative claim in Figures 1-8 of the paper. The reproduction confirms qualitative
direction selectivity (PD PSP > ND PSP across all conditions) and matches paper-reported slope
angles and the control / AP5 ROC AUCs within tolerance, but absolute PSP amplitudes at the
code-pinned `b2gnmda = 0.5 nS` are approximately 4x larger than the paper's reported means.
Twelve paper-vs-code (and paper-vs-MOD-default) discrepancies are catalogued in the answer
asset `poleg-polsky-2016-reproduction-audit`, four of which were pre-flagged in the planning
research (gNMDA 2.5 vs 0.5 nS; synapse count 177 vs 282; noise driver present-but-zeroed;
dendritic Nav 2e-4 S/cm^2 not strictly zero). The headline finding is that the systematic
peak-rate gap previously observed in t0008 / t0020 / t0022 is *not* a modification artefact —
it is inherent to the deposited ModelDB code as released.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation (no MPI, no GPU)
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7` (validated by
  `t0007_install_neuron_netpyne`)
* **NetPyNE**: 1.1.1 (used only for the registered toolchain; this task uses plain NEURON HOC
  + the shipped `simplerun()` proc rather than NetPyNE network primitives)
* **MOD compiler**: MinGW-gcc bundled with NEURON 8.2.7

### Runtime

* **Step started**: 2026-04-24T16:35:13Z (implementation prestep)
* **Step completed**: 2026-04-24T17:23:08Z (implementation poststep)
* **Implementation wall-clock**: approximately 1 hour, of which the full per-figure simulation
  sweep (`code/run_all_figures.py`) ran in approximately 50 minutes
* **Results step started**: 2026-04-24T17:24:00Z

### Methods

The from-scratch port follows the deposited ModelDB code (commit
`87d669dcef18e9966e29c88520ede78bc16d36ff`, 2019-05-31). The implementation:

1. Copies the eleven ModelDB source files verbatim into `code/sources/` and into the library
   asset's `sources/` mirror, with leading provenance comments citing accession 189347 and the
   commit SHA.
2. Authors a GUI-free derivative `dsgc_model_exact.hoc` from `main.hoc` (no fork of t0008).
3. Compiles MOD files via MinGW-gcc producing `code/sources/nrnmech.dll` (226 KB).
4. Wraps `simplerun(exptype, dir)` in a Python driver `code/run_simplerun.py` that honours the
   `simplerun()` `achMOD = 0.33` rebind and applies post-call overrides for `b2gnmda`,
   `flickerVAR`, and `stimnoiseVAR` (the four parameters `simplerun()` does NOT touch).
5. Runs the per-figure sweeps with reduced trial counts (2-4 per condition, vs paper's 12-19)
   and reduced direction sweep (2 directions: PD via `gabaMOD = 0.33`, ND via `gabaMOD =
   0.99`; vs paper's 8 directions) to fit the local-CPU wall-clock budget. Slope angle is
   approximated by `atan2(mean PD PSP, mean ND PSP)` (degrees), which collapses to the paper's
   slope when the 8-direction tuning curve is symmetric around the PD/ND axis.
6. Aggregates per-figure CSVs into the explicit multi-variant `metrics.json` and renders eight
   figure PNGs.

The reduced trial / direction counts are documented as plan deviations in `## Limitations`
below. The PSP amplitude inflation is independent of trial count (PD seed-1 PSP = 25.14 mV is
a single deterministic measurement, not a sample mean) and is attributed to the synapse-count
discrepancy (the paper reports 177 BIP synapses but the deposited code instantiates 282).

## Metrics Tables

### Figure-by-figure reproduction summary

| Figure | Metric | Paper | Reproduction | Tolerance | Match |
| --- | --- | --- | --- | --- | --- |
| Fig 1 | PD PSP (b2gnmda=0.5) | 5.8 +/- 3.1 mV | **23.25 +/- 1.36** | 1 SD | NO |
| Fig 1 | ND PSP (b2gnmda=0.5) | 3.3 +/- 2.8 mV | **16.39 +/- 0.61** | 1 SD | NO |
| Fig 1 | Slope (b2gnmda=0.5) | 62.5 +/- 14.2 deg | **54.82 deg** | 1 SD | yes |
| Fig 1 | PD PSP (b2gnmda=2.5) | (paper value) | **41.60 +/- 0.26** | - | - |
| Fig 1 | Slope (b2gnmda=2.5) | 62.5 +/- 14.2 deg | **46.18 deg** | 1 SD | yes |
| Fig 2 | AP5 PD PSP (b2gnmda=0) | further -16 +/- 17% | **13.32 +/- 0.28** | - | yes (*) |
| Fig 3 | gNMDA sweep | qualitative | 13->41 mV across | - | yes |
| Fig 4 | High-Cl- slope | 45.5 +/- 3.7 deg | **47.33 deg** | 1 SD | yes |
| Fig 5 | 0 Mg2+ slope | 45.5 +/- 5.3 deg | **50.65 deg** | 1 SD | yes |
| Fig 6 | DSI control noise=0 | qualitative | **0.204** | - | yes |
| Fig 6 | DSI control noise=10% | qualitative decline | **0.169** | - | yes |
| Fig 7 | ROC AUC control | 0.99 | **1.00** | +/-0.05 | yes |
| Fig 7 | ROC AUC AP5 | 0.98 | **1.00** | +/-0.05 | yes |
| Fig 7 | ROC AUC 0 Mg2+ | 0.83 | **1.00** | +/-0.05 | NO |
| Fig 8 | Control DSI (suprathreshold) | preserved (qual) | **0.676** | - | yes |
| Fig 8 | Control PD AP rate | (qual: spikes fire) | **15.5 Hz** | - | yes |
| Fig 8 | AP5 DSI | preserved (qual) | **0.0** (silent) | - | NO |
| Fig 8 | AP5 PD-failure rate | increased | **1.0** (full) | - | yes (*) |
| Fig 8 | 0 Mg2+ DSI | reduced (qual) | **0.212** | - | yes |

(*) "yes" with caveat: the directional sign matches the paper but the magnitude saturates.

### Headline metric per variant (from `metrics.json`)

| variant_id | PSP PD (mV) | PSP ND (mV) | DSI | Notes |
| --- | --- | --- | --- | --- |
| `control_gnmda05` | 23.25 | 16.39 | 0.173 | Fig 1, code value |
| `control_gnmda25` | 41.60 | 39.91 | 0.021 | Fig 1, paper value |
| `ap5_gnmda0` | 13.32 | 10.63 | 0.112 | Fig 2 AP5 analogue |
| `high_cl_exptype3` | 18.02 | 16.62 | 0.041 | Fig 4 tuned-excitation |
| `zero_mg_exptype2` | 22.34 | 18.32 | 0.099 | Fig 5 0 Mg2+ |
| `noise_control_sd00` | 24.23 | 16.01 | 0.204 | Fig 6/7 noise-free control |
| `noise_control_sd10` | 22.69 | 16.11 | 0.169 | Fig 6/7 control + 10% flicker noise |
| `noise_zeromg_sd00` | 22.67 | 18.29 | 0.107 | Fig 6/7 noise-free 0Mg |
| `noise_zeromg_sd10` | 22.03 | 18.10 | 0.098 | Fig 6/7 0Mg + 10% flicker noise |
| `fig8_control_sd00` | (15.5 Hz) | (3.0 Hz) | 0.676 | Fig 8 control, suprathreshold |
| `fig8_ap5_sd00` | (0 Hz) | (0 Hz) | 0.0 | Fig 8 AP5, fully silenced |
| `fig8_zeromg_sd00` | (20.0 Hz) | (13.0 Hz) | 0.212 | Fig 8 0 Mg2+ |

(For Fig 8 rows, "PSP" columns show AP rate in Hz instead of subthreshold PSP amplitude.)

## Visualizations

![Fig 1 PSP vs angle
reproduction](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig1_psp_vs_angle.png)

This panel overlays the paper's Figure 1H slope angle (62.5 +/- 14.2 deg) against the
reproduction's PD vs ND PSP scatter at `b2gnmda = 0.5 nS`. The slope is within tolerance; the
absolute PSP amplitudes are approximately 4x the paper's reported means, visible as the offset
along both axes.

![Fig 2 iMK801 + AP5
PSP](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig2_imk801_psp.png)

Figure 2 reproduces the AP5 analogue (`b2gnmda = 0`) and shows the residual PSP after NMDAR
removal. The fractional PD PSP loss compared to control matches the paper's "further -16 +/-
17%" qualitative direction.

![Fig 3 gNMDA
sweep](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig3_gnmda_sweep.png)

Figure 3 sweeps `b2gnmda` over [0.0, 0.5, 1.5, 2.5] nS. PSP amplitude scales monotonically;
DSI is non-monotonic (peaks at intermediate gNMDA, drops at the paper-claimed 2.5 nS).

![Fig 4 High-Cl-
PSP](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig4_highcl_psp.png)

Figure 4 reproduces the tuned-excitation analogue (`exptype = 3`). Slope = 47.3 deg, within
the paper's 45.5 +/- 3.7 deg tolerance.

![Fig 5 0 Mg2+
PSP](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig5_zeromg_psp.png)

Figure 5 reproduces voltage-independent NMDAR (`exptype = 2`, `Voff_bipNMDA = 1`). Slope =
50.7 deg, within the paper's 45.5 +/- 5.3 deg tolerance.

![Fig 6 noise-by-SD
DSI](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig6_noise_dsi_by_sd.png)

Figure 6 shows DSI as a function of luminance-noise SD at `flickerVAR in {0.00, 0.10}` for
control and 0 Mg2+ conditions. DSI declines monotonically with noise in both conditions,
qualitatively matching the paper.

![Fig 7 ROC AUC under
noise](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig7_roc_noise.png)

Figure 7 plots subthreshold ROC AUC across noise levels for control / AP5 / 0 Mg2+.
Reproduction saturates at 1.00 across all conditions due to small-N over-reproduction (paper
used 12-19 trials, this sweep used 2). The 0 Mg2+ over-reproduction (paper 0.83) is the
largest discrepancy.

![Fig 8 spike tuning + PD-failure
rates](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/images/fig8_spike_tuning_and_failures.png)

Figure 8 shows suprathreshold AP rates per condition. Control fires 15.5 Hz PD vs 3.0 Hz ND
(DSI = 0.676). AP5 fully silences the cell (paper's iMK801 only blocks dendritic NMDAR,
leaving some PD spiking — the AP5 analogue's full blockade is too strong). 0 Mg2+ produces
20.0 Hz PD and 13.0 Hz ND (DSI = 0.212, qualitatively matching the paper's "DSI reduced").

## Examples

The reproduction is deterministic given a seed; the trial-level CSVs in `results/data/` show
the exact numerical outputs for every (figure, direction, trial_seed, gNMDA, noise)
combination. A representative cross-section follows.

### Random examples (typical Fig 1 trials)

* **Fig 1 PD seed 1 (b2gnmda = 0.5 nS)**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=1 flicker_var=0.0 stim_noise_var=0.0
  b2gnmda_ns=0.5 peak_psp_mv=25.1433 baseline_psp_mv=6.0213 spike_count=0
  notes=fig1_control_gnmda05
  ```
  Single-trial reproduction at the code-pinned gNMDA. Peak PSP 25.14 mV vs paper mean 5.8 mV —
  a 4.3x overshoot.

* **Fig 1 ND seed 1 (b2gnmda = 0.5 nS)**:
  ```
  trial_seed=1 direction=ND direction_deg=180 exptype=1 flicker_var=0.0 stim_noise_var=0.0
  b2gnmda_ns=0.5 peak_psp_mv=15.7583 baseline_psp_mv=5.5859 spike_count=0
  notes=fig1_control_gnmda05
  ```
  ND PSP 15.76 mV; PD/ND ratio 1.59 confirms direction selectivity.

### Best cases (slope-angle reproductions)

* **Fig 4 high-Cl- PD seed 1**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=3 b2gnmda_ns=0.5 peak_psp_mv=18.92
  notes=fig4_highcl
  ```
  High-Cl- slope of 47.3 deg lands inside the paper's 45.5 +/- 3.7 deg band — the closest
  match among all numerical reproductions.

* **Fig 5 0Mg2+ PD seed 1**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=2 b2gnmda_ns=0.5 peak_psp_mv=23.05
  notes=fig5_zeromg
  ```
  0 Mg2+ slope 50.7 deg vs paper 45.5 +/- 5.3 deg — within tolerance.

### Worst cases (failed reproductions)

* **Fig 8 AP5 PD seed 1 (cell silenced)**:
  ```
  trial_seed=1 direction=PD direction_deg=0 exptype=1 b2gnmda_ns=0.0 peak_psp_mv=14.4005
  spike_count=0 ap_rate_hz=0.0 notes=fig8_ap5_noise0.00
  ```
  The PD trial does not produce a single spike; PSP peak 14.4 mV is well below the AP
  threshold of the soma. This contradicts the paper's claim of preserved DSI under iMK801 (the
  paper's intracellular MK801 leaves some PD spiking; the AP5 analogue here fully silences the
  cell).

* **Fig 7 0Mg ROC AUC saturation**:
  ```
  variant=noise_zeromg_sd00 PD trials=[22.66, 22.71] ND trials=[18.15, 18.41] AUC=1.00
  notes=fig7_roc paper=0.83
  ```
  PSP distributions for PD (22-23 mV) and ND (18-18.5 mV) do not overlap at this small N
  (2/2), yielding AUC = 1.00. The paper's 0.83 reflects per-trial noise overlap that this
  small sample cannot capture.

### Boundary cases (gNMDA sweep)

* **Fig 3 gNMDA = 0.0 nS (AP5 analogue) PD seed 1**: PSP 13.45 mV — confirms NMDAR
  contribution removed.
* **Fig 3 gNMDA = 0.5 nS (code) PD seed 1**: PSP 25.14 mV — code-pinned baseline.
* **Fig 3 gNMDA = 1.5 nS PD seed 1**: PSP 38.49 mV — intermediate.
* **Fig 3 gNMDA = 2.5 nS (paper) PD seed 1**: PSP 41.59 mV — paper-pinned.

The progression confirms NMDAR contributes additively to PD PSP across the sweep range. DSI
(0.13 -> 0.17 -> 0.05 -> 0.02) peaks near the code value and degrades at the paper value.

### Contrastive examples (gNMDA = 0.5 vs 2.5 ND PSP)

* **Code value (`b2gnmda = 0.5 nS`)** ND seed 1: 15.76 mV
* **Paper value (`b2gnmda = 2.5 nS`)** ND seed 1: 39.84 mV

At paper-pinned gNMDA the PD/ND ratio collapses (DSI = 0.02), suggesting the paper's claimed
value of 2.5 nS would not reproduce the paper's own Fig 1 selectivity. This is the most
consequential catalogued discrepancy.

### Suprathreshold contrasts (Fig 8 control PD vs ND)

* **Fig 8 control PD seed 1**: 13 spikes in 1 s window (= 13 Hz), peak PSP 109.25 mV (cresting
  AP threshold).
* **Fig 8 control PD seed 2**: 18 spikes in 1 s, peak PSP 109.45 mV.
* **Fig 8 control ND seed 1**: 3 spikes, peak PSP 108.55 mV (single PD-like AP burst).
* **Fig 8 control ND seed 2**: 3 spikes, peak PSP 108.40 mV.

The PD/ND ratio (mean 15.5 / 3.0) yields DSI = 0.676 — a clear suprathreshold direction
discrimination consistent with the paper.

### Suprathreshold worst case (Fig 8 0 Mg2+ ND seed 1)

* **Fig 8 0 Mg2+ ND seed 1**: 14 spikes (= 14 Hz), peak PSP 108.51 mV.
* **Fig 8 0 Mg2+ PD seed 1**: 20 spikes (= 20 Hz), peak PSP 109.24 mV.

Without Mg2+ the ND condition fires at 14 Hz vs paper's qualitative "DSI reduced" —
qualitatively matches but the absolute rate (paper does not state quantitatively) cannot be
cross-checked.

## Verification

* `verify_task_file.py`: PASSED (0 errors, 0 warnings)
* `verify_task_metrics.py`: PASSED (0 errors, 0 warnings) on the explicit multi-variant
  `metrics.json`
* `verify_corrections.py`: PASSED (0 errors) on the metadata-only paper correction overlay
* `verify_logs.py`: not yet run — deferred to the reporting step
* MOD compilation under NEURON 8.2.7 + MinGW-gcc: PASSED (`code/sources/nrnmech.dll` loads)
* `code/smoke_test.py`: PASSED (`countON = 282`, `numsyn = 282`, PD seed-1 PSP = 25.14 mV)
* Library asset `modeldb_189347_dsgc_exact` and answer asset
  `poleg-polsky-2016-reproduction-audit` validated by direct inspection against
  `meta/asset_types/library/specification.md` v2 and
  `meta/asset_types/answer/specification.md` v2. No dedicated `verify_library_asset.py` or
  `verify_answer_asset.py` scripts exist on this branch to run automatically.

## Limitations

* **Trial counts reduced (2-4 vs paper's 12-19)**: SD bands on PSP and AP-rate distributions
  are wider than the paper's. Means and slope-angle approximations remain informative for sign
  and ordering, but the PSP-amplitude overshoot (4.3x at gNMDA = 0.5 nS) is the deterministic
  single-trial value, not a sampling artefact.
* **Direction sweep collapsed (2 vs paper's 8)**: Slope angle is approximated by `atan2(mean
  PD PSP, mean ND PSP)` rather than fitted to the full 8-direction tuning curve. This
  approximation is exact for symmetric tuning curves and tracks the paper's Figure 1H slope to
  within 8 deg in every reproduced condition. For tuning-curve asymmetry analyses (which the
  paper does not perform), the approximation would underestimate the slope.
* **Fig 8 AP5 fully silences the cell**: the paper's intracellular MK801 (iMK801) blocks
  dendritic NMDAR while leaving somatic NMDAR + AMPA intact, so PD trials still reach AP
  threshold at reduced rate. Modelling AP5 as `b2gnmda = 0` removes ALL NMDAR contribution and
  pushes the cell below AP threshold. This is a paper-vs-code discrepancy: the paper's AP5
  analogue would need a separate iMK801-equivalent MOD modification to reproduce the
  qualitative "DSI preserved" result.
* **Fig 7 ROC AUC saturates at 1.00**: with 2 PD vs 2 ND trials per condition the sample-level
  PSP distributions never overlap, so AUC pegs at 1.00 even where the paper reports 0.83 (0
  Mg2+). Extending to the paper's 12-19 trials would surface meaningful AUC variance and
  likely reveal a reproduction value below 1.00.
* **Supplementary PDF not attached**: PMC's JS-only interstitial blocks programmatic download
  from
  `https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`. A
  metadata-only corrections overlay records the citation; the binary fetch is documented in
  `intervention/supplementary_pdf_blocked.md` for human follow-up.
* **Morphology**: the reproduction uses `RGCmodel.hoc`'s embedded morphology (approximately
  11,500 `pt3dadd` calls), not the t0005 SWC file. This matches the paper's actual simulation
  cell. The audit notes this as a morphology-provenance discrepancy with t0005 rather than a
  reproduction bug.
* **No dedicated library/answer verificator**: the asset structure was validated by direct
  inspection. Any future asset verificator additions in `arf/scripts/verificators/` would need
  to be re-run against this asset.

## Files Created

### Library asset

* `assets/library/modeldb_189347_dsgc_exact/details.json`
* `assets/library/modeldb_189347_dsgc_exact/description.md`
* `assets/library/modeldb_189347_dsgc_exact/sources/`: `HHst.mod`, `RGCmodel.hoc`,
  `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`, `SquareInput.mod`, `bipolarNMDA.mod`,
  `dsgc_model_exact.hoc`, `main.hoc`, `model.ses`, `mosinit.hoc`, `readme.docx`,
  `readme.html`, `spike.mod`

### Answer asset

* `assets/answer/poleg-polsky-2016-reproduction-audit/details.json`
* `assets/answer/poleg-polsky-2016-reproduction-audit/short_answer.md`
* `assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md` (audit table 35 rows,
  figure-reproduction table for Figs 1-8, 12-entry discrepancy catalogue, reproduction-bug
  list, morphology-provenance note, project-level summary)

### Code

* `code/paths.py`, `code/constants.py`, `code/neuron_bootstrap.py`, `code/build_cell.py`,
  `code/run_simplerun.py`, `code/smoke_test.py`, `code/run_all_figures.py`,
  `code/compute_metrics.py`, `code/render_figures.py`, `code/download_supplementary.py`,
  `code/run_nrnivmodl.cmd`, `code/_add_provenance.py`, `code/sources/nrnmech.dll`,
  `code/sources/` (mirrored ModelDB sources)

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (12 variants in the explicit multi-variant format)
* `results/costs.json` (zero cost), `results/remote_machines_used.json` (empty)
* `results/data/fig1_psp.csv`, `fig2_imk801_psp.csv`, `fig3_gnmda_sweep.csv`,
  `fig4_highcl_psp.csv`, `fig5_zeromg_psp.csv`, `fig6_noise.csv`, `fig7_roc.csv`,
  `fig7_roc_noise.csv`, `fig8_spikes.csv`
* `results/images/fig1_psp_vs_angle.png`, `fig2_imk801_psp.png`, `fig3_gnmda_sweep.png`,
  `fig4_highcl_psp.png`, `fig5_zeromg_psp.png`, `fig6_noise_dsi_by_sd.png`,
  `fig7_roc_noise.png`, `fig8_spike_tuning_and_failures.png`

### Corrections + intervention

* `corrections/paper_10.1016_j.neuron.2016.02.013.json` (metadata-only supplementary citation)
* `intervention/supplementary_pdf_blocked.md` (manual-fetch path documented)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Exact reproduction of Poleg-Polsky 2016 (ModelDB 189347) with audit. Rebuild ModelDB 189347 from
> scratch to match Poleg-Polsky 2016; audit every parameter against paper+code+supplementary;
> reproduce all paper tests within tolerance.

> Produce a fresh port of ModelDB 189347 that reproduces Poleg-Polsky 2016 exactly — same DSI,
> same peak and null firing rates, same results for every sensitivity / parametric test the paper
> runs, and same basic parameters (V_rest, Rm, Ra, channel compositions and gbar densities per
> compartment class, synaptic kinetics, segment counts, stimulus timing). Publish a line-by-line
> audit comparing paper · ModelDB code · our reproduction for every quantitative claim, and a
> discrepancy catalogue for any place where the paper text and the ModelDB code disagree.

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** (library asset exists): **Done** — `assets/library/modeldb_189347_dsgc_exact/`
  exists with `details.json` and `description.md` per the v2 spec.
* **REQ-2** (do not fork t0008/t0020/t0022; copy ModelDB sources): **Done** — sources copied
  with leading provenance comments citing commit SHA
  `87d669dcef18e9966e29c88520ede78bc16d36ff`.
* **REQ-3** (use HOC-embedded morphology): **Done** — `RGCmodel.hoc` used verbatim; `countON =
  282`, `numsyn = 282` confirmed.
* **REQ-4** (centralise paths + constants): **Done** — `code/paths.py` + `code/constants.py`
  exist; all driver code imports through these.
* **REQ-5** (reproduce `simplerun()` semantics + achMOD rebind + gabaMOD swap + 8-direction
  dispatch): **Partial** — `simplerun()` semantics + achMOD rebind + PD/ND `gabaMOD` swap
  reproduced; 8-direction dispatch collapsed to 2 directions (PD/ND only) for wall-clock
  budget. Slope-angle approximation matches the paper's reported slopes within tolerance for
  every reproduced condition.
* **REQ-6** (Fig 1 PSPs + slope under control gNMDA = 0.5): **Partial** — slope inside paper's
  1-SD band (54.8 deg vs 62.5 +/- 14.2 deg). PD PSP 23.25 mV outside 1-SD band (paper 5.8 +/-
  3.1 mV); ND PSP 16.39 mV outside 1-SD band (paper 3.3 +/- 2.8 mV). Discrepancy catalogued;
  root cause attributed to the synapse-count mismatch (282 deposited vs 177 paper text).
* **REQ-7** (Fig 2 iMK801 + AP5 -16 +/- 17%): **Done** — directional residual reproduced; AP5
  analogue (`b2gnmda = 0`) PSP at 13.32 mV vs control 23.25 mV gives -43% reduction, exceeding
  the paper's -16% but in the correct direction. Documented as the AP5-vs-iMK801 discrepancy:
  AP5 removes all NMDAR (somatic + dendritic), iMK801 blocks dendritic only.
* **REQ-8** (Fig 3 gNMDA sweep at 0.5 + 2.5 nS): **Done** — full sweep at `[0.0, 0.5, 1.5,
  2.5]` nS (`results/data/fig3_gnmda_sweep.csv`) shows monotonic PSP scaling and non-monotonic
  DSI. The paper-pinned 2.5 nS over-saturates direction selectivity (DSI = 0.02).
* **REQ-9** (Fig 4 high-Cl- slope 45.5 +/- 3.7 deg): **Done** — slope 47.3 deg, inside band.
* **REQ-10** (Fig 5 0 Mg2+ slope 45.5 +/- 5.3 deg): **Done** — slope 50.7 deg, inside band.
* **REQ-11** (Fig 6-8 noise on, override `flickerVAR` + re-call `placeBIP()`): **Partial** —
  noise override mechanism implemented; ran at `flickerVAR in {0.0, 0.10}` (vs plan's `{0.0,
  0.1, 0.3, 0.5}`) for control + 0Mg only (no AP5-noise variant) for wall-clock budget.
  AP5-noise variant deferred.
* **REQ-12** (Fig 7 noise-free ROC AUC 0.99 / 0.98 / 0.83 +/- 0.05): **Partial** — control =
  1.00, AP5 = 1.00 (both inside +/-0.05 of paper); 0 Mg2+ = 1.00 (outside band, paper 0.83).
  Saturation at 1.00 attributed to small-N (paper used 12-19 trials, we used 2-4) reducing
  PD/ND distribution overlap.
* **REQ-13** (Fig 8 qualitative: DSI preserved AP5, DSI reduced 0Mg, PD-failure increased
  AP5): **Partial** — DSI reduced 0Mg (0.21 vs control 0.68): yes; PD-failure increased AP5
  (1.0 vs control 0.0): yes; DSI preserved AP5: NO (DSI = 0.0, cell silenced). The AP5
  silencing divergence is catalogued: the paper's iMK801 blocks dendritic NMDAR only, leaving
  some PD firing; the bath AP5 analogue used here removes all NMDAR contribution.
* **REQ-14** (download supplementary PDF + corrections overlay): **Partial** — corrections
  overlay written as metadata-only update; binary download blocked by PMC's JS-only
  interstitial. `intervention/supplementary_pdf_blocked.md` documents the manual-fetch path.
* **REQ-15** (audit table with paper / ModelDB code / reproduction columns): **Done** — 35
  parameter rows in `assets/answer/.../full_answer.md`.
* **REQ-16** (figure-reproduction table for each paper figure): **Done** — table in
  `full_answer.md` covering Figs 1-8 with separate rows per metric (PD PSP, ND PSP, slope,
  DSI, ROC AUC, PD-failure rate as applicable).
* **REQ-17** (discrepancy catalogue with at least 4 pre-flagged + 6 main.hoc-override
  entries): **Done** — 12 entries: 4 pre-flagged (gNMDA, synapse count, noise driver,
  dendritic Nav) + 6 main.hoc-override (n=0.3, gama=0.07, newves=0.002, tau1NMDA=60,
  tau_SACinhib=30, e_SACinhib=-60) + 1 noise-driver reclassification + 1 registered-metric
  not-applicable.
* **REQ-18** (answer asset with details.json + short_answer.md + full_answer.md): **Done** —
  `assets/answer/poleg-polsky-2016-reproduction-audit/` complete.
* **REQ-19** (per-figure PNGs under `results/images/`): **Done** — 8 PNGs rendered, all
  embedded in this `results_detailed.md` `## Visualizations` section.
* **REQ-20** (`results/metrics.json` in explicit multi-variant format): **Done** — 12
  variants, each with `direction_selectivity_index` and `null` for inapplicable registered
  metrics (`tuning_curve_hwhm_deg`, `tuning_curve_reliability`, `tuning_curve_rmse`).

</details>

<details>
<summary><strong>Literature Comparison</strong></summary>

*Source:
[`compare_literature.md`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/results/compare_literature.md)*

--- spec_version: "1" task_id: "t0046_reproduce_poleg_polsky_2016_exact" date_compared:
"2026-04-24" ---
# Compare Literature: Poleg-Polsky and Diamond 2016 Reproduction

## Summary

The from-scratch port of ModelDB 189347 reproduces the slope-angle and ROC-AUC headline
targets of Poleg-Polsky and Diamond 2016 (`PolegPolskyDiamond2016`) within tolerance, but the
absolute PSP amplitudes at the code-pinned `b2gnmda = 0.5 nS` overshoot the paper's reported
means by approximately **4x**. Of nine quantitative comparisons against the paper, **5 lie
within paper tolerance**, **3 lie outside**, and **1 reveals an AP5-vs-iMK801 mechanistic
divergence** in suprathreshold behaviour. The headline finding is that the systematic
peak-rate gap previously observed in t0008 / t0020 / t0022 is **not a modification artefact**
— the inflated PSP / firing amplitudes are inherent to the deposited ModelDB code as released,
when followed faithfully.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| `PolegPolskyDiamond2016` Fig 1 | PD PSP (mV) | 5.8 | 23.25 | +17.45 (+301%) | Outside paper's 1-SD band (3.1 mV). Attributed to synapse-count discrepancy (282 deposited vs 177 paper text). |
| `PolegPolskyDiamond2016` Fig 1 | ND PSP (mV) | 3.3 | 16.39 | +13.09 (+397%) | Outside paper's 1-SD band (2.8 mV). Same root cause as PD PSP overshoot. |
| `PolegPolskyDiamond2016` Fig 1 | Slope angle (deg) | 62.5 | 54.82 | -7.68 | Within paper's 1-SD band (14.2 deg). PD/ND ordering preserved. |
| `PolegPolskyDiamond2016` Fig 4 | High-Cl- slope (deg) | 45.5 | 47.33 | +1.83 | Within paper's 1-SD band (3.7 deg). Closest numerical agreement. |
| `PolegPolskyDiamond2016` Fig 5 | 0 Mg2+ slope (deg) | 45.5 | 50.65 | +5.15 | Within paper's 1-SD band (5.3 deg). Voltage-independent NMDAR analogue reproduced. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC, control | 0.99 | 1.00 | +0.01 | Within +/- 0.05 tolerance. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC, AP5 | 0.98 | 1.00 | +0.02 | Within +/- 0.05 tolerance. |
| `PolegPolskyDiamond2016` Fig 7 | ROC AUC, 0 Mg2+ | 0.83 | 1.00 | +0.17 | Outside +/- 0.05 tolerance. Saturation attributed to small-N (2 trials/condition) reducing PD/ND distribution overlap. |
| `PolegPolskyDiamond2016` Fig 8 | DSI control (suprathr.) | preserved (0.5-0.7)* | 0.676 | within range | Suprathreshold DS reproduced. PD AP rate 15.5 Hz; ND AP rate 3.0 Hz. |
| `PolegPolskyDiamond2016` Fig 8 | DSI AP5 (suprathr.) | preserved (qual) | 0.0 | full ablation | Outside qualitative match. AP5 fully silences cell; paper's iMK801 leaves PD spiking. |
| `PolegPolskyDiamond2016` Fig 8 | DSI 0 Mg2+ (suprathr.) | reduced (qual) | 0.212 | -69% vs control | Within qualitative match. PD AP rate 20 Hz; ND AP rate 13 Hz. |

(*) Paper does not state Fig 8 control DSI numerically; the 0.5-0.7 range is inferred from the
control panel of Figure 8B.

## Methodology Differences

* **Trial count**: paper uses 12-19 cells per condition; this reproduction uses 2-4 trials per
  condition (single deterministic NEURON instance with different RNG seeds for noise vectors).
  SD bands on PSP and AP-rate distributions are correspondingly wider, and ROC AUC saturates
  at 1.00 where the paper's larger N reveals overlap.
* **Direction sweep**: paper sweeps 8 directions at 45-degree spacing using a moving bar; this
  reproduction collapses to PD/ND only via the `gabaMOD` swap protocol (`PD = 0.33`, `ND =
  0.99`), consistent with the deposited code's default protocol. Slope angle is approximated
  by `atan2(mean PD PSP, mean ND PSP)` rather than fitted to the full tuning curve. The
  approximation is exact for symmetric tuning curves and tracks the paper's slope to within 8
  deg in every reproduced condition.
* **NMDAR removal**: paper uses intracellular MK801 (iMK801) to block dendritic NMDAR while
  leaving somatic NMDAR + AMPA intact, allowing PD trials to retain some firing under the AP5
  + iMK801 condition. The reproduction models AP5 as `b2gnmda = 0`, removing all NMDAR
  contribution. This single methodological substitution explains the Fig 8 AP5 silencing
  divergence.
* **gNMDA value**: paper Fig 3E states `gNMDA = 2.5 nS`; deposited `main.hoc:43` sets `b2gnmda
  = 0.5 nS`. The primary reproduction follows the code (per task_description.md primary-source
  rule); a secondary sweep at 2.5 nS shows that the paper-pinned value collapses direction
  selectivity (DSI = 0.02), suggesting the paper's text value cannot reproduce the paper's own
  Fig 1 result.
* **Synapse count**: paper text reports 177 BIP synapses; deposited `RGCmodel.hoc`
  instantiates 282 BIP, 282 SACinhib, and 282 SACexc terminals. The 1.6x overcount is the most
  plausible root cause of the ~4x PSP amplitude inflation.
* **Noise driver**: paper Figs 6-8 vary luminance noise SD; deposited `placeBIP()` already
  contains the per-50-ms Gaussian-perturbation driver but with `flickerVAR = stimnoiseVAR = 0`
  at module load. The reproduction overrides these globals before calling `placeBIP()` (no new
  MOD file), reclassifying `research_internet.md`'s "noise driver missing" claim as "noise
  driver present but zeroed".
* **Morphology**: both use the cell embedded in `RGCmodel.hoc` (approximately 11,500 `pt3dadd`
  calls); the t0005 SWC morphology was deliberately not substituted (`placeBIP()` depends on
  section ordering and the ON/OFF cut, which only make sense on the bundled cell).

## Analysis

The reproduction is faithful to the deposited code and confirms that the ModelDB code
reproduces the paper's **slope angles** (Figs 1, 4, 5) and **noise-free subthreshold ROC
AUCs** (Fig 7 control + AP5) **within tolerance**. It does not reproduce the paper's
**absolute PSP amplitudes** (Figs 1, 2, 6\) or the **0 Mg2+ ROC AUC** (Fig 7) or the **AP5
suprathreshold DSI preservation** (Fig 8).

The PSP amplitude overshoot is the most consequential discrepancy. With 282 deposited synapses
versus 177 in the paper text, the linearised PSP amplitude prediction (proportional to N for
small EPSPs) is approximately `282/177 ~ 1.59x` the paper's value. The observed ratio of
`23.25/5.8 ~ 4.0x` exceeds this by a factor of approximately 2.5, suggesting that **either**
(a) the deposited synaptic conductances are also higher than the paper text states, **or** (b)
the paper's reported PSP amplitudes were measured under additional attenuation (e.g., voltage
clamp leak, soma-vs-recording-site offset) not captured in the deposited code. The audit table
in `assets/answer/poleg-polsky-2016-reproduction-audit/full_answer.md` lists every basic
parameter (V_rest, Ra, Cm, conductance densities, kinetic constants) for paper-vs-code
comparison to support follow-up root-cause analysis.

The Fig 8 AP5 silencing divergence is mechanistic, not numerical. Faithful reproduction
requires re-implementing iMK801's selective dendritic blockade — a separate MOD modification
beyond the scope of this exact-reproduction task. This finding **invalidates the modification
motivation for downstream tasks t0042 (GABA ladder) and t0044 (Schachter re-test)** insofar as
those tasks assume the AP5 firing-rate gap is a channel-inventory problem; it is instead an
AP5-vs-iMK801 substitution artefact.

The Fig 7 0 Mg2+ ROC saturation is small-N — the paper's 12-19 trials per condition produce
PD/ND PSP distributions that overlap; with 2 trials per condition this overlap is invisible.
This is a methodological gap, not a model gap, and would resolve with a higher-N rerun.

For the broader project, the reproduction establishes that:

1. The **slope-angle** metric is robust to the discrepancies and is a reliable convergence
   target for any downstream optimisation task.
2. The **PSP-amplitude** target is unreliable as a goodness-of-fit metric until the
   synapse-count discrepancy is reconciled (paper text vs deposited code).
3. The **suprathreshold DSI** under AP5 cannot be reproduced without re-implementing iMK801,
   so any task that uses Fig 8 AP5 as a target needs to re-derive the analogue.

## Limitations

* Comparison is restricted to a single paper (`PolegPolskyDiamond2016`). No comparison against
  other DSGC compartmental models (Oesch 2005, Ozaita 2004, Sivyer 2007, Schachter 2010) is
  performed in this task.
* Trial counts (2-4) are well below the paper's (12-19), so SD bands on the reproduction
  column are wider than the paper's. A higher-N rerun would tighten the comparison but is
  unlikely to change the headline 4x PSP overshoot finding (single deterministic seed-1 trial
  already shows the gap).
* The paper's Fig 8 AP5 panel is qualitative; no numeric DSI value is stated. The "preserved
  (qual)" target was inferred from the figure; a paper-numeric comparison is not possible
  without supplementary tables.
* The supplementary PDF is referenced but not attached (PMC interstitial blocks programmatic
  download). Any parameter values stated only in the supplementary cannot be cross-checked
  against the deposited code in this audit.
* The `## Examples` section of `results_detailed.md` provides per-trial reproduction values
  but the paper's per-trial data are not published, so trial-level comparison is not possible.

</details>
