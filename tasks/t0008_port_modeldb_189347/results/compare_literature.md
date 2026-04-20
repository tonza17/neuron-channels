---
spec_version: "1"
task_id: "t0008_port_modeldb_189347"
date_compared: "2026-04-20"
---
# Comparison with Published Results

## Summary

This reproduction of the Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC compartmental model (ModelDB
189347\) is **mechanically faithful but scientifically off-target**: the ported cell achieves a DSI
of **0.316** and preferred-direction peak of **18.1 Hz**, far below the **DSI approx 0.7-0.85** and
peak **40-80 Hz** commonly reported for mouse ON-OFF DSGCs. Null-rate **9.4 Hz** (PASS under the <
10 Hz ceiling) and HWHM **82.81 deg** (PASS within 60-90 deg) meet the envelope, but only because
the tuning curve is shallow rather than sharp. The root cause is a protocol mismatch: Poleg-Polsky
2016 implements direction selectivity by swapping a per-angle `gabaMOD` parameter (**0.33 ->
0.99**), whereas this task used a spatial-rotation-of-the-bar proxy while holding `gabaMOD` fixed.

## Comparison Table

| Method / Paper | Metric | Published Value | Our Value | Delta | Notes |
| --- | --- | --- | --- | --- | --- |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1G/4F/5G/6G/8E] | DSI (median, noise-free control, spike output) | ~**0.8** (qualitative, boxplot median) | **0.316** | -0.48 | Paper reports DSI as median+/-quartile boxplots without a single aggregate number; qualitative headline value taken from Figures 1G/4F/5G/6G/8E. Our protocol is a spatial-rotation proxy, not the paper's `gabaMOD` swap. |
| Poleg-Polsky 2016 [PolegPolsky2016, Experimental Procedures] | Preferred-direction peak firing rate (Hz) | not reported | **18.1** | n/a | Paper does not report a numeric peak firing rate anywhere in text or figures (see research_papers.md Gaps). The 40-80 Hz project envelope is drawn from broader DSGC literature, not reproduced from this paper. |
| Poleg-Polsky 2016 [PolegPolsky2016, Experimental Procedures] | HWHM (deg) | not reported | **82.81** | n/a | Paper does not report a tuning-curve half-width-at-half-maximum. Our value passes the 60-90 deg project envelope ceiling but is wide because the tuning curve is shallow. |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1D] | PD NMDAR-mediated PSP component (mV) | **5.8+/-3.1** (n=19, p=0.001) | not measured | n/a | Subthreshold validation target; not extracted in this task (the sweep uses spike output only). Listed to document the paper's quantitative hooks we did not reproduce. |
| Poleg-Polsky 2016 [PolegPolsky2016, Fig 1H] | NMDAR multiplicative scaling slope (deg) | **62.5+/-14.2** (multiplicative vs 45 deg additive) | not measured | n/a | Subthreshold validation; not extracted. |
| Schachter 2010 [Schachter2010, Figs 3-4] | DSI amplification (PSP -> spike output, rabbit active dendrites) | 0.2 -> ~**0.8** | 0.316 (mouse passive, our port) | n/a | Rabbit ON-OFF with active dendrites; different species and simulator (NeuronC). Direct numeric comparison invalid; we only match the passive-dendrite subset of their mouse counterpart. |
| Oesch 2005 [Oesch2005, Fig 2] | Rabbit DSGC somatic spike amplitude (mV) | **~55** | not measured | n/a | Electrophysiology target, not a reproducible-from-our-port metric (the port uses spike-count detection at a -10 mV threshold, not peak amplitude). Listed for completeness. |
| Hanson 2019 [Hanson2019 / Geoffder-offsetDSGC-2019] | PD-ND synaptic onset offset at moderate bar speed (ms) | up to **50** | not measured | n/a | Our protocol does not resolve E/I synaptic onset timing per angle; `geoffder/Spatial-Offset-DSGC-NEURON-Model` uses a different weight set (inhibWeight=0.004 uS, nmdaWeight=0.0015 uS) and `tstop = 750` ms. Hanson 2019 port is deferred to `S-0008-01`. |
| Jain 2020 [Jain2020-eLife, Fig 4] | Ca2+ subunit diameter (um) | **5-10** | not measured | n/a | Jain 2020's architecture is Poleg-Polsky 2016 base + Ca2+ subunit mechanism; our port does not include the CaV channel. Relevant as a mechanism gap rather than an architecture gap. |
| Project envelope target (t0004, this project) | DSI | **0.7-0.85** | 0.316 | -0.48 | Project-specific envelope built from literature consensus, not a single paper number. FAIL on this axis. |
| Project envelope target (t0004, this project) | Peak rate (Hz) | **40-80** | 18.1 | -21.9 (vs lower bound) | Project envelope; Poleg-Polsky 2016 does not supply this number. FAIL on this axis. |
| Project envelope target (t0004, this project) | Null rate (Hz) | **< 10** | 9.4 | +7.4 vs 2 Hz target-mean | PASS the ceiling by 0.6 Hz; passes weakly because the ceiling is permissive, not because ND firing is actively suppressed. |
| Project envelope target (t0004, this project) | HWHM (deg) | **60-90** | 82.81 | +16.81 vs 66 deg target-mean | PASS, but the wide half-width is a symptom of shallow tuning (low DSI), not an independent success. |
| Project envelope target (t0004, this project) | Trial reliability | **> 0.9** | **0.991** | +0.091 | PASS. Trial-to-trial variance is well below the ceiling; the seeding protocol is clean. |

### Prior Task Comparison

The plan cites the **t0004 canonical target curve** as the reference the t0012 scoring library
resolves by default. The target curve encodes peak **32.0 Hz**, null **2.0 Hz**, DSI **0.882**, HWHM
**66.0 deg**; our reproduced curve deviates by delta-DSI **-0.566**, delta-peak **-13.9 Hz**,
delta-null **+7.4 Hz**, and delta-HWHM **+16.81 deg**. The null residual is the clearest prior-task
contradiction: t0004's literature-consensus ND is 2 Hz, and our port produces ~4.2x that. The plan's
hypothesis (envelope compliance would survive the calibrated morphology swap per [ElQuessny2021]) is
**not refuted** by this task because we did not execute the swap into the sweep itself; REQ-4 is
only partially satisfied and the test is deferred to `S-0008-03`.

## Methodology Differences

* **Direction-selectivity driver**: Poleg-Polsky 2016 implements DS via a per-angle **`gabaMOD`**
  parameter swap (`0.33` in PD, `0.99` in ND) inside `main.hoc`'s `stim()` procedure
  [PolegPolsky2016, PolegPolsky2016-mainhoc-2016]. Our `run_tuning_curve.py` **rotated the bar
  through a fixed synapse field** while keeping `gabaMOD` constant. This is the dominant gap and the
  single largest contributor to DSI 0.316 vs ~0.8.
* **Stimulus direction count**: Paper uses **8 directions at 45 deg spacing** (noise-free and
  noisy). This task used **12 directions at 30 deg spacing** to support HWHM estimation with the
  t0012 scoring library's angular resolution requirement.
* **Bar speed**: Paper / `main.hoc` use `lightspeed = 1 um/ms` (= 1000 um/s). This task used **500
  um/ms** per the task description — a pre-declared divergence recorded in Limitations.
* **Simulation timestep, stopping time, and passive parameters**: **Identical** — `tstop = 1000 ms`,
  `dt = 0.1 ms`, `tau1NMDA_bipNMDA = 60 ms`, `e_SACinhib = -60 mV`, 177 AMPA + 177 NMDA + 177 GABA
  synapses, passive dendrites, Jahr-Stevens NMDA Mg2+ block (all read verbatim from `main.hoc` and
  `RGCmodel.hoc`).
* **Morphology**: Paper uses a single reconstructed mouse DRD4 DSGC bundled with 189347. This task
  **kept the bundled morphology for the sweep** (because `RGCmodel.hoc`'s `placeBIP()` synapse
  placement is section-ordering-dependent); the calibrated t0009 SWC was measured and compared in
  `data/morphology_swap_report.md` but not substituted into the simulation. Full swap deferred to
  `S-0008-03`.
* **Trial count**: Paper uses n = **25 / 21 / 34** cells (control / AP5 / 0 Mg2+) as biological
  replicates. This task uses **20 seeded trials per angle** as computational replicates — not
  directly comparable at the cell-level but above the 10-trial floor implied by the DSGC literature
  [Jain2020, Hanson2019].
* **Simulator and stack**: Paper uses NEURON (unspecified version). This task uses **NEURON 8.2.7 +
  NetPyNE 1.1.1** on Windows 11 + Python 3.13. MOD files compiled without any manual edits (the
  documented NEURON 8.2 implicit-declaration collision did not materialise).
* **Output metric**: Paper reports DSI as **median+/-quartile boxplots** across cells. This task
  reports DSI as the **vector-sum DSI** computed by the t0012 scoring library on the mean tuning
  curve (also **0.366** by the raw `(PD-ND)/(PD+ND)` definition on our data — both agree the port is
  under-selective).
* **Sibling methods not tried (mechanism gaps)**:
  * **Hanson 2019 native weights** (`inhibWeight = 0.004 uS`, `nmdaWeight = 0.0015 uS`,
    `tstop = 750 ms`, spatial E/I offset) — `S-0008-01` follow-up.
  * **Jain 2020 Ca2+ subunit mechanism** — no separate port required (architecture is identical to
    Poleg-Polsky); mechanism gap captured but not bridged in this task.
  * **Schachter 2010 active dendrites** (rabbit) — simulator is NeuronC, not NEURON; **not
    portable** within this stack per research findings.
  * **Ding 2016** — SAC network in NeuronC; not portable within this stack.
  * **Koren 2017** — no standalone NEURON DSGC model deposited; no repository located.

## Analysis

**The headline number (DSI 0.316) is not a port-fidelity failure.** MOD files compiled clean, the
HOC template instantiates verbatim, the morphology-swap report confirms structural parity, and the
scoring library passes its identity gate (`score(TARGET_MEAN_CSV).loss_scalar == 0.0`). The low DSI
is a **protocol mismatch**: Poleg-Polsky 2016's cell is architecturally agnostic to the bar's
direction — direction selectivity is injected by the `gabaMOD` swap inside `main.hoc`'s `stim()`
procedure, not by the geometry of the stimulus against the synapse field. A spatial-rotation proxy
therefore recovers only the residual direction sensitivity baked into the dendritic asymmetry (about
**1/3** of the paper's headline DSI, which is consistent with the ~0.2 PSP-level DSI measured by
Oesch 2005 before active-dendrite amplification).

**The shallow-tuning signature is visible across every axis**. Peak rate (18.1 Hz) sits **21.9 Hz
below** the envelope floor; ND rate (9.4 Hz) sits **7.4 Hz above** the t0004 target mean even though
it squeaks under the 10 Hz ceiling; HWHM (82.81 deg) widens precisely because the modulation depth
is small. This means three of the four envelope axes are telling the same story. The HWHM and null
PASSES are not independent successes — they are side-effects of the failing DSI and peak axes.

**What the comparison says about closing the gap**:

* **First fix (highest expected yield)**: replace rotation with native `gabaMOD` swap per
  [PolegPolsky2016, main.hoc] — captured as `S-0008-02`. Expected to move DSI from 0.316 into the
  paper's ~0.8 regime and peak rate toward the paper's implicit 32-40 Hz range.
* **Second fix (targeted re-tuning)**: if the native-protocol reproduction misses the **40-80 Hz**
  project envelope after morphology swap, apply **Hanson 2019 weights** from
  `geoffder/Spatial-Offset-DSGC-NEURON-Model` (inhibWeight=0.004 uS, nmdaWeight=0.0015 uS) — the
  Hanson 2019 re-tuning targeted a contemporary experimental dataset with explicit spike-rate
  targets and is the literature's nearest example of the same architecture hitting the project's
  firing-rate band.
* **Mechanism extension (stretch)**: incorporate **Jain 2020** Ca2+ subunit dynamics for the
  separate question of subcellular DS localisation (5-10 um subunits); not a route to closing the
  Phase A envelope gap but a logical next step once the baseline reproduction is correct.
* **Active-dendrite contrast (out of scope)**: **Schachter 2010** and **Oesch 2005** predict that
  adding dendritic Nav/Kv amplifies DSI from ~0.2 (PSP) to ~0.8 (spike output) in rabbit; this
  project's mouse DRD4 DSGC should not replicate this (passive dendrites are sufficient per
  [PolegPolsky2016]), but the literature contrast is important context for answering RQ4 (active vs
  passive dendrites) in later tasks.

**What the comparison does NOT tell us**: we cannot compare our port's subthreshold PSP amplitudes
(NMDAR-mediated PD component **5.8+/-3.1 mV**, slope **62.5 deg**) to [PolegPolsky2016, Fig 1D-H]
because this task only extracted spike output. A subthreshold validation sweep is a natural
follow-up and would strengthen the fidelity claim independent of the `gabaMOD` protocol question.

## Limitations

* **No single published numeric DSI for Poleg-Polsky 2016 control condition**. Every DSI reference
  in [PolegPolsky2016] is a median+/-quartile boxplot or a qualitative statement ("DSI preserved",
  "DSI reduced"). The ~0.8 headline we compare against is the research_papers.md qualitative reading
  of Figures 1G/4F/5G/6G/8E, not a verbatim paper number. Our -0.48 delta should be read "relative
  to the boxplot median visible in the paper's figures".
* **Peak firing rate and HWHM are not reported** in [PolegPolsky2016] anywhere in text or figures
  (research_papers.md Gaps). The 40-80 Hz peak / 60-90 deg HWHM envelope is a **project target**
  derived from literature consensus (t0004), not a paper-reproduction target. The "FAIL" verdict on
  peak and the "PASS" on HWHM are relative to the project envelope, not to a single paper.
* **PMC author-manuscript XML truncates Experimental Procedures** (Ri, Rm, Cm, Nav/Kv densities,
  synaptic decay constants) in [PolegPolsky2016]. We read these from the ModelDB 189347 source as
  the canonical reference, not from the paper prose.
* **Direct numeric comparison to Schachter 2010, Oesch 2005, Ding 2016, Koren 2017 is invalid by
  construction**: different species (rabbit vs mouse), different simulators (NeuronC vs NEURON for
  Schachter / Ding), different cell types (SAC network in Ding / Koren). These papers appear in the
  table as mechanism context, not as head-to-head comparisons.
* **Hanson 2019 and Jain 2020 comparisons are architecture-identical but weights-different**: they
  would produce numerically different tuning curves on the same Poleg-Polsky 2016 cell, and any
  direct reproduction of their published numbers requires porting their weight sets, not their
  architectures. Jain 2020's Ca2+ subunit mechanism is also mechanism-new relative to 189347.
  Attempting either comparison is deferred to `S-0008-01`.
* **Subthreshold metrics not measured**. [PolegPolsky2016, Fig 1D-H] provides PD NMDAR PSP component
  **5.8+/-3.1 mV**, ND **3.3+/-2.8 mV**, slope **62.5+/-14.2 deg** as concrete numeric validation
  targets. This task did not extract subthreshold traces; the comparison table lists them as "not
  measured" to document the gap.
* **The envelope PASS on null rate (9.4 vs < 10 Hz ceiling) and HWHM (82.81 vs 60-90 deg band) are
  coupled artifacts of the shallow tuning curve**, not independent confirmations of correctness.
  Reading them as three independent pass/fail axes (as the scoring library does) over-counts the
  evidence for fidelity.
* **Morphology swap not executed in the sweep** (REQ-4 is Partial). Whether the calibrated
  morphology from t0009 preserves or shifts envelope compliance is an open question captured as
  `S-0008-03` — it cannot be answered with this task's data.
