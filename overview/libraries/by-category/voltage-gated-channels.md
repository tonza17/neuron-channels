# Libraries: `voltage-gated-channels`

1 librar(y/ies).

[Back to all libraries](../README.md)

---

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
