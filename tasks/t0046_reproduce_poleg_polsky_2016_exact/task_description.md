# Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Motivation

The project has two prior ports of Poleg-Polsky & Diamond 2016 (ModelDB 189347): **t0008** (initial
port using a spatial-rotation proxy for the gabaMOD swap — DSI 0.316 vs paper 0.80) and **t0020**
(re-run with the native gabaMOD parameter-swap protocol — DSI 0.784, close to paper target). Both
focused primarily on the tuning curve and did not audit every parameter against the paper, did not
reproduce the other tests the paper runs, and did not publish a systematic paper-vs-code discrepancy
catalogue. Peak firing rate in both ports lands at ~15 Hz vs the paper's 40-80 Hz range — evidence
that deviations have accumulated without being fully traced.

The brainstorm-8 audit (t0040) identified paper-vs-observation mismatches across every port and
sweep, and proposed channel-inventory modifications (t0043 Nav1.6+Kv3+NMDA, t0042 GABA ladder, t0044
Schachter re-test) to attack the peak-rate gap. Those are modifications, not reproductions. This
task steps back to establish the faithful reproduction as the baseline before any further
modifications are proposed.

## Objective

Produce a fresh port of ModelDB 189347 that reproduces Poleg-Polsky 2016 exactly — same DSI, same
peak and null firing rates, same results for every sensitivity / parametric test the paper runs, and
same basic parameters (V_rest, Rm, Ra, channel compositions and gbar densities per compartment
class, synaptic kinetics, segment counts, stimulus timing). Publish a line-by-line audit comparing
**paper · ModelDB code · our reproduction** for every quantitative claim, and a discrepancy
catalogue for any place where the paper text and the ModelDB code disagree.

## Scope

### In Scope

* Full from-scratch port of ModelDB 189347 into a new library asset (do NOT fork t0008, t0020, or
  t0022). Target location:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`.
* Paper corpus review: Poleg-Polsky & Diamond 2016 (Neuron) PDF plus any supplementary materials
  available. Download both if not already in the corpus (t0008 and t0020 have the PDF; supplementary
  may not have been fetched).
* ModelDB 189347 release: every `.hoc`, `.mod`, `.py`, README, comment, and parameter file in the
  release. Cross-check the release version against the paper's cited version.
* **Reproduce every test the paper runs**, not just the headline tuning curve. Enumerate them during
  the research stage by reading the paper; likely includes:
  * Baseline tuning curve (DSI, peak Hz, null Hz, HWHM) under the native gabaMOD swap protocol.
  * Any parametric sensitivity experiments the paper describes (e.g., null-direction GABA
    conductance scan, dendritic diameter or length sweeps, NMDA contribution, active-vs-passive
    dendrite comparison).
  * Any spatial-asymmetry or control experiments in the paper.
* Basic parameters audited against paper + code + supplementary:
  * V_rest, Ra (axial resistance, Ohm.cm), Rm (membrane resistance, Ohm.cm^2), Cm (membrane
    capacitance, uF/cm^2).
  * Channel compositions per compartment class (soma, proximal dendrites, distal dendrites, AIS)
    with species (Nav, Kv, Kir, CaL, ...), kinetic parameters, and gbar densities.
  * Synaptic components (AMPA, NMDA, GABA-A) with reversal potentials, rise/decay time constants,
    and conductance amplitudes per terminal class.
  * Stimulus timing and spatial layout (bar width, sweep duration, BIP terminal count and positions,
    SAC terminal count and positions).

### Out of Scope

* Modifications or improvements beyond the original paper (that is what t0043, t0044, and similar
  modification tasks are for). This task is reproduction only.
* Integration with t0022, t0024, or other downstream modified testbeds.
* Any DSGC models other than Poleg-Polsky 2016.

## Source of Truth

Audit uses **all three sources** (per researcher confirmation):

1. **Published PDF** — Poleg-Polsky & Diamond 2016, Neuron.
2. **ModelDB 189347 release** — README, `.hoc`, `.mod`, `.py`, parameter files, and all code
   comments.
3. **Supplementary materials** — any supplementary PDFs, tables, or data accompanying the paper.
   Download if not already in the corpus.

## Paper-vs-Code Discrepancy Handling

Per researcher direction: the primary reproduction **follows their code** (what they actually ran).
If the code fails to reproduce a specific paper claim within tolerance, flag the discrepancy
explicitly. For each flagged case, record: the paper claim, the code's actual behaviour, and the
numerical gap. No paper-text-variant is run in the primary reproduction, but any discrepancy is
named in the audit.

## Pass Criterion

* Every quantitative claim in the paper is reproduced within tolerance:
  * DSI within **+/- 0.05** of the paper's stated value.
  * Firing rates (peak, null) within **+/- 10%** of the paper's stated value.
  * Any other quantitative result (time-to-peak, HWHM, correlation, ...) within **+/- 10%** unless
    the paper gives a tighter bound.
* Every basic parameter in the audit table matches ModelDB code exactly; any deviation is documented
  as a reproduction bug, not an intentional modification.
* Every paper-vs-code discrepancy is catalogued with numerical evidence.

## Deliverables

### Library asset (1)

`assets/library/modeldb_189347_dsgc_exact/`:

* Full NEURON port runnable under the project's NEURON 8.2.7 + NetPyNE 1.1.1 toolchain (from t0007).
* Uses the baseline DSGC morphology from t0005 (or the ModelDB-shipped morphology if that is what
  the paper actually used — audit this; if they differ, this is a discrepancy to flag).
* Source files mirror the ModelDB release structure where practical, with a clear mapping from each
  ModelDB file to the corresponding file in this library.
* Per-file comments identifying the ModelDB source file and line ranges that the port transcribes.
* Meets the library-asset specification in `meta/asset_types/library/specification.md`.

### Answer asset (1)

`assets/answer/poleg-polsky-2016-reproduction-audit/` with a full audit report.

The `full_answer.md` must include:

* **Audit table** — one row per basic parameter. Columns: **Parameter** (V_rest, Ra, Rm, Cm,
  Nav_gbar_soma, Nav_gbar_distal, Kv_gbar_soma, ..., AMPA_g, NMDA_g, GABA_g, ...), **Paper value**,
  **ModelDB code value**, **Our reproduction value**, **Match?**, **Citation**.
* **Test reproduction table** — one row per test the paper runs. Columns: **Paper test**, **Paper
  result** (DSI, peak Hz, ...), **Our reproduction result**, **Tolerance**, **Match?**, **Paper
  figure reference**.
* **Discrepancy catalogue** — one entry per paper-vs-code disagreement with numerical evidence.
* **Reproduction bugs** — any place where our port diverges from ModelDB code; each must be fixed
  before the library asset is considered complete.
* One-paragraph summary of what this reproduction establishes for the broader project: specifically,
  whether the systematic peak-rate gap seen in t0008, t0020, and t0022 is present in the faithful
  reproduction too (implicating the model or the protocol) or absent (implicating our prior
  modifications).

### Per-paper figure reproductions (under `results/images/`)

Each paper figure that reports a test this task reproduces gets its own PNG comparing our
reproduction against the paper's figure. Clearly labelled axes and matching ranges.

## Execution Guidance

* **Code-reproduction task type**. Optional steps to include: research-papers, research-code,
  planning, implementation, creative-thinking (for alternative reproduction strategies if the
  straight port misses targets), results, compare-literature, suggestions, reporting. Skip
  research-internet if the paper and ModelDB release are already in the corpus; include it if
  supplementary materials need to be sourced.
* Local CPU only. No Vast.ai. Estimate 1-2 days of execution time; MOD compilation on Windows may
  take a non-trivial fraction of that.
* Use absolute imports and centralised `paths.py` / `constants.py` per the project's Python style
  guide.

## Anticipated Risks

* **ModelDB 189347 may reference a morphology file not in t0005**: audit carefully; if the paper
  used a different morphology from t0005, flag and either fetch the paper's morphology or document
  the substitution as a reproduction bug.
* **MOD file compilation on Windows NEURON 8.2.7**: some MOD files in older ModelDB releases need
  minor adjustments to compile under modern NEURON. Record every adjustment as a potential
  discrepancy.
* **Supplementary materials may not exist**: if Poleg-Polsky & Diamond 2016 has no supplementary,
  note this in the audit and proceed with paper + code only.
* **Peak firing rate may still fall short** in the faithful reproduction. If so, the primary finding
  is that the original model produces ~15 Hz and the 40-80 Hz band may be a paper misstatement or a
  stimulus-protocol difference (not a channel-inventory problem in our ports). This would partly or
  fully invalidate the motivation for t0043 and similar modification tasks.

## Relationship to Other Tasks

* **Blocks**: t0042, t0043, t0044 should remain `intervention_blocked` until this task completes. If
  t0046 shows the peak-rate gap is inherent to the faithful model (not a modification artefact), the
  case for t0043 evaporates. If t0046 matches the paper's firing rates, t0043's peak-rate motivation
  becomes strong.
* **Complements**: t0008 (initial port) and t0020 (gabaMOD protocol fix) remain in the history as
  partial reproductions. This task does not modify them; it produces an independent, more complete
  reproduction.
* **Precedes**: any future optimisation task (t0033 style) should use this library asset as the
  starting point rather than t0022 or t0024 derivatives.

## Verification Criteria

* `verify_task_file.py` passes with 0 errors.
* `verify_library_asset.py` passes for `modeldb_189347_dsgc_exact`.
* `verify_answer_asset` (or the relevant answer-spec verificator) passes for
  `poleg-polsky-2016-reproduction-audit`.
* All pass criteria above met: DSI +/-0.05, firing rates +/-10%, basic parameters exact.
* Every paper test attempted is represented in the test reproduction table with a match / no- match
  verdict and numerical evidence.
