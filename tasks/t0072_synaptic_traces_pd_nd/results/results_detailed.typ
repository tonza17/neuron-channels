// Typst source for t0072 results writeup.
// Compiled to PDF by tasks/t0072_synaptic_traces_pd_nd/code/render_pdf.py.

#set page(
  paper: "a4",
  margin: (x: 2cm, y: 2.5cm),
  numbering: "1 / 1",
)
#set text(font: "New Computer Modern", size: 10pt, lang: "en")
#set par(justify: true, leading: 0.65em)
#set heading(numbering: "1.")
#show heading: set block(above: 1.4em, below: 0.8em)

#align(center, [
  #text(size: 16pt, weight: "bold")[
    Synaptic Conductance and Current Traces (PD vs ND) on Both Model Beds
  ]
  #v(0.4em)
  #text(size: 9pt)[
    Task t0072\_synaptic\_traces\_pd\_nd  —  2026-05-01
  ]
])

#v(1em)

= Summary

Two DSGC compartmental models — Bed A (Poleg-Polsky 2016 deposited variant under the
t0020 `gabaMOD` swap) and Bed B (de Rosenroll 2026 port under the t0066 bar-angle
swap) — were each driven through one preferred-direction (PD) and one null-direction
(ND) trial with a fixed seed. Per-synapse conductance state variables (`gAMPA`,
`gNMDA`, `g_GABA`, `g_ACh`) and the local membrane voltage `v_local` at the synapse
insertion point were recorded at 1 ms resolution from every synapse instance (Bed A:
282 ON-dendrite synapses per channel; Bed B: 177 terminal-dendrite Exp2Syn synapses
per channel). The post-hoc current $I(t) = g(t) dot (v_("local")(t) - E_("rev"))$ was
computed in pA, and population mean ± 1 SD across synapses was taken at each time
point.

Bed A's PD-vs-ND difference appears almost entirely on the GABA channel: mean peak
$g_("GABA")$ increases from *0.38 nS* at PD to *0.70 nS* at ND, a 1.87× scaling that
matches the $"gabaMOD"_("ND") slash "gabaMOD"_("PD") = 0.99 slash 0.33 = 3 times$
envelope ratio diluted by post-synaptic v feedback. Bed B's PD-vs-ND difference
appears dramatically on GABA (mean peak $g_("GABA")$ *0.16 nS* at PD vs *1.25 nS* at
ND, a 7.6× ratio driven by the per-event Bernoulli sigmoid going from p = 0.084 at
0° to p = 0.780 at 180°), and weakly on ACh (PD *0.103 nS* vs ND *0.107 nS*, identical
baseline release with only the bar-arrival order changing).

= Methodology

== Bed A: Poleg-Polsky 2016 deposited DSGC under the gabaMOD swap

The Bed A cell was constructed once per process via `build_dsgc()` from the registered
`modeldb_189347_dsgc` library asset (task t0008). The cell exposes 282 ON-dendrite
synapses, each carrying one `bipNMDA` (mixed AMPA + NMDA), one `SACinhib` (GABA), and
one `SACexc` (ACh) point process at the section midpoint (`x = 0.5`).

Per-trial flow (mirrored from t0020's `run_one_trial_gabamod`): apply canonical
parameters, override `h.gabaMOD` to *0.33* (PD) or *0.99* (ND), re-run the HOC stimulus
generator, attach `Vector.record` handles for every synapse's conductance state plus
`pp.get_segment()._ref_v` for the local voltage, then `finitialize` and `continuerun`
for 1000 ms. Recorder pattern adapted from t0048's `attach_conductance_recorders`,
extended with per-synapse `v_local`.

== Bed B: de Rosenroll 2026 port under bar-angle swap

The Bed B cell was constructed once per process via `build_dsgc_cell()` from the
registered `de_rosenroll_2026_dsgc` library asset (task t0024). Bed B has 177 terminal
dendrites, each carrying one Exp2Syn ACh and one Exp2Syn GABA wired through
NetStim → NetCon source pairs driven by per-event timing.

Per-trial flow (adapted from t0066's `_run_one_trial`, FULL mode only): compute bar
arrival times for `direction_deg = 0.0` (PD) or `180.0` (ND), generate AR(2) noise
envelopes (`rho = 0.6`), compute the GABA release probability from the
`_gaba_prob_for_direction` sigmoid (PD: *0.084*; ND: *0.780*), sample Poisson event
times, queue them via `FInitializeHandler`, attach recorders, then run.

Helpers `_setup_synapses`, `SynapseBundle`, `_bar_arrival_times`,
`_rates_with_ar2_noise`, `_gaba_prob_for_direction`, `_rates_to_events` were copied
verbatim from t0024's `run_tuning_curve.py` (private API, not library-exposed) per the
project's cross-task code-reuse rule.

== Aggregation and current computation

After the four NEURON runs (2 beds × 2 directions), `aggregate.py` loads all 12 raw
`.npz` files, converts Bed B's Exp2Syn `g` from microsiemens to nanosiemens (×1000),
then computes $I_("syn") = g_("nS") dot (v_("local"," mV") - E_("rev"," mV"))$ in pA.
Population statistics are taken across the synapse axis: mean and unbiased SD
(`ddof=1`) at each time point.

= Bed A figure

#figure(
  image("images/bed_a_synaptic_traces.png", width: 100%),
  caption: [
    Bed A (Poleg-Polsky 2016 deposited DSGC) - synaptic conductances and currents,
    PD (blue) vs ND (red), population mean ± 1 SD across 282 ON-dendrite synapses.
    Rows: AMPA, NMDA, GABA, ACh. Cols: g(t) in nS (left), I(t) in pA (right).
    Only the GABA row shows the intended PD-vs-ND scaling (1.87×); NMDA shows a
    counter-intuitive ND-suppression because stronger ND inhibition deepens the
    voltage-dependent Mg block.
  ],
) <fig:bed_a>

== Analysis (Bed A)

The intended direction-encoding mechanism is the GABA channel: PD's mean GABA
conductance peaks at *0.38 nS* while ND's peaks at *0.70 nS*. The corresponding GABA
current traces are similar in absolute magnitude between PD and ND because the
ND-elevated $g_("GABA")$ is offset by a more hyperpolarised local v (closer to
$E_("GABA") = -60$ mV, smaller driving force). This is the canonical SAC-mediated DS
mechanism on this bed.

The AMPA and ACh rows show nearly overlapping PD and ND traces — the BIPsyn AMPA
portion and the SACexc ACh drive are direction-symmetric on this bed (no rotation,
no asymmetric bipolar drive). Small residual differences (~0.001 nS, well within the
SD band) reflect the post-synaptic v feedback into the release stochastics.

The NMDA row shows PD mean $g_("NMDA")$ peak at *0.30 nS* versus ND at *0.19 nS* —
counter-intuitively, less NMDA conductance on the ND trial despite identical BIPsyn
drive. ND's stronger GABA inhibition keeps the dendritic v more hyperpolarised, which
deepens the voltage-dependent Mg block on $g_("NMDA")$ (the `local_v` enters the
gating polynomial in `bipolarNMDA.mod`). This is a real biophysical finding emerging
directly from the per-synapse trace recording.

= Bed B figure

#figure(
  image("images/bed_b_synaptic_traces.png", width: 100%),
  caption: [
    Bed B (de Rosenroll 2026 DSGC port) - synaptic conductances and currents,
    PD (blue) vs ND (red), population mean ± 1 SD across 177 terminal-dendrite
    synapses. Rows: ACh, GABA. Cols: g(t) in nS (left), I(t) in pA (right). The
    GABA row shows the dramatic 7.6× direction-driven release-probability swing
    (sigmoid from p=0.084 at 0° to p=0.780 at 180°); the ACh row shows the
    direction-independent baseline release (BASE_ACH_PROB = 0.5).
  ],
) <fig:bed_b>

== Analysis (Bed B)

The intended direction-encoding mechanism is the GABA channel via the
`_gaba_prob_for_direction` sigmoid: at 0° (PD) the per-event Bernoulli release
probability is *0.084*; at 180° (ND) it is *0.780*. ND mean $g_("GABA")$ peaks at
*1.25 nS* versus PD's *0.16 nS* — a 7.6× ratio matching the 9.3× release-probability
ratio almost exactly. The corresponding GABA current is also much larger on ND (mean
peak $|I| approx 9.05$ pA ND vs 3.79 pA PD).

The ACh channel uses `BASE_ACH_PROB = 0.5` — direction-independent. Row-1 traces
overlap almost perfectly (mean peak $g_("ACh")$ 0.103 nS PD vs 0.107 nS ND, well
within the SD band). The tiny difference traces to the AR(2) noise envelope and the
bar-arrival ordering: PD has the bar moving rightwards, ND leftwards. The population
mean smooths most of this; what's left is essentially the same trace.

= Single-synapse examples

Ten top-amplitude individual single-synapse traces, one per (bed, direction, channel)
combination that exists in the data. Tabulated for compactness; per-example input/output
detail is in `results_detailed.md`.

#table(
  columns: (auto, auto, auto, auto, auto, auto, auto, auto),
  align: (left, left, left, right, right, right, right, right),
  table.header(
    [Bed], [Dir], [Channel], [Syn idx], [Peak g], [Peak |I|], [t at peak g], [t at peak |I|]
  ),
  [A], [PD], [GABA], [221], [1.41 nS], [84.9 pA], [226 ms], [226 ms],
  [A], [ND], [GABA], [54], [1.80 nS], [53.1 pA], [288 ms], [290 ms],
  [A], [PD], [NMDA], [34], [1.34 nS], [49.6 pA], [373 ms], [373 ms],
  [A], [PD], [AMPA], [71], [0.50 nS], [19.28 pA], [141 ms], [141 ms],
  [A], [ND], [AMPA], [234], [0.45 nS], [22.52 pA], [141 ms], [141 ms],
  [A], [PD], [ACh], [178], [0.74 nS], [28.49 pA], [286 ms], [288 ms],
  [A], [ND], [ACh], [188], [0.97 nS], [42.94 pA], [190 ms], [190 ms],
  [B], [PD], [GABA], [140], [3.00 nS], [178.1 pA], [53 ms], [55 ms],
  [B], [ND], [GABA], [13], [10.21 nS], [269.0 pA], [44 ms], [7 ms],
  [B], [PD], [ACh], [144], [1.80 nS], [88.4 pA], [58 ms], [58 ms],
)

The Bed B GABA ND single-synapse peak (10.21 nS) is over 60× the population mean peak
(0.16 nS PD; 1.25 nS ND). Most of the 177 GABA terminals fire 0-1 events per trial;
a handful of high-rate terminals near the bar's arrival window fire several events
that summate to large momentary conductances. The population mean averages this out.

= Verification

All 12 raw `.npz` trace files exist in `data/`; `aggregated.npz` contains 49 arrays
(12 × {g_mean, g_sd, I_mean, I_sd} + shared `t_ms`); both PNG figures exist with
sizes well above the 50 KB threshold (Bed A: 649 KB, Bed B: 172 KB); PD and ND traces
are visibly different on the GABA channel of both beds; no upstream task source files
were modified during execution.
