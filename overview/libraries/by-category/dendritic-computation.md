# Libraries: `dendritic-computation`

2 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>de Rosenroll 2026 DSGC</strong>
(<code>de_rosenroll_2026_dsgc</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `de_rosenroll_2026_dsgc` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0024_port_de_rosenroll_2026_dsgc\code\ar2_noise.py`, `tasks\t0024_port_de_rosenroll_2026_dsgc\code\build_cell.py`, `tasks\t0024_port_de_rosenroll_2026_dsgc\code\constants.py`, `tasks\t0024_port_de_rosenroll_2026_dsgc\code\paths.py`, `tasks\t0024_port_de_rosenroll_2026_dsgc\code\plot_tuning_curves.py`, `tasks\t0024_port_de_rosenroll_2026_dsgc\code\run_tuning_curve.py`, `tasks\t0024_port_de_rosenroll_2026_dsgc\code\score_envelope.py` |
| **Dependencies** | neuron, numpy, pandas |
| **Date created** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Documentation** | [`description.md`](../../../tasks\t0024_port_de_rosenroll_2026_dsgc\assets\library\de_rosenroll_2026_dsgc\description.md) |

**Entry points:**

* `generate_ar2_batch` (function) — Vectorised AR(2) release-rate noise generator with
  configurable cross-channel correlation rho (0.6 reproduces the paper's correlated condition;
  0.0 the AMB/decorrelated control).
* `build_dsgc_cell` (function) — Bootstraps NEURON 8.2.7, loads the vendored nrnmech.dll,
  sources RGCmodelGD.hoc and returns a configured DSGC cell with its
  primary/non-terminal/terminal dendrites enumerated and plan-pinned channel densities
  applied.
* `run_tuning_curve` (script) — CLI driver for the four-condition moving-bar sweep
  (8-direction and 12-angle x {correlated, uncorrelated}); writes a trial-level CSV per
  condition under data/.
* `score_envelope` (script) — Scores the 12-angle correlated tuning curve against the t0004
  target envelope using the t0012 tuning_curve_loss library, evaluates the REQ-5 port-fidelity
  gate, and writes data/score_report.json + results/metrics.json.
* `plot_tuning_curves` (script) — Renders polar and Cartesian PNG plots from the four sweep
  CSVs into results/images/ (plan step 14).

Port of the de Rosenroll et al. 2026 direction-selective retinal ganglion cell (DSGC) model
into this project: NEURON HOC morphology template, compiled MOD mechanisms, and Python driver
that reproduces the correlated-vs-AMB tuning-curve contrast.

</details>

<details>
<summary>📦 <strong>Procedural DSGC Morphology Generator</strong>
(<code>procedural_dsgc_morphology_generator</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `procedural_dsgc_morphology_generator` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0090_morphology_generator_diversity_test\code\morphology_params.py`, `tasks\t0090_morphology_generator_diversity_test\code\generator.py`, `tasks\t0090_morphology_generator_diversity_test\code\verification.py`, `tasks\t0090_morphology_generator_diversity_test\code\constants.py`, `tasks\t0090_morphology_generator_diversity_test\code\paths.py`, `tasks\t0090_morphology_generator_diversity_test\code\load_default_params.py` |
| **Dependencies** | numpy, scipy, neuron, matplotlib |
| **Date created** | 2026-05-07 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |
| **Created by** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Documentation** | [`description.md`](../../../tasks\t0090_morphology_generator_diversity_test\assets\library\procedural_dsgc_morphology_generator\description.md) |

**Entry points:**

* `generate_morphology` (function) — Build a procedural DSGC cell from MorphologyParams +
  morph_seed; returns a MorphologyResult duck-typed as t0080 DSGCCellWithAIS.
* `MorphologyParams` (class) — Frozen dataclass with 14 typed fields (3 ints + 11 floats)
  describing one morphology spec; supports to_dict / from_dict serialisation.
* `MorphologyResult` (class) — Frozen dataclass mirroring the t0080 DSGCCellWithAIS interface:
  soma, all_dends, primary_dends, non_terminal_dends, terminal_dends, ais_proximal, ais_distal
  plus stability_flag, morphometric_summary, connectivity, section_endpoints_xy.
* `MorphometricSummary` (class) — Frozen dataclass with 6 morphometric features
  (total_dendritic_length_um, branch_count, max_strahler_depth, electrotonic_length_lambda,
  soma_displacement_um, field_major_axis_length_um).
* `StabilityKind` (class) — Enum classifying simulation stability outcomes (STABLE,
  NAN_VOLTAGE, DIVERGED, DISCONNECTED).
* `verify_one_morphology` (function) — Build, stability-check, and 8-direction-protocol one
  morphology under a 54-d ParameterVector; returns a VerificationResult.
* `BEDB_BASE_POINT` (class) — Constant dict mapping each of the 14 parameter names to its
  BedB-equivalent (de Rosenroll 2026) value.
* `PARAM_BOUNDS` (class) — Constant dict mapping each parameter name to its (lo, hi) bounds
  for LHS or NSGA-II sampling.

Pure-Python deterministic procedural DSGC morphology generator with 14 explicit knobs (5
topology + 4 asymmetry + 3 geometry + 2 stochastic), structurally compatible with the t0080
apply_parameter_vector harness.

</details>
