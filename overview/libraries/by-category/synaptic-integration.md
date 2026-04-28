# Libraries: `synaptic-integration`

5 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>Minimal DSGC AMPA + Mg-Block NMDA + Scalar gabaMOD</strong>
(<code>minimal_dsgc_mg_block_nmda</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `minimal_dsgc_mg_block_nmda` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0055_nmda_mg_block_dsi_recovery\code\constants.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\paths.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\swc_io.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\neuron_bootstrap.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\cell.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\placement.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\synapses.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\trial.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\run_tuning_curve.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\render_figures.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\compute_metrics.py`, `tasks\t0055_nmda_mg_block_dsi_recovery\code\metrics_extra.py` |
| **Dependencies** | neuron, numpy, matplotlib, pandas, tqdm |
| **Date created** | 2026-04-28 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Documentation** | [`description.md`](../../../tasks\t0055_nmda_mg_block_dsi_recovery\assets\library\minimal_dsgc_mg_block_nmda\description.md) |

**Entry points:**

* `build_dsgc_from_swc` (function) — Parse a calibrated SWC, collapse the soma into one
  Section, build one h.Section per non-soma compartment, attach a synthetic axon initial
  segment, and return a CellHandles dataclass.
* `sample_dendritic_locations` (function) — Sample N dendritic locations uniformly along total
  dendritic length using numpy.random.default_rng(seed).
* `build_ei_pairs` (function) — Construct one AMPA Exp2Syn + NMDA_MgBlock + GABA Exp2Syn
  triplet per Location; AMPA and NMDA share a single NetStim driven by two NetCons.
* `schedule_ei_onsets` (function) — Per-trial scheduler: set NetStim.start times from
  bar-leading-edge geometry; write per-trial AMPA, NMDA (gnmda_ns x 1e-3), and GABA NetCon
  weights.
* `gaba_mod` (function) — Scalar gabaMOD multiplier: returns 0.33 at preferred direction
  (theta=0) and 0.99 at null direction (theta=180).
* `TrialMode` (class) — StrEnum with members FULL, E_ONLY, GABA_ONLY for selecting which
  synaptic drive is active.
* `run_one_trial` (function) — Run one trial at a given (mode, angle, gnmda_ns); returns
  TrialResult carrying V(t), spike times, synapse onset times, and gnmda_ns.
* `run_full_sweep` (function) — End-to-end 4 gNMDA x 12 directions x 10 trials x 3 modes =
  1,440-trial sweep with dry-run validation gate; writes per-mode tuning-curve / spike-time /
  voltage-trace CSVs and an activation-time CSV.
* `ensure_nmda_mg_block_compiled` (function) — Build code/mod/NMDA_MgBlock.mod into
  nrnmech.dll via run_nrnivmodl.cmd if needed, then h.nrn_load_dll the result so
  h.NMDA_MgBlock becomes available.
* `compute_vector_sum_dsi` (function) — Vector-sum DSI from per-angle mean firing rates: |sum
  r_k * exp(i theta_k)| / sum r_k.
* `compute_preferred_direction_deg` (function) — Preferred direction in degrees from the
  complex sum of rate-weighted unit vectors.
* `compute_metrics_main` (script) — Compute 12-variant metrics (one per gNMDA x mode) with the
  gNMDA = 0 cross-task regression hard-fail gate against t0054, the IPSP-conductance-ratio
  sanity check, and the S-0054-01 PASS/FAIL evaluation.
* `render_figures_main` (script) — Render all per-direction figures (soma V, EPSP, IPSP, PSTH,
  activation histogram) for each gNMDA, plus polar/Cartesian overviews and four sweep-summary
  plots including the Mg-block g(v) sanity curve.

NEURON library for a minimal DSGC with co-located AMPA Exp2Syn and a custom Jahr-Stevens
Mg-block NMDA POINT_PROCESS, scalar gabaMOD inhibition, and a 12-direction x 4-gNMDA x 3-mode
moving-bar sweep harness.

</details>

<details>
<summary>📦 <strong>Minimal DSGC AMPA + NMDA Scalar gabaMOD</strong>
(<code>minimal_dsgc_ampa_nmda_scalar_gaba</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `minimal_dsgc_ampa_nmda_scalar_gaba` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\constants.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\paths.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\swc_io.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\neuron_bootstrap.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\cell.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\placement.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\synapses.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\trial.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\run_tuning_curve.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\render_figures.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\compute_metrics.py`, `tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\code\metrics_extra.py` |
| **Dependencies** | neuron, numpy, matplotlib, pandas, tqdm |
| **Date created** | 2026-04-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Documentation** | [`description.md`](../../../tasks\t0054_minimal_dsgc_ampa_nmda_scalar_gaba\assets\library\minimal_dsgc_ampa_nmda_scalar_gaba\description.md) |

**Entry points:**

* `build_dsgc_from_swc` (function) — Parse a calibrated SWC, collapse the soma into one
  Section, build one h.Section per non-soma compartment, attach a synthetic axon initial
  segment, and return a CellHandles dataclass.
* `sample_dendritic_locations` (function) — Sample N dendritic locations uniformly along total
  dendritic length using numpy.random.default_rng(seed).
* `build_ei_pairs` (function) — Construct one AMPA + NMDA + GABA Exp2Syn triplet per Location;
  AMPA and NMDA share a single NetStim driven by two NetCons.
* `schedule_ei_onsets` (function) — Per-trial scheduler: set NetStim.start times from
  bar-leading-edge geometry; write per-trial AMPA, NMDA (gnmda_ns × 1e-3), and GABA NetCon
  weights.
* `gaba_mod` (function) — Scalar gabaMOD multiplier: returns 0.33 at preferred direction
  (theta=0) and 0.99 at null direction (theta=180).
* `TrialMode` (class) — StrEnum with members FULL, E_ONLY, GABA_ONLY for selecting which
  synaptic drive is active. Replaces t0052's AMPA_ONLY with E_ONLY (AMPA + NMDA active, GABA
  zeroed).
* `run_one_trial` (function) — Run one trial at a given (mode, angle, gnmda_ns); returns
  TrialResult carrying V(t), spike times, synapse onset times, and gnmda_ns.
* `run_full_sweep` (function) — End-to-end 4 gNMDA × 12 directions × 10 trials × 3 modes =
  1,440-trial sweep with dry-run validation gate; writes per-mode tuning-curve / spike-time /
  voltage-trace CSVs and an activation-time CSV.
* `compute_vector_sum_dsi` (function) — Vector-sum DSI from per-angle mean firing rates: |sum
  r_k * exp(i theta_k)| / sum r_k.
* `compute_preferred_direction_deg` (function) — Preferred direction in degrees from the
  complex sum of rate-weighted unit vectors.
* `compute_metrics_main` (script) — Compute 12-variant metrics (one per gNMDA × mode) with the
  gNMDA = 0 regression hard-fail gate against t0052 and the IPSP-conductance-ratio sanity
  check.
* `render_figures_main` (script) — Render all per-direction figures (soma V, EPSP, IPSP, PSTH,
  activation histogram) for each gNMDA, plus 8 polar/Cartesian overviews and 3 sweep-summary
  plots.

Pure-Python NEURON library for a minimal DSGC with co-located AMPA + NMDA Exp2Syn excitation,
scalar gabaMOD inhibition, and a 12-direction × 4-gNMDA × 3-mode moving-bar sweep harness.

</details>

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
<summary>📦 <strong>Minimal DSGC with Spatial Centripetal-Gating GABA</strong>
(<code>minimal_dsgc_spatial_gaba</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `minimal_dsgc_spatial_gaba` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0053_minimal_dsgc_spatial_gaba\code\constants.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\paths.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\swc_io.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\neuron_bootstrap.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\cell.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\placement.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\synapses.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\trial.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\run_tuning_curve.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\render_figures.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\compute_metrics.py`, `tasks\t0053_minimal_dsgc_spatial_gaba\code\metrics_extra.py` |
| **Dependencies** | neuron, numpy, matplotlib, pandas, tqdm |
| **Date created** | 2026-04-25 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Documentation** | [`description.md`](../../../tasks\t0053_minimal_dsgc_spatial_gaba\assets\library\minimal_dsgc_spatial_gaba\description.md) |

**Entry points:**

* `build_dsgc_from_swc` (function) — Parse a calibrated SWC, collapse the soma into one
  Section, build one h.Section per non-soma compartment, attach a synthetic axon initial
  segment, and return a CellHandles dataclass that includes soma_origin_um for the spatial
  driver.
* `sample_dendritic_locations` (function) — Sample N dendritic locations uniformly along total
  dendritic length using numpy.random.default_rng(seed); seed=0 reproduces t0052's placement
  bit-for-bit.
* `build_ei_pairs` (function) — Construct one AMPA + GABA Exp2Syn pair per Location; each pair
  carries theta_centrifugal_rad = atan2(y - y_soma, x - x_soma) precomputed from
  soma_origin_um.
* `schedule_ei_onsets` (function) — Per-trial scheduler: set AMPA NetStim.start at
  bar-arrival; for each I synapse evaluate i_synapse_fires(theta_stim, theta_centrifugal);
  when fired set GABA weight to 2 nS, otherwise zero. Returns ScheduleResult with
  onset_times_ms and i_fired_mask.
* `i_synapse_fires` (function) — Pure boolean predicate: returns cos(radians(theta_stim_deg -
  theta_centrifugal_deg)) < 0 (strict; perpendicular does not fire).
* `ScheduleResult` (class) — Frozen dataclass returned by schedule_ei_onsets, with
  onset_times_ms: list[float] and i_fired_mask: list[bool] aligned with the pair list.
* `TrialMode` (class) — StrEnum with members FULL, AMPA_ONLY, GABA_ONLY for selecting which
  synaptic drive is active.
* `run_one_trial` (function) — Run one trial: schedule onsets via the spatial gate, apply
  mode-specific weight overrides, finitialize+continuerun, return TrialResult with V(t), spike
  times, synapse onset times, i_fired_mask, and i_active_fraction.
* `run_full_sweep` (function) — End-to-end 12 directions x 10 trials x 3 modes = 360-trial
  sweep with dry-run validation gate; writes per-mode tuning-curve / spike-time /
  voltage-trace CSVs, an activation-time CSV with is_fired column, and an
  active_fraction_per_direction CSV.
* `compute_vector_sum_dsi` (function) — Vector-sum DSI from the per-angle mean firing rates:
  |sum r_k * exp(i theta_k)| / sum r_k.
* `compute_preferred_direction_deg` (function) — Preferred direction in degrees from the
  complex sum of rate-weighted unit vectors.
* `render_active_fraction_polar` (function) — Render the per-direction active-fraction polar
  plot (closed polygon with reference circle at 0.5).
* `compute_metrics_main` (script) — Compute per-mode metrics (DSI, HWHM, reliability) and
  write metrics.json + derived_quantities.json with a soft active-fraction sanity check (mean
  in [0.4, 0.6]).
* `render_figures_main` (script) — Render all per-direction figures (soma V, EPSP, IPSP, PSTH,
  activation histograms) plus polar / Cartesian tuning curves, raster+PSTH per direction, and
  the active-fraction polar plot.

Pure-Python NEURON library for a minimal direction-selective ganglion cell with 100 co-located
E+I synapses where each I synapse fires only when the bar moves with a centripetal component
(cos(theta_stim - theta_centrifugal) < 0); the spatial-asymmetry sibling of t0052.

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
