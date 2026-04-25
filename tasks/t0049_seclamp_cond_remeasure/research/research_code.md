---
spec_version: "1"
task_id: "t0049_seclamp_cond_remeasure"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 4
libraries_found: 7
libraries_relevant: 1
date_completed: "2026-04-24"
status: "complete"
---
# Research Code: Re-measure Fig 3A-E Conductances Under Somatic SEClamp

## Task Objective

This task adds a NEURON `SEClamp` at the soma of the deposited Poleg-Polsky 2016 DSGC and
re-measures the per-channel synaptic conductance (NMDA, AMPA, GABA) under voltage clamp at -65 mV.
The goal is an apples-to-apples comparison with the paper's Fig 3A-E values, which are most likely
**somatic-voltage-clamp** conductances rather than the **per-synapse direct** `_ref_g` values that
[t0047] recorded. The re-measurement will adjudicate between H1 (modality-only mismatch), H2
(partial), and H0 (real parameter mismatch). The implementation reuses [t0046]'s `run_one_trial` and
the deposited `modeldb_189347_dsgc_exact` library wholesale, adding only a SEClamp wrapper and a
four-trial channel-isolation protocol.

## Library Landscape

The library aggregator is not present in this branch of `arf/scripts/aggregators/`, so libraries
were enumerated by walking `tasks/*/assets/library/*/details.json` directly. Seven libraries exist
across all completed tasks:

* **`modeldb_189347_dsgc_exact`** (created by [t0046], v0.1.0). Highly relevant — this is the
  exact library this task is built on. Module entry points include `build_dsgc`, `run_one_trial`,
  `ensure_neuron_importable`. Import path:
  `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial`.
* `modeldb_189347_dsgc` (from t0008). Predecessor port. Not relevant — superseded by the exact
  reproduction in [t0046].
* `modeldb_189347_dsgc_gabamod` (from t0020). GABA-modulation variant. Not relevant — this task
  zeroes GABA via the existing `gabaMOD` global, no fork needed.
* `modeldb_189347_dsgc_dendritic` (from t0022). Channel-testbed variant. Not relevant.
* `de_rosenroll_2026_dsgc` (from t0024). Sibling DSGC port. Not relevant — this task targets the
  Poleg-Polsky 2016 deposited cell only.
* `tuning_curve_viz` (from t0011) and `tuning_curve_loss` (from t0012). Not relevant — this task
  produces conductance bar charts, not tuning curves or loss surfaces.

Only the [t0046] library is imported; all other prior task code is referenced through the copy rule
(none copied here — the SEClamp wrapper is new code).

## Key Findings

### NEURON SEClamp Insertion Pattern

The standard NEURON two-step SEClamp instantiation places a series-resistance voltage clamp on a
chosen segment. From the NEURON reference (consistent with the wrapper documented in
`bipolarNMDA.mod` in [t0046]'s sources), the canonical idiom is:

```python
clamp = h.SEClamp(soma(0.5))
clamp.dur1 = h.tstop      # clamp duration covers the whole trial
clamp.amp1 = -65.0        # clamp potential in mV
clamp.rs = 0.001          # series resistance in MOhm; effectively a voltage source
i_rec = h.Vector()
i_rec.record(clamp._ref_i)  # records the clamp current i in nA, sub-sampled at dt
```

The clamp must be inserted **after** `placeBIP()` runs so it does not interact with synapse
placement. In [t0046]'s `run_one_trial` (`code/run_simplerun.py:130`),
`h.simplerun(int(exptype), int(direction))` internally calls `init_active`, `update`, `placeBIP`,
then `run()`. The cleanest hook for SEClamp insertion is to copy the pattern of the AP5-override
branch in `run_simplerun.py:135-151`: after `simplerun()` returns, override the desired globals
(here also the per-channel toggles), call `h("update()")` and `h("placeBIP()")`, attach the SEClamp
and recorder vectors, then `h.finitialize(V_INIT_MV); h.continuerun(TSTOP_MS)`.

### Soma Section Access from Python

[t0046] already accesses the soma via `h.RGC.soma(0.5)._ref_v` (`code/run_simplerun.py:115`, `:124`,
`:147`). The `RGC` is a HOC `objref` instance of the `DSGC` template from `RGCmodel.hoc:9-11`, which
declares `public soma, dend, ...`. The soma is created by `create soma, dend[350]`
(`RGCmodel.hoc:21`). The same `h.RGC.soma(0.5)` Python handle is the correct insertion point for the
SEClamp; pass it to `h.SEClamp(h.RGC.soma(0.5))`. No extra HOC calls are needed — the section is
already accessible whenever `_ensure_cell()` has run.

### Channel Isolation via HOC Globals

The deposited `simplerun()` proc (`dsgc_model_exact.hoc:316-334`) sets four key conductance globals
that are then propagated into the per-synapse RANGE variables by `update()` and `placeBIP()`:

| Global | Set in simplerun | Effect | Override target |
| --- | --- | --- | --- |
| `b2gampa` | `0.25` (line 317) | `gAMPAsingle_bipNMDA = b2gampa` (line 263) — AMPA per-vesicle conductance | zero AMPA |
| `b2gnmda` | `0.5*nmdaOn` (line 318) | `gNMDAsingle_bipNMDA = b2gnmda` (line 264) — NMDA per-vesicle conductance | zero NMDA |
| `gabaMOD` | `.33+.66*$2` (line 323) | Multiplies SAC inhib stimulus amplitude in `mulnoise.fill(VampT*gabaMOD,...)` (line 234) | zero GABA |
| `s2ggaba` | `0.5` (line 319) | `gsingle_SACinhib = s2ggaba` (line 265) — GABA per-vesicle conductance | alternative GABA off-switch |

For the four channel-isolation trials this task runs, the override pattern (after `simplerun()`
returns and before the SEClamp re-run) is:

* **Full circuit (`all`)**: no overrides.
* **AMPA-only**: `h.b2gnmda = 0`, `h.gabaMOD = 0`.
* **NMDA-only**: `h.b2gampa = 0`, `h.gabaMOD = 0`.
* **GABA-only**: `h.b2gnmda = 0`, `h.b2gampa = 0`.

These globals are write-accessible from Python because the existing [t0047] code in
`code/run_with_conductances.py` and [t0046]'s `code/run_simplerun.py:100, :137-138` already write
`h.b2gnmda` and `h.flickerVAR` directly via attribute setattr. The same mechanism applies to
`h.b2gampa` and `h.gabaMOD`.

### bipolarNMDA.mod AMPA / NMDA Independence

The MOD source `bipolarNMDA.mod` (in [t0046]'s `assets/library/modeldb_189347_dsgc_exact/sources/`)
defines the bipolar synapse as a single POINT_PROCESS with **two independent conductance state
variables**, `gAMPA` and `gNMDA` (lines 72, 80), driven by the same presynaptic vesicle-release
event (`releasefunc`, lines 138-159). On each release, `gAMPA` increments by `release * gAMPAsingle`
(line 150) and `gNMDA` (via state A/B) increments by `release * gNMDAsingle` (lines 151-152). The
two currents flow through separate non-specific channels: `iAMPA = (1e-3) * gAMPA * (v - e)` (line
110\) and `iNMDA = (1e-3) * gNMDA * (v - e)` (line 111), both with `e = 0` (line 49).

Because `gAMPAsingle` and `gNMDAsingle` are independent GLOBAL parameters bound to `b2gampa` and
`b2gnmda` respectively, setting `b2gampa = 0` zeroes only the AMPA component while NMDA continues to
release from the same presynaptic event (and vice versa). This is verified by the existing [t0047]
sweep in `code/run_with_conductances.py:111-119`, which records `_ref_gAMPA` and `_ref_gNMDA`
independently on each `bip` synapse, confirming both can be probed (and therefore silenced)
independently. The bipolarNMDA dual-component design makes channel isolation feasible without
forking the MOD file.

### Reversal Potentials and Driving Forces

The per-current → conductance conversion `g(t) = i_clamp(t) / (V_clamp - E_rev)` requires the
reversal potentials of each channel. From [t0046]'s `code/constants.py` (re-affirmed by [t0047]'s
`code/constants.py:38-41` assertion):

* `E_BIPNMDA_MV = 0.0` (`MOD e = 0`, lines 49 of `bipolarNMDA.mod`).
* `E_SACEXC_MV = 0.0` (same e=0 on the excitatory cholinergic synapse).
* `E_SACINHIB_MV = -60.0` (main.hoc / `dsgc_model_exact.hoc:80` overrides the MOD default of -65 mV;
  this is the canonical paper value).

At `V_clamp = -65 mV`, the driving forces are:

| Channel | E_rev (mV) | V_clamp - E_rev (mV) |
| --- | --- | --- |
| NMDA | 0 | -65 |
| AMPA | 0 | -65 |
| GABA (SACinhib) | -60 | -5 |

The GABA driving force is much smaller, so the per-pA → per-nS conversion factor is 13x larger for
GABA than for NMDA/AMPA. The wrapper must compute conductance with explicit per-channel reversal
potentials, not a single shared constant. Sign convention: NEURON's SEClamp `_ref_i` is positive
when current flows from clamp into cell; inward synaptic currents (NMDA/AMPA at -65 mV) will be
sourced by the clamp (negative i), so `g_soma_eq = abs(i_peak) / abs(V_clamp - E_rev)` is the
cleanest formulation.

### Baseline for Comparison: t0047 Per-Synapse-Direct Numbers

From [t0047]'s `results/results_summary.md` (lines 15-22), at gNMDA = 0.5 nS, the per-synapse direct
summed conductances (paper-comparison baseline this task replaces) are:

| Channel | PD (nS, summed) | ND (nS, summed) | Paper target PD / ND (nS) |
| --- | --- | --- | --- |
| NMDA | 69.55 +/- 5.86 | 33.98 +/- 1.83 | ~7.0 / ~5.0 |
| AMPA | 10.92 +/- 0.37 | 10.77 +/- 0.60 | ~3.5 / ~3.5 |
| GABA | 106.13 +/- 5.77 | 215.57 +/- 2.72 | ~12.5 / ~30.0 |

These are the t0047 values to plot side-by-side against the new SEClamp values and the paper targets
in the modality-comparison chart. The qualitative findings — AMPA ~direction-independent, GABA
ND/PD ~2x — should hold under SEClamp too if the modality is the only difference.

### Cell Build is Cached; Recorder Reset Required Between Trials

[t0047] discovered (`code/run_with_conductances.py:80-88`, lines 174-185) that [t0046]'s
`_ensure_cell()` builds the DSGC exactly once per Python process (state cached in `_CELL_STATE`),
which means SEClamp insertion only needs to happen once per process and the clamp / recorder vectors
persist across trials. Per-trial reset is just `recorder.resize(0)`. This is critical for wall-clock
— building the cell takes 30-60 s; running a trial is 5-10 s. The 32 trials this task needs
amortise to ~5 minutes after build.

## Reusable Code and Assets

### Library: `modeldb_189347_dsgc_exact` (created by [t0046])

* **Source**:
  `tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/library/modeldb_189347_dsgc_exact/`
* **Reuse method**: **import via library**.
* **Import paths**:
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun import run_one_trial, _ensure_cell, TrialResult, get_dt_ms, get_tstop_ms`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.build_cell import build_dsgc, assert_bip_positions_baseline, read_synapse_coords, get_cell_summary, reset_globals_to_canonical`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.constants import Direction, ExperimentType, V_INIT_MV, TSTOP_MS, DT_MS, B2GNMDA_CODE, B2GAMPA_NS, E_SACINHIB_MV`
  * `from tasks.t0046_reproduce_poleg_polsky_2016_exact.code.neuron_bootstrap import ensure_neuron_importable`
* **Key signatures**:
  * `run_one_trial(*, exptype: ExperimentType, direction: Direction, trial_seed: int, flicker_var: float = 0.0, stim_noise_var: float = 0.0, b2gnmda_override: float | None = None, record_spikes: bool = False) -> TrialResult`
    — runs `h.simplerun()` and returns peak PSP. For SEClamp use, this task will *not* use
    `run_one_trial` directly because we need to intercept between `placeBIP()` and `run()` to attach
    the SEClamp; instead the new wrapper re-implements the post-`simplerun()` re-run pattern from
    `run_simplerun.py:135-151`.
  * `_ensure_cell() -> tuple[Any, list[SynapseCoords]]` — idempotent cell builder; returns the `h`
    handle and baseline BIP positions.
* **Adaptation needed**: none for the imports themselves. The new SEClamp wrapper builds on top of
  `_ensure_cell()` directly (same pattern as [t0047]'s `build_cell_and_attach_recorders`).
* **Line count of wrapper**: estimated ~250 lines (`run_seclamp.py` ~150,
  `run_full_seclamp_sweep.py` ~100).

### Pattern: Conductance recorder + post-trial reset

* **Source**: `tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py:91-186`.
* **Reuse method**: **copy into task** — adapt for SEClamp current vector instead of per-synapse
  conductance vectors.
* **What it does**: Attaches `Vector.record()` handles to NEURON state variables once after
  `_ensure_cell()`, runs trials repeatedly, calls `vec.resize(0)` between trials to reset.
* **Adaptation**: replace the `for idx in range(num_synapses): bip._ref_gAMPA / _ref_gNMDA / ...`
  loop with a single `i_rec.record(clamp._ref_i, dt_record_ms)` vector. Re-use the
  `_reset_recorders` and `_peak_summed_*` shape (one vector instead of 282).
* **Line count to copy**: ~50 lines of recorder management; rewrite the conductance-extraction
  arithmetic for the per-channel SEClamp formula.

### Pattern: Override-and-rerun branch from [t0046]'s `run_one_trial`

* **Source**: `tasks/t0046_reproduce_poleg_polsky_2016_exact/code/run_simplerun.py:135-151`.
* **Reuse method**: **copy into task** as the canonical channel-isolation rerun pattern.
* **What it does**: After `h.simplerun()` returns, if a global was overridden, re-applies the
  override, then calls `h("update()")`, `h("placeBIP()")`, attaches fresh recorder vectors,
  `h.finitialize(V_INIT_MV)`, `h.continuerun(TSTOP_MS)`. This is exactly the pattern needed for the
  AMPA-only / NMDA-only / GABA-only trials.
* **Adaptation**: between `placeBIP()` and `finitialize`, additionally `h.SEClamp(...)` and attach
  `i_rec.record(clamp._ref_i)`. Keep the SEClamp object alive (Python reference) for the duration of
  the trial.
* **Line count to copy / adapt**: ~20 lines.

### Constants and reversal potentials

* **Source**: `tasks/t0047_validate_pp16_fig3_cond_noise/code/constants.py:34-56`.
* **Reuse method**: **copy into task** — `E_BIPNMDA_MV`, `E_SACEXC_MV`, `E_SACINHIB_MV_OVERRIDE`,
  paper-target conductances, and `CONDUCTANCE_TOLERANCE_FRAC = 0.25` are all directly applicable.
* **Adaptation**: rename to t0049 module path, add `V_CLAMP_MV = -65.0` and the per-channel
  driving-force table; keep the runtime assertion that re-affirms `E_SACINHIB_MV` against [t0046]'s
  constant.
* **Line count to copy**: ~50 lines of constants.

### Paths module template

* **Source**: `tasks/t0047_validate_pp16_fig3_cond_noise/code/paths.py` (39 lines).
* **Reuse method**: **copy into task**, then rename per-figure PNG / CSV paths for the SEClamp
  outputs (`seclamp_conductance_pd_vs_nd.png`, `seclamp_vs_per_syn_direct_modality_comparison.png`).
* **Adaptation**: trivial path / filename rename.
* **Line count to copy**: ~30 lines.

## Lessons Learned

* **The cell-build cache is the wall-clock bottleneck**: [t0046] documented (and [t0047] confirmed)
  that `build_dsgc()` takes 30-60 s while a single trial is ~5-10 s. Re-using `_ensure_cell()` and
  resetting recorder vectors between trials is essential — never rebuild the cell mid-sweep.
* **`simplerun()` rebinds globals every call**: [t0046]'s `run_simplerun.py:100-138` shows that
  `h.simplerun()` writes `b2gnmda = 0.5*nmdaOn` and `achMOD = 0.33` unconditionally, clobbering any
  pre-call Python overrides. The override-and-rerun pattern (lines 135-151) is the only correct way
  to apply non-canonical conductance values; the SEClamp wrapper must do the same for `b2gampa` and
  `gabaMOD`.
* **`gabaMOD` controls stimulus amplitude, not conductance**: looking at
  `dsgc_model_exact.hoc:234, 253`, `gabaMOD` and `achMOD` multiply the `VampT` stimulus amplitude in
  the SAC inhib / SAC exc `mulnoise.fill` calls; they do not modify `gsingle_SACinhib` or
  `gsingle_SACexc`. Setting `gabaMOD = 0` zeroes the inhibitory wave drive (no presynaptic
  activation), which is sufficient to remove all GABA current from the trial and is the cleanest
  "GABA-off" switch.
* **Per-synapse direct conductance does not match the paper's Fig 3A-E units**: [t0047]'s
  carefully-audited `_ref_g` recorder gives 6-9x over on the summed scale and 28-90x under on the
  per-synapse-mean scale. The compare-literature analysis (`results/compare_literature.md`) isolated
  the most likely cause as the modality difference (per-synapse direct vs somatic voltage-clamp) —
  the rationale this task acts on. If the SEClamp values still mismatch, the next investigation is
  the supplementary Methods PDF (S-0046-05) for the paper's exact clamp protocol.
* **DSI is robust across measurement modality** (per [t0047]'s compare-literature, line 95). This
  task should also report SEClamp PD/ND ratios alongside absolute amplitudes — the ratio is more
  likely to match the paper than the absolute nS value.
* **The bipolarNMDA dual-component synapse releases AMPA and NMDA on the same vesicle event**.
  Setting `b2gampa = 0` does not stop NMDA release (and vice versa), making the ampa-only /
  nmda-only isolation trials valid. This is a non-obvious property without reading the MOD file
  directly.

## Recommendations for This Task

1. **Import [t0046]'s library wholesale**. Use `_ensure_cell()` to build the DSGC, then attach the
   SEClamp once per process. Do **not** call `run_one_trial` directly — it runs `simplerun()`
   end-to-end and returns before the SEClamp can be attached. Instead, copy the override-and-rerun
   branch from `run_simplerun.py:135-151` and insert the SEClamp between `placeBIP()` and
   `finitialize`.
2. **Use four channel-isolation trial types** with the override pairs identified in Key Findings:
   `(b2gnmda=0, gabaMOD=0)` for AMPA-only, `(b2gampa=0, gabaMOD=0)` for NMDA-only,
   `(b2gnmda=0, b2gampa=0)` for GABA-only, no overrides for full. Run 4 trials each at PD and ND for
   variance estimates — total 32 trials.
3. **SEClamp parameters**: `dur1 = h.tstop`, `amp1 = -65.0`, `rs = 0.001`. Verify the soma voltage
   trace stays clamped at -65 mV by recording `h.RGC.soma(0.5)._ref_v` alongside `clamp._ref_i` and
   asserting the soma trace SD over the trial is below ~0.5 mV.
4. **Per-channel conductance formula**: `g_nS(t) = abs(i_clamp_nA(t) * 1000) / abs(V_clamp - E_rev)`
   with `E_rev = 0` for AMPA/NMDA and `E_rev = -60` for GABA. The peak across the trial gives the
   per-channel summed somatic-equivalent conductance to compare with the paper.
5. **Centralise paths and constants** in `code/paths.py` and `code/constants.py` per the project
   style guide; copy [t0047]'s patterns and rename. Re-affirm `E_SACINHIB_MV` against [t0046]'s
   constant via runtime assertion.
6. **Expected wall-clock**: 32 trials at ~5 s each plus ~60 s cell build = ~4 minutes. Local CPU
   only; no remote machine.
7. **For the comparison chart**: include three bars per channel × direction — paper target, t0047
   per-synapse-summed, this task's SEClamp. Use the t0047 numbers in Key Findings as the baseline.
   Plot in `results/images/seclamp_conductance_pd_vs_nd.png` and
   `results/images/seclamp_vs_per_syn_direct_modality_comparison.png` per the task description.
8. **Verdict per channel × direction**: tolerance is `CONDUCTANCE_TOLERANCE_FRAC = 0.25` from
   [t0047]'s constants. H1 if all 6 channel × direction cells fall within +/- 25% of paper; H2 if
   some but not all; H0 if SEClamp values are essentially equal (within 10%) to t0047's
   per-synapse-summed values.

## Task Index

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: Establishes the NEURON 8.2.7 environment that this task runs in. The deposited DSGC
  and the SEClamp insertion both depend on the toolchain and compiled MOD DLL produced by this task.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: First port of the ModelDB 189347 DSGC. Predates the [t0046] exact reproduction this
  task imports; documented here only for lineage. Not imported by this task.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Exact reproduction of Poleg-Polsky and Diamond 2016 from ModelDB 189347
* **Status**: completed
* **Relevance**: Direct dependency. Provides the `modeldb_189347_dsgc_exact` library and the
  `run_one_trial` API that this task wraps. The override-and-rerun pattern in
  `run_simplerun.py:135-151` is the canonical template for the SEClamp insertion path.

### [t0047]

* **Task ID**: `t0047_validate_pp16_fig3_cond_noise`
* **Name**: Validate Poleg-Polsky 2016 Fig 3A-F conductances and extend noise sweep
* **Status**: completed
* **Relevance**: Direct dependency. Provides the per-synapse-direct conductance baseline this task
  re-measures under SEClamp. Its `code/run_with_conductances.py` recorder pattern is copied (and
  adapted from per-synapse to SEClamp) here. Its compare-literature analysis is the explicit
  motivation for this task (the modality hypothesis to test).
