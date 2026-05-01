// Typst source for t0071 detailed writeup.
// Compile with `code/render_pdf.py` (uses the `typst` Python wheel).

#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2.5cm),
  numbering: "1",
)

#set text(size: 10pt)
#set par(justify: true, leading: 0.65em)

#set heading(numbering: none)
#show heading.where(level: 1): set text(size: 16pt, weight: "bold")
#show heading.where(level: 2): set text(size: 13pt, weight: "bold")
#show heading.where(level: 3): set text(size: 11.5pt, weight: "bold")
#show heading.where(level: 4): set text(size: 10.5pt, weight: "bold", style: "italic")

#show raw.where(block: false): box.with(fill: luma(240), inset: (x: 2pt), outset: (y: 2pt), radius: 1pt)

= Two Standard DSGC Model Beds: A Side-by-Side HH-Equation Reference (v2)

#emph[Task t0071_t0070_synaptic_eqs_pdf] #h(1fr) #emph[2026-05-01]

== Note

This document is the *v2 writeup* of the project's two standard DSGC model beds and *supersedes*
t0070's `results/results_detailed.md`. Two gaps in the v1 writeup are addressed here:

+ *Synaptic-current equations were missing.* The Hodgkin-Huxley membrane equation and every active
  conductance were given as explicit $I = g dot.c ... dot.c (V - E)$ blocks, but the synaptic
  currents (AMPA, NMDA, GABA, ACh in Bed A; Exp2Syn ACh, Exp2Syn GABA in Bed B) were described in
  prose and parameter tables only. This v2 adds the canonical
  $ I_"syn" (t,V) = g_"syn" (t,V) dot.c (V - E_"syn") $
  block under each bed's "Synaptic excitation" and "Synaptic inhibition" subsections, with the
  state-variable evolution and discrete release rule clearly stated. Five new equation blocks
  total: Bed A BIPsyn AMPA, Bed A BIPsyn NMDA, Bed A SACinhibsyn GABA, Bed A SACexcsyn ACh, and
  Bed B Exp2Syn ACh + Exp2Syn GABA.

+ *No typeset PDF.* v1 was markdown only. This v2 ships `results/results_detailed.typ` (Typst
  source) and `results/results_detailed.pdf` (typeset PDF) so equations render in proper math
  fonts. Every equation in the v1 fenced text blocks has been rewritten in math syntax so
  downstream renderers typeset them correctly.

No biophysical parameter value has changed between t0070 and this v2. Every numerical value carries
the same `code/<file>:L<line>` citation; only the surrounding markup has changed and the five new
equation blocks have been added.

== Summary

This task supersedes t0070's research-paper writeup of the project's two canonical
direction-selective ganglion cell (DSGC) model substrates, adding the missing synaptic-current
equation blocks and a typeset PDF. *Bed A* is the deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC
ported in t0008 (ModelDB 189347, library `modeldb_189347_dsgc`); it is the substrate for t0020,
t0065, t0067, t0068, and t0069. *Bed B* is the de Rosenroll 2026 DSGC ported in t0024 (library
`de_rosenroll_2026_dsgc`); it is the substrate for t0066. Each bed is presented in parallel
structure: Morphology #sym.arrow.r canonical Hodgkin-Huxley membrane equation #sym.arrow.r
conductance table #sym.arrow.r synaptic excitation (PD vs ND) #sym.arrow.r synaptic inhibition
(PD vs ND) #sym.arrow.r differences from the original paper. A side-by-side comparison table at
the end summarises the headline differences across 18 dimensions. Every numerical parameter
carries a `code/<file>:line` citation back to the committed source so the document is fully
auditable.

== Methodology

- *Machine*: local Windows 11 workstation; no remote compute, no GPU, no NEURON simulations.
- *Runtime*: total ~2 hours of equation transcription, Typst authoring, and PDF rendering. Typst
  compile under 5 seconds.
- *Methods*: documentation-only correction task. No new experiments were run. Every parameter
  quoted is the same value cited in t0070, traced back to a specific line of the committed library
  source.
- *Schematic figures*: four PNGs in `results/images/` are reused verbatim from t0070; copied with
  `shutil.copyfile` and not regenerated.
- *Equation typesetting*: every equation is in math syntax. Inline math uses `$...$` (no
  whitespace inside delimiters) and display math uses `$ ... $` (with whitespace) per Typst
  convention.

== Bed A: Poleg-Polsky 2016 (t0008 + t0020)

Bed A wraps the deposited Poleg-Polsky & Diamond 2016 ON-OFF DRD4 DSGC from ModelDB 189347 with no
modification to the morphology or kinetics. The library asset is
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`.

=== Morphology

#figure(
  image("images/bed_a_morphology.png", width: 90%),
  caption: [Figure A1 (illustrative; not to scale): 1 soma + 350 dendrite sections; 282 ON-typed
  dendrites bear the synaptic triple (BIPsyn AMPA + NMDA bipolar drive, SACinhibsyn GABA, SACexcsyn
  ACh); the OFF dendrites bear no synapses.],
)

The cell is built by the deposited HOC template `RGCmodel.hoc` (11 861 lines). Key facts:

- *Section count*: 1 soma + 350 `dend[i]` sections (`RGCmodel.hoc:L14`).
- *Compartment discretisation*: every section has $n_"seg" = 1$ (`RGCmodel.hoc:L11818`).
- *Per-dendrite diameter*: $"diam" = 0.5 + 2.58 dot.c exp(-(d(0.5)-10)/10)$ µm
  (`RGCmodel.hoc:L11814`).
- *ON / OFF sort*: 282 ON dendrites, 68 OFF (`RGCmodel.hoc:L11801-L11803`).
- *Synapse placement*: 846 point processes per cell (`RGCmodel.hoc:L11825-L11851`).
- *Passive cable*: $R_a = 100 #h(2pt) Omega dot.c "cm"$, $c_m = 1 #h(2pt) mu"F/cm"^2$,
  celsius $= 32$ °C, $V_"init" = -65$ mV.

=== Membrane equation

The Hodgkin-Huxley membrane equation governs each compartment of Bed A:

$ C_m frac(d V, d t) = - sum_i I_i - I_"syn" - I_"inj" $

The active currents $sum_i I_i$ enumerated for Bed A (taken from `HHst.mod:L190-L222` BREAKPOINT
block) are:

$ I_"Na" = g_"Na" dot.c m^3 dot.c h dot.c (V - E_"Na") quad #text[(HHst Na fast)] $

$ I_"Kdr" = g_"Kdr" dot.c n^4 dot.c (V - E_"K") quad #text[(HHst K delayed rectifier)] $

$ I_"Km" = g_"Km" dot.c n_m dot.c (V - E_"K") quad #text[(HHst K M-type)] $

$ I_"leak" = g_"leak" dot.c (V - E_"leak") quad #text[(HHst leak; zleak noise term off)] $

The `HHst.mod` source also defines $I_"CaL" = g_"CaL" dot.c l_m^2 dot.c l_h dot.c (V - E_"Ca")$
and $I_"CaT" = g_"CaT" dot.c t_m^2 dot.c t_h dot.c (V - E_"Ca")$ (`HHst.mod:L208-L209`), but Bed A
*explicitly zeros* these on every section in `init_active()` (`main.hoc:L155-L156`). A global
voltage shift $Delta V_"shift_HHst" = -4$ mV is applied to every gating variable.

=== Conductance table (Bed A)

#table(
  columns: (auto, auto, auto, auto, auto, auto),
  align: (left, left, right, right, right, left),
  [*Channel*], [*Gating*], [*gbar (S/cm²)*], [*$E_"rev"$ (mV)*], [*Notes*], [*Source*],
  [Na (soma)], [$m^3 h$], [0.4], [+60], [HHst Na fast], [`main.hoc:L148`],
  [Na (dend)], [$m^3 h$], [2e-4], [+60], [HHst Na fast], [`main.hoc:L152`],
  [Kdr (soma)], [$n^4$], [0.07], [-90], [HHst K delayed rectifier], [`main.hoc:L149`],
  [Kdr (dend)], [$n^4$], [7e-3], [-90], [], [`main.hoc:L153`],
  [Km (soma)], [$n_m$], [5e-4], [-90], [HHst K M-type, `taukm = 1`], [`main.hoc:L150`],
  [Km (dend)], [$n_m$], [0], [-90], [zeroed], [`main.hoc:L154`],
  [Leak (passive)], [-], [5e-5], [-60], [`pas` mode], [`main.hoc:L161`],
  [Leak (active)], [-], [5.5e-4], [-60], [`gleak_HHst`], [`main.hoc:L161`],
  [CaL], [$l_m^2 l_h$], [0], [$E_"Ca"$], [zeroed by `init_active`], [`main.hoc:L155, L302`],
  [CaT], [$t_m^2 t_h$], [0], [$E_"Ca"$], [zeroed by `init_active`], [`main.hoc:L156, L303`],
)

=== Synaptic excitation (PD vs ND)

#figure(
  image("images/bed_a_synaptic_diagram.png", width: 90%),
  caption: [Figure A2 (illustrative; analytically computed, not a NEURON trace): top row plots
  $g_"AMPA"$, $g_"NMDA"$, and $g_"GABA" dot.c "gabaMOD" = 0.33$ (PD); bottom row uses
  $"gabaMOD" = 0.99$ (ND). Bipolar excitation is unchanged across PD and ND.],
)

Bed A's excitatory drive is implemented as a single `bipNMDA` POINT_PROCESS combining AMPA and
voltage-dependent NMDA (`bipolarNMDA.mod`). One `BIPsyn` instance is placed at the midpoint of
every ON dendrite (282 instances total).

==== AMPA component — canonical synaptic-current block

The AMPA conductance is a single-decay state and the current obeys the canonical ohmic form
(`bipolarNMDA.mod:L103`):

$ I_"AMPA" (t,V) = 10^(-3) thin g_"AMPA" (t) thin (V - E_"AMPA"), quad E_"AMPA" = 0 thick "mV" $

with state-variable evolution and per-release update (`bipolarNMDA.mod:L156, L143`):

$ frac(d g_"AMPA", d t) = - frac(g_"AMPA", tau_"AMPA"), quad tau_"AMPA" = 2.0 thick "ms" $

$ #text[on each release event] k: quad g_"AMPA" arrow.l g_"AMPA" + r_k thin overline(g)_"AMPA"^"single", quad overline(g)_"AMPA"^"single" = 0.25 thick "nS" $

The factor $10^(-3)$ converts $g_"AMPA"$ from nS to µS so that $I$ is in nA when $V$ is in mV
(NEURON convention). $r_k in {0,1}$ is the per-vesicle Bernoulli release outcome.

==== NMDA component — bi-exponential rise/decay × Mg block

The NMDA conductance is the difference of two exponentials gated by a Jahr-Stevens-style Mg block
(`bipolarNMDA.mod:L102, L104`):

$ g_"NMDA" (t,V) = frac(A(t) - B(t), 1 + n dot.c exp(-gamma thin V_"loc")) $

$ I_"NMDA" (t,V) = 10^(-3) thin g_"NMDA" (t,V) thin (V - E_"NMDA"), quad E_"NMDA" = 0 thick "mV" $

with $V_"loc" = V (1 - V_"off") + V_"set" V_"off"$ ($V_"off" = 0$ uses the postsynaptic voltage;
$V_"off" = 1$ clamps to $V_"set" = -43$ mV). Bi-exponential states (`bipolarNMDA.mod` DERIVATIVE
block):

$ frac(d A, d t) = - frac(A, tau_(1\,"NMDA")), quad frac(d B, d t) = - frac(B, tau_(2\,"NMDA")) $

$ #text[on each release event] k: quad A arrow.l A + r_k thin overline(g)_"NMDA"^"single", quad B arrow.l B + r_k thin overline(g)_"NMDA"^"single" $

with $tau_(1\,"NMDA") = 60$ ms (decay), $tau_(2\,"NMDA") = 2$ ms (rise),
$overline(g)_"NMDA"^"single" = 0.5$ nS, $n = 0.30$ mM⁻¹, $gamma = 0.07$ mV⁻¹.

==== Vesicular release model (shared by AMPA and NMDA)

Vesicle release is updated every $Delta t_"rel" = 1$ ms (`bipolarNMDA.mod:L81`). The presynaptic
envelope $V_"pre"$ tracks the bar-driven input $V_"inf"$ via a low-pass filter
(`bipolarNMDA.mod:L157`):

$ frac(d V_"pre", d t) = frac(V_"inf" - V_"pre", tau_V), quad tau_V = 30 thick "/ms" $

Each release-tick (`bipolarNMDA.mod:L131-L152`), the per-vesicle release probability is set to
$s_oo = V_"pre" / 100$, and over the available pool of `numves` vesicles each is released
independently with probability $s_oo$. The vesicle pool has `maxves` $= 10$ and replenishes at
rate `newves` $= 0.002$ ms⁻¹ (project override of the `bipolarNMDA.mod:L23` default of 0.01 ms⁻¹).

==== SACexcsyn (cholinergic) — canonical synaptic-current block

A parallel cholinergic SAC pathway is also active: `SACexcsyn` (one per ON dendrite). Its kinetic
form is identical to the SACinhibsyn GABA mechanism:

$ I_"ACh" (t,V) = 10^(-3) thin g_"ACh" (t) thin (V - E_"ACh"), quad E_"ACh" = 0 thick "mV" $

$ frac(d g_"ACh", d t) = - frac(g_"ACh", tau_"ACh"), quad tau_"ACh" = 3 thick "ms" $

$ #text[on release event] k: quad g_"ACh" arrow.l g_"ACh" + r_k thin overline(g)_"ACh"^"single", quad overline(g)_"ACh"^"single" = 0.5 thick "nS" $

Driven by the same Bernoulli release model as `bipNMDA`, with $s_oo = V_"pre" / 100$ and the
modulating scalar `achMOD` $= 0.25$ multiplied into the presynaptic envelope (`main.hoc:L47`).

=== Synaptic inhibition (PD vs ND)

Bed A's inhibition is a single `SACinhib` POINT_PROCESS (`SAC2RGCinhib.mod`, 95 lines). One
`SACinhibsyn` instance per ON dendrite (282 instances).

==== SACinhibsyn (GABAergic) — canonical synaptic-current block

The conductance is a single-decay state with vesicular release (`SAC2RGCinhib.mod:L55, L92, L83`):

$ I_"GABA" (t,V) = 10^(-3) thin g_"GABA" (t) thin (V - E_"GABA"), quad E_"GABA" = -60 thick "mV" $

$ frac(d g_"GABA", d t) = - frac(g_"GABA", tau_"GABA"), quad tau_"GABA" = 30 thick "ms" $

$ #text[on release event] k: quad g_"GABA" arrow.l g_"GABA" + r_k thin overline(g)_"GABA"^"single", quad overline(g)_"GABA"^"single" = 0.5 thick "nS" $

The release model uses the same Bernoulli-over-vesicles structure. Direction selectivity enters
via the multiplicative `gabaMOD` scalar applied to $V_"inf"$ in `placeBIP()`
(`dsgc_model.hoc:L242-L243`):

$ "mulnoise.fill"(V_"ampT" dot.c "gabaMOD",  ...)  arrow.r.double  "noisevecSACI"[i]."mul"("mulnoise")  arrow.r.double  "SACinhibsyn"[i].V_"inf" $

so a `gabaMOD` $= 0.99$ trial scales $V_"inf"$ (and thus $s_oo$, and thus the per-vesicle release
probability) by ~3× relative to a `gabaMOD` $= 0.33$ trial. The per-vesicle peak conductance
$overline(g)_"GABA"^"single" = 0.5$ nS is unchanged across PD and ND.

#table(
  columns: (auto, auto, auto, auto),
  align: (left, right, left, left),
  [*Trial*], [*`gabaMOD`*], [*Effective release-probability scaling*], [*Source*],
  [PD (preferred)], [0.33], [weak inhibition; $s_oo$ envelope ~33% of peak], [`constants.py:L37`],
  [ND (null)], [0.99], [strong inhibition; $s_oo$ envelope ~99% of peak (~3× PD)], [`constants.py:L38`],
)

== Bed B: de Rosenroll 2026 (t0024)

Bed B wraps a subset of `geoffder/ds-circuit-ei-microarchitecture` at commit
`a23f642aa6557a23a51bf76f51e420e8149773fa`, vendored as
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`. The cell template
is inherited from the same Poleg-Polsky bundled cell as Bed A, but the active-channel densities
are tier-stratified, the HHst variant is the noiseless deterministic derivative, and synapses are
reimplemented in Python on top of `Exp2Syn`.

=== Morphology

#figure(
  image("images/bed_b_morphology.png", width: 90%),
  caption: [Figure B1: 1 soma + 350 dendrites discretised into three Python-derived tiers: ~10
  primary dends (darker green), ~163 non-terminal mid dends (medium green), and ~177 terminal
  dends (light green) bearing one Exp2Syn ACh + one Exp2Syn GABA each.],
)

The cell uses the same 350-section template as Bed A, reimplemented as `RGCmodelGD.hoc`
(11 830 lines). Key facts:

- *Section count*: 1 soma + 350 `dend[i]` (`RGCmodelGD.hoc:L12`).
- *Tier classification*: `_map_tree` partitions dendrites into ~10 primary, ~163 non-terminal,
  ~177 terminal (`build_cell.py:L140-L168`).
- *Synapse placement*: every terminal dendrite hosts one Exp2Syn ACh + one Exp2Syn GABA.
- *Passive cable*: $R_a = 100$ Ω·cm, $c_m = 1$ µF/cm², celsius $= 36.9$ °C,
  $V_"init" = -60$ mV.

=== Membrane equation

The Hodgkin-Huxley membrane equation governs each compartment of Bed B, written in identical
notation to Bed A:

$ C_m frac(d V, d t) = - sum_i I_i - I_"syn" - I_"inj" $

The active currents enumerated for Bed B (`HHst_noiseless.mod:L184-L222`) are:

$ I_"Na" = g_"Na" dot.c m^3 dot.c h dot.c (V - E_"Na") $

$ I_"Kdr" = g_"Kdr" dot.c n^4 dot.c (V - E_"K") $

$ I_"Km" = g_"Km" dot.c n_m dot.c (V - E_"K") $

$ I_"leak" = g_"leak" dot.c (V - E_"leak") $

$ I_"CaL" = g_"CaL" dot.c l_m^2 dot.c l_h dot.c (V - E_"Ca") quad #text[(active by default)] $

$ I_"CaT" = g_"CaT" dot.c t_m^2 dot.c t_h dot.c (V - E_"Ca") quad #text[(active by default)] $

Unlike Bed A, the Ca currents are at their `HHst_noiseless.mod` PARAMETER defaults on every
section: $g_"lbar" = 3 times 10^(-4)$ S/cm² and $g_"tbar" = 3 times 10^(-4)$ S/cm². Every section
also has `cad` (calcium-decay shell) inserted with $"depth" = 0.1$ µm, $tau_r = 5$ ms,
$"Ca"_oo = 2 times 10^(-4)$ mM. Reversal potentials: $E_"Na" = +60$ mV, $E_"K" = -90$ mV,
$E_"leak" = -60$ mV, $E_"Ca" = +132$ mV.

=== Conductance table (Bed B)

#table(
  columns: (auto, auto, auto, auto, auto),
  align: (left, left, right, right, left),
  [*Channel*], [*Gating*], [*gbar (S/cm²)*], [*$E_"rev"$ (mV)*], [*Source*],
  [Na (soma)], [$m^3 h$], [0.150], [+60], [`constants.py:L34` `GNA_SOMA_MS = 150`],
  [Na (primary)], [$m^3 h$], [0.200], [+60], [`constants.py:L35`],
  [Na (non-terminal)], [$m^3 h$], [0 (zeroed)], [+60], [`constants.py:L36`],
  [Na (terminal)], [$m^3 h$], [0.030], [+60], [`constants.py:L37`],
  [Kdr (soma)], [$n^4$], [0.035], [-90], [`constants.py:L38`],
  [Kdr (primary)], [$n^4$], [0.035], [-90], [`constants.py:L39`],
  [Kdr (non-term + term)], [$n^4$], [0.025], [-90], [`constants.py:L40`],
  [Km (uniform)], [$n_m$], [0.003], [-90], [`constants.py:L41`],
  [Leak (uniform)], [-], [1.667e-4], [-60], [`constants.py:L42` `G_LEAK_MS = 0.1667`],
  [CaL (uniform)], [$l_m^2 l_h$], [3e-4], [+132], [`HHst_noiseless.mod:L57` PARAMETER default],
  [CaT (uniform)], [$t_m^2 t_h$], [3e-4], [+132], [`HHst_noiseless.mod:L58` PARAMETER default],
  [`cad` (uniform)], [calcium decay], [-], [-], [`cadecay.mod:L44-L46`],
)

Note: Bed B's Na density on the primary dendrites (0.200 S/cm²) is *higher than the soma*
(0.150 S/cm²); non-terminal mid dendrites have Na zeroed entirely while Kdr remains at
0.025 S/cm². Inherited from upstream `ei_balance.py`.

=== Synaptic excitation (PD vs ND)

#figure(
  image("images/bed_b_synaptic_diagram.png", width: 90%),
  caption: [Figure B2: Exp2Syn ACh and Exp2Syn GABA traces from 5 representative terminal
  dendrites placed 25 µm apart along the bar's velocity axis. Top = PD (bar 0°, sweeping
  left#sym.arrow.r right); bottom = ND (bar 180°, sweeping right#sym.arrow.r left).],
)

Bed B's excitatory drive is implemented as the NEURON built-in `Exp2Syn` mechanism for ACh. One
Exp2Syn ACh instance is placed on every terminal dendrite (~177 instances) in
`run_tuning_curve.py:L189-L226 _setup_synapses`.

==== Exp2Syn ACh — canonical synaptic-current block

NEURON's standard `Exp2Syn` is a normalised bi-exponential mechanism. Its conductance is the
difference of two exponentials with decay $tau_2$ and rise $tau_1$, normalised so an event of
NetCon weight 1 produces a peak conductance of 1; the current obeys the ohmic form:

$ g_"ACh" (t) = f_"ACh" thin (B(t) - A(t)), quad f_"ACh" = frac(1, -exp(-t_p\/tau_1) + exp(-t_p\/tau_2)), quad t_p = frac(tau_1 thin tau_2, tau_2 - tau_1) ln frac(tau_2, tau_1) $

$ I_"ACh" (t,V) = g_"ACh" (t) thin (V - E_"ACh"), quad E_"ACh" = 0 thick "mV" $

with state-variable evolution

$ frac(d A, d t) = - frac(A, tau_(1\,"ACh")), quad frac(d B, d t) = - frac(B, tau_(2\,"ACh")), quad tau_(1\,"ACh") = 0.1 thick "ms",  tau_(2\,"ACh") = 4.0 thick "ms" $

$ #text[on each NetCon event:] quad A arrow.l A + w_"ACh", quad B arrow.l B + w_"ACh", quad w_"ACh" = 0.001 thick mu"S" $

Net effect: each `NetCon.event(t)` produces a conductance pulse of peak amplitude $w_"ACh"$ (in
µS), so $I$ is in nA when $V$ is in mV (NEURON's $g(V-E)$ convention already includes the µS-to-nA
scaling — no extra $10^(-3)$ factor needed unlike `bipolarNMDA.mod` which works in nS internally).

#table(
  columns: (auto, auto, auto, auto),
  align: (left, right, left, left),
  [*Parameter*], [*Value*], [*Units*], [*Source*],
  [Rise `tau1`], [0.1], [ms], [`constants.py:L45` `ACH_TAU1_MS = 0.1`],
  [Decay `tau2`], [4.0], [ms], [`constants.py:L46`],
  [Reversal `e`], [0], [mV], [`constants.py:L47`],
  [NetCon weight], [0.001], [µS], [`constants.py:L48`],
  [`BASE_ACH_PROB`], [0.5], [-], [`run_tuning_curve.py:L54`],
)

*PD vs ND encoding for excitation: per-synapse arrival times*. The bar moves at $v_"bar" = 1.0$
µm/ms with width 250 µm. For each direction the arrival time at each terminal synapse is computed
by `_bar_arrival_times` (`run_tuning_curve.py:L92-L109`):

$ t_"arr" ("syn") = t_"bar_start" + frac("proj"_(x y) ("syn") - x_"bar_start", v_"bar") $

where $"proj"_(x y) ("syn")$ is the dot product of the synapse's offset from the cell origin with
the unit velocity vector. PD = 0° (rightward), ND = 180° (leftward). The release rate is a
Gaussian envelope ($sigma_"bar" = 30$ ms), modulated by an AR(2) noise process.

=== Synaptic inhibition (PD vs ND)

Bed B's inhibition is also `Exp2Syn`. One Exp2Syn GABA instance per terminal dendrite (~177
instances) (`run_tuning_curve.py:L199-L202`).

==== Exp2Syn GABA — canonical synaptic-current block

Identical in form to Exp2Syn ACh, with reversal at the GABA reversal and direction-encoding via
the per-event Bernoulli release probability $p_"rel" (theta)$ and the AR(2) noise envelope:

$ g_"GABA" (t) = f_"GABA" thin (B(t) - A(t)), quad f_"GABA" = frac(1, -exp(-t_p\/tau_1) + exp(-t_p\/tau_2)), quad t_p = frac(tau_1 thin tau_2, tau_2 - tau_1) ln frac(tau_2, tau_1) $

$ I_"GABA" (t,V) = g_"GABA" (t) thin (V - E_"GABA"), quad E_"GABA" = -60 thick "mV" $

with state-variable evolution

$ frac(d A, d t) = - frac(A, tau_(1\,"GABA")), quad frac(d B, d t) = - frac(B, tau_(2\,"GABA")), quad tau_(1\,"GABA") = 0.5 thick "ms", quad tau_(2\,"GABA") = 12 thick "ms" $

and a per-event Bernoulli release driven by the direction-dependent probability:

$ #text[on each scheduled event] k: quad #text[release with probability] p_"rel" (theta); quad #text[if released:] quad A arrow.l A + w_"GABA", quad B arrow.l B + w_"GABA" $

with $w_"GABA" = 0.003 thick mu"S"$ (`constants.py:L53`).

#table(
  columns: (auto, auto, auto, auto),
  align: (left, right, left, left),
  [*Parameter*], [*Value*], [*Units*], [*Source*],
  [Rise `tau1`], [0.5], [ms], [`constants.py:L50` `GABA_TAU1_MS = 0.5`],
  [Decay `tau2`], [12.0], [ms], [`constants.py:L51`],
  [Reversal `e`], [-60], [mV], [`constants.py:L52`],
  [NetCon weight], [0.003], [µS], [`constants.py:L53`],
)

*PD vs ND encoding for inhibition: two simultaneous mechanisms.*

+ *Sigmoidal release probability* (`run_tuning_curve.py:L80-L89` `_gaba_prob_for_direction`):

$ p_"rel" (d) = p_"pref" + (p_"null" - p_"pref") (1 - frac(0.98, 1 + exp((d - 91)\/25))) $

$ d = abs(theta - theta_"cell_pref" + 180) thin mod thin 180 $

with $p_"pref" = 0.05$, $p_"null" = 0.80$, $theta_"cell_pref" = 0.0°$. PD #sym.arrow.r.double
$d approx 89$ #sym.arrow.r.double $p_"rel" approx 0.05$; ND #sym.arrow.r.double $d approx 1$
#sym.arrow.r.double $p_"rel" approx 0.80$.

+ *Per-synapse arrival times* also shift with direction via `_bar_arrival_times`. Leftward vs
  rightward sweep across the dendritic field.

+ *Optional AR(2) cross-channel correlation* between paired ACh and GABA streams
  (`ar2_noise.py:L68-L107`): $phi = (0.9, -0.1)$; "correlated" condition uses $rho = 0.6$;
  "uncorrelated/AMB" condition uses $rho = 0.0$ and additionally scales the GABA NetCon weight by
  1.8×.

== Side-by-side comparison

#table(
  columns: (auto, auto, auto, auto),
  align: (right, left, left, left),
  [*\#*], [*Dimension*], [*Bed A*], [*Bed B*],
  [1], [Morphology source], [350-section Poleg-Polsky bundled cell], [Same template as `RGCmodelGD.hoc`],
  [2], [Section count], [1 soma + 350 dends], [1 soma + 350 dends],
  [3], [Dendrite tiers], [ON (282) vs OFF (68), HOC-side], [primary/non-terminal/terminal, Python],
  [4], [Synapse placement code], [HOC-side], [Python-side],
  [5], [Point processes per cell], [846 (3 per ON dend × 282)], [~354 (2 per terminal × ~177)],
  [6], [HH variant], [`HHst.mod` stochastic; NF=0 by default], [`HHst_noiseless.mod` deterministic],
  [7], [Active channels at default], [Na+Kdr+Km+leak; CaL/CaT zeroed], [Na+Kdr+Km+leak+CaL+CaT+cad],
  [8], [Excitation mechanism], [`bipNMDA` (AMPA + voltage-dep NMDA)], [`Exp2Syn` ACh],
  [9], [NMDA active in driver], [Yes (every BIPsyn)], [No (Exp2NMDA wired but latent)],
  [10], [Inhibition mechanism], [`SACinhib` POINT_PROCESS], [`Exp2Syn` GABA + Poisson queue],
  [11], [GABA reversal], [-60 mV], [-60 mV],
  [12], [Per-event GABA peak], [`gsingle = 0.5 nS`], [NetCon weight 0.003 µS],
  [13], [PD encoding], [`gabaMOD = 0.33`], [`direction = 0°` + sigmoidal $p_"rel" approx 0.05$],
  [14], [ND encoding], [`gabaMOD = 0.99` (~3× PD)], [`direction = 180°` + sigmoidal $p_"rel" approx 0.80$],
  [15], [Release-noise model], [Linaro-Storace-Giugliano stochastic HHst], [AR(2) Python-side Poisson],
  [16], [Temperature], [32 °C], [36.9 °C],
  [17], [Resting $V_"init"$], [-65 mV], [-60 mV],
  [18], [Passive cable $R_a$/$c_m$], [100 Ω·cm / 1 µF/cm²], [100 Ω·cm / 1 µF/cm²],
)

== Verification

- Markdown source `results/results_detailed.md` passes the project's flowmark formatter and
  contains every equation block from t0070 in LaTeX math syntax plus the 5 new synaptic-current
  blocks.
- Typst source `results/results_detailed.typ` compiles cleanly via `typst.compile(...)` from
  `code/render_pdf.py`; resulting `results/results_detailed.pdf` is non-empty (size > 50 KB).
- Python: `ruff check`, `ruff format`, `mypy` all pass on `code/`.
- The four schematic PNGs were copied verbatim from t0070 (`shutil.copyfile`); no regeneration.

== Limitations

- *No quantitative metrics*: documentation-only correction task. `results/metrics.json` is `{}`.
- *Schematic figures, not NEURON renderings*: the four PNGs are illustrative; they do not
  reproduce the `RGCmodel.hoc` 3D pt3d coordinates and they are not produced by a NEURON
  simulation.
- *Only project default driver settings are documented*: the writeup tabulates effective parameter
  values under the canonical overrides; variant runs that change `use_active`, `NF_HHst`,
  `Voff`, `RHO_CORRELATED`, etc., will see different effective values.
- *Exp2NMDA in Bed B is latent*: parameterised in `constants.py:L57-L61` but no driver places
  instances.
- *Approximate dendrite-tier counts in Bed B*: ~10 / ~163 / ~177 are heuristic counts derived
  from upstream `ei_balance.py`.

== Files Created

- `tasks/t0071_t0070_synaptic_eqs_pdf/code/paths.py`
- `tasks/t0071_t0070_synaptic_eqs_pdf/code/render_pdf.py`
- `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.md`
- `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.typ`
- `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_detailed.pdf`
- `tasks/t0071_t0070_synaptic_eqs_pdf/results/results_summary.md`
- `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/{bed_a,bed_b}_morphology.png`
- `tasks/t0071_t0070_synaptic_eqs_pdf/results/images/{bed_a,bed_b}_synaptic_diagram.png`

== Task Requirement Coverage

#table(
  columns: (auto, auto, 1fr),
  align: (left, left, left),
  [*ID*], [*Status*], [*Result*],
  [REQ-1], [Done], [5 synaptic-current blocks present (Bed A AMPA, NMDA, GABA, ACh; Bed B Exp2Syn ACh + GABA)],
  [REQ-2], [Done], [HH equation in LaTeX form $C_m frac(d V, d t) = - sum_i I_i - I_"syn" - I_"inj"$],
  [REQ-3], [Done], [Every equation block in math syntax; no fenced text equations remain],
  [REQ-4], [Done], [`results_detailed.pdf` exists, non-empty (>50 KB)],
  [REQ-5], [Done], [`typst` listed in `pyproject.toml:L48`],
  [REQ-6], [Done], [4 PNGs copied from t0070 verbatim],
  [REQ-7], [Done], [`results_summary.md` references the new PDF and equation additions],
  [REQ-8], [Done], [Every numeric parameter unchanged from t0070; cross-checked verbatim],
  [REQ-9], [Done], [`## Note` section at the top of `results_detailed.md` states the supersession],
  [REQ-10], [Done], [`code/render_pdf.py` reproducible, with size-floor check],
)
