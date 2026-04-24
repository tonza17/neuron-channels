---
spec_version: "1"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
research_stage: "papers"
papers_reviewed: 16
papers_cited: 14
categories_consulted:
  - "compartmental-modeling"
  - "direction-selectivity"
  - "dendritic-computation"
  - "retinal-ganglion-cell"
  - "synaptic-integration"
  - "voltage-gated-channels"
  - "patch-clamp"
date_completed: "2026-04-24"
status: "complete"
---
# Research: Exact Reproduction of Poleg-Polsky and Diamond 2016 (ModelDB 189347)

## Task Objective

This task builds a fresh, from-scratch port of ModelDB 189347 (the compartmental DSGC model
described by [PolegPolsky2016]) and audits every parameter against the paper, the ModelDB code, and
the supplementary materials. The port must reproduce **every** test the paper runs - not only the
headline DSI/tuning curve that prior ports t0008 and t0020 targeted - within tight tolerance (DSI
+/-0.05, firing rates +/-10%). The research stage's job is to enumerate all those tests with
specific quantitative anchors and to gather the published DSI and firing-rate targets from sibling
DSGC papers that inform interpretation (e.g., Oesch 2005, Schachter 2010, Sivyer 2013, Hanson 2019,
Park 2014, Taylor 2002, Hausselt 2007).

## Category Selection Rationale

The seven consulted categories span the methodological and biological scope of the reproduction.
`compartmental-modeling` is the methodology itself - every DSGC model paper lives here.
`direction-selectivity` is the functional property being reproduced. `dendritic-computation` covers
dendritic spikes, NMDAR nonlinearity, and passive-versus-active debates that distinguish the
Poleg-Polsky mouse model from rabbit DSGC models. `retinal-ganglion-cell` narrows to the target cell
class. `synaptic-integration` covers AMPA, NMDA, GABA, and cholinergic wiring.
`voltage-gated-channels` matters because the reproduction audits channel densities (HHst Nav and Kv
per compartment class). `patch-clamp` is included because the paper's validation anchors are
patch-clamp measurements. Excluded `cable-theory` as a standalone filter - the reproduction is
code-driven rather than theory-driven - though cable ideas enter via the dendritic-computation and
voltage-gated-channels tags.

## Key Findings

### Enumeration of Every Test and Figure in PolegPolsky2016

This is the critical input for planning. The paper reports eight main figures plus eight
supplementary figures, each running a distinct experimental or simulation test. The reproduction
must produce one result row per item.

* **Figure 1 - Multiplicative NMDAR scaling (main result)**. Whole-cell subthreshold PSPs in control
  vs. AP5, 8 directions, bar at 1 mm/sec, n = 19 cells. Quantitative anchors: AP5-sensitive (NMDAR)
  PD PSP = **5.8 +/- 3.1 mV**, ND = **3.3 +/- 2.8 mV** (p = 0.001, paired t-test)
  [PolegPolsky2016, Figure 1D, main text]; AP5 reduces PD PSP by **~35%** and ND PSP by **~34%**
  (Figure 1E,F); slope of NMDAR scaling = **62.5 +/- 14.2 deg** vs. expected multiplicative **59.4
  +/- 10.7 deg** (p = 0.4, paired t-test; Figure 1H) [PolegPolsky2016, main text]. DSI unchanged by
  AP5 (Figure 1G, p > 0.5 paired Wilcoxon).

* **Figure 2 - Postsynaptic locus of multiplication (iMK801 control)**. Intracellular MK801 (2 mM)
  dialysis; subsequent bath AP5, n = 15 cells. Quantitative anchors: iMK801 reduces PSPs
  significantly (p < 0.001); subsequent bath AP5 further reduces PD PSP by only **16 +/- 17%**
  [PolegPolsky2016, Figure 2B, main text]. DSI preserved across iMK801 and AP5. EPSC reduction under
  AP5-after-iMK801 = **8 +/- 12%** (p = 0.25, n = 6; Figure S5).

* **Figure 3 - NEURON model of DS signaling (the model the reproduction must rebuild)**.
  Morphologically realistic reconstructed DSGC; **282 presynaptic cells** with vesicle release,
  homogeneous synapse distribution on ON dendrites only
  [PolegPolsky2016, Experimental Procedures, main text]. Each synaptic site carries GABA_A +
  nicotinic AChR (SAC-like) + AMPA + NMDA (bipolar-like). DS imposed by stronger inhibitory drive in
  ND. Tests: PD vs. ND simulated PSPs with **gNMDA = 2.5 nS** (blue) and **gNMDA = 0 nS** (black),
  Figure 3E; DSI as function of gNMDA, Figure 3F; alternative tuned-excitation scheme, Figure 3G-I,
  predicts additive NMDAR scaling. The model also reports simulated AP responses (Figure 3B) and
  synaptic conductance traces (Figure 3C).

* **Figure 4 - Tuned-excitation analogue (high-Cl- internal)**. Intracellular chloride = 65 mM
  reverses GABA_A drive from inhibitory to excitatory (E_Cl ~ -20 mV); n = 12 cells. Quantitative
  anchors: PD' - ND' difference = **14.1 +/- 4.7 vs. 11.9 +/- 4.8 mV** (p = 0.003, paired t-test);
  DS reversed to new PD in 15/20 cells [PolegPolsky2016, Figure 4D,E]; NMDAR scaling slope = **45.5
  +/- 3.7 deg** (additive, p = 0.01 vs. multiplicative; Figure 4G inset); DSI significantly reduced
  by AP5 (p = 0.03, Wilcoxon with Bonferroni; Figure 4F inset).

* **Figure 5 - Voltage-dependent NMDAR requirement (0 Mg++)**. Extracellular Mg++ removed, n = 8
  cells. Quantitative anchors: DSI reduced but PD vs. ND still different (p = 0.01, paired t-test;
  Figure 5F); NMDAR scaling slope = **45.5 +/- 5.3 deg** (additive, p < 0.001 vs. multiplicative;
  Figure 5G inset). Parallel simulation: Ohmic (voltage-independent) NMDAR substitute in the model
  also produces additive scaling (Figure 5B,C; Figure S7).

* **Figure 6 - DSGC responses to noisy visual stimulation (subthreshold)**. Bar luminance and
  background luminance each vary independently every **50 ms** with SD = **0%, 10%, 30%, 50%** of
  mean; n = 12 cells. Resting V_m in 0 Mg++ = control **+3.4 +/- 3.6 mV** (Figure 6C,D). PD PSP
  amplitude not different between control and 0 Mg++ (p = 0.8, paired t-test, n = 12; Figure 6F). ND
  PSPs consistently larger in 0 Mg++. DSI reduced by noise in all conditions; reduction strongest in
  0 Mg++ (Figure 6G).

* **Figure 7 - ROC / accuracy analysis (subthreshold)**. Noise-free ROC AUC for PD vs. baseline:
  control **0.99**, AP5 **0.98**, 0 Mg++ **0.83** (p = 0.008, Wilcoxon with Bonferroni, n = 12;
  Figure 7C,D) [PolegPolsky2016, main text]. ROC AUC falls with noise; Mg++-free significantly lower
  than control up to **50%** stimulus variability. Accuracy-curve area significantly larger in
  control than in AP5 or 0 Mg++ (Figure 7E,F).

* **Figure 8 - Suprathreshold AP responses**. Cell-attached spike recording, 0 Mg++ (n = 34),
  control (n = 25), AP5 (n = 21). Control DSI preserved under AP5; DSI significantly reduced in 0
  Mg++ (p < 0.001, ANOVA + Tukey; Figure 8E). Baseline firing elevated in 0 Mg++ (Figure 8A,C). PD
  spike count unchanged in 0 Mg++ (p = 0.3); ND spike count increased in 0 Mg++ (p = 0.04; Figure
  8D). **AP5 increases PD-stimulus failure rate** (Figure 8F). ROC/accuracy analyses on APs (Figure
  8G-J) reproduce the PSP ROC picture: control outperforms AP5 and 0 Mg++ under noise.

* **Supplementary Figure S1** - Extended AP and EPSC/IPSC directional tuning; DSI of AP responses >>
  PSP DSI (Wilcoxon p < 1e-8, n = 33).

* **Supplementary Figure S2** - Conditions suitable for multiplicative scaling analysis (slope-angle
  interpretation under different baseline PSP geometries).

* **Supplementary Figure S3** - NMDAR multiplication across contrast levels (preserved across tested
  contrasts).

* **Supplementary Figure S4** - NMDAR multiplication across developmental ages (P14-P70).

* **Supplementary Figure S5** - iMK801 control on voltage-clamped EPSCs and IPSCs (bath AP5 after
  iMK801 does not change EPSCs or IPSCs).

* **Supplementary Figure S6** - SACs do not receive NMDAR-mediated input (AP5 does not affect SAC
  PSPs).

* **Supplementary Figure S7** - Scaling additivity is independent of Ohmic conductance time course.

* **Supplementary Figure S8** - Conceptual single-compartment model explaining how ideal-current,
  Ohmic, NMDAR, and tuned-excitation schemes map to multiplicative vs. additive scaling.

Note: [PolegPolsky2016] reports these results with **8 stimulus directions at 45 deg spacing** (bar
at 1 mm/sec), not 12 directions. Prior project ports imposed a 12-direction protocol on top; for
exact reproduction, the 8-direction protocol is the paper's own test and must be replicated.

### What the Paper Does Not Report Numerically

[PolegPolsky2016] never reports a single **peak firing rate in Hz** for PD stimulation, nor an
aggregate DSI numeric for the control condition (uses box plots of median +/- quartile in Figures
1G, 4F, 5G, 6G, 8E). The paper does not report an aggregate **HWHM** (half-width at half max of the
tuning curve). It also does not specify explicit passive membrane parameters (V_rest, Ra, Rm, Cm),
channel densities (somatic/dendritic gbar for HHst Na/K), synaptic kinetics (tau rise/decay for
AMPA, NMDA, GABA), or the number of segments per compartment in the main text or the
(author-manuscript PMC XML) Experimental Procedures, which is truncated. These values must be read
from the ModelDB 189347 source files during the reproduction and treated as canonical for any
paper-vs-code audit. "Not found in paper" applies to: peak PD Hz, aggregate DSI numeric, HWHM,
V_rest, Ra, Rm, Cm, all channel gbar densities, all synaptic kinetics. Prior project ports (t0008,
t0020) both observed peak firing rate **~15 Hz** vs. the project envelope 40-80 Hz - that envelope
comes from a broader DSGC literature (e.g., [Oesch2005]) rather than the paper itself.

### Published DSI and Firing-Rate Targets from Sibling DSGC Papers

The 40-80 Hz peak-rate expectation propagated through this project comes from rabbit DSGC in vitro
recordings, where species differ from mouse DRD4. Specific anchors:

* Rabbit ON-OFF DSGC spike-based DSI: **0.67 +/- 0.13** (ON arbor) and **0.74 +/- 0.13** (OFF
  arbor); PSP-based DSI is ~6x lower, i.e., ~**0.1-0.13**
  [Oesch2005, Results; PSP DSI values collapsed to 0.04 (ON) and 0.21 (OFF) after bath TTX].

* Rabbit DSGC somatic excitation peak during full-field drift: **~72 spikes/stimulus** at modal rate
  **148 +/- 30 Hz** under current injection mimicking the light-evoked PSP; **41 +/- 47 Hz** under
  somatic current matching the PSP shape alone (p < 0.001) [Oesch2005, Results]. These are rabbit
  numbers.

* Rabbit DSGC modelled PSP DSI ~**0.2** and spike DSI ~**0.8** [Schachter2010, Results] - **6-fold**
  amplification via local dendritic-spike thresholds, achievable only with active dendrites.

* Rabbit DSGC E/I conductance ratios (compound drives during moving bar): PD g_exc ~ **6.5 nS** with
  g_inh ~ **3.5 nS**; ND g_exc ~ **2.5 nS** with g_inh ~ **6.0 nS** [Schachter2010]. On the on-arbor
  alone, ge ratio PD/ND = **1.66 +/- 0.48** and gi ratio null/preferred = **3.31 +/- 2.15**
  [Taylor2002, Results].

* Rabbit DSGC IPSC DSI (wild-type, SAC-driven): **0.33 +/- 0.019**; drops to **0.07 +/- 0.02** when
  SAC-SAC mutual inhibition is abolished (Gabra2 KO + ChR2) [Hanson2019, Results]. Paired E/I
  temporal offsets in PD reach **~50 ms** and collapse in ND (25-30 um spatial offset).

* Rabbit DSGC spike DSI when presynaptic DS is removed drops from **~0.8** to **~0.3-0.4**
  [Schachter2010, Results] - demonstrating that presynaptic DS (SAC-mediated GABA tuning) dominates
  the postsynaptic spatial-offset contribution.

* Mouse bipolar-cell excitation onto DSGC **lacks direction tuning** (iGluSnFR) [Park2014],
  validating PolegPolsky's "tuned inhibition only" architecture. Apparent DS in voltage-clamp EPSCs
  is shown to be a space-clamp artefact.

* Mouse DSGC spike contrast threshold **68 +/- 24%** (n = 43) vs. PSP threshold **45 +/- 25%** (n =
  13\) (p = 0.03, Wilcoxon) [PolegPolsky2016b]. E/I amplitude ratio in DSGCs is contrast-invariant
  (Pearson r = 0.94).

Implication for the reproduction: the 40-80 Hz peak band in the project envelope is a rabbit anchor
rather than a mouse PolegPolsky2016 anchor. The reproduction audit should flag this as a potential
misinterpretation of "target" - the proper mouse target is whatever ModelDB 189347 actually produces
at paper parameters. If that is 15 Hz, t0046 validates the existing ports (t0008, t0020) and
undermines the motivation for peak-rate modifications (t0043).

### Mouse DRD4 DSGC Passive Dendrite Assertion

[PolegPolsky2016] explicitly states: "We did not detect dendritic spikes in DRD4 DSGCs (data not
shown), and our computer simulations did not require regenerative dendritic events to replicate
experimentally recorded PSP and (somatic) AP responses and DSI values, suggesting that passive PSP
propagation to the soma is sufficient." This contrasts with rabbit ON-OFF DSGCs that generate
orthograde dendritic spikes [Oesch2005, Sivyer2013] and with rabbit models that require active
dendrites to hit spike DSI [Schachter2010]. The ModelDB 189347 source must therefore contain HHst
(Hodgkin-Huxley spike-capable) channels in the soma and AIS but minimal dendritic Nav density; the
reproduction audit must document soma/AIS/dendrite gNa and gK per compartment class.

### Morphology, Synapse Counts, and Jeon2002

[PolegPolsky2016] cites [Jeon2002] for the synapse distribution pattern and states "177 AMPAR + 177
NMDAR synapses from bipolar cells and 177 GABA_A synapses from starburst amacrine cells, distributed
homogeneously on ON dendrites only, plus nicotinic AChR inputs" - but the ModelDB 189347 release's
`RGCmodel.hoc` actually yields **countON = 282** triples [prior port t0008]. The reproduction must
determine whether the paper's 177 figure is a text error (not found in code), a subsampling of the
282, or a different cell instance. This is a prime candidate for the paper-vs-code discrepancy
catalogue.

### Best Practices Converged Across the DSGC Model Literature

* Report DSI as **median +/- quartile**, not mean +/- SD - the underlying distribution is
  non-Gaussian [PolegPolsky2016 uses box plots throughout]. Use the same convention in the audit
  output.

* Drive synapses via simulated vesicle release gated on presynaptic membrane potential rather than
  fixed spike trains [PolegPolsky2016 Experimental Procedures].

* Passive dendrites + Jahr-Stevens Mg++ block suffice for mouse DRD4 DSGC; do not add dendritic
  active conductances unless explicitly porting a rabbit model
  [PolegPolsky2016, Oesch2005, Schachter2010].

* Stimulus is **1 mm/sec bright bar in 8 directions**; 1-D bar traversal is the canonical protocol
  [PolegPolsky2016, Experimental Procedures]. 12-direction sweeps (used in t0008 for envelope
  scoring) are not part of the paper.

* Voltage-clamp EPSC measurements in DSGCs appear directionally tuned but are a space-clamp artefact
  [Park2014, PolegPolsky2011] - any "tuned excitation" target in the model must be rejected unless
  it comes from iGluSnFR or iMK801 controls.

## Methodology Insights

* **Enumerate every paper test before implementation.** The test list above (8 main + 8
  supplementary figures) becomes the row schema for the audit answer asset. Each row reports paper
  value, ModelDB code value, reproduction value, tolerance, match verdict, and the figure reference
  [PolegPolsky2016 Figure 1-8, S1-S8].

* **Treat the ModelDB code as canonical for parameters the paper does not specify.** The author-
  manuscript XML available in the corpus truncates Experimental Procedures - V_rest, Ra, Rm, Cm,
  channel gbar, synaptic kinetics, and segment counts must be read from the `HHst.mod`,
  `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`, `bipolarNMDA.mod`, `SquareInput.mod`, `spike.mod`,
  `RGCmodel.hoc`, and `main.hoc` files. This is consistent with the researcher directive in
  task_description.md: "the primary reproduction follows their code".

* **Reproduce the paper's protocol exactly, not the project's 12-angle scoring protocol.** Use 8
  directions at 45 deg spacing and 1 mm/sec bar. Use the native `gabaMOD` swap pipeline already
  validated in t0020 for the DS test (PD gabaMOD=0.33, ND gabaMOD=0.99) rather than the rotation
  proxy of t0008 [t0020 library description].

* **Log AP5 and 0 Mg++ as parameter flips.** For Figure 1, simulate with gNMDA=0 vs. gNMDA=2.5 nS
  (AP5 vs. control). For Figure 5, simulate with voltage-dependent NMDAR vs. Ohmic substitute
  [PolegPolsky2016 Figure 3E, 5B]. For Figure 4, flip E_GABA from -60 mV to -20 mV and set
  inhibition to zero (high-Cl- analogue) [PolegPolsky2016 Figure 4A]. All are single-parameter
  toggles and should live in `constants.py` with named flags.

* **Run noise-free stimuli first, noisy next.** The paper's Figures 6-8 add stimulus-luminance noise
  with SD = 0/10/30/50% of mean. Implement noise as per-50-ms frame luminance perturbations to the
  SquareInput/bar stimulus in the MOD files. Match the ROC/accuracy pipeline used by the paper; the
  python library `sklearn.metrics.roc_auc_score` will suffice for median AUC.

* **Report all subthreshold validation anchors in the audit.** Not just DSI and peak Hz: also
  NMDAR-mediated PD PSP (target **5.8 +/- 3.1 mV**), ND PSP (**3.3 +/- 2.8 mV**), slope angle
  (target **62.5 +/- 14.2 deg** for multiplicative, **45.5 +/- 3.7 deg** for high-Cl-, **45.5 +/-
  5.3 deg** for 0 Mg++), ROC AUC (**0.99 / 0.98 / 0.83** for control/AP5/0 Mg++ noise-free PD vs.
  baseline), and PD-failure rate under AP5 [PolegPolsky2016 Figures 1D-H, 4G, 5G, 7C, 8F].

* **Hypothesis (testable this task)**: If the faithful ModelDB 189347 port produces peak PD firing
  rate ~15 Hz (matching t0008 and t0020), the 40-80 Hz envelope is a literature-import error from
  rabbit [Oesch2005, Schachter2010] rather than a PolegPolsky2016 target. This invalidates the
  peak-rate motivation for t0043 and t0044 modification tasks.

* **Hypothesis (testable this task)**: The paper's "177 AMPA + 177 NMDA + 177 GABA" figure is a text
  error inconsistent with the ModelDB code's `countON = 282`. If confirmed by code inspection, this
  is the first paper-vs-code discrepancy to catalogue.

* **Best practice**: Pin the ModelDB release hash in the library description. t0008 used
  `87d669dcef18e9966e29c88520ede78bc16d36ff`; the reproduction should verify this is the same commit
  the paper cites (or flag the delta).

## Gaps and Limitations

* **Supplementary Experimental Procedures are missing from the corpus**. The author-manuscript XML
  file in the corpus
  (`tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/files/poleg-polsky_2016_nmda-dsgc-multiplicative.xml`)
  contains the main text, main figures' captions, and reference list, but **not** the Supplementary
  Experimental Procedures document. This is where V_rest, Ra, Rm, Cm, channel densities, and
  synaptic kinetics would be stated explicitly. The research-internet stage must attempt to download
  the supplementary PDF from the Cell/Neuron publisher; if unavailable, the reproduction proceeds
  from ModelDB code alone and every such parameter is flagged in the audit as "paper reference:
  Supplementary Procedures, not available".

* **ModelDB 189347 release version**. The paper cites the code but does not specify a release
  version or commit. t0008 pinned `87d669dcef18e9966e29c88520ede78bc16d36ff`. This reproduction
  needs to verify that the pinned commit is the version cited in the paper's Figure 3 caption or
  Supplementary Procedures (if that exists).

* **No aggregate numeric values for DSI, peak Hz, HWHM, or baseline firing rate in noise-free
  control**. The paper's Figures 1G, 6G, 8E display median +/- quartile boxplots; exact numeric
  medians are not printed in the main text or figure captions (as available in the corpus XML). The
  reproduction audit must re-extract these from the ModelDB code output rather than from the paper,
  which limits the definitiveness of any paper-vs-reproduction numerical claim.

* **No published ROC AUC CIs under noise levels 10%, 30%**. Figure 7D shows box plots at each noise
  level; only the noise-free AUCs (0.99 / 0.98 / 0.83) are stated numerically in the main text.
  Tolerance bands for noisy conditions must be read off Figure 7D panels; the reproduction audit
  will need to digitise the boxplots or record "visual-inspection match" rather than a tight numeric
  tolerance.

* **Passive-vs-active dendrite test is asymmetric**. The paper shows passive suffices but does not
  run a matched active-dendrite control [PolegPolsky2016 Discussion]. There is therefore no
  quantitative paper target for "what happens if you add Nav to the dendrites" in the mouse model.
  Sivyer2013 and Schachter2010 provide rabbit equivalents but the species gap means those cannot
  anchor a mouse audit.

* **Mouse DRD4 vs. rabbit conflation in the project's peak-rate envelope**. The 40-80 Hz peak target
  carried into t0012 and t0022 has never been attributed to a specific PolegPolsky2016 claim; it
  traces back to rabbit DSGC literature [Oesch2005]. This reproduction is the first task positioned
  to resolve whether the target is mislabeled.

* **Stafford 2014 (NMDAR subunit composition across development)** is cited by [PolegPolsky2016, S4]
  but is not in the project corpus. If the reproduction needs to parameterise NMDAR subunit
  composition for the developmental age comparison (Figure S4), it will need to fetch this or record
  the gap.

## Recommendations for This Task

1. **Enumerate the 8 main + 8 supplementary figure tests as audit rows before writing code.** Use
   the list in "Enumeration of Every Test and Figure in PolegPolsky2016" above as the row schema for
   the answer asset's test reproduction table.

2. **Attempt to fetch Supplementary Experimental Procedures via research-internet**, since the
   corpus XML omits them. If not available, proceed from ModelDB code and mark every missing
   parameter as "paper reference unavailable; code value canonical".

3. **Read V_rest, Ra, Rm, Cm, and every channel gbar from ModelDB 189347 `.mod` and `.hoc` files**.
   These are the audit's canonical paper-vs-code column. Cross-check against any residual paper
   mention in Experimental Procedures text.

4. **Use the gabaMOD swap protocol (PD = 0.33, ND = 0.99) as the primary DS test**, following the
   native paper pipeline validated in t0020, not the rotation proxy from t0008.

5. **Simulate the paper's Figure 3 / 4 / 5 parameter flips as distinct simulation runs**: control
   (gNMDA = 2.5 nS, Mg++ block on, E_GABA = -60 mV), AP5 (gNMDA = 0), 0 Mg++ (Mg++ block off),
   high-Cl- (E_GABA = -20 mV, inhibition zeroed), Ohmic NMDAR (voltage-independent substitute). Each
   yields a row in the test reproduction table.

6. **Report peak PD firing rate without assuming the 40-80 Hz target**. If the reproduction lands at
   ~15 Hz, this is the scientific finding of the task; the 40-80 Hz envelope came from rabbit
   literature, not PolegPolsky2016. Document this clearly in the audit summary paragraph.

7. **Implement stimulus-luminance noise (Figure 6-8)** as per-50-ms luminance perturbations at SD =
   0/10/30/50% of mean, then run ROC and accuracy pipelines to match Figure 7, 8.

8. **Compare mouse DRD4 DSGC results to rabbit anchors only as context, never as reproduction
   targets**. [Oesch2005, Schachter2010, Sivyer2013, Hanson2019] are rabbit or differ in circuit
   manipulations; they bound the plausibility range but do not set tolerances for the paper- vs-code
   match.

9. **Document the "177 vs. 282 synapses" paper-vs-code discrepancy explicitly** in the audit, given
   that the paper says 177 but the code yields 282.

## Paper Index

### [PolegPolsky2016]

* **Title**: NMDA Receptors Multiplicatively Scale Visual Signals and Enhance Directional Motion
  Discrimination in Retinal Ganglion Cells
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1016/j.neuron.2016.02.013`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `synaptic-integration`,
  `dendritic-computation`, `retinal-ganglion-cell`
* **Relevance**: The paper being reproduced. Defines every test, parameter, figure, and quantitative
  anchor this task must match. ModelDB 189347 is the code repository accompanying this paper.

### [PolegPolsky2016b]

* **Title**: Retinal Circuitry Balances Contrast Tuning of Excitation and Inhibition to Enable
  Reliable Computation of Direction Selectivity
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1523/JNEUROSCI.4013-15.2016`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1523_JNEUROSCI.4013-15.2016/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `synaptic-integration`,
  `retinal-ganglion-cell`
* **Relevance**: Second Poleg-Polsky 2016 paper. Provides DSGC contrast-threshold anchors (spike
  threshold 68 +/- 24%, PSP threshold 45 +/- 25%) and DSGC E/I contrast invariance (Pearson r =
  0.94), context for stimulus contrast choices in the reproduction.

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`
* **Relevance**: Rabbit spike DSI (0.67-0.74) and peak firing rates (148 +/- 30 Hz modal, 41 +/- 47
  Hz from PSP-shaped injection) anchor the high-firing-rate band that the project's 40-80 Hz peak
  envelope drew from. Establishes that the 40-80 Hz number is a rabbit anchor, not a PolegPolsky2016
  anchor.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `voltage-gated-channels`, `retinal-ganglion-cell`
* **Relevance**: Rabbit DSGC model with active dendrites; PSP DSI ~0.2 amplified to spike DSI ~0.8
  via local dendritic-spike thresholds. Provides E/I compound conductance anchors (PD 6.5/3.5 nS, ND
  2.5/6.0 nS) and demonstrates active-dendrite mechanism the PolegPolsky2016 mouse model explicitly
  does NOT use. Critical contrast for audit framing.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **Asset**: `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `voltage-gated-channels`
* **Relevance**: First direct recording of dendritic spikes in rabbit DSGC terminal dendrites.
  Establishes that species matters: rabbit has active dendrites; mouse DRD4 does not. Validates
  [PolegPolsky2016]'s passive-dendrite assertion as species-specific, not a universal DSGC rule.

### [Taylor2002]

* **Title**: Diverse Synaptic Mechanisms Generate Direction Selectivity in the Rabbit Retina
* **Authors**: Taylor, W. R., Vaney, D. I.
* **Year**: 2002
* **DOI**: `10.1523/JNEUROSCI.22-17-07712.2002`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.22-17-07712.2002/`
* **Categories**: `direction-selectivity`, `synaptic-integration`, `patch-clamp`,
  `retinal-ganglion-cell`
* **Relevance**: Voltage-clamp conductance decomposition in rabbit: on-response Ge PD/ND ratio 1.66
  +/- 0.48, on-response Gi null/preferred ratio 3.31 +/- 2.15. Cited by [PolegPolsky2016] as
  evidence for stronger ND inhibition, the architectural choice embedded in ModelDB 189347.

### [Park2014]

* **Title**: Excitatory Synaptic Inputs to Mouse On-Off Direction-Selective Retinal Ganglion Cells
  Lack Direction Tuning
* **Authors**: Park, S. J., Kim, I.-J., Looger, L. L., Demb, J. B., Borghuis, B. G.
* **Year**: 2014
* **DOI**: `10.1523/JNEUROSCI.5017-13.2014`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/`
* **Categories**: `direction-selectivity`, `synaptic-integration`, `retinal-ganglion-cell`
* **Relevance**: iGluSnFR demonstrates mouse bipolar-cell glutamatergic input to DSGCs is NOT
  directionally tuned; apparent tuning in voltage-clamp EPSCs is a space-clamp artefact. Cited by
  [PolegPolsky2016] as justification for "tuned inhibition, untuned excitation" architecture
  - the exact DS scheme the ModelDB 189347 model must implement.

### [Hausselt2007]

* **Title**: A Dendrite-Autonomous Mechanism for Direction Selectivity in Retinal Starburst Amacrine
  Cells
* **Authors**: Hausselt, S. E., Euler, T., Detwiler, P. B., Denk, W.
* **Year**: 2007
* **DOI**: `10.1371/journal.pbio.0050185`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pbio.0050185/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `compartmental-modeling`
* **Relevance**: Establishes that SAC dendrites compute DS autonomously via intrinsic dendritic
  mechanisms (soma-to-tip voltage gradient + HVA Ca2+ channels). Relevant because ModelDB 189347
  models SAC output as a presynaptic point process - if the SAC input already carries DS, the model
  does not need to simulate SAC dendritic computation. This is the justification for the paper's
  vesicle-release presynaptic approximation.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `synaptic-integration`, `compartmental-modeling`,
  `retinal-ganglion-cell`
* **Relevance**: Directly reuses and modifies the PolegPolsky2016 NEURON model
  (`geoffder/Spatial-Offset-DSGC-NEURON-Model`). Provides IPSC DSI anchors (wild-type 0.33,
  knockdown 0.07) and the 25-30 um cholinergic/GABAergic spatial offset that the PolegPolsky2016
  model does NOT use. Useful as a cross-validation that the base model behaves as expected under a
  second research group's hands.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`
* **Relevance**: Review tying the pre-vs-post-synaptic debate to specific cellular substrates;
  documents the 11:1 null:preferred SAC synapse ratio (SBEM) that underlies the paper's tuned-
  inhibition architecture.

### [Briggman2011]

* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: SBEM connectomic evidence that null-side SAC dendrites preferentially contact each
  DSGC. Cited by [PolegPolsky2016] as justification for null-direction inhibitory bias.

### [Fohlmeister2010]

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: `compartmental-modeling`, `voltage-gated-channels`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Canonical RGC channel-distribution paper. Five-channel model (Na, K-DR, Ca, K-A,
  K-Ca) with soma/dendrite/axon gbar densities. Provides defaults and comparison targets for the
  somatic and dendritic channel gbar values the ModelDB 189347 HHst.mod embeds.

### [Jeon2002]

* **Title**: Pattern of synaptic excitation and inhibition upon direction-selective retinal ganglion
  cells
* **Authors**: Jeon, C.-J., Kong, J.-H., Strettoi, E., Rockhill, R., Stasheff, S. F., Masland, R. H.
* **Year**: 2002
* **DOI**: `10.1002/cne.10288`
* **Asset**: Not in corpus (cited only as anatomical reference).
* **Categories**: `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Cited by [PolegPolsky2016] as the source of the homogeneous synapse- distribution
  assumption on ON dendrites. Not in corpus but flagged for optional fetch during research-internet
  stage if synapse-count audit ("177 vs. 282") cannot be resolved from code alone.

### [PolegPolsky2011]

* **Title**: Imperfect Space Clamp Permits Electrotonic Interactions between Inhibitory and
  Excitatory Synaptic Conductances, Distorting Voltage Clamp Recordings
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2011
* **DOI**: `10.1371/journal.pone.0019463`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1371_journal.pone.0019463/`
* **Categories**: `patch-clamp`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Same authors' earlier methods paper showing that space-clamp errors produce
  apparent but spurious directional tuning in voltage-clamp EPSCs. Explains why [PolegPolsky2016]
  trusts iGluSnFR (via [Park2014]) over voltage-clamp E/I measurements when deciding excitation is
  untuned. Validates the architecture choice embedded in ModelDB 189347.
