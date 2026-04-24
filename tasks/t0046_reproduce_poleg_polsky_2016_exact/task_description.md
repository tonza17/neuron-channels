# Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Correction — 2026-04-24

The original version of this task_description.md (as merged in PR #44) framed the peak-rate mismatch
(~15 Hz in our ports vs "paper's 40-80 Hz range") as a Poleg-Polsky 2016 claim and included a pass
criterion of "firing rates within +/-10% of the paper's stated value". This was wrong.
**Poleg-Polsky & Diamond 2016 is primarily a subthreshold-PSP paper.** Its main figures report PSP
amplitudes (mV), direction-tuning slope angles (degrees), and subthreshold ROC AUC. Only Figure 8
includes spikes, and even there the paper reports qualitative DSI preservation / reduction and
PD-failure rate — not specific peak Hz numbers. The 40-80 Hz target traces back to t0004's
project-internal tuning-curve envelope (sourced from Oesch 2005 rabbit recordings and Sivyer 2013),
not to Poleg-Polsky 2016.

This revision corrects the pass criteria to target PSP amplitudes, slope angles, and ROC AUC as the
primary reproduction metrics, with Figure 8 suprathreshold checks as a secondary qualitative pass.
Spike-rate comparisons against t0004's envelope are explicitly out of scope for this task.

## Motivation

The project has two prior ports of Poleg-Polsky & Diamond 2016 (ModelDB 189347): **t0008** (initial
port using a spatial-rotation proxy for the gabaMOD swap) and **t0020** (re-run with the native
gabaMOD parameter-swap protocol; DSI 0.784 ~ paper's median of ~0.80). Both focused primarily on the
tuning curve as measured through DSI and did not audit every parameter against the paper, did not
reproduce the other tests the paper runs, and did not publish a systematic paper-vs-code discrepancy
catalogue.

The brainstorm-8 audit (t0040) identified paper-vs-observation mismatches across every port and
sweep; some of those mismatches — particularly the peak-rate framing — conflated Poleg-Polsky
2016 with other DSGC papers (Oesch 2005, Sivyer 2013) and therefore do not belong to this task. This
task steps back to establish the faithful reproduction of Poleg-Polsky 2016 on its own terms, using
the paper's own figures and metrics as the target.

## Objective

Produce a fresh port of ModelDB 189347 that reproduces Poleg-Polsky 2016 exactly on the metrics the
paper actually reports — PSP amplitudes, direction-tuning slope angles, ROC AUC under the noise
conditions described in the paper, and qualitative Figure 8 suprathreshold behaviour — using the
paper's own protocols. Publish a line-by-line audit comparing **paper · ModelDB code · our
reproduction** for every quantitative claim, and a discrepancy catalogue for any place where the
paper text and the ModelDB code disagree.

## Paper's Reported Metrics (target of reproduction)

Primary (subthreshold PSP, Figures 1-7):

* **Figure 1** — 8-direction PSPs. PD PSP **5.8 +/- 3.1 mV**, ND PSP **3.3 +/- 2.8 mV**,
  direction-tuning slope **62.5 +/- 14.2 degrees** (multiplicative scaling under voltage-dependent
  NMDAR). DSI preserved under AP5. n=19.
* **Figure 2** — iMK801 (2 mM) dialysis + bath AP5: AP5-after-iMK801 further reduces PD PSP by
  only **16 +/- 17%**. n=15.
* **Figure 3** — NEURON model: 282 presynaptic cells, homogeneous ON-dendrite synapses, tuned
  inhibition, paper-stated **gNMDA = 2.5 nS** (paper) vs **0.5 nS** (ModelDB code)
  **[discrepancy flagged]**. Alternative tuned-excitation scheme predicts additive scaling.
* **Figure 4** — High-Cl- internal (tuned-excitation analogue): slope **45.5 +/- 3.7 degrees**
  (additive). DS reverses PD in 15/20 cells. n=12.
* **Figure 5** — 0 Mg2+ (voltage-dependent NMDAR removed, Ohmic NMDAR analogue): slope **45.5 +/-
  5.3 degrees** (additive). DSI reduced but PD != ND. n=8.
* **Figure 6** — Noisy PSPs under bar + background luminance noise at SD **0 / 10 / 30 / 50%**.
  DSI reduced by noise, strongest in 0 Mg2+. n=12.
* **Figure 7** — Subthreshold ROC / accuracy (noise-free): AUC **0.99 / 0.98 / 0.83** for control
  / AP5 / 0 Mg2+. Accuracy curve area larger in control.

Secondary (suprathreshold APs, Figure 8 only):

* **Figure 8** — DSI preserved under AP5 (qualitative); DSI reduced in 0 Mg2+ (qualitative); AP5
  **raises PD-failure rate**; ROC AUC on spikes under noise. **The paper does not report specific
  peak Hz or aggregate firing-rate numbers for the model.**

Basic parameters (read from ModelDB source, audited vs paper prose where stated):

* V_rest, Ra, Rm, Cm, soma/dendrite channel gbar densities, synaptic kinetics, Jahr-Stevens
  parameters, stimulus timing. See `research/research_internet.md` for extracted ModelDB values.

## Scope

### In Scope

* Full from-scratch port of ModelDB 189347 into a new library asset (do NOT fork t0008, t0020, or
  t0022). Target location:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`.
* Download and attach the supplementary PDF (NIHMS766337; PMC4795984) to the existing
  `10.1016_j.neuron.2016.02.013` paper asset.
* Paper corpus review: Poleg-Polsky & Diamond 2016 (Neuron) PDF + supplementary.
* ModelDB 189347 release: every `.hoc`, `.mod`, `.py`, README, comment, and parameter file in the
  release. Cross-check the release version against the paper's cited version.
* **Reproduce every quantitative claim in Figures 1-8**, as enumerated in "Paper's Reported Metrics"
  above.
* Basic parameters audited against paper + code + supplementary.

### Out of Scope

* **Comparisons against t0004's target tuning-curve envelope** (peak Hz 40-80, null Hz <10, HWHM
  60-90). Those targets come from Oesch 2005 / Sivyer 2013 / Chen 2009 and do not belong in a
  Poleg-Polsky 2016 reproduction task.
* Modifications or improvements beyond the original paper.
* Integration with t0022, t0024, or other downstream modified testbeds.
* Any DSGC models other than Poleg-Polsky 2016.

## Source of Truth

Audit uses all three sources:

1. **Published PDF** — Poleg-Polsky & Diamond 2016, Neuron.
2. **ModelDB 189347 release** — README, `.hoc`, `.mod`, `.py`, parameter files, and all code
   comments. Canonical commit `87d669dcef18e9966e29c88520ede78bc16d36ff` (2019-05-31).
3. **Supplementary materials** — NIHMS766337 (PMC4795984), bundled Supplemental Experimental
   Procedures plus supplementary figures S1-S8. Download during implementation and attach to the
   existing paper asset.

## Paper-vs-Code Discrepancy Handling

The primary reproduction **follows their code** (what they actually ran). If the code fails to
reproduce a specific paper claim within tolerance, flag the discrepancy explicitly with the paper
claim, the code's actual behaviour, and the numerical gap. Known pre-implementation flags from the
research stages:

* **gNMDA discrepancy**: paper Fig 3E states 2.5 nS, ModelDB code uses 0.5 nS.
* **Synapse count discrepancy**: paper states 177 synapses, ModelDB code instantiates 282.
* **Noise driver missing**: shipped `SquareInput.mod` has no luminance-noise driver despite Figures
  6-8 describing per-50-ms noise SD = 0 / 10 / 30 / 50%. Figures 6-8 cannot be reproduced from stock
  code without adding a noise driver; this must itself be flagged as a significant paper-vs-code
  discrepancy (the Figures 6-8 results in the paper must have come from a different code variant).
* **Dendritic Nav**: 2e-4 S/cm2 (small but non-zero), not strictly zero — refines the "passive
  dendrites" wording.

## Pass Criterion

Primary pass criteria (Figures 1-7 subthreshold):

* PD PSP amplitude within **1 SD** of the paper's reported mean (within 3.1 mV of 5.8 mV for Fig 1
  control).
* ND PSP amplitude within **1 SD** (within 2.8 mV of 3.3 mV).
* Slope angle within **1 SD** (within 14.2 degrees of 62.5 degrees for Fig 1; within 3.7-5.3 degrees
  for Figs 4-5 additive regime).
* Under 0 Mg2+: DSI reduced but not zero; preferred direction preserved (paper claim).
* Under High-Cl-: DS reverses PD in >= 50% of trials (paper's 15/20 is 75%; allow flexibility).
* Subthreshold noise-free ROC AUC within **+/- 0.05** of each paper value (0.99 / 0.98 / 0.83 for
  control / AP5 / 0 Mg2+).

Secondary pass criteria (Figure 8 suprathreshold):

* DSI qualitatively preserved under AP5 (both conditions direction-selective).
* DSI qualitatively reduced in 0 Mg2+.
* PD-failure rate increases under AP5 (direction: positive, magnitude not specified by paper).
* No numeric peak-Hz target is asserted; the paper does not state one.

Parameter-match criterion:

* Every basic parameter in the audit table matches ModelDB code exactly; any deviation is documented
  as a reproduction bug, not an intentional modification.

Discrepancy-catalogue criterion:

* Every paper-vs-code discrepancy is catalogued with numerical evidence, including the four
  pre-flagged above (gNMDA, synapse count, missing noise driver, dendritic Nav wording) and any
  further discrepancies found during implementation.

## Deliverables

### Library asset (1)

`assets/library/modeldb_189347_dsgc_exact/`:

* Full NEURON port runnable under the project's NEURON 8.2.7 + NetPyNE 1.1.1 toolchain (from t0007).
* Uses the baseline DSGC morphology from t0005 (or the ModelDB-shipped morphology if that is what
  the paper actually used — audit this; if they differ, this is a discrepancy to flag).
* Source files mirror the ModelDB release structure where practical, with a clear mapping from each
  ModelDB file to the corresponding file in this library.
* Per-file comments identifying the ModelDB source file and line ranges that the port transcribes.
* Adds a luminance-noise driver that reproduces the Figure 6-8 noise protocol (the shipped ModelDB
  code lacks one); this addition must itself be flagged as a paper-vs-code discrepancy.
* Meets the library-asset specification in `meta/asset_types/library/specification.md`.

### Answer asset (1)

`assets/answer/poleg-polsky-2016-reproduction-audit/` with a full audit report.

The `full_answer.md` must include:

* **Audit table** — one row per basic parameter. Columns: **Parameter**, **Paper value** (when
  stated), **ModelDB code value**, **Our reproduction value**, **Match?**, **Citation**.
* **Figure-reproduction table** — one row per figure (1-8) with the paper's reported metric, our
  reproduction metric, tolerance, match verdict, and paper figure reference. Separate rows for PD/ND
  PSP, slope, ROC AUC, etc. as applicable.
* **Discrepancy catalogue** — one entry per paper-vs-code disagreement with numerical evidence.
* **Reproduction bugs** — any place where our port diverges from ModelDB code; each must be fixed
  before the library asset is considered complete.
* One-paragraph summary of what this reproduction establishes for the broader project. Specifically:
  whether Poleg-Polsky's PSP + slope + ROC claims hold under a faithful reimplementation, and a note
  on whether Figure 8 suprathreshold behaviour depends on details that the published code does not
  specify.

### Per-paper figure reproductions (under `results/images/`)

Each paper figure that reports a test this task reproduces gets its own PNG comparing our
reproduction against the paper's figure. Clearly labelled axes and matching ranges.

## Execution Guidance

* **Code-reproduction task type**. Steps: research-papers (done), research-internet (done),
  research-code, planning, implementation, results, compare-literature, suggestions, reporting.
  Skipped: setup-machines, teardown, creative-thinking.
* Local CPU only. No Vast.ai. Estimate 1-2 days of execution time; MOD compilation on Windows may
  take a non-trivial fraction of that, and the noise-driver addition adds one iteration cycle.
* Use absolute imports and centralised `paths.py` / `constants.py` per the project's Python style
  guide.

## Anticipated Risks

* **ModelDB 189347 may reference a morphology file not in t0005**: audit carefully; if the paper
  used a different morphology, flag and either fetch the paper's morphology or document the
  substitution as a reproduction bug.
* **MOD file compilation on Windows NEURON 8.2.7**: some MOD files in older ModelDB releases need
  minor adjustments to compile under modern NEURON. Record every adjustment as a potential
  discrepancy.
* **Noise driver**: the shipped code cannot produce Figures 6-8 because it lacks a luminance noise
  driver. Our port must add one; document the addition as a discrepancy (the paper's Figure 6-8
  results therefore came from a version of the code the authors did not deposit).
* **gNMDA pick**: paper says 2.5 nS, code uses 0.5 nS. Primary reproduction uses 0.5 nS (follow
  code); secondary run at 2.5 nS documents whether the paper claim or the code publishes the Figure
  1-5 behaviour.

## Relationship to Other Tasks

* **Currently blocks (administrative)**: t0042, t0043, t0044 are `intervention_blocked` pending this
  task. **Note**: t0043's peak-rate framing was built on the same category error this task's revised
  scope addresses; after this task completes, the case for t0043 as currently scoped should be
  reviewed explicitly.
* **Complements**: t0008 (initial port) and t0020 (gabaMOD protocol fix) remain in the history as
  partial reproductions focused on DSI. This task does not modify them; it produces an independent,
  more complete reproduction against the paper's actual reported metrics.
* **Precedes**: any future optimisation task (t0033 style) should use this library asset as the
  starting point.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_library_asset.py` passes for `modeldb_189347_dsgc_exact`.
* Answer-asset verificator passes for `poleg-polsky-2016-reproduction-audit`.
* All pass criteria above met: PSP amplitudes within 1 SD, slope angles within 1 SD, ROC AUC within
  +/-0.05, Figure 8 qualitative checks pass, basic parameters match ModelDB code exactly.
* Every paper test attempted is represented in the figure-reproduction table with a match / no-match
  verdict and numerical evidence.
* Discrepancy catalogue is complete and includes the four pre-flagged items plus any new findings.
