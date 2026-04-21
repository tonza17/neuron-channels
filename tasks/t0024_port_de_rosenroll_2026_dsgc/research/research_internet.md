---
spec_version: "1"
task_id: "t0024_port_de_rosenroll_2026_dsgc"
research_stage: "internet"
searches_conducted: 5
sources_cited: 6
papers_discovered: 0
date_completed: "2026-04-21"
status: "complete"
---
# Research Internet: Port de Rosenroll 2026 DSGC

## Task Objective

Port de Rosenroll et al. 2026 (Cell Reports, 10.1016/j.celrep.2025.116833) into the project as a
third DSGC library asset with modern ion channels and evaluate it with the same 12-angle moving-bar
protocol used in t0022 and t0023. This internet-research step closes the gaps identified in
`research_papers.md` by reading the manually-uploaded PDF [deRosenroll2026] and the companion Zenodo
archive [dsMicro-Zenodo] / GitHub repository [dsMicro-GH] directly, pinning channel densities,
synaptic conductances, AIS geometry, noise-model parameters, and the target tuning envelope before
implementation begins.

## Gaps Addressed

From `research_papers.md` Gaps and Limitations:

1. **Quantitative AChE-block DSI drops from [deRosenroll2026]** - **Resolved**. Reading the PDF
   directly yielded the two headline numbers: correlated SAC ACh/GABA co-release produces DSI around
   0.39, while uncorrelated (or AMB-broadened) release collapses DSI to around 0.25, an
   approximately 36 percent drop [deRosenroll2026]. The AMB spatial footprint has a decay constant
   tau ~ 27 um, so subunits within ~ 100 um of the pipette are degraded while distant subunits and
   somatic E/I are spared.

2. **Nav1.6 / Nav1.2 V_half / tau / slope parameters (Kole2008, Hu2009)** - **Unresolved, but
   deprioritised.** The deRosenroll companion code [dsMicro-GH] does not implement a Nav1.6 / Nav1.2
   AIS split. It uses a single `HHst_noiseless.mod` (Hodgkin-Huxley-style Na+ / K+) on soma and
   primary dendrites only, with no explicit axon initial segment. Adding AIS kinetics would
   therefore diverge from the source. This finding contradicts the Recommendations in
   `research_papers.md` that called for a Van Wart 2007 / Werginz 2020 AIS overlay; that overlay is
   now out of scope for the port.

3. **Kv1.2 AIS density (KoleLetzkus2007)** - **Resolved as not applicable**. Same reasoning as gap
   2: without an explicit AIS section, no Kv1.2 density is required.

4. **MOD-file parameter values for the companion repository [dsMicro-GH]** - **Resolved**. Reading
   `ei_balance.py`, `HHst_noiseless.mod`, `cadecay.mod`, and `Exp2NMDA.mod` gave the full parameter
   set: Ra = 100 Ohm*cm, cm = 1 uF/cm^2, gleak = 5e-5 S/cm^2, eleak = -60 mV, gbar_Na = 150, 200, 30
   mS/cm^2 (soma / primary / distal), gbar_K = 35, 40, 25 mS/cm^2, ACh Exp2Syn 0.5/6 ms with gmax =
   140.85 pS, GABA Exp2Syn 0.5/35 ms with gmax = 450.72 pS, NMDA Exp2NMDA 2/80 ms with gmax = 140.85
   pS, Ca2+ decay tau = 10 ms, celsius = 36.9 C, dt = 0.1 ms. AR(2) release-rate noise with phi =
   [0.9, -0.1] and cross-channel correlation 0.6, calibrated to Cafaro and Rieke 2010 voltage-clamp
   data, reproduces the E/I noise spectrum. GABA is scaled 1.8x to match the empirical I:E ratio.

5. **Whole-cell-vs-subunit DSI dissociation magnitude** - **Resolved**. Somatic E/I ratio is
   preserved under AMB (p > 0.05) while dendritic Ca2+ subunit DSI drops significantly. The spatial
   signature of AMB (tau ~ 27 um) confirms this is a subcellular rather than global effect
   [deRosenroll2026].

**Additional note flagged back to the implementation plan**: paper text and repository code disagree
on Ra (paper: 200; code: 100), eleak (paper: -65; code: -60), and Na/K densities (paper: 200/70/35
and 40/12/18; code: 150/200/30 and 35/40/25). The repository values are authoritative for the port
[dsMicro-GH].

## Search Strategy

**Sources searched**: (a) the manually-uploaded PDF at the staging path
`C:\Users\md1avn\Documents\GitHub\neuron-channels-staging\de_rosenroll_2026.pdf` extracted with
`pdftotext`; (b) the companion Zenodo archive [dsMicro-Zenodo] at DOI 10.5281/zenodo.17666158; (c)
the companion GitHub repository [dsMicro-GH] at `geoffder/ds-circuit-ei-microarchitecture`,
specifically the `ei_balance.py` driver, the `RGCmodelGD.hoc` morphology, and the MOD sources
`HHst_noiseless.mod`, `cadecay.mod`, and `Exp2NMDA.mod`; (d) Cell Reports landing page at the
Elsevier ScienceDirect URL [CellRep-Page].

**Queries executed** (5 total):

1. WebFetch `https://zenodo.org/records/17666158` to confirm DOI resolves and extract repository
   metadata (version, deposit date, file manifest).
2. WebFetch `https://github.com/geoffder/ds-circuit-ei-microarchitecture` (root) and the raw
   `ei_balance.py`, `modelUtils.py`, `experiments.py`, `SacNetwork.py`, `NetQuanta.py`, `Rig.py`
   files to locate biophysics and synaptic parameters.
3. WebFetch
   `https://raw.githubusercontent.com/geoffder/ds-circuit-ei-microarchitecture/main/RGCmodelGD.hoc`
   and the `.mod` files under `mechanisms/` to extract channel and synaptic MOD parameters.
4. `pdftotext` extraction of the manually-uploaded [deRosenroll2026] PDF and grep for "DSI",
   "ambenonium", "AMB", "correlated", "tau", "HHst", and "celsius" to pin numerical values.
5. WebFetch `https://www.sciencedirect.com/science/article/pii/S2211124725013968` to confirm
   publication metadata (venue, date, DOI, ScienceDirect URL) [CellRep-Page].

**Date range**: 2025-2026 publication window for the primary paper; the companion repository code
was reviewed at its current state (2026-04 snapshot). Foundational references cited inside the paper
(Briggman 2011 connectome, Cafaro-Rieke 2010 noise calibration) were not independently searched
because they are already covered by `research_papers.md` corpus entries.

**Inclusion criteria**: Must provide (a) quantitative AChE-block phenotype numbers, (b) concrete
MOD-file parameter values, (c) explicit synaptic kinetics or conductance densities, or (d) the
noise-process specification. Excluded: general reviews, unrelated retinal modeling work, or
secondary summaries.

**Search iterations**: Query 2 was split into per-file WebFetches because initial WebFetch of the
repo root returned only a file listing. Biophysics parameters were located only after the fifth
per-file fetch (`ei_balance.py`); earlier fetches of `modelUtils.py`, `experiments.py`,
`SacNetwork.py`, `NetQuanta.py`, and `Rig.py` returned no channel densities. Query 4 was added after
WebFetch of `RGCmodelGD.hoc` showed only morphology (shape3d_1..13, topology) with no biophysics,
confirming that the biophysics lives exclusively in the Python driver.

## Key Findings

### Quantitative AChE-Block Phenotype and DSI Benchmarks

The paper [deRosenroll2026] provides the two numerical targets that were missing from the corpus.
Correlated ACh/GABA co-release at SAC varicosities yields DSI around **0.39**, while decorrelating
the two transmitters (or broadening ACh spatially with ambenonium) drops DSI to around **0.25**, a
~36 percent reduction. The spatial signature of AMB is a Gaussian-like decay with tau ~ **27 um**
around the pipette tip. Subunits closer than ~100 um lose DS tuning; subunits farther than ~100 um
and somatic spike output are preserved. Critically, the global somatic E/I ratio is statistically
unchanged (p > 0.05), establishing the subcellular-vs-global dissociation that defines the paper.

### Repository Biophysics and Synaptic Parameters

The companion code [dsMicro-GH] exposes every parameter required to reproduce the model (confirmed
by direct file read). The DSGC morphology has **341 sections** imported from `RGCmodelGD.hoc`.
Passive properties in the code: Ra = **100 Ohm*cm**, cm = **1 uF/cm^2**, gleak = **5e-5 S/cm^2**,
eleak = **-60 mV**. Active conductances use the custom `HHst_noiseless.mod` mechanism on soma and
primary dendrites only (no AIS, no axon): gbar_Na = **150, 200, 30 mS/cm^2** and gbar_K = **35, 40,
25 mS/cm^2** across soma, primary, and distal compartments. Synaptic inputs use Exp2Syn point
processes for ACh (tau1/tau2 = **0.5/6 ms**, E_rev = 0 mV, gmax = **140.85 pS**), GABA (**0.5/35
ms**, E_rev = -60 mV, gmax = **450.72 pS**), and AMPA (0.2/4 ms). NMDA uses `Exp2NMDA.mod` with Mg2+
block (**2/80 ms**, gmax = **140.85 pS**). Intracellular Ca2+ buffering via `cadecay.mod` with tau =
**10 ms**. Simulation runs at **celsius = 36.9 C** and **dt = 0.1 ms**.

### AR(2) Correlated Release Noise Model

Each SAC varicosity co-releases ACh and GABA with correlated, noisy release rates drawn from an
autoregressive AR(2) Gaussian process with **phi = [0.9, -0.1]** and cross-transmitter correlation
peak **rho = 0.6** [deRosenroll2026, dsMicro-GH]. This process is calibrated to Cafaro and Rieke
2010 oscillating voltage-clamp data. The GABA conductance is scaled **1.8x** to compensate for
chloride-reversal dynamics so the modeled I:E ratio matches the experimental observation. This is a
notable departure from the simpler Poisson or independent-release noise in the Hanson 2019 and
Poleg-Polsky 2016 lineages already in the corpus.

### No AIS in the Source Model (Contradicts research_papers.md)

Direct inspection of [dsMicro-GH] confirms that the de Rosenroll 2026 model does **not** contain an
explicit axon-initial-segment section. Spikes are somatic Na-driven using the same
`HHst_noiseless.mod` on soma and primary dendrites. This contradicts the Recommendations section of
`research_papers.md`, which advised overlaying a Van Wart 2007 / Werginz 2020 AIS parameterised with
Kole 2008 / Hu 2009 Nav1.6 / Nav1.2 kinetics. That overlay is now out of scope for the port:
reproducing the paper requires the single-`HHst_noiseless` channel set. Any AIS split should be
saved as a follow-up suggestion rather than included in the initial port.

### Stimulus Protocol and DSI Metric

The moving-bar stimulus uses **8 directions**, bar velocity **1 mm/s**, bar width **250 um**, with a
**30 um** minimum offset between SAC somata and their DSGC contacts (Briggman 2011 connectome
[deRosenroll2026]). DSI is computed as the normalized vector sum of spike counts across directions.
This differs in direction count from the project-standard t0022 / t0023 **12-angle** protocol; the
port must either (a) use 8 directions to match the paper, (b) extend to 12 for project consistency,
or (c) report both. Recommendation: run both and report the 8-direction DSI as the paper-match
benchmark (DSI ~ 0.39) and the 12-angle DSI as the project-comparable metric.

## Methodology Insights

* **Use the repository values, not the paper-text values, where they disagree.** Ra = 100 Ohm*cm
  (code) vs 200 Ohm*cm (paper text); eleak = -60 mV (code) vs -65 mV (paper text); gbar_Na =
  150/200/30 (code) vs 200/70/35 mS/cm^2 (paper text); gbar_K = 35/40/25 (code) vs 40/12/18 mS/cm^2
  (paper text) [dsMicro-GH]. The code is what actually produced the published DSI numbers;
  paper-text alternatives should be logged in the plan and tested as a sensitivity sweep only.

* **Adopt the AR(2) correlated release-rate noise model.** Independent Poisson release will not
  reproduce the Cafaro-Rieke 2010 noise spectrum or the correlated-vs-uncorrelated DSI contrast
  [deRosenroll2026]. Implement AR(2) with phi = [0.9, -0.1] and a 2-channel Gaussian
  cross-correlation rho = 0.6.

* **Skip the AIS overlay.** The port must not add a Nav1.6 / Nav1.2 AIS split; doing so would
  diverge from the source and change the spike output distribution. Treat Van Wart 2007 / Werginz
  2020 AIS kinetics as a follow-up suggestion, not as part of this port.

* **Place SAC varicosities by connectome, not by rule.** The model depends on individual release
  sites positioned per Briggman 2011 with a 30 um minimum SAC-soma offset. Lumping varicosities into
  a handful of compartments will destroy the subcellular DS signal that the paper reports
  [deRosenroll2026].

* **Benchmark with the two DSI targets.** DSI ~ 0.39 (correlated) and DSI ~ 0.25 (uncorrelated) are
  the port validation targets. Any reimplementation must recover the ~36 percent DSI drop under ACh
  decorrelation or AMB-style spatial broadening.

* **Hypothesis (testable in this task)**: extending the direction set from 8 to 12 angles will yield
  a slightly higher DSI (tighter vector-sum resolution) but preserve the correlated-vs- uncorrelated
  contrast. If true, 12-angle DSI serves as a monotone rescaling of 8-angle DSI and can be used as
  the project-consistent metric.

* **Hypothesis (follow-up)**: adding a Nav1.6 / Nav1.2 AIS overlay on top of the de Rosenroll base
  model (as originally suggested by `research_papers.md`) would increase somatic spike threshold
  sharpness but leave dendritic subunit DSI unchanged. This is a follow-up task, not part of this
  port.

## Discovered Papers

No new papers were discovered that need to be added to the corpus.

Rationale: the central paper [deRosenroll2026] is already present as a paper asset in this task; the
companion code is a repository, not a paper; and the foundational references cited inside the paper
(Briggman 2011, Cafaro-Rieke 2010) are already covered by prior tasks in the corpus. The frontmatter
field `papers_discovered` is therefore **0**.

## Recommendations for This Task

1. **Use the [dsMicro-GH] repository parameters as the authoritative source.** Passive: Ra = 100
   Ohm*cm, cm = 1 uF/cm^2, gleak = 5e-5 S/cm^2, eleak = -60 mV. Active: `HHst_noiseless` with
   gbar_Na 150/200/30 and gbar_K 35/40/25 mS/cm^2 on soma/primary/distal. Log paper-text
   alternatives (Ra 200, eleak -65, Na 200/70/35, K 40/12/18) for sensitivity sweep only. This
   updates `research_papers.md` Recommendations.

2. **Drop the Nav1.6 / Nav1.2 AIS overlay from the port.** The source model has no axon initial
   segment; adding one would diverge from the published biophysics [dsMicro-GH, deRosenroll2026].
   File a follow-up suggestion for a separate AIS-augmented variant.

3. **Implement the AR(2) correlated release-rate noise exactly as specified.** phi = [0.9, -0.1],
   cross-channel rho = 0.6, 1.8x GABA scaling, calibrated to Cafaro-Rieke 2010.

4. **Port synaptic kinetics verbatim**: ACh Exp2Syn 0.5/6 ms 140.85 pS; GABA Exp2Syn 0.5/35 ms
   450.72 pS; NMDA Exp2NMDA 2/80 ms 140.85 pS with voltage-dependent Mg2+ block; AMPA Exp2Syn 0.2/4
   ms. Ca2+ decay tau 10 ms.

5. **Validate against two DSI benchmarks**: DSI ~ 0.39 (correlated ACh/GABA) and DSI ~ 0.25
   (uncorrelated). The port must recover the ~36 percent drop; otherwise the noise process or
   correlation structure is misimplemented.

6. **Run both 8-direction (paper-match) and 12-angle (project-consistent) stimulus protocols.**
   Report 8-angle DSI as the primary paper-match metric, 12-angle DSI as the project-standard
   comparison to t0022 and t0023.

7. **Preserve 36.9 C simulation temperature and dt = 0.1 ms.** These are part of the parameter set
   that the code uses and they affect channel kinetics.

## Source Index

### [deRosenroll2026]

* **Type**: paper
* **Title**: Uncovering the "hidden" synaptic microarchitecture of the retinal direction selective
  circuit
* **Authors**: deRosenroll, G., Sethuramanujam, S., Awatramani, G. B.
* **Year**: 2026
* **DOI**: `10.1016/j.celrep.2025.116833`
* **URL**: https://www.sciencedirect.com/science/article/pii/S2211124725013968
* **Peer-reviewed**: yes (Cell Reports)
* **Relevance**: Primary source. Provides the DSI benchmarks (correlated 0.39 vs uncorrelated 0.25),
  the AMB decay constant (tau ~ 27 um), the AR(2) noise parameters, the stimulus protocol, and the
  subcellular-vs-global E/I dissociation result. Asset stored at
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/`.

### [dsMicro-Zenodo]

* **Type**: dataset
* **Title**: deRosenroll et al. 2026 DS circuit E/I microarchitecture model code
* **Author/Org**: deRosenroll, G.; Awatramani lab (University of Victoria)
* **Date**: 2026-02
* **URL**: https://zenodo.org/records/17666158 (DOI 10.5281/zenodo.17666158)
* **Peer-reviewed**: no (code archive)
* **Relevance**: Authoritative archived snapshot of the NEURON model code and MOD files. Contains
  the `RGCmodelGD.hoc` morphology, the `HHst_noiseless.mod`, `cadecay.mod`, and `Exp2NMDA.mod`
  mechanisms, and the Python driver. This is the frozen reference for the port.

### [dsMicro-GH]

* **Type**: repository
* **Title**: ds-circuit-ei-microarchitecture
* **Author/Org**: Geoff deRosenroll (`geoffder` on GitHub)
* **URL**: https://github.com/geoffder/ds-circuit-ei-microarchitecture
* **Last updated**: 2026-02 (tracks the Zenodo snapshot)
* **Peer-reviewed**: no (live code)
* **Relevance**: Primary source for all biophysics and synaptic parameter values. The
  `ei_balance.py` driver contains the authoritative Ra, cm, gleak, eleak, gbar_Na, gbar_K, synaptic
  conductance and kinetic values, the AR(2) noise model (phi = [0.9, -0.1], rho = 0.6), and the 1.8x
  GABA scaling factor. Use the repository values over the paper-text values where they disagree.

### [CellRep-Page]

* **Type**: documentation
* **Title**: Cell Reports ScienceDirect article landing page for deRosenroll 2026
* **Author/Org**: Elsevier / Cell Reports
* **URL**: https://www.sciencedirect.com/science/article/pii/S2211124725013968
* **Peer-reviewed**: yes (the underlying article is peer-reviewed)
* **Relevance**: Confirms venue (Cell Reports, journal), publication date (2026-02-24), DOI, and
  canonical landing-page URL recorded in the paper asset `details.json`.

### [Briggman2011]

* **Type**: paper
* **Title**: Wiring specificity in the direction-selectivity circuit of the retina
* **Authors**: Briggman, K. L., Helmstaedter, M., Denk, W.
* **Year**: 2011
* **DOI**: `10.1038/nature09818`
* **URL**: https://www.nature.com/articles/nature09818
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Source of the SAC to DSGC connectome that the deRosenroll model uses to place
  varicosities. Already covered by prior corpus tasks; cited here to document provenance of the 30
  um SAC-soma offset and wiring asymmetry encoded in the port.

### [CafaroRieke2010]

* **Type**: paper
* **Title**: Noise correlations improve response fidelity and stimulus encoding
* **Authors**: Cafaro, J., Rieke, F.
* **Year**: 2010
* **DOI**: `10.1038/nature09576`
* **URL**: https://www.nature.com/articles/nature09576
* **Peer-reviewed**: yes (Nature)
* **Relevance**: Provides the oscillating voltage-clamp E/I noise correlation data that
  [deRosenroll2026] uses to calibrate the AR(2) release-rate noise process (rho = 0.6 peak
  correlation). Cited to justify the choice of cross-transmitter correlation in the port.
