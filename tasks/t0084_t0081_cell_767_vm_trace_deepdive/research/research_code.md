---
spec_version: "1"
task_id: "t0084_t0081_cell_767_vm_trace_deepdive"
research_stage: "code"
tasks_reviewed: 75
tasks_cited: 2
libraries_found: 20
libraries_relevant: 1
date_completed: "2026-05-05"
status: "complete"
---
# Research Code: Vm-Trace Deep-Dive of t0081 Cell 767

## Task Objective

This task re-evaluates three cells from t0081's Pareto front — cell 767 (joint-pass; DSI 0.494 /
PD 11.39 Hz), cell 637 (near-pass; DSI 0.337), and cell 762 (near-pass; DSI 0.314) — on the v3
dendritic-spike-augmented Bed B substrate. For each cell, 8 direction simulations are run with
extended recording: per-section Vm at proximal soma, mid-dendrite, and distal dendrite; NMDA
conductance trajectories at distal synapses; Nav1.6 and NaP current decomposition at terminal
dendrites; and AIS spike onset times. The output is 12 figure assets (4 per cell) and one answer
asset attributing cell 767's joint-pass DSI to NMDA Mg-block, distal Nav1.6, NaP, or a combination
using a fractional-channel-contribution metric.

## Library Landscape

Twenty libraries are registered in `tasks/*/assets/library/` as of this research date (75 completed
tasks). The single directly relevant library is:

* **`de_rosenroll_2026_dsgc_ais_dendritic_spike`** — library ID, version 0.1.0, created by
  `t0080_bedb_mobo_v3_dendritic_spike_nsga2`. This is the v3 extension of the AIS-augmented Bed B
  substrate, adding Mg-block NMDA synapses (Exp2NMDA), distal Nav1.6, and distal NaP to the terminal
  dendrites. Import path:
  `from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.<module> import <symbol>`. Marked
  **import via library**.

Other libraries checked and found not relevant for this specific Vm-recording task:

* `de_rosenroll_2026_dsgc` (t0024) — base Bed B substrate without AIS; superseded by t0080 for
  this task.
* `de_rosenroll_2026_dsgc_ais` (t0078) — AIS-augmented v2 without dendritic-spike machinery; not
  v3-compatible.
* `tuning_curve_viz` (t0011), `tuning_curve_loss` (t0012), `dsgc_active_channel_pack` (t0074),
  `modeldb_189347_dsgc*` (t0008, t0020, t0022, t0046), `minimal_dsgc_*` (t0052–t0059, t0057) —
  these are earlier substrate generations or visualisation utilities that do not apply to the v3 Bed
  B recording pipeline.

No library corrections (replacement overlays) are applicable here; the aggregator reflects the
canonical `de_rosenroll_2026_dsgc_ais_dendritic_spike` without overlays.

## Key Findings

### Cell Parameter Data Layout in t0081

`tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` contains a JSON array of 768
objects, one per evaluated cell. Each object has keys:

```
cell_index, generation, params, dsi, pd_rate_hz, is_unstable, peak_vm_mv,
elapsed_s, constraint_violation, is_feasible
```

`params` is a 54-element list of float values in **natural units** (not normalised). The target
cells are:

* Cell 767: `cell_index=767`, `generation=7`, `dsi=0.4941`, `pd_rate_hz=11.39`; v3 dendritic params
  (indices 49–53): `[6.72e-3, 0.261, 6.28, 0.0149, 9.21e-5]` corresponding to
  `gnmda_dend=6.72e-3 uS`, `mg_conc_mm=0.261 mM`, `voff_nmda=6.28 mV`,
  `nav16_dend_distal=0.0149 S/cm²`, `nap_dend_distal=9.21e-5 S/cm²`.
* Cell 637: `cell_index=637`, `generation=6`, `dsi=0.3374`, `pd_rate_hz=11.82`; v3 dendritic params:
  `[2.75e-3, 0.402, -9.13, 0.0292, 2.23e-4]`.
* Cell 762: `cell_index=762`, `generation=7`, `dsi=0.3140`, `pd_rate_hz=12.93`; v3 dendritic params:
  `[3.12e-3, 0.286, 1.41, 7.11e-3, 1.10e-3]`.

`tasks/t0081_bedb_v3_warmstart_nsga2/results/data/pareto_front.json` is a dict with keys `cells` and
`n_total`. The `cells` list confirms all three target cells:
`[9, 112, 136, 331, 490, 571, 627, 637, 664, 699, 730, 741, 744, 747, 762, 767]` (16 total Pareto
cells). [t0081]

### v3 Substrate Architecture and Entry Points

The library `de_rosenroll_2026_dsgc_ais_dendritic_spike` from [t0080] exposes these key imports:

**Cell construction**:

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import (
    DSGCCellWithAIS,
    build_dsgc_cell_with_ais,
)
```

`build_dsgc_cell_with_ais()` returns a `DSGCCellWithAIS` dataclass with fields: `h` (NEURON hoc
object), `soma`, `all_dends` (list), `primary_dends`, `non_terminal_dends`, `terminal_dends`,
`terminal_locs_xy`, `origin_xy`, `ais_proximal`, `ais_distal`.

**Parameter application**:

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import ParameterVector
```

`apply_parameter_vector(cell=cell, params=params)` writes the 54-d `ParameterVector` to all
sections, including the v3 overlay: `seg.gbar_nav16t80 = params.nav16_dend_distal` and
`seg.gbar_napt80 = params.nap_dend_distal` on `cell.terminal_dends`. [t0080]

**Single-cell evaluation** (8 dir × n_seeds, parallel):

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    evaluate_parameter_vector,
)

result = evaluate_parameter_vector(
    params=params,
    angles_deg=(0, 45, 90, 135, 180, 225, 270, 315),
    n_seeds=1,       # deep-dive uses 1 seed per direction
    max_workers=1,   # sequential for recording (Vector refs must stay in-process)
)
```

`max_workers=1` runs sequentially in the calling process — critical for attaching NEURON
`h.Vector().record()` handles (which cannot cross process boundaries).

**Synapse creation** (returns `SynapseBundle`):

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    SynapseBundle,
    setup_synapses_parametric,
)

bundle = setup_synapses_parametric(
    h=cell.h, cell=cell, ..., gnmda_dend=params.gnmda_dend,
    mg_conc_mm=params.mg_conc_mm, voff_nmda=params.voff_nmda,
)
```

`SynapseBundle` carries `syns_ach`, `ncs_ach`, `syns_gaba`, `ncs_gaba`, `syn_xy_ach`, `syn_xy_gaba`,
`syns_nmda`, `ncs_nmda`. `syns_nmda` is a list of `Exp2NMDA` point-process objects co-located with
each ACh contact. [t0080]

### Recordable NEURON Variables

The v3 substrate uses mod files from `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/mods/`.
All variables are accessible via NEURON's `h.Vector().record(seg._ref_<var>)` idiom.

**Per-section Vm**: `v` is a standard NEURON variable on every segment.

```python
v_vec = h.Vector()
v_vec.record(section(x)._ref_v, dt_record)
```

**NMDA conductance** (`g`, uS): The `Exp2NMDA.mod` file declares `RANGE g, gmax`. `g` is the
Mg-block-modulated conductance (`gmax / (1 + n * exp(-gama * local_v))`), in uS. Record:

```python
for nmda_syn in bundle.syns_nmda:
    g_vec = h.Vector()
    g_vec.record(nmda_syn._ref_g, dt_record)
```

**Nav1.6 current** (`i`, mA/cm²): `nav16t80.mod` declares `RANGE gbar, i`. Record:

```python
for seg in terminal_section:
    i_nav16_vec = h.Vector()
    i_nav16_vec.record(seg.nav16t80._ref_i, dt_record)
```

**NaP current** (`i`, mA/cm²): `napt80.mod` declares `RANGE gbar, i`. Record:

```python
for seg in terminal_section:
    i_nap_vec = h.Vector()
    i_nap_vec.record(seg.napt80._ref_i, dt_record)
```

**AIS spike onset**: Record Vm at `cell.ais_distal(0.5)` and detect threshold crossings
(`AP_THRESHOLD_MV = -10.0 mV`) in post-processing.

### Existing Recorder Infrastructure

`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/recorder.py` provides
`attach_recorders(h, soma, bundle)` and
`save_recorders_npz(output_path, recorders, direction_label)`. This handles per-synapse ACh/GABA
conductance and local Vm recording but does NOT yet record per-segment NMDA `g`, per-mechanism `ina`
at terminal dendrites, or AIS Vm for spike onset. These extensions must be added in this task's own
`code/` directory. [t0080]

### t0081 Eval Harness Does Not Register New Libraries

t0081's `code/` directory (`run_loop.py`, `paths.py`, `warm_start.py`, `build_metrics.py`,
`plot_results.py`, `smoke_gate.py`) is not registered as a library. It wraps the t0080 NSGA-II loop
via monkey-patching of path constants. This task does NOT need to import from t0081's `code/`; it
reads parameter data directly from `results/data/all_evaluations.json`. [t0081]

### t0083 Concurrency Safety

t0083 (`bedb_v3_extend_nsga2_gen8plus`) is executing concurrently on Vast.ai in its own worktree.
Its task folder (`tasks/t0083_bedb_v3_extend_nsga2_gen8plus/`) has no `code/` directory in the
current main-branch snapshot. t0083 will write new code into its own branch, not into t0080's or
t0081's library paths. This task (t0084) **must not modify** any files in
`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/` or
`tasks/t0081_bedb_v3_warmstart_nsga2/code/`. All new recording logic goes exclusively into
`tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/`.

### ParamIndex Enumeration for v3 Machinery

The five v3 dendritic-spike dimensions occupy indices 49–53 of the 54-d `ParameterVector`:

| Index | `ParamIndex` | Description |
| --- | --- | --- |
| 49 | `GNMDA_DEND` | Exp2NMDA NetCon weight (uS); log-uniform [1e-5, 1e-2] |
| 50 | `MG_CONC_MM` | Mg concentration written to Exp2NMDA `n` (mM); linear [0.1, 0.5] |
| 51 | `VOFF_NMDA` | NMDA voltage-sensitivity offset (mV); linear [-10, 10] |
| 52 | `NAV16_DEND_DISTAL` | Terminal-dend Nav1.6 gbar (S/cm²); log-uniform [1e-5, 0.05] |
| 53 | `NAP_DEND_DISTAL` | Terminal-dend NaP gbar (S/cm²); log-uniform [1e-5, 0.01] |

Cell 767 has the highest `gnmda_dend` (6.72e-3) and `nav16_dend_distal` (0.0149) among the three
target cells, suggesting these two channels are the primary candidates for the joint-pass DSI
improvement. [t0080]

## Reusable Code and Assets

### 1. t0080 Library — import via library

**Source**: `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/` (registered as library
`de_rosenroll_2026_dsgc_ais_dendritic_spike`)

**What it provides**: Complete v3 Bed B substrate — cell construction
(`build_dsgc_cell_with_ais`), parameter application (`apply_parameter_vector`), synapse setup
(`setup_synapses_parametric`), sequential single-cell evaluation (`run_one_trial`,
`_worker_prepare`), and the existing per-synapse recorder (`attach_recorders`,
`save_recorders_npz`).

**Reuse method**: **import via library** — all of the following are direct imports from t0080:

```python
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import (
    DSGCCellWithAIS, build_dsgc_cell_with_ais,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ParameterVector, ANGLES_8DIR_DEG, TSTOP_MS, DT_MS, V_INIT_MV, AP_THRESHOLD_MV,
    CELSIUS_DEG_C, STEPS_PER_MS, SEED_BASE, PD_DIRECTION_DEG, ND_DIRECTION_DEG,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    SynapseBundle, setup_synapses_parametric,
    _bar_arrival_times, _count_spikes, _gaba_prob_for_direction,
    _rates_to_events, _rates_with_ar2_noise, BASE_ACH_PROB, RATE_DT_MS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    run_one_trial, _worker_prepare,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.recorder import (
    attach_recorders, save_recorders_npz, BedBRecorders,
)
```

**Adaptation needed**: None to the library code itself. This task wraps `run_one_trial` with
additional `h.Vector().record()` calls before calling `h.run()` to capture per-section Vm, NMDA `g`,
Nav1.6 `i`, NaP `i`, and AIS Vm.

### 2. t0081 Parameter Vectors — read from data file (no import needed)

**Source**: `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json`

**What it provides**: 768-entry JSON array containing the 54-d natural-unit parameter vector for
each evaluated cell. Target cell IDs are 767, 637, 762.

**Reuse method**: Read directly with `json.load()`; construct
`ParameterVector(values=np.array(entry["params"]))` for each target cell. No code import needed.

### 3. New Code to Write in tasks/t0084/code/

The following modules must be written fresh (no prior task provides this exact combination):

* `code/paths.py` — centralised `pathlib.Path` constants for results and figure output
* `code/constants.py` — task-local constants (recording sections, figure layout params)
* `code/deep_dive_recorder.py` — extended recorder adding NMDA `g`, Nav1.6 `i`, NaP `i`, AIS Vm
  alongside the existing t0080 recorder
* `code/run_deepdive.py` — orchestrates per-cell, per-direction simulations; saves numpy arrays
* `code/plot_figures.py` — generates the 4 figures per cell (12 total)
* `code/attribution_metric.py` — computes fractional channel contribution to PD-ND depolarisation
  delta
* `code/answer_writer.py` — writes `assets/answer/cell-767-dendritic-spike-mechanism-attribution/`

## Lessons Learned

**Sequential mode is mandatory for recording**: t0080's `evaluate_parameter_vector` with
`max_workers > 1` uses `ProcessPoolExecutor`, which pickles parameters and sends them to worker
processes. NEURON `h.Vector()` objects are not pickleable and cannot be shared across processes. The
deep-dive must call `run_one_trial` directly in the main process after manually calling
`_worker_prepare` with `max_workers=1`. This constraint is already documented in the trial_driver
CLI (`--max-workers 1` is the smoke-test default). [t0080]

**Exp2NMDA variable to record is `g` not `g_nmda`**: The `Exp2NMDA.mod` file uses `g` (uS) as the
conductance RANGE variable (not `g_nmda` or `gnmda`). The reference in Python is `nmda_syn._ref_g`.
The NEURON mechanism variable `gmax = B - A` is the unblocked conductance and
`g = gmax / (1 + n * exp(-gama * local_v))` is the Mg-block-modulated value. For mechanism
attribution, recording `g` (the effective conductance after Mg-block) is the right quantity; it
directly reflects the current flowing and the Mg-block state. [t0080]

**Nav1.6 and NaP current variable is `i` (mA/cm²)**: Both `nav16t80.mod` and `napt80.mod` expose
`RANGE i` as `i = gbar * activation_gates * (v - erev)`. The segment reference is
`seg.nav16t80._ref_i` and `seg.napt80._ref_i`. These are current densities (mA/cm²); multiply by
section area to get absolute current (nA). [t0080]

**t0081's warm-start harness is read-only for this task**: t0081 monkey-patches t0080 path constants
at runtime to redirect saves; it does not register any new library or modify t0080's evaluation
logic. t0084 can safely import from t0080's library and read from t0081's result data without risk
of conflicts from t0083 (which runs in a separate git worktree and branch). [t0081]

**Cell 767's v3 params suggest dominant NMDA + Nav1.6 channels**: `gnmda_dend = 6.72e-3 uS` is near
the upper end of the log-uniform range [1e-5, 1e-2], and `nav16_dend_distal = 0.0149 S/cm²` is also
near the upper bound [1e-5, 0.05]. `nap_dend_distal = 9.21e-5 S/cm²` is near the lower bound
[1e-5, 0.01], suggesting NaP contributes minimally. The fractional-contribution metric will confirm
or refute this observation. [t0081]

## Recommendations for This Task

1. **Use `run_one_trial` directly in-process**: Do not call `evaluate_parameter_vector` with
   `max_workers > 1`. Build the cell once per process, call `_worker_prepare` to apply parameters
   and set up the synapse bundle, then call `run_one_trial` per direction. Before each `h.run()`,
   attach the extended recorders (section Vm, NMDA `g`, Nav1.6 `i`, NaP `i`, AIS Vm). After
   `h.run()`, harvest the vectors and save to `.npz`.

2. **Import the v3 library for all substrate code**: All imports from t0080 are via the registered
   library path `tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.*`. Do not copy t0080 code.

3. **Read cell parameters from `all_evaluations.json`**: Load the 54-d parameter vector for cells
   767, 637, 762 from `tasks/t0081_bedb_v3_warmstart_nsga2/results/data/all_evaluations.json` using
   `json.load()` and construct `ParameterVector(values=np.array(entry["params"]))`.

4. **Record NMDA conductance as `_ref_g` on each `Exp2NMDA` synapse**: The bundle's `syns_nmda` list
   provides direct handles. Attach one `h.Vector` per synapse.

5. **Record Nav1.6 and NaP currents using `_ref_i`**: Iterate over segments of one representative
   terminal dendrite section per cell. The NEURON variable on `seg.nav16t80` is `_ref_i`.

6. **Attribution metric**: Integrate NMDA `g * (v - e_nmda)` (current through NMDA) over the PD
   window; integrate Nav1.6 `i` and NaP `i` over the same window at the distal dendrite. Compute the
   same integrals for ND. The fractional contribution of each channel is its (PD integral - ND
   integral) divided by the sum of all three absolute PD-ND deltas.

7. **Do not modify t0080 library code**: t0083 is concurrently using the same library from its own
   worktree snapshot. All new recording logic goes into
   `tasks/t0084_t0081_cell_767_vm_trace_deepdive/code/`.

## Task Index

### [t0080]

* **Task ID**: `t0080_bedb_mobo_v3_dendritic_spike_nsga2`
* **Name**: Bed B v3 MOBO with dendritic-spike machinery and NSGA-II
* **Status**: completed
* **Relevance**: Provides the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library (v3 substrate)
  with all entry points needed for this task: cell construction, parameter application, synapse
  setup (including Exp2NMDA), sequential single-cell evaluation, and the mod files whose RANGE
  variables are recorded (`nav16t80._ref_i`, `napt80._ref_i`, `Exp2NMDA._ref_g`).

### [t0081]

* **Task ID**: `t0081_bedb_v3_warmstart_nsga2`
* **Name**: Bed B v3 NSGA-II at full scope with combined t0078+t0080 warm-start
* **Status**: completed
* **Relevance**: Provides the 54-d natural-unit parameter vectors for target cells 767, 637, and 762
  in `results/data/all_evaluations.json`, and confirms all three cells are on the 16-cell Pareto
  front in `results/data/pareto_front.json`. Also provides context on the joint-pass criterion and
  which v3 parameters are likely dominant.
