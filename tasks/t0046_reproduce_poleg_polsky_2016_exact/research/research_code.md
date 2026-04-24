---
spec_version: "1"
task_id: "t0046_reproduce_poleg_polsky_2016_exact"
research_stage: "code"
tasks_reviewed: 39
tasks_cited: 9
libraries_found: 6
libraries_relevant: 4
date_completed: "2026-04-24"
status: "complete"
---
# Research Code: Exact Reproduction of Poleg-Polsky 2016 (ModelDB 189347)

## Task Objective

Build a from-scratch independent port of ModelDB 189347 (library asset `modeldb_189347_dsgc_exact`)
that reproduces Poleg-Polsky & Diamond 2016 on its own reported metrics — PSP amplitudes (Figs
1-5), subthreshold ROC AUC (Fig 7), and Figure 8 qualitative suprathreshold behaviour — and
publish a line-by-line audit of **paper vs ModelDB code vs our reproduction** with a discrepancy
catalogue. The task explicitly forbids forking `[t0008]` or `[t0020]` and is strictly scoped to the
paper's metrics (spike-rate comparisons against the t0004 envelope are out of scope). This
code-research stage surveys existing libraries (bundled HOC/MOD sources already sitting inside
`[t0008]`'s library asset, scoring/visualisation helpers from `[t0011]` and `[t0012]`, and the
calibrated baseline morphology from `[t0005]`/`[t0009]`) to decide what can be imported via library
and what must be copied verbatim into the new task's `code/` directory per the cross-task import
rule.

## Library Landscape

Six registered library assets exist in the project. The library aggregator is not installed in this
repo (a direct `assets/library/*/details.json` scan was used instead). No library has been replaced
or corrected; all entries below reflect their original as-authored state.

| Library ID | Creating task | Version | Relevant? | Why |
| --- | --- | --- | --- | --- |
| `modeldb_189347_dsgc` | `[t0008]` | 0.1.0 | **Yes** (source bundle + API reference) | Ships the verbatim ModelDB 189347 HOC/MOD files (`main.hoc`, `RGCmodel.hoc`, `dsgc_model.hoc`, `HHst.mod`, `bipolarNMDA.mod`, `SAC2RGCinhib.mod`, `SAC2RGCexc.mod`, `SquareInput.mod`, `spike.mod`, `mosinit.hoc`, `model.ses`, `readme.html`/`.docx`) under `sources/` and a Python driver (`build_cell.py`, `constants.py`, `paths.py`, `run_tuning_curve.py`, `score_envelope.py`, `report_morphology.py`, `swc_io.py`, `run_nrnivmodl.cmd`). **Not importable as a library for t0046**: the driver is coupled to the t0008 rotation-proxy protocol, not the gabaMOD-swap protocol the paper actually uses. Treat the `sources/` HOC/MOD files as the **canonical upstream release** for t0046's new library asset. |
| `modeldb_189347_dsgc_gabamod` | `[t0020]` | 0.1.0 | **Yes** (gabaMOD protocol reference) | Sibling port using the paper-native PD=0.33 / ND=0.99 gabaMOD swap. Registered library asset but `code/` is empty (`.gitkeep` only); `module_paths` in `details.json` point at the **task's** `code/` directory, not at the asset's own `code/`. Effective code lives at `tasks/t0020_port_modeldb_189347_gabamod/code/` and imports t0008 build helpers cross-task, which the t0046 instructions forbid copying. The protocol logic itself (gabaMOD override + `update()`/`placeBIP()` refresh + baseline-BIP-position assertion) must be re-expressed in t0046's own code. |
| `modeldb_189347_dsgc_dendritic` | `[t0022]` | — | No | Testbed modification with channel-partitioned AIS and spatially-asymmetric inhibition; structurally diverges from Poleg-Polsky baseline. Not relevant for exact reproduction. |
| `de_rosenroll_2026_dsgc` | `[t0024]` | — | No | Different DSGC paper (de Rosenroll 2026), out of scope per task.json. |
| `tuning_curve_viz` | `[t0011]` | 0.1.0 | **Yes, import via library** | Matplotlib visualiser: Cartesian + polar tuning curves, multi-model overlays, per-angle raster + PSTH from `(angle_deg, trial_seed, firing_rate_hz)` and spike-time CSVs. Useful for Fig 1/Fig 4/Fig 5 direction-tuning plots; adapt to plot PSP amplitudes instead of rates. Import path: `from tasks.t0011_response_visualization_library.code.tuning_curve_viz import ...`. |
| `tuning_curve_loss` | `[t0012]` | 0.1.0 | **Yes, import via library** | Canonical scorer over DSI / peak / null / HWHM with weighted loss and envelope gate. **Not directly useful for the paper's PSP-amplitude / slope-angle / ROC-AUC metrics**, but its `compute_dsi`, `compute_peak_hz`, `compute_null_hz` helpers remain useful for Fig 8 secondary suprathreshold pass. Import path: `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss import ...`. |

## Key Findings

### ModelDB 189347 release file-by-file catalogue

One-line purpose for every file shipped in the ModelDB release, as bundled in `[t0008]`'s `sources/`
directory (reused by reference, NOT re-downloaded). Line counts from the bundled copies.

* `main.hoc` (396 lines) — top-level GUI driver. Defines every simulation global (`b2gampa`,
  `b2gnmda`, `s2ggaba`, `s2gach`, `gabaMOD`, `achMOD`, `n_bipNMDA`, `gama_bipNMDA`,
  `newves_bipNMDA`, `tau1NMDA_bipNMDA`, `e_SACinhib`, `tau_SACinhib`, `vshift_HHst`, `rSYNchance`,
  `lightstart`, `lightspeed`, `lightwidth`, `lightX/Y*`, `SACdelt`, `SACdur`, `flickertime`,
  `flickerVAR`, `stimnoiseVAR`, `tstop`, `dt`), constructs `init_active()`, `placeBIP()`,
  `update()`, `init_sim()`, and the interactive `simplerun($1,$2)` callback that implements the
  paper's three conditions (`$1=1` control, `$1=2` zero-Mg++/Voff_bipNMDA=1, `$1=3` tuned
  excitation) and two directions (`$2=0` PD → `gabaMOD=.33`, `$2=1` ND → `gabaMOD=.99`) plus
  `nmdaOn`/`SpikesOn` GUI toggles [`t0008`].
* `RGCmodel.hoc` (11 861 lines) — DSGC template. Declares `begintemplate DSGC ... endtemplate`
  with fixed morphology `create soma, dend[350]`; `topol()` hard-codes the full 350-section
  connectivity; `shape3d()` loads explicit `pt3dadd` coordinates for the bundled DSGC reconstruction
  (approx. 11 500 of the 11 861 lines are `pt3dadd` calls). Section lists: `all`, `somas`, `dends`,
  `ON`, `OFF`. The ON/OFF cut is `z3d(n3d()-1) >= -.16*y3d(n3d()-1) + 46` (line 11801-11807). Places
  `SACinhibsyn[numsyn]`, `BIPsyn[numsyn]`, `SACexcsyn[numsyn]` on ON dendrites at segment 0.5 with
  `.locx`/`.locy` at the section midpoint (lines 11816-11851). Dendritic diameter taper:
  `diam=.5 + 2.58*exp(-(distance(01)-10)/10)` (line 11814) [`t0008`].
* `dsgc_model.hoc` (330 lines) — **task-local t0008 derivative**, NOT in the ModelDB release.
  Copies every parameter-block line from `main.hoc` with all
  `xpanel`/`xbutton`/`load_file("model.ses")` removed so Python drivers can `h.load_file()` it
  headlessly. Parameter values are bit-identical to `main.hoc`; only the GUI interactive layer is
  removed [`t0008`].
* `HHst.mod` (415 lines) — stochastic Hodgkin-Huxley with channel noise (Linaro et al. framework).
  Three conductances gated by `SUFFIX HHst`: `gnabar`, `gkbar`, `gkmbar` (Km), plus passive `gleak`,
  and present-but-zeroed `glbar` (L-Ca) and `gtbar` (T-Ca). Single-channel conductances
  `gamma_na = gamma_k = gamma_km = gamma_l = gamma_t = 10 pS`. `GLOBAL vshift` allows simultaneous
  shift of all activation curves via `vshift_HHst` (main.hoc sets `-4`) [`t0008`].
* `bipolarNMDA.mod` (160 lines) — the paper's combined AMPA+NMDA synapse. `POINT_PROCESS bipNMDA`.
  Presynaptic: `maxves=10`, `newves=0.01`, `Vtau=30 (/ms)`, release probability `s_inf = Vpre/100`,
  per-ms vesicle-release Bernoulli loop with `scop_random()`. Postsynaptic: `gAMPAsingle=0.2 nS`,
  `gNMDAsingle=0.2 nS`, `tau1NMDA=50 ms` (decay), `tau2NMDA=2 ms` (rise), `tauAMPA=2 ms`,
  `n=0.25 /mM`, `gama=0.08 /mV`, `e=0 mV`, `icaconst=0.1`, Jahr-Stevens form
  `gNMDA=(A-B)/(1+n*exp(-gama*local_v))`, `local_v = v*(1-Voff) + Vset*Voff` (`Voff=1` gives the
  voltage-independent "zero-Mg2+" variant, `Vset=-60`) [`t0008`].
* `SAC2RGCinhib.mod` (94 lines) — GABA-A synapse, `POINT_PROCESS SACinhib`. Same presynaptic
  machinery (`maxves=10`, `newves=0.01`, `Vtau=30`). Postsynaptic: `gsingle=0.2 nS`, `tau=10 ms`,
  `e=-65 mV` (overridden to `-60 mV` in `main.hoc` via `e_SACinhib`) [`t0008`].
* `SAC2RGCexc.mod` (94 lines) — nicotinic ACh synapse, `POINT_PROCESS SACexc`. Presynaptic same as
  above. Postsynaptic: `gsingle=0.2 nS`, `tau=3 ms`, `e=0 mV` [`t0008`].
* `SquareInput.mod` (56 lines) — `POINT_PROCESS square`. Deterministic square conductance pulse
  (`del=50 ms`, `dur=50 ms`, `gmax=1 nA`) with optional Jahr-Stevens Mg block (`n=0.25`,
  `gama=0.08`, toggled by `Vdependent` flag). No noise, no vesicle machinery; used only by the
  interactive ses file, not by `placeBIP()` [`t0008`].
* `spike.mod` (195 lines) — legacy Fohlmeister/Velte 1990 channel complement (gnabar, gkbar,
  gabar, gcabar, gkcbar). **Compiled into the DLL but never inserted** by `main.hoc`; `RGCmodel.hoc`
  inserts `HHst` only. Keep compilation working but confirm it never runs [`t0008`].
* `mosinit.hoc` (2 lines) — `load_file("nrngui.hoc")` + `load_file("main.hoc")`; standard ModelDB
  bootstrap [`t0008`].
* `model.ses` (NEURON session) — pre-configured graph/point-process plots. Loaded by `main.hoc` at
  `load_file("model.ses")` on line 392 of the upstream. **Problem for headless driver**: its
  `xopen`/`load_file` chain breaks on Windows NEURON 8.2.7 if `chdir()` is not set to the sources
  directory first. `[t0008]` solves this by (a) stripping the `load_file("model.ses")` line in the
  task-local `dsgc_model.hoc` and (b) `h(f'chdir("{sources_forward}")')` before any `load_file`
  call, emitting forward slashes so HOC's string-literal escape parser does not break on Windows
  backslashes [`t0008`, `build_cell.py:143-145`]. This pattern is mandatory for t0046.
* `readme.html` / `readme.docx` / `readme.fld/` — original lab README. No parameter values of
  their own; narrative-level description of what the GUI toggles do.

### Synapse count: 282 (code) vs 177 (paper) — catalogue origin

`RGCmodel.hoc:11825-11851` computes synapse counts as follows. Every `ON` section (cut at
`z >= -0.16*y + 46`) contributes `numsynperdend=1` synapse triples (`SACinhibsyn`, `SACexcsyn`,
`BIPsyn`), gated by `numdendskip=1`. `countON` is the number of ON sections;
`numsyn = int(countON*numsynperdend/numdendskip) + 1 = countON + 1`. The `+1` accounts for the
0-indexed `countn` assignment loop. `[t0008]` confirmed **282 ON dendrites** at build time
(`N_SYNAPSES_EACH_TYPE: int = 282`, `constants.py:59`, with comment: "The earlier task description
figure of 177 referred to a different paper architecture; the port is faithful to the released HOC
template, not to that number"). The paper's text "177 synapses" does not appear anywhere in the
shipped HOC/MOD sources; the 282 count is the authoritative value of the released code. t0046 must
preserve this behaviour and catalogue the discrepancy (paper 177 vs code 282) as pre-flagged.

### Luminance-noise driver: present in main.hoc but dormant

**Finding contradicts research_internet.md's "noise driver missing" claim.** `main.hoc:99-101` and
the identical block in `dsgc_model.hoc:89-91` declare `flickertime=50`, `flickerVAR=0`,
`stimnoiseVAR=0`. `placeBIP()` (main.hoc:191-282) implements per-`flickertime`-ms Gaussian
perturbation of both `BIPVbase` and `BIPVamp`:

```
for timer=0,tstop/flickertime-1{
  basenoise.fill((BIPVbase+rnoise.normal(0,flickerVAR)),timer*flickertime/dt,(timer+1)*flickertime/dt)
  ampnoise.fill((BIPVamp+rnoise.normal(0,flickerVAR+stimnoiseVAR)),timer*flickertime/dt,(timer+1)*flickertime/dt)
}
```

This is exactly the "per-50-ms luminance noise at SD = X%" protocol the paper's Figures 6-8
describe. It is merely parameterised to zero variance in the shipped code. To reproduce Figures 6-8
at SD ∈ {0, 10, 30, 50}, t0046 must override `flickerVAR` (and optionally `stimnoiseVAR`) to {0.0,
0.1, 0.3, 0.5} and call `placeBIP()` to re-roll the noise vectors. **No new MOD file needed.**
`SquareInput.mod` is unused by the moving-bar protocol (that's the `Vinf.play()` stream fed to each
BIP/SACinhib/SACexc `POINT_PROCESS`); the shipped mechanism is complete for Figures 6-8. The audit
discrepancy becomes: paper describes the noise in words only; the code parameterises it correctly
but at zero SD. This is a weaker discrepancy than "missing noise driver" and should be re-framed in
the audit catalogue.

### gabaMOD swap is the paper-native DS protocol

`main.hoc:46` sets `gabaMOD=0.33` at module load and the interactive `simplerun($1,$2)` rebinds
`gabaMOD = .33 + .66*$2` (line 351) where `$2=0` gives PD (`gabaMOD=0.33`) and `$2=1` gives ND
(`gabaMOD=0.99`). `gabaMOD` enters `placeBIP()` at line 256 as a **multiplier on the inhibitory
stimulus amplitude** during the transient window: `mulnoise.fill(VampT*gabaMOD, ...)`. A PD trial
uses 33% of the SAC→DSGC inhibitory drive, an ND trial uses 99% — a 3× asymmetry in inhibition
is how the paper's model converts an angle-agnostic excitatory bar into a direction-selective
response. `[t0020]` demonstrated that this protocol produces **DSI 0.78** (inside Poleg-Polsky's
0.70-0.85 median envelope) on the bundled morphology, whereas `[t0008]`'s spatial-rotation proxy
produces DSI 0.316 on the same cell [`t0008`, `t0020`]. t0046 must use the gabaMOD-swap protocol for
every direction-selectivity test; rotation-proxy trials are out of scope.

### Parameter audit: research_internet.md vs actual main.hoc

Direct re-reading of `main.hoc` (line numbers cited) reveals **several values where
`research_internet.md`'s extracted table disagrees with the actual shipped file**. These must be
corrected in the t0046 audit table:

| Parameter | research_internet.md says | main.hoc actual | Source line |
| --- | --- | --- | --- |
| `n_bipNMDA` (NMDA Mg-block n) | 0.25 | **0.3** | main.hoc:82, dsgc_model.hoc:72 |
| `gama_bipNMDA` (NMDA Mg-block γ) | 0.08 | **0.07** | main.hoc:83, dsgc_model.hoc:73 |
| `newves_bipNMDA` (vesicle replenishment) | 0.01 | **0.002** | main.hoc:84, dsgc_model.hoc:74 |
| `tau1NMDA_bipNMDA` (NMDA decay) | 50 ms | **60 ms** | main.hoc:86 (code sets 60; MOD default is 50) |
| `tau_SACinhib` (GABA decay) | 10 ms | **30 ms** | main.hoc:90 (code overrides MOD default of 10) |
| `e_SACinhib` (GABA reversal) | -65 mV | **-60 mV** | main.hoc:89 (code overrides MOD default of -65) |
| `achMOD` (default) | 0.25 | **0.25 in main.hoc:47, but `simplerun()` rebinds to 0.33** | main.hoc:47 vs 352 |
| `gabaMOD` (default PD) | 0.33 | **0.33** | main.hoc:46 (confirmed) |

The MOD file defaults (`bipolarNMDA.mod:40-41` n=0.25 gama=0.08; `bipolarNMDA.mod:23` newves=0.01;
`bipolarNMDA.mod:37` tau1NMDA=50; `SAC2RGCinhib.mod:24-25` tau=10, e=-65) exist in PARAMETER blocks
but `main.hoc` **overrides all of them at top level** via direct global assignment. The canonical
audit values are the `main.hoc` assignments, not the MOD defaults. research_internet.md extracted
MOD defaults where it should have extracted main.hoc values; t0046's audit table must use the
main.hoc values throughout and catalogue this as a correction against t0046's own upstream research
stage [`t0008`].

### Morphology source: ModelDB ships its own; t0005 is a substitute

`RGCmodel.hoc:11860+` (topol + shape3d at lines 15-11780) ships its own DSGC morphology — 1 soma +
350 dend sections — encoded directly as `pt3dadd(x,y,z,d)` calls with hard-coded 3D points. There
is **no `.swc` file** in the ModelDB release; morphology is hoc-embedded. `[t0005]` downloaded a
different DSGC reconstruction (`141009_Pair1DSGC.CNG.swc` from NeuroMorpho.org, Feller lab) as the
project's baseline; `[t0009]` later calibrated its diameters. `[t0008]`'s `report_morphology.py`
confirms the two morphologies have similar section-count and surface-area parity but different
3D-coordinate layouts; `[t0008]` explicitly did **not** swap in the t0005 SWC because `placeBIP()`
depends on section ordering and the `z >= -0.16*y + 46` ON/OFF cut that only makes sense on the
bundled morphology [`t0008`]. t0046 must therefore use the bundled `RGCmodel.hoc` morphology, not
the t0005 SWC, and catalogue this: the paper used its own reconstruction, and t0005's candidate is a
different cell that cannot be dropped in without re-implementing `placeBIP()`.

### NEURON 8.2.7 Windows compile and loader pattern

`[t0007]` validated NEURON 8.2.7 + NetPyNE 1.1.1 installs cleanly at `C:\Users\md1avn\nrn-8.2.7`.
`[t0008]` added a `run_nrnivmodl.cmd` Windows shell script that invokes the MinGW-gcc toolchain to
produce `x86_64/nrnmech.dll`. The Python loader pattern, copied verbatim into `[t0020]`'s
`run_gabamod_sweep.py:29-81` and `[t0022]`'s `neuron_bootstrap.py`, is: (1) set `NEURONHOME` in the
C environment before any `import neuron` by `os.execv`-re-execing the process if missing; (2) insert
`<NEURONHOME>/lib/python` into `sys.path`; (3) `os.add_dll_directory(<NEURONHOME>/bin)` so `hoc.pyd`
can resolve `libnrniv.dll`. Forget any of these steps and NEURON fails with a cryptic import error
on Windows — this has been demonstrated three times across `[t0008]`, `[t0020]`, `[t0022]`. t0046
must replicate the same pattern; the code is approximately 55 lines.

### Cross-task import rule violations in prior ports

`[t0020]` imports
`tasks.t0008_port_modeldb_189347.code.build_cell.{build_dsgc, run_one_trial, read_synapse_coords, SynapseCoords, apply_params, get_cell_summary}`
and `tasks.t0008_port_modeldb_189347.code.constants.*` directly. **This is a violation** of the
cross-task import rule (task code may only import from registered libraries). t0046 must **not
follow this pattern** and must copy rather than import. The same applies to t0022's reuse of the
t0020 bootstrap via file-level copy with renamed sentinel env var (pattern shown in
`tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py:1-20`, which explicitly documents
the copy-verbatim + rename-sentinel approach). t0046 should follow t0022's copy pattern, not t0020's
import pattern.

### Scoring/visualisation integration path for a PSP-first reproduction

`[t0012]`'s `tuning_curve_loss` is built around **firing rates**, not PSP amplitudes. t0046's
primary metrics are PSP amplitudes (mV), direction-tuning slope angles (degrees), and ROC AUC —
none of which the t0012 scorer covers. The `compute_dsi` helper is trivially reusable for the Figure
8 secondary suprathreshold DSI check, but the PSP/slope/ROC audit requires new computation that
t0046 must implement from scratch. `[t0011]`'s `tuning_curve_viz` renders tuning curves from the
canonical CSV schema; the Cartesian/polar plotters assume firing rates on the y-axis but accept any
(angle, trial, value) schema, so they can be driven with PSP-amplitude values if the CSV label says
so. Target-envelope overlays from the t0004 canonical tuning curve are out of scope for this task.

## Reusable Code and Assets

### ModelDB 189347 HOC/MOD sources

* **Source**: `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/`
* **What it contains**: `main.hoc`, `RGCmodel.hoc`, `HHst.mod`, `bipolarNMDA.mod`,
  `SAC2RGCinhib.mod`, `SAC2RGCexc.mod`, `SquareInput.mod`, `spike.mod`, `mosinit.hoc`, `model.ses`,
  `readme.html`/`.docx`/`.fld/`.
* **Reuse method**: **copy into task** (the sources live inside `[t0008]`'s library asset folder but
  are the upstream ModelDB files; t0046's new library asset `modeldb_189347_dsgc_exact` needs its
  own copy under `tasks/t0046_.../assets/library/modeldb_189347_dsgc_exact/sources/` to remain
  self-contained).
* **Adaptation needed**: copy `main.hoc` verbatim; create a task-local `dsgc_model_exact.hoc`
  (ported equivalent of `[t0008]`'s `dsgc_model.hoc`) that strips GUI lines. MOD files compile
  unchanged on NEURON 8.2.7.
* **Line count**: ~13 600 total (11 861 for `RGCmodel.hoc` alone; rest ~1 750).

### HOC-safe source-dir chdir + forward-slash loader pattern

* **Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py:120-175` (`_sources_dir_hoc_safe`,
  `build_dsgc`).
* **What it does**: chdirs HOC into the sources directory using forward slashes so
  `load_file("RGCmodel.hoc")` and `load_file("dsgc_model.hoc")` resolve on Windows.
* **Reuse method**: **copy into task**.
* **Function signatures**:
  ```python
  def _sources_dir_hoc_safe() -> str
  def build_dsgc() -> Any  # returns h with RGC initialised
  def load_neuron() -> Any  # loads nrnmech.dll and stdrun.hoc
  ```
* **Adaptation needed**: rename `MODELDB_*` path constants to t0046 paths; replace
  `MODELDB_GUI_FREE_HOC` with `MODELDB_EXACT_HOC` pointing at t0046's own `dsgc_model_exact.hoc`.
* **Line count**: ~60 lines.

### NEURONHOME bootstrap with process re-exec

* **Source**: `tasks/t0022_modify_dsgc_channel_testbed/code/neuron_bootstrap.py` (cleanest of the
  three versions; itself a copy-with-renamed-sentinel of t0020's).
* **What it does**: sets NEURONHOME, re-execs process if missing, adds DLL dir on Windows, places
  NEURON Python bindings on `sys.path`.
* **Reuse method**: **copy into task** with renamed sentinel `_T0046_NEURONHOME_BOOTSTRAPPED`.
* **Function signature**: `def ensure_neuron_importable() -> None`.
* **Adaptation needed**: rename sentinel env var; change the `from tasks.t0022_...constants import`
  line to import from t0046 constants.
* **Line count**: ~55 lines.

### Synapse-coordinate snapshot dataclass

* **Source**: `tasks/t0008_port_modeldb_189347/code/build_cell.py:63-74, 192-208`.
* **What it does**: snapshots `BIPsyn/SACinhibsyn/SACexcsyn` `.locx`/`.locy` for all 282 synapses so
  they can be asserted-unchanged before/after trials.
* **Reuse method**: **copy into task**.
* **Function signatures**:
  ```python
  @dataclass(frozen=True, slots=True)
  class SynapseCoords: ...  # index, bip_locx/y, sac_inhib_locx/y, sac_exc_locx/y
  def read_synapse_coords(h: Any) -> list[SynapseCoords]: ...
  def get_cell_summary(h: Any) -> CellSummary: ...
  ```
* **Adaptation needed**: none — paste into t0046's `build_cell.py`.
* **Line count**: ~40 lines.

### BIP-position baseline assertion (anti-rotation guard)

* **Source**: `tasks/t0020_port_modeldb_189347_gabamod/code/run_gabamod_sweep.py:109-127`
  (`_assert_bip_positions_baseline`).
* **What it does**: asserts `RGC.BIPsyn[i].locx == baseline` after every `placeBIP()` to prevent
  silent reactivation of the rotation proxy. Indispensable for a pure-gabaMOD reproduction.
* **Reuse method**: **copy into task**.
* **Function signature**:
  ```python
  def _assert_bip_positions_baseline(
      *, h: Any, baseline_coords: list[SynapseCoords]
  ) -> None
  ```
* **Adaptation needed**: none.
* **Line count**: ~20 lines.

### Tuning-curve visualisation (import via library)

* **Source**: library `tuning_curve_viz` at
  `tasks/t0011_response_visualization_library/assets/ library/tuning_curve_viz/` (code lives at
  `tasks/t0011_response_visualization_library/code/tuning_curve_viz/`).
* **What it does**: Cartesian + polar tuning-curve plots, multi-model overlays, per-angle raster +
  PSTH.
* **Reuse method**: **import via library**. Import path:
  `from tasks.t0011_response_visualization_library.code.tuning_curve_viz.cartesian import plot_cartesian_tuning_curve`
  (and `polar`, `overlay`, `raster_psth`).
* **Function signatures**: `plot_cartesian_tuning_curve(df, out_path, *, target_df=None)`,
  `plot_polar_tuning_curve(...)`, `plot_multi_model_overlay(...)`, `plot_angle_raster_psth(...)`.
* **Adaptation needed**: feed PSP-amplitude CSVs with the same `(angle_deg, trial_seed, value)`
  schema; override y-axis label to "PSP amplitude (mV)". No code changes to the library.
* **Line count**: n/a — library import.

### DSI/peak/null helpers (import via library)

* **Source**: library `tuning_curve_loss` at
  `tasks/t0012_tuning_curve_scoring_loss_library/ assets/library/tuning_curve_loss/`.
* **What it does**: `compute_dsi`, `compute_peak_hz`, `compute_null_hz`, `compute_hwhm_deg`.
* **Reuse method**: **import via library**. Import:
  `from tasks.t0012_tuning_curve_scoring_loss_library.code.tuning_curve_loss.metrics import ( compute_dsi, compute_peak_hz, compute_null_hz, compute_hwhm_deg)`.
* **Adaptation needed**: Fig 8 secondary pass only. Do NOT use the `score()` aggregator; its
  weighted-loss formulation over peak/null/HWHM/DSI does not match the paper's metrics.
* **Line count**: n/a — library import.

### ModelDB 189347 morphology (verbatim reuse; no swap)

* **Source**: embedded inside
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/ sources/RGCmodel.hoc` (350
  `create dend[i]` + `pt3dadd()` calls for the DSGC).
* **Reuse method**: **copy into task** (as part of the sources bundle).
* **Adaptation needed**: none.
* **Do not swap** the `[t0005]`/`[t0009]` SWC morphology in; `placeBIP()` cannot consume an SWC and
  the paper used its own reconstruction. Flag as discrepancy only if t0005's is found to be the
  paper's actual morphology (it is not — the paper's Methods cite their own recording).

## Lessons Learned

* **Rotation proxy understates DSI by >2x** compared to the paper-native gabaMOD swap (DSI 0.316 vs
  0.784 on the same cell) — this is the central empirical finding of `[t0008]` and `[t0020]`. Any
  DS reproduction that is not using `gabaMOD=0.33`/`gabaMOD=0.99` swap is misaligned with the
  paper's mechanism [`t0008`, `t0020`].
* **Firing rates stay depressed regardless of protocol**: `[t0008]` peak 18.1 Hz, `[t0020]` peak
  14.85 Hz. Both fail the 40-80 Hz envelope. The t0046 task explicitly reframes the comparison
  target to PSP amplitudes because that is what the paper actually reports; this is the correct
  call. The 40-80 Hz band comes from Oesch 2005 rabbit recordings [`t0020`].
* **Windows NEURON 8.2.7 needs three discrete steps** to make `import neuron` work: set `NEURONHOME`
  before Python starts (requires re-exec), extend `sys.path`, and register the DLL directory. Each
  of the three downstream ports re-solves this identically; t0046 should copy one of them verbatim
  [`t0007`, `t0008`, `t0020`, `t0022`].
* **`h.load_file()` + Windows paths require forward slashes and pre-emptive `chdir()`** inside HOC.
  The backslash-as-escape-char interaction between HOC string literals and `os.PathLike` breaks
  silently if not handled; `[t0008]`'s `_sources_dir_hoc_safe()` wrapper is the canonical fix.
* **MOD defaults can disagree with main.hoc globals** and are often wrong if read in isolation.
  `bipolarNMDA.mod` declares `n=0.25 gama=0.08 newves=0.01 tau1NMDA=50` in its PARAMETER block but
  `main.hoc` overrides all of these at top level. The research_internet.md audit extracted MOD
  defaults instead of main.hoc globals for several rows and must be corrected [this task].
* **Per-trial `placeBIP()` is mandatory** whenever any of `gabaMOD`, `achMOD`, `b2gnmda`, light
  geometry, or noise SD changes, because those globals are read at `placeBIP()` invocation to build
  the `Vinf.play()` vectors. `[t0020]` forgot this once during development and DSI collapsed to ~0.1
  until the call was restored [`t0020`].
* **Test framework is local-only**; tasks `[t0008]` and `[t0020]` use `pytest`-style
  `code/test_smoke_single_angle.py` files but no CI run. t0046 should follow the same pattern and
  include a smoke test that builds the cell and confirms `numsyn=282`.

## Recommendations for This Task

1. **Create the new library asset's `sources/` by copying every file** from
   `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/` into
   `tasks/t0046_.../assets/library/modeldb_189347_dsgc_exact/sources/`. Keep `main.hoc` verbatim
   (with the original 2019-05-31 commit SHA `87d669dcef18e9966e29c88520ede78bc16d36ff` documented in
   `details.json`). Create `dsgc_model_exact.hoc` = `main.hoc` with GUI lines stripped, patterned on
   `[t0008]`'s existing `dsgc_model.hoc` but written from scratch (no code copy).
2. **Copy the three helper patterns** (NEURONHOME bootstrap, HOC-safe chdir + load, synapse-coord
   snapshot with baseline assertion) into `tasks/t0046_.../code/` with renamed constants and
   sentinel. Do **not** import from `tasks.t0008_...` or `tasks.t0020_...`; the cross-task import
   rule forbids it.
3. **Use gabaMOD swap (`0.33`/`0.99`) as the DS mechanism**, not rotation. Rotation is already known
   to understate DSI by 2.5× [`t0008`, `t0020`].
4. **Drive subthreshold PSP recording by setting `exptype=2` + `SpikesOn=0`** in the HOC loader
   before `h.run()`. `main.hoc:132-133` handles this: `if (exptype==2){TTX=1}` zeroes the somatic
   gNa, and `init_active()` propagates. For Fig 1-5 metrics, record soma `V_m` and integrate the
   peak depolarisation relative to `v_init=-65 mV`.
5. **For Figure 6-8 noisy-luminance reproductions, override `h.flickerVAR` and `h.stimnoiseVAR`** to
   the paper's `{0, 0.1, 0.3, 0.5}` SDs and call `h('placeBIP()')` to re-roll the noise vectors. The
   noise driver is already present in `main.hoc`'s `placeBIP()` procedure; it is parameterised to
   zero in the shipped code. Re-frame the "missing noise driver" discrepancy as **"noise driver
   present but zeroed"** in the audit.
6. **For the zero-Mg2+ variant (Figure 5), set `h.Voff_bipNMDA=1`** rather than editing
   `bipolarNMDA.mod`. Line 101 of that MOD file implements `local_v = v*(1-Voff) + Vset*Voff` which
   collapses the Jahr-Stevens block to Ohmic when `Voff=1` and `Vset=-60`.
7. **For the High-Cl- / tuned-excitation variant (Figure 4), set `gabaMOD=1` and
   `achMOD += 0.66*(1-$2)`** per `simplerun($1=3, $2)` in `main.hoc:354-357`.
8. **Populate the audit table's ModelDB-code column from `main.hoc` (not MOD defaults)** — use
   this research_code.md's parameter-correction table as the source of truth.
9. **Preserve the 282 synapse count exactly** and record the paper's 177 claim as a catalogued
   paper-vs-code discrepancy with no reproduction action.
10. **Import `[t0011]` and `[t0012]` libraries** via absolute
    `tasks.t0011_....code.tuning_curve_viz` and `tasks.t0012_....code.tuning_curve_loss` paths for
    plotting and the Figure 8 DSI helper. Do not depend on their CLI entry points; call the
    functions directly.
11. **Use the t0005/t0009 SWC morphology only for reporting**, not for simulation. `[t0008]`'s
    `report_morphology.py` demonstrates the comparison report layout; copy it if section-count/
    surface-area reporting is needed for the audit.
12. **Plan for ~1.5 min/20 trials local runtime** on the Windows workstation (observed in
    `[t0020]`); budget an afternoon for the Fig 1-7 subthreshold sweep of approx. 8 angles × 3
    conditions × 20 trials = 480 trials. Fig 6-8 noise conditions add another 4 SD levels × 20
    trials.

## Task Index

### [t0005]

* **Task ID**: `t0005_download_dsgc_morphology`
* **Name**: Download candidate DSGC morphology
* **Status**: completed
* **Relevance**: Downloaded `141009_Pair1DSGC.CNG.swc`. t0046 uses the bundled ModelDB morphology,
  not this SWC, but references this dataset for an explicit morphology-provenance discrepancy note.

### [t0007]

* **Task ID**: `t0007_install_neuron_netpyne`
* **Name**: Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain
* **Status**: completed
* **Relevance**: Validates the NEURON 8.2.7 + NetPyNE 1.1.1 toolchain t0046 depends on; supplies
  `NEURONHOME=C:\Users\md1avn\nrn-8.2.7` and the MinGW compile recipe.

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: First port; bundles the verbatim ModelDB HOC/MOD sources under its library asset's
  `sources/` directory and provides the canonical Windows-NEURON loader pattern. t0046 copies those
  sources into its own library asset and re-implements the driver.

### [t0009]

* **Task ID**: `t0009_calibrate_dendritic_diameters`
* **Name**: Calibrate dendritic diameters for dsgc-baseline-morphology
* **Status**: completed
* **Relevance**: Calibrated the t0005 SWC; referenced only for the morphology-provenance discussion
  — t0046 uses the ModelDB bundled morphology, not the calibrated SWC.

### [t0011]

* **Task ID**: `t0011_response_visualization_library`
* **Name**: Response-visualisation library (firing rate vs angle graphs)
* **Status**: completed
* **Relevance**: Registered library `tuning_curve_viz`; import its Cartesian + polar plotters for
  the per-figure reproduction PNGs under `results/images/`.

### [t0012]

* **Task ID**: `t0012_tuning_curve_scoring_loss_library`
* **Name**: Tuning-curve scoring loss library
* **Status**: completed
* **Relevance**: Registered library `tuning_curve_loss`; import `compute_dsi`/`compute_peak_hz`/
  `compute_null_hz` for the Fig 8 secondary suprathreshold DSI check. Do not use the full scorer.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Proves the gabaMOD swap reproduces the paper's DS envelope (DSI 0.78). t0046 must
  re-implement the swap pattern in its own code (no cross-task import) but uses the `[t0020]` result
  as the target contrast for Fig 8 qualitative checks.

### [t0022]

* **Task ID**: `t0022_modify_dsgc_channel_testbed`
* **Name**: Modify DSGC port with spatially-asymmetric inhibition for channel testbed
* **Status**: completed
* **Relevance**: Source of the cleanest copy-into-task pattern for the NEURON bootstrap
  (`neuron_bootstrap.py`, with a renamed sentinel env var). t0046 copies its approach, not t0020's
  cross-task-import approach.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Sibling DSGC port (different paper); confirms the copy-source-files-per-task
  pattern is standard across multiple reproduction tasks in this project, reinforcing the
  recommendation that t0046 bundle its own `sources/` copy rather than symlinking t0008's.
