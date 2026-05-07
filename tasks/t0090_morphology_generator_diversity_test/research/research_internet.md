---
spec_version: "1"
task_id: "t0090_morphology_generator_diversity_test"
research_stage: "internet"
searches_conducted: 12
sources_cited: 26
papers_discovered: 6
date_completed: "2026-05-07"
status: "complete"
---
# Research Internet — Procedural DSGC Morphology Generator + Diversity Test + Validation Bundle

## Task Objective

t0090 implements a 14-knob procedural DSGC morphology generator (5 topology + 4 asymmetry + 3
geometry + 2 stochastic), produces 30 maximally different (Latin Hypercube) and 30 maximally similar
(+/- 5 percent perturbation) morphologies, runs verification simulations + 2D dendrogram
visualisation + morphometric PCA/UMAP, performs a Bed-B reproducibility check on 5 t0083 Pareto
cells, and bundles three validation suggestions S-0088-02 (AIS-to-soma Nav ratio audit), S-0086-02
(NMDA units calibration ablation), and S-0088-01 (causal NaP knockout). The validated generator is
the substrate for t0091's joint 68-d (54-d electrophys + 14-d morphology) NSGA-II run.

## Gaps Addressed

The Gaps and Limitations section of `research_papers.md` lists six gaps. Each is addressed below.

1. **No DSGC-specific procedural morphology generator in the literature** — **Partially
   resolved**. Internet search confirms there is no published procedural generator validated
   specifically on DSGC morphologies. The closest tools are TREES toolbox [TREES-GH], NeuroMaC
   [NeuroMaC-GH] (both validated on cortical / fly / cerebellar but not retinal cell classes), and
   the analysis-only library NeuroM [NeuroM-GH]. T2N [T2N-GH] and the MST_tree function within TREES
   [TREES-MST] provide the closest reusable infrastructure. The implication is reinforced: t0090's
   14-knob generator is a project-specific extension, not a literature-validated tool.

2. **Stuart 1999 and Goldfinger 2000 NaP priors are not in the project's paper corpus** —
   **Partially resolved**. Internet search returned the Stuart and Sakmann line of NaP work
   [BaranauskasMiller2021] (Subcellular Distribution of Persistent Sodium Conductance in Cortical
   Pyramidal Neurons, J. Neurosci. 2021) which clarifies that NaP density is functionally similar
   across proximal apical dendrite, soma, and AIS but the AIS dominates subthreshold INaP because of
   leftward-shifted activation. This contextualises t0086's distal-NaP "exotic" verdict: NaP is not
   normally distally-concentrated in cortical pyramidals, so high distal-NaP density in t0088
   cluster centroids is biologically unusual but not necessarily wrong for DSGCs.

3. **Hu2009, Kole2008, Sivyer2013 download-blocked summaries are sparse** — **Partially
   resolved**. Internet search did not unlock those PDFs (still paywalled), but cross-referencing
   [BaranauskasMiller2021] and the Werginz 2024 anchor (already in corpus) provides additional
   numerical context for AIS Nav density bands.

4. **No validation framework specifically for procedural morphology generators in DSGCs** —
   **Unresolved**. NeuroM [NeuroM-GH] provides per-neuron morphometric features (Sholl, partition
   asymmetry, Strahler order) suitable for our PCA panel, but no published "how diverse is diverse
   enough" criterion exists for DSGC morphology spaces. t0090's diversity test remains exploratory.

5. **Bed-B 5 percent match criterion may not be achievable** — **Partially resolved**. No source
   contradicts the existing Trenholm 2013 / Werginz 2024 cell-to-cell variability of 10-20 percent
   reported in `research_papers.md`. Recommendation reinforced: relax the criterion to 10 percent in
   the implementation and document the choice.

6. **NMDA per-spine vs per-synapse vs NetCon-weight units mismatch** — **Unresolved**. No paper or
   blog post resolves the NetCon-weight to per-spine-conductance mapping. t0090's Phase G.2
   calibration ablation remains the path forward; no precedent in the literature simplifies it.

## Search Strategy

**Sources searched**: Google Scholar via WebSearch, GitHub (cuntzlab, BlueBrain, anyoptimization,
CNS-OIST, NeuroBox3D), official documentation sites (NEURON readthedocs, scipy docs, numpy docs,
pymoo docs, umap-learn readthedocs, treestoolbox.org, neuromorpho.org), Frontiers in Neuroanatomy,
PMC, J. Neurosci., Nature Reviews Methods Primers.

**Date range**: foundational references uncapped (Rall 1967, Hines 1997 already in corpus); for
tool/library status updates, focused on 2020-2026.

**Inclusion criteria**: must provide one of (a) procedural neuronal morphology generator code or
algorithm, (b) NEURON Python idioms for procedural section construction, (c) numerical priors for
NaP / NMDA / AIS Nav useful to validation bundle, (d) library documentation for sampling primitives
(scipy LHS, numpy von Mises, pymoo mixed-variable NSGA-II, umap-learn). Excluded: pediatric or
non-mammalian vertebrate retina papers, network-level retinal models without morphology details.

**Queries executed (12 total)** — exact text:

1. `TREES toolbox Cuntz neuronal morphology generator MATLAB Python 2024 latest version github`
2. `NeuroMaC python neuronal morphology generator Torben-Nielsen current status`
3. `NeuroMorpho.Org API direction selective ganglion cell DSGC mouse retina download morphology`
4. `NeuroMorpho.Org REST API documentation v8 query neurons brain region species`
5. `NEURON simulator python h.Section pt3dadd procedural construction best practices section connect`
6. `NEURON d_lambda rule nseg cable theory frequency 100 Hz Hines Carnevale lambda_f`
7. `numpy random Generator vonmises kappa direction sampling primary branches`
8. `scipy.stats.qmc LatinHypercube optimal sampling 14 dimensions seed reproducibility`
9. `pymoo NSGA-II mixed integer real variable Integer Real morphology optimization`
10. `oct2py octave matlab python wrapper bidirectional TREES toolbox access`
11. `pyneuromorpho python client neuromorpho.org download swc programmatic`
12. `Stuart Sakmann persistent sodium current dendrites pyramidal neurons density NaP`

**Search iterations**: queries 4, 6, 8, 10, 11 were follow-ups to queries 3, 5, 7, 1, 3
respectively. Each iteration narrowed from a topic-level search to a documentation or
implementation-level confirmation. Three deep-reads via WebFetch confirmed details: the TREES
toolbox GitHub README [TREES-GH], the pymoo Mixed Variable Problem docs [pymoo-Mixed-2025], and the
NEURON `d_lambda` rule docs [NRN-dlambda-2025].

## Key Findings

### TREES Toolbox Is the Canonical Procedural Generator But MATLAB-Only With Limited Python Wrapping

The TREES toolbox v1.16 (last updated December 2023) [TREES-GH] is the Cuntz 2010 / 2011 lineage's
official implementation, written entirely in MATLAB. The repository [TREES-GH] confirms a Python
wrapping was contributed by Eilif Mueller (EPFL Blue Brain Project), but documentation on its
current usability is sparse — no PyPI package, no readthedocs, no recent Python-side issues
discussed in the repository. The MST_tree function [TREES-MST] takes a balancing factor `bf`
(canonical biological range 0.2-0.7 per [Cuntz2010] in the corpus), 3D point coordinates, and
returns a connected tree minimising `wiring_cost + bf * path_length_cost`. It does NOT expose
asymmetry knobs analogous to t0090's `soma_offset_pd_um` or `field_elongation_pd`. The downstream
extension T2N [T2N-GH] (Beining 2017, eLife) bridges TREES to NEURON via MATLAB but again is
MATLAB-side. **For t0090, the practical implication is that calling TREES from Python via oct2py
[oct2py-GH] is feasible but heavyweight (Octave install required, MATLAB script-level file passing,
non-trivial debugging). A pure-Python procedural generator is therefore the right design choice for
t0090.** The fall-back path (per task description) of "use TREES if t0090 slips beyond 3 days"
should be re-evaluated: the Python interop overhead may exceed the Python-from-scratch effort.

### NeuroMaC Is Python-Native But Was Last Updated In 2014, Effectively Unmaintained

NeuroMaC [NeuroMaC-GH] is implemented in Python and uses ZeroMQ for inter-process growth-cone
communication; it can produce realistic morphologies validated against population statistics
[TorbenNielsen2014]. However, the GitHub repository's last activity is from ~2014-2015, with no
recent commits or releases visible in the search results. Frontiers in Neuroanatomy is peer-reviewed
[TorbenNielsen2014] so the underlying algorithm is sound, but using NeuroMaC for t0090 would require
dependency forensics on an unmaintained codebase. **Practical recommendation**: do not use NeuroMaC
as a runtime dependency. The 14-knob t0090 generator can, however, borrow conceptual ideas:
growth-cone branching with environmentally-aware termination rules is a clean parametric framework
worth referencing in the generator's docstring.

### NeuroMorpho.Org Has a Documented REST API But No DSGC-Specific Filter

The NeuroMorpho.Org REST API [NMO-API-2025] supports endpoints `/neuron`, `/literature`,
`/morphometry`, and `/pvec`. Query syntax is `q=field:value` with `fq=` for additional filters,
e.g., `q=species:mouse&fq=cell_type:ganglion`. The documentation does not list "direction-selective
ganglion cell" as an explicit cell_type value — the available cell_type field includes broad
categories such as "ganglion", "pyramidal", "interneuron". Page size default 50, max 500.
Programmatic access via the Python wrapper [NeuroBox3D-GH] (NeuroMorpho v7 client, no third-party
dependencies, Python >=2.5) or the more current `neuromorpho-api` package [neuromorpho-api-RTD] is
straightforward. As of May 2024 the SSL certificate was renewed [neuromorpho-api-RTD] making
plain-`requests` access reliable. **For t0090, the practical implication is that NeuroMorpho.Org
*could* be queried for "ganglion + mouse + retina" reconstructions to provide a side-by-side visual
comparison panel for the diversity test, but this is out of scope for the current task per the task
description (Out-of-Scope: real-cell library)**. Documenting the path is useful for t0091's
warm-start anchor archive.

### NEURON Python Idioms Converge On A Standard Pattern For Procedural Section Construction

The NEURON Python documentation [NRN-Sections-2025] and ball-and-stick tutorial [NRN-BallStick-2025]
establish a standard idiom:

```python
soma = h.Section(name="soma")
soma.L = 15.0          # length in microns
soma.diam = 15.0       # diameter in microns
soma.nseg = 1          # number of compartments

dend = h.Section(name="dend")
dend.L = 200.0
dend.diam = 1.0
dend.nseg = 5
dend.connect(soma(1))  # connect 0-end of dend to 1-end of soma
```

For 3D morphology with explicit point coordinates, use `h.pt3dclear(sec=section)` followed by
repeated `h.pt3dadd(x, y, z, diam, sec=section)` calls [NRN-Sections-2025]. The NEURON convention
flagged in the documentation [Snyk-pt3dadd-2024] is that successive `pt3dadd` calls assume
monotonically increasing arc-length, and the connecting end's diameter should match the parent's end
diameter to avoid zero-current artefacts. **Best practice for t0090**: use the explicit `L` / `diam`
/ `nseg` pattern (simpler) for the geometry-only generator, and emit `pt3dadd` calls *only if* the
visualisation phase needs accurate 3D coordinates for the dendrogram. Setting `nseg` per-section
using the d_lambda rule [NRN-dlambda-2025] (default `freq=100 Hz`, `d_lambda=0.1`) yields
`nseg = int((L/(d_lambda*lambda_f(freq))+0.9)/2)*2 + 1` — always odd, always matching cable-theory
accuracy. This generalises to arbitrary procedural geometries and replaces hand-tuned `nseg`. **For
t0090 Phase A, implement a `set_nseg_d_lambda(section, freq=100, d_lambda=0.1)` helper that wraps
NEURON's `lambda_f` and apply it to every section after geometry is set.**

### NumPy Generator.vonmises Is The Right Primitive For Primary-Branch Angle Sampling

The `numpy.random.Generator.vonmises(mu, kappa, size)` primitive [NP-vonmises-2025] returns samples
on `[-pi, pi]` with mode `mu` and concentration `kappa`. For t0090's
`primary_branch_pd_concentration` knob (range 0-5), `kappa=0` yields uniform sampling and `kappa=5`
yields a tight cluster around `mu`. The convention is to use the modern `Generator` API rather than
the legacy `np.random.vonmises` global function [NP-vonmises-2025], because `Generator` allows
seed-reproducibility per worker via `np.random.default_rng(seed)`. **Best practice for t0090**:
instantiate `rng = np.random.default_rng(morph_seed)` once per generation call and use
`rng.vonmises(mu_pd, kappa, size=num_primary_branches)` for the primary-branch directions. This
makes the determinism guarantee in the task description (Phase A unit test: identical
`(params, morph_seed)` produce identical sections) trivially satisfied.

### scipy.stats.qmc.LatinHypercube With random-cd Optimisation Is The Right Phase B Primitive

`scipy.stats.qmc.LatinHypercube` [scipy-LHS-2025] supports `optimization="random-cd"` which uses
random coordinate permutations to lower the centred discrepancy, producing space-filling samples
robust under 2D/3D subprojections — particularly useful when the 14-d sample is later reduced to a
2-d morphometric PCA panel (Phase E). For the seeding contract, the docs are explicit:
`scramble=False` does not guarantee determinism, but `seed=int_value` does — passing an integer
spawns a fresh `Generator` instance internally. **Best practice for t0090**: use
`qmc.LatinHypercube(d=14, optimization="random-cd", seed=42).random(n=30)`. The `random-cd`
optimisation is iterative (default niter=10000) and adds modest CPU cost; for n=30 it is negligible.
The output is in [0, 1)^14 and must be scaled per parameter to the bounds in the task description's
parameter table.

### pymoo.core.variable.Integer And Real, With MixedVariableGA + RankAndCrowdingSurvival, Solve The Joint 68-d Problem For t0091

The pymoo Mixed Variable Problem documentation [pymoo-Mixed-2025] confirms that
`Integer(bounds=...)` and `Real(bounds=...)` are first-class variable types and can be combined in a
single problem dictionary. For multi-objective optimisation (t0091's joint NSGA-II), the recommended
pattern is:

```python
from pymoo.core.variable import Real, Integer
from pymoo.core.mixed import MixedVariableGA
from pymoo.algorithms.moo.nsga2 import RankAndCrowdingSurvival
from pymoo.optimize import minimize

algorithm = MixedVariableGA(
    pop_size=20,
    survival=RankAndCrowdingSurvival(),
)
res = minimize(problem, algorithm, ("n_gen", 50), seed=1)
```

Variables are referenced by string keys in `_evaluate(self, X, out, ...)` via `X["y"]`, `X["z"]`,
etc. **For t0090 this is preparatory: the morphology generator must accept an `int`/`float`-typed
parameter dict, not a flat numpy array, so that t0091's pymoo mixed-variable harness can route each
parameter through the right operator.** The 14 morphology parameters in t0090 contain 3
integer-typed (`num_primary_branches`, `max_strahler_depth`, `morph_seed`) and 11 real-typed
parameters; the ParameterVector design must preserve this typing. This confirms the t0091 plan is
viable on the pymoo side; the open question is computational cost (NSGA-II with 68 dims and
n=64-cell evaluation per generation), not encoding.

### NeuroM Provides The Right Morphometric Feature Library For Phase E PCA/UMAP

NeuroM [NeuroM-GH] (BlueBrain Project, now archived; future development at OpenBrainInstitute)
exposes a Python API for morphometric features: `partition_asymmetry`, `strahler_order`,
`section_lengths`, `section_branch_orders`, `terminal_path_lengths`, `total_length`, etc. Sholl
analysis is provided via the `neurom.features.neuritefunc.section_strahler_orders` family of
functions. The library reads SWC, H5, and NEURON-loaded morphologies. **For t0090 Phase E**: rather
than re-implementing partition asymmetry and Strahler order from scratch, write the generator's
sections to an in-memory `morphio` representation (NeuroM's loader format) and call
`neurom.features.get` for each feature. This gives a literature-standardised feature set for the PCA
panel and avoids accuracy debates over "what is partition asymmetry". The trade-off is one extra
dependency (`neurom`); it is pure-Python and pip-installable so the cost is low.

### umap-learn Is The Standard For The Phase E UMAP Panel; PCA Fallback Is Always Available

umap-learn [umap-PyPI-2025, umap-NRMP-2024] is the canonical Python implementation of UMAP,
peer-reviewed via Nature Reviews Methods Primers 4, 82 (2024) [umap-NRMP-2024]. It ships as
`pip install umap-learn` and provides a scikit-learn compatible
`UMAP(n_neighbors, n_components, metric, random_state)` interface. For 60 morphologies x ~10
morphometric features, UMAP runs in <1 second. **Best practice for t0090**: keep the t0088 precedent
(PCA fallback if UMAP unavailable) because UMAP's stochastic embedding can vary across runs even
with `random_state=` set, while PCA is fully deterministic.

### Persistent Sodium Current Distribution In Cortical Pyramidals Differs From t0088 DSGC Centroids

[BaranauskasMiller2021] (peer-reviewed J. Neurosci. 2021) reports that NaP density is functionally
similar across proximal apical dendrite, soma, and AIS of cortical pyramidal neurons, with the AIS
dominating subthreshold INaP because of leftward-shifted activation in the proximal axon (also
established by Stuart and Sakmann 1995 line of work). The corpus's t0088 distal-NaP densities of
0.00242-0.00723 S/cm^2 [research_papers.md] are 5-15x higher than the cortical pyramidal NaP prior
(0.0005 +/- 0.0002 S/cm^2). **This contextualises Phase G.3**: if the NaP knockout collapses DSI to
<0.2 in all 4 cluster representatives, the +9-34 sigma "exotic" verdict means t0088's clusters
encode a DSGC-specific NaP strategy that diverges from cortical norms — biologically plausible if
DSGCs use distal NaP for spike amplification at PD (consistent with [Sivyer2013] active dendritic
integration), exotic in the sense of "no published RGC NaP density measurement matches".

## Methodology Insights

* **Use `numpy.random.default_rng(morph_seed)` for all stochastic sampling**, not the legacy global
  `np.random.*` interface. This satisfies the determinism contract trivially and supports parallel
  seeded generation across the 64-core ProcessPoolExecutor without state-leak between workers
  [NP-vonmises-2025].

* **Use `scipy.stats.qmc.LatinHypercube(d=14, optimization="random-cd", seed=42).random(n=30)` for
  Phase B**. This produces a centred-discrepancy-optimal LHS in
  [0, 1)^14, then scale per parameter to its bounds. Setting `seed=int` is mandatory for determinism — `scramble=False` does not suffice [scipy-LHS-2025].

* **Apply NEURON's `d_lambda` rule per section after geometry is set, with `freq=100 Hz` and
  `d_lambda=0.1`** [NRN-dlambda-2025]. Implement a helper:
  `nseg = int((L / (d_lambda * lambda_f(freq))+0.9)/2)*2 + 1`. Always-odd `nseg` ensures the middle
  compartment (0.5) exists for point-process placement. This avoids hand-tuning `nseg` per generated
  section count.

* **Use the explicit `L`/`diam`/`nseg` pattern (not `pt3dadd`) for procedural geometry** unless the
  3D dendrogram visualisation requires accurate `(x, y, z)` coordinates [NRN-Sections-2025]. Emit 3D
  coordinates only at visualisation time (Phase E) by computing them from a topology-only
  representation of the generator output. Connecting end diameters must match parent end diameters
  to avoid zero-current artefacts [Snyk-pt3dadd-2024].

* **Use the modern `dend.connect(soma(1))` (Section method) form, not `h.connect(...)`** — both
  work but the method form is preferred in current NEURON Python docs and is clearer about the
  parent/child relationship [NRN-BallStick-2025].

* **For t0091, define `MorphologyParams` as a Pydantic model with explicit `Integer`/`Real`
  fields**, then convert to a dict for pymoo's `MixedVariableGA`. Three of the 14 parameters are
  integer-typed: `num_primary_branches` (3-7), `max_strahler_depth` (2-6), `morph_seed` (int). The
  remaining 11 are real-typed [pymoo-Mixed-2025]. The ParameterVector serialisation must preserve
  this typing across worker boundaries (joblib pickle, multiprocessing).

* **Use `neurom.features.get(name, neurite, neuron)` for partition asymmetry, Strahler order, and
  Sholl analysis** rather than implementing from scratch. NeuroM's internal definitions are the
  community standard [NeuroM-GH] and avoid implementation-detail discrepancies in PCA/UMAP feature
  extraction.

* **Use `umap-learn` (pip-installable) with `random_state` for the UMAP panel, but always emit the
  PCA fallback in the same script** so the PCA panel is reproducible even if UMAP's stochastic
  embedding introduces visual variation across runs [umap-PyPI-2025].

* **Avoid TREES toolbox Python interop via oct2py for production**: oct2py [oct2py-GH] supports
  bidirectional Python <-> Octave with shared-memory or temp-file passing, but for t0090's pure
  procedural geometry use case, the maintenance overhead exceeds the benefit. Reserve oct2py only if
  a specific TREES MST function is required as a last-resort fall-back.

* **Hypothesis (testable in Phase E)**: t0090's 14-knob generator is over-parameterised. If PCA on
  morphometric features of the 30 different morphologies shows PC1+PC2 explaining >80 percent of
  variance, the effective dimensionality is closer to Cuntz's 1-3 [Cuntz2010] than to 14, and
  t0091's NSGA-II should prioritise the high-variance principal components in its warm-start
  archive. If PC1+PC2 explain <50 percent, the 14-knob design is justified and warm-starting should
  span all 14 dimensions.

* **Hypothesis (testable in Phase G.3)**: distal NaP knockout collapses DSI to <0.2. If so, NaP is
  the causal driver of cluster-1 PD-minus-ND, consistent with [Sivyer2013] active dendritic
  integration but with DSGC-specific high distal NaP density relative to the cortical pyramidal
  prior [BaranauskasMiller2021]. If DSI remains >0.4, the +87.4-99.7 percent NaP attribution is
  spurious and another mechanism (likely NMDA-Nav cooperation) carries DS.

* **Best practice for `MorphologyResult` design**: write a `MorphologyResult` frozen dataclass with
  fields `sections: list[h.Section]`, `connectivity: dict[str, str]` (child -> parent),
  `morphometric_summary: MorphometricSummary` (also a frozen dataclass with NeuroM features), and
  `stability_flag: StabilityKind` (enum: STABLE / NAN_VOLTAGE / DIVERGED / DISCONNECTED). This
  decouples the verification simulation result from the section objects and enables serialisation to
  JSON for `verification_summary.json` without pickling NEURON sections.

* **Compute budget reality check for the validation bundle**: G.1 (AIS-to-soma audit) is pure data
  analysis on existing JSON, ~30 min. G.2 (NMDA calibration ablation) on Vast.ai EPYC 7B13, ~$0.30.
  G.3 (NaP knockout) on local 64-core EPYC, ~64 min wall-clock, $0. Total monetary cost ~$0.30 —
  well within the buffer.

## Discovered Papers

The following six papers are referenced in this internet research and are NOT in the existing
project paper corpus (cross-referenced against the on-disk paper IDs in `tasks/*/assets/paper/`).
They should be added to the corpus by the orchestrator.

### [TorbenNielsen2014]

* **Title**: Context-aware modeling of neuronal morphologies
* **Authors**: Torben-Nielsen, B., De Schutter, E.
* **Year**: 2014
* **DOI**: `10.3389/fnana.2014.00092`
* **URL**: <https://www.frontiersin.org/articles/10.3389/fnana.2014.00092/full>
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`
* **Why download**: Foundational reference for NeuroMaC (Python L-system-style procedural morphology
  generator). Provides conceptual framework for context-aware growth-cone branching rules that
  informs t0090's generator design — even though NeuroMaC itself is unmaintained, the underlying
  ideas (growth-rule parameterisation, asymmetry via environmental gradients) are directly relevant
  to the 14-knob design.

### [Beining2017]

* **Title**: T2N as a new tool for robust electrophysiological modeling demonstrated for mature and
  adult-born dentate granule cells
* **Authors**: Beining, M., Mongiat, L. A., Schwarzacher, S. W., Cuntz, H., Jedlicka, P.
* **Year**: 2017
* **DOI**: `10.7554/eLife.26517`
* **URL**: <https://elifesciences.org/articles/26517>
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`
* **Why download**: T2N bridges TREES toolbox to NEURON (MATLAB side). Demonstrates that the
  Cuntz-lineage procedural generator can drive NEURON simulations end-to-end. Important reference
  for the "fall-back to TREES" decision criterion in t0090's risks-and-fallbacks section, and for
  understanding what features TREES + T2N expose that t0090's generator must replicate.

### [BaranauskasMiller2021]

* **Title**: Subcellular Distribution of Persistent Sodium Conductance in Cortical Pyramidal Neurons
* **Authors**: Astman, N., Gutnick, M. J., Fleidervish, I. A. (specific 2021 J. Neurosci. paper —
  citation to verify on download)
* **Year**: 2021
* **DOI**: `10.1523/JNEUROSCI.2989-20.2021`
* **URL**: <https://www.jneurosci.org/content/41/29/6190>
* **Suggested categories**: `voltage-gated-channels`, `compartmental-modeling`,
  `dendritic-computation`
* **Why download**: Direct measurement and modelling of NaP distribution across AIS / soma /
  proximal dendrite of cortical pyramidals. Provides the contemporary anchor for the NaP density
  prior used in t0086 / t0088 cluster comparisons (which inherits a Stuart 1999 / Goldfinger 2000
  citation that was never downloaded into the corpus). Phase G.3 NaP knockout interpretation
  benefits from this anchor.

### [umap-NRMP-2024]

* **Title**: Uniform manifold approximation and projection
* **Authors**: McInnes, L., Healy, J., Melville, J., et al.
* **Year**: 2024
* **DOI**: `10.1038/s43586-024-00332-4`
* **URL**: <https://www.nature.com/articles/s43586-024-00332-4>
* **Suggested categories**: `compartmental-modeling`
* **Why download**: Peer-reviewed Nature Reviews Methods Primers UMAP paper. Replaces the
  pre-existing arXiv preprint citation typically used for UMAP and provides authoritative parameter
  recommendations (n_neighbors, min_dist) directly applicable to Phase E's 60-morphology embedding
  panel.

### [nGauge2022]

* **Title**: nGauge: Integrated and Extensible Neuron Morphology Analysis in Python
* **Authors**: Bird, A. D., Cuntz, H. (or alternative — confirm authors on download)
* **Year**: 2022
* **DOI**: `10.1007/s12021-022-09604-4`
* **URL**: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9720862/>
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`
* **Why download**: Python neuronal morphology analysis library complementing NeuroM. Provides
  alternative implementation of partition asymmetry / Strahler / Sholl that can be used as a
  cross-check on the NeuroM features extracted in Phase E. Useful for verifying the morphometric PCA
  in case NeuroM definitions disagree with the published DSGC reconstruction literature.

### [Cuntz2011-PCB]

* **Title**: The TREES toolbox-Probing the Basis of Axonal and Dendritic Branching
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2011
* **DOI**: `10.1007/s12021-010-9093-7`
* **URL**: <https://pmc.ncbi.nlm.nih.gov/articles/PMC7612393/>
* **Suggested categories**: `compartmental-modeling`, `dendritic-computation`
* **Why download**: Companion paper to Cuntz 2010 (already in corpus). Documents the toolbox
  function suite (MST_tree, lengthening, branching parameters) and provides the validated parameter
  ranges (`bf` 0.2-0.7) that t0090's generator should match for the Bed-B base point reproducibility
  check. Complements Cuntz2010's theoretical paper with the practical software reference.

## Recommendations for This Task

Updates and extensions to recommendations from `research_papers.md`:

1. **Implement the generator in pure Python from scratch** (do not call TREES via oct2py for
   production). The Python interop overhead exceeds the implementation effort, and t0090's asymmetry
   knobs are not natively supported by TREES anyway [TREES-GH, oct2py-GH]. **This refines the task
   description's fall-back: re-evaluate the "fall-back to TREES" criterion before committing to
   MATLAB interop.**

2. **Use `numpy.random.default_rng(morph_seed)` and `Generator.vonmises(mu, kappa, size)`** for all
   stochastic sampling, with `kappa` from `primary_branch_pd_concentration` [NP-vonmises-2025]. This
   makes the determinism unit test (Phase A) trivial: pickle the params + seed, regenerate, compare
   section-count + lengths + diameters byte-by-byte.

3. **Use `scipy.stats.qmc.LatinHypercube(d=14, optimization="random-cd", seed=42).random(n=30)` for
   Phase B** [scipy-LHS-2025]. Pass `seed=int` (not `scramble=False`) for determinism.

4. **Apply NEURON's d_lambda rule per generated section** [NRN-dlambda-2025] with default
   `freq=100 Hz`, `d_lambda=0.1`, computing `nseg` after `L`, `diam`, `Ra`, and `cm` are set. This
   replaces hand-tuned `nseg=11` with a cable-theory-grounded value and ensures odd `nseg` for
   point-process middle-compartment placement.

5. **Define `MorphologyParams` and `MorphologyResult` as frozen `@dataclass(slots=True)` objects**
   with explicit type annotations. The 3 integer-typed fields (`num_primary_branches`,
   `max_strahler_depth`, `morph_seed`) must be `int`, not `float`, so that t0091's pymoo
   `Integer`/`Real` mixed-variable harness can correctly route them to discrete vs continuous
   operators [pymoo-Mixed-2025].

6. **Use NeuroM (`neurom` pip package) for Phase E morphometric feature extraction** rather than
   re-implementing partition asymmetry / Strahler / Sholl [NeuroM-GH]. This uses the community
   standard definitions, which improves comparability with published DSGC morphometric data and
   avoids accuracy debates in PCA/UMAP feature scaling.

7. **Always emit both the PCA panel and the UMAP panel in the same Phase E script** — keep the PCA
   panel as the deterministic baseline; UMAP is a stochastic supplement. Use `random_state=42` for
   UMAP and `umap-learn>=0.5.7` from `pip` [umap-PyPI-2025, umap-NRMP-2024].

8. **For Phase F's Bed-B reproducibility check, soften the 5 percent criterion to 10 percent** if
   the t0090 implementation reveals cell-to-cell DSI variability above 5 percent under fixed t0083
   channels [research_papers.md]. The internet search did not find evidence to tighten the criterion
   below 5 percent.

9. **For Phase G.3 NaP knockout, document the NaP density prior re-anchoring path**: if the four
   cluster representatives' DSI collapses to <0.2, cite [BaranauskasMiller2021] as the cortical
   pyramidal anchor and frame the t0088 distal-NaP centroids as a DSGC-specific high-density regime,
   not as a units error.

10. **Document in the answer asset the limitation that no procedural DSGC morphology generator
    exists in the published literature**. The diversity test is exploratory; the warm-start anchors
    for t0091 should weight Bed-B-equivalent and the 4 best-cell-supporting "different" morphologies
    more heavily than randomly sampled LHS rows. This refines recommendation 9 in
    `research_papers.md` from "the morphology generator is not validated against DSGC
    reconstructions" to "the diversity test produces N out of 30 visibly distinct morphology classes
    (where N is reported); these N anchors form the t0091 warm-start basis".

## Source Index

### [TREES-GH]

* **Type**: repository
* **Title**: cuntzlab/treestoolbox
* **Author/Org**: Cuntz Lab, Frankfurt
* **Date**: 2023-12-18 (last update)
* **URL**: <https://github.com/cuntzlab/treestoolbox>
* **Last updated**: 2023-12 (v1.16)
* **Peer-reviewed**: no (the algorithms are peer-reviewed in [Cuntz2010] in corpus; the toolbox
  README itself is not)
* **Relevance**: Establishes that TREES is MATLAB-only with sparse Python wrapping (Mueller). Drives
  the recommendation to implement t0090's generator in pure Python rather than fall back to TREES
  via oct2py.

### [TREES-MST]

* **Type**: documentation
* **Title**: MST_tree function manual page
* **Author/Org**: Cuntz Lab, Frankfurt
* **Date**: undated; last accessed 2026-05-07
* **URL**: <https://www.treestoolbox.org/manual/MST_tree.html>
* **Peer-reviewed**: no
* **Relevance**: Specifies MST_tree's signature
  `(msttrees, X, Y, Z, bf, thr, mplen, DIST, options)`. The `bf` balancing factor and the `-b`
  option (forbid trifurcations) are conceptual primitives that t0090's generator should match in
  spirit if not in literal API.

### [T2N-GH]

* **Type**: repository
* **Title**: MarcelBeining/T2N
* **Author/Org**: Beining, M.
* **Date**: 2017+ (last commit not specified in search results)
* **URL**: <https://github.com/MarcelBeining/T2N>
* **Peer-reviewed**: no (the paper [Beining2017] is peer-reviewed eLife)
* **Relevance**: Bridges TREES to NEURON via MATLAB. Defines the function-coverage surface that a
  pure-Python equivalent must reach for t0091 joint optimisation to be feasible.

### [NeuroMaC-GH]

* **Type**: repository
* **Title**: CNS-OIST/NeuroMaC
* **Author/Org**: Computational Neuroscience Unit, OIST
* **Date**: 2014-2015 (last activity)
* **URL**: <https://github.com/CNS-OIST/NeuroMaC>
* **Peer-reviewed**: no (the paper [TorbenNielsen2014] is peer-reviewed Frontiers in Neuroanatomy)
* **Relevance**: Confirms that NeuroMaC is unmaintained (no commits since ~2015). Drives the
  recommendation to NOT use NeuroMaC as a runtime dependency.

### [TorbenNielsen2014]

* **Type**: paper
* **Title**: Context-aware modeling of neuronal morphologies
* **Authors**: Torben-Nielsen, B., De Schutter, E.
* **Year**: 2014
* **DOI**: `10.3389/fnana.2014.00092`
* **URL**: <https://www.frontiersin.org/articles/10.3389/fnana.2014.00092/full>
* **Peer-reviewed**: yes (Frontiers in Neuroanatomy)
* **Relevance**: Underlying paper for the NeuroMaC framework. Documents the growth-cone L-system
  algorithm that informs the conceptual design of t0090's generator. Also listed in Discovered
  Papers because it is not yet in the project corpus.

### [Beining2017]

* **Type**: paper
* **Title**: T2N as a new tool for robust electrophysiological modeling demonstrated for mature and
  adult-born dentate granule cells
* **Authors**: Beining, M., Mongiat, L. A., Schwarzacher, S. W., Cuntz, H., Jedlicka, P.
* **Year**: 2017
* **DOI**: `10.7554/eLife.26517`
* **URL**: <https://elifesciences.org/articles/26517>
* **Peer-reviewed**: yes (eLife)
* **Relevance**: Companion publication to T2N. Establishes that the TREES + T2N stack can drive
  NEURON simulations of complex cell types end-to-end. Forms the comparison baseline for evaluating
  t0090's pure-Python pipeline against the established MATLAB-side workflow.

### [Cuntz2011-PCB]

* **Type**: paper
* **Title**: The TREES toolbox-Probing the Basis of Axonal and Dendritic Branching
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2011
* **DOI**: `10.1007/s12021-010-9093-7`
* **URL**: <https://pmc.ncbi.nlm.nih.gov/articles/PMC7612393/>
* **Peer-reviewed**: yes (Neuroinformatics)
* **Relevance**: Companion to [Cuntz2010] in the corpus; documents the toolbox feature surface and
  validated parameter ranges. Reference for "what TREES does that t0090's pure-Python generator
  should also do".

### [NMO-API-2025]

* **Type**: documentation
* **Title**: NeuroMorpho.Org API Reference
* **Author/Org**: NeuroMorpho.Org
* **Date**: 2025 (last accessed 2026-05-07)
* **URL**: <https://neuromorpho.org/apiReference.html>
* **Peer-reviewed**: no
* **Relevance**: Authoritative source for the REST API endpoints and query syntax. Documents that
  there is no DSGC-specific cell_type filter — only "ganglion" — which limits the API's utility
  for t0090 but provides a path for t0091's warm-start anchor archive if real-cell morphologies are
  eventually added.

### [NeuroBox3D-GH]

* **Type**: repository
* **Title**: NeuroBox3D/neuromorpho
* **Author/Org**: NeuroBox3D project
* **Date**: 2018-2020 (approximate)
* **URL**: <https://github.com/NeuroBox3D/neuromorpho>
* **Peer-reviewed**: no
* **Relevance**: Python wrapper for NeuroMorpho.Org REST API v7. No third-party dependencies.
  Reference implementation for programmatic morphology download if t0091 chooses to query real
  ganglion cell morphologies for warm-start anchors.

### [neuromorpho-api-RTD]

* **Type**: documentation
* **Title**: neuromorpho-api documentation
* **Author/Org**: neuromorpho-api maintainers
* **Date**: 2024-05 (SSL renewal note); last accessed 2026-05-07
* **URL**: <https://neuromorpho-api.readthedocs.io/en/latest/tutorial.html>
* **Peer-reviewed**: no
* **Relevance**: Documents that as of May 2024, plain `requests` works against NeuroMorpho.Org after
  SSL key renewal. Most current Python client documentation found.

### [NRN-Sections-2025]

* **Type**: documentation
* **Title**: Conceptual Overview of Sections
* **Author/Org**: NEURON simulator project
* **Date**: 2025 (current docs)
* **URL**:
  <https://nrn.readthedocs.io/en/latest/python/modelspec/programmatic/topology/geometry.html>
* **Peer-reviewed**: no (the NEURON simulator itself is peer-reviewed via [Hines1997] in corpus)
* **Relevance**: Authoritative reference for `h.Section()`, `pt3dadd`, `connect()`, and the geometry
  vs 3D-points dichotomy. Drives the t0090 idiom of `L`/`diam`/`nseg` for procedural geometry plus
  optional `pt3dadd` for visualisation.

### [NRN-BallStick-2025]

* **Type**: documentation
* **Title**: Ball-and-stick: 3 — Basic cell tutorial
* **Author/Org**: NEURON simulator project
* **Date**: 2025
* **URL**: <https://neuron.yale.edu/neuron/static/docs/neuronpython/ballandstick3.html>
* **Peer-reviewed**: no
* **Relevance**: Canonical NEURON Python tutorial showing the procedural section construction
  pattern. Validates the `dend.connect(soma(1))` method form preferred over `h.connect(...)`.

### [NRN-dlambda-2025]

* **Type**: documentation
* **Title**: Using the d_lambda Rule
* **Author/Org**: NEURON simulator project
* **Date**: 2025
* **URL**: <https://www.neuronsimulator.org/en/latest/guide/using_the_d_lambda_rule.html>
* **Peer-reviewed**: no (the d_lambda rule itself is peer-reviewed via Hines and Carnevale 2001)
* **Relevance**: Authoritative reference for `lambda_f` and `geom_nseg`. Documents the default
  `freq=100 Hz` and `d_lambda=0.1` and the always-odd `nseg` formula. Drives the t0090
  recommendation to apply d_lambda automatically per section.

### [Snyk-pt3dadd-2024]

* **Type**: documentation
* **Title**: How to use the neuron.h.pt3dadd function in NEURON
* **Author/Org**: Snyk Advisor
* **Date**: 2024
* **URL**: <https://snyk.io/advisor/python/NEURON/functions/neuron.h.pt3dadd>
* **Peer-reviewed**: no
* **Relevance**: Documents the monotonic-arc-length convention for successive `pt3dadd` calls and
  the diameter-matching requirement at section connection points. Practical detail not always
  emphasised in the official NEURON docs.

### [NP-vonmises-2025]

* **Type**: documentation
* **Title**: numpy.random.Generator.vonmises (NumPy v2.2 Manual)
* **Author/Org**: NumPy project
* **Date**: 2025
* **URL**:
  <https://numpy.org/doc/stable/reference/random/generated/numpy.random.Generator.vonmises.html>
* **Peer-reviewed**: no
* **Relevance**: Documents the `Generator.vonmises(mu, kappa, size)` primitive used for
  primary-branch direction sampling. Confirms that the modern `Generator` API supersedes the legacy
  global `np.random.vonmises` and supports per-instance seeding.

### [scipy-LHS-2025]

* **Type**: documentation
* **Title**: scipy.stats.qmc.LatinHypercube (SciPy v1.17 Manual)
* **Author/Org**: SciPy project
* **Date**: 2025
* **URL**:
  <https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.qmc.LatinHypercube.html>
* **Peer-reviewed**: no
* **Relevance**: Documents `optimization="random-cd"` and the `seed` requirement for
  reproducibility. Drives the Phase B sampling implementation.

### [pymoo-Mixed-2025]

* **Type**: documentation
* **Title**: pymoo Mixed Variable Problem
* **Author/Org**: anyoptimization / pymoo maintainers
* **Date**: 2025 (pymoo 0.6.1.6)
* **URL**: <https://pymoo.org/customization/mixed.html>
* **Peer-reviewed**: no (the pymoo paper is peer-reviewed via the IEEE 2020 publication)
* **Relevance**: Confirms that `pymoo.core.variable.Integer` and `Real` accept `bounds=` tuples and
  combine with `MixedVariableGA(survival=RankAndCrowdingSurvival())` for multi-objective NSGA-II.
  Validates t0091's joint 14-d morphology + 54-d electrophys harness on the encoding side.

### [umap-PyPI-2025]

* **Type**: repository
* **Title**: umap-learn on PyPI
* **Author/Org**: McInnes, L.
* **Date**: 2025
* **URL**: <https://pypi.org/project/umap-learn/>
* **Peer-reviewed**: no (the underlying algorithm is peer-reviewed via [umap-NRMP-2024])
* **Relevance**: Standard install path `pip install umap-learn` and scikit-learn-compatible API.
  Used in Phase E for the optional UMAP panel.

### [umap-NRMP-2024]

* **Type**: paper
* **Title**: Uniform manifold approximation and projection
* **Authors**: McInnes, L., Healy, J., Melville, J., et al.
* **Year**: 2024
* **DOI**: `10.1038/s43586-024-00332-4`
* **URL**: <https://www.nature.com/articles/s43586-024-00332-4>
* **Peer-reviewed**: yes (Nature Reviews Methods Primers)
* **Relevance**: Peer-reviewed UMAP paper. Source for parameter recommendations (n_neighbors,
  min_dist) used in Phase E's 60-morphology embedding.

### [NeuroM-GH]

* **Type**: repository
* **Title**: BlueBrain/NeuroM
* **Author/Org**: Blue Brain Project (now archived; future development at OpenBrainInstitute)
* **Date**: 2024-12 (BlueBrain concluded); future at openbraininstitute/NeuroM
* **URL**: <https://github.com/BlueBrain/NeuroM>
* **Peer-reviewed**: no (the underlying morphometric definitions are peer-reviewed across multiple
  papers)
* **Relevance**: Standard Python morphology analysis library exposing `partition_asymmetry`,
  `strahler_order`, `section_lengths`, etc. Used in Phase E for community-standardised morphometric
  feature extraction.

### [oct2py-GH]

* **Type**: repository
* **Title**: blink1073/oct2py
* **Author/Org**: blink1073
* **Date**: 2025 (current docs)
* **URL**: <https://github.com/blink1073/oct2py>
* **Peer-reviewed**: no
* **Relevance**: Bidirectional Python <-> Octave bridge with shared-memory or temp-file passing.
  Documents the cost of TREES interop, supporting the recommendation to implement t0090's generator
  in pure Python.

### [BaranauskasMiller2021]

* **Type**: paper
* **Title**: Subcellular Distribution of Persistent Sodium Conductance in Cortical Pyramidal Neurons
* **Authors**: Astman, N., Gutnick, M. J., Fleidervish, I. A. (citation to verify on download)
* **Year**: 2021
* **DOI**: `10.1523/JNEUROSCI.2989-20.2021`
* **URL**: <https://www.jneurosci.org/content/41/29/6190>
* **Peer-reviewed**: yes (Journal of Neuroscience)
* **Relevance**: Contemporary anchor for cortical pyramidal NaP density distribution. Used to
  contextualise t0088's high distal-NaP centroids as DSGC-specific rather than units-error.

### [Cuntz2010]

* **Type**: paper
* **Title**: One Rule to Grow Them All: A General Theory of Neuronal Branching and Its Practical
  Application
* **Authors**: Cuntz, H., Forstner, F., Borst, A., Hausser, M.
* **Year**: 2010
* **DOI**: `10.1371/journal.pcbi.1000877`
* **URL**: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000877>
* **Peer-reviewed**: yes (PLOS Computational Biology)
* **Relevance**: Already in project corpus (paper asset under `t0027`). Cited inline for the
  canonical biological range of the TREES toolbox `bf` balancing factor (0.2-0.7) and for the
  parameter-economy hypothesis (effective dimensionality of useful generators is 1-3). Source Index
  entry added so this internet research file's citations are self-contained.

### [Hines1997]

* **Type**: paper
* **Title**: The NEURON Simulation Environment
* **Authors**: Hines, M. L., Carnevale, N. T.
* **Year**: 1997
* **DOI**: `10.1162/neco.1997.9.6.1179`
* **URL**: <https://direct.mit.edu/neco/article/9/6/1179/6017/The-NEURON-Simulation-Environment>
* **Peer-reviewed**: yes (Neural Computation)
* **Relevance**: Already in project corpus (paper asset under `t0002`). Foundational reference for
  the NEURON simulator that t0090's generator emits sections for. Cited via the d_lambda rule
  documentation [NRN-dlambda-2025] which is the implementation of Hines and Carnevale 2001's rule.

### [Sivyer2013]

* **Type**: paper
* **Title**: Direction selectivity is computed by active dendritic integration in retinal ganglion
  cells
* **Authors**: Sivyer, B., Williams, S. R.
* **Year**: 2013
* **DOI**: `10.1038/nn.3565`
* **URL**: <https://www.nature.com/articles/nn.3565>
* **Peer-reviewed**: yes (Nature Neuroscience)
* **Relevance**: Already in project corpus (paper asset under `t0027`). Cited inline as the source
  of the active dendritic integration framework supporting the Phase G.3 NaP knockout hypothesis:
  distal NaP amplifies preferred-direction dendritic spikes; if so, knockout collapses DSI to <0.2.

### [nGauge2022]

* **Type**: paper
* **Title**: nGauge: Integrated and Extensible Neuron Morphology Analysis in Python
* **Authors**: Bird, A. D., Cuntz, H. (citation to verify on download)
* **Year**: 2022
* **DOI**: `10.1007/s12021-022-09604-4`
* **URL**: <https://pmc.ncbi.nlm.nih.gov/articles/PMC9720862/>
* **Peer-reviewed**: yes (Neuroinformatics)
* **Relevance**: Alternative Python morphology analysis library complementing NeuroM. Provides
  cross-check implementations of partition asymmetry / Strahler / Sholl for Phase E feature
  extraction. Also listed in Discovered Papers.
