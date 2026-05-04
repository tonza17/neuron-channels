# Libraries: `voltage-gated-channels`

3 librar(y/ies).

[Back to all libraries](../README.md)

---

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
