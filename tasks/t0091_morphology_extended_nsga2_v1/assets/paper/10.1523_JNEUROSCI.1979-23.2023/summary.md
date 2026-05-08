---
spec_version: "3"
paper_id: "10.1523_JNEUROSCI.1979-23.2023"
citation_key: "Roy2024"
summarized_by_task: "t0091_morphology_extended_nsga2_v1"
date_summarized: "2026-05-08"
---
# GABAergic Inhibition Controls Receptive Field Size, Sensitivity, and Contrast Preference of Direction Selective Retinal Ganglion Cells Near the Threshold of Vision

## Metadata

* **File**: `files/roy_2024_gaba-dsgc-scotopic.pdf`
* **Published**: 2024
* **Authors**: Suva Roy 🇺🇸, Xiaoyang Yao 🇺🇸, Jay Rathinavelu 🇺🇸, Greg D. Field
  🇺🇸
* **Venue**: J Neurosci 44(11):e1979232023 (March 13, 2024)
* **DOI**: `10.1523/JNEUROSCI.1979-23.2023`

## Abstract

Information about motion is encoded by direction-selective retinal ganglion cells (DSGCs). These
cells reliably transmit this information across a broad range of light levels, spanning moonlight to
sunlight. Previous work indicates that adaptation to low light levels causes heterogeneous changes
to the direction tuning of ON-OFF (oo)DSGCs and suggests that superior-preferring ON-OFF DSGCs
(s-DSGCs) are biased toward detecting stimuli rather than precisely signaling direction. Using a
large-scale multielectrode array, we measured the absolute sensitivity of ooDSGCs and found that
s-DSGCs are 10-fold more sensitive to dim flashes of light than other ooDSGCs. We measured their
receptive field (RF) sizes and found that s-DSGCs also have larger receptive fields than other
ooDSGCs; however, the size difference does not fully explain the sensitivity difference. Using a
conditional knock-out of gap junctions and pharmacological manipulations, we demonstrate that
GABA-mediated inhibition contributes to the difference in absolute sensitivity and receptive field
size at low light levels, while the connexin36-mediated gap junction coupling plays a minor role. We
further show that under scotopic conditions, ooDSGCs exhibit only an ON response, but
pharmacologically removing GABA-mediated inhibition unmasks an OFF response. These results reveal
that GABAergic inhibition controls and differentially modulates the responses of ooDSGCs under
scotopic conditions.

## Overview

Roy, Yao, Rathinavelu and Field investigate the cellular and circuit mechanisms that explain why
superior-preferring ON-OFF direction-selective ganglion cells (s-DSGCs) detect dim flashes far more
reliably than the other three cardinal ooDSGC subtypes (anterior, inferior, posterior). They record
from ex vivo dark-adapted mouse retina using a 519-electrode planar MEA covering a 450 um hexagonal
patch, while delivering two stimulus families: brief (2-8 ms) full-field LED flashes spanning ~0.001
to 6.31 R*/rod, and 1 s flashed squares (60 to 160 um per side) at 900% Michelson contrast on
uniform backgrounds from scotopic (0.2 R*/rod/s) to photopic (2000 R*/rod/s).

Using a 2AFC ideal-observer analysis on spike-train responses, the authors quantify each cell
absolute detection threshold (the flash strength yielding 84% correct, SNR = 1). They map RF extent
by fitting 2D Gaussians to spatially-resolved ON and OFF responses, and use a published biophysical
rod-pooling model (linear and Bayesian-nonlinear variants) to predict how RF size should propagate
into 2AFC performance.

The mechanistic dissection uses two interventions. Conditional Cx36 knock-out (FACx mice) ablates
homotypic gap-junction coupling among s-DSGCs while leaving upstream AII-bipolar coupling intact.
Pharmacological GABA-A blockade with 15 uM gabazine (also confirmed not further changed by the
GABA-C antagonist TPMPA) tests the contribution of inhibition. The headline finding: GABAergic
inhibition - not gap junctions - dominates the threshold and RF asymmetry, and additionally masks
ooDSGC OFF responses entirely under scotopic conditions.

The work motivates two new putative GABAergic amacrine cell types in the DSGC circuit: one that
selectively suppresses anterior, posterior, and inferior ooDSGCs at scotopic levels (sparing
s-DSGCs), and another that selectively masks the OFF channel under low light. Critically, the
authors conclude that asymmetric inhibition cannot come from the classical starburst amacrine cell,
because the inhibition is not direction-tuned, depends on light level, and differs across ooDSGC
subtypes.

## Architecture, Models and Methods

**Animals and tissue**: C57BL/6J wild-type mice and FACx (conditional Cx36 knock-out specific to
s-DSGCs, from Awatramani lab) of either sex, 2-12 months old. Dark-adapted overnight, decapitated
under infrared, dorsal peripheral retina mounted ganglion-cell-down on the MEA in carbogenated Ames
solution at 30-32 C, pH 7.4.

**Recording**: 519-electrode hexagonal MEA, 30 um inter-electrode spacing, 450 um per side. Spike
sorting via voltage thresholding plus 5D PCA Gaussian-mixture clustering; clusters with >10%
refractory contamination or <100 spikes excluded; duplicate units (>25% shared spike times) removed.
Electrical images (1 ms pre-, 3 ms post-spike voltage averages) used to determine the dorsal-ventral
axis from RGC axon trajectories and to track cells across stimulus conditions.

**Stimuli**: (1) gamma-corrected OLED at 60.35 Hz delivering flashed squares 60x60 to 160x160 um at
900% Michelson contrast for RF mapping; (2) drifting gratings, 8 directions, 24-2400 um/s, spatial
period 960 um (49.2 deg visual angle), 50% contrast, 8 s per presentation with 2 s gray intervals,
3-4 repeats; (3) 490 nm LED full-field flashes (2-8 ms) over a 4 mm circular field for
absolute-sensitivity measurement; 60 repeats per intensity at 3 s ISI, presented dim-to-bright to
avoid adaptation of the most sensitive cells. "No flash" trials drawn from 60 segments of 3 s
spontaneous activity recorded at the start of each session.

**2AFC ideal-observer analysis**: Each trial spike train binned at 20 ms; a difference-of-means
linear discriminant fit per flash strength on a training subset; held-out flash and no-flash trials
compared by dot product against the discriminant. Performance fit by Naka-Rushton: Pc = 0.5 * C^n /
(C^n + C50^n) + 0.5. Detection threshold = flash strength giving Pc = 0.84 (SNR = 1). Cells whose
curves never crossed 0.84 were excluded.

**Rod-pooling model**: Field 2019 biophysical rod model with continuous dark noise (Gaussian
filtered to match measured power spectrum), Poisson-distributed single-photon responses with mean
rm(t) and covariance from eigenvector decomposition, and Poisson thermal isomerizations at 0.005
R*/rod/s. Mouse-specific corrections: continuous noise +22%, single-photon variability +37.5%
relative to primate. RF area mapped to rod count via 500,000 rods/mm^2 mouse rod density; 12,000
rods for ooDSGCs (RF sigma 0.012 mm^2) and 96,000 rods for s-DSGCs (8x larger). Linear pooling =
optimal linear discriminant from 5,000 simulated single-photon vs 5,000 dark-noise trials. Nonlinear
pooling = same dot product weighted by Bayesian likelihood ratio between single-photon and
continuous-noise distributions, with flash strength acting as the prior.

**Pharmacology**: 15 uM gabazine (SR-95531, GABA-A blocker), 5 min wash-in / 30 min wash-out; TPMPA
tested for GABA-C (no additional effect).

**Statistics**: One-way and two-way ANOVA with Bonferroni correction; mean +/- SEM unless noted;
significance threshold p <= 0.05.

## Results

* s-DSGCs detect dim flashes at **~10-fold lower threshold** than anterior, inferior, and posterior
  ooDSGCs (p < 0.001, one-way ANOVA Bonferroni; data from 2 retinas, n=31 superior, n=29 anterior,
  n=10 inferior, n=5 posterior).
* s-DSGC absolute thresholds approach within **~0.5 log unit** of the most sensitive RGCs recorded
  (likely ON sustained alpha cells, **~3-fold gap**).
* s-DSGCs have larger ON RFs than other ooDSGCs across all light levels; the difference is maximal
  at scotopic 0.2 R*/rod/s with **ON ratio ~8.4x and OFF ratio ~4.0x**, narrowing to **ON ~3.1x and
  OFF ~2.3x** at photopic 2000 R*/rod/s.
* Linear rod-pooling predicts only a **sqrt(8) ~ 3-fold** sensitivity gain from an 8-fold RF area
  increase; optimal Bayesian-nonlinear pooling with mouse rod noise yields only a **~70%**
  performance gain between 12,000 and 96,000 rods. RF size therefore explains roughly **half** of
  the observed 10-fold threshold difference.
* Locally flashed in-RF spots elicit higher gain in s-DSGCs than other ooDSGCs at 0.2 R*/rod/s: ON
  peak **34.5 +/- 1.4 vs 22.4 +/- 5.9 spike/s**, OFF peak **15.4 +/- 1.0 vs 6.0 +/- 2.4 spike/s**.
* Cx36 ablation in FACx s-DSGCs leaves absolute threshold unchanged (p = 0.61 superior, p = 0.32
  others) and produces only a modest s-DSGC RF reduction (p = 0.03), with no change in other ooDSGCs
  (p = 0.35). Gap junctions are therefore a **minor** contributor.
* GABA-A blockade with gabazine reduces the s-DSGC vs other-ooDSGC threshold ratio from **9.4-fold
  to 3.2-fold** (p < 0.001 superior, p = 0.003 others; control n=15 superior, n=15 anterior, n=10
  inferior, n=5 posterior). All ooDSGC types become more sensitive in absolute terms.
* Gabazine increases ON RF area by **~40% in s-DSGCs and ~75% in other ooDSGCs**, and OFF RF area by
  **~10x in s-DSGCs and ~30x in other ooDSGCs** under scotopic 0.2 R*/rod/s.
* GABA-A blockade unmasks a previously absent OFF response of similar amplitude to the ON response
  under scotopic conditions, demonstrating that inhibition gates contrast polarity at low light
  levels.
* Density estimates of **~80 s-DSGCs/mm^2 (Hb9)** vs **~130 posterior-DSGCs/mm^2 (DRD4)** match the
  photopic 1.5x RF-size ratio, implying similar coverage factors across types under photopic but
  **coverage ~3 for s-DSGCs and <1 for other ooDSGCs** under scotopic conditions.

## Innovations

### Quantitative Decomposition Of S-DSGC Sensitivity Excess

First study to combine MEA-wide threshold measurements, RF mapping across six log units of
background light, and a calibrated biophysical rod-pooling model in the same animal preparation. The
decomposition shows that the well-known ~10-fold s-DSGC absolute-sensitivity advantage is not
explained by RF size alone (which a fully optimised nonlinear pool predicts to give only ~70% gain)
and is dominated instead by GABAergic inhibition asymmetry.

### Conditional Cx36 Knockout As A Selective Coupling Probe

Use of FACx (Awatramani lab) mice as a clean dissociation between s-DSGC homotypic gap-junction
coupling and upstream AII / cone-bipolar coupling. This allows the authors to rule out the common
assumption that homotypic coupling drives the s-DSGC sensitivity advantage. The absence of a
threshold effect in FACx is the strongest direct evidence to date that Cx36 plays only a secondary
role in scotopic absolute sensitivity for these cells.

### GABA-A As A Polarity Gate Under Scotopic Conditions

Demonstration that gabazine unmasks a full-amplitude OFF response in ooDSGCs that is otherwise
absent at scotopic light levels. This reframes the Pearson and Kerschensteiner 2015 observation of
an "ON-only ooDSGC under scotopic conditions" as actively maintained by GABAergic masking, not by a
missing OFF input. The result implies a putative second GABAergic amacrine cell that targets the OFF
subfield (or its OFF bipolar inputs) selectively at low light.

### Two-Amacrine-Cell Hypothesis For Scotopic DSGC Circuitry

Synthesis of the threshold-asymmetry and OFF-masking results into an explicit hypothesis (their Fig.
7\) that two yet-unidentified GABAergic amacrine cell types exist in the DSGC circuit: one that
suppresses inferior, posterior, and anterior ooDSGCs sparing s-DSGCs, and one that masks the OFF
channel of all ooDSGCs. The authors explicitly rule out starburst amacrine cells as the source on
three grounds (no direction tuning, light-level dependence, subtype asymmetry).

## Datasets

This is a primary experimental study with no public dataset. Data are recordings from ex vivo mouse
retina:

* **C57BL/6J wild-type retinas**: ~5 retinas across the experiments. Threshold measurements pool 2
  retinas (n = 31 superior, 29 anterior, 10 inferior, 5 posterior). RF measurements use 2 retinas (n
  = 23 superior, 30 other). Gabazine experiments use 2 retinas (n = 15 superior, 15 anterior, 10
  inferior, 5 posterior; replicated in a third retina).
* **FACx Cx36 conditional knock-out**: 1 retina for thresholds (n = 14 superior, 9 anterior, 2
  inferior, 1 posterior); 2 retinas for RF size (n = 12 superior, 15 other).
* **MEA recordings**: 519-channel hexagonal Litke-style array, 30 um pitch, 450 um per side,
  spike-sorted offline with 5D PCA mixture-of-Gaussians.
* No raw datasets are released alongside this paper.

## Main Ideas

* The classical starburst-amacrine direction-selective microcircuit cannot account for ooDSGC
  scotopic asymmetry. There is a separate non-starburst GABAergic amacrine population whose density
  / strength must vary across the ooDSGC subtypes - relevant when interpreting model GABA priors at
  scotopic vs photopic operating points.
* Under photopic stimulation (the regime t0091 NSGA-II sweep targets), the s-DSGC vs other-ooDSGC
  RF-size ratio shrinks to ~1.5-3x and density-corrected coverage factors equalise. This supports
  the project existing single-photopic operating point assumption and the Trenholm 2013 photopic
  peak-rate prior.
* The Roy 2024 result is about *threshold sensitivity* and *RF size at scotopic levels*, not channel
  densities or per-spine NMDA conductance. It does NOT change the t0086 / t0088 scorecard GABA
  spatial-gradient or per-spine NMDA priors used in t0091.
* Gap-junction coupling among s-DSGCs is functionally minor for absolute sensitivity (FACx knockout
  = no threshold change), so gap-junction-mediated lateral spread can be safely omitted from t0091
  single-cell model under photopic conditions.
* The OFF subfield of ooDSGCs is actively suppressed by GABA-A inhibition at scotopic levels. This
  is a *low-light* phenomenon irrelevant to the project photopic regime but worth flagging if a
  future task extends the model to scotopic operating points.

## Summary

Roy, Yao, Rathinavelu, and Field address the long-standing observation that superior-preferring
ON-OFF DSGCs (s-DSGCs) detect dim stimuli substantially more reliably than the three other cardinal
ooDSGC subtypes (anterior, inferior, posterior). The paper asks two questions: how large is the
s-DSGC sensitivity advantage at the absolute threshold of vision, and which of three plausible
mechanisms (RF size, Cx36 gap-junction coupling, GABAergic inhibition asymmetry) account for it? The
motivation comes from prior work (Yao et al. 2018) suggesting s-DSGCs sacrifice direction-tuning
precision for stimulus detection at scotopic levels.

The authors record dark-adapted mouse retina ex vivo on a 519-electrode MEA, using brief full-field
LED flashes (2-8 ms) and spatially mapped square flashes (60-160 um, 900% contrast) across
backgrounds spanning six log units of light intensity. They quantify absolute thresholds with a 2AFC
ideal-observer analysis (84% correct = SNR = 1, Naka-Rushton fit) and RF area by 2D-Gaussian fits to
ON / OFF subfield maps. A calibrated rod-pooling model with mouse-specific noise parameters and
0.005 R*/rod/s thermal isomerization rate is used to translate RF area into predicted 2AFC
performance. The mechanistic dissection uses FACx conditional Cx36-knockout mice to ablate s-DSGC
homotypic coupling, and 15 uM gabazine to block GABA-A inhibition.

The headline result is a **10-fold lower s-DSGC absolute threshold** that approaches within 0.5 log
unit of the most sensitive RGCs (presumed ON sustained alpha cells). RF size differences (~8x larger
ON subfields at scotopic 0.2 R*/rod/s) explain only **~50%** of the gap, even under optimal
nonlinear rod pooling. Cx36 ablation has **no significant effect** on threshold and only a modest RF
reduction in s-DSGCs. GABA-A blockade compresses the s-DSGC vs other-ooDSGC threshold ratio from
**9.4x to 3.2x**, expands all ooDSGC RFs (especially OFF subfields by 10-30x), and unmasks a
full-amplitude scotopic OFF response. The authors conclude that two unidentified GABAergic amacrine
cells differentially shape ooDSGC sensitivity, RF size, and contrast polarity at low light, and
explicitly exclude starburst amacrine cells as the source.

For this project (t0091 morphology / NSGA-II Pareto-front sweep under photopic stimulation), the
paper supplies critical context but no parameter changes. Under photopic conditions the s-DSGC
RF-size advantage collapses to 1.5-3x with similar coverage factors across types, supporting the
project existing single-cell, single-operating-point Pareto framing using Trenholm 2013-style
photopic peak rates. The GABA spatial-gradient prior on the t0086 / t0088 scorecard is about
classical-RF SAC-mediated inhibition; Roy 2024 two hypothesised non-starburst GABAergic amacrine
cells operate at scotopic levels and are out of scope. Cx36 gap-junction coupling can safely be
excluded from the photopic single-cell model. The paper is therefore most useful as an interpretive
boundary - it confirms that t0091 photopic-only NSGA-II results should not be overgeneralised to
scotopic firing-rate predictions, where additional GABAergic and OFF-masking mechanisms would
dominate.
