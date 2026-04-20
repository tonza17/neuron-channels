---
spec_version: "1"
task_id: "t0009_calibrate_dendritic_diameters"
research_stage: "papers"
papers_reviewed: 10
papers_cited: 9
categories_consulted:
  - "compartmental-modeling"
  - "cable-theory"
  - "dendritic-computation"
  - "direction-selectivity"
  - "retinal-ganglion-cell"
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Replace the uniform 0.125 µm placeholder radii in the CNG-curated SWC of mouse ON-OFF DSGC
`141009_Pair1DSGC` (NeuroMorpho neuron 102976, the project's `dsgc-baseline-morphology` dataset)
with a literature-derived diameter taper keyed on Strahler order or path distance from the soma,
preserving topology and the non-placeholder 19 soma compartments, and register the result as
`dsgc-baseline-morphology-calibrated` [t0005Asset]. The review below identifies which papers in the
project corpus supply defensible per-order or per-location DSGC dendritic diameters and how their
reported morphometric or compartmental-model values should be mapped onto our CNG tree.

## Category Selection Rationale

I consulted five `meta/categories/` slugs: `compartmental-modeling` (the taper rule must produce a
geometry that cable-theory simulators can use and is cited by previously published NEURON/NeuronC
DSGC models), `cable-theory` (the diameter distribution drives axial resistance and electrotonic
length constants directly), `dendritic-computation` (DSGC direction selectivity depends on
dendritic-subunit electrotonic isolation, which is a direct function of segment diameter),
`direction-selectivity` (the target cell type is the mouse ON-OFF DSGC so every paper with DSGC
morphometric or biophysical-model data must be consulted), and `retinal-ganglion-cell` (broader RGC
morphometric and passive-property constraints when DSGC-specific numbers are unavailable). The
entire project paper corpus is deposited in `t0002_literature_survey_dsgc_compartmental_models`; no
other task folder holds papers. I excluded `voltage-gated-channels`, `synaptic-integration`, and
`patch-clamp`-only papers unless they also reported dendritic diameter or compartmental geometry.
`project/description.md` calls out Poleg-Polsky & Diamond 2016 (ModelDB 189347) and the
Vaney/Sivyer/Taylor 2012 review as the primary candidate sources; both were reviewed in full.

## Key Findings

### No DSGC-specific per-order diameter taper is published in the corpus

None of the reviewed papers reports a numeric per-Strahler-order or per-path-distance diameter table
for the mouse ON-OFF DSGC of this lineage. `dsgc-baseline-morphology`'s own description states
plainly that the Simple Neurite Tracer source "did not record diameters" and that all CNG SWC radii
are a default 0.125 µm that "should not be used as biophysical inputs without re-measurement"
[t0005Asset]. The foundational review [Vaney2012] fixes DSGC geometry qualitatively — bistratified
dendrites, ~150-200 µm arbor radius per sublamina, ~40 µm subunit spacing — but does not
enumerate segment diameters. Oesch, Euler & Taylor 2005 [Oesch2005] give the one scalar anchor I
found for DSGC dendritic calibre: "~0.5 µm dendritic diameters" (cited to justify why distal
dendritic patch is impractical in DSGCs). This ~0.5 µm figure is substantially thicker than the
0.25 µm diameter (0.125 µm radius) placeholder in the CNG SWC, so any re-calibration will thicken,
not thin, the model.

### Poleg-Polsky & Diamond 2016 (ModelDB 189347) is the primary per-compartment source

The most directly reusable diameter profile in the corpus is the multicompartmental NEURON model of
Poleg-Polsky & Diamond 2016 [PolegPolsky2016], distributed on ModelDB under accession 189347. The
paper documents a "morphologically realistic reconstruction of one DRD4 DSGC" that the model's .hoc
geometry files list explicitly: somatic, primary-dendrite, and terminal-dendrite diameters are
specified per section, not uniformly 0.25 µm. Subsequent NEURON studies have reused this exact
geometry: Hanson et al. 2019 [Hanson2019] built on the Poleg-Polsky morphology, parametrised it at
Cm = 1 µF/cm², Ra = 100 Ω·cm, and reported distinct soma/primary/terminal conductance densities
(Na 150/150/30 mS/cm², K rectifier 70/70/35 mS/cm², delayed rectifier 3/0.8/0.4 mS/cm²) — a
partition that only makes physiological sense if the three compartments have distinct diameters.
Jain et al. 2020 [Jain2020] likewise re-used "the Poleg-Polsky & Diamond 2016" reconstruction,
quoting soma/primary/terminal Na = 150/200/30 mS/cm², K rectifier = 35/35/25 mS/cm², and 700
recorded dendritic compartments in its NEURON build.

### Three-compartment partition is the community convention for mouse ON-OFF DSGCs

Every NEURON DSGC model in the corpus that predates this project uses the same coarse dendritic
partition: soma, primary (proximal) dendrite, and terminal (distal) dendrite
[PolegPolsky2016, Hanson2019, Jain2020]. The Schachter et al. 2010 NeuronC model for rabbit DSGC
uses the same three-bin structure (soma, proximal, distal), quotes Ra = 110 Ω·cm, Rm = 10-22
kΩ·cm², and reports that the partition yields input resistances of "~150-200 MΩ on proximal
dendrites" and ">1 GΩ at distal tips" [Schachter2010]. That dendritic input-resistance gradient is
the key electrotonic property the taper rule must reproduce — since input resistance scales with
d^(-3/2) for a cylindrical cable, the ~5-10x Rin ratio (proximal to distal) is consistent with a
diameter ratio on the order of 3-4x between primary and terminal dendrites.

### Strahler order is a stable mapping onto the three-compartment convention

Strahler order on a CNG-curated tree cleanly separates terminal dendrites (order 1), mid-branch
dendrites, and primary dendrites (highest order, adjacent to soma). Because the corpus models
describe only three dendritic bins, we can apply a Strahler-order-based rule with: order 1 =
terminal (thinnest), intermediate orders = mid (graded), maximum order = primary (thickest). This
preserves topology (required by the task's "connectivity unchanged" validation criterion) and
matches the soma/primary/terminal split that every reusable community model assumes
[PolegPolsky2016, Hanson2019, Jain2020, Schachter2010]. The alternative — keying on path distance
from the soma — gives a continuous taper but is more sensitive to sparse-branch artefacts in the
CNG tree (1,536 µm total path length distributed over 6,717 dendritic compartments).

### Fohlmeister 2010 provides broader RGC passive-property baselines

For sanity-checking the post-calibration passive properties, Fohlmeister et al. 2010
[Fohlmeister2010] fits compartmental channel-density maps to several RGC types (rat Type I / Type
II, cat alpha / beta) under Rm = 40 kΩ·cm², Cm = 1 µF/cm², Ri = 100 Ω·cm. Note that this Rm
value is higher than Schachter2010's DSGC-specific 10-22 kΩ·cm², so any reuse of Fohlmeister's
numbers should be restricted to the Ri = 100 Ω·cm axial-resistivity anchor, which agrees with
every DSGC model in the corpus [PolegPolsky2016, Hanson2019, Schachter2010].

### SAC-model precedent for "measured dendritic diameters + multiplicative scaling"

Ding et al. 2016 [Ding2016] — the Helmstaedter-lab mouse vs. rabbit SAC connectomics paper —
used a Neuron-C network model with "a digitized SAC morphology with multiplicative diameter factors
from EM measurements". This is the strongest cross-task precedent for the approach this task should
adopt: take a morphology with reliable topology, keep the topology, and impose diameters from an
external source (literature or EM) using a multiplicative factor per compartment class. We should
copy that pattern, substituting Strahler-order class for the SAC's proximal/medial/distal class.

## Methodology Insights

* **Use the Poleg-Polsky & Diamond 2016 ModelDB 189347 .hoc geometry as the primary per-compartment
  diameter source** [PolegPolsky2016]. The community convention is to partition DSGC dendrites into
  three classes (soma/primary/terminal), and Poleg-Polsky & Diamond is the canonical mouse ON-OFF
  DSGC NEURON model. Extract the primary-dendrite and terminal-dendrite radii from the public .hoc
  files and record them in `research/research_code.md` when inspected. Fallback order: if ModelDB
  189347 is unavailable or ambiguous, fall back to the Hanson 2019 extended model
  (`github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model` [Hanson2019]), which uses the same
  morphology.

* **Preserve the 19 soma compartments verbatim.** The task description explicitly requires this, and
  the corpus agrees: every model quotes a per-section soma diameter in the 10-15 µm class (e.g.
  Schachter2010 lists "soma ~15 µm"). The CNG soma contour encodes these diameters already and they
  are not placeholders.

* **Key the taper on Strahler order, not on path distance.** Strahler order on a CNG-curated tree
  cleanly recovers the three-compartment (soma/primary/terminal) partition that every corpus NEURON
  model uses [PolegPolsky2016, Hanson2019, Jain2020, Schachter2010], is insensitive to sparse-branch
  artefacts, and preserves topology. Map: order 1 = terminal radius, order 2..(max-1) = interpolated
  mid-dendrite radius, max order = primary radius. Document the exact per-order radii in the
  calibrated dataset's `description.md`.

* **Clamp the terminal (order 1) radius at a floor.** The task's risk section specifies a 0.15 µm
  floor. Literature supports this: Oesch2005 reports ~0.5 µm "dendritic diameters" as the
  justification for avoiding dendritic patch (i.e. a typical value, not a minimum) [Oesch2005], and
  Schachter2010 achieves the required >1 GΩ distal input resistance with dendrites sized so that
  "each dendritic segment is <0.1 lambda" — floors below ~0.1 µm diameter (0.05 µm radius) would
  produce unphysiological input impedances.

* **Validate against three electrotonic targets.** After calibration, (i) compute dendritic input
  resistance at representative proximal and distal nodes using Ra = 100 Ω·cm and Rm = 10-22
  kΩ·cm²; it should fall in the ~150-200 MΩ (proximal) to >1 GΩ (distal) range reported by
  Schachter2010 [Schachter2010]. (ii) Check that total dendritic surface area scales up from the
  placeholder baseline (surface area is 2π r L; a ~2-4x mean radius increase implies ~2-4x surface
  area). (iii) Confirm compartment count, branch-point count (129), and leaf count (131) match the
  source SWC exactly [t0005Asset].

* **Hypothesis to test in implementation.** If the Poleg-Polsky primary-to-terminal diameter ratio
  is approximately 3-4x, the resulting axial-resistance profile along the preferred-to-null
  dendritic axis should match the Schachter2010 ~150-200 MΩ proximal vs. >1 GΩ distal input-
  resistance gradient within 50%. If it does not, the taper rule is likely wrong.

* **Best practice: document the taper source paper in the calibrated dataset's `details.json`.** The
  community precedent from Ding2016 is "multiplicative diameter factors from EM measurements" with
  the source explicitly cited [Ding2016]. `details.json` `source_paper_id` must point to
  PolegPolsky2016 (or Hanson2019 as fallback), not be `null`.

## Gaps and Limitations

* **No EM-grade per-compartment DSGC diameter table is published in the corpus or — to the best of
  the reviewed literature — anywhere else.** The Briggman et al. 2011 SBEM DSGC reconstructions
  cited by [Vaney2012] do carry diameters, but the original data were not included in the project
  paper corpus and are not downloadable with the review paper alone.

* **Shrinkage correction is not applied.** The CNG SWC carries a documented ~10-20% confocal
  under-estimation bias in lengths [t0005Asset]; diameters copied from other reconstructions that
  were or were not shrinkage-corrected cannot be transferred without acknowledging this residual
  systematic error.

* **Per-sublamina diameter differences (ON vs OFF arbor) are not reported.** Bistratified DSGCs have
  two sublaminar arbors that may have different calibres, but [Vaney2012], [PolegPolsky2016],
  [Hanson2019], and [Jain2020] all treat them with identical diameter profiles. This forces the
  taper rule to be symmetric across ON/OFF sublaminae, which may bias ON vs OFF axial conductance in
  the same direction.

* **The Poleg-Polsky morphology is one cell, not a population.** Reusing its diameter profile on
  `141009_Pair1DSGC` assumes between-cell morphological similarity within the mouse ON-OFF DSGC
  class; this assumption is explicit in [Jain2020] which re-uses the Poleg-Polsky tree for all its
  NEURON simulations, but no literature quantifies the within-class spread of primary or terminal
  diameters.

* **Strahler order is not unique for CNG-curated trees with three-way branch points.** The CNG SWC
  has 129 branch points and 131 leaves; if any branch point has more than two children, Strahler
  order definitions diverge. The calibrated dataset must document which Strahler variant was used.

## Recommendations for This Task

1. **Adopt Poleg-Polsky & Diamond 2016 (ModelDB 189347) as the primary taper source** for the
   soma/primary/terminal three-bin partition [PolegPolsky2016]. Cite it as `source_paper_id` in
   `details.json`.

2. **Use Hanson 2019 (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) as the fallback** if the ModelDB
   189347 `.hoc` numbers are ambiguous or unavailable [Hanson2019].

3. **Key the taper on Strahler order**, not path distance. Map order 1 to "terminal", max order to
   "primary", interior orders to a log-linear interpolation. Preserve the 19 soma compartments
   verbatim.

4. **Clamp the terminal radius at 0.15 µm** per the task's risk section and document the clamp
   count in the calibrated asset's `description.md`.

5. **Validate with three targets**: (a) Rin gradient 150-200 MΩ proximal to >1 GΩ distal
   [Schachter2010]; (b) compartment count, branch-point count, leaf count unchanged from source
   [t0005Asset]; (c) per-order radius histograms documented as PNGs in `results/images/`.

6. **If the Poleg-Polsky diameter profile produces an Rin gradient more than 50% off the Schachter
   target, flag a fallback in `corrections/`** and re-run with Hanson 2019 numbers; mark the asset
   as "Poleg-Polsky-profile calibrated, Hanson-fallback" per the task's risk section.

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
* **Relevance**: Primary per-compartment diameter source. Public NEURON model on ModelDB 189347 with
  a reconstructed mouse DRD4 ON-OFF DSGC morphology whose .hoc geometry files list per- section
  diameters for soma, primary, and terminal dendrites — the taper rule this task adopts.

### [Vaney2012]

* **Title**: Direction selectivity in the retina: symmetry and asymmetry in structure and function
* **Authors**: Vaney, D. I., Sivyer, B., Taylor, W. R.
* **Year**: 2012
* **DOI**: `10.1038/nrn3165`
* **Asset**: `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nrn3165/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`
* **Relevance**: Decadal review of DSGC morphology and function. Fixes the qualitative geometric
  frame (bistratified, 150-200 µm dendritic field per sublamina, ~40 µm subunit spacing) that the
  calibrated morphology must remain consistent with, even though it does not quote per-segment
  diameters directly.

### [Schachter2010]

* **Title**: Dendritic Spikes Amplify the Synaptic Signal to Enhance Detection of Motion in a
  Simulation of the Direction-Selective Ganglion Cell
* **Authors**: Schachter, M. J., Oesch, N., Smith, R. G., Taylor, W. R.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000899`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/`
* **Categories**: `compartmental-modeling`, `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`, `voltage-gated-channels`, `cable-theory`
* **Relevance**: Rabbit-DSGC compartmental model with explicit Rm = 10-22 kΩ·cm², Ra = 110
  Ω·cm, and reported dendritic input resistances (~150-200 MΩ proximal to >1 GΩ distal).
  Supplies the electrotonic validation targets for the calibrated SWC.

### [Hanson2019]

* **Title**: Retinal direction selectivity in the absence of asymmetric starburst amacrine cell
  responses
* **Authors**: Hanson, L., Sethuramanujam, S., deRosenroll, G., Jain, V., Awatramani, G. B.
* **Year**: 2019
* **DOI**: `10.7554/eLife.42392`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.42392/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `synaptic-integration`,
  `compartmental-modeling`, `dendritic-computation`, `patch-clamp`
* **Relevance**: Fallback taper source. Re-uses the Poleg-Polsky morphology in a public GitHub
  NEURON model (`geoffder/Spatial-Offset-DSGC-NEURON-Model`) with explicit soma/primary/terminal
  conductance-density partition (Na 150/150/30, K rectifier 70/70/35, delayed rectifier 3/0.8/0.4
  mS/cm²) that only makes sense with a three-diameter partition.

### [Jain2020]

* **Title**: The functional organization of excitation and inhibition in the dendrites of mouse
  direction-selective ganglion cells
* **Authors**: Jain, V., Murphy-Baum, B. L., deRosenroll, G., Sethuramanujam, S., Delsey, M.,
  Delaney, K. R., Awatramani, G. B.
* **Year**: 2020
* **DOI**: `10.7554/eLife.52949`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.7554_eLife.52949/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `dendritic-computation`,
  `synaptic-integration`, `compartmental-modeling`, `patch-clamp`
* **Relevance**: Another independent re-use of the Poleg-Polsky & Diamond 2016 DSGC morphology with
  the same soma/primary/terminal three-bin convention (Na 150/200/30, K rect 35/35/25, K delayed
  0.8/0.8/0.8 mS/cm²), confirming the three-bin partition is the community standard.

### [Oesch2005]

* **Title**: Direction-Selective Dendritic Action Potentials in Rabbit Retina
* **Authors**: Oesch, N., Euler, T., Taylor, W. R.
* **Year**: 2005
* **DOI**: `10.1016/j.neuron.2005.06.036`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2005.06.036/`
* **Categories**: `direction-selectivity`, `dendritic-computation`, `voltage-gated-channels`,
  `retinal-ganglion-cell`, `patch-clamp`
* **Relevance**: Gives the only scalar DSGC dendritic-calibre anchor in the corpus: "~0.5 µm
  dendritic diameters" cited as the reason dendritic patch is impractical. Provides an
  order-of-magnitude sanity check that any calibrated profile must span.

### [Ding2016]

* **Title**: Species-specific wiring for direction selectivity in the mammalian retina
* **Authors**: Ding, H., Smith, R. G., Poleg-Polsky, A., Diamond, J. S., Briggman, K. L.
* **Year**: 2016
* **DOI**: `10.1038/nature18609`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature18609/`
* **Categories**: `direction-selectivity`, `retinal-ganglion-cell`, `compartmental-modeling`,
  `synaptic-integration`
* **Relevance**: Methodological precedent — the SAC network model uses "a digitized SAC morphology
  with multiplicative diameter factors from EM measurements", exactly the class of approach proposed
  here (known topology + external diameter factors). Cited as the cross-cell-type analogue for the
  taper strategy.

### [Fohlmeister2010]

* **Title**: Mechanisms and Distribution of Ion Channels in Retinal Ganglion Cells: Using
  Temperature as an Independent Variable
* **Authors**: Fohlmeister, J. F., Cohen, E. D., Newman, E. A.
* **Year**: 2010
* **DOI**: `10.1152/jn.00123.2009`
* **Asset**:
  `tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/`
* **Categories**: `retinal-ganglion-cell`, `compartmental-modeling`, `voltage-gated-channels`,
  `patch-clamp`
* **Relevance**: General-RGC passive-property reference (Rm = 40 kΩ·cm², Cm = 1 µF/cm², Ri =
  100 Ω·cm). Supplies the Ri anchor shared with every DSGC model; its Rm differs from
  DSGC-specific values and should not be transferred.

### [t0005Asset]

* **Title**: DSGC Baseline Morphology (Feller 141009_Pair1DSGC) dataset asset
* **Authors**: t0005_download_dsgc_morphology task
* **Year**: 2026
* **DOI**: `no-doi_t0005_dsgc-baseline-morphology`
* **Note**: Internal project dataset asset, not a publication
* **Asset**: `tasks/t0005_download_dsgc_morphology/assets/dataset/dsgc-baseline-morphology/`
* **Categories**: `compartmental-modeling`, `retinal-ganglion-cell`
* **Relevance**: The calibration input. Documents the 0.125 µm placeholder-radius problem (6,736
  compartments, 19 soma / 6,717 dendrite, 129 branch points, 131 leaves, 1,536 µm total path
  length) and explicitly states that all radii are placeholders requiring re-calibration.
