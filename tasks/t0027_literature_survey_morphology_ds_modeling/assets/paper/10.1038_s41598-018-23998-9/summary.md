---
spec_version: "3"
paper_id: "10.1038_s41598-018-23998-9"
citation_key: "Dan2018"
summarized_by_task: "t0027_literature_survey_morphology_ds_modeling"
date_summarized: "2026-04-21"
---
# Non-uniform weighting of local motion inputs underlies dendritic computation in the fly visual system

## Metadata

* **File**: `files/dan_2018_vs-cells-dendritic-weighting.pdf`
* **Published**: 2018-04-10
* **Authors**: Ohad Dan 🇮🇱, Elizabeth Hopp 🇩🇪, Alexander Borst 🇩🇪, Idan Segev 🇮🇱
* **Venue**: Scientific Reports 8:5787 (journal)
* **DOI**: `10.1038/s41598-018-23998-9`

## Abstract

The fly visual system offers a unique opportunity to explore computations performed by single
neurons. Two previous studies characterized, in vivo, the receptive field (RF) of the vertical
system (VS) cells of the blowfly (calliphora vicina), both intracellularly in the axon, and,
independently using Ca2+ imaging, in hundreds of distal dendritic branchlets. We integrated this
information into detailed passive cable and compartmental models of 3D reconstructed VS cells.
Within a given VS cell type, the transfer resistance (TR) from different branchlets to the axon
differs substantially, suggesting that they contribute unequally to the shaping of the axonal RF.
Weighting the local RFs of all dendritic branchlets by their respective TR yielded a faithful
reproduction of the axonal RF. The model also predicted that the various dendritic branchlets are
electrically decoupled from each other, thus acting as independent local functional subunits. The
study suggests that single neurons in the fly visual system filter dendritic noise and compute the
weighted average of their inputs.

## Overview

This paper asks how hundreds of local motion-sensitive dendritic inputs onto a single blowfly
(*Calliphora vicina*) VS (vertical-system) tangential cell are integrated into a single axonal
direction-selective receptive field. The authors combine two pre-existing *in vivo* datasets —
intracellular axonal recordings by Wertz et al. (2009) and dendritic Ca2+ imaging of up to ~116
branchlet receptive fields per cell type by Hopp et al. — and map both onto six 3D-reconstructed
prototypical morphologies (VS1, VS2, VS3, VS4, VS5, VS9). They then ask whether the axonal receptive
field can be reconstructed from the dendritic receptive fields under a pure passive cable model with
no free fitting parameters beyond the published Rm and Ri.

**Important correction note for this literature survey**: this paper does NOT perform a
morphology-variant sweep. It uses **6 fixed prototypical VS-cell reconstructions** and analyses how
passive cable transfer resistance from each dendritic branchlet to the axon weights the contribution
of that branchlet to the axonal receptive field. The original task brief had it listed as "Haag2018
— 200 morphology variants"; that attribution was wrong — the paper is by Dan, Hopp, Borst and Segev
(2018), not Haag, and it is a single-morphology-per-cell-type passive cable analysis, not a
morphology sweep. It is included as a borderline entry in the survey as a **passive-cable /
dendrite-as-weighted-summator** reference, NOT as a morphology-sweep reference. The organism is an
invertebrate (blowfly), so translation to vertebrate retinal DSGC modelling requires care.

The key finding is that the axonal RF is well-approximated not by a simple linear sum of dendritic
branchlet RFs (as a uniform-weight null model would predict), but by a sum weighted by each
branchlet's transfer resistance to the axon, plus a threshold non-linearity that removes small
(noise-level) dendritic vectors. The dendritic branchlets are shown to be electrically decoupled and
therefore operate as essentially independent functional subunits.

## Architecture, Models and Methods

The model is a steady-state passive cable / compartmental model of six 3D-reconstructed VS cells
(VS1, VS2, VS3, VS4, VS5, VS9), implemented in NEURON. Passive parameters are fixed throughout at
**Rm = 2,000 Ω·cm²** and **Ri = 40 Ω·cm** (from Borst and Haag measurements). Because the analysis
is steady-state, membrane capacitance Cm does not enter numerically — the authors explicitly drop
the time-dependent term of Rall's one-dimensional cable equation, justified by the measured
effective VS-cell membrane time constant being less than 2 ms, which is very short relative to the
timescale of motion-detector input. Morphological analysis uses the TREES toolbox. The models are
deposited in ModelDB, accession 231815.

For each branchlet in each reconstructed cell, the authors compute (i) the electrotonic distance x/λ
from branchlet to the axonal measurement point, (ii) the local input resistance at the branchlet
(V/I measured at the branchlet itself), and (iii) the **transfer resistance** TR = V_axon /
I_branchlet, i.e. the steady-state voltage at the axonal measurement point in response to unit
current injected at the branchlet. Because the system is passive and reciprocal, TR(i,j) = TR(j,i),
so inter-branchlet coupling can be represented by a triangular matrix.

Dendritic inputs are represented as steady currents, each carrying one local RF vector map of 50
preferred-direction vectors (covering 50 non-overlapping visual-field locations). Predicted axonal
RFs are formed either by uniform average ∑RF_i / n (null model) or by transfer-resistance weighted
average ∑w_i·RF_i / ∑w_i where w_i is the branchlet's TR. Optionally, a linear-nonlinear threshold
filters out the smallest α-percentile of vectors at each branchlet. Fit quality is quantified by a
**difference index (DI)** — average Euclidean distance between predicted and measured RF vectors at
50 matched locations; DI = 0 is perfect match, DI = 2 is the theoretical maximum. Significance of
the TR-weighted fit is assessed against a null distribution built by randomly re-shuffling the TR
weights across branchlets and recomputing the DI. Dendritic-branchlet receptive field measurements
from several specimens (2 cells for VS3, 8 cells for VS4, 3 cells for VS5) were superimposed onto
single prototypical morphologies, yielding 17, 116 and 39 branchlet RFs respectively.

## Results

* **Transfer resistance is highly non-uniform across branchlets within one VS cell**: for VS3,
  branchlet-to-axon TR values range over roughly a factor of 20% across the tree, with example
  values of **2.92 MΩ** (branchlet #6, electrotonically close) and **2.47 MΩ** (branchlet #12, more
  distal); across cell types the branchlet-to-axon TR spans **2.4–3.0 MΩ**.
* **Axon input resistance** (V_axon / I_axon) is **4.6 MΩ** for the modelled VS3 cell.
* **Branchlet input resistance** ranges from **8 to 13 MΩ** (with the largest value ~13.2 MΩ in
  VS4), whereas **inter-branchlet transfer resistance** ranges from only **3 to 4 MΩ**, so
  branchlets are ~3x more strongly coupled to themselves than to each other — they are
  **electrically decoupled and act as independent functional subunits**.
* **Electrotonic distance (x/λ)** of distal terminals to the axonal measurement point: VS1 **0.83 ±
  0.15**, VS2 **0.37 ± 0.16**, VS3 **0.71 ± 0.15**, VS4 **0.54 ± 0.13**, VS5 **0.84 ± 0.14**, VS9
  **0.60 ± 0.22**; distal branchlets lie around ~0.6 λ from the axon.
* **Morphology counts** (from six 3D reconstructions, TREES toolbox): total dendritic length per
  cell ~4,000–7,000 μm, total membrane area 32,000–60,000 μm², **average 449 ± 194 branchlets per
  cell**, average branchlet diameter 1.02 ± 0.18 μm, terminal diameters ~0.59 μm.
* **VS3 has more than 200 dendritic terminals** spanning up to **~600 μm** from the axon.
* **Reducing Rm** disproportionately lowers inter-branchlet transfer resistance versus local input
  resistance (input resistance drops by factor 0.70, inter-branchlet TR by factor 0.48), i.e.
  smaller Rm ⇒ **more decoupled branchlets**.
* **Fit to experimental axonal RF** (difference index, lower = better): for VS5 uniform weighting
  gives **DI = 0.411**, TR-weighted summation gives **DI = 0.293**; the improvement exceeds **2 SD**
  of the shuffled-weight null distribution in both VS3 and VS5, confirming TR is the correct
  weighting.
* **Adding the noise-filter non-linearity** (threshold on smallest vectors) drives the DI down
  further: **VS3 DI = 0.283, VS4 DI = 0.236, VS5 DI = 0.280**. For VS4 specifically: uniform =
  0.411, weighted-only = 0.316, filter-only = 0.27, **weighted + filtered = 0.236**, showing the two
  mechanisms are approximately additive.
* **>95% of the 239 analyzed branchlet RFs** have only 1 or 2 vectors larger than 0.7 (on a scale
  normalized to 1); in all but one, at least 80% of the 50 vectors have magnitude < 0.4 — i.e. each
  branchlet is dominated by one to two preferred-direction locations and is noise elsewhere,
  motivating the threshold filter.

## Innovations

### Transfer-resistance weighting as the canonical dendrite-to-axon integration rule

The paper's central contribution is formalizing and quantitatively testing the rule that the axonal
receptive field of a fly VS cell equals the **transfer-resistance-weighted sum** of its
dendritic-branchlet receptive fields, rather than a uniform sum. The null test (shuffled TR weights)
makes the claim falsifiable and the 2+ SD separation from the null distribution makes it convincing.

### Branchlets as independent functional subunits

By computing the full triangular inter-branchlet TR matrix and showing it is much smaller than the
local input resistance at each branchlet, the paper provides a clean, quantitative demonstration
that VS-cell dendrites implement an **independent-subunit architecture** — each branchlet is an
isolated local processor whose output is routed to the axon with its own (unequal) gain. This is a
concrete example of the "dendrite as layer of sub-linear processors" concept realized in an
invertebrate visual neuron.

### Noise-filter non-linearity motivated by sparse dendritic RFs

The observation that each branchlet RF is dominated by 1–2 large vectors plus many small vectors
motivates a threshold non-linearity (discard bottom α-percentile). This turns each branchlet into a
**denoising local feature detector**, and when combined with TR weighting reproduces the axonal RF
with DI ≈ 0.24–0.28 — close to the inter-specimen limit.

### Superposition of branchlets across specimens onto a single prototype

To overcome the small number (~13) of branchlets accessible in a single *in vivo* experiment, the
authors register dendritic RFs from multiple specimens onto a single prototypical reconstructed
morphology per cell type, exploiting VS-cell stereotypy. This yields up to **116 branchlet RFs on a
single VS4 prototype** from 8 specimens — a methodological trick that underlies the statistical
power of the paper.

## Datasets

* **VS-cell 3D morphological reconstructions**: six prototypical VS cells (VS1, VS2, VS3, VS4, VS5,
  VS9), publicly available on ModelDB (accession **231815**). These are not a population sweep —
  **one canonical morphology per cell type**, 6 cells total.
* **Dendritic-branchlet Ca2+ imaging receptive fields**: from Hopp et al.; 17 branchlet RFs from 2
  VS3 specimens, 116 from 8 VS4 specimens, 39 from 3 VS5 specimens. Each RF is a vector map at 50
  non-overlapping visual-field locations.
* **Axonal intracellular recording receptive fields**: from Wertz et al. 2009; one axonal RF per
  VS-cell type at 50 matched locations, used as ground truth.
* **Tools**: NEURON (compartmental simulation, Impedance class), TREES toolbox (morphometric
  analysis), custom Matlab R2014b code (registration, vector-map statistics, DI computation).
* No new experimental data is collected in this paper — it is a **modelling re-analysis** of
  previously published datasets. All data and models are redistributable via the cited ModelDB
  entry.

## Main Ideas

* The correct passive-cable rule for integrating many dendritic direction-selective inputs onto a
  single axonal DS output is a **transfer-resistance-weighted sum** — the equal-weight linear sum is
  a non-trivially inferior approximation. This is directly relevant to any compartmental DSGC model
  where many dendritic BC or SAC inputs converge on a single output: TR weighting, not equal
  weighting, is the default expectation.
* **Inter-branchlet electrical decoupling** (local input resistance ≫ inter-branchlet TR) is the
  structural condition that makes branchlets behave as independent functional subunits. For
  vertebrate DSGC dendritic subunit hypotheses, this paper provides a quantitative template for how
  to test subunit independence with purely passive cable measurements — no active conductances
  needed.
* Even with fixed Rm = 2000 Ω·cm² and Ri = 40 Ω·cm and a steady-state passive model (no Cm, no
  active channels), one can recover the axonal RF to DI ≈ 0.24–0.29; **morphology plus passive cable
  plus a simple threshold non-linearity already explains most of the direction-selectivity
  integration**. More complex active models should be added only if they measurably beat this
  baseline.
* **Borderline inclusion note for this task**: this paper is an **invertebrate passive-cable
  reference**, not a morphology-sweep paper. Use it to justify TR-weighted summation and
  independent-subunit framing, not to justify morphology-variant analyses. If a morphology sweep is
  the target, this paper supports the *null-model* (uniform-weight) rejection but does not itself
  provide a morphology-variant dataset.

## Summary

Dan, Hopp, Borst and Segev (2018) resolve the long-standing question of how the ~400–600
motion-sensitive dendritic branchlets of a blowfly VS tangential cell are integrated into the cell's
single direction-selective axonal output. They combine two prior *in vivo* datasets — axonal
intracellular recordings and branchlet-level Ca2+ imaging — and fuse them onto six prototypical 3D
reconstructions of VS1, VS2, VS3, VS4, VS5 and VS9 cells by exploiting the morphological stereotypy
of VS cells across specimens. The fused dataset yields up to 116 local receptive fields on a single
prototype, enabling the first quantitative test of the rule by which dendritic RFs are combined into
the axonal RF.

The methodology is a steady-state passive cable / compartmental model in NEURON with fixed Rm =
2,000 Ω·cm² and Ri = 40 Ω·cm and no free parameters. For each branchlet they compute the
electrotonic distance (x/λ), the local input resistance (8–13 MΩ), and — crucially — the
branchlet-to-axon transfer resistance (2.4–3.0 MΩ range, ~20% variability within a cell). They then
compare two integration rules against the experimentally measured axonal receptive field: uniform
average (the null model from Hopp et al.) versus transfer-resistance-weighted average. A
supplementary threshold non-linearity that filters out the smallest dendritic vectors is added on
top.

The headline result is that TR-weighted summation significantly outperforms uniform summation: for
VS5 the difference index drops from 0.411 to 0.293, with the improvement exceeding 2 SD of a
shuffled-weights null distribution. Adding the non-linearity improves the fit further to DI = 0.283
(VS3), 0.236 (VS4), 0.280 (VS5). Separately, the full inter-branchlet TR matrix (3–4 MΩ) is much
smaller than the local branchlet input resistance (8–13 MΩ), establishing that VS-cell dendritic
branchlets are **electrically decoupled and function as independent local subunits**. The effective
membrane time constant (<2 ms) is much shorter than the motion-detector input timescale, validating
the steady-state approximation.

For this literature survey, the paper is included as a borderline entry: it is a single-
morphology-per-cell-type passive-cable study of an invertebrate visual neuron, not a
morphology-variant sweep (the earlier task brief mis-attributed it as "Haag2018 — 200 morphology
variants", which was wrong). It is nonetheless a strong reference for (a) transfer-resistance
weighting as the correct passive rule for many-to-one dendritic integration, (b) the
independent-subunit architecture as a passively-derivable property of dendritic trees, and (c) the
methodological pattern of fusing branchlet-level imaging across specimens onto a prototypical
morphology. Translation to vertebrate retinal DSGCs requires adjusting for active dendritic
mechanisms and gap-junctional network effects (the authors flag axo-axonal coupling between
neighboring VS cells, coupling coefficients up to 50%, as one reason their fit is not perfect), but
the core TR-weighting result is a morphology-agnostic passive-cable prediction that any
compartmental DSGC model should reproduce as a baseline before invoking active conductances.
