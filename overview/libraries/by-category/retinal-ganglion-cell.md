# Libraries: `retinal-ganglion-cell`

9 librar(y/ies).

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
