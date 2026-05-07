# Brainstorm Session 18: Strategic pivot to morphology-extended optimisation

Eighteenth brainstorming session. Run on 2026-05-07 after t0088
(`recluster_marginals_and_vm_motifs`) extended t0086's biological-plausibility analysis to a 13-cell
pool (6 Genuine + 7 Marginal), confirmed `shared_mechanism_different_scale` across all 4 clusters
(NaP-dominant in PD-minus-ND attribution at 87.4-99.7%, NMDA frac 0.000), and surfaced a new extreme
prior violation (Cluster 1 AIS-to-soma Nav ratio 116x = +33 sigma above Werginz 2024). Project spend
$15.56 / $20.00; **$4.44 remaining**.

The researcher's directive was a strategic pivot: "Optimisation technique seems to work. We now need
to add a big and important part of cells - cell morphology." After two iterations on parametrisation
strategy, the agreed approach is a **procedural DSGC morphology generator with 14 explicit knobs**
covering topology, asymmetry, and geometry, called inside the NSGA-II evaluation loop.

## Decisions

* **Create t0090** -- procedural DSGC morphology generator + 30-different + 30-similar diversity
  test + Bed-B reproducibility check + validation bundle. Phases:

  * **Phase A (generator implementation)**: implement procedural generator in Python that takes 14
    morphology parameters plus a `morph_seed` and emits NEURON sections + connectivity. Parameters:
    5 topology (`num_primary_branches` 3-7, `branch_prob_per_um` 0.005-0.05, `max_strahler_depth`
    2-6, `mean_branching_angle_deg` 30-90, `rall_exponent` 0.5-2.0); 4 asymmetry
    (`soma_offset_pd_um` -150 to +150, `field_elongation_pd` 1.0-3.0, `branch_density_gradient_pd`
    -1 to +1, `primary_branch_pd_concentration` 0-5 von Mises kappa); 3 geometry
    (`mean_segment_length_um` 10-60, `soma_diameter_um` 8-18, `ais_length_um` 15-60); 2 stochastic
    control (`morph_seed`, `branch_length_cv` 0-0.5). Deterministic given (`params`, `seed`).

  * **Phase B (30 very-different morphologies)**: wide Latin Hypercube sample over the 14-d morph
    param space; generate in parallel on 64-core EPYC.

  * **Phase C (30 very-similar morphologies)**: tight perturbations (+/- 5%) around a
    Bed-B-equivalent base point; generate in parallel.

  * **Phase D (verification simulation)**: build each morphology in NEURON, run a 50 ms no-stim
    stability check + 8-direction bar protocol with default t0083 best-cell channels; catch
    degenerate geometries (NaN, divergence, disconnected sections). Parallelise on 64 cores.

  * **Phase E (visualisation)**: 2D dendrograms for all 60 morphologies, PCA / UMAP of morphometric
    features (total dendritic length, branch count, electrotonic length, soma displacement, max
    Strahler depth); side-by-side panels of 30-different vs 30-similar so the diversity coverage is
    visually obvious.

  * **Phase F (Bed-B reproducibility)**: pick a `morph_params` point that approximates de Rosenroll
    2026 / Bed B; run 5 t0083 Pareto cells through the generator at that point; confirm DSI / PD
    within 5% of original Bed B.

  * **Phase G (validation bundle)**: bundle three cheap validation suggestions that sharpen
    biological interpretation in t0091. (1) **S-0088-02** AIS-to-soma Nav ratio audit (cluster 1's
    116x is suspicious; 30 min, $0). (2) **S-0086-02** NMDA units calibration ablation (1 hour,
    ~$0.30). (3) **S-0088-01** causal NaP-knockout per cluster representative (4 cells x 16 dirs;
    ~64 min, $0).

  **Pass criteria**: generator deterministic; 60 / 60 morphologies simulate without errors;
  "different" set covers visibly distinct morphology classes; "similar" set produces tight clusters
  in morphometric PCA; Bed-B reproducibility within 5%; all 3 validation suggestions answered.

  **Output**: validated generator library + a curated warm-start anchor archive of viable diverse
  morphologies for t0091. **Cost ~$0.30, ~3-4 days wall-clock, mostly local 64-core CPU.**

  Source suggestions: covers S-0088-02, S-0086-02, S-0088-01 in Phase G; t0090 is otherwise a new
  direction with no source suggestion. Dependencies: t0024, t0078, t0080, t0081, t0083, t0086,
  t0088. `expected_assets = {"library": 1, "answer": 1}`. Task types:
  `["library-implementation", "data-analysis", "answer-question"]`.

* **Create t0091** -- first joint 68-d NSGA-II optimisation with morphology generated inside the
  evaluation loop, warm-started from 5 distinct morphology anchor points. Phases:

  * **Phase A (warm-start population)**: build pop 96 from 5 anchors x ~19 t0083 Pareto electrophys
    variants each. Anchors: (1) **Bed-B-like** (matches existing t0083 substrate); (2) **symmetric**
    (`soma_offset_pd_um=0`, `field_elongation_pd=1.0`, `branch_density_gradient_pd=0`,
    `primary_branch_pd_concentration=0`); (3) **PD-asymmetric** (soma offset +100 um toward PD,
    field elongated 2x along PD, branches biased toward PD); (4) **ND-asymmetric** mirror of #3; (5)
    **alternative-topology** (more primary branches, deeper Strahler depth, smaller field).

  * **Phase B (joint NSGA-II)**: pop 96, <=8 generations, generator inside eval loop; adaptive
    HV-plateau stop + cost watchdog (post-S-0083-04 fix). On Vast.ai EPYC 7B13 64-core. Each
    evaluation: NSGA-II proposes 68-d vector -> generator builds NEURON model from 14 morph params
    + morph_seed -> 54 channel/synapse params inserted into generated sections -> bar-rotation
      simulation -> objectives returned (DSI, PD firing rate, robustness).

  * **Phase C (Pareto + biological-plausibility analysis)**: extend t0086 / t0088 framework to 68-d
    cells; do morph-extended Pareto cells reach biologically-plausible NMDA / NaP regimes that 54-d
    cells could not?

  * **Phase D (anchor-tracking analysis)**: which of the 5 anchors are over- vs under-represented in
    the final Pareto? If anchor #3 (PD-asymmetric) is preserved more than anchor #4 (ND-asymmetric),
    that is strong evidence for soma-displacement-toward-PD as a functional DS mechanism (Schachter
    2010, Trenholm 2013).

  * **Phase E (answer asset)**: "Does in-loop morphology optimisation open biologically-plausible
    joint-pass regions, and which morphological asymmetries does the optimiser favour?"

  **Pass criteria**: Phase B converges with HV plateau or 8-gen cap; Phase C extends t0086 framework
  cleanly; Phase D produces a definitive yes/no on whether morphology variation reaches biologically
  plausible cells; anchor-tracking yields a clear PD-vs-ND asymmetry verdict. **Acceptable
  negative**: optimiser pegs all anchors back toward Bed-B-like -> conclusion is the v3 substrate's
  biological-plausibility ceiling is not raised by this morphology parametrisation, motivating
  Option G (NeuroMorpho real-cell library) in a future task.

  **Cost ~$3.00-3.50, ~14-16 hours Vast.ai. Buffer remaining ~$0.94-1.44.**

  Source suggestions: none directly (new direction). Dependencies: t0024, t0078, t0080, t0081,
  t0083, t0086, t0088, t0090. `expected_assets = {"answer": 1, "predictions": 1}`. Task types:
  `["experiment-run", "data-analysis", "answer-question"]`.

## Suggestion Cleanup

### Rejected (covered by new tasks)

* **S-0086-02** (NMDA units calibration) -- covered by t0090 Phase G.
* **S-0088-01** (causal NaP-knockout per cluster representative) -- covered by t0090 Phase G.
* **S-0088-02** (AIS-to-soma Nav ratio audit) -- covered by t0090 Phase G.
* **S-0084-05** (channel-knockout DSI causal-attribution variant) -- duplicate of S-0088-01 (which
  itself is now covered by t0090 Phase G).
* **S-0083-03** (per-direction Vm-trace deep-dive of cell 1304) -- covered by t0088 (cell 1304 is a
  member of cluster 1 with representative cell 1634; mechanism attribution NaP 87.4% / Nav1.6 12.6%
  / NMDA 0.0% applies to all cluster-1 cells including 1304).

### Reprioritised (high -> medium)

* **S-0083-01** (extend NSGA-II from t0083 gen 17 to gen 25 with pop 144) -- estimated $8-12, out of
  remaining $4.44 budget; superseded by the morphology-extended NSGA-II direction in t0091.
* **S-0084-01** (NaP density sweep on cells 767 / 637 / 762) -- superseded by S-0088-01-style binary
  knockout in t0090 Phase G; older single-cell scope.
* **S-0084-02** (per-seed mechanism decomposition of cell 767) -- older single-cell scope; mechanism
  attribution at population level already established by t0088.

### Stays high

* **S-0086-01** (NSGA-II re-run with tightened NMDA bounds, $1.50) -- natural follow-up after t0091;
  if t0091 finds biologically plausible joint-pass cells under morphology variation, may also
  benefit from tightened-bounds variant.
* **S-0070-01** (harmonise PD / ND encoding across Bed A and Bed B) -- independent infra; not
  affected by morphology direction.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.

## Assets Produced

No assets in this brainstorm task. The new tasks t0090 and t0091 will produce: t0090 a morphology
generator library + a mechanism-distinctness answer asset; t0091 a Pareto-front predictions asset
+ an answer asset on morphology-extended biological plausibility.

## Budget Context

Project budget $20.00; **$15.56 spent** before t0090 / t0091; **$4.44 remaining**. t0090 estimated
**$0.30** (validation bundle in Phase G). t0091 estimated **$3.00-3.50** (Vast.ai EPYC 7B13). Buffer
remaining after both: **$0.94-1.44**.
