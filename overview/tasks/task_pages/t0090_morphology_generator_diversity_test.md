# ⏹ Procedural DSGC morphology generator + diversity test + validation bundle

[Back to all tasks](../README.md)

## Overview

| Field | Value |
|---|---|
| **ID** | `t0090_morphology_generator_diversity_test` |
| **Status** | ⏹ not_started |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md), [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md), [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md), [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Task types** | `write-library`, `data-analysis`, `answer-question` |
| **Expected assets** | 1 library, 1 answer |
| **Task folder** | [`t0090_morphology_generator_diversity_test/`](../../../tasks/t0090_morphology_generator_diversity_test/) |

<details>
<summary><strong>Task Description</strong></summary>

*Source:
[`task_description.md`](../../../tasks/t0090_morphology_generator_diversity_test/task_description.md)*

# Procedural DSGC morphology generator + diversity test + validation bundle

## Motivation

The project is making a strategic pivot from electrophys-only optimisation (t0080-t0088) to
**morphology-extended optimisation**. Up to t0088, all NSGA-II runs (t0076 through t0083) used
the fixed Bed B morphology (de Rosenroll 2026 port from t0024). Morphology was
sensitivity-tested one-axis-at-a-time (t0029, t0030, t0034, t0035, t0041) but was never inside
the optimisation vector.

Brainstorm session 18 (t0089) commissioned a procedural DSGC morphology generator that exposes
explicit knobs for topology, asymmetry, and geometry. Once validated, the generator will be
called inside t0091's NSGA-II evaluation loop, producing a 68-d joint optimisation (54-d v3
electrophys + 14-d morphology) warm-started from 5 distinct morph anchors.

This task delivers the validated generator, a diversity test demonstrating it covers the
intended morphology space, a Bed-B reproducibility check, and three bundled validation
suggestions that sharpen the biological interpretation of t0091's results.

## Scope

### In Scope

* Procedural Python generator emitting NEURON sections + connectivity from 14 morphology
  parameters
* Deterministic given (`params`, `morph_seed`) — same inputs produce identical sections
* 30 very-different morphologies generated via wide Latin Hypercube over the 14-d parameter
  space
* 30 very-similar morphologies generated via tight perturbations (+/- 5 percent) around a
  Bed-B-equivalent base point
* Verification simulation per morphology (50 ms no-stim stability + 8-direction bar protocol
  with default t0083 best-cell channels)
* 2D dendrogram visualisation for all 60 morphologies + PCA / UMAP of morphometric features
* Bed-B reproducibility check on 5 t0083 Pareto cells
* Validation bundle (S-0088-02 AIS-to-soma Nav ratio audit, S-0086-02 NMDA units calibration,
  S-0088-01 causal NaP-knockout per cluster representative)
* One library asset (the generator) and one answer asset (mechanism distinctness across the
  validation triplet)

### Out of Scope

* The joint 68-d NSGA-II run itself (deferred to t0091)
* Topology-changing perturbations beyond the generator's parametric knobs (e.g., stochastic
  L-system extensions, real-cell library)
* Alternative simulators (NetPyNE / Brian2 / Arbor); NEURON only

## Approach

### Phase A — Implement procedural generator

Implement a Python module under `tasks/t0090_morphology_generator_diversity_test/code/` that
exposes:

```python
def generate_morphology(
    params: MorphologyParams,
    morph_seed: int,
) -> MorphologyResult:
    ...
```

The 14 morphology parameters:

| Group | Parameter | Range | Type |
| --- | --- | --- | --- |
| Topology | `num_primary_branches` | 3-7 | int |
| Topology | `branch_prob_per_um` | 0.005-0.05 | float |
| Topology | `max_strahler_depth` | 2-6 | int |
| Topology | `mean_branching_angle_deg` | 30-90 | float |
| Topology | `rall_exponent` | 0.5-2.0 | float |
| Asymmetry | `soma_offset_pd_um` | -150 to +150 | float |
| Asymmetry | `field_elongation_pd` | 1.0-3.0 | float |
| Asymmetry | `branch_density_gradient_pd` | -1 to +1 | float |
| Asymmetry | `primary_branch_pd_concentration` | 0-5 (von Mises kappa) | float |
| Geometry | `mean_segment_length_um` | 10-60 | float |
| Geometry | `soma_diameter_um` | 8-18 | float |
| Geometry | `ais_length_um` | 15-60 | float |
| Stochastic | `morph_seed` | int | int |
| Stochastic | `branch_length_cv` | 0-0.5 | float |

Sampling primary branches at angles drawn from a von Mises distribution biased by
`primary_branch_pd_concentration`; recursive branching constrained by `branch_prob_per_um`,
`mean_branching_angle_deg`, `max_strahler_depth`; daughter / parent diameter scaling by
`rall_exponent` (Rall's law); asymmetry transforms applied post-hoc (soma offset, field
elongation, branch density gradient).

Unit tests (in `code/test_*.py`):
* Determinism: same `(params, seed)` produces identical sections (compare section count,
  lengths, diameters)
* Edge cases: `num_primary_branches=3` (minimum) and `=7` (maximum), `max_strahler_depth=2`
  (shallow) and `=6` (deep)
* Round-trip: serialise NEURON sections to dict, reconstruct, confirm electrical-equivalence
* No-NaN: all section lengths > 0, all diameters > 0, no disconnected sections

Style: follow `arf/styleguide/python_styleguide.md`. Centralise paths in `paths.py`, constants
in `constants.py`. Use frozen dataclasses for `MorphologyParams` and `MorphologyResult`.

**Time**: ~1.5-2 days local development.

### Phase B — Generate 30 very-different morphologies

Wide Latin Hypercube sample over the 14-d morph parameter space. Each LHS row is a complete
parameter vector; generation is embarrassingly parallel across 64 cores using a
`ProcessPoolExecutor`.

Output: 30 morphology specifications saved to
`tasks/t0090_morphology_generator_diversity_test/data/different_morphologies/`.

**Time**: seconds (generation only).

### Phase C — Generate 30 very-similar morphologies

Define a Bed-B-equivalent base point (matches de Rosenroll 2026 morphology approximately).
Generate 30 perturbations: each parameter independently jittered uniform +/- 5 percent of its
range. Same parallel infrastructure as Phase B.

Output: 30 morphology specifications saved to `data/similar_morphologies/`.

**Time**: seconds.

### Phase D — Verification simulation per morphology

For each of the 60 morphologies (30 different + 30 similar):

1. Build the morphology as NEURON sections.
2. Run a 50 ms no-stim stability check at V_rest = -70 mV; confirm no NaN voltages, no
   divergence, no disconnected sections.
3. Run an 8-direction bar protocol with default t0083 best-cell channels (1400 ms trial length
   per the recorded researcher protocol; HH on for Vm / firing rate / DSI mode); confirm DSI
   is computable, simulation does not diverge.

Parallelise on 64 cores. Catch NaN / divergence / disconnected sections per morphology and
write a per-morphology stability flag.

**Cost**: $0 if local 64-core CPU; ~$0.10-0.20 if Vast.ai. **Time**: ~5-10 min on 64 cores.

### Phase E — Visualisation

Per morphology:
* 2D dendrogram (parent-segment radial layout)
* Morphometric features: total dendritic length (um), branch count, max Strahler depth,
  electrotonic length, soma displacement (sqrt of `soma_offset_pd_um^2`), dendritic field
  major-axis length

Across morphologies:
* Side-by-side panel: 30 different morphologies in a 5x6 grid; 30 similar morphologies in a
  5x6 grid; visual comparison of diversity coverage.
* Morphometric PCA: scatter of all 60 morphologies in PC1-PC2 with different / similar
  colour-coded.
* UMAP if `umap-learn` is available; PCA fallback if not (per t0088 precedent).

**Charts** (saved to `results/images/`):
* `morphology_grid_different.png` — 5x6 panel of 30 different morphologies
* `morphology_grid_similar.png` — 5x6 panel of 30 similar morphologies
* `morphometric_pca.png` — PCA of morphometric features
* `morphometric_umap.png` — UMAP if available

**Time**: ~1 hour local.

### Phase F — Bed-B reproducibility

Identify the `morph_params` point that approximates the de Rosenroll 2026 / Bed B port from
t0024:
* Use `num_primary_branches` matching the published value
* `mean_segment_length_um` calibrated to the published total dendritic length
* `soma_offset_pd_um=0` (Bed B is symmetric in the absence of explicit asymmetry)
* `field_elongation_pd=1.0`, `branch_density_gradient_pd=0`,
  `primary_branch_pd_concentration=0`
* `rall_exponent` matching Bed B's diameter taper
* `soma_diameter_um` matching Bed B's soma
* `ais_length_um` matching Bed B's AIS

Run 5 t0083 Pareto cells through the generator at this point; compare DSI / PD firing rate to
their original Bed B values (from t0083's `all_evaluations.json`). Pass criterion: within 5
percent.

**Time**: ~1 hour on 64 cores.

### Phase G — Validation bundle

Three bundled validation suggestions:

#### G.1 — S-0088-02: AIS-to-soma Nav ratio audit (cluster 1)

t0088 reported cluster 1 (cells 1304, 1504, 1624, 1634) has an AIS-to-soma Nav ratio = 116,
+33 sigma above Werginz 2024's 17.3 +/- 3 — the most extreme single-prior violation in t0086
or t0088. Audit the ratio computation:

* Confirm `centroid_unnormalised[NAV16_AIS_GBAR] / centroid_unnormalised[NAV16_SOMA_GBAR]` is
  in matching units (S/cm^2 / S/cm^2 = dimensionless).
* Check the soma Nav lower bound is not pinning the centroid soma value to a near-zero value,
  inflating the ratio.
* Check whether the 4 cluster-1 cells individually have AIS-to-soma ratios near 116, or
  whether the centroid is averaging across heterogeneous values.

Pure data analysis on existing JSON outputs from t0088 / t0086. **Time**: ~30 min, **cost**:
$0.

#### G.2 — S-0086-02: NMDA units calibration ablation

t0086's NMDA exotic verdict (>=85 sigma above Sivyer 2013) is so extreme that it likely
partially reflects a units / scope mismatch rather than a genuinely outlier biological
mechanism. The t0080 ParameterVector encoding `gnmda_dend` is the NetCon weight used in the
Exp2NMDA mechanism, while Sivyer 2013's value is a per-spine synaptic conductance measured in
voltage-clamp on RGC dendritic spines. These may differ by a per-cell area normalisation or by
an effective open-channel-fraction factor.

Run a calibration ablation: take a single t0080 cell, vary `gnmda_dend` from 1e-5 to 1e-2 uS,
measure the per-spine effective open conductance from the NEURON state during a stimulus, and
produce a calibration curve mapping NetCon weight to per-spine conductance. Then re-score the
t0086 / t0088 clusters against Sivyer 2013 in the corrected units. **Time**: ~1 hour,
**cost**: ~$0.30.

#### G.3 — S-0088-01: Causal NaP-knockout per cluster representative

t0088 attributed PD-minus-ND fractional contributions correlationally (NMDA 0%, Nav1.6
0.3-12.6%, NaP 87.4-99.7% across the 4 cluster representatives). To causally confirm NaP as
the dominant mechanism, set `nap_dend_distal = 0` in each of the 4 representative cells (1604,
1634, 767, 1639) and re-measure DSI at the 16 directions used by t0088. Expected effect: DSI
collapses to <0.2 in all 4 cells if NaP is causally responsible; DSI partially preserved if
NMDA + Nav1.6 + GABA also contribute.

Local-CPU only: 4 cells x 16 directions x ~60 s/sim = ~64 min wall-clock, **cost** $0.

#### G — Synthesis answer asset

One answer asset at
`assets/answer/validation-triplet-implications-for-biological-plausibility/` synthesising the
three findings: (a) does the cluster-1 AIS-to-soma Nav ratio reflect a units bug or a real
biological signal? (b) does the NMDA units calibration shift the cluster-NMDA-exotic verdict?
(c) does causal NaP-knockout confirm NaP-dominance, or does the attribution shift? Confidence
rating based on which findings converge.

## Pass Criteria

* Generator deterministic: 100 random `(params, seed)` pairs produce byte-identical NEURON
  section dumps when re-run.
* 60 / 60 morphologies (30 different + 30 similar) build successfully and pass the 50 ms
  no-stim stability check.
* "Different" set covers visibly distinct morphology classes when laid out in
  `morphology_grid_different.png`.
* "Similar" set produces tight clusters in morphometric PCA (cluster radius <= 10 percent of
  PC1-PC2 axis range).
* Bed-B reproducibility: 5 / 5 t0083 Pareto cells reproduce DSI / PD within 5 percent.
* All 3 validation suggestions produce concrete answers with quantitative verdicts.

**Acceptable negative**: if the Bed-B reproducibility check fails, fall back to the TREES
toolbox (Cuntz 2010) for the generator. If 60 / 60 morphologies do not all simulate cleanly,
the generator's parameter ranges are too wide; tighten before t0091.

## Compute and Budget

* **Local 64-core EPYC** for Phases B, C, D, E, F (generation and verification simulations).
* **No remote machine for t0090 Phases A-F**.
* **Vast.ai EPYC 7B13** optional for Phase G.2 (NMDA units calibration ablation, ~$0.30).

**Total estimated cost**: ~$0.30 (Phase G.2 only). Buffer remaining after t0090: ~$4.14.

## Time Estimation

* Phase A (generator implementation): 1.5-2 days local
* Phase B (30 different): seconds
* Phase C (30 similar): seconds
* Phase D (verification sims): ~5-10 min on 64 cores
* Phase E (visualisation): ~1 hour
* Phase F (Bed-B reproducibility): ~1 hour
* Phase G (validation bundle): ~3-4 hours total

**Total wall-clock**: ~3-4 days.

## Expected Assets

* **Library asset**: the procedural DSGC morphology generator (`expected_assets["library"] =
  1`)
* **Answer asset**: validation-triplet biological-plausibility synthesis
  (`expected_assets["answer"] = 1`)

## Risks and Fallbacks

* **Generator implementation slips beyond 3 days**: fall back to TREES toolbox (Cuntz 2010)
  with asymmetry knobs added post-hoc.
* **Some morphologies fail to simulate**: mark them in the `verification_summary.json`,
  exclude from the warm-start anchor archive for t0091, narrow the LHS bounds for the next
  run.
* **Bed-B reproducibility outside 5 percent**: investigate before t0091; the generator may
  need a diameter-taper correction or an axial connectivity fix.
* **NMDA units calibration shows the Sivyer 2013 prior is correctly applied (no units bug)**:
  the
  >=85 sigma exotic verdict is genuine, motivating S-0086-01 (NSGA-II re-run with tightened NMDA
  bounds) as a higher-priority follow-up after t0091.

## Verification Criteria

* All unit tests pass (`uv run pytest tasks/t0090_morphology_generator_diversity_test/code/`).
* `verify_logs.py t0090_morphology_generator_diversity_test` passes.
* `verify_task_file.py t0090_morphology_generator_diversity_test` passes.
* `verify_research_code.py`, `verify_plan.py`, `verify_assets.py` pass.
* The answer asset passes `verify_answer.py`.

## Cross-References

* **t0089_brainstorm_results_18** — commissioning brainstorm session.
* **t0086_robustness_cluster_bio_comparison**, **t0088_recluster_marginals_and_vm_motifs** —
  biological-plausibility framework re-used for cluster scoring.
* **t0024_port_de_rosenroll_2026_dsgc** — Bed B reference for reproducibility check.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**, **t0083_bedb_v3_extend_nsga2_gen8plus** —
  source of the 5 t0083 Pareto cells used in Phase F and the cluster representatives used in
  Phase G.3.
* Source suggestions covered: **S-0088-02** (Phase G.1), **S-0086-02** (Phase G.2),
  **S-0088-01** (Phase G.3).

</details>
