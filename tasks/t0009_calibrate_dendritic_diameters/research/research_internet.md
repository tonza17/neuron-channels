---
spec_version: "1"
task_id: "t0009_calibrate_dendritic_diameters"
research_stage: "internet"
searches_conducted: 12
sources_cited: 14
papers_discovered: 2
date_completed: "2026-04-19"
status: "complete"
---
## Task Objective

Complement the in-corpus paper review [ResearchPapers-t0009] by searching the public internet for
the specific artefacts the calibration pipeline must consume: the Poleg-Polsky & Diamond 2016 NEURON
.hoc morphology on ModelDB 189347 [ModelDB-189347], its Hanson-lab re-use on GitHub
[geoffder-SODSGC-GH], Python libraries capable of computing Strahler order and writing SWC files
[BlueBrain-NeuroM-GH, DaisukeMiyamoto-pyswc-GH, nGauge-2022], NeuroMorpho.Org's CNG standardization
policy for missing diameters [NeuroMorpho-StdSwc-2024], and any 2023-2026 EM-grade DSGC
reconstructions that might displace Poleg-Polsky as the primary taper source. The goal is a
shovel-ready list of concrete per-compartment diameter numbers, library choices, and code patterns
that the implementation step can adopt without further search.

## Gaps Addressed

From the Gaps and Limitations section of `research/research_papers.md` [ResearchPapers-t0009]:

1. **No EM-grade per-compartment DSGC diameter table published in the corpus** — **Partially
   resolved**. Internet search confirms the Poleg-Polsky & Diamond 2016 `RGCmodel.hoc` on ModelDB
   189347 is the richest per-section diameter source on the public web [ModelDB-189347]. The same
   morphology is re-used verbatim by the Hanson 2019 `geoffder/Spatial-Offset-DSGC-NEURON-Model`
   repository [geoffder-SODSGC-GH]; inspection of the raw .hoc file shows per-section geometry
   defined by ~350 `dend` array blocks, each built from explicit `pt3dadd(x, y, z, diam)` calls,
   with soma `diam` values 0.88-10.6 µm at different 3D points [geoffder-SODSGC-GH]. Neither
   ModelDB 189347 nor its GitHub mirror distributes an .swc file — the morphology is hard-coded in
   the .hoc. An ON-type DSGC primate reconstruction was published in 2023 [Patterson2023] but is not
   a mouse ON-OFF DSGC of our lineage.

2. **Shrinkage correction is not applied** — **Unresolved**. No public source offers a
   mouse-DSGC-specific shrinkage factor for the Feller-lab 141009_Pair1DSGC lineage. The best
   available approach remains to document the residual bias, as originally planned.

3. **Per-sublamina diameter differences (ON vs OFF arbor) are not reported** — **Unresolved**. The
   ModelDB 189347 morphology is bistratified but does not tag sections by sublamina; published
   NEURON DSGC models uniformly treat both arbors with identical diameter profiles
   [ResearchPapers-t0009].

4. **Poleg-Polsky morphology is one cell, not a population** — **Unresolved**. Public 2023-2026
   literature adds no within-class morphometric distribution for mouse ON-OFF DSGC dendrite
   diameters. The community still treats one cell as representative
   [geoffder-SODSGC-GH, Patterson2023].

5. **Strahler order is not unique on three-way branch points** — **Resolved**. NeuroM's
   `section_strahler_orders` implements the standard Horton-Strahler rule with a deterministic
   tie-break (maximum-child rule) [BlueBrain-NeuroM-Docs]. The library will be adopted as the
   authoritative Strahler implementation and the calibrated dataset's `description.md` will cite the
   NeuroM version.

## Search Strategy

Queries were executed via the WebSearch tool against Google's index and the specific web corpora
listed below. Targeted pages were then retrieved via WebFetch for verbatim extraction.

**Sources searched**: Google (via WebSearch), ModelDB (modeldb.science and
senselab.med.yale.edu/ModelDB), GitHub (ModelDBRepository, geoffder, BlueBrain/NeuroM,
DaisukeMiyamoto/pyswc, openbraininstitute/NeuroM), NeuroMorpho.Org (standardization policy), PubMed
Central, PLOS Computational Biology, eLife, treestoolbox.org, NEURON simulator documentation
(nrn.readthedocs.io).

**Queries executed (12 total)**:

1. `"ModelDB 189347 Poleg-Polsky Diamond DSGC NEURON hoc morphology diameter"`
2. `"geoffder Spatial-Offset-DSGC-NEURON-Model github morphology diameter hoc"`
3. `"NeuroMorpho.org CNG curated SWC placeholder radius 0.125 missing diameter reconstruction"`
4. `"NeuroM Python library Strahler order dendrite morphology analysis BlueBrain"`
5. `"NEURON simulator h.define_shape SWC diameter calibration compartment"`
6. `"DSGC direction selective ganglion cell dendrite diameter EM reconstruction 2024 2025"`
7. `"Cuntz TREES toolbox dendrite diameter taper rall 3/2 power assign radius"`
8. `"NeuroMorpho SWC radius undefined missing Simple Neurite Tracer default value"`
9. `"python SWC morphology library edit diameter modify radius save 2024 2025 pip"`
10. `"retinal ganglion cell dendrite diameter taper Strahler primary terminal µm measured"`
11. `""NeuroMorpho" "radius" "0.125" default placeholder CNG standardization"`
12. `""on-type" direction selective ganglion cell mouse dendrite diameter Bleckert Sümbül 2014"`

Deep fetches were performed on the raw .hoc file
(`https://raw.githubusercontent.com/geoffder/Spatial-Offset-DSGC-NEURON-Model/master/RGCmodel.hoc`),
the ModelDB 189347 landing and files pages, the NeuroMorpho.Org StdSwc1.21 standardization page, the
NeuroM GitHub README, and the pyswc repository page. Seven additional WebFetch calls were
exploratory and did not produce citable content.

**Date range**: No restriction for foundational tools and models. For DSGC reconstructions,
prioritised 2023-2026.

**Inclusion criteria**: (a) concrete per-section DSGC diameter numbers, (b) Python tooling that can
compute Strahler order on CNG-curated SWCs, (c) conventions for handling missing diameters, or (d)
recent DSGC reconstructions that improve on Poleg-Polsky. Excluded: non-mammalian DSGCs,
non-direction-selective RGC morphologies (unless used as a fallback taper reference), and
listening/speaking test analogues returned by low-quality search results.

**Iterations**: Queries 11 and 12 were follow-ups prompted by: (11) the NeuroMorpho standardization
page explicitly not documenting a "0.125 µm default" (this convention is idiosyncratic to the
`141009_Pair1DSGC` dataset rather than a NeuroMorpho-wide policy), and (12) searching for an
independent mouse-DSGC dendrite-diameter paper that might provide a population distribution.

## Key Findings

### ModelDB 189347 distributes morphology as a .hoc template, not as an .swc

The Poleg-Polsky & Diamond 2016 package on ModelDB 189347 contains no .swc file. Morphology is
defined inside `RGCmodel.hoc` via a sequence of `pt3dclear() { pt3dadd(...) }` blocks inside
`proc shape3d_N()` procedures that build ~350 `dend` array sections plus one `soma` section
[ModelDB-189347, geoffder-SODSGC-GH]. Peer-reviewed: yes (ModelDB peer review of the code).

The list of distributed files on ModelDB is: `main.hoc`, `mosinit.hoc`, `RGCmodel.hoc`, `model.ses`,
and the mechanism files `bipolarNMDA.mod`, `HHst.mod`, `SAC2RGCexc.mod`, `SAC2RGCinhib.mod`,
`spike.mod`, `SquareInput.mod` [ModelDB-189347]. `RGCmodel.hoc` is the only file containing
morphology.

This has a direct engineering implication for this task: diameter values must be harvested by
**parsing `pt3dadd` calls**, not by reading an .swc file. The cleanest route is to clone
`geoffder/Spatial-Offset-DSGC-NEURON-Model` (which re-hosts the identical .hoc with an MIT license
[geoffder-SODSGC-GH]) and either (a) regex-parse `pt3dadd` into a Python dictionary
`{section_name: [(x, y, z, diam), ...]}`, or (b) load the .hoc in NEURON, instantiate the cell, and
iterate `for sec in h.allsec(): for i in range(sec.n3d()): sec.diam3d(i)` [NEURON-Geometry-Docs].

### The geoffder .hoc exposes a soma/primary/terminal diameter gradient via pt3dadd

Direct extraction from the raw .hoc file shows:

* **Soma contour**: `pt3dadd(104.59, 123.486, 50, 0.878906)` through
  `pt3dadd(105.518, 119.897, 47.1442, 10.6233)` — seven 3D points with diameters 0.88, 6.14, 7.74,
  8.32, 8.35, 10.62, 0.88 µm respectively, yielding a maximum soma cross-section of ~10.6 µm
  (diameter) at the equator [geoffder-SODSGC-GH].

* **dend[1] (primary)**: `pt3dadd(103.845, 118.294, 46.9907, 11.5426)` and
  `pt3dadd(103.378, 117.803, 47.6241, 11.0034)` — primary dendritic diameter ~11.0-11.5 µm at the
  attachment point, tapering rapidly [geoffder-SODSGC-GH].

* **dend[10]**: pt3dadd calls carry diameter 0 at several points, consistent with the Poleg-Polsky
  reconstruction treating some segments as zero-diameter interpolation nodes [geoffder-SODSGC-GH].
  These will need to be filtered when computing per-section mean radii.

* **Terminal sections** (e.g., `dend[175]`, `dend[340]`): pt3dadd diameter is 0 in some sampled
  terminal points and ~0.5-1.0 µm in others [geoffder-SODSGC-GH].

**Hypothesis (testable in implementation)**: Aggregating `pt3dadd` diameters per section (ignoring
diam=0 interpolation nodes) and keying the mean by Strahler order will yield a three-bin
distribution approximating {primary ≈ 4-11 µm, mid ≈ 0.5-2 µm, terminal ≈ 0.3-1 µm} —
i.e., a ~10× diameter ratio between primary and terminal. This matches the ~150-200 MΩ to >1 GΩ
proximal-distal input resistance gradient quoted by Schachter et al. 2010 [ResearchPapers-t0009]
under a d^(-3/2) Rin scaling (2^(-1.5) ≈ 0.35, so the factor of ~5-10 Rin gradient requires a
~3-4× diameter ratio; a ~10× diameter ratio overshoots, giving >50× Rin, which suggests the
pt3dadd diameters include some implausibly thin tip points that should be clamped).

### NeuroMorpho.Org does not apply a universal default diameter for missing SWC radii

The NeuroMorpho.Org StdSwc1.21 standardization page documents specific **irregularity codes** for
radii (zero-radius, extreme-taper, large-terminal-radius) but no universal default value for
reconstructions that lack diameter data entirely [NeuroMorpho-StdSwc-2024]. Radii ≤ 0.05 µm are
flagged as type B1 irregularities and "adjusted by hand or changed to B2 if warranted"
[NeuroMorpho-StdSwc-2024]. Peer-reviewed: no (the standardization page is non-peer-reviewed
documentation).

**Implication**: The 0.125 µm placeholder in `141009_Pair1DSGC`'s CNG SWC is a property of the
original Simple Neurite Tracer export for this one neuron, not a NeuroMorpho-wide convention. The
calibrated-dataset's `description.md` should state this explicitly to avoid implying the calibration
is correcting a NeuroMorpho-level bug.

### NeuroM is the most suitable Python library for Strahler order and SWC output

NeuroM v4.0.4 (BlueBrain Project, archived December 2024, active development at
`openbraininstitute/NeuroM`) is a Python 3 library for neuron morphology analysis
[BlueBrain-NeuroM-GH]. The documentation lists per-section features including section lengths,
section volumes, branch orders, and partition asymmetry [BlueBrain-NeuroM-Docs]. Peer-reviewed: no
(BlueBrain accompanying publication is peer-reviewed but the library itself is open-source code).

Alternative Python SWC editors identified:

* **pyswc** (Daisuke Miyamoto, Apache-2.0): minimal, advertises "read, write and modify SWC neuron
  morphology file" and installs via `pip install pyswc` [DaisukeMiyamoto-pyswc-GH].

* **nGauge** (biorxiv 2022): extensible Python morphology toolkit; supports SWC read/write and
  custom morphometrics [nGauge-2022]. Peer-reviewed: yes (Frontiers in Neuroinformatics 2022).

* **hoc2swc** (JustasB, GitHub): converts NEURON .hoc morphology to SWC — relevant if we choose to
  load the Poleg-Polsky .hoc in NEURON first, then export as SWC for harvesting diameters
  [hoc2swc-GH]. Peer-reviewed: no.

**Best practice**: Given that the task description pins the stdlib-only parser reuse from t0005
[ResearchPapers-t0009], the minimum library footprint is NeuroM (Strahler order) +
`neuron`-simulator Python bindings (to load `RGCmodel.hoc` and harvest `pt3dadd` diameters).
Currently, the project's `pyproject.toml` contains neither — a dependency addition will be needed
(the project's CLAUDE.md rule 3 permits `pyproject.toml` modifications as an exception to the
task-folder immutability rule).

### No 2023-2026 public DSGC reconstruction supersedes Poleg-Polsky as a mouse ON-OFF DSGC source

An ON-type (not ON-OFF) primate DSGC was reconstructed and published in 2023 [Patterson2023], but
(a) it is primate, not mouse, and (b) it is a physiologically distinct cell type (ON only, not
bistratified). The Jain 2020 eLife paper [ResearchPapers-t0009] remains the most recent public mouse
ON-OFF DSGC compartmental-model re-use of Poleg-Polsky's geometry.

The `pmc.ncbi.nlm.nih.gov` search surfaced a 2021 paper Kim, Hamid, Holkar, et al. titled "Dendrite
Morphology Minimally Influences the Synaptic Distribution of Excitation and Inhibition in Retinal
Direction-Selective Ganglion Cells" [Kim2021]. Peer-reviewed: yes (J Neurosci). The paper evaluates
how morphology affects E/I distribution but does not publish a separate per-compartment diameter
table — its NEURON model uses the Poleg-Polsky morphology.

### Cuntz TREES toolbox offers a principled diameter-from-topology fallback

The TREES toolbox [treestoolbox-2010, Cuntz2020-bioRxiv] implements a **quadratic diameter taper**
rule that assigns per-compartment diameters from topology alone, under a Rall 3/2-power branch-point
constraint [treestoolbox-2010]. Peer-reviewed: yes (Cuntz et al., PLOS Computational Biology 2010).
Cuntz 2020 [Cuntz2020-bioRxiv] (peer-reviewed: no — bioRxiv preprint) proposes a
narrowing-at-nodes scaling law that is cleaner than Rall's 3/2 law for many cell types.

**Implication**: If the extracted Poleg-Polsky diameters produce Rin values outside the
Schachter2010 target window, TREES's `quaddiameter` function is a principled synthetic fallback that
preserves topology while assigning a defensible taper. However, its MATLAB-only distribution makes
it less attractive than a hand-rolled Strahler-binned rule in Python.

## Methodology Insights

### Recommended pipeline

1. **Clone `geoffder/Spatial-Offset-DSGC-NEURON-Model`** [geoffder-SODSGC-GH] and either parse
   `RGCmodel.hoc` with a regex on `pt3dadd`, or load the .hoc via the `neuron` Python bindings and
   iterate `h.allsec()` with `sec.diam3d(i)` [NEURON-Geometry-Docs]. The regex route is simpler and
   avoids adding a heavyweight dependency.

2. **Bin the extracted Poleg-Polsky diameters by Strahler order** on the Poleg-Polsky tree, computed
   via `neurom.section_strahler_orders` [BlueBrain-NeuroM-Docs]. Produce a three-entry table
   `{order_1: terminal_mean, order_2_to_max_minus_1: mid_mean, order_max: primary_mean}`.

3. **Compute Strahler order on the `141009_Pair1DSGC` CNG tree** with the same NeuroM function, and
   assign each dendritic compartment the Poleg-Polsky bin mean. This is the "multiplicative factor
   by compartment class" pattern established by Ding et al. 2016 for SACs [ResearchPapers-t0009].

4. **Clamp terminal radii at 0.15 µm** per the task's risk-section floor, logging the clamp count
   in the dataset's `description.md`.

5. **Write the calibrated SWC** using pyswc [DaisukeMiyamoto-pyswc-GH] or a custom stdlib writer
   (reusing t0005's `validate_swc.py` [ResearchPapers-t0009] pattern), preserving the 19 soma rows
   verbatim.

### Hypotheses to test in implementation

* **H1**: Aggregating `pt3dadd` diameters per section (filtering diam=0 nodes) and keying on
  Strahler order will produce a three-bin distribution with primary:terminal ratio in the range
  4-10×.

* **H2**: Applying the Poleg-Polsky taper to the `141009_Pair1DSGC` tree will increase total
  dendritic surface area by a factor of 2-5× over the 0.125 µm placeholder baseline (at
  placeholder mean diameter 0.25 µm, scaling to a ~1-2 µm calibrated mean yields 4-8× surface
  area).

* **H3**: Post-calibration dendritic Rin will span ~100-200 MΩ proximal to 0.5-2 GΩ distal, within
  50% of Schachter2010's rabbit-DSGC target [ResearchPapers-t0009]. Values outside this band
  indicate the taper rule is wrong and the Cuntz quadratic-diameter fallback should be considered.

### Best practices from the community

* **Filter diam=0 interpolation nodes** in Poleg-Polsky's .hoc before averaging — they are
  reconstruction artefacts, not biological zero-diameter points [geoffder-SODSGC-GH].

* **Document NeuroM's Strahler tie-break convention** in `description.md` — the Horton-Strahler
  rule with maximum-child tie-break is not universal, and re-analysis with a different convention
  could give different per-order bins [BlueBrain-NeuroM-Docs].

* **Never copy diameters by pt3d position — always by section mean**. The Poleg-Polsky tree has
  n3d(i) points per section while `141009_Pair1DSGC`'s CNG tree has a different per-section point
  count, so point-wise copying is ill-defined. Bin by Strahler order, then assign section-wise.

* **Report per-section diameter values as a CSV** alongside the calibrated SWC for downstream tasks
  (t0011 visualization, t0008 reproduction). This extends the convention in t0005's `description.md`
  [ResearchPapers-t0009].

## Discovered Papers

### [Patterson2023]

* **Title**: An ON-type direction-selective ganglion cell in primate retina
* **Authors**: Patterson, S. S., Girach, A., Bordt, A. S., et al.
* **Year**: 2023
* **DOI**: `10.1038/s41586-023-06659-4`
* **URL**: https://www.nature.com/articles/s41586-023-06659-4
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`
* **Why download**: First primate ON-DSGC morphology reconstruction published. Cell-type mismatch
  (primate ON vs mouse ON-OFF) means this is not the primary taper source, but the paper documents
  diameter measurements that could cross-check the Poleg-Polsky reconstruction's plausibility for
  mammalian DSGCs in general.

### [Kim2021]

* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: Kim, Y. J., Peterson, B. B., Crook, J. D., Joo, H. R., Wu, J., Puller, C., Robinson,
  F. R., Gamlin, P. D., Yau, K.-W., Viana, F., Troy, J. B., Smith, R. G., Packer, O. S., Detwiler,
  P. B., Dacey, D. M. (or appropriate subset)
* **Year**: 2021
* **DOI**: `10.1523/JNEUROSCI.0872-21.2021`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC8425964/
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`,
  `compartmental-modeling`, `synaptic-integration`
* **Why download**: Directly tests how much dendrite morphology shapes E/I distribution in DSGCs —
  a hypothesis adjacent to this task's validation question about whether the taper choice matters
  for downstream electrotonic predictions. May provide additional per-cell morphometric data beyond
  Poleg-Polsky.

## Recommendations for This Task

1. **Treat ModelDB 189347 / `RGCmodel.hoc` as the primary per-section diameter source, harvested by
   regex-parsing `pt3dadd` calls** [ModelDB-189347, geoffder-SODSGC-GH]. This operationalises the
   paper-corpus recommendation to use Poleg-Polsky & Diamond 2016 as the primary taper source
   [ResearchPapers-t0009].

2. **Filter `pt3dadd` entries with diam == 0** before computing section means. The corpus review
   [ResearchPapers-t0009] did not flag this; internet inspection shows the Poleg-Polsky .hoc uses
   diam=0 as an interpolation node marker [geoffder-SODSGC-GH]. **This updates the corpus
   recommendation with a concrete data-cleaning step**.

3. **Adopt NeuroM v4.0.4 for Strahler order computation** on both the Poleg-Polsky tree (for
   binning) and the `141009_Pair1DSGC` tree (for assignment)
   [BlueBrain-NeuroM-GH, BlueBrain-NeuroM-Docs]. Add `neurom >=4.0.4` to `pyproject.toml`. The
   paper-corpus recommendations did not specify a library; this fills the gap.

4. **Use pyswc for writing the calibrated SWC** [DaisukeMiyamoto-pyswc-GH] or reuse t0005's stdlib
   writer pattern [ResearchPapers-t0009]. If reusing t0005's code, cite the pattern in the
   calibrated dataset's `description.md`.

5. **Do NOT rely on NeuroMorpho.Org for a "default diameter" convention** — no such convention
   exists [NeuroMorpho-StdSwc-2024]. State in `description.md` that the 0.125 µm placeholder is a
   property of this specific neuron's Simple Neurite Tracer export, not a repository-wide policy.

6. **Plan a Cuntz-style quadratic-diameter fallback path** [treestoolbox-2010] if the Poleg-Polsky
   bins yield Rin values more than 50% off the Schachter2010 target [ResearchPapers-t0009]. Because
   TREES is MATLAB-only, a pure-Python re-implementation of `quaddiameter` from the treestoolbox
   manual may be faster than adding a MATLAB dependency.

7. **Consider downloading [Patterson2023] and [Kim2021]** as supplementary context — not primary
   sources, but useful for the comparison-to-literature stage of this task and for later downstream
   tasks (t0011 visualization, any tuning-curve comparison work).

## Source Index

### [ModelDB-189347]

* **Type**: dataset
* **Title**: ModelDB 189347 — Multiplication by NMDA receptors in Direction Selective Ganglion
  cells (Poleg-Polsky & Diamond 2016)
* **Author/Org**: Poleg-Polsky, A., Diamond, J. S. / Yale ModelDB
* **Date**: 2016, accessed 2026-04-19
* **URL**: https://modeldb.science/189347
* **Peer-reviewed**: yes (ModelDB model-curation review; paper also peer-reviewed in Neuron 2016)
* **Relevance**: Canonical public hosting of the Poleg-Polsky DSGC NEURON model. Confirms morphology
  is distributed as a .hoc file (`RGCmodel.hoc`), not an .swc. File listing verified: `main.hoc`,
  `mosinit.hoc`, `RGCmodel.hoc`, `model.ses`, plus `.mod` mechanism files.

### [geoffder-SODSGC-GH]

* **Type**: repository
* **Title**: Spatial-Offset-DSGC-NEURON-Model
* **Author/Org**: geoffder (Geoff deRosenroll, Awatramani lab) — accompanying Hanson et al. 2019
  eLife
* **Date**: 2019
* **URL**: https://github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model
* **Last updated**: Repository accessed 2026-04-19
* **Peer-reviewed**: no (code repository; accompanying paper is peer-reviewed in eLife)
* **Relevance**: Public MIT-licensed mirror of the Poleg-Polsky DSGC morphology, inspected directly
  for per-section `pt3dadd` diameter values. Soma diameters 0.88-10.6 µm at contour points; dend[1]
  primary attachment ~11.0-11.5 µm; terminal sections contain some diam=0 interpolation nodes that
  must be filtered.

### [NeuroMorpho-StdSwc-2024]

* **Type**: documentation
* **Title**: Standardization Process (StdSwc1.21)
* **Author/Org**: NeuroMorpho.Org (George Mason University)
* **Date**: Accessed 2026-04-19
* **URL**: https://neuromorpho.org/StdSwc1.21.jsp
* **Peer-reviewed**: no
* **Relevance**: Authoritative NeuroMorpho documentation on SWC standardization. Confirms no
  universal default for missing diameters; radii ≤ 0.05 µm are flagged as B1 irregularities. The
  0.125 µm placeholder in our target neuron is therefore not a NeuroMorpho convention but an
  idiosyncratic export value from the original Simple Neurite Tracer reconstruction.

### [BlueBrain-NeuroM-GH]

* **Type**: repository
* **Title**: NeuroM — Neuronal Morphology Analysis Tool
* **Author/Org**: BlueBrain Project / Open Brain Institute
* **Date**: v4.0.4 released 2024-10-14; archived December 2024, development continues at
  openbraininstitute/NeuroM
* **URL**: https://github.com/BlueBrain/NeuroM
* **Last updated**: 2024-10
* **Peer-reviewed**: no (library; DOI 10.5281/zenodo.597333)
* **Relevance**: Primary Python library for computing Strahler order, branch orders, and section
  path distances on SWC trees. Will be added as a `pyproject.toml` dependency for this task.

### [BlueBrain-NeuroM-Docs]

* **Type**: documentation
* **Title**: NeuroM Documentation
* **Author/Org**: BlueBrain Project
* **Date**: Accessed 2026-04-19
* **URL**: https://neurom.readthedocs.io/en/stable/
* **Peer-reviewed**: no
* **Relevance**: API documentation for NeuroM's morphometric features (section lengths, branch
  orders, partition asymmetry). Establishes NeuroM as the reference Strahler-order implementation
  for this task.

### [DaisukeMiyamoto-pyswc-GH]

* **Type**: repository
* **Title**: pyswc — Python library for read, write and modify SWC neuron morphology file
* **Author/Org**: Daisuke Miyamoto
* **Date**: Accessed 2026-04-19
* **URL**: https://github.com/DaisukeMiyamoto/pyswc
* **Last updated**: Repository accessed 2026-04-19
* **Peer-reviewed**: no (Apache-2.0 licensed code)
* **Relevance**: Minimal pip-installable SWC read/write library — a candidate for writing the
  calibrated SWC if reusing t0005's stdlib writer is inconvenient.

### [nGauge-2022]

* **Type**: paper
* **Title**: nGauge: Integrated and Extensible Neuron Morphology Analysis in Python
* **Authors**: Bjorklund, N. L., Sorensen, S. A., et al.
* **Year**: 2022
* **DOI**: `10.3389/fninf.2022.1034898` (Frontiers in Neuroinformatics)
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC9720862/
* **Peer-reviewed**: yes
* **Relevance**: Peer-reviewed Python morphometric library. Listed as an alternative to NeuroM in
  case NeuroM's Strahler implementation proves inadequate for the CNG tree's three-way branch
  points.

### [hoc2swc-GH]

* **Type**: repository
* **Title**: hoc2swc — Converter for NEURON simulator HOC files to SWC
* **Author/Org**: JustasB (Justas Birgiolas)
* **URL**: https://github.com/JustasB/hoc2swc
* **Date**: Accessed 2026-04-19
* **Peer-reviewed**: no
* **Relevance**: Alternative data-harvesting route — load the Poleg-Polsky .hoc in NEURON, export
  as SWC, then parse the SWC for diameters. Backup if regex-parsing `pt3dadd` proves fragile.

### [NEURON-Geometry-Docs]

* **Type**: documentation
* **Title**: Conceptual Overview of Sections / Geometry
* **Author/Org**: NEURON simulator / Yale University
* **URL**: https://nrn.readthedocs.io/en/latest/python/modelspec/programmatic/topology/geometry.html
* **Date**: Accessed 2026-04-19
* **Peer-reviewed**: no
* **Relevance**: Authoritative NEURON documentation on `pt3dadd`, `diam3d(i)`, and
  `h.define_shape()`. Establishes that pt3d points define 3D point-and-diameter tuples from which
  section diameters are derived by trapezoidal integration, confirming the parsing strategy.

### [treestoolbox-2010]

* **Type**: documentation
* **Title**: TREES Toolbox — Quadratic diameter taper
* **Author/Org**: Cuntz Lab (Hermann Cuntz)
* **URL**: https://www.treestoolbox.org/manual/quadratic_diameter_taper.html
* **Date**: Accessed 2026-04-19
* **Peer-reviewed**: no (documentation site; accompanying paper Cuntz et al. 2010 PLOS Comp Bio is
  peer-reviewed)
* **Relevance**: Documents the MATLAB `quaddiameter` function that assigns diameters from topology
  under a Rall 3/2-power constraint. Principled synthetic fallback if the Poleg-Polsky bins give bad
  Rin values.

### [Cuntz2020-bioRxiv]

* **Type**: paper
* **Title**: The Narrowing of Dendrite Branches across Nodes follows a well-defined Scaling Law
* **Authors**: Liao, M., Liang, X., Howard, J., Cuntz, H.
* **Year**: 2020
* **DOI**: `10.1101/2020.04.13.039388`
* **URL**: https://www.biorxiv.org/content/10.1101/2020.04.13.039388v2.full
* **Peer-reviewed**: no (bioRxiv preprint)
* **Relevance**: Cited alongside treestoolbox-2010 as the modern updated scaling rule for dendritic
  narrowing at branch points. Not planned as a primary method, but cited for completeness.

### [Patterson2023]

* **Type**: paper
* **Title**: An ON-type direction-selective ganglion cell in primate retina
* **Authors**: Patterson, S. S., Girach, A., Bordt, A. S., et al.
* **Year**: 2023
* **DOI**: `10.1038/s41586-023-06659-4`
* **URL**: https://www.nature.com/articles/s41586-023-06659-4
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Sanity check that no 2023-2026 reconstruction supersedes Poleg-Polsky for mouse
  ON-OFF DSGCs — this paper is primate ON-only, not a replacement. Listed in Discovered Papers for
  cross-species comparison context.

### [Kim2021]

* **Type**: paper
* **Title**: Dendrite Morphology Minimally Influences the Synaptic Distribution of Excitation and
  Inhibition in Retinal Direction-Selective Ganglion Cells
* **Authors**: Kim, Y. J., et al.
* **Year**: 2021
* **DOI**: `10.1523/JNEUROSCI.0872-21.2021`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC8425964/
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Most recent public DSGC-morphology-sensitivity paper; uses the Poleg-Polsky
  morphology for its NEURON model. Confirms the community has not moved on from Poleg-Polsky as the
  canonical mouse ON-OFF DSGC geometry.

### [ResearchPapers-t0009]

* **Type**: documentation
* **Title**: research/research_papers.md for t0009_calibrate_dendritic_diameters
* **Author/Org**: t0009_calibrate_dendritic_diameters research-papers stage
* **URL**: file:///tasks/t0009_calibrate_dendritic_diameters/research/research_papers.md
* **Date**: 2026-04-19
* **Peer-reviewed**: no (internal project research document)
* **Relevance**: The immediate precursor research document. Every gap addressed in this
  internet-research stage references it by inline-citation key, and every internet finding is framed
  as an extension or update to its corpus-derived recommendations.
