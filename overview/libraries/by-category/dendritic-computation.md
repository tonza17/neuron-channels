# Libraries: `dendritic-computation`

1 librar(y/ies).

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
