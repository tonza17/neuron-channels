# Libraries: `synaptic-integration`

2 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>Minimal DSGC with Scalar gabaMOD</strong>
(<code>minimal_dsgc_scalar_gaba</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `minimal_dsgc_scalar_gaba` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0052_minimal_dsgc_scalar_gaba\code\constants.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\paths.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\swc_io.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\neuron_bootstrap.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\cell.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\placement.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\synapses.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\trial.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\run_tuning_curve.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\render_figures.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\compute_metrics.py`, `tasks\t0052_minimal_dsgc_scalar_gaba\code\metrics_extra.py` |
| **Dependencies** | neuron, numpy, matplotlib, pandas, tqdm |
| **Date created** | 2026-04-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Documentation** | [`description.md`](../../../tasks\t0052_minimal_dsgc_scalar_gaba\assets\library\minimal_dsgc_scalar_gaba\description.md) |

**Entry points:**

* `build_dsgc_from_swc` (function) — Parse a calibrated SWC, collapse the soma into one
  Section, build one h.Section per non-soma compartment, attach a synthetic axon initial
  segment, and return a CellHandles dataclass.
* `sample_dendritic_locations` (function) — Sample N dendritic locations uniformly along total
  dendritic length using numpy.random.default_rng(seed).
* `build_ei_pairs` (function) — Construct one AMPA + GABA Exp2Syn pair per Location, each
  driven by a single-event NetStim+NetCon.
* `schedule_ei_onsets` (function) — Per-trial scheduler: set NetStim.start times from the
  bar-leading-edge crossing geometry and apply gabaMOD scaling to GABA NetCon weights.
* `gaba_mod` (function) — Scalar gabaMOD multiplier: returns 0.33 at preferred direction
  (theta=0) and 0.99 at null direction (theta=180).
* `TrialMode` (class) — StrEnum with members FULL, AMPA_ONLY, GABA_ONLY for selecting which
  synaptic drive is active.
* `run_one_trial` (function) — Run one trial: schedule onsets, apply mode-specific weight
  overrides, finitialize+continuerun, return TrialResult with V(t), spike times, and synapse
  onset times.
* `run_full_sweep` (function) — End-to-end 12 directions x 10 trials x 3 modes = 360-trial
  sweep with dry-run validation gate; writes per-mode tuning-curve / spike-time /
  voltage-trace CSVs and an activation-time CSV.
* `compute_vector_sum_dsi` (function) — Vector-sum DSI from the per-angle mean firing rates:
  |sum r_k * exp(i theta_k)| / sum r_k.
* `compute_preferred_direction_deg` (function) — Preferred direction in degrees from the
  complex sum of rate-weighted unit vectors.
* `compute_metrics_main` (script) — Compute per-mode metrics (DSI, HWHM, reliability,
  vector-sum DSI, preferred direction, IPSP ratio) and write metrics.json +
  derived_quantities.json with a hard IPSP-ratio sanity check.
* `render_figures_main` (script) — Render all per-direction figures (soma V, EPSP, IPSP, PSTH,
  activation histograms) plus polar and Cartesian tuning curves.

Pure-Python NEURON library for a minimal direction-selective ganglion cell with 100 co-located
E+I synapses, scalar gabaMOD inhibition, and a 12-direction moving-bar trial runner.

</details>

<details>
<summary>📦 <strong>ModelDB 189347 DSGC (exact reproduction)</strong>
(<code>modeldb_189347_dsgc_exact</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `modeldb_189347_dsgc_exact` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\paths.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\constants.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\neuron_bootstrap.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\build_cell.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\run_simplerun.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\run_all_figures.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\compute_metrics.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\render_figures.py`, `tasks\t0046_reproduce_poleg_polsky_2016_exact\code\download_supplementary.py` |
| **Dependencies** | matplotlib, numpy, tqdm |
| **Date created** | 2026-04-24 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Documentation** | [`description.md`](../../../tasks\t0046_reproduce_poleg_polsky_2016_exact\assets\library\modeldb_189347_dsgc_exact\description.md) |

**Entry points:**

* `build_dsgc` (function) — Build the ModelDB 189347 DSGC cell (350 dend sections, 282 ON
  synapses) under NEURON 8.2.7.
* `run_one_trial` (function) — Run a single drifting-bar trial via h.simplerun() with explicit
  exptype, direction, b2gnmda, and noise overrides; returns peak PSP, baseline mean, and spike
  times.
* `ensure_neuron_importable` (function) — NEURON-on-Windows bootstrap: sets NEURONHOME,
  registers DLL dirs, inserts the bindings on sys.path.
* `main` (script) — Runs every Poleg-Polsky 2016 figure reproduction sweep (Fig 1-8) and
  writes per-figure CSVs under results/data/.
* `main` (script) — Aggregates the per-figure CSVs into the explicit multi-variant
  results/metrics.json.
* `main` (script) — Renders results/images/fig{1..8}_*.png from the per-figure CSVs with
  paper-vs-reproduction overlays.

From-scratch port of ModelDB accession 189347 (Poleg-Polsky and Diamond 2016) reproducing
every paper figure on its own metrics: PSP amplitudes, slope angles, ROC AUC, Figure 8 spikes;
pinned to commit 87d669dcef18e9966e29c88520ede78bc16d36ff.

</details>
