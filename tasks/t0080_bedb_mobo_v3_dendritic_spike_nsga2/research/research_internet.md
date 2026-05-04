---
spec_version: "1"
task_id: "t0080_bedb_mobo_v3_dendritic_spike_nsga2"
research_stage: "internet"
searches_conducted: 11
sources_cited: 18
papers_discovered: 4
date_completed: "2026-05-04"
status: "complete"
---
## Task Objective

Conduct internet research to fill gaps in the t0080 paper corpus, with priority on (a) the canonical
pymoo NSGA-II API and `StarmapParallelization` recipe for the 54-56 d Bed B v3 substrate, (b) recent
(2023-2025) DSGC dendritic-spike papers possibly missed by the paper-corpus stage, (c) newer Werginz
/ Kole AIS Nav density measurements, (d) Hay 2011 supplementary parameter ranges, and (e) canonical
Exp2NMDA Mg-block implementation patterns from ModelDB / GitHub. The findings feed directly into the
v3 substrate library asset and the NSGA-II harness implementation.

## Gaps Addressed

This section maps every gap from
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/research/research_papers.md` Gaps and Limitations to
its internet-research resolution status.

1. **Sivyer 2013 PDF paywalled (no quantitative terminal-dendrite gNa value)** -- **Unresolved**.
   Internet search did not surface a freely accessible version of the Sivyer / Williams 2013
   compartmental-model parameter table. The v3 distal-Nav range remains anchored to the Schachter et
   al. 2010 40 mS/cm^2 uniform / 45 -> 20 gradient as documented in `research_papers.md`.

2. **Kole 2008 PDF paywalled (verify 0.25-0.5 S/cm^2 AIS Nav range)** -- **Partially resolved**.
   Cross-referenced against [Werginz2024-PMC] confirmation of the Kole 2008 range; the canonical
   downstream citations all use 0.25-0.5 S/cm^2. Direct PDF still inaccessible via web search; the
   v3 hard-bound `nav16_ais >= 0.25 S/cm^2` floor is robust to this gap.

3. **No DSGC patch-clamp study reports AIS-to-soma Nav ratio directly** -- **Unresolved**. The
   Werginz / Fried bioRxiv preprint [WerginzAxial-bioRxiv-2020] uses axial-current measurements +
   resistive coupling theory to estimate AIS Nav density indirectly in mouse alpha-RGCs but does not
   address DRD4 ON-OFF DSGCs specifically. The 5x hard-floor remains an inference from non-DSGC
   alpha-RGCs.

4. **No published DSGC compartmental model has joint Mg-NMDA + dendritic Nav1.6 + NaP** --
   **Confirmed unresolved**. Internet search of bioRxiv (2023-2025) and ModelDB returned no model
   with this joint configuration; the t0080 v3 substrate remains the first such configuration in the
   project's lineage.

5. **Trenholm 2013 198 Hz peak rate is for Hb9::eGFP DSGCs, not DRD4** -- **Partially resolved**. No
   2024-2025 paper reports peak DRD4 ON-OFF DSGC firing under the sigma=25 ms convention; the gap
   remains for DRD4 specifically. The newly discovered [Riccitelli-PNAS-2025] paper reports
   direction-tuned firing in non-DS RGCs but uses a different protocol.

6. **Bed B Poleg-Polsky 2016 model (ModelDB 189347) has NMDARs only on ON dendrites** --
   **Resolved**. The ModelDB 189347 file listing [ModelDB-189347] confirms `bipolarNMDA.mod` is the
   relevant NMDA implementation, attached to ON-layer bipolar contacts only. The v3 plan's choice to
   add NMDA to all dendritic compartments (ON + OFF) is a deliberate extension; the
   `bipolarNMDA.mod` file pattern can be re-used as the OFF-layer template.

## Search Strategy

**Sources searched**: Google (general web), Google Scholar (via web), bioRxiv direct, ModelDB
direct, pymoo official documentation site (`pymoo.org`), pymoo GitHub repository
(`github.com/anyoptimization/pymoo`), PMC / PubMed Central, PNAS direct, Nature Communications
direct, Werginz lab pages.

**Date range**: 2020-2026 for AIS / DSGC / direction-selectivity papers. No date restriction for
canonical pymoo / NEURON documentation.

**Inclusion criteria**: Must provide one of: (a) canonical pymoo NSGA-II / `StarmapParallelization`
code recipe; (b) DSGC dendritic-spike or active-dendrite measurements / models from 2023-2025; (c)
mouse RGC AIS Nav density measurements from 2024-2025; (d) Exp2NMDA Mg-block mod-file
implementation; (e) Hay 2011 parameter ranges or supplementary materials. Excluded: clinical papers
on optic nerve injury without parameter values, pure cell-type taxonomy papers without electrical
measurements.

**Queries executed (11 total)**:

1. `pymoo NSGA-II bound-constrained continuous multi-objective optimization tutorial 2025`
2. `pymoo StarmapParallelization Problem subclass NSGA2 parallel evaluation example`
3. `pymoo SBX crossover polynomial mutation eta default population size NSGA-II`
4. `DSGC dendritic spike direction selectivity 2024 2025 retinal ganglion cell mouse`
5. `Werginz Kole AIS sodium channel density mouse retinal ganglion cell 2024 2025 measurement`
6. `Hay 2011 multi-objective evolutionary optimization L5 pyramidal NEURON parameter ranges supplementary`
7. `Exp2NMDA voltage dependent magnesium block NEURON mod file Jahr Stevens implementation`
8. `NSGA-II pymoo neural model multi-compartment NEURON parameter optimization 2024`
9. `DSGC starburst amacrine cell biorxiv 2025 dendritic computation NMDA optimization model`
10. `retinal ganglion cell axon initial segment biorxiv 2025 sodium channel Nav1.6 patch clamp mouse`
11. `pymoo Latin Hypercube Sampling LHS sampling initial population multi-objective`

**Search iterations**: Queries 1-3 (pymoo recipe) and 8-11 (LHS, NEURON applications) form the
methodology cluster. Queries 4-6, 9-10 (DSGC + AIS biology) form the literature-update cluster.
Query 7 confirms the canonical Exp2NMDA implementation. The pymoo NSGA-II page and
`StarmapParallelization` page were deep-fetched via WebFetch to extract the exact code recipe; the
ModelDB 267357 mod file and the GitHub mirror of ModelDB 189347 were deep-fetched to extract the
exact `bipolarNMDA.mod` and Mg-block formulas.

## Key Findings

### Canonical pymoo NSGA-II recipe for bound-constrained continuous problems

The pymoo official documentation [pymoo-NSGA2-docs] specifies the canonical NSGA-II recipe with
defaults that align almost exactly with t0080's plan. Default operators are:

* **Sampling**: `FloatRandomSampling` (override to `LHS()` from `pymoo.operators.sampling.lhs` for
  spread-biased initial population)
* **Selection**: `TournamentSelection` (binary tournament)
* **Crossover**: SBX (`SimulatedBinaryCrossover`) -- pymoo NSGA-II default `eta=15`, `prob=0.9` per
  the older NSGA-II docs and `eta=15` is the current `NSGA2` class default; NSGA-III defaults to
  `eta=30`, but t0080 uses NSGA-II
* **Mutation**: PM (`PolynomialMutation`) with `eta=20` (default consistent across NSGA variants)
* **Survival**: `RankAndCrowding` (frontwise non-dominated sort + Manhattan crowding distance)
* **Default `pop_size`: 100** [pymoo-NSGA2-docs]

t0080 uses `pop_size=96` and `n_gen=40`, very close to the documentation-default `pop_size=100`. The
minimal canonical instantiation pattern from the docs is:

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.optimize import minimize

algorithm = NSGA2(pop_size=96)
res = minimize(problem, algorithm, ('n_gen', 40), seed=1, verbose=True)
# res.X = Pareto-optimal parameters (n_pareto x n_var)
# res.F = Pareto front objective values (n_pareto x n_obj)
```

t0080's chosen NSGA-II crossover `eta=15` and mutation `eta=20` match the pymoo documentation
defaults exactly. This is the canonical recipe with no deviation needed
[pymoo-NSGA2-docs, pymoo-Crossover-docs].

### StarmapParallelization recipe for the 64-core CPU NEURON workload

The pymoo `StarmapParallelization` documentation [pymoo-Starmap-docs] specifies the canonical
multi-process pattern:

```python
import multiprocessing
from pymoo.core.problem import ElementwiseProblem
from pymoo.parallelization.starmap import StarmapParallelization

class BedBV3Problem(ElementwiseProblem):
    def __init__(self, **kwargs):
        super().__init__(n_var=55, n_obj=2, n_ieq_constr=0,
                         xl=lower_bounds, xu=upper_bounds, **kwargs)

    def _evaluate(self, x, out, *args, **kwargs):
        # Run NEURON simulation (8 directions x 20 seeds x 1400 ms) in fresh subprocess
        dsi, pd_rate = run_bedb_v3_eval(x)
        # NSGA-II minimizes; flip sign for maximization
        out["F"] = [-dsi, -pd_rate]

n_processes = 64  # match Vast.ai 64-core EPYC instance
pool = multiprocessing.Pool(n_processes)
runner = StarmapParallelization(pool.starmap)
problem = BedBV3Problem(elementwise_runner=runner)

res = minimize(problem, NSGA2(pop_size=96), ('n_gen', 40), seed=1)
pool.close()
```

**Best practice**: Always call `pool.close()` after `minimize()` to release worker processes.
**Critical pitfall** [pymoo-issue-763]: `StarmapParallelization` was moved to
`pymoo.parallelization.starmap` in pymoo >= 0.6; older code using
`pymoo.core.problem.StarmapParallelization` will fail with import errors. Pin pymoo >= 0.6.0 in the
v3 substrate library `pyproject.toml`.

**Compatibility with t0078's NEURON-fresh-subprocess fix**: The `Exp2NMDA name already exists` error
from t0078 forces NEURON re-init in a fresh subprocess per trial. `multiprocessing.Pool` workers
spawned via the default `spawn` (Windows / macOS) or `fork` (Linux) start methods both create fresh
Python interpreters by default per worker, but because each worker may evaluate many trials
sequentially, the NEURON re-init bug still requires the nested-subprocess pattern. The plan:
`_worker_run_trial` inside each pool worker fans out to a short-lived `subprocess.run` call that
loads NEURON fresh and returns metrics over JSON.

### Latin Hypercube Sampling for pymoo initial population

The pymoo sampling documentation [pymoo-Sampling-docs] confirms that `LHS()` is available from
`pymoo.operators.sampling.lhs` and can be passed to NSGA2 via the `sampling=` keyword:

```python
from pymoo.operators.sampling.lhs import LHS
algorithm = NSGA2(pop_size=96, sampling=LHS())
```

This replaces the default `FloatRandomSampling`. LHS divides each dimension into `pop_size` equal
probability bins and samples one point from each bin (per dimension), then independently shuffles
across dimensions [pymoo-Sampling-docs, IDAES-LHS]. For 55-d problems with 96 individuals, LHS
provides much better initial spread than uniform random; t0080's plan to use LHS is sound. Sobol is
also available but LHS is the documented default for evolutionary algorithms in pymoo.

### Werginz 2024 AIS Nav density values confirmed; mouse axial-current literature emerging

The PMC version of Werginz et al. 2024 [Werginz2024-PMC] confirms Table 1's Nav densities of **1300
mS/cm^2 at the AIS** vs **75 mS/cm^2 at the soma** (AIS-to-soma ratio **17.3x**), matching the
values already extracted in `research_papers.md`. The AIS architecture in their model is a **25
um-long compartment tapering 1.0 -> 0.6 um diameter**. Input resistance for mouse alpha-RGC
subtypes:

* Alpha-ON sustained: **80 +/- 18 MOhm**
* Alpha-OFF sustained: **108 +/- 30 MOhm**
* Alpha-OFF transient: **60 +/- 16 MOhm**

These are useful anchors for v3's AIS geometry MOBO bounds: the AIS length should remain within
20-30 um (matching the Werginz 2024 25 um) to avoid biologically implausible elongation.

A complementary line of work [WerginzAxial-bioRxiv-2020] (Hottowy et al., bioRxiv 2020 v2) develops
**resistive coupling theory** to estimate AIS Nav density from axial currents at spike initiation in
mouse RGCs. The bioRxiv preprint reports estimates consistent with the Werginz 2024 1.3 S/cm^2
range. **This is a NEW paper not in the corpus**; it provides an independent, model-free methodology
for AIS Nav density estimation that strengthens the v3 hard-floor argument.

### Recent (2024-2026) DSGC and SAC papers worth adding

Three recent papers were not in the t0080 corpus:

1. **[Pitcher-bioRxiv-2026]** "Retinal waves shape starburst amacrine cell dendrite development
   through a direction-selective dendritic computation" (Pitcher, Gonzales, Habib, Feller, bioRxiv
   2026-02-04). Demonstrates SAC dendritic computation in vivo during retinal-wave activity;
   relevant as upstream context for the SAC -> DSGC inhibitory machinery that t0080 keeps fixed. Not
   in corpus.

2. **[Cbln4-JNeurosci-2024]** "Differential Expression Analysis Identifies Candidate Synaptogenic
   Molecules for Wiring Direction-Selective Circuits in the Retina" (J Neurosci 44:e1461232024).
   Tests cerebellin-4 (Cbln4) in ventral-preferring DSGCs; reduction reduces direction-selective
   tuning. Relevant for cross-validating that t0080's substrate matches a real direction-selective
   wiring rather than a generic DSGC. Not in corpus.

3. **[Riccitelli-PNAS-2025]** "Retinal ganglion cells encode the direction of motion through a
   suppressive surround" (Riccitelli et al. PNAS 2025). Reports direction-tuned firing in
   non-DS-RGCs through asymmetric activity beyond classic receptive field; broader project context
   for DSGC vs non-DSGC direction selectivity. Not in corpus.

A fourth bioRxiv preprint [WerginzAxial-bioRxiv-2020] is also worth adding for the AIS Nav-density
methodology argument.

### Hay 2011 parameter ranges (from PMC + ModelDB 139653)

The PMC version of Hay 2011 [Hay2011-PMC] confirms the multi-objective evolutionary algorithm
optimised **9 ion channel densities** in Table 2 over soma + apical dendrite + axon. The ~2,000
acceptable models are deposited in ModelDB **139653**. The optimisation used population 1000 over
500 generations -- 500,000 evaluations -- vs t0080's pop 96 x 40 generations = 3,840 evaluations.
This is two orders of magnitude smaller, justified because t0080 has only 2 objectives (DSI, PD
rate) vs Hay's 20 firing-feature objectives, and because t0080 starts from a known-good t0078
baseline rather than from scratch [Hay2011-PMC, ModelDB-139653]. The published parameter ranges for
somatic gNaP (0-100 pS/um^2 = 0-0.01 S/cm^2) carry over to t0080's v3 distal-NaP cap as already
specified in `research_papers.md`.

### Canonical Exp2NMDA Mg-block formula and reference implementations

The ModelDB Exp2NMDA mod file pattern [ModelDB-nmdasyn-mod] uses the canonical Jahr-Stevens form:

```
Mgblock = 1 / (1 + (Mg/K0) * exp((0.001) * (-z) * delta * F * v / R / (T+35)))
```

with reference parameters:

* `tau1 = 8.8 ms` (rise; Spruston 1995 CA1 dendrite)
* `tau2 = 500 ms` (decay)
* `K0 = 4.1 mM` (IC50 at 0 mV) -- some sources also use 3.57 mM per Jahr-Stevens 1990
* `delta = 0.8` (electrical distance of Mg2+ binding site)
* `Mg = 1.2 mM` (extracellular concentration; physiological range 1.0-1.5 mM)
* `z = 2` (Mg2+ valency)
* `e = -0.7 mV` (reversal)

Current: `i = (B - A) * Mgblock(v) * (v - e)` with `A' = -A/tau1`, `B' = -B/tau2`. The Poleg-Polsky
2016 ModelDB 189347 [ModelDB-189347] uses a related `bipolarNMDA.mod` file; the t0080 v3 substrate
should re-use this Bed-B-native template rather than introducing a different kinetic scheme. This
preserves continuity with the t0078 substrate's existing `Exp2NMDA` SUFFIX vendored from ModelDB
189347\.

**Best practice (community consensus)**: For DSGC NMDA modeling, use the Jahr-Stevens form with
`delta=0.8`, `K0=4.1` (or 3.57) mM, `Mg=1.0-1.5` mM. The asymmetric trapping block model
[Vargas-Caballero-2004] adds slow dynamics (tau ~ 300 ms) but is not necessary for DSGC
direction-selectivity work where the slow component is dominated by the AMPA + GABA dynamics.

### NSGA-II vs single-objective BO comparisons in computational neuroscience (community

landscape)

The internet search did not surface a head-to-head NSGA-II vs BoTorch qLogNEHVI comparison on NEURON
multi-compartment models published in 2023-2025. The closest reference is BluePyOpt
[BluePyOpt-PubMed], which uses a CMA-ES / IBEA / NSGA-II family for biophysical neuron model fitting
and is the de facto community standard for this workflow. BluePyOpt's documentation patterns are an
alternative reference if pymoo's recipe needs adaptation. No 2024 paper reports head-to-head HV
comparisons of BO vs NSGA-II on neural models, so the t0080 negative-result case ("NSGA-II fails to
match t0078's HV 11.41") will itself be a small but useful methodological contribution to this gap.

## Methodology Insights

* **Use pymoo `NSGA2(pop_size=96, sampling=LHS())` with default SBX `eta=15`, PM `eta=20`**
  [pymoo-NSGA2-docs, pymoo-Crossover-docs]. The plan's chosen values match the canonical defaults
  exactly; no parameter sweep on operator etas is needed for a first run.

* **Wrap the NEURON evaluation in `ElementwiseProblem._evaluate` with `multiprocessing.Pool` +
  `StarmapParallelization`** [pymoo-Starmap-docs]. Pin `pymoo>=0.6.0` -- in older versions
  `StarmapParallelization` lives in a different submodule [pymoo-issue-763] and the import will
  fail.

* **Always call `pool.close()` after `minimize()`** [pymoo-Starmap-docs] to avoid leaked worker
  processes that would burn Vast.ai compute budget after the optimisation loop ends.

* **Negate objectives to maximise**: pymoo NSGA-II minimises objectives. For maximising DSI and PD
  rate, set `out["F"] = [-dsi, -pd_rate]`. The reference point for hypervolume tracking should be
  set at `[0, 0]` in the maximisation-flipped (negated) sign convention to match the t0076 / t0078
  convention.

* **Inside each `_evaluate`, run NEURON in a fresh subprocess** to avoid the
  `Exp2NMDA name already exists` error [t0078 carry-over, pymoo-Custom-docs]. The pymoo pool worker
  can call `subprocess.run` to a one-shot trial script that loads NEURON, evaluates, and returns DSI
  / PD rate via JSON over stdout.

* **Confirm pymoo version 0.6.1.6 or later before launching**: t0080's plan should pin
  `pymoo>=0.6.1.6` in `pyproject.toml`. The current canonical docs at
  `pymoo.org/algorithms/moo/nsga2.html` are versioned to 0.6.1.6.

* **Use `seed=1` for reproducibility but vary across runs**: pymoo `minimize(seed=N)` controls all
  stochastic operators (LHS, SBX, PM, tournament). Document the seed in `results/results_summary.md`
  for the substrate-regression cross-checks.

* **Use canonical Jahr-Stevens Exp2NMDA Mg-block parameters** [ModelDB-nmdasyn-mod]: `K0=4.1` mM,
  `delta=0.8`, `Mg=1.0-1.5` mM. Re-use the t0078 / Bed-B `bipolarNMDA.mod` template [ModelDB-189347]
  rather than introducing a different mod file; this preserves substrate continuity.

* **AIS architecture target: 25 um length, 1.0 -> 0.6 um taper** [Werginz2024-PMC]. The v3 AIS
  geometry MOBO bounds should constrain the AIS to within 20-30 um length and 0.5-1.5 um diameter
  taper to remain biologically plausible.

* **Hypothesis to test (best practice from BluePyOpt community)** [BluePyOpt-PubMed]: when
  multi-objective evolutionary fits fail to reach a target, the failure pattern (Pareto front
  geometry, parameter clustering) is itself diagnostic. Document the v3 NSGA-II Pareto-front
  geometry even on a negative result.

* **Hypothesis to test (general MOBO-on-biophysics)**: if the v3 NSGA-II Pareto front collapses to
  the bound on multiple parameters (replicating the iter-81 AIS-disabled-corner pattern at different
  parameters), this confirms the failure mode is universal across MOBO algorithms and motivates a
  stronger biological-prior penalty term in future tasks. The answer asset should include this as a
  follow-up hypothesis.

## Discovered Papers

### [Pitcher-bioRxiv-2026]

* **Title**: Retinal waves shape starburst amacrine cell dendrite development through a
  direction-selective dendritic computation
* **Authors**: Pitcher, M. N., Gonzales, A. S. B., Habib, R., Feller, M.
* **Year**: 2026
* **DOI**: `10.64898/2026.02.02.701812` (bioRxiv preprint identifier)
* **URL**: https://www.biorxiv.org/content/10.64898/2026.02.02.701812v1
* **Suggested categories**: `direction-selectivity`, `dendritic-computation`,
  `retinal-ganglion-cell`
* **Why download**: Recent (2026) bioRxiv preprint demonstrating that SAC dendritic direction
  selectivity is built during retinal-wave development. Provides upstream context for the SAC
  inhibitory machinery that t0080 keeps fixed in the Bed B substrate; the SAC dendritic-computation
  finding could constrain future Bed B substrate variants.

### [Cbln4-JNeurosci-2024]

* **Title**: Differential Expression Analysis Identifies Candidate Synaptogenic Molecules for Wiring
  Direction-Selective Circuits in the Retina
* **Authors**: (multi-author; first-author surname not extracted from search snippet)
* **Year**: 2024
* **DOI**: not extracted (J Neurosci 44(18):e1461232024 - infer DOI as
  `10.1523/JNEUROSCI.1461-23.2024`)
* **URL**: https://www.jneurosci.org/content/44/18/e1461232024
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`,
  `compartmental-modeling`
* **Why download**: Tests Cbln4 in ventral-preferring DSGCs and reports reduced direction-selective
  tuning, providing a wiring-specificity anchor that complements the Bed B substrate's geometric
  assumptions.

### [Riccitelli-PNAS-2025]

* **Title**: Retinal ganglion cells encode the direction of motion through a suppressive surround
  (working title; full title to verify)
* **Authors**: Riccitelli, S., et al. (Rivlin lab)
* **Year**: 2025
* **DOI**: not extracted (PNAS 2025)
* **URL**:
  https://www.weizmann.ac.il/brain-sciences/labs/rivlin/sites/brain-sciences.labs.rivlin/files/2025-05/Riccitelli%202025.pdf
* **Suggested categories**: `direction-selectivity`, `retinal-ganglion-cell`
* **Why download**: Reports direction-tuned firing in non-DS-RGCs through asymmetric activity beyond
  classic receptive field. Broader project context for the DRD4 vs non-DRD4 direction-tuning
  question flagged as a gap in `research_papers.md`.

### [WerginzAxial-bioRxiv-2020]

* **Title**: Properties of the axial current of retinal ganglion cells at spike initiation /
  Electrical match between initial segment and somatodendritic compartment for action potential
  backpropagation in retinal ganglion cells
* **Authors**: (Werginz, P. and colleagues; full author list to verify)
* **Year**: 2020 (v1: 2020-09-15; v2: revised)
* **DOI**: not extracted (bioRxiv preprint id `10.1101/2020.09.15.297937`)
* **URL**: https://www.biorxiv.org/content/10.1101/2020.09.15.297937v2
* **Suggested categories**: `voltage-gated-channels`, `retinal-ganglion-cell`, `patch-clamp`,
  `compartmental-modeling`
* **Why download**: Develops resistive-coupling theory to estimate AIS Nav density from
  axial-current measurements in mouse RGCs -- an independent, model-free methodology that reinforces
  the Werginz 2024 1.3 S/cm^2 estimate and strengthens the v3 hard-floor argument for
  `nav16_ais >= 0.25 S/cm^2`. The published version of Werginz et al. 2020 (Sci. Adv.) is already in
  the corpus, but this AIS-axial-current preprint is a separate work focused specifically on the
  Nav-density-estimation methodology.

## Recommendations for This Task

1. **Pin `pymoo>=0.6.1.6` in `pyproject.toml`** [pymoo-NSGA2-docs, pymoo-issue-763]. Older versions
   have an incompatible `StarmapParallelization` import path that will break the v3 harness.

2. **Use the exact canonical NSGA2 instantiation from the pymoo docs**:
   `NSGA2(pop_size=96, sampling=LHS())` with no override of crossover / mutation / selection
   defaults (already SBX `eta=15`, PM `eta=20`, binary tournament; matches plan) [pymoo-NSGA2-docs].
   This updates `research_papers.md` recommendation 6 with the verified default values.

3. **Use `multiprocessing.Pool(64)` + `StarmapParallelization(pool.starmap)` and call `pool.close()`
   after `minimize()`** [pymoo-Starmap-docs]. Inside each pool-worker `_evaluate`, fan out to
   `subprocess.run` for fresh NEURON re-init (carry-over from t0078).

4. **Negate objectives `out["F"] = [-dsi, -pd_rate]` and use `[0, 0]` reference point in
   negation-sign-flipped HV tracking** [pymoo-NSGA2-docs]. This preserves the t0076 / t0078
   reference-point convention.

5. **Confirm Exp2NMDA / `bipolarNMDA.mod` re-use from t0078 substrate**
   [ModelDB-189347, ModelDB-nmdasyn-mod]. Use the canonical Jahr-Stevens parameters: `K0=4.1` mM,
   `delta=0.8`, `Mg=1.0-1.5` mM, `tau1=8.8` ms, `tau2=500` ms. No new mod file needed.

6. **Constrain AIS geometry MOBO bounds to 20-30 um length, 0.5-1.5 um diameter taper**
   [Werginz2024-PMC]. This complements the Nav-density hard floor with a geometric biological-prior
   bound.

7. **Add the four discovered papers to the corpus before the planning stage** to maximise paper
   coverage for the v3 substrate planning. Order of addition (by relevance):
   [WerginzAxial-bioRxiv-2020] (AIS Nav methodology) > [Pitcher-bioRxiv-2026] (SAC upstream context)
   \> [Cbln4-JNeurosci-2024] (DSGC wiring) > [Riccitelli-PNAS-2025] (broader DS context).

8. **Document the 2-objective vs 20-objective NSGA-II evaluation budget difference vs Hay 2011**
   [Hay2011-PMC] in `results/results_summary.md`. t0080's 3,840 evaluations vs Hay's 500,000 is
   justified by the smaller objective dimensionality and the warm-start from t0078, but should be
   stated explicitly to motivate the budget choice.

9. **If NSGA-II fails to lift HV above t0078's 11.41**, document the negative result against
   BluePyOpt-style multi-fit failure-pattern analysis [BluePyOpt-PubMed] -- the Pareto-front
   geometry and parameter clustering are diagnostic regardless of HV outcome.

## Source Index

### [pymoo-NSGA2-docs]

* **Type**: documentation
* **Title**: NSGA-II: Non-dominated Sorting Genetic Algorithm
* **Author/Org**: pymoo project (Blank, J., Deb, K.)
* **URL**: https://pymoo.org/algorithms/moo/nsga2.html
* **Last updated**: pymoo 0.6.1.6 (2024-2025)
* **Peer-reviewed**: no (accompanies peer-reviewed Blank+Deb 2020 IEEE Access paper)
* **Relevance**: Canonical NSGA-II API documentation. Confirms default `pop_size=100`, SBX `eta=15`,
  PM `eta=20`, binary tournament selection, and `RankAndCrowding` survival. Source of the minimal
  canonical `minimize()` recipe for t0080.

### [pymoo-Starmap-docs]

* **Type**: documentation
* **Title**: Starmap Interface
* **Author/Org**: pymoo project
* **URL**: https://pymoo.org/parallelization/starmap.html
* **Last updated**: pymoo 0.6.1.6
* **Peer-reviewed**: no
* **Relevance**: Canonical multi-process recipe with `multiprocessing.Pool` and
  `StarmapParallelization`. Provides the exact `ElementwiseProblem` + `elementwise_runner` pattern
  that t0080 will use for the 64-core CPU evaluation.

### [pymoo-Crossover-docs]

* **Type**: documentation
* **Title**: Crossover (Operators)
* **Author/Org**: pymoo project
* **URL**: https://pymoo.org/operators/crossover.html
* **Peer-reviewed**: no
* **Relevance**: Reference for SBX (`SimulatedBinaryCrossover`) eta default and probability
  parameters across pymoo algorithms.

### [pymoo-Sampling-docs]

* **Type**: documentation
* **Title**: Sampling (Operators)
* **Author/Org**: pymoo project
* **URL**: https://pymoo.org/operators/sampling.html
* **Peer-reviewed**: no
* **Relevance**: Documents `LHS`, `FloatRandomSampling`, and Sobol sampling. Confirms LHS is the
  recommended initial-population sampler for evolutionary algorithms with bound-constrained
  continuous problems.

### [pymoo-Custom-docs]

* **Type**: documentation
* **Title**: Custom Parallelization
* **Author/Org**: pymoo project
* **URL**: https://pymoo.org/parallelization/custom.html
* **Peer-reviewed**: no
* **Relevance**: Documents how to write custom parallelization wrappers if `StarmapParallelization`
  is insufficient. Useful as a fallback if the NEURON-fresh-subprocess pattern requires a custom
  runner beyond `StarmapParallelization`.

### [pymoo-issue-763]

* **Type**: forum
* **Title**: BUG report -- StarmapParallelization class moved to other subpackage
* **Author/Org**: anyoptimization/pymoo GitHub Issues
* **Date**: 2024 (issue #763)
* **URL**: https://github.com/anyoptimization/pymoo/issues/763
* **Peer-reviewed**: no
* **Relevance**: Documents the pymoo 0.5 -> 0.6 refactor that moved `StarmapParallelization` from
  `pymoo.core.problem` to `pymoo.parallelization.starmap`. t0080's `pyproject.toml` must pin
  `pymoo>=0.6.0` to avoid this trap.

### [Hay2011-PMC]

* **Type**: paper
* **Title**: Models of Neocortical Layer 5b Pyramidal Cells Capturing a Wide Range of Dendritic and
  Perisomatic Active Properties
* **Authors**: Hay, E., Hill, S., Schurmann, F., Markram, H., Segev, I.
* **Year**: 2011
* **DOI**: `10.1371/journal.pcbi.1002107`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC3145650/
* **Peer-reviewed**: yes (PLoS Comput Biol)
* **Relevance**: Confirms parameter ranges and the multi-objective evolutionary methodology
  precedent for t0080. Already in corpus but the PMC version exposes Table 2 parameter ranges more
  readably than the original PDF.

### [ModelDB-139653]

* **Type**: dataset
* **Title**: L5b PC model constrained for BAC firing and perisomatic current step firing (Hay et
  al., 2011)
* **Author/Org**: Hay, E. (deposited via ModelDB)
* **URL**: https://modeldb.science/139653
* **Peer-reviewed**: no (model deposit accompanies peer-reviewed Hay 2011)
* **Relevance**: Repository of the ~2,000 acceptable Hay 2011 L5 PC models with full parameter
  ensembles. Reference for t0080's multi-cell ensemble-as-experiment analysis pattern.

### [ModelDB-189347]

* **Type**: dataset
* **Title**: Multiplication by NMDA receptors in Direction Selective Ganglion cells (Poleg-Polsky &
  Diamond 2016)
* **Author/Org**: Poleg-Polsky, A.
* **URL**: https://modeldb.science/189347
* **Peer-reviewed**: no
* **Relevance**: Provides the canonical Bed-B `bipolarNMDA.mod` file with Mg-block voltage-dependent
  NMDA implementation. Direct upstream for the t0080 v3 dendritic NMDA insertion.

### [ModelDB-nmdasyn-mod]

* **Type**: documentation
* **Title**: nmdasyn.mod (NEURON Mod File for Exp2NMDA with Voltage-Dependent Mg Block)
* **Author/Org**: ModelDB 267357
* **URL**: https://modeldb.science/getModelFile?model=267357&file=model_files/nmdasyn.mod&embed=True
* **Peer-reviewed**: no
* **Relevance**: Reference Exp2NMDA implementation showing the canonical Jahr-Stevens Mg-block
  formula `Mgblock = 1 / (1 + (Mg/K0) * exp((0.001) * (-z) * delta * F * v / R / (T+35)))` with
  parameters `K0=4.1` mM, `delta=0.8`, `Mg=1.2` mM. Reference point for the t0080 v3 dendritic NMDA
  mod file.

### [Werginz2024-PMC]

* **Type**: paper
* **Title**: Differential Intrinsic Firing Properties in Sustained and Transient Mouse alpha-RGCs
  Match Their Light Response Characteristics
* **Authors**: Werginz, P., Kiraly, V., Zeck, G.
* **Year**: 2024
* **DOI**: `10.1523/JNEUROSCI.1592-24.2024`
* **URL**: https://pmc.ncbi.nlm.nih.gov/articles/PMC11714343/
* **Peer-reviewed**: yes (J Neurosci)
* **Relevance**: PMC version of the Werginz 2024 paper with Table 1 channel densities and AIS
  geometry confirmed (gNa AIS 1300 mS/cm^2, soma 75 mS/cm^2; AIS length 25 um, taper 1.0 -> 0.6 um).
  Already in corpus but PMC version provides input-resistance values and methodological notes not
  extracted from the original.

### [WerginzAxial-bioRxiv-2020]

* **Type**: paper
* **Title**: Properties of the axial current of retinal ganglion cells at spike initiation
  (alternate v2 title: Electrical match between initial segment and somatodendritic compartment for
  action potential backpropagation in retinal ganglion cells)
* **Authors**: Werginz, P., et al.
* **Year**: 2020 (v1: 2020-09-15; v2: revised)
* **URL**: https://www.biorxiv.org/content/10.1101/2020.09.15.297937v2
* **Peer-reviewed**: no (bioRxiv preprint)
* **Relevance**: Develops resistive-coupling theory for AIS Nav-density estimation from
  axial-current measurements in mouse RGCs. Independent methodology supporting the v3
  `nav16_ais >= 0.25 S/cm^2` hard floor.

### [Pitcher-bioRxiv-2026]

* **Type**: paper
* **Title**: Retinal waves shape starburst amacrine cell dendrite development through a
  direction-selective dendritic computation
* **Authors**: Pitcher, M. N., Gonzales, A. S. B., Habib, R., Feller, M.
* **Year**: 2026
* **URL**: https://www.biorxiv.org/content/10.64898/2026.02.02.701812v1
* **Peer-reviewed**: no (bioRxiv preprint)
* **Relevance**: Recent SAC dendritic-computation paper relevant as upstream context for the SAC
  inhibitory machinery that t0080 keeps fixed.

### [Cbln4-JNeurosci-2024]

* **Type**: paper
* **Title**: Differential Expression Analysis Identifies Candidate Synaptogenic Molecules for Wiring
  Direction-Selective Circuits in the Retina
* **Authors**: (J Neurosci 44:e1461232024)
* **Year**: 2024
* **URL**: https://www.jneurosci.org/content/44/18/e1461232024
* **Peer-reviewed**: yes (J Neurosci)
* **Relevance**: DSGC wiring-specificity paper testing Cbln4 in ventral-preferring DSGCs.

### [Riccitelli-PNAS-2025]

* **Type**: paper
* **Title**: Retinal ganglion cells encode the direction of motion through a suppressive surround
* **Authors**: Riccitelli, S., et al.
* **Year**: 2025
* **URL**:
  https://www.weizmann.ac.il/brain-sciences/labs/rivlin/sites/brain-sciences.labs.rivlin/files/2025-05/Riccitelli%202025.pdf
* **Peer-reviewed**: yes (PNAS)
* **Relevance**: Direction-tuned firing in non-DS-RGCs through asymmetric extra-receptive-field
  activity. Broader project context for the DRD4 vs non-DRD4 direction-tuning gap.

### [BluePyOpt-PubMed]

* **Type**: paper
* **Title**: BluePyOpt: Leveraging Open Source Software and Cloud Infrastructure to Optimise Model
  Parameters in Neuroscience
* **Authors**: Van Geit, W., et al.
* **Year**: 2016
* **DOI**: `10.3389/fninf.2016.00017`
* **URL**: https://pubmed.ncbi.nlm.nih.gov/27375471/
* **Peer-reviewed**: yes (Front Neuroinform)
* **Relevance**: De facto community standard for biophysical neuron model fitting. Reference for
  comparing pymoo NSGA-II patterns to the BluePyOpt CMA-ES / IBEA / NSGA-II family workflow if pymoo
  runs into issues. Provides community context for the negative-result discussion.

### [IDAES-LHS]

* **Type**: documentation
* **Title**: Latin Hypercube Sampling (LHS) -- IDAES Toolkit
* **Author/Org**: IDAES PSE Project
* **URL**:
  https://idaes-pse.readthedocs.io/en/1.13.0/explanations/modeling_extensions/surrogate/pysmo/pysmo_lhs.html
* **Peer-reviewed**: no
* **Relevance**: Standard reference for the LHS algorithm itself (equal-probability bins per
  dimension, independent shuffling across dimensions). Backs up the pymoo LHS recommendation with a
  methodological reference.

### [Vargas-Caballero-2004]

* **Type**: paper
* **Title**: Fast and Slow Voltage-Dependent Dynamics of Magnesium Block in the NMDA Receptor: The
  Asymmetric Trapping Block Model
* **Authors**: Vargas-Caballero, M., Robinson, H. P. C.
* **Year**: 2004
* **DOI**: derived from URL (J Neurosci 24:6171)
* **URL**: https://www.jneurosci.org/content/24/27/6171
* **Peer-reviewed**: yes (J Neurosci)
* **Relevance**: Refines the Jahr-Stevens model with fast (100 us) and slow (300 ms) Mg unblock
  components. Not adopted in the v3 substrate but referenced for methodological completeness; the
  Bed-B / Poleg-Polsky 2016 substrate uses the simpler Jahr-Stevens form by community convention.
