---
spec_version: "1"
task_id: "t0091_morphology_extended_nsga2_v1"
research_stage: "papers"
papers_reviewed: 21
papers_cited: 19
categories_consulted:
  - "compartmental-modeling"
  - "dendritic-computation"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
  - "voltage-gated-channels"
  - "synaptic-integration"
  - "patch-clamp"
  - "cable-theory"
date_completed: "2026-05-08"
status: "complete"
---
# Research Papers — First Joint 68-d NSGA-II With Morphology In Eval Loop (t0091)

## Task Objective

t0091 runs the project's first joint 68-d NSGA-II (54-d v3 electrophys + 14-d morphology) on the
Bed-B substrate, using the t0092-patched procedural DSGC morphology generator
(`generate_fixed_morphology`, canonicalised by C-0093-01) inside the evaluation loop. A 5-anchor
warm-start population (Bed-B-like, symmetric, PD-asymmetric, ND-asymmetric, alternative-topology)
seeds pop 96; the run iterates up to 8 generations under an adaptive HV-plateau stop and a $4.00
cost watchdog. The strategic question is whether enabling morphology as an optimisation axis opens
biologically-plausible joint-pass regions that t0080-t0088's fixed-Bed-B substrate could not reach
(NMDA per-synapse +85 to +116 sigma above [Sivyer2013, Sethuramanujam2017]; distal NaP +9 to +34
sigma above the Stuart-style cortical priors). A secondary question is whether the optimiser
preserves PD-asymmetric over ND-asymmetric anchors, which would be evidence for
soma-displacement-toward-PD as a functional DS mechanism per
[Schachter2010, Trenholm2013, Briggman2011].

## Category Selection Rationale

t0091 sits at the intersection of optimisation methodology and DSGC biology, so the category set is
broader than a typical implementation task. Six categories are core. **`compartmental-modeling`**
covers prior DSGC and SAC compartmental models that link morphology to direction selectivity
[Schachter2010, Tukker2004, Wu2023, Ezra-Tsur2021, Hausselt2007, Hay2011] and informs the
biological-plausibility scorecard's morphology priors. **`dendritic-computation`** supplies the
local-spike-threshold + electrotonic-subunit framework [Schachter2010, Sivyer2013, Aldor2024] that
makes morphology an active variable rather than a passive scaffold. **`direction-selectivity`**
covers the central question — whether morphological asymmetry is a functional DS mechanism in the
PD-vs-ND sense [Briggman2011, Kim2014, Vaney2012, Hausselt2007, Tukker2004] — and supplies the
PD-vs-ND-asymmetric anchor design rationale. **`retinal-ganglion-cell`** is consulted because every
biological prior in the scorecard is RGC-targeted and the firing-rate / DSI baselines come from DSGC
patch-clamp data [Trenholm2013, Sethuramanujam2017]. **`voltage-gated-channels`** covers the NaP /
Kv3 / Nav active-channel knobs whose interaction with morphology is the fitness-landscape shaping
mechanism [Aldor2024, Goethals2020]. **`synaptic-integration`** provides the NMDA / GABA
spatial-distribution priors against which Pareto cells are scored
[Sivyer2013, Sethuramanujam2017, PolegPolsky2016, Srivastava2022].

Two additional categories are consulted with a smaller cited footprint. **`patch-clamp`** is the
ground-truth methodology underlying [Sivyer2013, Trenholm2013, Aldor2024] but does not directly
shape NSGA-II decisions. **`cable-theory`** is consulted because Rall-law / electrotonic-length
arguments are central to interpreting morphology-extended Pareto cells
[Cuntz2010, Tukker2004, Anderson1999]; the [Anderson1999] cortical negative result is included
specifically to guard against over-interpreting any morphology-DS finding without checking velocity
tuning and integration statistics.

The category `wsd-evaluation` and other tags inherited from the project template are excluded as
unrelated to retinal compartmental modelling and multi-objective optimisation.

## Key Findings

### Morphological Asymmetry Alone Can Generate DS in DSGC Dendrites — Up To a Bounded Ceiling

[Tukker2004] built the first peer-reviewed compartmental SAC model demonstrating that a passive,
inhibition-free starburst with realistic dendritic geometry generates direction selectivity at its
distal output zones via a *local-global EPSP summation* mechanism. With a ~150-um radial morphology,
moving 30-um bars at ~2000 um/s produced **DSI ~0.2** at dendritic tips and essentially **DSI ~0**
at the soma; sine-wave gratings (spatial period ~400 um, ~5000 um/s) drove dendritic-tip DSI **up to
0.9** while soma DSI stayed below **0.1**. Crucially, stripping the cell to a single branchless
dendrite collapsed DSI to **0.03-0.08**, showing that sibling-dendrite recruitment of the global
EPSP is necessary; the mechanism is a property of the *whole* asymmetric tree, not of a single
branch. [Tukker2004] also performed an artificial-morphology sweep showing DSI is largely invariant
to first-branch-point distance but rises **up to 2-fold** when more branch points are concentrated
in the outer 20% of the tree, and that varying dendritic length across the eight dendrites of an
artificial cell increased annulus-DSI **roughly 3-fold** — a direct prediction that t0091's
PD-asymmetric and alternative-topology anchors are testing.

[Hausselt2007] complemented this with *experiment + model*: SAC dendrite DS persists under full
GABA-A / GABA-C / glycine block (ruling out lateral inhibition as a *required* mechanism), the F2/F1
harmonic ratio is **2-3x larger for centrifugal than centripetal** stimuli, and Ca2+ transients at
distal tips are **2-3x larger for centrifugal motion**. Most relevant for t0091, [Hausselt2007]'s
compartmental model showed **DSI scales monotonically with dendritic length over 50-200 um**: DSI
drops from ~0.35 at long (~150 um) dendrites to ~0.12 at short (~50 um) dendrites, because shorter
cables lose the soma-to-tip voltage gradient. Branch-order asymmetry adds another **~+0.1 DSI** when
active Ca2+ conductance is concentrated on higher-order distal branches. These two findings
(length-DSI scaling and distal-bias amplification) directly motivate t0091's `field_elongation_pd`
and `branch_density_gradient_pd` knobs.

[Wu2023] extended this to primate SAC and demonstrated that a *morphological* mechanism
(electrotonic propagation along dendrite preferentially summing centrifugal inputs) and a
*space-time* mechanism (proximal-sustained / distal-transient bipolar input kinetics) coexist and
dominate at *different* stimulus regimes: morphological dominates for small fast objects, space-time
for large slow objects. This is the central design pressure on the 5-anchor warm-start — both
classes of mechanism must be present in the seed population to give NSGA-II room to discover their
joint operating points.

**Hypothesis (HM-1)**: If t0091's symmetric anchor (anchor 2: `soma_offset_pd_um=0`,
`field_elongation_pd=1.0`, `branch_density_gradient_pd=0`) achieves joint-pass DSI through the
electrophys-only channel mechanism and is over-represented in the final Pareto, the Tukker /
Hausselt / Wu morphology mechanism is *not necessary* for the v3 substrate. If it is
under-represented, the morphology mechanism contributes additively.

**Hypothesis (HM-2)**: Per [Hausselt2007]'s monotonic DSI-vs-length finding and [Tukker2004]'s
distal-branch-density finding, anchor 3 (PD-asymmetric: field elongated 2x along PD, branch density
biased toward PD) should reach higher DSI than the symmetric anchor at matched electrophys
parameters. If the optimiser converges to PD-asymmetric morphologies but not ND-asymmetric, the
asymmetry direction is functionally meaningful (one axis of [Briggman2011]).

### Wiring And Soma-Position Asymmetry Is The Empirical Substrate Of Mammalian DSGC DS

[Briggman2011] is the structural ground truth. Combining two-photon Ca2+ imaging with serial
block-face EM of the *same* mouse retinal tissue, they identified **831 putative SAC-to-DSGC
synapses** across 24 SACs and 6 DSGCs and showed:

* SAC dendrite-to-DSGC-null-direction angle: mean **165.2 +/- 51.7 degrees** (n = 831 synapses) —
  most SAC inputs arise from null-antiparallel dendrites.
* Null-side SAC somata contributed **524 synapses** vs. only **41** from preferred-side somata, a
  **~12.8:1 ratio** that establishes wiring asymmetry as the structural substrate of DS.
* Critically, when soma-soma axis and dendrite orientation conflict, **dendrite orientation wins**
  (connected dendrites run **24.3 +/- 2.8 degrees closer** to null than the soma-soma vector); the
  unit of wiring specificity is the SAC dendrite, not the SAC soma.

[Briggman2011] therefore establishes that the relevant geometric variable is *orientation along the
PD-ND axis*, not absolute position. This is exactly what t0091's PD-asymmetric vs ND-asymmetric
anchor mirror tests in the DSGC. [Kim2014] extended the connectomic story by showing space-time
wiring specificity in mouse Off-SAC: bipolar cell type segregation along the SAC dendrite (proximal
sustained, distal transient) imparts a centrifugal velocity bias on each SAC dendrite, validated
later by [Srivastava2022]'s direct iGluSnFR imaging of glutamate kinetics — the proximal release
rate is **~3x larger than distal**, mapping the dendritic length onto stimulus delay.

[Trenholm2013] adds the soma-coupling layer: superior-coding Hb9+ DSGCs in mouse couple to **7.4 +/-
0.7 neighbours** (n = 5/5) via reciprocal gap junctions of conductance **~1 nS** that act as
low-pass filters with corner frequency **~10 Hz**. They report DSGC peak firing rates of **198 +/-
14 Hz preferred / 27 +/- 12 Hz null** under control and **244 +/- 18 / 202 +/- 14 Hz** under
picrotoxin (n = 6 / n = 4). These peak-rate numbers — distinct from the trial-averaged ~10 Hz mean
— are the canonical biological target for any modelling work that fits firing rates, including
t0091's joint-pass criterion. [Trenholm2013] also notes that response *skew* (preferred-direction SI
= **1.6 +/- 0.1** for coupled vs **1.1 +/- 0.1** for uncoupled cells, p = 0.009) survives full
GABA-A block (SI **2.3 +/- 0.3** preferred under picrotoxin), consistent with intrinsic membrane
mechanisms (Na slow inactivation, Ca-activated K) maintaining DS at the spike level even when
network inhibition is removed — a useful constraint when interpreting the Pareto's
biological-plausibility distribution.

### Dendritic Spikes Convert Weak PSP DSI Into Strong Spike DSI Via Local Threshold Nonlinearity

[Schachter2010] is the single most-cited reference for the DSGC compartmental modelling done in this
project. Using NeuronC on a reconstructed rabbit On-Off DSGC, they showed:

* PSP-level DSI is weak (**~0.2**) but somatic spike DSI is strong (**~0.8**) — a **~4x
  amplification** via the dendritic spike threshold nonlinearity.
* Dendritic spike initiation requires **~1 nS** at distal tips (input resistance **>1 GOhm**) but
  **3-4 nS** near the soma (input resistance **150-200 MOhm**). This spatial gradient of threshold
  is the substrate of the local-subunit computation.
* Inhibition (**4-10 nS** physiological peak) prevents spike *initiation* but cannot block
  *propagation*; blocking propagation would require **~85 nS**, an order of magnitude larger than
  measured. Inhibition is therefore a *spike-initiation veto*, not a propagation shunt.
* Removing presynaptic SAC-derived DS drops spike DSI from **~0.8** to **~0.3-0.4** even with
  postsynaptic inhibition intact; postsynaptic inhibition alone gives robust DS only at the most
  isolated distal tips.
* Baseline dendritic Na density used: **40 mS/cm^2** uniform (or **45 -> 20 mS/cm^2**
  proximal-to-distal gradient); somatic gNa **150 mS/cm^2**.
* Most striking for morphology-extended optimisation, [Schachter2010] identified an **intrinsic
  dendritic DS effect that *opposes* the desired tuning on the preferred side** by roughly **DSI
  -0.1 to -0.2**, because excitation arriving distal-to-proximal (null direction on the preferred
  side) sums more effectively. Network DS must be strong enough to overcome this intrinsic bias.

[Sivyer2013] (Nature Neuroscience; metadata-only because download failed — paywalled, in
intervention) provides the *direct in-vivo dendritic-spike measurement* in rabbit DSGC, confirming
that preferred-direction motion triggers terminal-dendritic Na spikes that propagate to the soma
with high probability while null-direction motion fails to initiate them due to spatially offset
inhibition; this is the empirical ground for the [Schachter2010] mechanism.

[Aldor2024] (mouse SAC) shows complementary perisomatic Kv3 and dendritic mGluR2 contributions —
mGluR2 modulates dendritic Ca2+ initiation but not somatic; Kv3 dampens fast somatic transients —
providing further evidence that subcellular *channel placement* shapes DS computation. This is
relevant to t0091's interpretation of the Pareto: cells where channel densities concentrate at the
"wrong" subcellular locations should be flagged exotic.

**Hypothesis (HM-3)**: If [Schachter2010]'s intrinsic-DS-opposing-network-DS effect (DSI -0.1 to
-0.2 on the preferred side) is reproduced in t0091's Bed-B-like anchor, the morphology-extended
Pareto cells with stronger network DS should be those with higher `field_elongation_pd`, since this
geometrically reduces the distal-to-proximal opposition.

### High-Dimensional Multi-Objective Optimisation: Lessons From Prior Modelling

[Hay2011] is the methodological precedent within neuroscience: they used a multi-objective
evolutionary algorithm (PEPCO) to fit ion channel densities of a layer-5b pyramidal cell against
both perisomatic Na firing and dendritic Ca spike features simultaneously, generating a *family* of
acceptable models rather than a single tuned one. This is the canonical demonstration that NSGA-II
in compartmental neuroscience produces a populated Pareto with mechanistically distinct solutions
— the same pattern t0083 observed in this project's 54-d substrate. [Hay2011]'s lesson is that the
useful artefact is the *family of solutions*, and that morphological perturbations should be applied
to the family ensemble (the t0091 design pattern) rather than to a single tuned cell.

[Ezra-Tsur2021] ran NSGA-II / IBEA on an **8-d SAC input parameter space** (refilling rate, release
probability, kinetic-transition start/end, conductance, anatomical-transition point, scaling, and
offset), 100 individuals x 20-45 generations, 6 random seeds. Their headline finding has direct
implications for t0091: with the *natural* spatiotemporal arrangement (sustained proximal, transient
distal), GA converges on multiple parameter sets reproducing measured CF preference; with the
*reversed* arrangement, **0 of 2125** simulated SACs are CF-preferring. SAC-SAC reciprocal
inhibition is a *modulator* (CSI rises moderately up to ~0.1 nS then declines), not a generator —
adding inhibition to non-CF-preferring or reversed-kinetics cells fails to generate CF preference at
any strength. For a DSGC embedded in this network, **random SAC-to-DSGC wiring produces DSI ~ 0;
asymmetric null-side wiring produces positive DSI even without SAC-SAC inhibition**. The
methodological takeaway: NSGA-II on retinal circuit parameters is a tractable, established
technique, and the GA-discovered Pareto exposes which mechanisms are *necessary* vs *modulatory*.

[Ament2023] is the project's own reference for high-d Bayesian optimisation pathologies. They prove
(Theorem 1) that canonical Expected Improvement suffers a *vanishing-gradient pathology* in
double-precision arithmetic — `phi(z) + z*Phi(z)` evaluates to exactly zero for `z < ~-37`,
producing a domain region where >90% of points have `|grad EI| < 1e-10` by n=1000 in d=8 on Ackley.
In the Ackley d-sweep, the gap between LogEI and canonical EI **widens with dimension**; canonical
EI fails to leave the random-search baseline at d=16, while LogEI reaches good values within 250
evaluations. **The relevant scaling lesson for t0091**: canonical GP-BO methods (qLogNEHVI in
BoTorch) hit O(N^3) scaling in d=68, which contributed to t0078's GP-based d=40+ MOBO blowing its
cost envelope (per the project memo on NSGA-II for high-d MOBO). NSGA-II via pymoo avoids this and
is the project's standing default for d > 40, but [Ament2023]'s vanishing-gradient pathology and the
SAAS prior remedies remain a useful comparison baseline if NSGA-II convergence is sluggish.

[Cuntz2010] supplies the procedural-morphology generator framework underlying t0090's 14-knob
generator: a single balancing factor `bf` (biological range **0.2-0.7**) plus a target spanning-
field density profile suffices to reproduce Sholl intersections, branch-order distributions, total
dendritic length within a few percent, and electrotonic compartmentalisation across cell classes
from fly LPTCs to cerebellar Purkinje cells. [Cuntz2010] explicitly excludes asymmetry; t0091's
morphology generator extends Cuntz with the asymmetry knobs (`soma_offset_pd_um`,
`field_elongation_pd`, `branch_density_gradient_pd`, `primary_branch_pd_concentration`) that
[Briggman2011] and [Vaney2012] identify as the missing dimension for DSGC.

### Negative Cortical Control Against Over-Interpreting Any Morphology-DS Finding

[Anderson1999] is the methodological cautionary control. They reconstructed **32 cat V1 neurons**
with known direction preferences and tested the Livingstone (1998) hypothesis that V1 directional
selectivity arises from dendritic asymmetry. The angular-offset distribution between preferred
direction and dendritic-bias angle is **indistinguishable from uniform random** (Kolmogorov-Smirnov
**p = 0.23**); the predicted peak at 180 degrees is not observed. Their compartmental Meynert-cell
simulation showed that even at unphysical extremes, the analytically optimal preferred velocity for
a single asymmetric dendrite is **~77 degrees/s** — an order of magnitude faster than measured V1
tuning (~10-20 degrees/s) and only achievable with `tau_m = 5 ms`; raising `tau_m` to 50 ms shifts
the peak to ~24 degrees/s but simultaneously eliminates the preferred-vs-null voltage difference.
Adding synapses to a single opposing basal dendrite (closer to real input statistics) **destroys the
velocity peak entirely**. The cable-theoretic optimum **v_opt ≈ 2 lambda / tau_m** is the
constraint that must be checked when interpreting any morphology-extended Pareto cell.

The retinal DSGC case is *not* analogous to the V1 case [Vaney2012, Briggman2011, Tukker2004], but
[Anderson1999]'s methodological framework — log the implied v_opt from each Pareto cell's
electrotonic length and compare against [Trenholm2013]'s 600 um/s preferred bar velocity — is a
sanity check t0091 should adopt to prevent over-interpreting morphology-DS findings.

### The Biological Plausibility Scorecard: Five Priors Relevant To 68-d Pareto Cells

The project's biological-plausibility scorecard (from t0086, t0088) evaluates each Pareto cell
against priors derived from this corpus:

* **NMDA per-synapse density** ([Sivyer2013, Sethuramanujam2017]): t0086 / t0088 reported v3 Bed-B
  substrate joint-pass cells at **+85 to +116 sigma** above the [Sivyer2013] per-spine ~0.1 nS
  prior. Whether morphology variation can shift `gnmda_dend` toward the prior is a primary t0091
  question.
* **Distal NaP density**: t0086 / t0088 reported **+9 to +34 sigma** above the Stuart-style
  cortical-pyramidal NaP prior (sub-1 % of Nav at distal sites). Morphology variation that
  redistributes section length in the distal compartment may legitimise higher per-section density
  via a smaller integrated current.
* **GABA spatial-gradient**: [PolegPolsky2016] established that bipolar-cell input contrast
  sensitivities differ between BC subtypes feeding SACs vs DSGCs to maintain a stable E/I ratio
  across visual contrast; v3 substrate cells violate the spatial gradient by placing GABA inputs in
  unphysiological dendritic zones. Morphology-extended cells with longer/elongated dendrites may
  achieve geometrically valid GABA placement.
* **DSGC peak firing rates** ([Trenholm2013]): preferred 198 Hz / null 27 Hz under control are the
  targets. Pareto cells exceeding 250 Hz preferred are flagged hyperbolic.
* **AIS Nav density** ([Goethals2020]): reports a strong axial AIS current implying high Nav density
  consistent with Werginz 2024's measured **17.3 +/- 3 ratio**; t0088 cluster 1 reported a 116x
  ratio (+33 sigma above the prior). Morphology that respects the AIS-to-soma diameter constraint
  may legitimise higher Nav density.

## Methodology Insights

* **5-anchor warm-start design is informed by [Briggman2011]'s wiring asymmetry directionality.**
  Anchor 3 (PD-asymmetric: soma offset +100 um toward PD, field elongated 2x along PD) and anchor 4
  (ND-asymmetric: soma offset -100 um) are the *mirror pair* whose differential preservation tests
  the soma-displacement-toward-PD hypothesis (one of the two asymmetry classes [Briggman2011]
  identifies as biologically meaningful: SAC dendrite orientation along null axis with asymmetry
  *toward* preferred-side soma).

* **Use [Schachter2010]'s baseline channel densities as the v3 substrate's electrophys reference.**
  Dendritic Na **40 mS/cm^2** uniform (or **45 -> 20 mS/cm^2** gradient); somatic gNa **150
  mS/cm^2**; AMPA peak excitation **0.2-1.0 nS** per synapse; GABA peak inhibition **4-10 nS** with
  placement within ~20 um of paired excitation. Pareto cells with values >>10x these are exotic by
  definition and should be scored accordingly.

* **DSI metric must use vector-sum across 16 directions, not pref/null ratio at a single angle.**
  [Trenholm2013, Tukker2004, Hausselt2007] all use vector-sum or full angular tuning curves; this is
  what t0091's joint-pass criterion already does.

* **Pop 96 x 8 generations is at the lower bound for d=68.** [Ezra-Tsur2021] used pop 100 x 20-45
  generations on d=8; [Hay2011] used the BluePyOpt successor frameworks at pop 1000+ on d~30.
  t0091's adaptive HV-plateau stop and 5-anchor warm-start compensate by frontloading prior
  knowledge, but the cost-watchdog-driven 6-gen fallback is a known under-budget regime where the
  Pareto may not fully converge.

* **NSGA-II via pymoo is the right algorithm class for d=68.** Per the project's standing preference
  (NSGA-II for high-d MOBO follow-ups, BoTorch GP-based qLogNEHVI for d <= 40): [Ezra-Tsur2021]'s
  NSGA-II / IBEA equivalence (results qualitatively identical across 6 seeds in d=8) suggests the
  algorithm choice is robust; [Ament2023]'s LogEI improvements would be the first thing to try if
  NSGA-II convergence stalls, but only after dropping back to d <= 40.

* **Biological-plausibility scorecard should evaluate every Pareto cell, not just the
  joint-pass-or-better subset.** Per [Tukker2004]'s point that DSI varies continuously with
  morphology, the *boundary* between plausible and exotic is itself an information-rich variable
  that informs whether morphology shifts the boundary or merely moves cells along it.

* **Anchor-tracking statistics need bootstrap CIs because pop 96 / 5 = ~19 cells per anchor is
  small.** The expected-vs-observed Pareto representation per anchor should be reported with 95%
  bootstrap CIs (1000 resamples), not just point estimates, to avoid overclaiming significance from
  small per-anchor samples.

* **The t0093 patched-generator re-sweep result (60/60 STABLE-firing under the t0083 channel set)
  means generator instability under NSGA-II mutation is unlikely.** The patched generator covers the
  morphology parameter space without NaN_VOLTAGE failures. The remaining instability risk is the
  tail of the distribution — extreme parameter combinations that the LHS sample missed.
  Penalty-objective fallback for any cell whose simulation NaNs out is the safe default.

* **Hypothesis-driven Pareto analysis should test [Hausselt2007]'s monotonic DSI-vs-length
  scaling.** If t0091's Pareto cells with longer `field_elongation_pd` consistently dominate cells
  with shorter, the [Hausselt2007] mechanism is operative in the optimised substrate. If not, the
  Pareto is finding DSI through a non-morphological channel mechanism (the "v3 ceiling not raised by
  morphology" outcome).

## Gaps and Limitations

The reviewed corpus has six gaps directly relevant to t0091's question:

* **No prior NSGA-II at d > 40 in retinal compartmental modelling.** [Ezra-Tsur2021] is at d=8;
  [Hay2011] at d~30. t0091 at d=68 is in unmapped territory for the retinal DSGC literature, and the
  convergence rate of NSGA-II at this dimensionality on this substrate is not predictable from any
  cited paper. This is the primary risk: 8 generations may be insufficient, and the
  cost-watchdog-driven 6-gen fallback is an even thinner Pareto.

* **No quantitative biological-plausibility scorecard for joint morphology + electrophys cells in
  the literature.** [Tukker2004, Hausselt2007, Wu2023] vary morphology against fixed electrophys;
  [Hay2011, Ezra-Tsur2021] vary electrophys at fixed morphology. The 9-prior scorecard t0086 / t0088
  built is project-specific and has no published cross-comparison; its calibration depends on the
  Sivyer 2013 / Stuart 1999 priors which themselves come from cell types other than mouse DSGC.

* **No published soma-displacement-vs-DSI experimental data in DSGC.** [Briggman2011] establishes
  that *SAC dendrite orientation along null axis* is the structural substrate of asymmetry in mouse,
  but the *DSGC's* soma position relative to its own dendritic field is not systematically varied in
  any cited paper. t0091's PD-asymmetric vs ND-asymmetric anchor mirror is therefore a *novel test*
  not directly anchored to existing experimental data — its outcome will inform which
  morphological asymmetries are functional.

* **No measurement of how t0090's 14 generator knobs map to in-vivo morphological variation.**
  [Cuntz2010] showed `bf` alone captures cell-class-level realism; the 14 knobs are project-defined
  and their physiological ranges are inferred from [Vaney2012, Briggman2011] qualitative
  descriptions plus engineering judgement. t0091 cannot validate the knob *ranges* against the
  literature; it can only ask whether the optimiser uses them.

* **Limited published data on per-section vs per-segment NaP density gradients along DSGC
  dendrites.** [Sivyer2013] establishes dendritic Na spikes initiate; [Goethals2020] establishes
  high AIS Nav. The detailed gradient between AIS, soma, proximal dendrite, and distal dendrite is
  not directly measured in DSGC, so the +9 to +34 sigma exotic-ness reported in t0086 / t0088 is
  benchmarked against cortical-pyramidal priors (Stuart 1999) rather than DSGC-specific priors.
  Morphology variation may push the Pareto into a regime where the cortical-prior comparison is even
  less appropriate; this should be flagged in the answer asset.

* **Cost-budget watchdog limits the depth of Phase D anchor-tracking analysis.** With pop 96 and
  bootstrap resampling, statistical power for distinguishing moderate over-representation (e.g., 60%
  Bed-B-like vs uniform 20%) is adequate; for distinguishing PD-asymmetric vs ND-asymmetric mirror
  representation in a final Pareto of <30 cells, power is marginal. [Tukker2004]'s 16-tip-per-cell
  sampling and [Briggman2011]'s 24-SAC-x-6-DSGC sampling are guidance for the minimum sample sizes
  needed to claim significance — t0091 may fall short.

## Recommendations for This Task

1. **Use the [Schachter2010] reference channel densities (40 mS/cm^2 dendritic Na, 150 mS/cm^2
   somatic Na, 0.2-1.0 nS AMPA, 4-10 nS GABA placed within 20 um of excitation) as the "biologically
   plausible" baseline** in the scorecard for Phase C. Any Pareto cell more than 10x off these
   values on any axis is automatically flagged exotic, regardless of joint-pass status.

2. **Include [Trenholm2013]'s peak preferred (198 Hz) / null (27 Hz) firing rates and the >250 Hz
   ceiling as hard biological-plausibility bands** in the Phase C scorecard. Cells outside these
   bands but joint-pass-by-our-DSI-criterion should be reported as "DSI-by-spike-rate-inflation"
   rather than as a biological win.

3. **Build the 5-anchor warm-start so that anchor 3 (PD-asymmetric) and anchor 4 (ND-asymmetric) are
   exact mirrors** — same |soma_offset_pd_um|, same field elongation magnitude, same branch
   density gradient magnitude, opposite signs. Per [Briggman2011]'s dendrite-direction-not-soma-side
   finding, the asymmetry should also be applied to the *primary branch concentration* so that the
   anchors test orientation, not just translation.

4. **Compute the cable-theoretic v_opt = 2 * lambda / tau_m for every Pareto cell** and tabulate
   alongside DSI / firing-rate metrics in Phase D. Per [Anderson1999]'s methodological critique, any
   cell whose v_opt is far from the [Trenholm2013] 600 um/s stimulus velocity should be reported
   with that mismatch noted; the Pareto's distribution over v_opt will indicate whether
   morphological variation is shifting the cells toward or away from biological tuning.

5. **Run [Hausselt2007]'s length-vs-DSI sanity check on the final Pareto.** Plot DSI as a function
   of effective dendritic length (extracted from the 14-d morphology vector); a monotonic positive
   relationship would confirm the Hausselt mechanism is operative. A flat or inverted relationship
   indicates the Pareto is exploiting a non-Hausselt mechanism (likely the [Schachter2010]
   intrinsic-DS-overcoming-network-DS regime, which is the v3 substrate's existing mechanism).

6. **Use [Ezra-Tsur2021]'s necessity-vs-modulator decomposition framing in Phase E.** For each
   feature of the Pareto distribution (anchor preservation, channel-density centroid, morphology
   centroid), explicitly classify it as *necessary* (loss eliminates joint-pass), *sufficient*
   (presence enables joint-pass), or *modulator* (presence shifts the Pareto but does not gate it).
   This framing forces precision in the answer asset.

7. **If NSGA-II convergence stalls at gen 5-6, do NOT extend to BoTorch qLogNEHVI**. Per the project
   memo (NSGA-II for d > 40 due to GP O(N^3) cost) and t0078's blowup, the right fallback is to
   accept the partial Pareto, document what's missing, and propose a follow-up at lower
   dimensionality (e.g., fix a subset of electrophys parameters and re-run NSGA-II at d=40-45).

8. **Document all anchor representations with bootstrap 95% CIs** computed from 1000 resamples of
   the final Pareto. Per [Briggman2011]'s 524 vs 41 (12.8:1) ratio level of effect size, t0091 needs
   at least a 5:1 over-representation of one anchor to claim significance with the small per-anchor
   pop available.

## Paper Index

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`, `synaptic-integration`, `cable-theory`
* **Relevance**: The single most directly relevant compartmental DSGC paper. Defines the dendritic
  spike threshold mechanism, intrinsic-DS-opposing-network-DS effect, and reference channel
  densities that t0091's biological-plausibility scorecard uses as the v3 baseline.

### [Briggman2011]

* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`
* **Relevance**: Structural ground truth for asymmetric SAC-to-DSGC wiring (12.8:1 null vs
  preferred). Directly motivates t0091's PD-asymmetric vs ND-asymmetric anchor mirror design.

### [Trenholm2013]

* **Title**: Dynamic Tuning of Electrical and Chemical Synaptic Transmission in a Network of Motion
  Coding Retinal Neurons
* **Authors**: Trenholm, S., McLaughlin, A. J., Schwab, D. J., Awatramani, G. B.
* **Year**: 2013
* **DOI**: `10.1523/JNEUROSCI.0808-13.2013`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.0808-13.2013/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `patch-clamp`,
  `synaptic-integration`
* **Relevance**: Canonical mouse Hb9+ DSGC peak firing rate measurements (198 Hz preferred / 27 Hz
  null) used as biological targets. Establishes the soma-coupling and skew-index baselines.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Authoritative review framing structural and functional asymmetry as the organising
  principle of retinal DS. Provides the conceptual scaffold for interpreting t0091's anchor-tracking
  results.

### [Sivyer2013]

* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **Asset**: `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nn.3565/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `patch-clamp`
* **Relevance**: Source of the per-spine NMDA conductance prior (~0.1 nS) used in the
  biological-plausibility scorecard. Provides the in-vivo dendritic-spike measurement that
  underwrites [Schachter2010]'s mechanism. Paper PDF was paywalled; metadata-only.

### [Hausselt2007]

* **Title**: A Dendrite-Autonomous Mechanism for Direction Selectivity in Retinal Starburst Amacrine
  Cells
* **Authors**: Hausselt, S. E., Euler, T., Detwiler, P. B., Denk, W.
* **Year**: 2007
* **DOI**: `10.1371/journal.pbio.0050185`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pbio.0050185/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Establishes monotonic DSI-vs-dendritic-length scaling (DSI 0.35 at 150 um vs 0.12
  at 50 um) and tonic-depolarisation-gradient mechanism. Directly motivates t0091's field-elongation
  knob and the length-vs-DSI sanity check in Phase D.

### [Tukker2004]

* **Title**: Direction selectivity in a model of the starburst amacrine cell
* **Authors**: Tukker, J. J., Taylor, W. R., Smith, R. G.
* **Year**: 2004
* **DOI**: `10.1017/S0952523804214109`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1017_S0952523804214109/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `cable-theory`
* **Relevance**: First peer-reviewed compartmental SAC model showing morphology-only DS via
  local-global EPSP summation. Artificial-morphology sweep documents 2-fold and 3-fold DSI
  amplifications when distal branch density and dendritic-length asymmetry are increased — the
  prior for t0091's `branch_density_gradient_pd` and `field_elongation_pd` knobs.

### [Wu2023]

* **Title**: Two mechanisms for direction selectivity in a model of the primate starburst amacrine
  cell
* **Authors**: Wu, J., Kim, Y. J., Dacey, D. M., Troy, J. B., Smith, R. G.
* **Year**: 2023
* **DOI**: `10.1017/S0952523823000019`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1017_S0952523823000019/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `retinal-ganglion-cell`
* **Relevance**: Demonstrates morphology-mechanism + space-time-mechanism dominance regimes (small
  fast vs large slow stimuli). Frames the question of whether t0091's optimiser is trading between
  mechanism classes per anchor.

### [Ezra-Tsur2021]

* **Title**: Realistic retinal modeling unravels the differential role of excitation and inhibition
  to starburst amacrine cells in direction selectivity
* **Authors**: Ezra-Tsur, E., Amsalem, O., Ankri, L., Patil, P., Segev, I., Rivlin-Etzion, M.
* **Year**: 2021
* **DOI**: `10.1371/journal.pcbi.1009754`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1009754/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `retinal-ganglion-cell`
* **Relevance**: Methodological precedent for NSGA-II / IBEA on retinal DS parameters (d=8, pop 100
  x 20-45 generations). Establishes the necessity-sufficiency-modulator framework adopted in t0091's
  Phase E.

### [Hay2011]

* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1371_journal.pcbi.1002107/`
* **Categories**: `voltage-gated-channels`, `compartmental-modeling`, `dendritic-computation`
* **Relevance**: Classic precedent for multi-objective evolutionary optimisation of channel
  densities in a compartmental model with dendritic + perisomatic objectives. The Pareto-as-family
  philosophy is what t0091 inherits.

### [Cuntz2010]

* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Häusser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000877/`
* **Categories**: `compartmental-modeling`, `dendritic-computation`, `cable-theory`
* **Relevance**: Foundation for procedural-morphology generators — the project's t0090 generator
  extends Cuntz's symmetric-envelope approach with the asymmetry knobs t0091 optimises.

### [Anderson1999]

* **Title**: Dendritic asymmetry cannot account for directional responses of neurons in visual
  cortex
* **Authors**: Anderson, J. C., Binzegger, T., Kahana, O., Martin, K. A. C., Segev, I.
* **Year**: 1999
* **DOI**: `10.1038/12194`
* **Asset**: `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_12194/`
* **Categories**: `direction-selectivity`, `dendritic-computation`
* **Relevance**: Negative cortical control. Provides the cable-theoretic v_opt = 2 lambda / tau_m
  constraint that t0091's Phase D analysis should compute for every Pareto cell as a sanity check
  against over-interpreting any morphology-DS finding.

### [Kim2014]

* **Title**: Space-time wiring specificity supports direction selectivity in the retina
* **Authors**: Kim, J. S., Greene, M. J., Zlateski, A., Lee, K., et al.
* **Year**: 2014
* **DOI**: `10.1038/nature13240`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_nature13240/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `retinal-ganglion-cell`,
  `synaptic-integration`
* **Relevance**: Establishes space-time wiring of bipolar cells onto SAC dendrites. Connects
  morphology-mechanism (electrotonic propagation) with synaptic-mechanism (input-kinetic gradient)
  on the same dendrite. Paper PDF was paywalled; metadata-only.

### [Srivastava2022]

* **Title**: Spatiotemporal properties of glutamate input support direction selectivity in the
  dendrites of retinal starburst amacrine cells
* **Authors**: Srivastava, P., de Rosenroll, G., Matsumoto, A., Michaels, T., et al.
* **Year**: 2022
* **DOI**: `10.7554/eLife.81533`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.7554_eLife.81533/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `dendritic-computation`,
  `synaptic-integration`, `retinal-ganglion-cell`
* **Relevance**: iGluSnFR-imaging confirmation of [Kim2014]'s space-time wiring (proximal release
  rate ~3x distal). Direct experimental support for the input-kinetic-gradient mechanism that
  t0091's space-time-wiring proxies in the electrophys parameter set.

### [Aldor2024]

* **Title**: Dendritic mGluR2 and perisomatic Kv3 signaling regulate dendritic computation of mouse
  starburst amacrine cells
* **Authors**: Acaron Ledesma, H., Ding, J., Oosterboer, S., Huang, X., et al.
* **Year**: 2024
* **DOI**: `10.1038/s41467-024-46234-7`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1038_s41467-024-46234-7/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `synaptic-integration`,
  `voltage-gated-channels`
* **Relevance**: Subcellular channel-distribution evidence (perisomatic Kv3, dendritic mGluR2)
  supporting t0091's interpretation that channel-placement-by-compartment matters. Informs the
  scorecard's "wrong subcellular location" exotic flag.

### [Sethuramanujam2017]

* **Title**: "Silent" NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit
* **Authors**: Sethuramanujam, S., Yao, X., deRosenroll, G., Briggman, K. L., Field, G. D.,
  Awatramani, G. B.
* **Year**: 2017
* **DOI**: `10.1016/j.neuron.2017.09.058`
* **Asset**: `tasks/t0017_literature_survey_patch_clamp/assets/paper/10.1016_j.neuron.2017.09.058/`
* **Categories**: `direction-selectivity`, `voltage-gated-channels`, `retinal-ganglion-cell`,
  `patch-clamp`, `synaptic-integration`
* **Relevance**: Establishes the silent-NMDA mechanism in adult mouse DSGC. Paired with [Sivyer2013]
  as the source of the per-synapse NMDA prior (~0.1 nS) that the scorecard uses to flag exotic
  Pareto cells. Paper PDF was paywalled; metadata-only.

### [Ament2023]

* **Title**: Unexpected Improvements to Expected Improvement for Bayesian Optimization
* **Authors**: Ament, S., Daulton, S., Eriksson, D., Balandat, M., Bakshy, E.
* **Year**: 2023
* **DOI**: `no-doi_Ament2023_logei-bo`
* **Asset**: `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/`
* **Categories**: `compartmental-modeling`
* **Relevance**: LogEI / qLogNEHVI methodology for high-d MOBO. Establishes the GP-BO scaling
  ceiling that motivates t0091's NSGA-II choice over BoTorch qLogNEHVI for d=68. The
  vanishing-gradient pathology and Theorem 1 are the project's reference for why GP-BO failed at
  d=40+.

### [Goethals2020]

* **Title**: Electrical match between initial segment and somatodendritic compartment for action
  potential backpropagation in retinal ganglion cells
* **Authors**: Goethals, S., Sierksma, M. C., Nicol, X., Réaux-Le Goazigo, A., Brette, R.
* **Year**: 2020
* **DOI**: `10.1101/2020.09.15.297937`
* **Asset**:
  `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/assets/paper/10.1101_2020.09.15.297937/`
* **Categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `patch-clamp`,
  `compartmental-modeling`
* **Relevance**: Establishes that mouse RGC AIS produces a strong axial current implying high Nav
  conductance density that depolarises the soma by ~30 mV. Provides the AIS-Nav prior used in the
  biological-plausibility scorecard's AIS-to-soma ratio comparison.

### [PolegPolsky2016]

* **Title**: Retinal Circuitry Balances Contrast Tuning of Excitation and Inhibition to Enable
  Reliable Computation of Direction Selectivity
* **Authors**: Poleg-Polsky, A., Diamond, J. S.
* **Year**: 2016
* **DOI**: `10.1523/JNEUROSCI.4013-15.2016`
* **Asset**:
  `tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1523_JNEUROSCI.4013-15.2016/`
* **Categories**: `direction-selectivity`, `compartmental-modeling`, `synaptic-integration`,
  `retinal-ganglion-cell`
* **Relevance**: Establishes that bipolar-cell input contrast sensitivity differences between BCs
  feeding SACs vs DSGCs maintain a stable E/I ratio across visual contrast. Provides the GABA
  spatial-gradient prior against which v3 substrate cells are scored.
