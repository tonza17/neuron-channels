---
spec_version: "3"
paper_id: "10.1098_rsob.220073"
citation_key: "Jedlicka2022"
summarized_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"
date_summarized: "2026-05-25"
---

# Pareto Optimality, Economy-Effectiveness Trade-offs and Ion Channel Degeneracy

## Metadata

* **File**: `files/jedlicka_2022_pareto-optimality-ion-channels.pdf`
* **Published**: 2022
* **Authors**: Peter Jedlicka 🇩🇪, Alexander D. Bird 🇩🇪, Hermann Cuntz 🇩🇪
* **Venue**: Open Biology (Royal Society)
* **DOI**: `10.1098/rsob.220073`

## Abstract

Neurons encounter unavoidable evolutionary trade-offs between multiple tasks. They must consume as
little energy as possible while effectively fulfilling their functions. Cells displaying the best
performance for such multi-task trade-offs are said to be Pareto optimal, with their ion channel
configurations underpinning their functionality. Ion channel degeneracy, however, implies that
multiple ion channel configurations can lead to functionally similar behaviour. Therefore, instead
of a single model, neuroscientists often use populations of models with distinct combinations of
ionic conductances. This approach is called population (database or ensemble) modelling. It remains
unclear, which ion channel parameters in the vast population of functional models are more likely to
be found in the brain. Here we argue that Pareto optimality can serve as a guiding principle for
addressing this issue by helping to identify the subpopulations of conductance-based models that
perform best for the trade-off between economy and functionality. In this way, the high-dimensional
parameter space of neuronal models might be reduced to geometrically simple low-dimensional
manifolds, potentially explaining experimentally observed ion channel correlations. Conversely,
Pareto inference might also help deduce neuronal functions from high-dimensional Patch-seq data. In
summary, Pareto optimality is a promising framework for improving population modelling of neurons
and their circuits.

## Overview

This is a methodological review article that argues for using Pareto optimality as a guiding
principle to constrain the parameter space of conductance-based neuron population models. The
problem the authors target is well known: landmark studies by Prinz, Bucher and Marder (2003, 2004)
showed that disparate ion channel configurations can yield indistinguishable voltage traces ("ion
channel degeneracy"). Population (or database/ensemble) modelling generates many valid
configurations, but it is unclear which of these the brain actually selects.

The authors propose that evolution selects, among the many functionally equivalent configurations,
the subset that is **Pareto optimal** for a trade-off between **functional effectiveness** (e.g.
dendritic computation, coincidence detection, sparse firing) and **energy economy** (typically ATP
consumption per second). They review the geometric theory of Pareto fronts due to Shoval and Alon
(systems-biology school), which predicts that for n competing tasks the Pareto-optimal phenotypes
fall on an (n-1)-dimensional polytope in parameter space (line for two tasks, triangle for three,
tetrahedron for four), with archetypes at the vertices.

The paper then surveys the few studies that have explicitly or implicitly applied this idea to
conductance-based neuron models. The headline example is Remme, Rinzel and Schreiber (2018) on
medial superior olive (MSO) neurons, which showed that the experimentally constrained MSO model lies
close to the Pareto front for the coincidence-detection vs ATP-cost trade-off. Other discussed
examples are Bast and Oberlaender (2021) on L5 pyramidal cells (dendritic computation vs energy)
and Deistler, Macke and Goncalves (2022) on the stomatogastric circuit (energy efficiency vs
temperature robustness).

A second major thread is **Pareto Task Inference (ParTI)**, due to Shoval et al. (2012) and Hart et
al. (2015). The authors argue that ParTI applied to Patch-seq datasets (which combine ion channel
expression, electrophysiology and morphology) could deduce neuronal functions from the geometric
shape of the data cloud, without needing to specify the tasks in advance. The paper does not
present new experiments or simulations -- it is a conceptual and methodological review.

## Architecture, Models and Methods

This is a theoretical/review paper, so the "methodology" is the **Pareto-optimality framework**
itself, formalized as follows. Given a population of conductance-based neuron models indexed by
parameters p in n-dimensional parameter space, and a vector of task performances f(p) in
m-dimensional performance space, a model p* is Pareto optimal if no other p in the population
strictly dominates it on every task. The set of Pareto-optimal models is the **Pareto front**.

The theoretical results the authors emphasize, drawn from Shoval et al. (Science 2012) and Alon
2020 book, are:

* For **m = 2 tasks**, the Pareto front in parameter space is a **line segment** between two
  archetypes -- independently of the dimension n of parameter space.
* For **m = 3 tasks**, the Pareto front is a **triangle** with three archetype vertices.
* For **m = n tasks**, the Pareto front is an (m-1)-dimensional polytope with m vertices.

These theorems assume that performance decays monotonically with metric distance from each task
archetype, with one global peak per task and a common distance metric. When these conditions are
relaxed, the Pareto fronts become mildly curved rather than straight but still terminate at
archetypes.

For energy estimation in conductance-based models, the authors endorse the standard
**current-counting ATP accounting** introduced by Attwell and Laughlin (2001) and refined by
Hasenstaub et al. and Remme et al. The ionic current through each channel is integrated over time
and converted to ATP via the stoichiometry of the Na+/K+ pump (3 Na+ extruded and 2 K+ imported per
ATP) and the Ca2+-ATPase. The authors highlight that this is computationally cheap and can be added
as an additional objective to any existing multi-objective fitting framework such as Druckmann et
al. (2007) feature-based BluePyOpt-style optimization.

The third methodological pillar is **Pareto Task Inference (ParTI)**: given a high-dimensional
dataset, fit polytopes (lines, triangles, tetrahedra) using algorithms such as PCHA, identify the
vertices, and interpret each vertex as a task archetype. The authors argue that PCA-then-ParTI can
work for Patch-seq data, although they caution that PCA projection can mask archetypes if true
high-dimensional polytopes are projected onto lower-dimensional spaces. They cite a phylogeny-aware
extension of ParTI as a remedy for biological data violating the ParTI independence assumption.

Hardware and compute requirements are not reported because no new simulations are performed.

## Results

This is a review paper with no original simulations or measurements, but the authors summarize and
synthesize the following quantitative claims from the cited literature:

* The Pareto front in parameter space for **2 tasks** is a 1-dimensional line segment irrespective
  of how many ion channel parameters are varied (theorem from Shoval et al. 2012).
* For **n tasks**, the Pareto front is an (**n - 1**)-dimensional polytope with **n** vertices.
* MSO neurons in Remme et al. (2018) lie close to the Pareto front for the trade-off between
  coincidence detection and ATP cost, with the default biophysically-constrained model close to the
  front; their energy axis is shown as energy cost in units of **10^9 ATP/s** per cell (default of
  **6.2 x 10^9 ATP/s**).
* Bast and Oberlaender (2021) L5 PC population models showed that energy-efficient dendritic
  computation correlated with **low Kv3.1** (fast non-inactivating K+) channel density and **low
  high-voltage-activated Ca2+** channel density in the dendritic hot zone.
* Deistler, Macke and Goncalves (2022) found that imposing energy efficiency on the stomatogastric
  ganglion network reduced parameter space but did not collapse degeneracy; sodium and calcium
  conductances were predicted to be **less variable** than network-fitness-only models would imply.
* The energy budget of the brain consumes **~20% of resting metabolic rate** in humans despite
  being ~2% of body mass (cited from Attwell and Laughlin 2001).
* The paper reports **no new F1, accuracy, or other ML metrics** -- it presents no original
  experimental data.

## Innovations

### Reframing Population Modelling as Multi-task Optimization with Energy as an Explicit Objective

The paper central conceptual contribution is to argue that population (database/ensemble) models of
neurons should include **ATP cost as a first-class objective alongside voltage-trace features**.
Existing population-modelling pipelines (e.g. Druckmann BluePyOpt) optimize for
electrophysiological features only; the authors propose extending them to function-economy
trade-offs and using Pareto-front position to select biologically plausible parameter sets.

### Geometric Reduction of High-d Conductance Space to Low-d Manifolds

The authors transplant the Shoval-Alon theorems (originally developed for life-history and gene
expression) into the conductance-based-modelling literature. The novel claim is that ion channel
degeneracy in n-dimensional conductance space should collapse to an (m-1)-dimensional polytope when
m << n tasks are simultaneously optimized. This is offered as a **prediction** explaining the ion
channel correlations observed experimentally by Schulz et al., Goaillard et al. and others.

### Pareto Inference for Patch-Seq Data

A second methodological innovation is to extend ParTI to neuronal Patch-seq data, which combines
transcriptomics, electrophysiology and morphology. The vertices in the resulting polytope would
correspond to functional archetypes (e.g. fast-spiking vs energy-saving), potentially **deducing
neuronal computations directly from high-dimensional expression data**.

### Distinguishing Parameter-Space and Performance-Space Pareto Fronts

The paper carefully distinguishes the geometry of the Pareto front in performance space (where
shape is dataset-specific) from parameter space (where shape is the universal (n-1)-polytope). This
distinction has been muddled in earlier trade-off literature; the authors clarify it with worked
figures.

## Datasets

This is a theoretical review paper; no datasets were used. The cited empirical examples reference
the following pre-existing datasets, none of which are produced by this paper:

* Remme et al. (2018) MSO compartmental model simulations.
* Bast and Oberlaender (2021) L5 PC population model database.
* Deistler, Macke and Goncalves (2022) stomatogastric ganglion population models.
* Patch-seq datasets from the Allen Brain Atlas (cited as the target for future ParTI analyses).
* Shoval et al. (2012) and Hart et al. (2015) ParTI test datasets (cancer cells, liver cells, fly
  morphology) -- used in figures but not re-analyzed.

## Main Ideas

* **Pareto-front position is the right way to read NSGA-II outputs** for the t0124 DSI-vs-ATP-cost
  optimization. Solutions on the front represent biologically plausible trade-offs; solutions far
  from the front are likely evolutionarily disfavoured even if they pass DSI thresholds. This
  directly grounds the t0124 task hypothesis that DSI and ATP cost are competing objectives that
  evolution balances.
* **Report the population of parameter combinations** that achieve points on the front, not just
  the front itself. The authors stress that ion channel degeneracy means the same Pareto-optimal
  performance point can correspond to many parameter combinations -- for t0124, this means
  reporting the 68-d parameter cloud that achieves each front position is more informative than
  reporting only the (DSI, ATP) pairs.
* **Two-task Pareto fronts are 1-d line segments in parameter space regardless of n**. For t0124
  with 68 free parameters and 2 objectives (DSI and ATP per spike), the geometric prediction is
  that the Pareto-optimal parameter cloud should collapse to a curve through the 68-d parameter
  space. Testing whether the NSGA-II Pareto-front parameter sets actually lie close to such a 1-d
  manifold (e.g. by PCA) is a direct test of the Jedlicka hypothesis on our model.
* **Ion channel correlations on the Pareto front are predicted to emerge naturally**. If the t0124
  Pareto front has shape consistent with the Jedlicka polytope theorem, then specific pairs of
  conductances (e.g. Kv3.1 vs Ca-HVA) should be correlated across the front -- and these
  correlations can be compared against experimentally observed correlations in DSGC patch-clamp
  data.
* **Add ATP cost as a first-class objective**, not a post-hoc filter. The Bast and Oberlaender
  workflow filtered population models for energy efficiency after voltage-feature optimization;
  Jedlicka argues that direct multi-objective optimization (which t0124 already does via NSGA-II)
  is conceptually cleaner.

## Summary

The paper, by Jedlicka, Bird and Cuntz (Open Biology 2022), is a methodological review that argues
for adopting **Pareto optimality** as a unifying framework for constraining the high-dimensional
parameter space of conductance-based neuron population models. The motivation is the well-known
problem of **ion channel degeneracy**: many disparate combinations of ionic conductances yield
indistinguishable voltage traces, leaving population-modelling pipelines with a vast space of valid
but biologically implausible candidates. The research question is whether evolution selects, among
the degenerate solutions, the subset that is Pareto optimal for a trade-off between functional
effectiveness and energy economy.

Methodologically the paper has no new simulations -- it synthesizes (1) the Shoval-Alon theorems
from systems biology, which predict that Pareto fronts in n-d parameter space collapse to
(m-1)-dimensional polytopes with m vertices when m tasks are jointly optimized, (2) the standard
**current-counting ATP-accounting** approach for conductance-based models due to Attwell-Laughlin
and refined by Remme et al., and (3) the **Pareto Task Inference (ParTI)** algorithm of Shoval-Hart
for inferring tasks from data. The authors then walk through three case studies from the
literature (MSO coincidence detection, L5 PC dendritic computation, stomatogastric ganglion) where
Pareto-style analysis has either been done explicitly or could be done.

The headline findings are conceptual rather than quantitative: the geometric theorems imply that
Pareto-optimal subsets of n-d conductance spaces should be **(m-1)-d manifolds**, naturally
explaining experimentally observed ion channel correlations. The MSO example shows that an
experimentally constrained model sits on the Pareto front for the coincidence-detection vs ATP-cost
trade-off; the L5 PC example links low Kv3.1 and Ca-HVA expression in the dendritic hot zone to
joint efficiency in energy and computation. Pareto Task Inference applied to Patch-seq data is
proposed as a way to deduce functional archetypes without specifying tasks a priori.

For this project, and specifically for task t0124 (DSI vs ATP per spike NSGA-II on a 68-d DSGC),
the paper provides direct theoretical grounding. It justifies reporting the NSGA-II Pareto front as
a biologically meaningful low-d manifold (predicted to be a 1-d curve through 68-d space for two
objectives), motivates testing whether parameter sets on the front exhibit predictable conductance
correlations, and supports the project use of degeneracy as an explanatory hypothesis (multiple
68-d parameter sets yield equivalent DSI but vary in ATP cost). The framework also suggests
follow-up tasks: PCA of the Pareto front to test the 1-d-manifold prediction, and ParTI on the
population of valid DSGC models to infer whether DSI and ATP cost are the only relevant tasks or
whether additional latent objectives (e.g. robustness) are needed.
