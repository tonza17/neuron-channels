---
spec_version: "1"
task_id: "t0070_writeup_two_model_beds"
research_stage: "code"
tasks_reviewed: 5
tasks_cited: 5
libraries_found: 2
libraries_relevant: 2
date_completed: "2026-05-01"
status: "complete"
---
# Research Code: Two Standard DSGC Model Beds

## Task Objective

Produce a research-paper-format writeup that documents the project's two canonical DSGC model beds:
**Bed A** — the deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC ported in [t0008] (ModelDB 189347) with
the gabaMOD-swap protocol added in [t0020]; and **Bed B** — the de Rosenroll 2026 DSGC ported in
[t0024]. The writeup must start each bed with the canonical Hodgkin-Huxley membrane equation,
enumerate every conductance with `gbar` / `V_half` / `τ` / `e_rev` (and source citation), and
document the synaptic excitation + inhibition models for PD vs ND. The downstream EPSP/IPSP/Vm
protocols added in [t0065] (bed A) and [t0066] (bed B) define how PD vs ND is encoded at the
protocol level for each bed and how the FULL / EPSP_PASSIVE / IPSP_PASSIVE trio is produced.

This is a documentation-only task — no simulations are run. The implementation step needs file:line
citations for every parameter so the writeup is auditable against the committed code.

## Library Landscape

The aggregate-libraries script is not available in this branch's `arf/scripts/aggregators/`
directory (only the metadata aggregators are wired here), so libraries were enumerated by inspecting
`tasks/*/assets/library/`. Two NEURON library assets are immediately relevant — both are direct
dependencies of the writeup.

* **`modeldb_189347_dsgc`** v0.1.0, created by [t0008]. Path:
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`. Categories:
  `direction-selectivity`, `compartmental-modeling`, `retinal-ganglion-cell`. Wraps Poleg-Polsky &
  Diamond 2016's ModelDB 189347 sources (HOC + MOD) at upstream commit
  `87d669dcef18e9966e29c88520ede78bc16d36ff`. Module entry points include `build_dsgc()`,
  `apply_params()`, and the GUI-stripped `dsgc_model.hoc`. Sources include `RGCmodel.hoc` (the cell
  template, 11 861 lines), `main.hoc` (paper driver, preserved verbatim, 397 lines),
  `dsgc_model.hoc` (GUI-free derivative used by Python drivers), and four `.mod` files: `HHst.mod`
  (stochastic HH + Km + L/T-Ca, 416 lines), `bipolarNMDA.mod` (vesicular AMPA + NMDA point process,
  161 lines), `SAC2RGCinhib.mod` (SAC GABA point process, 95 lines), `SAC2RGCexc.mod` (SAC ACh point
  process, 95 lines). No corrections registered; aggregator output reflects raw files. **Highly
  relevant** — this is the source of every Bed A parameter.

* **`de_rosenroll_2026_dsgc`** v0.1.0, created by [t0024]. Path:
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`. Categories:
  `compartmental-modeling`, `direction-selectivity`, `retinal-ganglion-cell`,
  `dendritic-computation`. Vendors a subset of the upstream
  `geoffder/ds-circuit-ei-microarchitecture` repo at commit
  `a23f642aa6557a23a51bf76f51e420e8149773fa`: `RGCmodelGD.hoc` (350-section DSGC template, 11 830
  lines), `HHst_noiseless.mod` (deterministic HH + Km + L/T-Ca, 397 lines), `Exp2NMDA.mod` (dual-
  exp NMDA with Mg block, 103 lines), `cadecay.mod` (calcium decay, 76 lines). **Highly relevant** —
  this is the source of every Bed B membrane-channel parameter. Note that the upstream Python E/I
  model (`ei_balance.py`, `SacNetwork.py`) is **not** vendored; the t0024 port reimplements the
  synaptic / release-noise model in Python.

No other library assets exist in `tasks/*/assets/library/`. No tuning-curve scoring or response-
visualization library is needed for this documentation task.

## Key Findings

### Both beds share the Hodgkin-Huxley `HHst` mechanism but use different variants

Both Bed A and Bed B use the same source-level mechanism family `SUFFIX HHst`, but the variants
differ in noise treatment.

* Bed A uses the **stochastic** `HHst.mod`
  (`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/HHst.mod`). It
  defines five gated currents — fast Na (`m³h`), delayed-rectifier K (`n⁴`), M-type K (`nm`), L-type
  Ca (`lm²lh`), T-type Ca (`tm²th`) — plus a non-specific leak with a stochastic noise term
  (`zleak`, line 220). Channel-noise is implemented as Linaro–Storace–Giugliano OU-style state
  variables `zn[3]`, `zm[6]`, `zkm`, `zt[5]`, `zl[5]` driven by `normrand(0, NF)` (lines 77–85,
  286–290, 309–313, 322–323, 348–352, 374–378). The number of channels per compartment scales with
  area: `Nna = ceil(area_cm2 * gnabar / gamma_na_S)` (line 142). Project-wide drivers set `NF=0` to
  disable noise — see [t0008] `apply_params` and `dsgc_model.hoc` line 85 `NF_HHst=0`.

* Bed B uses the **noiseless** `HHst_noiseless.mod`
  (`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod`).
  Same `SUFFIX HHst`, same five conductances, same gating equations, but the `z` arrays are zeroed
  via `zn[i] = zn[i]*mu_zn[i]` with no innovation term (lines 282–284, 304–305, 314–315, 340–342,
  365–367), and the leak has no `zleak` term (line 216). Effectively a deterministic HH variant. The
  two `.mod` files share the same `BREAKPOINT` structure — the only differences are the noise terms
  and the absence of the `seed`, `set_seed`, `mulnoise`, and `NFleak` parameters.

The kinetics are identical between the two variants. Specifically (reading `HHst.mod` lines 243–360
and confirming against `HHst_noiseless.mod` lines 237–351):

* **Na m**: `α=-0.6·vtrap(V+30,-10)`, `β=20·exp(-(V+55)/18)`, `m_inf = α/(α+β)`, `τ_m = 1/(α+β)`.
  (HHst.mod L249-251 / HHst_noiseless.mod L244-246)
* **Na h**: `h_inf = 1/(1+exp((V+44)/4))`,
  `τ_h = hslow / ((1+exp((V+30)/4)) + exp(-(V+50)/2)) + hfast`, with `hslow=100`, `hfast=0.3`
  (HHst.mod L72-73, L265-266 / HHst_noiseless.mod L70-71, L260-261). V_half_inact = -44 mV.
* **K (delayed rectifier) n**: `α=-0.02·vtrap(V+40,-10)`, `β=0.4·exp(-(V+50)/80)`. Quartic gating
  `n⁴`. (HHst.mod L294-297)
* **Km (M-type K) nm**: `α=-0.001/taukm · vtrap(V+30,-9)`, `β=0.001/taukm · vtrap(V+30, 9)`. Linear
  gating in `nm`. `taukm=1` is the speed-up factor (HHst.mod L70).
* **L-Ca m**: `α=0.055·vtrap(-(V+27),3.8)`, `β=0.94·exp((-75-V)/17)`. (HHst.mod L326-327)
* **L-Ca h**: `α=0.000457·exp((-13-V)/50)`, `β=0.0065/(exp((-V-15)/28)+1)`. (HHst.mod L331-332)
* **T-Ca m**: `tm_inf = 1/(1+exp(-(V+50)/7.4))`, `τ_tm = 4/(exp((V+25)/20)+exp(-(V+100)/15))`.
  V_half_act = -50 mV. (HHst.mod L355-356)
* **T-Ca h**: `th_inf = 1/(1+exp((V+78)/5))`, `τ_th = 86/(exp((V+46)/4)+exp(-(V+405)/50))`.
  V_half_inact = -78 mV. (HHst.mod L359-360)

The default `PARAMETER` block of `HHst.mod` (lines 54-74) sets `gnabar=0.12 S/cm²`,
`gkbar=0.036 S/cm²`, `glbar=0.0003 S/cm²` (L-Ca), `gtbar=0.0003 S/cm²` (T-Ca), `gkmbar=0.002 S/cm²`,
`gleak=1e-5 S/cm²`, `eleak=-60 mV`, `vshift=0`. **These default values are overridden in both beds
at runtime** — see the next two findings.

### Bed A (Poleg-Polsky 2016) keeps L-Ca and T-Ca at zero, runs in passive mode by default

In Bed A the active conductances are scoped by the HOC `update()` proc and only inserted on the
`somas` SectionList; the dendrites get either `pas` (`use_active=0`, the project default) or `HHst`
with reduced densities (`use_active=1`).
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc` L36
`use_active=0`; L324-333 `init_sim` inserts `HHst` only on soma, `pas` everywhere else by default;
L284-318 `update()` writes the per-section densities.)

The active densities live in `init_active()` (`main.hoc` L125-163, mirrored in `dsgc_model.hoc`
L114-152). Reading the assignments under `active=1`, `TTX=0`:

| Section group | gnabar (S/cm²) | gkbar (S/cm²) | gkmbar (S/cm²) | gleak (S/cm²) | eleak (mV) |
| --- | --- | --- | --- | --- | --- |
| `somas` (1 soma) | 0.4 (`RGCsomana`, L148) | 0.07 (`RGCsomakv`, L149) | 0.0005 (`RGCsomakm`, L150) | 5.5e-4 (`RGCgpas/2`, L161,304) | -60 (`RGCepas`, L162) |
| `dends` (350 dends, only when `use_active`) | 0.0002 (`RGCdendna`, L152) | 0.007 (`RGCdendkv`, L153) | 0 (`RGCdendkm`, L154) | 5.5e-4 / 2 (L290) | -60 |
| `all` (passive default) | n/a (`pas` only) | n/a | n/a | 5e-5 (`RGCgpas`, L161 `5e-5*(1+active*0)`) → 5.5e-4 active | -60 (`e_pas`, L301) |

`RGCcaT`, `RGCcaL`, `RGCcaP`, `RGCih`, `RGCkca` are all set to 0 (`init_active()` L155-159), so the
`glbar_HHst` and `gtbar_HHst` defaults in `HHst.mod` (which would otherwise insert L- and T-type Ca
current) are overwritten to 0 on every section that has HHst inserted. Bed A therefore effectively
has only Na, Kdr, Km currents when `use_active=1`. `vshift_HHst=-4 mV` is set globally (`main.hoc`
L91, `apply_params` L312 in `tasks/t0008_port_modeldb_189347/code/build_cell.py`).

The downstream protocol [t0065] toggles between active and passive via `h.exptype`: `exptype=1` ⇒ HH
on (the FULL trial mode), `exptype=2` ⇒ TTX (HH off, used for EPSP_PASSIVE and IPSP_PASSIVE; setting
`RGCsomana=RGCsomakv=RGCsomakm=0` via `init_active` L121-122,148-150). See
`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` L184-194 and
`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/constants.py` L23-27.

`Ra=100 Ω·cm` is set globally in `init_sim` (`dsgc_model.hoc` L317). `cm` is left at the NEURON
default (1 µF/cm²). `celsius=32 °C` (`apply_params` L284 in
`tasks/t0008_port_modeldb_189347/code/build_cell.py`, originally `main.hoc`'s implicit default
overridden by Python). `dt=0.1 ms`, `tstop=1000 ms`, `v_init=-65 mV` (`apply_params` L282-285).
Active-passive bifurcation in `RGCgpas=5e-5*(1+active*10)` (L161): passive sees 5e-5 S/cm², active
sees 5.5e-4 S/cm² leak.

### Bed B (de Rosenroll 2026) tier-stratifies HHst on every section

In Bed B every section gets `HHst + cad` inserted by Python in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py` `_configure_soma` (L192-201) and
`_configure_dends` (L204-248). Three dendrite tiers are distinguished by the `_map_tree` helper
(L140-168): `primary_dends = order_list[0]` (first-order branches off soma), `non_terminal_dends`
(intermediate), `terminal_dends` (leaves, where synapses land). Densities (S/cm², values from
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py` L34-42 with the *1e-3 mS→S conversion
applied at the boundary):

| Section tier | gnabar (S/cm²) | gkbar (S/cm²) | gkmbar (S/cm²) | gleak (S/cm²) | eleak (mV) | Ra | cm |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Soma | 0.150 | 0.035 | 0.003 | 1.667e-4 | -60 | 100 Ω·cm | 1 µF/cm² |
| Primary dendrites (order 0) | 0.200 | 0.035 | 0.003 | 1.667e-4 | -60 | 100 | 1 |
| Non-terminal mid dendrites | 0 (zeroed) | 0.025 | 0.003 | 1.667e-4 | -60 | 100 | 1 |
| Terminal dendrites | 0.030 | 0.025 | 0.003 | 1.667e-4 | -60 | 100 | 1 |

Note Bed B's primary-dendrite gNa is **higher** than the soma (0.200 vs 0.150 S/cm²). The
mid-dendrites have gNa zeroed but keep gKbar — this matches the upstream `ei_balance.py` choice. Cm
and Ra are set explicitly per section. Like Bed A, `glbar_HHst` (L-Ca) and `gtbar_HHst` (T-Ca) are
left at the `HHst_noiseless.mod` PARAMETER defaults (3e-4 each) on every section because the Python
builder does not write them. **This is a meaningful divergence between Bed A (Ca currents zeroed by
`init_active`) and Bed B (Ca currents at default).** The implementation of t0070's writeup must
explicitly note this.

`celsius=36.9 °C` (`constants.py` L19), `dt=0.1 ms`, `steps_per_ms=10`, `tstop=1000 ms`,
`v_init=-60 mV` (L20-24). The HH-on/HH-off toggle for [t0066] EPSP_PASSIVE / IPSP_PASSIVE modes is
implemented by zeroing every segment's `seg.HHst.gnabar = seg.HHst.gkbar = seg.HHst.gkmbar = 0.0`
for any non-FULL mode (`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py` L186-194);
FULL keeps them at the canonical state captured by `_snapshot_canonical_state` (L129-154).

The cadecay mechanism (`cadecay.mod`, only used in Bed B) maintains intracellular Ca²⁺ via a shell
of `depth=0.1 µm` and time constant `taur=5 ms`, with `cainf=2e-4 mM` (lines 44-49). It is present
on every section that has HHst inserted, so the Ca current `ica` (sum of `il` and `it` from
`HHst_noiseless.mod` L218-219) drives `cai` into the shell.

### Bed A excitation: vesicular AMPA + voltage-dependent NMDA in one bipNMDA point process

Bed A's bipolar excitation is implemented as a single `bipNMDA` POINT_PROCESS (`SUFFIX bipNMDA`)
defined in
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/bipolarNMDA.mod`. Each
ON dendrite carries one `BIPsyn` instance (placed at the section midpoint by `RGCmodel.hoc`
L11841-11843). Per-vesicle peak conductances:

* `gAMPAsingle = 0.2 nS` (default, `bipolarNMDA.mod` L35), overridden at runtime by
  `gAMPAsingle_bipNMDA = b2gampa = 0.25 nS` (`main.hoc` L42, `update()` L288, `apply_params` in
  `code/build_cell.py` L294 `h.b2gampa = B2GAMPA_NS=0.25`).
* `gNMDAsingle = 0.2 nS` (default, L36), overridden to `b2gnmda = 0.5 nS` (`main.hoc` L43,
  `update()` L289, `apply_params` L295).
* `tauAMPA = 2 ms` (decay, L39); AMPA has no rise — the conductance jumps on vesicle release.
* `tau1NMDA = 50 ms` (decay, L37); overridden at runtime to `tau1NMDA_bipNMDA = 60 ms` (`main.hoc`
  L86, `apply_params` L313 `h.tau1NMDA_bipNMDA = TAU1_NMDA_BIP_MS=60.0`).
* `tau2NMDA = 2 ms` (rise, L38); not overridden.
* `e = 0 mV` (reversal for AMPA and NMDA, L42).

NMDA voltage-dependence (Jahr-Stevens-style Mg block, `bipolarNMDA.mod` L102):

```
gNMDA = (A - B) / (1 + n * exp(-gama * local_v))
```

where `n = 0.25 /mM` (default L40), overridden to `n_bipNMDA = 0.3` (`main.hoc` L82, `apply_params`
L315 `h.n_bipNMDA = N_NMDA_V_DEP=0.3`); and `gama = 0.08 /mV` (default L41), overridden to
`gama_bipNMDA = 0.07` (`main.hoc` L83, `apply_params` L316
`h.gama_bipNMDA = GAMMA_NMDA_V_DEP=0.07`). `local_v = v*(1-Voff) + Vset*Voff` (L101) — when `Voff=0`
(default) the Mg block uses the postsynaptic voltage; when `Voff=1` the block is clamped at
`Vset=-43 mV` (the "voltage-independent NMDA" toggle used by `simplerun(2,*)`).

Vesicular release model (`bipolarNMDA.mod` L131-152): every 1 ms (`if (t>t1)` L81), the presynaptic
voltage `Vpre` (driven by the bar arrival via `noisevecBIP[i].play(&BIPsyn[i].Vinf, dt)` in
`placeBIP` L239) sets `s_inf = Vpre/100`; the proc loops over `numves` available vesicles and
releases each with probability `s_inf` (L135-139). Each release adds `release*gAMPAsingle` to
`gAMPA` and `release*gNMDAsingle` to both `A` and `B`. `Vpre` is a filtered version of `Vinf` with
time constant `Vtau=30 /ms` (L32, DERIVATIVE state L157). `maxves=10` (L22), `newves=0.01` baseline
replenishment (L23) overridden to `newves_bipNMDA=0.002` (`main.hoc` L84).

### Bed A inhibition: SAC GABA point process with gabaMOD direction-encoding scalar

Bed A's SAC-mediated inhibition lives in `SAC2RGCinhib.mod` (`SUFFIX SACinhib`,
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCinhib.mod`). One
`SACinhibsyn` instance per ON dendrite, placed at the section midpoint (`RGCmodel.hoc`
L11835-11838). Per-vesicle peak conductance:

* `gsingle = 0.2 nS` (default, L23), overridden at runtime to `gsingle_SACinhib = s2ggaba = 0.5 nS`
  (`main.hoc` L44, `update()` L290, `apply_params` L296 `h.s2ggaba = S2GGABA_NS=0.5`).
* `tau = 10 ms` (single-exponential decay, L24), overridden to `tau_SACinhib = 30 ms` (`main.hoc`
  L90 — but this overrides the *global* `tau`; not directly written in `apply_params`, so the
  runtime value is whatever HOC's `update()` wrote, which is the default 10 ms unless
  `tau_SACinhib=30` is read directly. **Open question for the writeup**: is the effective decay 10
  ms or 30 ms? Trace shows `update()` does *not* write `tau_SACinhib` to the per-instance `tau`, so
  the per-instance value sits at `gsingle*` defaults. The HOC global `tau_SACinhib` is set only
  because the global is named `tau`. Since `tau` is GLOBAL in the mod (L7), assigning to
  `tau_SACinhib` in HOC does set the mechanism's `tau` parameter for all instances. **Effective
  decay = 30 ms.**)
* `e = -65 mV` (default reversal, L26), overridden to `e_SACinhib = -60 mV` (`main.hoc` L89,
  `apply_params` L314 `h.e_SACinhib = E_SAC_INHIB_MV=-60.0`).

Vesicular release model (`SAC2RGCinhib.mod` L71-90): identical structure to `bipNMDA.mod` but
single-conductance — `g` accumulates `release*gsingle` on each release event, decays as `g'=-g/tau`.
`Vpre` is driven by the modulation envelope `noisevecSACI[i]` from `placeBIP` (L259,
`RGC.SACinhibsyn[i].Vinf`).

The PD/ND direction-encoding scalar **`gabaMOD`** modulates the GABA *modulation envelope*, not the
per-vesicle peak. In `placeBIP` (L256, `dsgc_model.hoc` L242):

```
mulnoise.fill(VampT*gabaMOD, ...)
```

where `mulnoise` then multiplies the active portion of the SAC inhibitory drive trace via
`noisevecSACI[i].mul(mulnoise)` (L257). So `gabaMOD` linearly scales the peak presynaptic voltage
(and thus `s_inf = Vpre/100` and the Bernoulli release probability). Canonical values
(`tasks/t0020_port_modeldb_189347_gabamod/code/constants.py` L37-38, [t0020]):

* **PD (preferred direction)**: `gabaMOD = 0.33` — weak inhibition.
* **ND (null direction)**: `gabaMOD = 0.99` — strong (~3x) inhibition.

This is the `simplerun(1,$2)` HOC convention in `main.hoc` L351 (`gabaMOD = 0.33 + 0.66*$2`, `$2=0`
⇒ PD ⇒ 0.33, `$2=1` ⇒ ND ⇒ 0.99). [t0020]'s `run_one_trial_gabamod` (`code/run_gabamod_sweep.py`
L130-182) implements the swap by setting `h.gabaMOD = gabamod_value` then calling `h("update()")`
and `h("placeBIP()")` so the inhibitory point processes pick up the new modulation envelope
(L154-155). The protocol sets BIP synapse coords *fixed at baseline* — direction selectivity comes
purely from the inhibitory scalar swap. An assertion `_assert_bip_positions_baseline` (L109-127)
guards against rotation re-engaging.

There is also a parallel SAC excitatory pathway (cholinergic) implemented as `SAC2RGCexc.mod`
(`SUFFIX SACexc`, identical structure to `SACinhib` but `e=0 mV` and `tau=3 ms`, `SAC2RGCexc.mod`
L24-26). One `SACexcsyn` per ON dendrite. The PD/ND-modulating scalar is `achMOD = 0.25` (`main.hoc`
L47, `apply_params` L299 `h.achMOD = ACH_MOD=0.25`). This is held constant across PD/ND in [t0020]
but [t0065] zeroes it for IPSP_PASSIVE (`run_protocol.py` L166 `h.achMOD = float(ACH_MOD_OFF)` where
`ACH_MOD_OFF=0.0` per `constants.py` L40).

### Bed B excitation: Exp2Syn ACh + Exp2NMDA NMDA driven by Poisson event queues

Bed B's excitatory pathway uses NEURON's built-in `Exp2Syn` mechanism for ACh (the cholinergic SAC
drive that survives in the de Rosenroll model) plus the vendored `Exp2NMDA.mod` for NMDA
(`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`).
The synapses are created in `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`
`_setup_synapses` (L189-226).

Per terminal dendrite (one E + one I synapse, no NMDA in the Vm protocol pipeline):

* **ACh (Exp2Syn)** — `tau1 = 0.1 ms` (rise), `tau2 = 4.0 ms` (decay), `e = 0 mV`, NetCon weight
  `0.001 µS` (`constants.py` L45-48). `BASE_ACH_PROB = 0.5` per release event (`run_tuning_curve.py`
  L54).
* **NMDA (Exp2NMDA)** — `tau1 = 50 ms` (deactivation, L50 default), `tau2 = 2 ms` (activation, L51
  default), `e = 0 mV` (L52), `n = 0.213 /mM`, `gama = 0.074 /mV` (Mg block, L53-54). Project
  constants give `tau1=2 ms`, `tau2=7 ms`, `e=0 mV`, `n=0.25`, `gama=0.08`, weight=`0.0015 µS`
  (`constants.py` L57-61). **Note**: `Exp2NMDA` is wired into the library but **not used by either
  tuning_curve or the EPSP/IPSP/Vm protocol** — `_setup_synapses` only creates ACh and GABA
  synapses. NMDA is parameterised in `constants.py` for potential future use but no driver places
  NMDA synapses.

The Mg block in `Exp2NMDA.mod` follows the same Jahr-Stevens form as `bipolarNMDA.mod`:

```
g = (B - A) / (1 + n * exp(-gama * local_v))    -- Exp2NMDA.mod L90
```

with the same `Voff` / `Vset` voltage-independence override (L88, default `Voff=0`). `B-A` is the
difference of two exponentials; `factor` (L80-82) normalises so that an event of weight 1 gives a
peak conductance of 1.

PD vs ND in Bed B is encoded via the **bar arrival time** projected onto the velocity axis
(`run_tuning_curve.py` `_bar_arrival_times` L92-109). The bar moves at
`BAR_VELOCITY_UM_PER_MS = 1.0`, width 250 µm (`constants.py` L78-79). For each direction the arrival
time at each terminal synapse is `BAR_START_TIME + (proj_xy - BAR_X_START) / velocity` where
`proj_xy` is the dot product of the synapse's offset from the cell origin and the unit velocity
vector. PD = 0° (rightward), ND = 180° (leftward) — see [t0066] `code/constants.py` L19-20
`DIRECTION_PD_DEG=0.0`, `DIRECTION_ND_DEG=180.0`.

The release rate at each synapse is a Gaussian envelope centred on the arrival time
(`BAR_SIGMA_MS = 30 ms`, L53), modulated by an AR(2) noise process (`_rates_with_ar2_noise`
L112-142). Spike-event times are then drawn as Poisson counts per `RATE_DT_MS = 1 ms` bin
(`_rates_to_events` L145-175) and queued via `NetCon.event(t)` inside a `FInitializeHandler`
(`run_single_trial` L286-298).

### Bed B inhibition: Exp2Syn GABA with direction-modulated release probability

Bed B's GABA synapse is also `Exp2Syn` (`_setup_synapses` L199-202): `tau1 = 0.5 ms` (rise),
`tau2 = 12 ms` (decay), `e = -60 mV` (`constants.py` L50-52). NetCon weight = `0.003 µS` per release
event (L53).

Direction selectivity in Bed B is encoded by **two mechanisms simultaneously**:

1. **Sigmoidal release probability** as a function of bar direction relative to the cell's preferred
   direction (`_gaba_prob_for_direction` `run_tuning_curve.py` L80-89). The sigmoid is
   `pref_prob + (null_prob - pref_prob) * (1 - 0.98 / (1 + exp((d - 91)/25)))` where
   `d = |direction - CELL_PREF + 180| mod 180`, `pref_prob = 0.05`, `null_prob = 0.80`,
   `CELL_PREF = 0°` (L54-57). PD ⇒ release prob ≈ 0.05; ND ⇒ release prob ≈ 0.80.
2. **AR(2) cross-channel correlation** between paired ACh and GABA streams (`ar2_noise.py`,
   `generate_ar2_batch` L68-107). `phi = (0.9, -0.1)` (`constants.py` L67). The "correlated"
   condition uses `rho = 0.6` (L68), the "uncorrelated / AMB" condition uses `rho = 0.0` (L69). The
   uncorrelated condition additionally scales the GABA NetCon weight by 1.8x
   (`GABA_SCALE_UNCORRELATED = 1.8`, L54; `_setup_synapses` parameter `gaba_weight_scale`, L189;
   applied in `run_sweep` L332).

[t0066]'s EPSP/IPSP/Vm protocol simplifies this to a fixed-direction protocol: only `RHO=0.6`
(correlated), no AMB toggle. PD = 0°, ND = 180°. EPSP_PASSIVE zeroes every GABA NetCon weight
(`run_protocol.py` L181-182); IPSP_PASSIVE zeroes every ACh NetCon weight (L184-185).

### Both protocols use the same EPSP_PASSIVE / IPSP_PASSIVE / FULL trio but implement it differently

Both [t0065] and [t0066] expose three `TrialMode` enum values: `FULL`, `EPSP_PASSIVE`,
`IPSP_PASSIVE` (both: `code/constants.py` `class TrialMode(Enum)` lines 8-13 of each). The
*semantics* are identical: FULL records the spike-generating Vm with HH on; EPSP_PASSIVE records
pure excitation (HH off, GABA silenced); IPSP_PASSIVE records pure inhibition (HH off, excitation
silenced). The *implementations* differ:

* **[t0065] (Bed A)** uses HOC-level globals: `h.exptype = 1` ⇒ HH on; `h.exptype = 2` ⇒ HH off via
  `init_active`'s `TTX=1` branch zeroing `RGCsomana` (`dsgc_model.hoc` L121-122, L137-139).
  EPSP_PASSIVE additionally sets `h.gabaMOD = 0` and `h.s2ggaba = 0` (belt-and- braces: gabaMOD
  silences the modulation envelope, s2ggaba silences the per-vesicle peak — see `run_protocol.py`
  L158-161). IPSP_PASSIVE sets `h.b2gampa = h.b2gnmda = h.s2gach = 0` and `h.achMOD = 0` (L162-167).
  Direction is encoded via `h.gabaMOD = 0.33` (PD) or `0.99` (ND) (constants L30-31).

* **[t0066] (Bed B)** uses Python-level overrides on the constructed cell. HH on/off is implemented
  by snapshotting `seg.HHst.gnabar/gkbar/gkmbar` in `_snapshot_canonical_state` (`run_protocol.py`
  L129-154) then setting them all to 0 for any non-FULL mode (`_apply_mode_overrides` L186-194).
  EPSP_PASSIVE zeroes every `bundle.ncs_gaba[i].weight[0]` (L181-182); IPSP_PASSIVE zeroes every
  `bundle.ncs_ach[i].weight[0]` (L184-185). Direction is encoded by the bar's `direction_deg`
  parameter passed to `_bar_arrival_times` (L222-226; PD=0°, ND=180° per constants L19-20).

Both protocols use `BASELINE_END_MS = 100.0` ([t0065] constants L68) or `BASELINE_WINDOW_MS = 50.0`
([t0066] constants L47) for the `baseline_v_mv` mean window, then report `peak_minus_baseline_mv`
per trial.

### Both beds share the same 350-section `DSGC` template but configure it differently

Both `RGCmodel.hoc` (Bed A) and `RGCmodelGD.hoc` (Bed B) use **the same morphology** — the upstream
Poleg-Polsky bundled cell. Compare:

* `RGCmodel.hoc` L14: `create soma, dend[350]` (Bed A,
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/RGCmodel.hoc`)
* `RGCmodelGD.hoc` L12: `create soma, dend[350]` (Bed B,
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/RGCmodelGD.hoc`)

The `topol()` proc body (the entire `connect dend[i](0), dend[j](1)` table from L17-209 in Bed A,
identical L15-209 in Bed B) defines the same connectivity. Both have 54 `shape3d_*()` procedures
(lines 212-11722 in Bed A, identical line range in Bed B) with the same pt3d coordinates. The 11
861-line vs 11 830-line difference is purely cosmetic (comments, extra template fields).

The `init()` proc differs in two ways:

* Bed A (`RGCmodel.hoc` L11801-11803): the ON/OFF sort uses
  `if (z3d(n3d()-1)>=-.16*y3d(n3d()-1)+46) {ON.append()}`; downstream `init` then places `numsyn` (=
  282\) synapse triples on the ON dendrites (L11825-11851). The `placeBIP` proc in `dsgc_model.hoc`
  then drives them.
* Bed B (`RGCmodelGD.hoc` L11801-11806): same ON/OFF sort (line 11802 verbatim), but the
  synapse-placement loop at L11824-11826 is empty (`forsec ON{ //was used to place synapses }`).
  Synapse placement is done in Python (`build_cell.py` `_setup_synapses`) on the Python-derived
  `terminal_dends` list, not on the HOC-derived `ON` SectionList.

Both apply `diam = 0.5 + 2.58*exp(-(distance(0.5)-10)/10)` per dendrite (Bed A L11814, Bed B L11814
verbatim). Both set `nseg = 1` per section (L11818). The numerical morphology is therefore identical
between the two beds — what differs is which sections receive what mechanisms and synapses.

### Default counts and shared morphology constants

Reading the `init()` procs and confirming via [t0008] `code/constants.py` L57-69:

* **Bed A**: 1 soma + 350 dend sections, 282 ON dendrites → 282 BIPsyn + 282 SACinhibsyn + 282
  SACexcsyn (846 point processes total). `BUNDLED_NUM_SOMA=1`, `BUNDLED_NUM_DEND=350`,
  `N_SYNAPSES_EACH_TYPE=282` (`code/constants.py` L59,68-69).
* **Bed B**: 1 soma + 350 dend sections. The Python `_map_tree` derives a small set of
  `primary_dends` (≈ 10), a larger set of `non_terminal_dends`, and a set of `terminal_dends` (the
  leaves) where ACh + GABA synapses land. Upstream code refers to ~177 terminal dendrites; the
  actual number is determined by morphology traversal at runtime. Total point processes per bed: 2 ×
  n_terminal (one Exp2Syn ACh + one Exp2Syn GABA per terminal). `RGCmodelGD.hoc` L10:
  `numDends = 350`.

## Reusable Code and Assets

Reminder: this is a documentation-only task. No code is implemented; the writeup synthesises
information from the cited files. There are therefore no functions or classes that need to be copied
into `tasks/t0070_writeup_two_model_beds/code/`. All cited code lives in the two registered library
assets and the four protocol tasks. The implementation step will read these files directly when
filling in tables and equations. Listed here for clarity:

### MOD mechanism files (read directly; never imported)

* **`HHst.mod`** —
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/HHst.mod`, 416 lines.
  Bed A's stochastic HH + Km + L/T-Ca channel. Use for: every Bed A conductance equation (Na:
  L249-266, Kdr: L294-297, Km: L315-318, L-Ca: L326-334, T-Ca: L355-360); default gbar values
  (L55-60); `BREAKPOINT` block showing the current expressions (L190-222). **Reuse method: cite by
  file:line in the writeup.** No copy.

* **`HHst_noiseless.mod`** —
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod`,
  397 lines. Bed B's deterministic HH + Km + L/T-Ca. Same kinetics as Bed A's `HHst.mod` (verified
  by inspection — equations at L244-351 are identical to L249-360 of Bed A). Use for: Bed B
  conductance citations. **Reuse method: cite by file:line.**

* **`bipolarNMDA.mod`** —
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/bipolarNMDA.mod`, 161
  lines. Bed A's bipolar AMPA + NMDA point process. Use for: AMPA/NMDA peak conductances (L35-36),
  kinetics (L37-39), Mg block (L40-41,102), reversal (L42), vesicular release model (L131-152).
  **Reuse method: cite by file:line.**

* **`SAC2RGCinhib.mod`** —
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCinhib.mod`, 95
  lines. Bed A's SAC GABA point process. Use for: GABA peak conductance (L23), τ (L24), reversal
  (L26), release model (L71-90). **Reuse method: cite by file:line.**

* **`SAC2RGCexc.mod`** —
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/SAC2RGCexc.mod`, 95
  lines. Bed A's SAC ACh point process. Use for: ACh peak conductance (L23, default 0.2 nS), τ (L24,
  3 ms), reversal (L25, 0 mV). **Reuse method: cite by file:line.**

* **`Exp2NMDA.mod`** —
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/Exp2NMDA.mod`,
  103 lines. Bed B's NMDA mechanism (vendored but unused by current drivers). Use for: NMDA Mg block
  formula (L90), kinetics (L50-51), default `n` and `gama` (L53-54). **Reuse method: cite by
  file:line.** The writeup should explicitly note this mechanism exists but is not wired into either
  tuning_curve or EPSP/IPSP/Vm runs.

* **`cadecay.mod`** —
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/cadecay.mod`,
  76 lines. Bed B's calcium decay. Use for: shell depth (L44), tau (L45), cainf (L46).

### HOC template files

* **`RGCmodel.hoc`** —
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/RGCmodel.hoc`, 11 861
  lines. Bed A's morphology + synapse placement. Use for: section count (`create soma, dend[350]`
  L14), topology (L17-209), 3D coordinates (`shape3d_1` to `shape3d_54`, L212-11722), ON/OFF sort
  (L11801-11803), per-dendrite diameter formula (L11814), synapse placement (L11825-11851). **Reuse
  method: cite by file:line.**

* **`RGCmodelGD.hoc`** —
  `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/RGCmodelGD.hoc`,
  11 830 lines. Bed B's morphology. Same as Bed A except synapse placement is empty (L11824-11826) —
  placement is done in Python.

* **`main.hoc`** / **`dsgc_model.hoc`** —
  `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc` and
  `dsgc_model.hoc`. Both 397 / 331 lines. Use for: synaptic conductance globals (`b2gampa`,
  `b2gnmda`, `s2ggaba`, `s2gach`, `gabaMOD`, `achMOD`: L42-47); active-channel densities
  (`init_active`, L125-163 / L114-152); placeBIP stimulus driver (L191-282 / L177-268); `update()`
  proc (L284-318 / L270-304); `init_sim` (L320-338 / L306-324). **Reuse method: cite by file:line.**

### Python configuration files

* **`tasks/t0008_port_modeldb_189347/code/constants.py`** L1-86. The single source of truth for
  every Bed A runtime parameter overridden from the HOC defaults. Lines 18-46 enumerate TSTOP_MS,
  DT_MS, CELSIUS_DEG_C, TAU1_NMDA_BIP_MS, E_SAC_INHIB_MV, all four synaptic conductances
  `B2GAMPA_NS`, `B2GNMDA_NS`, `S2GGABA_NS`, `S2GACH_NS`, `GABA_MOD`, `ACH_MOD`, `V_SHIFT_HHST_MV`,
  `N_NMDA_V_DEP`, `GAMMA_NMDA_V_DEP`. **Reuse method: cite by file:line for every parameter the
  writeup quotes.**

* **`tasks/t0008_port_modeldb_189347/code/build_cell.py`** L280-316 `apply_params`. The function
  that writes every constant into the HOC namespace at the start of every trial. Use to verify which
  of the HOC defaults are actually used vs overridden.

* **`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py`** L1-119. Bed B parameters. L26-30
  passive cable; L33-42 channel densities (mS/cm² → S/cm² conversion at boundary); L45-61 ACh / GABA
  / NMDA synaptic kinetics; L67-71 AR(2) noise; L78-89 bar stimulus.

* **`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py`** L192-248 `_configure_soma` /
  `_configure_dends`. The Python boundary that writes mS/cm² constants into S/cm² `seg.HHst.gnabar`
  etc. for every section.

* **`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py`** L189-226 `_setup_synapses`,
  L80-89 `_gaba_prob_for_direction`, L92-109 `_bar_arrival_times`. The synaptic + stimulus reference
  code for Bed B.

* **`tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py`** L146-244. The EPSP/IPSP/Vm
  protocol on Bed A. Use for the PD/ND encoding column of the side-by-side table.

* **`tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py`** L129-298. The EPSP/IPSP/Vm
  protocol on Bed B. Same purpose as t0065's.

## Lessons Learned

* **Cross-bed mechanism naming is misleading**: both beds insert a mechanism named `HHst` but the
  source `.mod` files differ. Bed A uses the Linaro stochastic variant; Bed B uses a noise-stripped
  derivative. The kinetics happen to be byte-identical but a reader who sees `HHst` in both
  libraries should not assume `seed`, `NF`, or `mulnoise` mean the same thing. The writeup must
  label them as `HHst (stochastic)` and `HHst (noiseless)` to avoid confusion. ([t0008] HHst.mod
  L1-51 vs [t0024] HHst_noiseless.mod L1-51.)

* **Effective parameter values can hide behind GLOBAL vs RANGE in MOD**: `tau`, `e`, and `gsingle`
  in `SAC2RGCinhib.mod` are GLOBAL (L7), not RANGE — so HOC's `tau_SACinhib = 30` updates the
  per-instance `tau` for *every* SACinhib instance. `gsingle_SACinhib = s2ggaba` likewise updates
  the per-vesicle peak globally. The writeup should report effective runtime values, not the `.mod`
  PARAMETER defaults.

* **Bed B does not use NMDA in any current driver** despite vendoring `Exp2NMDA.mod` and
  parameterising `NMDA_TAU1_MS`, `NMDA_TAU2_MS`, `NMDA_WEIGHT_US` in [t0024] `code/constants.py`
  L56-61. `_setup_synapses` in `run_tuning_curve.py` (L189-226) only creates ACh and GABA synapses.
  The writeup should note this asymmetry — Bed A always has NMDA active; Bed B has the NMDA
  mechanism wired but not placed.

* **Bed A's `gabaMOD` is the modulation envelope scaler, not a per-vesicle peak**: looking at
  `placeBIP` line 256 (`mulnoise.fill(VampT*gabaMOD,...)`), `gabaMOD` multiplies the *active
  portion* of the SAC inhibitory drive trace, which then plays into `SACinhibsyn.Vinf`. It scales
  the presynaptic voltage, not the postsynaptic conductance. This is unintuitive — many readers will
  expect `gabaMOD` to be a postsynaptic gain. The writeup should be explicit.

* **The PD/ND encoding mechanism differs entirely between beds**: Bed A keeps the bar geometry fixed
  and swaps `gabaMOD` (modulation-envelope scalar; PD=0.33, ND=0.99). Bed B keeps the GABA
  conductance fixed and changes the bar's spatial direction (PD=0°, ND=180°), which changes the
  per-synapse arrival time *and* the GABA release probability via the sigmoid
  `_gaba_prob_for_direction`. The writeup must present these as fundamentally different encodings,
  not as "two ways to do the same thing".

* **Bed B uses Python-driven NetCon events for synaptic input**: there is no presynaptic-voltage
  vesicle-release model like Bed A's `bipolarNMDA.mod`. Instead, AR(2)-modulated rates are converted
  to Poisson event times in Python (`_rates_to_events` L145-175 of `run_tuning_curve.py`) and queued
  via `nc.event(t)`. This makes Bed B's noise model fundamentally Python-side, not HOC-side. The
  writeup should document this clearly.

* **Bed A inherits `Ca` currents at zero; Bed B inherits them at default 3e-4 S/cm²**: `init_active`
  in `dsgc_model.hoc` L155-156 sets `RGCcaT=0`, `RGCcaL=0` — and `update()` L302-303 then writes
  those zeros into `glbar_HHst` / `gtbar_HHst` for every section. Bed B's `_configure_soma` /
  `_configure_dends` never write `glbar_HHst` or `gtbar_HHst`, so the `HHst_noiseless.mod` PARAMETER
  defaults `glbar=0.0003`, `gtbar=0.0003` (L57-58) remain active on every section. **This is a
  non-trivial biophysical difference between the beds.**

## Recommendations for This Task

1. **Use a side-by-side template** for the two beds: same heading order, same equation formatting,
   same column structure for conductance tables. The task description specifies this; it should be
   honoured strictly.

2. **Cite every numerical parameter with `file:line`** in a footnote-style superscript or in the
   source column of each table. Use the form `tasks/t0008.../sources/HHst.mod L249` (relative to
   repo root). The implementation step needs to be auditable.

3. **Lead each bed with the canonical HH equation** in the form
   `C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj` then expand `Σᵢ Iᵢ` for that bed. Use the same notation in
   both beds so the comparison table at the end works.

4. **Tabulate the conductance currents** with columns: channel, gating, V_half_act, τ_m,
   V_half_inact, τ_h, gbar (per compartment class), e_rev, source citation. For Bed B the gbar
   column has three sub-rows (soma, primary, terminal). For Bed A the gbar column has two sub-rows
   (soma, dend) with a "passive default" footnote noting that `use_active=0` is the project default.

5. **Include the synaptic-conductance equation explicitly** for each pathway. Bed A's `bipNMDA.mod`
   `gNMDA = (A-B) / (1 + n·exp(-gama·V))` (L102) and Bed B's `Exp2NMDA.mod`
   `g = (B-A) / (1 + n·exp(-gama·V))` (L90) are mathematically identical (sign flip on `B-A` is
   matched by the rise/decay convention). Stating this side-by-side makes the cross-bed comparison
   rigorous.

6. **Document the PD/ND encoding mechanism explicitly** for each bed:
   * Bed A: `gabaMOD = 0.33` (PD) vs `0.99` (ND), applied via the modulation-envelope scalar in
     `placeBIP`. BIP synapse coordinates fixed.
   * Bed B: bar `direction_deg = 0.0` (PD) vs `180.0` (ND), applied via per-synapse arrival time in
     `_bar_arrival_times` and via the GABA release-probability sigmoid in
     `_gaba_prob_for_direction`. Conductances fixed at canonical state.

7. **Add a "Differences from the original paper" subsection per bed**:
   * Bed A: Ca currents zeroed (vs Poleg-Polsky 2016's enabled L/T-Ca); `tau1NMDA = 60 ms`
     overridden from the `.mod` default of 50 ms; `n = 0.3`, `gama = 0.07` overridden from defaults
     `0.25` / `0.08`.
   * Bed B: NMDA mechanism vendored but not wired into any driver; HHst is the noiseless variant (de
     Rosenroll's upstream uses the same); release noise is AR(2) Python-side rather than the
     upstream Python `ei_balance.py` model (which the t0024 port reimplements in simplified form).

8. **Build the side-by-side comparison table** at the end with rows: number of compartments,
   morphology source, ON-dendrite count, synapses per dendrite, presence of NMDA, AMPA peak per
   release event, GABA peak per release event, GABA reversal, ACh peak, NMDA Mg-block parameters, HH
   variant, Ca currents enabled, Ra, Cm, celsius, dt, tstop, v_init, PD/ND encoding mechanism. This
   is the single most-cited table in the writeup.

## Task Index

### [t0008]

* **Task ID**: `t0008_port_modeldb_189347`
* **Name**: Port ModelDB 189347 and similar DSGC compartmental models to NEURON
* **Status**: completed
* **Relevance**: Owns the `modeldb_189347_dsgc` library asset (Bed A's HOC + MOD sources). The
  writeup's Bed A section enumerates every conductance and synapse parameter from this task's
  `assets/library/modeldb_189347_dsgc/sources/` directory. The Python wrappers
  (`code/build_cell.py`, `code/constants.py`) define which HOC defaults are overridden at runtime —
  this is the only authoritative source for effective parameter values.

### [t0020]

* **Task ID**: `t0020_port_modeldb_189347_gabamod`
* **Name**: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol
* **Status**: completed
* **Relevance**: Establishes the canonical PD/ND encoding for Bed A — `gabaMOD = 0.33` (PD) and
  `gabaMOD = 0.99` (ND), applied via `h.gabaMOD = ...` then `update()` + `placeBIP()`.
  `code/run_gabamod_sweep.py` `run_one_trial_gabamod` (L130-182) is the canonical reference for how
  this swap is realised. The writeup's "Synaptic inhibition (PD vs ND)" subsection for Bed A cites
  this task.

### [t0024]

* **Task ID**: `t0024_port_de_rosenroll_2026_dsgc`
* **Name**: Port de Rosenroll 2026 DSGC model
* **Status**: completed
* **Relevance**: Owns the `de_rosenroll_2026_dsgc` library asset (Bed B's HOC + MOD sources) and the
  Python driver that defines Bed B's synapses, release-noise model, and bar stimulus.
  `code/build_cell.py` (L192-248) writes every channel density; `code/constants.py` (L26-89) is the
  single source of truth for every Bed B parameter; `code/run_tuning_curve.py` (L80-226) defines the
  synapse construction, GABA direction sigmoid, and bar arrival times. The writeup's entire Bed B
  section depends on this task.

### [t0065]

* **Task ID**: `t0065_t0020_epsp_ipsp_vm_protocol`
* **Name**: Test t0020 deposited DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol
* **Status**: completed
* **Relevance**: Defines the FULL / EPSP_PASSIVE / IPSP_PASSIVE trial trio for Bed A and the
  protocol-level mapping from `h.exptype = 1/2` to "HH on / HH off". `code/run_protocol.py` L146-194
  documents how each mode is produced — the writeup's "Differences from the original paper"
  subsection for Bed A cites this task as the canonical Vm-recording protocol.

### [t0066]

* **Task ID**: `t0066_t0024_epsp_ipsp_vm_protocol`
* **Name**: Test t0024 de Rosenroll DSGC under EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol
* **Status**: completed
* **Relevance**: Defines the FULL / EPSP_PASSIVE / IPSP_PASSIVE trial trio for Bed B and the
  Python-side mechanism for HH on/off (zero `seg.HHst.gnabar/gkbar/gkmbar` per segment) and for
  synaptic silencing (zero `nc.weight[0]`). `code/run_protocol.py` L129-194 is the canonical
  reference. The writeup's "Synaptic excitation (PD vs ND)" and "Synaptic inhibition (PD vs ND)"
  subsections for Bed B cite this task as the protocol-level driver.
