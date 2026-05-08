# Libraries: `compartmental-modeling`

14 librar(y/ies).

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
<summary>📦 <strong>De Rosenroll 2026 DSGC with AIS</strong>
(<code>de_rosenroll_2026_dsgc_ais</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `de_rosenroll_2026_dsgc_ais` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\build_cell_ais.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\extend_with_ais.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\apply_params.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\constants.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\paths.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\bootstrap.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\parametric_placer.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\trial_helpers.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\trial_driver.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\recorder.py`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\skahpt78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\nav16t78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\napt78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\nart78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\kdrt78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\kv3t78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\kv4t78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\kv7t78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\iht78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\calt78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\catt78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\bkt78.mod`, `tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\code\mods\skt78.mod` |
| **Dependencies** | neuron, numpy, botorch, torch, gpytorch |
| **Date created** | 2026-05-03 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Documentation** | [`description.md`](../../../tasks\t0078_bedb_mobo_v2_ais_tiered_ahp\assets\library\de_rosenroll_2026_dsgc_ais\description.md) |

**Entry points:**

* `build_dsgc_cell_with_ais` (function) — Build a Bed B DSGC cell and attach a two-subsegment
  AIS (proximal + distal). Returns DSGCCellWithAIS dataclass.
* `DSGCCellWithAIS` (class) — Dataclass exposing every field of the t0024 DSGCCell plus
  ais_proximal and ais_distal NEURON Section handles.
* `apply_parameter_vector` (function) — Write a 49-d ParameterVector to a Bed B cell with AIS:
  tier-stratified channel densities, uniform-channel densities, slow-AHP gbar +
  tau_ca_multiplier, AIS geometry, and passive properties.
* `extend_with_ais` (function) — Build the two-subsegment AIS (proximal + distal) sections,
  attach to soma(1), insert HHst basal Na+K. Permitted SUFFIXes (nav16t78/kv3t78/kv7t78) are
  inserted later by apply_parameter_vector.
* `ParameterVector` (class) — Frozen 49-d candidate dataclass: 25 tier-stratified densities +
  7 uniform-channel densities + 2 slow-AHP params + 13 synaptic placement + 2 AIS geometry.

AIS-augmented Bed B DSGC substrate: forks the de Rosenroll 2026 cell builder, attaches a
two-subsegment AIS (proximal HHst stand-in for Nav1.1/Nav1.2, distal Nav1.6+Kv3+Kv7), exposes
49-d MOBO parameter space with tier-stratified channel densities and SK_E2 slow-AHP.

</details>

<details>
<summary>📦 <strong>DSGC Active Channel Pack</strong>
(<code>dsgc_active_channel_pack</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `dsgc_active_channel_pack` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0074_channel_tuning_width_bed_a\code\mods\nav16t74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\napt74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\nart74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\kv3t74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\kv4t74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\bk74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\sk74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\kv7t74.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\cadecay.mod`, `tasks\t0074_channel_tuning_width_bed_a\code\mods\mod_func.c`, `tasks\t0074_channel_tuning_width_bed_a\code\dsgc_model_t74.hoc`, `tasks\t0074_channel_tuning_width_bed_a\code\run_nrnivmodl.cmd` |
| **Dependencies** | — |
| **Date created** | 2026-05-02 |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Documentation** | [`description.md`](../../../tasks\t0074_channel_tuning_width_bed_a\assets\library\dsgc_active_channel_pack\description.md) |

**Entry points:**

* `nav16t74` (class) — Nav1.6 fast transient sodium NEURON SUFFIX (NONSPECIFIC_CURRENT).
  V_half_act ~ -43 mV, V_half_inact ~ -65 mV. Carter-Bean 2009.
* `napt74` (class) — Persistent sodium NEURON SUFFIX (NONSPECIFIC_CURRENT). Single-gate m^1,
  V_half ~ -50 mV. Magistretti-Alonso 1999.
* `nart74` (class) — Resurgent sodium NEURON SUFFIX (NONSPECIFIC_CURRENT). m^3*h*s with slow s
  gate reactivating around -50 mV. Khaliq 2003.
* `kv3t74` (class) — Kv3 fast delayed-rectifier potassium NEURON SUFFIX (NONSPECIFIC_CURRENT).
  m^4 kinetics, V_half ~ -15 mV. Erisir 1999.
* `kv4t74` (class) — Kv4 / IA transient A-type potassium NEURON SUFFIX (NONSPECIFIC_CURRENT).
  m^4*h, V_half_act ~ -50 mV. Hoffman 1997.
* `bk74` (class) — BK / KCa1.1 voltage- and Ca-dependent K channel NEURON SUFFIX (USEION ca
  READ cai; NONSPECIFIC_CURRENT). V_half ~ -28 mV, K_d = 0.18 uM (Hill exponent 1), Q10 = 2.3.
  Mainen-Sejnowski 1996 (ModelDB 2488), DOI 10.1038/382363a0.
* `sk74` (class) — SK / KCa2 voltage-independent Ca-driven K channel NEURON SUFFIX (USEION ca
  READ cai; NONSPECIFIC_CURRENT). EC50 = 0.43 uM, Hill = 4.8, tau = 1 ms. Hay 2011 (ModelDB
  139653, SK_E2.mod), DOI 10.1371/journal.pcbi.1002107.
* `kv7t74` (class) — Kv7 / M-current NEURON SUFFIX (NONSPECIFIC_CURRENT). Adams 1982
  alpha/beta formalism, V_half ~ -35 mV, Q10 = 2.3. Hay 2011 (ModelDB 139653, Im.mod), DOI
  10.1371/journal.pcbi.1002107.
* `cad` (class) — Single-shell calcium pool. depth = 0.1 um, taur = 5 ms, cainf = 2e-4 mM.
  Destexhe 1995 formalism. Reused verbatim from t0024 de_rosenroll_2026_dsgc library.
* `init_active` (function) — Forked HOC procedure that overrides Bed A's init_active to
  un-zero RGCcaT and RGCcaL (set to 0.0001 S/cm^2) so the cad calcium pool has a current
  source. Source after build_dsgc() and before init_active is called per trial.
* `run_nrnivmodl` (script) — Windows CMD script that compiles the 9 MOD files in code/mods/
  into code/build/nrnmech.dll using NEURON's canonical nrnivmodl wrapper.

Vendored 8-channel pack (Nav1.6, NaP, NaR, Kv3, Kv4, BK, SK, Kv7) plus cad calcium pool plus a
forked Bed A HOC with un-zeroed CaT/CaL, for active-conductance sweeps on the deposited
Poleg-Polsky DSGC (t0008 modeldb_189347_dsgc).

</details>

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
<summary>📦 <strong>Minimal DSGC with Bar-Arrival-Locked Tonic GABA + AMPA
Sweep</strong> (<code>minimal_dsgc_bar_locked_gaba_ampa_sweep</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `minimal_dsgc_bar_locked_gaba_ampa_sweep` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\constants.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\paths.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\swc_io.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\neuron_bootstrap.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\cell.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\placement.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\synapses.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\trial.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\run_tuning_curve.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\render_figures.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\compute_metrics.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\metrics_extra.py`, `tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\code\mod\GabaTonic.mod` |
| **Dependencies** | neuron, numpy, matplotlib, pandas, tqdm |
| **Date created** | 2026-04-29 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Documentation** | [`description.md`](../../../tasks\t0059_bar_locked_gaba_ampa_sweep_t0057\assets\library\minimal_dsgc_bar_locked_gaba_ampa_sweep\description.md) |

**Entry points:**

* `AMPA_PEAK_NS_VALUES` (function) — Public 5-tuple of swept per-synapse AMPA peak conductance
  values in nS (0.5, 1.0, 2.0, 3.0, 4.0). The outer loop in run_full_sweep iterates over
  these; threaded as ``gampa_ns: float`` through schedule_ei_onsets and run_one_trial.
* `GABA_BASE_NS_VALUES` (function) — Public 5-tuple of swept per-synapse peak GABA conductance
  values in nS (0.1, 0.2, 0.5, 1.0, 2.0). The inner loop in run_full_sweep iterates over
  these.
* `WINDOW_MS` (function) — Public per-synapse tonic-window width in ms (default 200). Active
  GABA synapses receive g = gaba_base_ns * 1e-3 (uS) over [t_on_i, t_on_i + WINDOW_MS] where
  t_on_i is the per-synapse bar-arrival time.
* `TrialMode` (class) — StrEnum with members FULL, EPSP_PASSIVE, IPSP_PASSIVE. EPSP_PASSIVE /
  IPSP_PASSIVE save-and-zero HH gnabar / gkbar on soma + AIS so the soma trace is the pure
  synaptic envelope (no spikes).
* `gaba_tonic` (class) — NEURON POINT_PROCESS registered as h.gaba_tonic after
  ensure_gaba_tonic_compiled() runs. RANGE attributes: g (uS), e (mV), t_on (ms), t_off (ms),
  ramp_ms (ms; default 1). Conductance envelope is g * envelope(t) where envelope is 0 outside
  [t_on, t_off], a 1 ms cosine ramp at each edge, and 1.0 in the middle. NONSPECIFIC_CURRENT i
  = envelope * g * (v - e). No NET_RECEIVE block; conductance is set by direct attribute write
  per trial. Unchanged from t0057.
* `ensure_gaba_tonic_compiled` (function) — Build code/mod/nrnmech.dll from
  code/mod/GabaTonic.mod via the run_nrnivmodl.cmd shim if missing, then load the DLL via
  h.nrn_load_dll so h.gaba_tonic becomes available. Idempotent. Must be called AFTER
  ensure_neuron_importable + load_stdrun and BEFORE any h.gaba_tonic(seg) construction.
* `build_dsgc_from_swc` (function) — Parse a calibrated SWC, collapse the 19 soma rows into
  one Section, build one h.Section per non-soma compartment, attach a synthetic axon initial
  segment, and return a CellHandles dataclass. HH only on soma + AIS; pas everywhere else.
* `sample_dendritic_locations` (function) — Sample N dendritic locations uniformly along total
  dendritic length using numpy.random.default_rng(seed); seed=0 reproduces t0052 / t0053 /
  t0057 placement bit-for-bit.
* `build_ei_pairs` (function) — Construct one AMPA Exp2Syn + tonic gaba_tonic instance per
  Location; each pair carries theta_centrifugal_rad. AMPA NetCon weight is set per trial by
  schedule_ei_onsets (was hard-coded at AMPA_PEAK_NS * 1e-3 in t0057).
* `i_synapse_fires` (function) — Pure boolean predicate: returns cos(radians(theta_stim_deg -
  theta_centrifugal_deg)) < 0 (strict; perpendicular does not fire). Bit-identical to t0053 /
  t0057.
* `schedule_ei_onsets` (function) — Per-trial scheduler: set AMPA NetStim.start AND
  ampa_netcon.weight[0] = gampa_ns * 1e-3 (REQ-7); for each I synapse evaluate
  i_synapse_fires; when fired set pair.gaba_syn.g = gaba_base_ns * 1e-3 (uS) and (t_on, t_off)
  = (onset_ms, onset_ms + WINDOW_MS) per REQ-1, otherwise zero g and collapse the window.
  Returns ScheduleResult with onset_times_ms and i_fired_mask.
* `ScheduleResult` (class) — Frozen dataclass returned by schedule_ei_onsets, with
  onset_times_ms: list[float] and i_fired_mask: list[bool] aligned with the pair list.
* `HhConductanceSnapshot` (class) — Frozen dataclass of per-segment HH gnabar / gkbar values
  on soma + AIS, captured by _save_and_zero_hh and consumed by _restore_hh.
* `_save_and_zero_hh` (function) — Save HH gnabar / gkbar on every segment of soma and
  axon_initial_segment, then zero them. Returns an HhConductanceSnapshot. Dendrites are NOT
  touched (no hh mechanism). Used by run_one_trial for EPSP_PASSIVE / IPSP_PASSIVE modes.
* `_restore_hh` (function) — Restore HH gnabar / gkbar from a snapshot. Always called from a
  try/finally inside run_one_trial so HH is restored even if NEURON raises.
* `run_one_trial` (function) — Run one trial: schedule onsets via the spatial gate at the
  supplied (gampa_ns, gaba_base_ns), apply mode-specific weight overrides, save-and-zero HH
  for passive modes (try/finally), finitialize + continuerun, return TrialResult with V(t),
  spike times, i_fired_mask, i_active_fraction, gampa_ns and gaba_base_ns.
* `run_full_sweep` (function) — End-to-end 5 (gampa) x 5 (gaba) x 12 directions x 10 trials x
  3 modes = 9,000-trial sweep with dry-run validation gate (including the bar-locked IPSP
  centre-of-mass shift check). Writes per-mode tuning-curve / spike-time / voltage-trace CSVs
  each carrying leading (gampa_ns, gaba_base_ns) columns, active_fraction_per_direction CSV,
  placement_seed0.json, and wallclock.json. Activation-time CSV is dropped per REQ-5.
* `compute_vector_sum_dsi` (function) — Vector-sum DSI from the per-angle mean firing rates:
  |sum r_k * exp(i theta_k)| / sum r_k.
* `compute_preferred_direction_deg` (function) — Preferred direction in degrees from the
  complex sum of rate-weighted unit vectors.
* `compute_metrics_main` (script) — Compute per-(gampa, gaba, mode) tuning-curve metrics and
  write metrics.json (75-variant explicit format: 5 gampa x 5 gaba x 3 modes) plus
  derived_quantities.json (cross-grid 5x5 arrays for peak Hz, null Hz, primary DSI, vector-sum
  DSI, HWHM, RMSE; per-(gampa, gaba, angle) EPSP / IPSP envelopes; EPSP-decay grid). Enforces
  the EPSP_PASSIVE peak-Vm soft gate (REQ-15).
* `render_figures_main` (script) — Render all per-(gampa, gaba, direction) figures (soma V,
  EPSP, IPSP, PSTH) plus per-(gampa, gaba) polar tuning curves, the active-fraction polar
  plot, the 6 cross-grid heatmaps, and the regime-boundary contour overlay. Total ~1233 PNGs
  across the 5x5 grid.

Pure-Python NEURON library for a minimal direction-selective ganglion cell with 100 co-located
E + I synapses; the GABA branch uses the t0057 gaba_tonic POINT_PROCESS gated by a per-synapse
bar-arrival-locked (t_on_i, t_off_i) window; trial-mode dispatcher exposes FULL / EPSP_PASSIVE
/ IPSP_PASSIVE with HH save-and-zero on soma + AIS for the passive modes; sweeps a 5x5 (gAMPA,
GABA_BASE_NS) grid via public AMPA_PEAK_NS_VALUES and GABA_BASE_NS_VALUES constants.

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
<summary>📦 <strong>Minimal DSGC with Tonic GABA Sweep</strong>
(<code>minimal_dsgc_tonic_gaba_sweep</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `minimal_dsgc_tonic_gaba_sweep` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0057_tonic_gaba_sweep_t0053\code\constants.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\paths.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\swc_io.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\neuron_bootstrap.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\cell.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\placement.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\synapses.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\trial.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\run_tuning_curve.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\render_figures.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\compute_metrics.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\metrics_extra.py`, `tasks\t0057_tonic_gaba_sweep_t0053\code\mod\GabaTonic.mod` |
| **Dependencies** | neuron, numpy, matplotlib, pandas, tqdm |
| **Date created** | 2026-04-28 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |
| **Created by** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Documentation** | [`description.md`](../../../tasks\t0057_tonic_gaba_sweep_t0053\assets\library\minimal_dsgc_tonic_gaba_sweep\description.md) |

**Entry points:**

* `GABA_BASE_NS_VALUES` (function) — Public 5-tuple of swept per-synapse peak GABA conductance
  values in nS (0.25, 0.5, 1.0, 1.5, 2.0). The sweep harness iterates over these values in
  run_full_sweep; downstream callers can override by importing the constant and rebuilding the
  GABA_BASE_NS_VALUES module-level binding before invoking the sweep.
* `T_ON_MS` (function) — Public per-synapse tonic-window start time in ms (default 100).
  Active GABA synapses receive g = GABA_BASE_NS * 1e-3 (uS) over [T_ON_MS, T_OFF_MS].
* `T_OFF_MS` (function) — Public per-synapse tonic-window end time in ms (default 1400).
  Together with T_ON_MS, defines the 1300 ms tonic interval covering the full stimulus window
  minus the 100 ms BASE_OFFSET buffer.
* `gaba_tonic` (class) — Custom NEURON POINT_PROCESS registered as h.gaba_tonic after
  ensure_gaba_tonic_compiled() runs. RANGE attributes: g (uS), e (mV), t_on (ms), t_off (ms),
  ramp_ms (ms; default 1). Conductance envelope is g * envelope(t) where envelope is 0 outside
  [t_on, t_off], a 1 ms cosine ramp at each edge, and 1.0 in the middle. NONSPECIFIC_CURRENT i
  = envelope * g * (v - e). No NET_RECEIVE block; conductance is set by direct attribute write
  per trial.
* `ensure_gaba_tonic_compiled` (function) — Build code/mod/nrnmech.dll from
  code/mod/GabaTonic.mod via the run_nrnivmodl.cmd shim if missing, then load the DLL via
  h.nrn_load_dll so h.gaba_tonic becomes available. Idempotent across multiple calls within
  the same process. Must be called AFTER ensure_neuron_importable + load_stdrun and BEFORE any
  h.gaba_tonic(seg) construction.
* `build_dsgc_from_swc` (function) — Parse a calibrated SWC, collapse the 19 soma rows into
  one Section, build one h.Section per non-soma compartment, attach a synthetic axon initial
  segment, and return a CellHandles dataclass that includes soma_origin_um for the spatial
  driver.
* `sample_dendritic_locations` (function) — Sample N dendritic locations uniformly along total
  dendritic length using numpy.random.default_rng(seed); seed=0 reproduces t0052 / t0053
  placement bit-for-bit.
* `build_ei_pairs` (function) — Construct one AMPA Exp2Syn + tonic gaba_tonic instance per
  Location; each pair carries theta_centrifugal_rad = atan2(y - y_soma, x - x_soma)
  precomputed from soma_origin_um. AMPA path is bit-identical to t0053 (Exp2Syn + NetStim +
  NetCon, peak 0.5 nS); GABA branch uses no NetStim or NetCon.
* `schedule_ei_onsets` (function) — Per-trial scheduler: set AMPA NetStim.start at bar-arrival
  time; for each I synapse evaluate i_synapse_fires(theta_stim, theta_centrifugal); when fired
  set pair.gaba_syn.g = gaba_base_ns * 1e-3 (uS) and (t_on, t_off) = (T_ON_MS, T_OFF_MS),
  otherwise zero g and collapse the window. Returns ScheduleResult with onset_times_ms and
  i_fired_mask.
* `i_synapse_fires` (function) — Pure boolean predicate: returns cos(radians(theta_stim_deg -
  theta_centrifugal_deg)) < 0 (strict; perpendicular does not fire). Bit-identical to t0053's
  spatial centripetal-gating rule.
* `ScheduleResult` (class) — Frozen dataclass returned by schedule_ei_onsets, with
  onset_times_ms: list[float] and i_fired_mask: list[bool] aligned with the pair list.
* `TrialMode` (class) — StrEnum with members FULL, AMPA_ONLY, GABA_ONLY for selecting which
  synaptic drive is active.
* `run_one_trial` (function) — Run one trial: schedule onsets via the spatial gate at the
  supplied gaba_base_ns, apply mode-specific weight overrides, finitialize+continuerun, return
  TrialResult with V(t), spike times, synapse onset times, i_fired_mask, i_active_fraction,
  and gaba_base_ns.
* `run_full_sweep` (function) — End-to-end 5 GABA values x 12 directions x 10 trials x 3 modes
  = 1,800-trial sweep with dry-run validation gate (including the IPSP-sustained-window check
  at theta = 210 deg). Writes per-mode tuning-curve / spike-time / voltage-trace CSVs each
  carrying a leading gaba_base_ns column, an activation-time CSV with is_fired column, an
  active_fraction_per_direction CSV, and a wall-clock log.
* `compute_vector_sum_dsi` (function) — Vector-sum DSI from the per-angle mean firing rates:
  |sum r_k * exp(i theta_k)| / sum r_k.
* `compute_preferred_direction_deg` (function) — Preferred direction in degrees from the
  complex sum of rate-weighted unit vectors.
* `render_active_fraction_polar` (function) — Render the per-direction active-fraction polar
  plot (closed polygon with reference circle at 0.5).
* `render_cross_conductance_summary` (function) — Render the 6 cross-conductance summary PNGs
  (DSI primary, DSI vector-sum, peak Hz, null Hz, HWHM, RMSE vs t0004 target) from
  derived_quantities.json. Each is a single-curve scalar-vs-GABA_BASE_NS line plot with
  markers.
* `compute_metrics_main` (script) — Compute per-(gaba, mode) tuning-curve metrics and write
  metrics.json (15-variant explicit format: 5 conductances x 3 modes) plus
  derived_quantities.json (cross-conductance summary arrays + per-variant peak/null/vector-sum
  DSI + per-(gaba) aggregate EPSP/IPSP envelopes). Enforces the AMPA_ONLY peak-Hz regression
  sentinel (REQ-14).
* `render_figures_main` (script) — Render all per-(gaba, direction) figures (soma V, EPSP,
  IPSP, PSTH, activation histograms) plus per-(gaba) polar / Cartesian tuning curves,
  raster+PSTH per (gaba, direction), the active-fraction polar plot, and the 6
  cross-conductance summary plots.

Pure-Python NEURON library for a minimal direction-selective ganglion cell with 100 co-located
E + I synapses where the GABA branch uses a custom tonic POINT_PROCESS (gaba_tonic) gated by a
(t_on, t_off) window per synapse instead of t0053's per-event Exp2Syn; exposes
GABA_BASE_NS_VALUES so the sweep harness can vary peak conductance without re-importing.

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

<details>
<summary>📦 <strong>ModelDB 189347 DSGC -- Dendritic-Computation Driver</strong>
(<code>modeldb_189347_dsgc_dendritic</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `modeldb_189347_dsgc_dendritic` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0022_modify_dsgc_channel_testbed\code\neuron_bootstrap.py`, `tasks\t0022_modify_dsgc_channel_testbed\code\run_tuning_curve.py`, `tasks\t0022_modify_dsgc_channel_testbed\code\score_envelope.py`, `tasks\t0022_modify_dsgc_channel_testbed\code\plot_tuning_curve.py`, `tasks\t0022_modify_dsgc_channel_testbed\code\constants.py`, `tasks\t0022_modify_dsgc_channel_testbed\code\paths.py`, `tasks\t0022_modify_dsgc_channel_testbed\code\dsgc_channel_partition.hoc` |
| **Dependencies** | neuron, numpy, pandas, tqdm, matplotlib |
| **Date created** | 2026-04-21 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |
| **Created by** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Documentation** | [`description.md`](../../../tasks\t0022_modify_dsgc_channel_testbed\assets\library\modeldb_189347_dsgc_dendritic\description.md) |

**Entry points:**

* `run_one_trial_dendritic` (function) — Run one per-dendrite E-I trial at a given bar
  direction and return somatic firing rate in Hz.
* `build_ei_pairs` (function) — Create one AMPA (distal 0.9) and one GABA_A (proximal 0.3)
  Exp2Syn per ON-dendrite with NetStim burst drivers.
* `schedule_ei_onsets` (function) — Set per-pair NetStim start times and GABA weights for a
  given bar direction.
* `run_tuning_curve` (script) — CLI driver: --dry-run, --preflight (4x2), or default full
  12-angle x 10-trial sweep.
* `score_envelope` (script) — Score the emitted tuning curve via t0012 tuning_curve_loss and
  emit metrics.json.
* `plot_tuning_curve` (script) — Emit a polar+Cartesian tuning-curve PNG from the emitted CSV.

Per-dendrite excitation-inhibition driver for the Poleg-Polsky DSGC model, producing direction
selectivity via on-the-path shunting inhibition with a channel-modular AIS partition.

</details>

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
<summary>📦 <strong>ModelDB 189347 DSGC Port -- gabaMOD-swap protocol</strong>
(<code>modeldb_189347_dsgc_gabamod</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `modeldb_189347_dsgc_gabamod` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0020_port_modeldb_189347_gabamod\code\constants.py`, `tasks\t0020_port_modeldb_189347_gabamod\code\paths.py`, `tasks\t0020_port_modeldb_189347_gabamod\code\run_gabamod_sweep.py`, `tasks\t0020_port_modeldb_189347_gabamod\code\score_envelope.py`, `tasks\t0020_port_modeldb_189347_gabamod\code\plot_pd_vs_nd.py` |
| **Dependencies** | neuron, numpy, pandas, pydantic, tqdm, matplotlib |
| **Date created** | 2026-04-20 |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Documentation** | [`description.md`](../../../tasks\t0020_port_modeldb_189347_gabamod\assets\library\modeldb_189347_dsgc_gabamod\description.md) |

**Entry points:**

* `run_one_trial_gabamod` (function) — Apply canonical parameters, override h.gabaMOD to the
  condition-specific scalar (0.33 for PD, 0.99 for ND), assert BIP synapse positions stay at
  their baseline values, and return the somatic firing rate in Hz for a single trial.
* `main` (script) — Build the DSGC once, iterate over (condition, trial_seed) pairs for PD and
  ND, and emit data/tuning_curves.csv with schema (condition, trial_seed, firing_rate_hz).
* `main` (script) — Read data/tuning_curves.csv, compute DSI = (mean_PD - mean_ND) / (mean_PD
  + mean_ND) and peak = mean_PD, gate against the literature envelope (DSI 0.70-0.85, peak
  40-80 Hz), and write results/score_report.json and results/metrics.json.
* `main` (script) — Generate a PD vs ND mean firing-rate bar chart with per-trial scatter
  overlay and save it to results/images/pd_vs_nd_firing_rate.png.

Sibling port of ModelDB 189347 (Poleg-Polsky & Diamond 2016 DSGC) that implements direction
selectivity via the paper's native gabaMOD parameter swap (PD=0.33, ND=0.99) instead of the
t0008 spatial-rotation proxy.

</details>

<details>
<summary>📦 <strong>Procedural DSGC Morphology Generator Fix</strong>
(<code>procedural_dsgc_morphology_generator_fix</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `procedural_dsgc_morphology_generator_fix` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0092_diagnose_morphology_generator_silence\code\morphology_generator_fix.py`, `tasks\t0092_diagnose_morphology_generator_silence\code\baseline_channels.py`, `tasks\t0092_diagnose_morphology_generator_silence\code\paths.py`, `tasks\t0092_diagnose_morphology_generator_silence\code\constants.py` |
| **Dependencies** | neuron, numpy |
| **Date created** | 2026-05-08 |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |
| **Created by** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Documentation** | [`description.md`](../../../tasks\t0092_diagnose_morphology_generator_silence\assets\library\procedural_dsgc_morphology_generator_fix\description.md) |

**Entry points:**

* `generate_fixed_morphology` (function) — Build a procedural DSGC cell with the soma-area bug
  patched. Drop-in compatible with t0090's generate_morphology signature: same
  MorphologyParams + morph_seed inputs, same MorphologyResult output.
* `insert_baseline_channels` (function) — Insert HHst + cad on soma + dendrites + AIS of one
  cell. Idempotent; copy of t0090's verification.py:_insert_baseline_channels (task-internal
  there, exposed here for downstream re-use).

Drop-in replacement for t0090's generate_morphology that patches the soma-pt3d bug causing
zero spikes (or NaN voltage) under the t0083 best-cell channel set.

</details>
