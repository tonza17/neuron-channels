# Libraries: `retinal-ganglion-cell`

2 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>ModelDB 189347 DSGC Port</strong>
(<code>modeldb_189347_dsgc</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `modeldb_189347_dsgc` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0008_port_modeldb_189347\code\build_cell.py`, `tasks\t0008_port_modeldb_189347\code\constants.py`, `tasks\t0008_port_modeldb_189347\code\paths.py`, `tasks\t0008_port_modeldb_189347\code\run_tuning_curve.py`, `tasks\t0008_port_modeldb_189347\code\score_envelope.py`, `tasks\t0008_port_modeldb_189347\code\report_morphology.py`, `tasks\t0008_port_modeldb_189347\code\swc_io.py`, `tasks\t0008_port_modeldb_189347\code\run_nrnivmodl.cmd` |
| **Dependencies** | neuron, tqdm |
| **Date created** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Documentation** | [`description.md`](../../../tasks\t0008_port_modeldb_189347\assets\library\modeldb_189347_dsgc\description.md) |

**Entry points:**

* `build_dsgc` (function) — Load the compiled nrnmech.dll, source RGCmodel.hoc and the
  GUI-free dsgc_model.hoc, and return a fully-initialised NEURON h-handle with RGC.numsyn
  point processes placed on ON dendrites.
* `run_one_trial` (function) — Apply per-trial seed and angle, rotate BIP synapse coords,
  rerun placeBIP(), finitialize and continuerun to tstop, and return the soma firing rate in
  Hz.
* `main` (script) — Sweep 12 angles x 20 trials on the bundled DSGC and emit a
  canonical-schema tuning curve CSV consumable by tuning_curve_loss.
* `main` (script) — Score the emitted tuning curve against the t0004 target via
  tuning_curve_loss and write results/metrics.json plus data/score_report.json.
* `main` (script) — Compare the bundled Poleg-Polsky morphology with the calibrated t0009 SWC
  and write data/morphology_swap_report.md.

Python-driven port of ModelDB 189347 (Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC) with a
NEURON/HOC back-end, 12-angle drifting-bar tuning-curve runner, and t0012-based envelope
scoring.

</details>

<details>
<summary>📦 <strong>Tuning Curve Loss</strong> (<code>tuning_curve_loss</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `tuning_curve_loss` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\__init__.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\paths.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\loader.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\metrics.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\envelope.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\weights.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\scoring.py`, `tasks\t0012_tuning_curve_scoring_loss_library\code\tuning_curve_loss\cli.py` |
| **Dependencies** | numpy, pandas |
| **Date created** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Documentation** | [`description.md`](../../../tasks\t0012_tuning_curve_scoring_loss_library\assets\library\tuning_curve_loss\description.md) |

**Entry points:**

* `score` (function) — Score a simulated tuning-curve CSV against the target CSV and return a
  ScoreReport with loss, residuals, and envelope pass/fail.
* `score_curves` (function) — Score two pre-loaded TuningCurve objects; supports custom
  weights and weights loaded from a JSON file.
* `ScoreReport` (class) — Frozen dataclass carrying loss_scalar, residuals,
  normalized_residuals, per_target_pass, passes_envelope, candidate_metrics, target_metrics,
  weights_used, and rmse_vs_target.
* `load_tuning_curve` (function) — Load a 12-angle tuning curve from CSV in canonical,
  t0004-trials, or t0004-mean schema.
* `compute_dsi` (function) — Direction Selectivity Index = (peak - null) / (peak + null);
  returns 0.0 for a zero-sum denominator.
* `compute_peak_hz` (function) — Firing rate (Hz) at the preferred direction.
* `compute_null_hz` (function) — Firing rate (Hz) at the null direction (minimum of the
  curve).
* `compute_hwhm_deg` (function) — Half-width at half-maximum in degrees via linear
  interpolation, rotated so the peak is at the grid midpoint.
* `compute_reliability` (function) — Split-half Pearson correlation over even/odd trials;
  returns None when trials are absent or variance is zero.
* `check_envelope` (function) — Evaluate a curve against the four concurrent envelope gates
  and return per-target pass flags.
* `validate_weights` (function) — Validate a weight mapping (correct keys, non-negative,
  non-zero sum).
* `load_weights_from_json` (function) — Load a weights mapping from a JSON file and validate
  it.
* `tuning_curve_loss.cli` (script) — Command-line entry point: score a simulated CSV against
  the t0004 target (or a supplied target) with optional custom weights and JSON output.

Canonical scorer for 12-angle direction-selectivity tuning curves against the t0004 target,
returning a weighted scalar loss over DSI, preferred-peak, null, and HWHM residuals plus
per-metric diagnostics and a Poleg-Polsky envelope pass/fail.

</details>
