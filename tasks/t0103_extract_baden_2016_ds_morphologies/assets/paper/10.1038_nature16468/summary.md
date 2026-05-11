---
spec_version: "3"
paper_id: "10.1038_nature16468"
citation_key: "Baden2016"
summarized_by_task: "t0103_extract_baden_2016_ds_morphologies"
date_summarized: "2026-05-11"
---
# The functional diversity of retinal ganglion cells in the mouse

## Metadata

* **File**: `files/baden_2016_functional_diversity_rgc.pdf`
* **Published**: 2016-01-21
* **Authors**: Tom Baden, Philipp Berens, Katrin Franke, Miroslav Roman Roson, Matthias Bethge,
  Thomas Euler
* **Venue**: Nature, 529(7586):345-350
* **DOI**: `10.1038/nature16468`
* **PMC**: PMC4724341, PMID 26735013

## Abstract

In the vertebrate visual system, all output of the retina is carried by retinal ganglion cells. Each
type encodes distinct visual features in parallel for transmission to the brain. How many such
"output channels" exist and what each encodes is an area of intense debate. In mouse, anatomical
estimates range between 15-20 channels, and only a handful are functionally understood. Combining
two-photon calcium imaging to obtain dense retinal recordings and unsupervised clustering of the
resulting sample of >11,000 cells, we here show that the mouse retina harbours substantially more
than 30 functional output channels. These include all known and several new ganglion cell types, as
verified by genetic and anatomical criteria. Therefore, information channels from the mouse's eye to
the mouse's brain are considerably more diverse than shown thus far by anatomical studies,
suggesting an encoding strategy resembling that used in state-of-the-art artificial vision systems.

## Overview

Baden et al. address a longstanding question in retinal neuroscience: how many functionally distinct
types of retinal ganglion cell (RGC) exist in the mouse retina, and what visual features does each
type extract? Before this paper, anatomical estimates ranged between 15 and 20 RGC types, yet only a
handful had been characterised functionally. The authors used two-photon calcium imaging in
whole-mount mouse retina to record from essentially every soma in the ganglion-cell layer (GCL)
across local fields of view, building a dense and unbiased sample of >11,000 cells spanning 11,210
individual recordings from 15 retinas. Each cell was probed with a standardised battery of light
stimuli: a full-field "chirp" (sinusoidal temporal-frequency and contrast sweep), moving bars at
eight directions, full-field steps, coloured (UV/green) stimuli, and a binary checker-flicker for
receptive-field mapping.

The functional fingerprints, together with response-quality and immunohistochemical/genetic markers
(GAD67 for displaced amacrines, SMI-32 for alpha-RGCs, melanopsin for ipRGCs, parvalbumin for
Pvalb-Cre RGCs), were fed into an unsupervised probabilistic Mixture-of-Gaussians clustering
pipeline that selected the number of clusters via the Bayesian Information Criterion. DS and non-DS
cells were clustered independently (24 DS clusters and 48 non-DS clusters) and then merged back into
32 RGC groups plus additional displaced amacrine groups (groups 33+). The result is a
near-saturating taxonomy that nearly doubles the previously accepted estimate of mouse RGC type
count and provides a benchmark against which subsequent retinal-coding studies can map their data.

The paper's significance for downstream work is twofold: (i) it establishes the operating reference
catalogue of mouse RGC functional groups, providing per-cell traces and per-group means for chirp,
moving-bar, receptive-field, and colour stimuli; and (ii) it shows that direction-selective (DS)
RGCs are more diverse than the textbook four ON-OFF subtypes — the authors identify 8
DS-containing groups (G2, G6, G12, G13, G16, G25, G26, G29) that together account for 70% of all
1,757 DS cells recorded.

## Architecture, Models and Methods

**Recording**: A custom MOM-type two-photon microscope with a 920 nm excitation laser and a fast
resonant scanner. RGC somata in the GCL were loaded with OGB-1 (a calcium indicator) via electric
bath application. Each field of view typically contained 50-150 cells; 15 retinas yielded 11,210
total cell recordings. Recordings spanned the entire dorsoventral axis of the retina.

**Stimulus battery**: A standardised set of light stimuli was projected through the condenser onto
the photoreceptor layer:

* "Chirp" stimulus: 32 s full-field sinusoidal modulation sweeping temporal frequency (1-32 Hz) and
  contrast (10-100%); designed to probe polarity, kinetics, and contrast/frequency tuning.
* Moving bar: a bright bar drifting at 1 mm/s in eight equally-spaced directions; primary DS/OS
  probe.
* Full-field step: bright/dark 2 s steps; ON/OFF and transience characterisation.
* Coloured stimuli: alternating UV and green LED flashes; chromatic preference.
* Binary checkerboard flicker: 5 Hz, 25 mum check size; linear receptive-field mapping via
  Ca2+-transient-triggered averaging.

**Feature extraction**: Each cell's raw Ca2+ traces were reduced to feature vectors using SVD on
normalised time-by-direction matrices for the moving-bar response (yielding the time-course and the
directional tuning function), and per-stimulus average traces for the chirp, full-field, and
coloured stimuli. Additional scalar features were computed: receptive-field diameter and time
kernel, soma area and volume, ON-OFF index, full-field index, DS index (DSi), OS index (OSi), DS
significance p-value (cell_dp from a permutation test), OS significance p-value (cell_op),
response-quality index, and immunohistochemistry/genetic markers.

**Clustering**: A Mixture-of-Gaussians model was fit independently on DS-positive cells (cell_dp <
0.05, n = 1,757 cells, ~35% of RGCs) and non-DS cells. The number of clusters was selected by the
minimum of the BIC: 24 DS clusters and 48 non-DS clusters. Clusters were merged across DS/non-DS
domains when their functional fingerprints were similar and there was no positive reason (genetic,
anatomical, or physiological) to keep them separate. The final catalogue is 32 RGC groups + 17
displaced amacrine groups (49 total in the extended >32 taxonomy). Cluster posterior probability per
cell is recorded; cluster-mean traces are recorded per stimulus.

**Validation**: Independent juxtacellular electrophysiological recordings from a subset of cells (n
= 245 with biocytin fills and morphological reconstruction), and immunohistochemistry +
parvalbumin/Pcp2 genetic labels were used to cross-validate cluster identities against known
genetically-defined RGC types. Coverage-factor analysis (cluster cell density on retina vs. expected
mosaic spacing) was used to test whether each cluster behaves as a true type.

**Software / hardware**: MATLAB 2012/2014a for all analysis. The paper's authors release a Dryad
deposit (doi:10.5061/dryad.d9v38) containing the per-cell data structure and a separate MATLAB
visualisation zip with `plotOverview.m` and `plotStamp.m` for reproducing the per-group/per-cluster
figures.

## Results

* Identified a **minimum of 32 functionally distinct RGC types** in the mouse retina, nearly
  doubling the prior anatomical estimate of 15-20 types
* Total dataset: **11,210 cells** recorded across **15 retinas**
* Of these, **7,982 cells were RGCs** (the rest were displaced amacrine cells or could not be
  confidently classified)
* Identified an additional **~17 displaced amacrine cell types** in the GCL (groups 33+ in the
  extended taxonomy)
* **1,757 cells (35% of RGCs)** were direction-selective (DS), classified at cell_dp < 0.05 by the
  permutation test
* **8 DS-containing groups account for 70% of all DS cells**: G2 (OFF DS), G6 ((ON-)OFF JAM-B mix),
  G12 (ON-OFF DS 1), G13 (ON-OFF DS 2), G16 (ON DS transient), G25 (ON DS sustained 1), G26 (ON
  slow), G29 (ON local sustained OS)
* The 32 RGC groups comprise: **9 OFF, 12 ON, 3 ON-OFF** non-DS groups and **2 OFF, 4 ON, 2 ON-OFF**
  DS groups
* Cluster quality (posterior probability) is high for the major groups (median posterior > 0.9 for
  cells assigned to G2, G12, G13, G16, G24, G31)
* Three DS groups show **single-direction preference**: G16 (ON DS transient) prefers backward
  motion, the JAM-B RGC (G6) prefers upward motion, G25 (ON DS sustained 1) prefers forward motion
* The **two ON-OFF DS groups (G12, G13)** together contain the four classical ON-OFF DS subtypes
  preferring nasal/temporal/dorsal/ventral motion
* Identified a previously unreported **OFF DS cell type (G2)** that stratifies between the two ChAT
  bands of the IPL; n = 162 cells; matched to a specific dendritic morphology
* Alpha-RGC types: sustained OFF alpha (G5), transient OFF alpha (G8), ON alpha (G24); confirmed via
  SMI-32 immunoreactivity in a subset of cells
* Coverage factors (CF) for most groups cluster around 1, supporting the interpretation that they
  represent single RGC types; CF > 2 in a few groups (notably G12) suggests those still mix multiple
  types

## Innovations

### Near-saturating functional RGC taxonomy in mouse

First study to demonstrate that mouse retina contains **>30 functional RGC types**, more than double
prior anatomical estimates. The combination of dense optical recording, standardised stimulus
battery, and unsupervised clustering with rigorous statistical model-selection (BIC + cluster
posterior + coverage factor) sets a new benchmark for retinal taxonomy that subsequent papers (Bae
2018, Goetz 2022, Ran 2020) have built directly on.

### Independent DS/non-DS clustering strategy

Rather than including DSi/OSi as features in a single clustering pass, the authors first separate
cells using a permutation-based DS significance test (cell_dp < 0.05) and cluster the two subsets
independently. This is critical because DS RGCs share functional features with non-DS cells in
chirp/colour space, and a joint clustering merged most DS subtypes into mixed clusters in their
ablation analysis. The strategy yields a clean DS taxonomy: 24 DS clusters merged into 8 DS-
dominated groups.

### Open canonical reference dataset

The Dryad release (doi:10.5061/dryad.d9v38, `BadenEtAl_RGCs_2016_v1.mat`, ~426 MB) provides per-cell
group/cluster assignments, full traces for every stimulus, scalar functional indices, and
immunohistochemistry/genetics flags for all 11,210 recorded cells. Together with the visualisation
scripts (`plotOverview.m`, `plotStamp.m`) this constitutes a reusable benchmark that downstream
modelling and physiology studies can cite directly. This is the foundation for the current task's
DS-cell extraction (t0103).

### Group-vs-cluster distinction

The catalogue maintains two parallel granularities: 32 RGC groups (after DS/non-DS merging) and ~49
fine-grained clusters (the union of the 24 DS and 25 non-DS clusters surviving quality control).
Future taxonomy refinements can either split groups or merge clusters with explicit evidence — the
dataset preserves both levels.

## Datasets

* **Primary dataset**: Dryad deposit `doi:10.5061/dryad.d9v38`
  ([landing page](https://datadryad.org/dataset/doi:10.5061/dryad.d9v38)). Contains
  `BadenEtAl_RGCs_2016_v1.mat` (~426 MB) — a single MATLAB struct with per-cell fields for cluster
  ID, group ID, scalar functional indices (DSi, OSi, response quality, ON-OFF, full-field, RF size),
  full Ca2+ traces for chirp/moving-bar/coloured/RF stimuli, soma area/volume, and IHC/genetic flags
  (GAD67, SMI-32, melanopsin, PV).
* **Accompanying visualisation code**: lab-distributed zip at
  `http://retinal-functomics.net/wp-content/uploads/2015/12/Baden_et_al_2016_visualization.zip`
  (5,624 bytes, downloaded 2026-05-11; SHA-256 in `data/download_manifest.json`). Contains
  `plotOverview.m`, `plotStamp.m`, `shadedErrorBar.m`.
* **Sample size**: 11,210 recorded cells from 15 mouse retinas; 7,982 confidently classified as
  RGCs; 1,757 cells (35% of RGCs) marked as direction-selective at cell_dp < 0.05.
* **License**: CC0 (Dryad default) for the data deposit. Code reuse follows the
  retinal-functomics.net distribution.
* **Availability**: Public, but the Dryad downloads require authenticated access via the v2 REST API
  (bearer token). Direct CLI downloads via the legacy `file_stream/<id>` URLs return HTTP 403 or an
  Anubis JS challenge. See `intervention/dryad_download_blocked.json` for evidence.

## Main Ideas

* The Baden 2016 group taxonomy with 32 RGC groups and 8 DS-containing groups (G2, G6, G12, G13,
  G16, G25, G26, G29) is the canonical reference for any DSGC-modelling task in this project
* DS-RGC diversity is much higher than the textbook four ON-OFF subtypes — multiple ON-only,
  OFF-only, and ON-OFF DS subtypes exist with distinct directional preferences and IPL
  stratification depths
* The independent DS/non-DS clustering strategy is essential — if DSi is mixed in as a feature in
  a single clustering pass, most DS subtypes vanish into mixed clusters
* Per-group cluster posterior and coverage factor must be checked when selecting a "representative
  cell" — groups with CF > 2 (notably G12) likely mix multiple underlying types
* The dataset does **not** include per-cell morphological reconstructions for most cells; a subset
  has biocytin fills (~245 cells) which the authors used for validation. Morphologies for the full
  DS population must be sourced from complementary papers (Bae 2018, Ran 2020, or similar)
* Functional fingerprints (chirp + moving-bar means) are the most distinctive per-group
  characteristic — these are the recommended inputs for matching simulated DSGC responses against
  Baden 2016 cell types
* The DS-defining stimulus is the **moving bar** (`bar_tc` field in the Dryad data, `bar_time`
  axis), not the chirp — any DSGC-validation script should compare simulated bar responses to the
  cluster-mean `bar_tc` of the appropriate Baden 2016 group

## Summary

Baden, Berens, Franke, Roman Roson, Bethge, and Euler used dense two-photon calcium imaging of RGC
somata in whole-mount mouse retina, combined with a standardised stimulus battery (chirp, moving
bar, full-field, coloured, checkerboard) and unsupervised probabilistic clustering, to produce a
near-saturating taxonomy of mouse RGC functional types. Across 11,210 cell recordings from 15
retinas, they identify a minimum of 32 RGC functional groups — nearly double the prior anatomical
estimate of 15-20 — plus an additional ~17 displaced amacrine cell groups.

The clustering strategy is methodologically important: rather than mixing direction-selective and
non-DS cells in a single clustering pass, the authors first apply a permutation-based DS
significance test (cell_dp < 0.05) and cluster the two subsets independently, then merge similar
clusters back together with explicit evidence. This yields 24 DS clusters merged into 8 DS-
dominated groups (G2, G6, G12, G13, G16, G25, G26, G29) that account for 70% of all 1,757 DS cells.
They confirm cluster identities via independent juxtacellular electrophysiology with biocytin fills,
immunohistochemistry for known markers (GAD67, SMI-32, melanopsin), and genetic labels in PV-Cre and
Pcp2 transgenic lines. Cluster quality is high for major groups (median posterior > 0.9) and
coverage factors typically cluster around 1, supporting interpretation as single types.

The paper's primary results are quantitatively striking. Of 11,210 imaged GCL somata, 7,982 were
RGCs; the remaining cells were displaced amacrines or unclassifiable. Of the RGCs, 1,757 (35%) were
direction-selective at the cell_dp < 0.05 significance threshold. The 32 RGC groups break down into
9 OFF + 12 ON + 3 ON-OFF non-DS groups and 2 OFF + 4 ON + 2 ON-OFF DS groups. Cluster posterior
quality exceeds 0.9 for the major groups, coverage factors cluster around 1 for most groups, and
biocytin morphologies in a 245-cell validation subset confirm cluster-to-morphology correspondence
for the classical alpha, JAM-B, and ON-OFF DS types.

For this project, the Baden 2016 paper and the accompanying Dryad release define the canonical
reference dataset for direction-selective RGC properties in the mouse retina. The 8 DS-containing
groups, their cluster-mean moving-bar responses, IPL stratification depths, and scalar indices (DSi,
OSi, response quality) are the targets that any DSGC compartmental simulation in this project must
match. The per-cell traces enable construction of biologically-grounded parameter envelopes for the
t0090 morphology generator and validation distributions for the t0102 joint-pass corner. The
principal limitation is that morphological reconstructions are not provided for the bulk of recorded
cells — DS-cell morphologies for downstream modelling must be sourced from a complementary paper
such as Bae et al. 2018 or Ran et al. 2020. The cell-level reconciliation of the user- supplied
cluster IDs `[2, 17, 18, 19, 22, 35, 36, 40]` against the authoritative paper taxonomy is recorded
in `code/visualization_code_notes.md`; only G2 from the user list is in the paper's DS-group set,
which is documented as a blocking intervention in `intervention/cluster_id_mismatch.json`.
