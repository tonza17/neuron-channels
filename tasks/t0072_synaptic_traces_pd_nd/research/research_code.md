---
spec_version: "1"
task_id: "t0072_synaptic_traces_pd_nd"
research_stage: "code"
tasks_reviewed: 14
tasks_cited: 11
libraries_found: 13
libraries_relevant: 2
date_completed: "2026-05-01"
status: "complete"
---
# Research Code: Per-Synapse PD/ND Conductance Traces on Bed A and Bed B

## Task Objective

Run one PD trial and one ND trial on each of the two model beds (Bed A: Poleg-Polsky 2016 deposited
DSGC under the t0020 gabaMOD swap; Bed B: de Rosenroll 2026 DSGC under the t0066 bar-angle swap),
record per-synapse conductance state variables (`gAMPA`, `gNMDA` for Bed A's `bipNMDA`; `g` for
`SACinhib`, `SACexc`, `Exp2Syn` ACh, `Exp2Syn` GABA) and the local membrane voltage at each synapse
insertion point, then plot population mean +/- SD per synapse type with PD and ND overlaid. Compute
current `I(t) = g(t) * (v_local(t) - E_rev)` post-hoc. Produce two multi-panel PNGs and a
Typst-typeset PDF. The implementation is mostly *recording* and *plotting*: the cell-build,
PD/ND-encoding, and trial-runner code already exist in dependency tasks and need only thin wrappers
+ a per-synapse recorder array that mirrors [t0048] / [t0047]'s pattern.

## Library Landscape

The library aggregator script is not present in this branch's `arf/scripts/aggregators/` (only the
metadata aggregators are wired here, consistent with [t0070]'s finding). Libraries were enumerated
by globbing `tasks/*/assets/library/*/details.json`. 13 libraries exist; only 2 are directly
relevant to this task. None has corrections registered, so aggregator output (when available) would
reflect raw files.

* **`modeldb_189347_dsgc`** v0.1.0, created by [t0008]. Path:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. Categories:
  `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`. Wraps the Poleg-Polsky
  2016 ModelDB 189347 sources. Module entry points include `build_dsgc()` and `apply_params()`. The
  cell exposes `h.RGC.BIPsyn[i]` (POINT_PROCESS bipNMDA), `h.RGC.SACinhibsyn[i]` (POINT_PROCESS
  SACinhib), and `h.RGC.SACexcsyn[i]` (POINT_PROCESS SACexc) arrays of length `h.RGC.numsyn` (= 282
  in the canonical config). **Highly relevant** — Bed A's cell builder. Import path:
  `from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords, SynapseCoords`.

* **`de_rosenroll_2026_dsgc`** v0.1.0, created by [t0024]. Path:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`. Categories:
  `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `dendritic-computation`. Provides `build_dsgc_cell()` returning a `DSGCCell` dataclass with
  `terminal_dends`, `terminal_locs_xy`, `origin_xy`. **Highly relevant** — Bed B's cell builder.
  Import path:
  `from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell, DSGCCell`.

Other libraries discovered but not relevant to this trace-recording task: `tuning_curve_loss`
(t0012), `tuning_curve_viz` (t0011), `modeldb_189347_dsgc_gabamod` ([t0020] — a thin package
wrapper around t0008; not needed because [t0020]'s `code/run_gabamod_sweep.py` directly uses t0008's
library), `modeldb_189347_dsgc_dendritic` (t0022), `modeldb_189347_dsgc_exact` ([t0046] — an exact
reproduction with the GUI-stripped derivative; not needed because the t0008 library already exposes
the same synapse arrays), and the `minimal_dsgc_*` family (t0052 through t0059, single-compartment
toy models). None expose synaptic-recorder utilities directly.

## Key Findings

### Bed A: synapse arrays exposed as `h.RGC.BIPsyn[i]`, `h.RGC.SACinhibsyn[i]`, `h.RGC.SACexcsyn[i]`

Bed A's `RGCmodel.hoc` constructor (the `init` proc) declares
`objref SACinhibsyn[numsyn], SACexcsyn[numsyn], BIPsyn[numsyn]` at line 11828 of
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/RGCmodel.hoc`. The
placement loop at L11832-11850 iterates `forsec ON{...}` (the ON dendrites identified by
`z3d(n3d()-1) >= -0.16*y3d(n3d()-1)+46`, RGCmodel.hoc L11801-11803) and creates one of each synapse
type **at the section midpoint** (`new SACinhib(.5)`, `new SACexc(.5)`, `new bipNMDA(.5)`,
L11835/11836/11841). With the canonical `numsynperdend=1` and `numdendskip=1` (L11825,
`countON=numsyn=282`), this produces 282 BIPsyn + 282 SACinhibsyn + 282 SACexcsyn = 846 point
processes total, all at the midpoint of distinct ON dendrite sections [t0008].

The HOC constructor saves *no Python-side handle to the section* — the synapse object lives at
`h.RGC.BIPsyn[i]` and is implicitly anchored to the section it was created in. To recover the parent
segment from Python, use `pp.get_segment()` (NEURON's standard accessor). This returns the nrn
`Segment` object at the midpoint, from which `seg._ref_v` gives the local membrane voltage
reference. The section is `seg.sec`. We will use this in the recording loop (see "Recording stubs"
below).

### Bed A: `bipNMDA.gAMPA`, `bipNMDA.gNMDA` are RANGE; `SACinhib.g`, `SACexc.g` are RANGE

Confirmed by inspecting the MOD files:

* `bipolarNMDA.mod` L7-8: `RANGE Vpre,Vdel,Vdur,Vamp,Vbase,locx,locy,local_v,i,g,release,numves` and
  `RANGE gAMPA,gNMDA,s_inf,t1,A,B,Vinf`. Both `gAMPA` (declared in `STATE` at L73) and `gNMDA`
  (declared in `ASSIGNED` at L65) are exposed as RANGE variables. Reversal `e=0 mV` (PARAMETER L42,
  GLOBAL not RANGE — but constant, so safe to use as a single value). `local_v` is RANGE on L7 and
  equals `v*(1-Voff)+Vset*Voff` (L101); with project default `Voff=0`, this equals the postsynaptic
  `v` directly.

* `SAC2RGCinhib.mod` L7-8: `RANGE release,numves,g,s_inf,t1,i,g` and `RANGE locx,locy,local_v`. So
  `g` is RANGE (declared in `STATE` L45). Reversal `e` is GLOBAL on L6 — runtime value
  `e_SACinhib = -60 mV` ([t0008] `code/build_cell.py` L314 `h.e_SACinhib = E_SAC_INHIB_MV=-60.0`).
  `local_v` is RANGE L8 and equals `v` (L56 `local_v=v`).

* `SAC2RGCexc.mod` L7-8: identical layout. `g` RANGE, `e` GLOBAL = 0 mV (PARAMETER L25, never
  overridden), `local_v` RANGE.

These RANGE declarations are *exactly* what NEURON's Python-side `Vector.record(syn._ref_X, dt)`
needs. There is no need for a custom MOD edit or a wrapper mechanism.

### Bed A precedent: [t0048]/[t0047] already implement the exact recorder pattern this task needs

`tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` L100-150 contains the canonical
recorder-attachment function used by t0048's NMDA-flatness sweep — copied from
`tasks/t0047_validate_pp16_fig3_cond_noise/code/run_with_conductances.py` per the project's
cross-task reuse rule (since neither t0047 nor t0048 is library-registered). The pattern is:

```python
for idx in range(num_synapses):
    bip = h.RGC.BIPsyn[idx]
    sacexc = h.RGC.SACexcsyn[idx]
    sacinhib = h.RGC.SACinhibsyn[idx]
    v_ampa = h.Vector(); v_ampa.record(bip._ref_gAMPA, dt_record_ms)
    v_nmda = h.Vector(); v_nmda.record(bip._ref_gNMDA, dt_record_ms)
    v_sacexc = h.Vector(); v_sacexc.record(sacexc._ref_g, dt_record_ms)
    v_sacinhib = h.Vector(); v_sacinhib.record(sacinhib._ref_g, dt_record_ms)
```

Both tasks use `DT_RECORD_MS = 0.25` ([t0048] `code/constants.py` L31, [t0047] same value). They
also record `v_soma = h.RGC.soma(0.5)._ref_v` and `t_rec = h._ref_t` at the same dt. **What they do
NOT do**: record per-synapse local v. They use a single soma v as a proxy when computing
`I = g * (v_soma - e)`. For the present task we need the **per-synapse local v** (the dendritic v at
the synapse insertion point), because the same synaptic conductance produces wildly different
currents at different dendritic compartments. This is the one extension over [t0048]'s pattern.

The t0049 SEClamp re-measurement task ([t0049] `code/run_seclamp.py` L138-143) demonstrates the
generic `Vector.record(handle, DT_RECORD_MS)` idiom with `dt_record_ms = 0.25` for a single
recorder; the per-synapse extension is just iterating this over the synapse arrays.

### Bed A: PD/ND encoded by `h.gabaMOD = 0.33 (PD) | 0.99 (ND)`, applied via re-`update()` + re-`placeBIP()`

[t0020]'s `code/run_gabamod_sweep.py` `run_one_trial_gabamod` (L130-182) is the canonical reference
for the swap. The flow:

1. `apply_params(h, seed=seed)` ([t0008] `code/build_cell.py` L280-316) — writes the canonical
   constants including `h.gabaMOD = GABA_MOD = 0.33` (the default).
2. `h.gabaMOD = gabamod_value` (L149 — overrides with per-trial value).
3. `h("update()")` then `h("placeBIP()")` (L154-155) — re-runs the HOC stimulus generator so the
   inhibitory point processes pick up the new modulation envelope. The `gabaMOD` scalar enters at
   `mulnoise.fill(VampT*gabaMOD,...)` (`dsgc_model.hoc` L242), modulating the active portion of the
   SAC inhibitory drive trace which then plays into `SACinhibsyn[i].Vinf`.
4. Optional guard: `_assert_bip_positions_baseline(h, baseline_coords)` (L106-127) confirms that BIP
   synapse coordinates are still at their baseline (no rotation re-engaged).
5. `h.finitialize(V_INIT_MV)`; `h.continuerun(TSTOP_MS)`.

PD/ND constants: `GABA_MOD_PD = 0.33`, `GABA_MOD_ND = 0.99` ([t0020] `code/constants.py` L37-38;
mirrored in [t0065] `code/constants.py` L30-31).

Trial duration: `TSTOP_MS = 1000.0 ms`, `DT_MS = 0.1 ms` ([t0008] `code/constants.py` L18-19; same
values used by [t0020] and [t0065]).

### Bed B: synapses are Python-side `h.Exp2Syn` instances on the terminal dendrites

[t0024]'s `code/run_tuning_curve.py` `_setup_synapses` (L189-226) creates the Bed B synapses in
Python:

```python
for dend in cell.terminal_dends:
    syn_e = h.Exp2Syn(0.5, sec=dend)
    syn_e.tau1 = C.ACH_TAU1_MS    # 0.1 ms
    syn_e.tau2 = C.ACH_TAU2_MS    # 4.0 ms
    syn_e.e = C.ACH_EREV_MV       # 0 mV
    syn_i = h.Exp2Syn(0.5, sec=dend)
    syn_i.tau1 = C.GABA_TAU1_MS   # 0.5 ms
    syn_i.tau2 = C.GABA_TAU2_MS   # 12.0 ms
    syn_i.e = C.GABA_EREV_MV      # -60 mV
    # ... NetStim + NetCon wiring, weight = ACH_WEIGHT_US / GABA_WEIGHT_US
    bundle.syns_ach.append(syn_e)
    bundle.syns_gaba.append(syn_i)
```

The function returns a `SynapseBundle` dataclass with `syns_ach: list[Any]` and
`syns_gaba: list[Any]` lists, indexed in the same order as `cell.terminal_dends`. Each `Exp2Syn` is
at the section midpoint (0.5) of a terminal dendrite. Since `Exp2Syn` is NEURON's built-in
mechanism, its `g` is exposed as `syn._ref_g` (post-factor conductance, ready for I = g*(v-e)).

The number of terminal dendrites depends on morphology traversal at runtime (the `_map_tree` helper
at [t0024] `code/build_cell.py` L140-168 walks the tree from the soma); upstream's description of
~177 terminals is the expected count. `gaba_weight_scale=1.0` matches the correlated-condition
setting used by [t0066] (`code/run_protocol.py` L406).

### Bed B: PD/ND encoded by bar `direction_deg = 0.0 (PD) | 180.0 (ND)`

[t0066]'s `code/run_protocol.py` `_direction_deg` (L111-114) returns `DIRECTION_PD_DEG = 0.0` for PD
and `DIRECTION_ND_DEG = 180.0` for ND ([t0066] `code/constants.py` L19-20). The direction enters via
`_bar_arrival_times` ([t0024] `code/run_tuning_curve.py` L92-109): the bar arrival time at each
terminal synapse is `BAR_START_TIME + (proj_xy - BAR_X_START) / velocity` where `proj_xy` is the dot
product of the synapse XY offset and the unit velocity vector. PD = 0° (rightward), ND = 180°
(leftward).

Direction also modulates GABA release probability via `_gaba_prob_for_direction` ([t0024]
`code/run_tuning_curve.py` L80-89), a sigmoid from `pref_prob = 0.05` (PD) to `null_prob = 0.80`
(ND). This is *the* direction-encoding mechanism for Bed B GABA.

Trial runner: [t0066] `code/run_protocol.py` `_run_one_trial` (L205-298) is the canonical Bed B
trial loop. It sets up bar arrival times, AR(2) noise (with `RHO_CORRELATED = 0.6`), Poisson events
queued via `FInitializeHandler`, then `h.finitialize(V_INIT_MV)` + `h.run()`. Trial duration:
`C24.TSTOP_MS = 1000.0 ms`, `C24.DT_MS = 0.1 ms`, `STEPS_PER_MS = 10` ([t0024] `code/constants.py`
L19-23). Seed pattern: `seed = SEED_BASE + key.trial_index` with separate
`rng = np.random.default_rng(seed + 1_000_003)` for the Poisson event sampler ([t0066]
`code/run_protocol.py` L218, L239).

### Per-synapse local v: use `pp.get_segment()._ref_v` for both beds

NEURON's `POINT_PROCESS.get_segment()` returns the `nrn.Segment` the point process is attached to.
The segment's `_ref_v` is the membrane voltage at that compartment, identical to what
`section(x)._ref_v` returns when `x` is the same midpoint. For Bed A's synapses, all three types
(BIPsyn[i], SACinhibsyn[i], SACexcsyn[i]) sit on the **same** ON dendrite section at the same
midpoint x=0.5 (`RGCmodel.hoc` L11835-11841), so a single `v_local` recorder per ON dendrite is
sufficient — but it is simpler and not measurably more expensive to record three identical v_local
traces, one per synapse type, indexed parallel to the synapse arrays. For Bed B, ACh and GABA
likewise share the same terminal section midpoint ([t0024] `code/run_tuning_curve.py` L194-203 both
use `h.Exp2Syn(0.5, sec=dend)` on the same `dend`), so the same applies.

Alternative (Bed A only): record `bip._ref_local_v`, `sacexc._ref_local_v`, `sacinhib._ref_local_v`
directly via the `local_v` RANGE variables already exposed in the MOD files. This works for Bed A
(all three MODs declare `RANGE local_v` and write `local_v=v` or `local_v=v*(1-Voff)+Vset*Voff` in
the BREAKPOINT). For Bed B (Exp2Syn), no `local_v` is exposed — must use
`syn.get_segment()._ref_v`. **Recommendation: use `pp.get_segment()._ref_v` uniformly across both
beds for code consistency.**

### Recording dt: 1 ms gives ~1000 samples per trial, ~5 MB total

NEURON's `Vector.record(_ref_x, dt)` resamples the recorded reference at intervals of `dt` ms
(NEURON evaluates the variable at `t = 0, dt, 2*dt, ...`). Both [t0048] and [t0049] use
`DT_RECORD_MS = 0.25` (4000 samples per 1000 ms trial). For the present task:

* Synaptic conductance rise times: AMPA ~2 ms (`tauAMPA=2 ms`), GABA Bed A ~30 ms decay
  (`tau_SACinhib=30 ms`), GABA Bed B 0.5 + 12 ms (rise+decay), ACh ~3 ms (Bed A) or 0.1 + 4 ms (Bed
  B). All on the ms scale.
* Sampling at **1 ms** captures these shapes faithfully (Nyquist >= 2-fold oversampling for the
  fastest 0.1 ms rise of Bed B's ACh, which is acceptable since the rise transient is brief and the
  *peak* and decay are what matter for the population mean +/- SD plot).
* Memory: 1000 samples per trace * 8 bytes (float64) = 8 kB per trace. Bed A: 282 synapses * 4
  g-traces + 282 v-traces = 1410 traces => ~11 MB raw per trial; * 2 directions = 22 MB. Bed B: ~177
  synapses * 2 g-traces + 177 v-traces = ~531 traces => ~4 MB per trial; * 2 = 8 MB. Total raw <50
  MB across both beds and both directions. Compressed `.npz` will be much less.

**Recommendation: `RECORD_DT_MS = 1.0` for all conductance and voltage traces.** This satisfies the
task description's risk-mitigation #1 ("subsample to 1 sample per ms") preemptively. The existing
[t0048]/[t0047] convention of 0.25 ms is finer than needed for the visualization-focused goal here.

### Reversal potentials for post-hoc current computation

The task computes `I(t) = g(t) * (v_local(t) - E_rev)` post-hoc, in Python, after the simulation.
The reversal potentials per channel:

* **Bed A AMPA** (`bipNMDA.gAMPA` portion): `e = 0 mV` (`bipolarNMDA.mod` L42; not overridden). Code
  constant: [t0048] `code/constants.py` L38 `E_BIPNMDA_MV = 0.0`.
* **Bed A NMDA** (`bipNMDA.gNMDA` portion): `e = 0 mV` (same as AMPA — bipNMDA uses one reversal
  for both currents).
* **Bed A GABA** (`SACinhib.g`): `e = -60 mV` (effective runtime: `e_SACinhib = -60` is GLOBAL, set
  in [t0008] `code/build_cell.py` L314 `h.e_SACinhib = E_SAC_INHIB_MV=-60.0`). Code constant:
  [t0008] `code/constants.py` `E_SAC_INHIB_MV = -60.0`.
* **Bed A ACh** (`SACexc.g`): `e = 0 mV` (`SAC2RGCexc.mod` L25; never overridden). Code constant:
  [t0048] `code/constants.py` L39 `E_SACEXC_MV = 0.0`.
* **Bed B ACh** (`Exp2Syn.g`): `e = 0 mV` ([t0024] `code/constants.py` L47 `ACH_EREV_MV = 0.0`).
* **Bed B GABA** (`Exp2Syn.g`): `e = -60 mV` ([t0024] `code/constants.py` L52
  `GABA_EREV_MV = -60.0`).

Unit note: bipNMDA's BREAKPOINT computes `iAMPA = (1e-3) * gAMPA * (v - e)` (`bipolarNMDA.mod` L103)
— `gAMPA` is in nS, `v - e` in mV, and the 1e-3 factor converts nS*mV = pA to nA (NEURON's
canonical current unit). The task description says to plot I in pA, so the post-hoc computation
should use `I_pA = g_nS * (v_local_mV - e_mV)` directly (no 1e-3 factor); the result is in pA
already. SACinhib and SACexc apply the same 1e-3 in their BREAKPOINTs (`SAC2RGCinhib.mod` L55,
`SAC2RGCexc.mod` L55), confirming the unit convention.

Bed B's Exp2Syn does NOT have a unit-prefix convention — `Exp2Syn.g` is in microsiemens (µS) by
NEURON convention because the NetCon weight (which determines event size) is unitless multiplied by
µS. **Bed B units to be careful with**: `g_Bed_B_uS * (v - e)_mV = nA`. To plot I in pA across both
beds: multiply Bed B's I by 1000 to convert nA -> pA, OR convert Bed B's `g` from µS to nS
(multiply by 1000) and apply `I_pA = g_nS * (v - e)_mV` uniformly. The latter is cleaner and is what
the task description implies ("converted to nS for plotting consistency").

### Cell-build idempotence and trial isolation

For Bed A: [t0048] `code/run_with_conductances.py` documents that
`build_cell_and_attach_recorders()` is idempotent — `_ensure_cell()` (from [t0046] / mirrored in
the t0008-based usage) builds the cell exactly once per process, then recorders are attached once.
Across trials, `apply_params()` rewrites the global parameters, `update()` + `placeBIP()` re-seat
the stimulus drivers, and the recorder vectors **persist** because the synapse POINT_PROCESS objects
persist (only `Vinf` playback vectors get re-bound, not the synapses themselves). After each
`h.continuerun`, `list(v_rec)` extracts the trace as Python floats; then the recorder's internal
buffer can be cleared with `v_rec.resize(0)` or simply reused on the next `finitialize` (NEURON
resets recorder buffers on `finitialize` automatically).

For Bed B: [t0066] `code/run_protocol.py` `_run_one_trial` (L205-298) follows the same pattern —
`_restore_canonical_state()` (L157-175) resets weights and HHst conductances;
`_apply_mode_overrides()` (L178-194) silences synapses for EPSP/IPSP mode; then `h.finitialize` +
`h.run`. Recorders attached once before the first trial work across all subsequent trials.

For this task we run **only 2 trials per bed (PD + ND)** so per-trial setup overhead is negligible.
Build cell once per bed; attach recorders once per bed; iterate (PD, ND).

### Typst PDF compilation: reuse [t0071]'s render_pdf.py verbatim

[t0071]'s `code/render_pdf.py` (59 lines total) compiles a Typst source to PDF via
`import typst; typst.compile(source, output=output)`. The dependency is a pure-Python pip package
— no LaTeX install needed. The function `compile_typst(*, source_path, output_path)` returns a
`CompileResult` dataclass with `output_size_bytes`. A `MIN_PDF_SIZE_BYTES = 50_000` warn threshold
is enforced. For this task, we copy `render_pdf.py` verbatim (just retargeting paths), and write a
Typst source `results/results_detailed.typ` that includes
`#image("images/bed_a_synaptic_traces.png")` and the same for Bed B.

## Reusable Code and Assets

### Bed A cell-build + parameter application (import via library)

**Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py` (registered library
`modeldb_189347_dsgc`).

**What to use**:

* `build_dsgc() -> Any` (L129-175): loads NEURON, sources HOC, runs `init_sim` + `init_active` +
  `update`. Returns `h` with `h.RGC` populated.
* `apply_params(h: Any, *, seed: int) -> None` (L280-316): writes canonical Poleg-Polsky parameters
  (`h.b2gampa`, `h.b2gnmda`, `h.s2ggaba`, `h.s2gach`, `h.gabaMOD = 0.33`, `h.achMOD`, light-bar
  geometry, `h.tau1NMDA_bipNMDA`, `h.e_SACinhib`, `h.n_bipNMDA`, `h.gama_bipNMDA`).
* `read_synapse_coords(h: Any) -> list[SynapseCoords]` (L192-208): used to capture baseline
  positions for the gabaMOD-swap protocol (matches [t0020]'s pattern).
* `SynapseCoords` dataclass (L63-73): for the position-baseline guard.

**Reuse method**: import via library —
`from tasks.t0008_port_modeldb_189347.code.build_cell import build_dsgc, apply_params, read_synapse_coords, SynapseCoords`.

**Adaptation needed**: none. Call `build_dsgc()` once per process; call `apply_params(h, seed=...)`
at the start of each trial; immediately set `h.gabaMOD = GABA_MOD_PD or GABA_MOD_ND`; call
`h("update()")` + `h("placeBIP()")`; then `h.finitialize(V_INIT_MV)` + `h.continuerun(TSTOP_MS)`.

### Bed A constants (import via library)

**Source**: `tasks/t0008_port_modeldb_189347/code/constants.py` (registered library
`modeldb_189347_dsgc`).

**What to use**: `TSTOP_MS = 1000.0`, `DT_MS = 0.1`, `CELSIUS_DEG_C`, `V_INIT_MV = -65.0`,
`AP_THRESHOLD_MV`, `E_SAC_INHIB_MV = -60.0`, all the synaptic conductance scalars (`B2GAMPA_NS`,
`B2GNMDA_NS`, `S2GGABA_NS`, `S2GACH_NS`).

**Reuse method**: import via library —
`from tasks.t0008_port_modeldb_189347.code.constants import TSTOP_MS, DT_MS, V_INIT_MV, E_SAC_INHIB_MV`.

### Bed A PD/ND constants and trial-setup pattern (copy into task)

**Source**: `tasks/t0020_port_modeldb_189347_gabamod/code/constants.py` L37-38 (PD/ND values) and
`tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py` L130-160
(`run_one_trial_gabamod` flow without the spike-counting tail).

**What to use**: `GABA_MOD_PD = 0.33`, `GABA_MOD_ND = 0.99`. Mirror the order of operations:
`apply_params -> override h.gabaMOD -> h("update()") -> h("placeBIP()") -> attach recorders -> finitialize -> continuerun`.

**Reuse method**: copy into task. [t0020] is not library-registered (it owns
`modeldb_189347_dsgc_gabamod` library which is just a wrapper, not the driver itself). The two
constants are 2 lines; the trial-setup flow is ~30 lines. Both go into
`tasks/t0072_synaptic_traces_pd_nd/code/record_synapses.py`.

**Adaptation needed**: drop the spike-counting tail (we record raw traces, not firing rates). Do not
call `_assert_bip_positions_baseline` unless we are doing rotation; for PD/ND swap with no rotation,
the assertion is a no-op safety check that can be retained as-is.

### Bed A per-synapse recorder pattern (copy into task)

**Source**: `tasks/t0048_voff_nmda1_dsi_test/code/run_with_conductances.py` L100-150
(`attach_conductance_recorders`) and the `ConductanceRecorders` dataclass L47-61.

**What to use**: the loop over `range(h.RGC.numsyn)` that creates `Vector.record(syn._ref_X, dt)`
handles for `bip._ref_gAMPA`, `bip._ref_gNMDA`, `sacexc._ref_g`, `sacinhib._ref_g`.

**Reuse method**: copy into task. [t0048] is not library-registered.

**Adaptation needed**: extend the recorder set with **per-synapse local v** — for each synapse
type, also create `v_local = h.Vector(); v_local.record(syn.get_segment()._ref_v, RECORD_DT_MS)`.
Replace [t0048]'s `DT_RECORD_MS = 0.25` with `RECORD_DT_MS = 1.0` (see "Recording dt" finding
above). Drop the post-trial peak-summing logic (we save raw per-synapse traces to .npz, not summary
scalars). Estimated size: ~80 lines including the dataclass and the new v_local recorders.

### Bed B cell-build + synapse setup (import via library + copy synapse-setup)

**Source**: `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` (registered library
`de_rosenroll_2026_dsgc`) and `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`
L189-226 (`_setup_synapses`, `SynapseBundle`).

**What to use**:

* `build_dsgc_cell() -> DSGCCell` (L251-291 of `build_cell.py`): builds the Bed B cell with
  primary/non-terminal/terminal dendrites enumerated.
* `DSGCCell` dataclass (L94-106): provides `cell.h`, `cell.terminal_dends`, `cell.terminal_locs_xy`,
  `cell.origin_xy`, `cell.soma`.
* `_setup_synapses(*, cell: DSGCCell, gaba_weight_scale: float) -> SynapseBundle` (L189-226 of
  `run_tuning_curve.py`): creates Exp2Syn ACh and GABA on every terminal dendrite, with
  NetStim/NetCon wiring. Returns `SynapseBundle` with `syns_ach`, `syns_gaba`, `ncs_ach`,
  `ncs_gaba`, `netstims` lists.

**Reuse method**: `build_dsgc_cell` and `DSGCCell` — import via library
(`from tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell import build_dsgc_cell`).
`_setup_synapses` and `SynapseBundle` — copy into task (it is in `run_tuning_curve.py`, not the
library asset's documented entry points; the underscore-prefix indicates a private API). ~40 lines
to copy.

**Adaptation needed**: call `_setup_synapses(cell=cell, gaba_weight_scale=1.0)` (matching [t0066]
correlated-condition default at `code/run_protocol.py` L406). The bundle's `syns_ach[i]` and
`syns_gaba[i]` are the recording targets.

### Bed B trial driver (copy into task)

**Source**: `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py` L205-298
(`_run_one_trial` body) and L111-114 (`_direction_deg`).

**What to use**: the Bed B trial-setup logic — `_bar_arrival_times` call, `_rates_with_ar2_noise`
call, `_gaba_prob_for_direction` call, `_rates_to_events` call, `FInitializeHandler` to queue NetCon
events, `h.celsius / h.dt / h.steps_per_ms / h.v_init / h.tstop` setters, `h.finitialize`, `h.run`.
The PD/ND mapping is `direction_deg = 0.0 (PD) | 180.0 (ND)`.

**Reuse method**: copy into task. The helpers `_bar_arrival_times` (L92-109 of
`run_tuning_curve.py`), `_rates_with_ar2_noise` (L112-142), `_gaba_prob_for_direction` (L80-89),
`_rates_to_events` (L145-175) all live in [t0024]'s `run_tuning_curve.py` (not in the library's
documented entry points — copy these too). Plus the AR(2) module
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/ar2_noise.py` is library-registered (entry point
`generate_ar2_batch`) so import that.

**Adaptation needed**: drop the EPSP_PASSIVE / IPSP_PASSIVE mode logic from [t0066] — for this
task we only need the FULL mode (HH on, all synapses active). Use `RHO_CORRELATED = 0.6` ([t0066]
`code/constants.py` `RHO_CORRELATED`) for the AR(2) noise. Estimated ~150 lines copied (4 helpers +
1 trial runner stripped of mode-switching).

### Typst PDF compilation (copy into task)

**Source**: `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py` (59 lines).

**What to use**: `compile_typst(*, source_path: Path, output_path: Path) -> CompileResult` and the
`CompileResult` dataclass.

**Reuse method**: copy into task. [t0071] is not library-registered.

**Adaptation needed**: retarget the imports from `tasks.t0071_t0070_synaptic_eqs_pdf.code.paths` to
a new `tasks/t0072_synaptic_traces_pd_nd/code/paths.py` defining `TYPST_SOURCE_PATH` and
`PDF_OUTPUT_PATH`. The body of `compile_typst` is unchanged.

### Recording stubs (the implementation step will write these)

```python
# Per Bed A synapse i (one of 282 ON dendrites):
bip = h.RGC.BIPsyn[i]
sacinhib = h.RGC.SACinhibsyn[i]
sacexc = h.RGC.SACexcsyn[i]

v_g_ampa = h.Vector(); v_g_ampa.record(bip._ref_gAMPA, RECORD_DT_MS)
v_g_nmda = h.Vector(); v_g_nmda.record(bip._ref_gNMDA, RECORD_DT_MS)
v_g_gaba = h.Vector(); v_g_gaba.record(sacinhib._ref_g, RECORD_DT_MS)
v_g_ach  = h.Vector(); v_g_ach.record(sacexc._ref_g, RECORD_DT_MS)

# All four sit on the same ON dendrite midpoint, so v_local is the same for all.
seg = bip.get_segment()
v_v_local = h.Vector(); v_v_local.record(seg._ref_v, RECORD_DT_MS)

# Per Bed B synapse i (one of n_terminal terminal dendrites):
syn_ach = bundle.syns_ach[i]
syn_gaba = bundle.syns_gaba[i]

v_g_ach = h.Vector(); v_g_ach.record(syn_ach._ref_g, RECORD_DT_MS)
v_g_gaba = h.Vector(); v_g_gaba.record(syn_gaba._ref_g, RECORD_DT_MS)

# Both Bed B synapses share the same terminal section midpoint.
seg = syn_ach.get_segment()
v_v_local = h.Vector(); v_v_local.record(seg._ref_v, RECORD_DT_MS)
```

After `h.continuerun`, extract as numpy:
`g_ampa_trace = np.array(list(v_g_ampa), dtype=np.float64)`. Stack across synapses to a 2D array
`(n_synapses, n_samples)`. Save per (bed, direction, type) to `data/<bed>_<dir>_<type>.npz` keys
`g_traces`, `v_local_traces`, `t_ms` (the time vector, common to all traces).

## Lessons Learned

* **The full per-synapse recorder pattern is already validated**: [t0048] / [t0047]'s
  `attach_conductance_recorders` runs cleanly, was used to compute physiologically-meaningful peak
  conductances, and matches the SEClamp re-measurement results within 25% ([t0049] confirmed the
  per-synapse `_ref_g` recorder gives 6-9x larger somatic-equivalent conductance because
  voltage-clamp at the soma sees only the summed *post-electrotonic-attenuation* signal — see
  [t0049] `assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md`). For the
  visualization-focused goal of this task, the per-synapse direct recording is exactly what we want;
  we are not trying to compare to somatic-clamp values, so the [t0049] caveat does not apply.

* **Bed A's `gabaMOD` is the modulation envelope scalar**, not a per-vesicle peak. It scales the
  presynaptic voltage delivered to the SAC inhibitory point processes, which then linearly maps into
  Bernoulli release probability. The visible PD vs ND difference in `gGABA(t)` should be
  approximately a 3x amplitude scaling of the same time-domain shape, NOT a temporal shift.
  [t0070]'s research_code.md (Lessons Learned bullet 4) makes this explicit.

* **Bed A's NMDA voltage-dependence enters via `local_v`**, computed as
  `local_v = v*(1-Voff) + Vset*Voff` ([t0070] `research_code.md` L213). With `Voff=0` (project
  default), the Mg block uses `v` at the synapse — meaning the recorded `gNMDA(t)` already
  reflects voltage-gating in real time. This is what we want.

* **Bed B's Exp2Syn `g` is post-factor conductance**, ready for `I = g*(v-e)`. The risk description
  #2 in `task_description.md` flags this explicitly. NEURON's `Exp2Syn` BREAKPOINT computes
  `g = factor * (B - A)` where `factor` normalizes the dual-exponential to a peak of 1 per unit
  weight. The recorded `g_ref` is this normalized post-factor value.

* **NEURON `Vector.record(handle, dt)` resamples on a fixed grid**: the value is sampled at
  `t = 0, dt, 2*dt, ...` regardless of the simulator's adaptive time step. Trace lengths are
  predictable: `n_samples = int(tstop/dt) + 1`. [t0048]'s `_peak_summed_g_ns` (L153-166) defensively
  asserts all per-synapse vectors have the same length, catching the bug where a recorder is
  attached after `finitialize` (the first samples would be missing).

* **Bed A and Bed B run length is the same**: 1000 ms each ([t0008] `code/constants.py` L18, [t0024]
  `code/constants.py` L22). This means the time axis is identical across beds, which simplifies the
  side-by-side comparison.

* **Bed B's NMDA mechanism (Exp2NMDA) is vendored but not wired**: [t0070] research_code.md Lessons
  Learned bullet 3 makes this explicit. We do NOT record NMDA on Bed B because no Exp2NMDA instances
  exist. Only ACh and GABA are recorded, matching the task description.

* **Use `pp.get_segment()._ref_v` to access local voltage**, not `pp.get_loc()` (which returns the
  arc position 0..1 — useful for plotting but not for recording). The segment-resolved approach
  works uniformly across MOD POINT_PROCESS and built-in mechanisms (Exp2Syn).

* **Trial-isolation across PD and ND runs is automatic** if recorders are *not* re-attached between
  trials: NEURON resets recorder buffers on `finitialize`. But for PD/ND clarity we should attach a
  *fresh* set of recorders between trials so the .npz output is unambiguous. This costs ~0.1s per
  trial and avoids any stale-buffer ambiguity.

## Recommendations for This Task

1. **Library imports for cell builders**: import `build_dsgc` + `apply_params` from
   `tasks.t0008_port_modeldb_189347.code.build_cell` (Bed A) and `build_dsgc_cell` from
   `tasks.t0024_port_de_rosenroll_2026_dsgc.code.build_cell` (Bed B). Both libraries are registered.
   No copying needed for cell construction.

2. **Copy the per-synapse recorder pattern from [t0048]** into
   `tasks/t0072_synaptic_traces_pd_nd/code/record_synapses.py`. Extend it with per-synapse `v_local`
   recorders via `pp.get_segment()._ref_v` (the one extension over [t0048]'s pattern). Use
   `RECORD_DT_MS = 1.0` to keep memory and disk usage bounded.

3. **Copy [t0024]'s `_setup_synapses`, `SynapseBundle`, `_bar_arrival_times`,
   `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events`** from
   `code/run_tuning_curve.py` into the task's code folder. These helpers are not library-exposed.
   Strip the EPSP/IPSP mode logic when copying [t0066]'s `_run_one_trial` — we only need FULL.

4. **Save raw traces as compressed npz** per (bed, direction, synapse_type), with array shape
   `(n_synapses, n_samples)` for both `g_traces` and `v_local_traces`, plus a 1D `t_ms` array.
   Naming: `bed_a_{pd,nd}_{ampa,nmda,gaba,ach}.npz`, `bed_b_{pd,nd}_{ach,gaba}.npz`. Total 12 files
   across both beds and both directions.

5. **Compute current post-hoc** as `I_pA = g_nS * (v_local_mV - e_mV)`. Bed B's Exp2Syn returns `g`
   in µS — multiply by 1000 first to convert to nS, then apply the same formula. Reversal
   potentials per type from [t0008]/[t0024] constants (see "Reversal potentials" finding above).

6. **Plotting**: Bed A figure = 4 rows (AMPA, NMDA, GABA, ACh) x 2 cols (g, I), each panel with PD
   solid + ND solid + their +/- SD bands; Bed B figure = 2 rows (ACh, GABA) x 2 cols (g, I), same
   format. Use a consistent color scheme (PD = blue, ND = red is conventional in DS literature).
   Save as PNG into `results/images/`.

7. **PDF rendering**: copy [t0071]'s `code/render_pdf.py` verbatim, retarget paths to a local
   `paths.py`, and write `results/results_detailed.typ` that includes the two PNGs and prose. Use
   `python -c "import typst; typst.compile(...)"` invocation pattern.

8. **Suggested file layout** (per task plan): `code/paths.py`, `code/constants.py`,
   `code/record_synapses.py` (driver: build cells, attach recorders, run PD+ND, save .npz),
   `code/plot_traces.py` (load .npz, compute I post-hoc, render PNGs), `code/render_pdf.py` (copy
   from [t0071]). Keep each module under 300 lines.

9. **Trial-isolation**: build each cell once per process; attach a fresh set of recorders before
   each of the 4 trials (Bed A PD, Bed A ND, Bed B PD, Bed B ND); after each
   `h.continuerun(TSTOP_MS)`, immediately serialize traces to .npz then drop the recorder list so
   memory is reclaimed.

10. **No HH on/off toggling needed**: this task records FULL trials only (HH on, all synapses
    active). Skip the `_apply_mode_overrides` and `_snapshot_canonical_state` machinery from
    [t0065]/[t0066].

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Owns the `modeldb_189347_dsgc` library asset (Bed A's HOC + MOD sources + Python
  builder). `build_dsgc()`, `apply_params()`, `read_synapse_coords()`, and the `SynapseCoords`
  dataclass are all imported directly. The synapse arrays `h.RGC.BIPsyn[i]`, `h.RGC.SACinhibsyn[i]`,
  `h.RGC.SACexcsyn[i]` are the recording targets for Bed A.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Provides the canonical PD/ND constants (`GABA_MOD_PD = 0.33`, `GABA_MOD_ND = 0.99`)
  and the trial-setup pattern
  (`apply_params -> override gabaMOD -> update -> placeBIP -> finitialize -> continuerun`) that this
  task mirrors. The trial-runner body in `code/run_gabamod_sweep.py` is the template for Bed A's
  PD/ND swap.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Owns the `de_rosenroll_2026_dsgc` library asset (Bed B's HOC + MOD sources + Python
  builder). `build_dsgc_cell()` and `DSGCCell` are imported. `_setup_synapses` (the
  Exp2Syn-creator), `_bar_arrival_times`, `_rates_with_ar2_noise`, `_gaba_prob_for_direction`, and
  `_rates_to_events` from `code/run_tuning_curve.py` are copied because they are not library entry
  points.

### [t0046]

* **Task ID**: `t0046_reproduce_poleg_polsky_2016_exact`
* **Name**: Reproduce Poleg-Polsky 2016 exactly (deposited variant + GUI-stripped derivative)
* **Status**: completed
* **Relevance**: Source of the original `attach_conductance_recorders` pattern (its
  `code/run_simplerun.py` and `code/build_cell.py` provide the `_ensure_cell()` idempotence pattern
  that [t0047] / [t0048] / [t0049] all reuse). Has its own library `modeldb_189347_dsgc_exact`
  (parallel to t0008). Not directly needed for this task because the t0008 library exposes the same
  synapse arrays, but the recorder-attachment idiom traces back here.

### [t0047]

* **Task ID**: `t0047_validate_pp16_fig3_cond_noise`
* **Name**: Validate Poleg-Polsky 2016 Fig 3 conductances + noise scan on the deposited DSGC
* **Status**: completed
* **Relevance**: Origin of the `attach_conductance_recorders` function (later copied by [t0048] and
  [t0049]). `code/run_with_conductances.py` L91-141 is the canonical reference for attaching
  `Vector.record(syn._ref_gAMPA / _ref_gNMDA / _ref_g, dt)` per-synapse loops on Bed A. This task's
  recorder code copies this pattern with the addition of per-synapse `v_local`.

### [t0048]

* **Task ID**: `t0048_voff_nmda1_dsi_test`
* **Name**: Test Voff_bipNMDA=1 (voltage-independent NMDA) on DSI vs gNMDA flatness
* **Status**: completed
* **Relevance**: Provides a clean copy of the per-synapse recorder pattern
  (`code/run_with_conductances.py` L100-150) plus the `ConductanceRecorders` dataclass and the
  canonical reversal constants (`E_BIPNMDA_MV = 0.0`, `E_SACEXC_MV = 0.0`,
  `E_SACINHIB_MV_OVERRIDE = -60.0`). The task's `record_synapses.py` will copy this file and extend
  it with per-synapse `v_local` recorders.

### [t0049]

* **Task ID**: `t0049_seclamp_cond_remeasure`
* **Name**: Re-measure Fig 3A-E conductances under somatic SEClamp on the deposited DSGC
* **Status**: completed
* **Relevance**: Provides the simpler pattern `Vector.record(handle, DT_RECORD_MS)` with
  `dt_record_ms = 0.25` (`code/run_seclamp.py` L138-143) and the SEClamp comparison data showing
  per-synapse direct conductance is 6-9x larger than somatic-clamp equivalent. For this task this is
  informational only — we record per-synapse direct values and plot them, with no claim that they
  match somatic-clamp values.

### [t0065]

* **Task ID**: `t0065_t0020_epsp_ipsp_vm_protocol`
* **Name**: Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol
* **Status**: completed
* **Relevance**: Confirms the canonical PD/ND values for Bed A (`GABA_MOD_PD = 0.33`,
  `GABA_MOD_ND = 0.99`, `code/constants.py` L30-31) and that `tstop = 1000 ms` is the correct trial
  length for Bed A. We use only the FULL mode (skip the EPSP/IPSP machinery).

### [t0066]

* **Task ID**: `t0066_t0024_epsp_ipsp_vm_protocol`
* **Name**: Test t0024 de Rosenroll DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol
* **Status**: completed
* **Relevance**: Confirms the canonical PD/ND values for Bed B (`DIRECTION_PD_DEG = 0.0`,
  `DIRECTION_ND_DEG = 180.0`, `code/constants.py` L19-20) and that `tstop = C24.TSTOP_MS = 1000 ms`
  is correct for Bed B. The trial-runner body (`_run_one_trial` L205-298 of `code/run_protocol.py`)
  is the copy template for Bed B's trial-setup logic, with EPSP/IPSP mode logic stripped.

### [t0070]

* **Task ID**: `t0070_writeup_two_model_beds`
* **Name**: Writeup of the two canonical DSGC model beds
* **Status**: completed
* **Relevance**: This task's parent writeup. Its `research/research_code.md` is the single
  authoritative source for the file:line citations for every conductance and synaptic parameter on
  both beds. We reuse those citations directly. Its `results/results_detailed.md` (and [t0071]'s PDF
  derivative) is what these new visualization figures complement.

### [t0071]

* **Task ID**: `t0071_t0070_synaptic_eqs_pdf`
* **Name**: Add synaptic-current equations + Typst PDF to t0070's writeup
* **Status**: completed
* **Relevance**: Provides the Typst PDF compilation pipeline (`code/render_pdf.py`, 59 lines). This
  task copies that file verbatim with paths retargeted to render `results/results_detailed.typ` ->
  `results/results_detailed.pdf`.
