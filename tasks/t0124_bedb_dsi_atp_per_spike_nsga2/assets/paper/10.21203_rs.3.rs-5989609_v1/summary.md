---
spec_version: "3"
paper_id: "10.21203_rs.3.rs-5989609_v1"
citation_key: "Wang2025"
summarized_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_summarized: "2026-05-25"
---

# Energetic Diversity in Retinal Ganglion Cells Is Modulated by Neuronal Activity and Correlates with Resilience to Degeneration

## Metadata

* **File**: `files/williams_2025_energetic-diversity-rgcs.pdf`
* **Published**: 2025-03-12 (Research Square preprint, In Review)
* **Authors**: Zelun Wang 🇺🇸, Christopher Zhao 🇺🇸, Shelly Xu 🇺🇸, Sean McCracken 🇺🇸, Rajendra S. Apte 🇺🇸, Philip R. Williams 🇺🇸 (co-corresponding)
* **Venue**: Research Square preprint (Springer Nature; "In Review")
* **DOI**: `10.21203/rs.3.rs-5989609/v1`

## Abstract

Neuronal function requires high energy expenditure that is likely customized to meet specific
signaling demands. However, little is known about diversity of metabolic homeostasis among
divergently-functioning types of neurons. To this end, we examined retinal ganglion cells (RGCs), a
population of closely related, yet electrophysiologically distinct excitatory projection neurons.
Using in vivo 2-photon imaging to measure ATP with single cell resolution, we identified
differential homeostatic energy maintenance in the RGC population that correspond to distinct RGC
types. In the presence of circuit activity, the most active RGC type (Alpha RGCs), had lower
homeostatic ATP levels than other types and exhibited the greatest magnitude of ATP decline when
ATP synthesis was inhibited. By simultaneously manipulating circuit activity and mitochondrial
function, we found that while oxidative phosphorylation was required to meet ATP demands during
circuit activity, it was expendable to maintain resting ATP levels. We also examined ATP signatures
associated with survival and injury response after axotomy and report a correlation between low
homeostatic ATP and increased survival. In addition, we observed transient ATP increases in RGCs
following axon injury. Together, these findings identify diversity of energy handling capabilities
of dynamically active neurons with implications for neuronal resilience.

## Overview

Wang et al. present the first in vivo, single-cell measurements of steady-state ATP across
identified mouse retinal ganglion cell (RGC) types -- Alpha RGCs (alphaRGCs), intrinsically
photosensitive RGCs (ipRGCs), and ON-OFF direction-selective RGCs (ooDSGCs). Prior RGC metabolism
studies pooled whole retina or enriched bulk RGC populations, obscuring per-type differences. By
expressing the ATeam1.03-nD/nA FRET ATP biosensor with a Cre-dependent AAV in VGlut2-Cre mice and
imaging through the pupil with 2-photon microscopy, the authors quantify homeostatic YFP/CFP
(proportional to intracellular ATP) at individual-soma resolution and then match cells to RGC type
by post hoc immunostaining (SPP1 for alphaRGCs, TBR2 for ipRGCs, CART for ooDSGCs) using BigWarp
landmark alignment.

The headline finding is counter-intuitive: the most electrically active RGC type, alphaRGCs, have
**lower** baseline ATP than the other types (ipRGCs and ooDSGCs both higher). The depressed
alphaRGC ATP is not driven by reduced production capacity -- quantitative immunofluorescence shows
alphaRGCs have **higher** mitochondrial and ETC component protein expression -- and is not
abolished by pharmacological silencing, suggesting it reflects an elevated steady-state demand,
possibly from cytoskeletal and large-dendritic-arbor maintenance. ETC inhibitor titrations (ROT,
TTFA, AA, KCN) deplete alphaRGC ATP most severely, and the alphaRGC-selective depletion under
Complex I-III block is rescued by simultaneously blocking glutamatergic input (NBQX/AP5), proving
that activity-driven turnover is the dominant ATP sink during signaling.

A second-order finding bears directly on neurodegeneration: RGCs that survive optic nerve crush
(ONC) over 14 days had **lower** pre-injury homeostatic ATP than RGCs that died, even when
restricted to alphaRGCs or to non-alphaRGCs. ATP transiently rises 2-6 days after ONC before
recovering. For the present project, the key quantitative anchor is that ooDSGCs sit at the upper
end of the homeostatic ATP distribution among the three measured RGC families -- they are not the
most active type, and their ATP demand per cell during in vivo signaling appears modest relative
to alphaRGCs.

## Architecture, Models and Methods

The biosensor is ATeam1.03-nD/nA, a FRET-based reporter where YFP/CFP is monotonic in
intracellular ATP and saturates near 10 mM. Delivery: Cre-dependent AAV2 intravitreal injection in
VGlut2-Cre transgenic C57BL/6J mice (2-6 months old, both sexes), at least 2 weeks before imaging.
Imaging hardware: Scientifica Hyperscope with Mitutoyo 20X 0.4 NA objective, Mai Tai Ti:Sapphire
laser at 850 nm capped at 45 mW at the objective, ChromoFlex GaAsP PMTs, 505 LP dichroic + 535/30
(YFP) and 480/40 (CFP) bandpass filters, ScanImage acquisition. Frames are 512x512 single-plane
raster at 1.07 frames/s. Anaesthesia: ketamine/xylazine induction, 0.5-1% isoflurane maintenance
on 0.5 L/min room air. Pupils dilated with 1% atropine + 2.5% phenylephrine; coverslip-coupled to
the cornea via gel.

Image processing pipeline: ScanImageTiffReader, background subtraction, Suite2p motion correction,
SIFT-based cross-session registration, Cellpose soma segmentation with manual correction,
TrackMate LAP cell matching, 20-frame moving-average filter, then z-score normalisation of YFP/CFP
to baseline population mean/SD. ROIs with fewer than 100 pixels or with mean YFP+CFP under 50 are
discarded. ATP samples per condition: ROT n=264 RGCs / 5 retinas; TTFA n=212/4; AA n=220/4;
KCN n=218/4; Str/Bic n=251/3; NBQX/AP5 n=282/4; light-onset Twitch2B Ca2+ n=2055/13; ONC
longitudinal n=188 RGCs / 3 retinas (survival cohort n=264/5). Confocal mitochondrial protein
quantification (TOM20, NDUFB8, SDHA, UQCRC2, ATP5A) uses Zeiss LSM800/LSM980 with 20X 0.8 NA,
0.2 um z-step volumes from dorsal/ventral/temporal/nasal quadrants ~1000 um from the optic nerve
head, with thousands of RBPMS-segmented cells per stain (TOM20 n=2218, NDUFB8 n=2204, SDHA n=2604,
UQCRC n=2063, ATP5A n=2170).

Pharmacology: rotenone (ROT, Complex I), thenoyltrifluoroacetone (TTFA, Complex II), antimycin A
(AA, Complex III), potassium cyanide (KCN, Complex IV) for ATP-synthesis block;
strychnine + bicuculline (Str/Bic, disinhibition) and NBQX + AP5 (glutamate block) for activity
modulation; all in 1:1 dPBS/DMSO vehicle. ONC: 5-second 2-mm-posterior crush with Dumont #5/45
forceps; longitudinal imaging every 2 days for 14 days. Statistics: ANOVA + Tukey, Kruskal-Wallis
+ Dunn, rank-sum, paired t-test, computed in SciPy/statsmodels/scikit-posthocs/Prism 9. Code
released at `https://github.com/zelunw/RGC-ATP`.

## Results

* alphaRGCs have **lower** baseline YFP/CFP than ipRGCs and ON-OFF DSGCs (Fig 1H, n=349 RGCs /
  5 retinas, ANOVA + Tukey) -- i.e., among the three families measured, **ooDSGCs sit in the
  upper part of the homeostatic ATP distribution**, similar to ipRGCs.
* ON-sustained alphaRGCs (M4 ipRGC overlap, SPP1+TBR2+) sit at alphaRGC-like lower ATP,
  statistically **below** other ipRGC subtypes.
* Repeat-imaging stability: per-cell baseline ATP correlates **R = 0.65** between sessions 7 days
  apart (n=381 RGCs / 7 retinas), confirming heterogeneity is intrinsic rather than measurement
  noise.
* Complex I block (ROT) causes the largest ATP decline in alphaRGCs, especially ON-sustained
  alphaRGCs (Fig 2N,R; n=264/5); Complex II (TTFA n=212/4) and Complex III (AA n=220/4) similarly
  hit alphaRGCs hardest; Complex IV block (KCN n=218/4) depletes ATP across all RGCs uniformly.
* The selective alphaRGC ATP decline under ROT is **rescued by NBQX/AP5 co-injection** (n=349
  RGCs / 4 retinas vs ROT-only n=733/6, Dunn post-hoc significant) -- activity-driven turnover
  causes the alphaRGC-selective drop.
* Pausing 2-photon scanning during ROT restores ATP toward baseline; resumption re-depletes it
  (n=284 RGCs / 3 retinas, ANOVA + Tukey), confirming OXPHOS is required for active signalling
  but **dispensable at rest**.
* alphaRGCs have **higher** mitochondrial / ETC protein expression (TOM20, NDUFB8, SDHA, UQCRC2,
  ATP5A) by quantitative immunofluorescence in thousands of cells (**p < 0.001**, Student t-test);
  lower ATP is therefore **demand-driven, not supply-limited**.
* Str/Bic disinhibition causes population-wide ATP decline that recovers to baseline by 15 min
  despite sustained Ca2+ elevation (n=251/3); relative cross-cell ATP ordering preserved
  (R at 140 s = **0.68**, R at 15 min = **0.80**).
* Physiological activity (2-photon-laser-evoked light response) elevates Ca2+ but produces no
  detectable ATP change (n=485/4) -- intracellular ATP is robust to acute physiological demand
  when OXPHOS is intact.
* Pre-injury baseline ATP is **lower** in RGCs that survive 14 days post ONC than in those that
  die (n=264 RGCs / 5 retinas, paired t-test, p significant); the effect holds separately for
  alphaRGCs and for non-alphaRGCs (one-way ANOVA + Tukey).
* Population ATP **transiently rises** 2-6 days after ONC, peaking at day 4, then recovers
  (n=188/3, rank-sum vs pre).
* Estimated absolute intracellular ATP range across the RGC population is **~2-3.5 mM** difference
  between high- and low-baseline cells, sitting within published 6-10 mM whole-retina estimates
  and ~20 percent of the ATeam dynamic range.

## Innovations

### First in Vivo Per-Type RGC ATP Map

This is the first study to measure homeostatic ATP at single-cell resolution in identified mouse
RGC types in their native circuit. Prior work used whole-retina lysates, ex vivo explants, or
enriched-but-unidentified RGC pools, which cannot resolve per-type metabolic differences within
the shared retinal milieu.

### Activity-Dependent vs Activity-Independent ATP Demand Dissected in Vivo

By combining ETC inhibitors with glutamatergic block (NBQX/AP5) and with light-driven
laser-scanning activity, the authors cleanly separate signalling ATP consumption (rescuable by
NBQX/AP5) from baseline ATP demand (not rescuable). They show OXPHOS is required during
signalling but dispensable at rest -- direct in vivo validation of prior in vitro findings from
the Magistretti and Yellen lines of work.

### Counter-Intuitive Low-ATP-Predicts-Survival Result

By measuring pre-injury per-cell baseline ATP and then tracking the same cells through ONC for
14 days, the study shows that **lower** homeostatic ATP correlates with **better** survival,
contrary to the prevailing assumption that energetic robustness is protective. The result holds
within alphaRGCs and within non-alphaRGCs separately, ruling out a pure type-enrichment
explanation.

### High-Throughput Per-Cell ATP Pipeline

The processing stack -- Cellpose-segmented somas, BigWarp landmark alignment of in vivo and post
hoc confocal stacks, TrackMate LAP cross-session matching, Suite2p motion correction -- yields
hundreds of identified RGCs per retina per condition. Code is released at
`https://github.com/zelunw/RGC-ATP`.

## Datasets

This is a primary experimental study; no public datasets are deposited beyond the analysis code.
Mouse strains used: VGlut2-Cre (JAX 028863) and C57BL/6J (JAX 000664). AAV constructs encode
ATeam1.03-nD/nA and Twitch2B (Ca2+ FRET). The published code repository
(`https://github.com/zelunw/RGC-ATP`) contains the image-processing and quantification pipeline
but no raw image data. RGC type identification uses commercial antibodies for SPP1 (alphaRGCs),
TBR2 (ipRGCs), and CART (ooDSGCs), with RBPMS as a pan-RGC marker. Sample sizes range from
n=188 to n=2604 cells per measurement, drawn from 3-13 retinas per condition.

## Main Ideas

* **ooDSGCs sit at the upper end of homeostatic in vivo ATP** among the three measured RGC
  families (alphaRGCs lowest, ipRGCs and ooDSGCs higher) -- they are **not** the most
  metabolically active RGC type. The empirical hierarchy is alpha < ipRGC ~= ooDSGC, so the
  ATP-per-spike Pareto front for the t0124 DSGC optimization should not be calibrated assuming
  ooDSGCs are extremal energy consumers.
* In vivo activity-driven ATP turnover (signalling load) is the dominant cause of per-cell ATP
  drawdown, while resting-state ATP demand is OXPHOS-independent -- this validates separating
  signalling ATP (Na+/K+-ATPase + Ca2+ handling driven by spikes and synaptic currents) from
  resting leak in any compartmental ATP-per-spike accounting.
* The ~2-3.5 mM intracellular ATP spread across the RGC population, on a 6-10 mM baseline, is a
  usable absolute anchor for the t0124 Pareto front. If the model implied total ATP turnover per
  Pareto-front cell exceeds what these baseline pools can sustain in steady state under measured
  ETC supply (alphaRGC mito-protein intensities are highest, yet baseline ATP is lowest), the
  model is unrealistic.
* Lower homeostatic ATP correlates with better post-ONC survival -- i.e., absolute ATP-per-spike
  budget is not a quality-of-life signal; the relevant constraint is matching the per-type
  empirical baseline, not minimising it. For the DSGC optimization, this argues for using ooDSGC
  ATP as a target band rather than a minimisation objective in its own right.
* The paper provides no direct ATP-per-spike number for any RGC type -- it measures
  **homeostatic** ATP, not turnover. Any t0124 cross-check against this paper must compare
  relative ordering and steady-state intracellular ATP sustainability, not per-spike consumption.

## Summary

Wang et al. address an open question about whether closely related but electrophysiologically
distinct excitatory projection neurons differ in steady-state metabolic homeostasis when they
share a single tissue microenvironment. They use in vivo 2-photon imaging of the ATeam1.03-nD/nA
FRET ATP biosensor in mouse RGCs and exploit post hoc immunostaining (SPP1, TBR2, CART) plus
BigWarp landmark alignment to assign every imaged soma to one of three RGC families: alphaRGCs,
ipRGCs, and ON-OFF DSGCs. The motivation is partly mechanistic (what drives per-type metabolic
differences?) and partly applied (do metabolic traits predict resilience to optic nerve injury?).

Methodologically, the study combines per-cell ATP imaging with pharmacological perturbations:
ETC inhibitors (rotenone, TTFA, antimycin A, KCN) to block ATP synthesis stage by stage; Str/Bic
and NBQX/AP5 to manipulate circuit activity; and a 14-day optic nerve crush followed by
longitudinal imaging. Quantitative confocal microscopy of mitochondrial and ETC protein expression
(TOM20, NDUFB8, SDHA, UQCRC2, ATP5A) on thousands of cells per stain checks whether ATP
differences reflect supply or demand. Image processing relies on Cellpose, Suite2p, TrackMate,
BigWarp and SIFT registration, with code released at `https://github.com/zelunw/RGC-ATP`.

The headline findings: (1) alphaRGCs, the most active type, have **lower** homeostatic ATP than
ipRGCs and ooDSGCs; (2) alphaRGCs are most depleted by Complex I-III block, but Complex IV block
depletes all RGCs equally; (3) silencing activity with NBQX/AP5 rescues alphaRGC ATP decline
under ROT, proving activity-driven turnover dominates; (4) alphaRGCs have **higher**, not lower,
mitochondrial protein expression -- supply is fine, demand is the issue; (5) pre-injury baseline
ATP is **lower** in RGCs that survive ONC, holding for alphaRGCs and non-alphaRGCs separately;
(6) population ATP transiently rises 2-6 days post-ONC. The absolute intracellular ATP spread
across the population is **~2-3.5 mM** on a 6-10 mM baseline.

For the present project, the most actionable result is the **per-type baseline ATP ordering**:
alphaRGC < ipRGC ~= ooDSGC. The user-supplied note that ooDSGCs rank highest matches the
homeostatic intracellular ATP data (ooDSGCs are in the high-ATP group), but the inference that
ooDSGCs are the most active type is incorrect -- alphaRGCs are. For the t0124 Pareto front, this
means (i) ooDSGCs are not the most energy-hungry RGC type per unit time and the optimal
ATP-per-spike landscape should reflect a moderate-activity, moderate-ATP-baseline cell;
(ii) any implied total ATP turnover per Pareto-front DSGC must be sustainable under the measured
steady-state intracellular ATP range (6-10 mM whole-retina; ~2-3.5 mM cell-to-cell spread);
(iii) the paper offers no per-spike ATP number directly, so the cross-check is steady-state
plausibility, not a numerical match. Limitations to flag: the ATeam-FRET signal is bounded by a
10 mM saturation ceiling, activity is operationalised as 2-photon-laser-evoked retinal response
not directional motion, and alphaRGCs include subtypes that themselves differ in ATP. As a 2025
preprint, the paper is "In Review" and the results are not yet peer reviewed.
