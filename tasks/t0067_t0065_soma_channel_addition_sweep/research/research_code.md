---
spec_version: "1"
task_id: "t0067_t0065_soma_channel_addition_sweep"
research_stage: "code"
tasks_reviewed: 3
tasks_cited: 3
libraries_found: 1
libraries_relevant: 1
date_completed: "2026-05-01"
status: "complete"
---
# Research: Code Survey for t0067

## Task Objective

Identify the t0008 cell-builder + t0065 trial-driver code surface that t0067 reuses, and the
NEURON-side mechanism for adding 5 new voltage-gated ion channels to the deposited Poleg-Polsky soma
without breaking the existing HHst / bipNMDA / SACinhib / SACexc mechanism set.

## Library Landscape

The relevant library asset is `modeldb_189347_dsgc` (under
`tasks/t0008_port_modeldb_189347/assets/library/`). It supplies the NEURON HOC template and the
mechanism MOD files (HHst, bipolarNMDA, SAC2RGCexc, SAC2RGCinhib, SquareInput, spike). t0067 extends
this set with 5 new MOD files (`nav16t67`, `napt67`, `nart67`, `kv3t67`, `kv4t67`) in a task-local
DLL that loads alongside (not replacing) the t0008 DLL — NEURON allows multiple `nrn_load_dll`
calls when the loaded DLLs do not redefine the same SUFFIX.

## Methodology Review

Read in full:

* `tasks/t0008_port_modeldb_189347/code/build_cell.py` (cell builder + idempotent load_neuron)
* `tasks/t0008_port_modeldb_189347/code/run_nrnivmodl.cmd` (Windows MOD compile script)
* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc` (HHst
  density assignments, soma + dendrite gnabar/gkbar wiring)
* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCinhib.mod`
  (NONSPECIFIC_CURRENT pattern for our new MODs)
* `tasks/t0019_literature_survey_voltage_gated_channels/assets/answer/nav-kv-combinations-for-dsgc-modelling/short_answer.md`
  (kinetic priors for Nav1.6, Kv1, Kv3 channels)
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` (per-trial driver template)

## Key Findings

### 1. Cell builder (t0008)

* `build_dsgc()` returns the NEURON `h` handle after sourcing `RGCmodel.hoc` + `dsgc_model.hoc` and
  instantiating the `DSGC` template. The cell is `h.RGC` with `h.RGC.soma` exposed.
* `load_neuron()` is idempotent (uses `_loaded` flag on the function) — second call just returns
  the cached `h`. So t0067 can call it without re-loading the DLL.
* `apply_params(h, seed=...)` writes canonical conductances and the random-stream seed; called per
  trial in t0065.

### 2. HH mechanism in the deposited cell

* The deposited cell uses `HHst` (same family as de Rosenroll t0024 but separately compiled).
* Soma `gnabar_HHst = RGCsomana = 0.4 * active * (1 - TTX)` S/cm² → 400 mS/cm² when active=1,
  TTX=0. (For comparison, our added Nav1.6 at "high" 90 mS/cm² is ~22% of the existing somatic Na
  density.)
* Dendrite `gnabar_HHst = RGCdendna = 0.0002 S/cm²` → 0.2 mS/cm² (essentially passive
  dendrites).

### 3. Loading multiple DLLs

* `h.nrn_load_dll(path)` returns 1.0 on success, raises if the DLL contains mechanism SUFFIXes that
  conflict with already-loaded ones.
* Strategy: vendor 5 new MOD files into `tasks/t0067_*/code/mods/`, compile via `run_nrnivmodl.cmd`,
  get `tasks/t0067_*/code/build/nrnmech.dll`. After t0008's `load_neuron()` runs,
  `h.nrn_load_dll(t0067_dll_path)` adds the 5 new mechanisms without conflict (suffixes `nav16t67`,
  `napt67`, `nart67`, `kv3t67`, `kv4t67` don't collide).

### 4. Inserting a new mechanism on the soma

* `h.RGC.soma.insert("nav16t67")` creates the mechanism on every segment of the soma section.
* Per-segment density: `for seg in h.RGC.soma: seg.gbar_nav16t67 = density_S_cm2`.
* Init/state vars are initialized by the mechanism's `INITIAL` block when `h.finitialize()` runs —
  no Python-side init needed.

### 5. NONSPECIFIC_CURRENT pattern for the new MODs

The deposited cell already defines the `na_ion` and `k_ion` USEION via HHst. Adding new MODs that
also `USEION na WRITE ina` would create a conflict at compile time (NEURON allows multiple mechs to
write the same ion's current, but the tracking gets confusing with non-physiological ion
accumulation). Cleaner: each new MOD uses `NONSPECIFIC_CURRENT i` with its own reversal constant
(`erev = 50 mV` for Na-like, `-85 mV` for K-like). This is the same pattern used by
`SAC2RGCinhib.mod` (`NONSPECIFIC_CURRENT i`, `e = -65 mV`).

### 6. Per-trial state reset

`apply_params(h, seed=...)` re-seeds NEURON's RNG and rewrites the synapse parameter defaults.
`h("init_active()")` rebinds `RGCsomana` onto `gnabar_HHst`, then `h("update()")` pushes those onto
each section. **Critical**: our new channel `gbar_<suffix>` values are set AFTER `init_active()` to
ensure they survive the rebind (init_active only touches HHst).

### 7. Spike detection

Reuse t0065 pattern: `h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)` with
`threshold = -10 mV`, `record(spike_vec)`. `int(spike_vec.size())` gives the spike count.

## Reusable Code and Assets

* **t0008 library asset**: `nrnmech.dll` (deposited mechanisms) + `RGCmodel.hoc` morphology.
* **t0008 cell builder**: `build_dsgc()`, `apply_params()`, `read_synapse_coords()`,
  `load_neuron()`. All reusable verbatim.
* **t0008 compile script**: `run_nrnivmodl.cmd` — used to compile the t0067-local DLL.
* **t0019 channel priors**: `nav-kv-combinations-for-dsgc-modelling` answer asset gives V_half,
  kinetic time constants, and density references for Nav1.6 / Kv1 / Kv3 (also covers
  Fohlmeister-Miller HH).
* **t0065 trial driver**: per-trial sequence (apply_params → set gabaMOD → set exptype →
  init_active → update → placeBIP → finitialize → continuerun → record spikes).

## Lessons Learned

* From t0065 (immediate predecessor): the cell builder is stateful — build once, reuse across all
  trials.
* From t0024/t0066: `nrn_load_dll` cannot be called twice on the SAME DLL (re-defines mechanisms).
  But it CAN be called multiple times with DIFFERENT DLLs as long as no SUFFIX collisions.
* From t0008: HHst already provides Na and K currents on the soma. Our new channels are ADDITIONS to
  that, not replacements. The total somatic Na current is
  `i_HHst_Na + i_nav16t67 + i_napt67 + i_nart67`; total K current is
  `i_HHst_K + i_kv3t67 + i_kv4t67`.

## Recommendations for This Task

1. Vendor 5 MOD files into `tasks/t0067_*/code/mods/`. Use NONSPECIFIC_CURRENT pattern (no USEION)
   to avoid ion-accumulation conflicts.
2. Compile via the t0008 `run_nrnivmodl.cmd` into a task-local
   `tasks/t0067_*/code/build/nrnmech.dll`.
3. In `code/run_sweep.py`:
   * Call `build_dsgc()` once (loads t0008 DLL).
   * Then call `h.nrn_load_dll(t67_dll_path)` to add the 5 new mechanisms.
   * Insert ALL 5 mechanisms on the soma at gbar=0; per-trial set the active one's gbar to the
     target density and zero the others.
4. Per-trial:
   `apply_params → gabaMOD → exptype=1 → init_active → update → placeBIP → set active channel gbar → finitialize → continuerun → count spikes`.
5. 160 trials at ~3 s each = ~8 min sweep. No remote machines.

## Task Index

Prior tasks reviewed for this research stage:

* **t0008_port_modeldb_189347** — primary code source. Cell builder, HOC template, deposited MOD
  set.
* **t0019_literature_survey_voltage_gated_channels** — kinetic priors for the 5 new channels.
* **t0065_t0020_epsp_ipsp_vm_protocol** — trial driver template, baseline DSI = 0.875 (single
  seed) — note that t0067's baseline at 5 seeds gives DSI = 0.797 (the noise variance is real with
  multiple seeds even though the deposited cell is "deterministic given seed").

t0024 (de Rosenroll) and t0066 (Rosenroll EPSP/IPSP) were NOT used — t0067 is on the Poleg-Polsky
substrate per user spec.
