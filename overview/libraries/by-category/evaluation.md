# Libraries: `evaluation`

1 librar(y/ies).

[Back to all libraries](../README.md)

---

<details>
<summary>📦 <strong>De Rosenroll 2026 DSGC with AIS and Dendritic-Spike
Machinery</strong>
(<code>de_rosenroll_2026_dsgc_ais_dendritic_spike</code>)</summary>

| Field | Value |
|---|---|
| **ID** | `de_rosenroll_2026_dsgc_ais_dendritic_spike` |
| **Version** | 0.1.0 |
| **Modules** | `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\build_cell_ais.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\extend_with_ais.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\apply_params.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\constants.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\trial_helpers.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\parametric_placer.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\trial_driver.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\recorder.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\bootstrap.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\paths.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\nsga2_loop.py`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\bkt80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\calt80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\catt80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\iht80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\kdrt80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\kv3t80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\kv4t80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\kv7t80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\napt80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\nart80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\nav16t80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\skahpt80.mod`, `tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\code\mods\skt80.mod` |
| **Dependencies** | neuron, numpy, pymoo |
| **Date created** | 2026-05-04 |
| **Categories** | [`ais`](../../../meta/categories/ais/), [`evaluation`](../../../meta/categories/evaluation/) |
| **Created by** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Documentation** | [`description.md`](../../../tasks\t0080_bedb_mobo_v3_dendritic_spike_nsga2\assets\library\de_rosenroll_2026_dsgc_ais_dendritic_spike\description.md) |

**Entry points:**

* `build_dsgc_cell_with_ais` (function) — Build a DSGC cell with AIS extension; v3 substrate
  uses the same builder but with the 5 new dendritic-spike parameters in the v3
  ParameterVector.
* `apply_parameter_vector` (function) — Write a 54-d v3 ParameterVector to all sections of the
  DSGC cell, including v3 distal Nav1.6 + NaP overlay on terminal dendrites.
* `DSGCCellWithAIS` (class) — Cell wrapper class re-exported from t0078; carries AIS sections
  and dendritic tier accessors.
* `ParameterVector` (class) — 54-d frozen dataclass with @property accessors for each
  parameter group, including the 5 v3 dendritic-spike parameters (gnmda_dend, mg_conc_mm,
  voff_nmda, nav16_dend_distal, nap_dend_distal).
* `BedBV3Problem` (class) — pymoo Problem subclass with n_var=54, n_obj=2, n_ieq_constr=1
  (AIS-to-soma Nav ratio constraint per Werginz 2024).
* `run_nsga2_loop` (function) — Main entry-point for the NSGA-II MOBO loop on the v3
  substrate; arms a cost-cap watchdog that exits cleanly on $2.00 hard cap trip.
* `evaluate_parameter_vector` (function) — Run a single 8 directions x 20 seeds evaluation of
  one parameter vector; returns DSI / PD rate / stability flag.

v3 extension of the t0078 AIS-augmented Bed B DSGC substrate adding dendritic Mg-block NMDA,
distal Nav1.6 + NaP, and hard biological bounds on AIS Nav density.

</details>
