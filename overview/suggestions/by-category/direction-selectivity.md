# Suggestions: `direction-selectivity`

293 suggestion(s) in category
[`direction-selectivity`](../../../meta/categories/direction-selectivity/) **261 open** (61
high, 178 medium, 22 low), **32 closed**.

[Back to all suggestions](../README.md)

---

## High Priority

<details>
<summary>📊 <strong>16-direction polar re-evaluation of t0112's 7 unique joint-pass
cells (mirrors t0107 on t0106)</strong> (S-0112-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0107 re-evaluated 10 t0106 top cells at 8 directions and found that the 2-direction ratio DSI
overstates selectivity by ~0.42 absolute (mean 8-dir DSI 0.519 vs 2-dir 0.939). t0112's 7
unique joint-pass cells inherit this caveat unmodified and must be polar re-evaluated before
any cross-seed claim can be reported. Apply the same 8-direction (or extended 16-direction)
drifting-bar protocol used by t0107 to all 7 t0112 joint-pass cells, with N_EVAL_SEEDS matched
to t0107. Decision: if the 8-direction DSI rank-correlates with the 2-direction ratio DSI
(Spearman r > 0.7 across the t0106 + t0112 pool of 133 joint-pass cells), the 2-direction
metric is a usable proxy for substrate exploration; otherwise the 2-direction joint-pass
cohort must be treated as candidate-only until polar-confirmed. Distinct from S-0106-03
(covers 50 t0106 cells, not the 7 t0112 cells). Recommended task types: experiment-run,
comparative-analysis. Cost: <$1 (7 cells x 8 dirs x 3 trials on one Vast.ai instance).

</details>

<details>
<summary>🧪 <strong>Active dendritic conductances (Nav1.6 + Kv3) layered on the t0059
bar-locked GABA + AMPA-escape substrate</strong> (S-0059-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0059-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Source paper** | [`10.1523_JNEUROSCI.4495-13.2014`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/paper/10.1523_JNEUROSCI.4495-13.2014/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The t0059 negative result (max FULL peak Hz = 2.143, max vector-sum DSI = 0.209) most
plausibly stems from passive dendrites capping local depolarisation; Park2014 [p. 3977] and
PolegPolsky2016 [p. 1278] both implicitly assume active dendritic mechanisms. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, install Nav1.6 (g_Nabar in {0.05, 0.10, 0.20} S/cm^2)
and Kv3 (g_Kv3bar in {0.05, 0.10} S/cm^2) on dendritic sections, and run a focused 3x2x3
(gNa_dend x gKv3_dend x gAMPA in {1.0, 2.0, 4.0}) sweep at GABA_BASE_NS = 0.10 nS (the t0059
vector-sum DSI optimum). Pass criterion: at least one operating point with peak Hz >= 5 Hz AND
vector-sum DSI > 0.3. Distinct from S-0009-03 (calibrates densities against PolegPolsky2016
spike-shape and Ih-sag waveforms only) and S-0002-01 (somatic g_Na/g_K only). Directly
addresses RQ4 on the bar-locked substrate. Recommended task types: build-model,
experiment-run.

</details>

<details>
<summary>🧪 <strong>AIS-localised Kv7 follow-up (t0075 candidate)</strong>
(S-0074-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Kv7 was inert at all 3 somatic densities tested in t0074 (vector-sum DSI delta < 0.003 at
every density). Compare-literature confirmed this matches Hu 2007 / Shah 2008's prediction
that Kv7's canonical site is the AIS, not the soma. Build a virtual AIS section on Bed A (30
µm, between soma and virtual axon, with HHst at 5x somatic density), and re-run the 3-density
Kv7 sweep with insertion on the AIS rather than the soma. This was already proposed as the
t0075 candidate in earlier brainstorming (S-0067-03). Hypothesis: Kv7_AIS at 0.001-0.005
mS/cm² produces a measurable change in either HWHM or vector-sum DSI; M-current's slow
accumulation is well-suited to the AIS firing regime.

</details>

<details>
<summary>🧪 <strong>AMPA conductance escape sweep on t0057 tonic-GABA substrate to
enter multi-spike regime first</strong> (S-0057-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0057-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0057 confirmed (alongside t0052, t0053, t0054) that AMPA = 0.5 nS x 100 synapses gives at
most one spike per trial; this binary regime cannot produce graded DSI under any inhibition
mechanism. S-0052-01 proposes the AMPA escape on the t0052 scalar-gabaMOD substrate; this
suggestion proposes the matching experiment on the t0057 tonic substrate so the AMPA-escape
and tonic-GABA-amplitude axes are directly cross-comparable. Sweep AMPA per-synapse
conductance in {0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0} nS at fixed GABA_BASE_NS in {0.5, 1.0, 1.5}
nS (21 grid cells, 7560 trials). Report peak Hz, FULL-mode primary and vector-sum DSI, HWHM,
and reliability per cell. Pass criterion: locate at least one (gAMPA, gGABA) point on the
tonic substrate with peak Hz in 5-50 Hz AND vector-sum DSI > 0.3, or rule out such a point in
the sustained-envelope regime. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>AMPA per-synapse conductance sweep on t0052 minimal DSGC to close
the 30-150x peak-rate gap</strong> (S-0052-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0052 hits primary DSI 1.0 but peak rate is only 0.667 Hz, ~22x below the t0004 target (30 Hz)
and 30-150x below the in vivo / in vitro DSGC range (30-100 Hz, Park2014 / PolegPolsky2016).
The current AMPA conductance is 0.5 nS x 100 synapses (AMPA-only by design) and the cell is
locked in a single-spike-per-trial regime that makes DSI = 1.0 trivially. Sweep the
per-synapse AMPA peak conductance over {0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0} nS at fixed synapse
count and gabaMOD design, re-run the 12-direction x 10-trial FULL sweep, and report peak Hz,
vector-sum DSI, HWHM, and reliability per gAMPA. Goal: locate the gAMPA where peak rate enters
the 30-100 Hz band and the cell leaves the binary on/off regime, so DSI dynamics become
biologically informative. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Anchor-1-only warm-start NSGA-II to isolate which part of t0091's
warm-start was load-bearing</strong> (S-0099-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0099-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-10 |
| **Source task** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0099 confirmed t0091's 5-anchor warm-start was load-bearing (0/55 random-init joint-pass
cells vs t0091's 1/57). Open question: was anchor 1 (Bed-B-like) sufficient, or did the
diversity of all 5 anchors matter? Run NSGA-II with all 96 init cells cloned from anchor 1
only (96 different t0083 electrophys vectors), pop=96, 8 gens, $5 cap. Outcome (a): joint-pass
emerges -> anchor 1 was load-bearing alone. Outcome (b): no joint-pass -> warm-start diversity
itself was load-bearing. Either narrows future morphology-extended NSGA-II design
substantially. Cost ~$3.50 single seed.

</details>

<details>
<summary>🧪 <strong>Apply EPSP/IPSP/FULL protocol to from-scratch DSGC family
substrate (t0052-t0059)</strong> (S-0066-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0066-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0065 ran the protocol on deposited Poleg-Polsky; t0066 ran it on de Rosenroll. Both showed
flat IPSP_PASSIVE because of e_GABA = v_rest design. The from-scratch family (t0052-t0059) is
trapped in a binary regime (single-spike-trivial-DSI or full-suppression-zero-DSI). A direct
EPSP_PASSIVE / IPSP_PASSIVE / FULL decomposition on the from-scratch substrate would tell us
whether (a) the from-scratch family also has e_GABA = v_rest (if so, the binary regime is from
a different cause), or (b) the from-scratch family uses e_GABA != v_rest (in which case the
IPSP would be hyperpolarising and could explain the binary trap). The same protocol code is
portable: copy run_protocol.py, swap the cell builder import, adjust HH knob names. Cost: ~1
hour code + ~30 min sweep (the from-scratch family is faster — fewer trials needed because
lower noise variance). This is the natural successor to S-0065-01, now made more urgent by the
t0066 findings.

</details>

<details>
<summary>🧪 <strong>Apply EPSP/IPSP/FULL protocol to the from-scratch DSGC family
substrate</strong> (S-0065-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0065-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0065 isolated the deposited cell's EPSP and IPSP shapes and showed that direction selectivity
in that cell comes from differential shunting inhibition (e_SACinhib = v_rest = -60 mV, so
opening Cl- channels produces zero net Vm deflection). The from-scratch family (t0052-t0059)
is trapped in a binary regime: single-spike-per-trial trivial DSI = 1, or full suppression DSI
= 0. A direct EPSP_PASSIVE / IPSP_PASSIVE / FULL decomposition on the from-scratch substrate
(using t0057's library wiring: 100 E + 100 I synapses on t0009 morphology) would tell us
whether the binary-regime failure is excitatory under-drive, hyperpolarising rather than
shunting inhibition, or HH miscalibration. The same six-trial protocol from tasks/t0065_*/code
can be ported to the from-scratch cell builder with minimal changes. Expected output: six
traces showing whether the from-scratch IPSP is hyperpolarising (would localise the
binary-regime cause) or flat-at-reversal (would invalidate the shunting hypothesis).

</details>

<details>
<summary>🧪 <strong>Build a minimal DSGC compartmental model implementing the 6-point
specification</strong> (S-0015-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0015-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0015_literature_survey_cable_theory`](../../../overview/tasks/task_pages/t0015_literature_survey_cable_theory.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modelling`](../../../meta/categories/compartmental-modelling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The answer asset cable-theory-implications-for-dsgc-modelling produces a concrete 6-point
specification for DSGC modelling in NEURON (morphology, d_lambda, DS mechanism, passive
parameters, validation suite, spike-generator tuning). A follow-up experiment task should
implement a minimal working DSGC model in NEURON/NetPyNE following the specification, using a
publicly-available DSGC morphology (e.g. NeuroMorpho.org) and validate it with the four-part
test battery (shape-index, graded DS, inhibition block, contrast-response).

</details>

<details>
<summary>📚 <strong>Build a small reusable library for target-vs-simulated tuning
curve metrics</strong> (S-0004-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0004-03` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Factor the closed-form DSI, HWHM, tuning_curve_rmse, and tuning_curve_reliability computations
out of individual tasks into a shared library asset. Every later fitting task will need these
four functions; centralising them avoids divergent reimplementations and makes metric values
reproducible from parameters alone.

</details>

<details>
<summary>🧪 <strong>Causal NaP-knockout ablation per cluster representative</strong>
(S-0088-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0088-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0088 attributed PD-minus-ND fractional contributions correlationally (NMDA 0%, Nav1.6
0.3-12.6%, NaP 87.4-99.7% across the 4 cluster representatives). The attribution is
correlation-based; to causally confirm NaP as the dominant mechanism, set nap_dend_distal = 0
in each of the 4 representative cells (1604, 1634, 767, 1639) and re-measure DSI at the 16
directions used by t0088. Expected effect: DSI collapses to <0.2 in all 4 cells if NaP is
causally responsible; DSI partially preserved if NMDA + Nav1.6 + GABA also contribute. Compare
to baseline DSI_measured (cell 1604: 0.71; cell 1634: 0.20; cell 767: 0.60; cell 1639: 0.43).
Local-CPU only: 4 cells x 16 directions x ~60 s/sim = ~64 min wall-clock, $0 cost. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>📊 <strong>Change the t0033 optimiser objective to a vector-sum-DSI-weighted
blend instead of pure primary DSI</strong> (S-0030-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0029 and t0030 both pinned primary DSI at 1.000 and only vector-sum DSI retained weak
sensitivity (ranges 0.021 and 0.012 respectively). The t0033 joint morphology-channel
optimisation plan currently proposes primary DSI as the objective; under the t0022 schedule
the optimiser will see a flat landscape and cannot discover morphology-channel interactions.
Change the t0033 objective to a weighted blend (e.g., 0.5 * vector_sum_DSI + 0.3 *
peak_Hz_match + 0.2 * HWHM_match) OR switch to vector-sum DSI outright. Distinct from
S-0029-07 which proposes promoting peak-Hz and HWHM to co-primary outcomes - this proposal
keeps DSI as the headline objective but replaces its pinned primary form with its unpinned
vector-sum form. Update tasks/t0012 tuning_curve_loss to expose a loss_kind='vector_sum_dsi'
option. Recommended task types: write-library, answer-question.

</details>

<details>
<summary>📊 <strong>Channel-knockout DSI causal-attribution variant of the t0084
metric</strong> (S-0084-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0084-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0084's fractional-channel-contribution metric is correlative: it measures which channel's
PD-vs-ND integrated current differs most in absolute magnitude, but does not establish causal
contribution to DSI. Replace it with a counterfactual knockout metric: for each cell, run 4
conditions (full / NMDA-knockout / Nav1.6-knockout / NaP-knockout) across 8 directions and
compute `delta_DSI = DSI_full - DSI_knockout` per channel. The dominant mechanism is the
channel whose knockout collapses DSI the most. Apply to cells 767 / 637 / 762; if NaP-knockout
collapses DSI by the most, t0084's NaP-dominant correlative finding is causally confirmed;
otherwise the attribution shifts. ~96 runs on local CPU. Distinct from S-0084-01 which sweeps
NaP density continuously; S-0084-05 tests all three channels simultaneously with binary
on/off. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>📊 <strong>Correct fabricated content in Poleg-Polsky 2026 summary.md via
the corrections mechanism</strong> (S-0101-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0101-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-11 |
| **Source task** | [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md) |
| **Source paper** | [`10.1038_s41467-026-70288-4`](../../../tasks/t0101_brainstorm_results_21/assets/paper/10.1038_s41467-026-70288-4/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/summary.md has
claims absent from the paper: (a) wrong title (published 'supporting elementary motion
detection'); (b) wrong primitives ('NMDA multiplicative gating', 'velocity-dependent
coincidence detection', 'distance-graded delay lines'); (c) wrong search axes ('A-type
potassium density'); (d) wrong scope (paper covers retina + cortex L2/3). Actual 8 primitives:
H&R, anti-H&R, amplitude, temporal-alignment, B&L, anti-B&L, pause-in-inhibition,
directionally-tuned inhibition. Real DSI 2.4-73.1% from subthreshold voltage. Downstream task
writes corrections/paper_summary_10.1038_s41467-026-70288-4.json with PDF-verified content
(quotes in t0101 session_log). Cost $0.

</details>

<details>
<summary>🧪 <strong>Dang 2023 theory-grounded NSGA-II at pop>=290 (mu = n log n
floor) with N_EVAL_SEEDS=4, gens=10</strong> (S-0102-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | [`10.48550_arXiv.2306.04525`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2306.04525/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Dang 2023 Theorem 8 requires mu = Omega(n log n) for noisy NSGA-II to retain polynomial
expected runtime under Bernoulli or Gaussian noise. For our 68-d substrate, the theoretical
floor is Omega(68 * log(68)) = approximately 290; t0102 ran at pop=96, three times below this
floor. compare_literature.md Methodology Differences identifies this as a principled lever to
pull before concluding the substrate is structurally empty of joint-pass cells. Run a single
random-init NSGA-II at pop=320 (slightly above the Dang floor for headroom), gens=10,
N_EVAL_SEEDS=4, 1 GA seed -- total budget approximately 3200 evaluations, comparable to t0102.
If pop>=290 finds joint-pass cells where pop=96 found none, the population-floor argument is
empirically confirmed; if not, the substrate-limitation reading hardens. Recommended task
types: experiment-run, comparative-analysis. Cost: ~$5-7 on Vast.ai (single seed at higher pop
offsets the fewer generations).

</details>

<details>
<summary>📊 <strong>Direct re-evaluation of t0083 / t0091 anchor library at
N_EVAL_SEEDS=4 to disambiguate substrate vs algorithm limitation</strong>
(S-0102-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

creative_analysis.md Section 4 proposes a < $0.20 follow-up that disambiguates
'substrate-limited vs algorithm-limited' definitively. Take the 5 anchor families from t0091's
warm-start (alt_topology, symmetric, bedb_like, t0083 anchors 1559 and 1677) and re-evaluate
each at N_EVAL_SEEDS=4 with no NSGA-II/LHS/mutation -- just per-cell evaluation. Count how
many clear the strict joint-pass corner. Outcome A (zero clear): joint corner is empirically
unreachable on this substrate at N=4 regardless of algorithm; further NSGA-II is futile.
Outcome B (>= 1 clears): NSGA-II at random init is failing to find what is empirically
present; algorithm replacement (IBEA/CMAES) justified. Also re-evaluate t0091's joint-pass
cell (DSI=0.511, PD=35.1 Hz, rob=0.79) at N=4 to test the noise-floor prediction. Recommended
task types: baseline-evaluation, comparative-analysis. Cost: < $0.20 (~95 evaluations, no GA,
~30 min on Vast.ai).

</details>

<details>
<summary>🧪 <strong>Direct test of the t0076-vs-t0068 contradiction: isolate Nav1.6 +
Kv3 effect at the t0076 best-joint operating point</strong> (S-0076-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0076-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0068 reported that Nav1.6 + Kv3 co-expression jointly rescues DSI and rate, but the t0076
25-d Pareto front contains no cell with DSI>=0.6 AND rate>=40 Hz at any (Nav1.6, Kv3)
combination. The contradiction is either (a) substrate-specific (t0068 used Bed A; t0076 used
Bed B); (b) a t0068 local-minimum that wider search escaped; or (c) the other 23 t0076
parameters destructively interfere with the rescue. Resolve by fixing the t0076 iter-424
best-joint cell (DSI=0.42, rate=4.95 Hz) and sweeping ONLY (Nav1.6, Kv3) over the t0068 grid
(5x5 densities, both substrates). Compare: does the rescue appear on Bed B at this fixed
background? Does it disappear on Bed A when the other 23 t0076-style parameters are perturbed
away from t0068 defaults? Recommended task types: experiment-run.

</details>

<details>
<summary>📂 <strong>Download Bae et al. 2018 dense EM reconstructions for Baden
cluster IDs</strong> (S-0103-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0103-01` |
| **Kind** | dataset |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0103_extract_baden_2016_ds_morphologies`](../../../overview/tasks/task_pages/t0103_extract_baden_2016_ds_morphologies.md) |
| **Source paper** | [`10.1038_nature16468`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Baden 2016's Dryad release contains no dendritic morphology. Bae et al. 2018 (EyeWire/E2198
dense EM dataset) published reconstructed RGC morphologies and explicitly linked many of them
to Baden 2016 functional cluster IDs. Download Bae 2018 morphologies for the 8
paper-authoritative DS clusters {2, 6, 12, 13, 16, 25, 26, 29} and emit one dataset asset of
SWC/JSON morphologies keyed by Baden cluster ID. This is the most direct way to ground t0090's
morphology-generator parameter envelopes (field diameter, branch count, total length,
asymmetry) in real biological DS-cell shapes. Recommended task types: download-dataset,
download-paper.

</details>

<details>
<summary>📂 <strong>Download Ran et al. 2020 ON-OFF DS-cell morphologies as a
complementary morphology source</strong> (S-0103-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0103-02` |
| **Kind** | dataset |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0103_extract_baden_2016_ds_morphologies`](../../../overview/tasks/task_pages/t0103_extract_baden_2016_ds_morphologies.md) |
| **Source paper** | [`10.1038_nature16468`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Ran et al. 2020 (Nat Commun) provides dye-fill reconstructions of mouse ON-OFF DS RGCs with
co-recorded preferred-direction labels. The Baden 2016 Dryad release does not include
morphologies, and Ran 2020 covers exactly the ON-OFF DS subtypes (Baden clusters G12/G13) most
relevant to the t0024 ON-OFF DSGC modelling line. Download the published SWC files (or extract
from supplementary materials), register them as a dataset asset, and tag each morphology with
its preferred-direction angle and any Baden-cluster correspondence available. Useful as a
second, independent morphology source against Bae 2018 for the t0090 envelope grounding.
Recommended task types: download-dataset, download-paper.

</details>

<details>
<summary>🧪 <strong>Experimentally test NMDA-spike contribution to DSGC direction
selectivity via compartmental simulation</strong> (S-0016-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0016-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Source paper** | [`10.1038_35005094`](../../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_35005094/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The answer asset dendritic-computation-motifs-for-dsgc-direction-selectivity identifies NMDA
spikes as the highest-confidence transferable motif. Build a NEURON/NetPyNE compartmental DSGC
model with explicit NMDA synapses (dynamic Mg2+ block, NMDA:AMPA ratio swept from 0.5 to 2.0)
and test whether spatially-clustered co-directional bipolar-cell input produces supralinear
summation during preferred-direction motion and is suppressed by asymmetric inhibition during
null-direction motion. Compare the resulting DSI (direction selectivity index) against the
no-NMDA baseline to quantify the NMDA-spike contribution to DS.

</details>

<details>
<summary>🧪 <strong>F1-axis-seeded NSGA-II initial population to test whether
targeted seeding escapes the joint-corner block</strong> (S-0105-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

F1 is the only factor weakly correlated with both DSI (r = -0.322) and PD (r = -0.265). Its
top loadings span NAP_PRIMARY, SK_MID, MG_CONC_MM, RA_OHM_CM (and morph_seed - see S-0105-01
caveat). Build a random-init NSGA-II run whose initial population samples along the F1 axis
(positive and negative directions) and orthogonal to F1, instead of uniform sampling. If
F1-axis seeding accelerates Pareto exploration into the joint corner, the substrate has a
discoverable direction that random-init NSGA-II misses. If F1-axis seeding produces the same
L-shape, the substrate-limit reading is reinforced. Recommended task type: experiment-run.
Cost: ~$8-12 (one Vast.ai NSGA-II run at matched budget to t0104 seed 44). Complements
S-0102-03 / S-0104-04 IBEA suggestions.

</details>

<details>
<summary>🧪 <strong>Find the NaP density at which DSI crosses zero</strong>
(S-0067-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0067-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0067 showed NaP at 0.8 mS/cm² gives DSI = 0.117 (positive but low) and at 2.4 mS/cm² gives
DSI = -0.179 (inverted). The exact crossing density is between 0.8 and 2.4 mS/cm². Run a finer
5-point density sweep on NaP only (e.g., 0.8, 1.0, 1.3, 1.7, 2.4 mS/cm²) with 10 seeds each
(~25 min compute) to characterise the DSI-vs-NaP-density transition curve and identify the
threshold density at which directional inversion becomes statistically robust. This is the
most surprising finding from t0067 and warrants quantitative refinement.

</details>

<details>
<summary>🔧 <strong>Fix DSI vector-sum objective: gate by minimum total spike count
to eliminate silenced-cell DSI=1.0 artifact</strong> (S-0102-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-01` |
| **Kind** | technique |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Finding 1 in results_detailed.md: 27 t0102 cells reach DSI = 1.0 because vector-sum DSI in
evaluator.py divides by near-zero total spike count on silenced cells, with floating-point
dust producing a spurious 'perfect selectivity' score that pulls half the NSGA-II Pareto into
the silence corner. Single-line fix: return 0.0 when total_spike_count across 16 directions is
< 10. Bug affects the entire t0080-t0102 lineage; highest-leverage change for recovering
joint-pass cells at fixed algorithm and budget. Implementation: patch evaluator.py in a new
task that copies the t0099 substrate, add a silenced-cell unit test, re-run random-init
NSGA-II at pop=96, gens=8, 1 GA seed, N=4. Expected: joint-pass yield > 0 from random init;
DSI distribution loses its 1.0 spike. Recommended task types: write-library, experiment-run.
Cost: ~$2-3 (one pop=96 x 8-gen Vast.ai run).

</details>

<details>
<summary>🧪 <strong>GABA-reduction ladder on Mg-block t0055 architecture to find a
DSI-preserving operating point with peak Hz >= 5</strong> (S-0055-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0055 established that Mg-block NMDA recovers DSI to 0.7464 but the cell stays at 0.667 Hz
peak in FULL mode because the scalar gabaMOD inhibition (peak 2 nS, gaba_mod_PD = 0.33,
gaba_mod_ND = 0.99) clamps Vm below the Mg-unblock voltage. Sweep peak GABA conductance at
{2.0, 1.5, 1.0, 0.7, 0.5, 0.3} nS at gNMDA = 0.5 nS (mid-sweep) and trace DSI and peak Hz. The
S-0054-01 pass criterion (DSI > 0.50 AND peak Hz >= 5 Hz) should become reachable somewhere on
this ladder. This is a tighter, faster, and conceptually cleaner experiment than the full
S-0054-02 3D sweep, and it directly answers the t0055 finding. Pass criterion: at least one
GABA value yields DSI > 0.50 AND peak Hz >= 5 Hz. Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA-synapse-count sweep on t0052 to characterise driving-force
saturation of scalar gabaMOD IPSPs</strong> (S-0052-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0052_minimal_dsgc_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

The headline secondary finding of t0052 is that the somatic IPSP voltage ratio (1.54x)
substantially under-predicts the gabaMOD conductance ratio (3.0x) because driving force (V -
E_GABA) saturates as ~100 GABA synapses fire near-synchronously and local Vm approaches E_GABA
= -75 mV. Characterise this saturation curve by sweeping the number of GABA synapses N_I in
{10, 25, 50, 75, 100, 150, 200, 300} at fixed per-synapse peak (2 nS) and fixed gabaMOD(theta)
design, holding 100 AMPA synapses constant. Report somatic IPSP voltage ratio (gNULL_voltage /
gPD_voltage), peak / null PSP magnitudes, primary and vector-sum DSI, and peak Hz per N_I.
Goal: produce a quantitative voltage-vs-conductance saturation curve that future
scalar-gabaMOD models can use to translate nominal conductance ratios into expected somatic
suppression. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Ground t0090 morphology-generator parameter envelopes in the
Baden 2016 + Bae/Ran morphologies</strong> (S-0103-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0103-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0103_extract_baden_2016_ds_morphologies`](../../../overview/tasks/task_pages/t0103_extract_baden_2016_ds_morphologies.md) |
| **Source paper** | [`10.1038_nature16468`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0090's morphology generator currently samples field diameter, branch count, total length, and
asymmetry from hand-picked ranges around the t0024 canonical De Rosenroll cell. The t0103
Baden subset (RF diameter, DSI, OSI per cell across 1,238 DS cells) plus the morphologies that
the Bae 2018 / Ran 2020 follow-ups would deliver give us per-cluster biological envelopes for
each shape statistic. Run a re-calibration task that fits empirical per-cluster distributions
(mean +/- SD per Baden DS group) and replaces t0090's parametric ranges, then re-runs a small
NSGA-II validation to confirm the bio-grounded envelopes still admit the Pareto-front cells.
This is the original motivation for downloading Baden 2016 in the first place. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Harmonise PD/ND encoding across Bed A and Bed B so cross-bed
sweep results are directly comparable</strong> (S-0070-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0070-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0070 writeup shows Bed A (t0008) and Bed B (t0024) encode PD vs ND by fundamentally
different mechanisms. Bed A keeps bar geometry fixed and swaps a presynaptic envelope scalar
`gabaMOD = 0.33` (PD) / `0.99` (ND) applied uniformly to every SACinhib synapse. Bed B keeps
conductances fixed and rotates the bar direction (0 deg / 180 deg), simultaneously shifting
per-synapse arrival times AND changing a sigmoidal release probability `p_rel ~= 0.05` (PD) /
`0.80` (ND) plus AR(2) noise. Any cross-bed comparison (t0065 vs t0066, or future Bed B ports
of t0067/t0068/t0069) is therefore confounded. Pick one canonical encoding (recommended:
spatial bar rotation, biophysically grounded) and either (a) port it to Bed A by replacing the
gabaMOD scalar with per-synapse spatial gating (extending S-0050-01), or (b) define a shared
effective-inhibition-strength calibration curve. Recommended task types: experiment-run,
comparative-analysis.

</details>

<details>
<summary>🧪 <strong>HV-plateau auto-stop sensitivity: re-run t0112 seed 77 with
auto-stop disabled to gen 60 ceiling</strong> (S-0112-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0112's HV-plateau detector fired at gen 21 (well below the 60-gen ceiling), and t0106
produced most of its joint-pass cells in gens 21-39 - after t0112's auto-stop. The 7-cell
joint-pass count may be censored by an over-aggressive plateau detector when the local mode is
'deep but narrow'. Re-run t0112 seed 77 with HV-plateau termination disabled (operator-stop or
N_GEN=60 only); keep all other constants identical. Decision: if post-plateau gens (22-60) add
>=10 more unique joint-pass cells, the detector censors the long tail and should be
reparameterised (longer window, tighter threshold, or removed) for all long-horizon runs. If
post-plateau yield is <=3 cells, the early auto-stop is benign. Recommended task types:
experiment-run, comparative-analysis. Cost: ~$5.

</details>

<details>
<summary>🧪 <strong>IBEA replacement for NSGA-II at matched budget (pop=96, gens=15,
N=4, 2 GA seeds) on Bed B + morphology substrate</strong> (S-0102-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Mohacsi 2024 (Neuroptimus benchmark, PLOS Comp Bio) reports IBEA is 'clearly the best among
the multi-objective methods' on six neuron-fitting benchmarks including Hay 2011 L5PC,
outperforming all three NSGA-II implementations tested. t0102 only tested NSGA-II, leaving
algorithm choice as an unexamined factor in the 0/4800 random-init joint-pass yield. Port the
t0099 substrate to pymoo's IBEA (or DEAP/BluePyOpt IBEA wrapper) at matched budget (pop=96,
gens=15, N_EVAL_SEEDS=4, 2 GA seeds, $8 cap), apply the S-0102-01 DSI fix if available, and
compare front structure to t0099+t0102. Expected: IBEA's hypervolume-density selection avoids
placing half the front in the DSI=1/PD=0 corner that NSGA-II crowding distance keeps;
joint-pass yield improves even if the corner remains hard. Run after or alongside S-0102-02.
Recommended task types: experiment-run, comparative-analysis. Cost: ~$6-8 matched to t0102
envelope (IBEA's O(N^2) overhead manageable at pop=96).

</details>

<details>
<summary>🧪 <strong>IBEA replacement for NSGA-II at matched budget on Bed B +
morphology substrate (renews S-0102-03)</strong> (S-0104-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0104-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0104's 0/2,208 random-init joint-pass null with the DSI guard active strengthens the case for
S-0102-03 (IBEA replacement). NSGA-II crowding-distance selection produced an L-shaped front
in both t0102 (3-obj) and t0104 (2-obj) on the same substrate, suggesting the selection
operator itself prefers extreme-corner cells over interior trade-off cells. Mohacsi 2024
explicitly recommends IBEA as the strongest multi-objective optimiser on neuron-fitting
problems (six of six benchmarks beat NSGA-II). Port t0104's substrate to pymoo IBEA at matched
budget (pop = 96, gens = 12, N_EVAL_SEEDS = 4, 2 GA seeds, DSI guard active, n_obj = 2).
Expected outcome: IBEA's hypervolume-density selection produces an interior-weighted front;
even if it does not surface a joint-pass cell, it should populate the diagonal region between
the two corners more densely than NSGA-II did. Cost: ~$8-10 matched to t0104 envelope.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Implement AIS compartment, NMDARs, and simulated voltage-clamp
block in the downstream DSGC model build task</strong> (S-0017-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

The answer asset patch-clamp-techniques-and-constraints-for-dsgc-modelling produces a 7-point
specification for DSGC modelling in NEURON extending the cable-theory and
dendritic-computation specifications from t0015 and t0016. The downstream DSGC
compartmental-model build task must implement: (1) an explicit AIS compartment with Nav1.6 at
7x the somatic Na+ density, with AIS length as a tunable parameter; (2) NMDARs with standard
Mg2+ block kinetics on DSGC dendrites alongside AMPARs; (3) a simulated somatic voltage-clamp
block (SEClamp) so experimental and simulated voltage-clamp readouts can be compared on the
same footing; (4) depolarisation-block threshold and AMPA/NMDA charge ratio during preferred
and null motion as named fitting objectives. Validation must include DSI reduction under
simulated NMDAR block to match Sethuramanujam2017 and maintained activity under simulated
synaptic blockade to resolve the MargolisDetwiler2007 intrinsic-vs-synaptic question for the
target DSGC subtype.

</details>

<details>
<summary>🧪 <strong>Implement AMPA + NMDA + GABA_A synapses with E-I temporal
co-tuning and SAC-to-DSGC asymmetric inhibition in downstream DSGC
model</strong> (S-0018-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The answer asset synaptic-integration-priors-for-dsgc-modelling produces a 6-point
specification for DSGC synaptic integration in NEURON extending the space-clamp/AIS/NMDAR
constraints from t0017. The downstream DSGC compartmental-model build task must implement: (1)
AMPA with dual-exponential kinetics (tau_rise 0.2-0.4 ms, tau_decay 1-3 ms) and NMDA with
Mg2+-block + tau_decay 100-200 ms at 32 degC on glutamatergic inputs, (2) GABA_A with shunting
(reversal near resting Vm) and tau_decay 5-20 ms on SAC inputs, (3) E->I temporal lag of 15-50
ms on preferred-direction stimuli reproducing Wehr & Zador 2003 co-tuning, (4) asymmetric
GABAergic inputs that are strong on null-side dendrites (to match Euler-Detwiler-Denk 2002 SAC
Ca2+ DS index 0.3-0.5) and weak on preferred-side dendrites, (5) dendritic-location-dependent
EPSP attenuation consistent with Hausser-Mel lambda_DC 100-300 um, (6) named fitting
objectives for DSI under shunting-inhibition block (should drop toward 0) and EPSP/IPSP charge
balance during null-direction motion.

</details>

<details>
<summary>🧪 <strong>Inspect the seed-55 gen-11 DSI=0.54 cell's 68-d parameter vector
— what makes it work; what would push PD up?</strong> (S-0104-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0104-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Seed 55 generation 11 produced the first cell in the t0080-t0104 NSGA-II lineage with DSI
cleanly above 0.5 (DSI = 0.5417 at PD = 3.57 Hz). Read this cell's 68-d parameter vector from
assets/predictions/nsga2-seed55-bedb-morph-n4-gen20-2obj/files/predictions-seed55.jsonl
(cell_id = 6 on the Pareto front). Compare the electrophys 54-d subvector and the 14-d
morphology subvector against the seed-44 best cell (DSI = 0.4073) and against t0091's reported
joint-pass anchor at DSI = 0.511 / PD = 35.1 Hz. Identify what biophysical knobs concentrate
near the high-DSI region of parameter space; perform a one-knob-at-a-time perturbation around
this cell to see whether a single sodium- or potassium-conductance bump can raise PD without
collapsing DSI. Recommended task types: data-analysis, experiment-run. Cost: ~$0.50 (no
NSGA-II, just ~120 evaluations of one-knob perturbations on a single Vast.ai instance for 1-2
hours).

</details>

<details>
<summary>🧪 <strong>Inspect the seed-55 gen-8 DSI=0.42 / PD=15 Hz cell's 68-d
parameter vector — the closest project-best joint trade-off</strong>
(S-0104-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0104-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Seed 55 generation 8 produced the project-best joint trade-off so far: DSI = 0.4192 at PD =
15.00 Hz. This sits ~15 Hz below the strict joint-pass threshold of 30 Hz and ~0.08 DSI below
the 0.5 threshold, but is the closest combined-axis cell observed across the full t0080-t0104
NSGA-II lineage. Read its 68-d vector from the seed-55 predictions JSONL (cell_id = 3 on the
Pareto front), classify its anchor neighbourhood, and run a 2-knob perturbation grid varying
the top-2 Cohen's-d-distinguished electrophys knobs from the t0102 silence-vs-firing
comparison. Outcome: a 2-d grid that estimates the local PD ceiling around this cell's DSI =
0.4192 plateau. Recommended task types: experiment-run, data-analysis. Cost: ~$1.00 (100-200
evaluations on Vast.ai, 2-3 hours).

</details>

<details>
<summary>🧪 <strong>Integrate tuning_curve_loss into the t0008 Poleg-Polsky DSGC
reproduction to score the ported ModelDB 189347 curve</strong> (S-0012-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0008 (port ModelDB 189347) is the first downstream consumer that will produce a real
simulated 12-angle tuning curve. Wire tuning_curve_loss.score into t0008's verification step
so the Poleg-Polsky reproduction's simulated curve is scored against the t0004 target and the
resulting ScoreReport.to_metrics_dict() is written straight into t0008/results/metrics.json
under the four registered keys (direction_selectivity_index, tuning_curve_hwhm_deg,
tuning_curve_reliability, tuning_curve_rmse). Deliverable: a short task that runs t0008's
simulated curve through score(), records ScoreReport.loss_scalar and passes_envelope, and
produces a side-by-side overlay plot (simulated vs target). This is the first end-to-end
validation that the scorer library does what it promises on a non-trivial candidate.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Isolate the pool-restart-cadence effect: paired re-runs at fixed
seed comparing cadence 10 vs 25</strong> (S-0112-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0112's 3.5x per-generation wall-clock speedup (620s/gen vs t0106's 2,167s/gen) is confounded
with the seed-44 -> seed-77 change. Run two paired comparisons at matched seed but different
pool_restart_every: (a) seed 44 with cadence=10 vs t0106's existing seed-44/cadence-25
baseline; (b) seed 77 with cadence=25 vs t0112's existing seed-77/cadence-10 baseline.
Decision rule: if the cadence-10 variant matches its cadence-25 baseline on Pareto front
geometry (best DSI, best PD, joint-pass count within seed noise) AND retains the 3-4x speedup,
then cadence=10 should become the project default for all downstream NSGA-II tasks. If the
cadence change shifts joint-pass yield, the speedup is algorithmically meaningful and the
trade-off must be characterised before adoption. Recommended task types: experiment-run,
comparative-analysis. Cost: ~$8 (one new cadence-10 seed-44 run at ~$2 plus one new cadence-25
seed-77 run at ~$5-6).

</details>

<details>
<summary>🧪 <strong>Joint (gAMPA, gNMDA, gGABA) conductance sweep on t0054 minimal
architecture to locate a DSI-preserving operating point</strong>
(S-0054-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0054 fixed AMPA at 0.5 nS and used the unchanged t0052 scalar gabaMOD (2 nS base, ratio 3.0),
varying only gNMDA. The DSI collapse may be recoverable by rebalancing the three conductances
jointly. Run a 3-D grid: gAMPA in {0.25, 0.5, 1.0} nS, gNMDA in {0.0, 0.1, 0.25, 0.5} nS, base
gGABA in {2, 4, 8, 16} nS, all on the t0054 codebase with placement seed 0 unchanged,
voltage-independent NMDA kept (so this is the no-Mg-block control complementary to S-0054-01).
Use 12 dirs x 5 trials per cell = 60 trials per (gAMPA, gNMDA, gGABA) point; 48 grid cells =
2880 trials. Apply early stop on cells where E_ONLY peak Hz > 30 Hz to prune the saturated
subgrid. Pass criterion: locate at least one (gAMPA, gNMDA, gGABA) triple with vector-sum DSI
>= 0.5 and peak Hz in 10-50 Hz, or rule out such an operating point in the voltage-independent
regime. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Match the from-scratch GABA reversal to resting potential and
re-test direction selectivity</strong> (S-0065-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0065-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The deposited cell places e_SACinhib = -60 mV which equals the cell's leak-driven quiescent
potential, making inhibition purely shunting. If the from-scratch family uses an e_GABA below
resting potential (e.g., -75 mV which is biologically plausible for Cl- with low [Cl-]_i),
inhibition becomes hyperpolarising and can collapse the DSI to 0 by pulling the cell off
threshold across all directions. Conversely, if e_GABA > v_rest, inhibition can depolarise
toward threshold and generate spurious spikes. Setting e_GABA = v_rest in the from-scratch
substrate is a single-line change (modify the gaba_tonic.mod e parameter or the synapse
mechanism's reversal). This directly tests whether the deposited cell's success is
structurally dependent on its e_GABA = v_rest design choice. Expected output: from-scratch
family with e_GABA = v_rest produces a graded tuning curve with 5-15 Hz peak in PD and DSI in
[0.5, 0.85], matching the deposited cell's behaviour.

</details>

<details>
<summary>🧪 <strong>Mg-block NMDA + bar-locked tonic GABA + AMPA-escape combination
sweep on the t0059 substrate</strong> (S-0059-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0059-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

S-0057-06 covers Mg-block NMDA + tonic GABA but uses t0057's global (100, 1400) ms tonic
window and fixed gAMPA = 0.5 nS. t0059 demonstrates the bar-locked window mechanism delivers
an 8.5 ms direction-dependent IPSP centre-of-mass shift (REQ-13 PASS) the global window
cannot. Layering Mg-block NMDA on the bar-locked substrate combines all three plausible
gap-closers identified in compare-literature: voltage-dependent NMDA gain (PolegPolsky2016),
per-synapse bar-arrival timing (deRosenroll2026), and AMPA escape. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, install the Jahr-Stevens NMDA_MgBlock mechanism from
t0055 at each E synapse, sweep gNMDA in {0.0, 0.25, 0.5, 1.0} nS x gAMPA in {1.0, 2.0, 4.0} nS
at GABA_BASE_NS = 0.10 nS (12 cells, 4320 trials at 10 trials x 12 directions x 3 modes). Pass
criterion: vector-sum DSI > 0.3 AND peak Hz >= 5 Hz. Distinct from S-0057-06 (global tonic
window, gAMPA=0.5 fixed). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>Multi-replicate confirmation of the t0081 joint-pass result with
3-5 independent LHS + warm-start RNG seeds</strong> (S-0081-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0081's joint-pass cell 767 (DSI 0.494 / PD 11.39 Hz) is a single-replicate observation from
one NSGA-II chain with one Sobol/LHS seed (seed 43 for fresh LHS) and one warm-start RNG seed
(42 for the t0078 49-d to 54-d projection). Re-run the same pop=96 / gen=8 NSGA-II
configuration on the v3 substrate with 3-5 different seed pairs (e.g., (44,45), (46,47),
(48,49)) and report joint-pass rate, HV trajectory variance, and Pareto-front overlap across
replicates. Reuse the t0081 harness verbatim. Cost ~$5-10 across 3-5 replicates at $2.39 each.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Multi-seed confirmation of t0106 2-direction NSGA-II at GA seeds
55 and 66</strong> (S-0106-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0106's 3.3% joint-pass yield (123 joint-pass cells / 3,744 evals) was produced from a single
random GA seed. No published NSGA-II benchmark (Hay2011, Druckmann2007, Mohacsi2024) accepts a
single-seed acceptance-rate point estimate. Re-run the exact t0106 configuration (2 antipodal
directions, ratio DSI, N_EVAL_SEEDS = 3, pop = 96, n_gen = 40, operator-stop, silence guard)
at GA seeds 55 and 66. Decision rule: if both seeds discover joint-pass cells (DSI >= 0.5 AND
PD >= 30 Hz) within 40 gens, the 2-direction substrate is genuinely populated and the
t0080-t0104 null was an objective-surface artefact, not a per-seed lucky draw. If either seed
returns zero, weaken the headline. Recommended task types: experiment-run,
comparative-analysis. Cost: ~$20 (two single-seed runs at $10 each).

</details>

<details>
<summary>🧪 <strong>Multi-seed substrate-rate confirmation at restart cadence 10:
N>=3 new GA seeds on the t0106 substrate</strong> (S-0112-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0106 (seed 44) yielded 123 unique joint-pass cells (3.3% rate); t0112 (seed 77) yielded only
7 (0.35%) on the same substrate. With two seeds spanning a factor of ~17 in joint-pass
density, the substrate-level acceptance rate is currently a 2-point sample and unreportable.
Run N>=3 additional GA seeds (suggested 33, 88, 99) on the identical t0106 substrate using
t0112's tighter pool_restart_every=10 and N_GEN=60 with HV-plateau auto-stop. Combined with
t0106 (44) and t0112 (77), this yields a 5-seed sample suitable for reporting a
substrate-level mean +/- s.e. acceptance rate against Hay2011's 0.40% and Druckmann2007's
0.10%. Distinct from S-0106-01 (which uses t0106's exact cadence=25 at only 2 new seeds and is
not actionable for a cadence-10 rate). Recommended task types: experiment-run,
comparative-analysis. Cost: ~$6 (3 seeds x ~$2 each at t0112 wall-clock).

</details>

<details>
<summary>📊 <strong>N_EVAL_SEEDS = 20 robustness re-evaluation of top 10 t0106 cells
(esp. the 3 DSI = 1.0 cells)</strong> (S-0106-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | [`10.1523_JNEUROSCI.0808-13.2013`](../../../tasks/t0106_long_pdnd_nsga2_300gen/assets/paper/10.1523_JNEUROSCI.0808-13.2013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Three t0106 top-50 cells (ranks 16, 19, 27) achieve ratio DSI = 1.0 with deterministic zero ND
firing. Total-spike silence guard (>= 10 spikes across PD + ND) is exceeded (47-154
spikes/trial) so they are not silence-guard artefacts, but Trenholm2013 reports peak ND ~ 27
+/- 12 Hz in real mouse Hb9 DSGCs and Oesch2005 reports OFF DSI = 0.74 +/- 0.13. ND = 0 across
only 3 noise replicates may be an AR(2)-seed + deterministic-GABA loophole that fails at
higher replication. Re-evaluate the top 10 cells (3 DSI = 1.0 + 7 next-best incl. DSI = 0.98
at PD = 84.5 Hz and PD-frontier DSI = 0.92 at PD = 122.6 Hz) at N_EVAL_SEEDS = 20. Decision:
if DSI = 1.0 collapses to <= 0.9, mark as noise-undersampling artefacts; if DSI > 0.95 holds,
escalate. Recommended task types: experiment-run, data-analysis. Cost: ~$1 (10 cells x 20
seeds, ~10 min on one Vast.ai instance).

</details>

<details>
<summary>📊 <strong>Per-cell field_elongation_pd vs DSI test on t0091 + t0099 Pareto
cells (HM-3 follow-up)</strong> (S-0099-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0099-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-10 |
| **Source task** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

HM-3 (cells with stronger DS have higher field_elongation_pd) remained inconclusive in both
t0091 and t0099. Pure data-analysis on the now-available 57+19+22+14 = 112 Pareto cells:
extract per-cell field_elongation_pd from each cell's 14-d morphology vector, plot vs DSI
vector-sum, compute Spearman rho. n=112 gives statistical power. Cost $0. Could resolve a
2-task-old open question.

</details>

<details>
<summary>📊 <strong>Per-cell field_elongation_pd vs DSI test on the 57-cell t0091
Pareto to resolve HM-3 inconclusive</strong> (S-0091-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | [`10.1371_journal.pbio.0050185`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1371_journal.pbio.0050185/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0091 reported a Spearman rho=-0.07 between total dendritic length and DSI vector-sum across
the 57-cell Pareto, leaving HM-3 (length-vs-DSI scaling, Hausselt2007) inconclusive because
total length conflates field_elongation_pd with branch_density_gradient_pd and
num_primary_branches. Pure data-analysis task on existing pareto_front.json: extract
field_elongation_pd from each Pareto cell's 14-d morph_params vector, compute Spearman +
Kendall correlations against DSI, PD-rate, robustness, and the 9 channel-side priors, plot
per-anchor scatter overlays, and stratify by anchor lineage. Goal: definitively confirm or
refute that elongation along PD is the morphology axis driving DSI in joint optimisation,
separate from branch density. Cost: $0 (local CPU analysis on existing JSONL files).
Recommended task types: data-analysis.

</details>

<details>
<summary>📊 <strong>Per-direction DSI re-scoring of the t0091 57-cell Pareto to
surface DSGC subtype-specific tuning</strong> (S-0091-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0091 used vector-sum DSI across 16 directions, which is direction-blind: a cell tuned to PD
with peak at 0 deg and a cell tuned to a non-cardinal direction (e.g., 45 deg) collapse to the
same vector-sum DSI. The PD vs ND anchor-asymmetry test (12 vs 9, p=0.331) may be
artifactually washed out by this collapse. Brendly2025 and Riccitelli2025 (now in the t0091
corpus from research-internet) report DSGC subtypes with distinct preferred directions. Pure
data-analysis on existing pareto_front.json + per-direction firing rate JSONL: re-score each
Pareto cell with per-direction DSI (peak direction, half-width-at-half-maximum, peak-to-trough
ratio); recompute the PD-asymmetric vs ND-asymmetric anchor test using direction-binned DSI;
compare per-direction tuning curve shapes between bedb_like, alt_topology, and the 21
asymmetric anchor cells. Cost: $0 (local CPU). Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Per-direction Vm-trace deep-dive of cell 1304 to identify the
headline cell's biophysical mechanism</strong> (S-0083-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0083-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Cell 1304 (gen 13, DSI 0.7652 / PD 13.96 Hz) is the project's first cell statistically
indistinguishable from RivlinEtzion 2012's published mouse ON-OFF DSGC stable-cell
distribution (DSI z=-0.08, PD z=+0.42). Its biophysical mechanism has not been attributed to
specific dendritic-spike machinery (NMDA Mg-block vs distal Nav1.6 vs NaP_dend). t0084 found
NaP_dend dominant for cell 767 (now dominated and off-Pareto); cell 1304's parameter vector
differs structurally from cell 767's (cf. [0.006, 0.001, 0.999, 0.995, 0.876, 0.992] vs
[0.008, 0.018, 1.000, 1.000, 0.250, 0.000]). Re-run cell 1304 in subprocess with per-direction
Vm recording at soma + 4 dendritic locations + AIS, then run conductance-knockout ablations
(zero out g_NaP_dend / g_NMDA / g_Nav_dend_distal) to identify the dominant DSI driver.
Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Plot polar tuning curves to distinguish SK_high narrowing from
flat-top clipping</strong> (S-0074-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

SK_high produced HWHM = 41 deg (delta -42 deg, the largest narrowing in the sweep).
Creative-thinking flagged that this could be a flat-top clipping artefact rather than true
narrowing: if SK acts as a firing-rate ceiling, the curve becomes flat-topped near the peak
and HWHM becomes ill-defined. Resolution requires a per-condition polar curve plot for SK_high
(and as a control, SK_med, SK_low, baseline). Cost: ~30 min coding using the existing t0011
plot_polar_tuning_curve. If polar plot shows flat-top with sharp shoulders, the narrowing is a
clipping artefact; if it shows a true narrow bell, the effect is real and SK_high is
biologically interesting. This is purely an analysis task on the existing per_trial_full.csv —
no new sim runs.

</details>

<details>
<summary>🧪 <strong>Re-run t0055 Mg-block sweep on the corrected
EPSP_PASSIVE/IPSP_PASSIVE protocol to validate the headline DSI
recovery</strong> (S-0055-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

After S-0055-01 lands, re-run the gNMDA={0,0.25,0.5,1.0} nS sweep on the Mg-block architecture
using the corrected trial-mode trio so EPSP and IPSP traces become spike-free synaptic
envelopes. Verify that vector-sum DSI = 0.7464 (FULL) is preserved across all gNMDA
(regression), record clean EPSP envelopes for the EPSP-decay metric, and report the EPSP
envelope's true peak (no spike contamination) per direction. Pass criterion: FULL DSI
bit-identical to t0055; EPSP_PASSIVE peak Vm < spike threshold (~-50 mV) at every direction
and gNMDA. Recommended task type: experiment-run. Bridges the protocol fix into the Mg-block
lineage and produces re-publishable EPSP/IPSP figures.

</details>

<details>
<summary>🧪 <strong>Re-run varimax factor analysis excluding integer morph_seed to
test whether F1's correlates survive</strong> (S-0105-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

morph_seed (an integer dimension bounded [0, 99] driving generator randomness, not
biologically meaningful) loads +0.68 on F1 next to NAP_PRIMARY (+0.75), SK_MID (+0.66),
MG_CONC_MM (+0.65), and RA_OHM_CM (+0.65). F1's r_DSI = -0.322 / r_PD = -0.265 could partly be
a 'warm-start vs random-init' indicator disguised as a mechanistic factor because t0091 fixed
morph_seed = 31 while t0099/t0102/t0104 randomise it. Re-run the t0105 factor analysis on a
67-d matrix excluding morph_seed and check whether F1's top loadings (NAP_PRIMARY, SK_MID,
MG_CONC_MM, Ra) and its Pearson r vs DSI / PD survive. If they do, F1 is mechanistic; if F1
dissolves, F1 was a lineage indicator. Recommended task type: data-analysis. Cost: $0 (pure
local re-analysis of existing data). Effort: 1-2 hours.

</details>

<details>
<summary>📂 <strong>Record per-trial soma spike times from modeldb_189347_dsgc to
exercise plot_angle_raster_psth on real data</strong> (S-0011-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The tuning_curve_viz raster+PSTH plot is currently exercised only by a deterministic synthetic
Poisson fixture (seed 42) because neither t0004 nor t0008 emits spike times. Extend the t0008
Poleg-Polsky NEURON driver to record soma membrane voltage, threshold-detect action
potentials, and write a spike-time CSV with columns (angle_deg, trial_seed, spike_time_s)
alongside the existing tuning-curve CSV. Target: 12 angles x 8 trials of spike times for the
baseline ModelDB 189347 port. Once available, re-point tuning_curve_viz.test_smoke.raster_psth
to the real CSV and add the resulting PNGs to assets/library/tuning_curve_viz/files/ via a
correction, replacing the synthetic fixture outputs. Recommended task types:
feature-engineering, code-reproduction.

</details>

<details>
<summary>🧪 <strong>Run G.3 NaP-knockout sweep at scale on local 64-core EPYC with
ProcessPoolExecutor</strong> (S-0090-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0090 Phase G.3 committed the NaP-knockout driver as infrastructure_only because the
single-process wall-clock projection (~42 min/cell x 4 cluster representatives = ~3 hours)
plus NEURON DLL state-management on Windows blew the implementation budget. After S-0090-01
retunes BEDB_BASE_POINT so the procedural cell fires under t0083 params, run the deferred 4
cells x 16 directions sweep across the 64-core EPYC using ProcessPoolExecutor with one NEURON
sub-process per worker to bypass the DLL-cleanup serialisation cost. Pass criterion (per t0090
plan): DSI collapses to <0.2 in all 4 cluster representatives if NaP is causally responsible
for PD-vs-ND attribution; otherwise the NMDA / Nav1.6 / GABA mix matters more than t0088's
correlational analysis suggested. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Substrate regression check on the t0076 iter-424 vector mapped
to the v3 54-d parameter space</strong> (S-0080-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

REQ-9 / REQ-16 of the t0080 plan deferred the substrate-regression check under cost pressure.
Without it, the t0080 negative result cannot conclusively distinguish 'v3 substrate is
regressed' from 'NSGA-II under-budgeted in 54-d' as the dominant cause of the dramatic Pareto
compression (94% DSI regression vs t0076 at the comparable PD regime). Map t0076's iter-424
25-d vector to the v3 54-d parameterisation with new dendritic-spike parameters at zero (no
dendritic NMDA, no distal Nav1.6/NaP) and run a single 8-direction x 20-seed evaluation
locally. Pass: reproduce DSI within +/- 0.05 of t0076's 0.42 at PD ~ 8.34 Hz. Cheap (~$0.05,
~5 min wall-clock); must precede any further v3 architectural extension. Recommended task
types: experiment-run, baseline-evaluation.

</details>

<details>
<summary>🧪 <strong>Synapse-count scaling sweep on t0059 substrate (100 -> 200 -> 300
E + I) to break the single-spike regime</strong> (S-0059-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0059-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0059 uses 100 E + 100 I synapses; PolegPolsky2016 [p. 1280] uses ~177, t0046 reproduction
uses 282, deRosenroll2026 [p. 5] uses >1000 SAC varicosities. The compare-literature
Synapse-count comparison identifies this >2.8x to >10x mismatch as a structural drive
bottleneck consistent with the 2.143 Hz peak ceiling. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, parameterise N_AMPA = N_GABA in {100, 200, 300}
(re-running the placement_seed0 generator to produce three larger placement bundles), and
sweep at gAMPA in {1.0, 2.0} nS, GABA_BASE_NS = 0.10 nS, holding bar-locked windows fixed (3 N
x 2 gAMPA = 6 cells, 2160 trials). Pass criterion: at least one (N, gAMPA) point with peak Hz
>= 5 Hz. This is the smallest single-axis test of the structural-drive hypothesis on the
validated bar-locked substrate. Distinct from S-0052-02 (GABA-count sweep on scalar gabaMOD
t0052, no bar-lock). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>Targeted Ca-K channel ablation sweep on top-PC1 asymmetric cells
to validate the SK/BK mechanistic hypothesis</strong> (S-0105-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | [`10.1038_s41467-026-70288-4`](../../../tasks/t0105_cluster_factor_analysis_dsi_pd/assets/paper/10.1038_s41467-026-70288-4/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

PC1 separates symmetric from asymmetric cells at p = 1.48e-10 with top loadings SK_TERMINAL,
BK_TERMINAL, SK_SOMA, BK_MID, NAP_PRIMARY. The mechanistic hypothesis is that asymmetric
dendrites concentrate Ca influx along the PD axis, so high terminal SK/BK locally quenches
PD-side over-excitation. Test by taking the top-3 PC1-positive asymmetric cells (high Ca-K
regime, e.g. the t0102 / t0104 cells in the cohort), independently ablating SK_TERMINAL = 0,
BK_TERMINAL = 0, SK_SOMA = 0, BK_MID = 0 (one at a time and combined), and re-evaluating DSI +
PD on the de Rosenroll Bed B substrate. Outcome: a 4x4 ablation grid per cell showing which
Ca-K conductance is load-bearing for the asymmetric direction-selectivity regime. Recommended
task types: experiment-run, data-analysis. Cost: ~$2-3 (small Vast.ai instance for 3-6 hours;
or local if NEURON runs locally). Aligns with PolegPolsky2026's ML channel-importance finding.

</details>

<details>
<summary>🧪 <strong>Tier-stratify channel densities in a follow-up Bed B MOBO (per
soma / proximal / distal / terminal)</strong> (S-0076-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0076-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

REQ-10 follow-up. The t0076 25-d search applied each of 12 channel densities uniformly across
soma + 350 dendrites. Real RGCs have ~50x higher Nav at AIS than soma (Kole 2008) and graded
Ih/Kv distributions per dendritic tier. Re-run the BoTorch MOBO with channels stratified into
4 region tiers (soma, proximal-dendrite, mid-dendrite, terminal), expanding the input to
~40-50 d. Seed the new GP with the 12-cell t0076 Pareto front (uniform-density solutions).
Test whether tier-stratification breaks the inherent DSI-vs-rate trade-off observed in the
25-d search. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Tighten NSGA-II priors on gnmda_dend to match Sivyer 2013
per-synapse value, then re-run</strong> (S-0086-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0086-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Source paper** | [`sivyer_2013`](../../../tasks/t0086_robustness_cluster_bio_comparison/assets/paper/sivyer_2013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0086's biological scorecard found that both Genuine-cell clusters have NMDA per-synapse
conductance 85-122 sigma above Sivyer 2013's published 0.1 nS. The NSGA-II search routinely
pushes gnmda_dend to the upper boundary of its log-uniform [1e-5, 1e-2] uS range. Tighten the
parameter bounds to [1e-5, 5e-4] uS (5x Sivyer 2013's value as a soft cap) and re-run NSGA-II
from t0083's gen-17 final population for 5 additional generations at population 96. Test
whether any joint-pass cells emerge in the biologically-plausible NMDA regime. If not, this
confirms that the v3 substrate cannot satisfy the joint-pass DSI/PD criterion using
biologically-plausible NMDA -- a major finding that would motivate either (a) revisiting the
joint-pass thresholds, (b) revisiting the substrate's NMDA implementation, or (c) revisiting
Sivyer 2013's measurement scope. Expected cost: ~$1.50 USD on Vast.ai EPYC 7B13 (5 gens x 96
cells x 30 s = 4 h x $0.35/hr). Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Tighten t0091 LHS morphology bounds using the 9 STABLE cells
from the t0090 diversity sweep</strong> (S-0090-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

51/60 morphologies in the t0090 diversity sweep failed NAN_VOLTAGE under the fixed t0083
best-cell channel set, consistent with Mainen 1996 morphology-determines-firing-pattern. Both
ends of the parameter range fail (e.g. 10-dendrite and 199-dendrite cells), so this is a
parameter-combination issue rather than a topology-size issue. Before launching t0091's joint
68-d NSGA-II, fit per-axis empirical bounds to the 9 STABLE cells (across both different and
similar populations) and use those tightened bounds for the LHS warm-start sample, instead of
the wide-open Phase B bounds. This keeps the population in the ~30 percent regime that
produces STABLE cells under any fixed channel set, materially improving NSGA-II sample
efficiency on the morphology axis. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Tonic GABA + Mg-block NMDA combination on t0054-style
architecture to test multiplicative gain rescue</strong> (S-0057-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0057-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0057_tonic_gaba_sweep_t0053/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Cumulative project evidence (t0054, t0055, t0057) converges on PolegPolsky2016's argument that
voltage-dependent NMDA Mg-block is necessary for non-trivial DSI. t0055 added Mg-block NMDA
but kept scalar gabaMOD inhibition; t0057 swapped inhibition to tonic but kept AMPA-only
excitation. Neither tested the combination. Build a minimal architecture combining (a) AMPA +
Jahr-Stevens Mg-block NMDA (t0055 NMDA_MgBlock.mod) on each E synapse and (b) tonic GABA via
gaba_tonic.mod (t0057) with the t0053 spatial centripetal gating predicate on each I synapse.
Sweep gNMDA in {0.0, 0.25, 0.5, 1.0} nS x GABA_BASE_NS in {0.1, 0.25, 0.5, 1.0} nS at fixed
gAMPA = 0.5 nS, seed 0 (16 grid cells, 5760 trials). Pass criterion: locate at least one
(gNMDA, GABA_BASE_NS) point with vector-sum DSI > 0.3 AND peak Hz >= 5 Hz, or rule it out.
Distinct from S-0054-02 (voltage-independent NMDA + scalar GABA) and S-0055-03 (Mg-block NMDA
+ scalar GABA ladder). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>📊 <strong>Verify NaR broadening hypothesis: ND-lobe firing rescue at
sub-threshold angles</strong> (S-0074-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

NaR_med and NaR_high broadened HWHM by +34 / +36 deg without changing peak rate or vector-sum
DSI. Creative-thinking hypothesised NaR's slow `s` reactivation gate creates a sub-threshold
floor that pushes ND-direction firing above zero, broadening the curve symmetrically. Test:
load per_trial_full.csv, filter rows where condition_id in (nar_high, nar_med, baseline) and
angle in (90, 120, 150, 180, 210, 240) deg, count trials with n_spikes > 0. Hypothesis
confirmed if NaR_high has > 30% of trials firing at angle 90-180 deg vs baseline ~5%. Cost:
pure-data analysis, no new sims (~15 min coding). If confirmed, NaR is a natural candidate for
AIS-localised follow-up since AIS-localised NaR could selectively boost ND firing without
affecting PD.

</details>

<details>
<summary>🧪 <strong>Warm-start NSGA-II from t0078 Pareto cells mapped into the v3
54-d parameter space</strong> (S-0080-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0080 LHS init started fresh; t0078's known-good cells (closest-to-joint at DSI 0.316 / PD
9.68 Hz; max-DSI rail at DSI 1.000) were not seeded into the v3 search. Mapping the t0078 49-d
Pareto cells into 54-d (new dendritic-spike parameters set near zero) would give NSGA-II a
near-Pareto starting population, dramatically reducing the generations needed to converge.
Implement a `seed_population` hook in `nsga2_loop.py` that mixes ~12 t0078 Pareto cells with
~12 LHS cells for the initial pop=24, then re-run for at least gen=20. Direct test: does
warm-start recover t0078's DSI 0.316 within the first generation? Cost: ~$1.00-$1.50 on
Vast.ai 64-core. Recommended task types: experiment-run, build-model.

</details>

## Medium Priority

<details>
<summary>🧪 <strong>10-replication robustness extension: rerun the 6 Genuine + 7
Marginal cells at 10 outer seeds</strong> (S-0086-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0086-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0086 used 5 outer seeds, distinguishing Genuine (5/5) from Marginal (3-4/5) from Stochastic
(<=2/5). A 10-rep extension on the 13 Genuine + Marginal cells (skip the 7 Stochastic that
already failed) would produce a finer 10/9-8/<=7 partition that more accurately separates
truly-genuine cells from borderline-Marginal cases like cell 1379 (4/5 in t0086) and cell 1559
(4/5). The bootstrap ARI would also tighten. Expected cost: ~$0.65 USD on Vast.ai EPYC 7B13
(13 cells x 5 additional reps x 135 s/rep = 2.4 h x $0.35/hr). Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>13-cell full deep-dive (extend Phase B to all 13 cells, not just
representatives)</strong> (S-0088-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0088-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0088 Phase B ran the Vm-trace deep-dive on 4 representative cells; the 13-cell pool's other 9
cells could have within-cluster mechanism heterogeneity invisible to the representative-only
analysis. Extend Phase B to all 13 cells: 13 x 16 directions = 208 NEURON sims. Compare
per-cell fractional NaP / Nav1.6 / NMDA across all cells within each cluster; report
within-cluster spread as a measure of mechanism homogeneity per cluster. Local-CPU only: 13 x
16 x ~60 s/sim = ~3.5 hours wall-clock, $0 cost. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary>🧪 <strong>2-D distal length x diameter sweep on t0024 to disambiguate
cable-filtering vs local-spike-failure</strong> (S-0034-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0034 produced a non-monotonic primary DSI (0.545-0.774, p=0.038) and a clean monotonic
vector-sum DSI decline (R^2=0.91) that falsified Dan2018's passive-TR prediction and did not
fit Sivyer2013's plateau. Creative-thinking flagged passive cable filtering past an optimal
electrotonic length (Tukker2004, Hausselt2007) as the best fit, with local-spike-failure
(Schachter2010) explaining the preferred-angle jumps at 1.5x and 2.0x. A marginal length sweep
alone cannot distinguish these two mechanisms because lambda = sqrt(d*Rm/(4*Ra)) couples
length and diameter nonlinearly. Run a 3x3 grid (length in {0.5, 1.0, 2.0} x diameter in {0.5,
1.0, 2.0}) on the t0024 port with AR(2) rho=0.6, 12-direction x 10-trial protocol per cell,
and classify each cell as cable-limited, spike-amplified, or threshold-transition. Distinct
from S-0030-04 (same approach on t0022 testbed, which was pinned at DSI=1.000 and cannot
resolve the effect). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>5-parameter CMA-ES vs Bayesian-optimisation spike on t0022 to
validate sample-efficiency assumptions</strong> (S-0033-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

The t0033 cost model commits literature-derived sample counts (CMA-ES=1,300, BO=500,
Surrogate-NN-GA=18,500) on 25 dims without empirical DSGC validation. Before the full joint
optimiser is commissioned, run a low-dim spike on t0022: (a) pick 5 representative parameters
from the committed 25 (3 Cuntz scalars: bf, distal-length, distal-diameter + gNa_dend +
gKdr_dend), (b) run 200-300 deterministic 12-angle evaluations each under CMA-ES and
sequential BO, (c) compare the DSI converged-to-within-1% sample count against the cost-grid
extrapolations, and (d) report whether either method actually converges on DSGC landscapes or
hits plateaus that the corpus did not flag. Outcome calibrates the strategy row of the cost
model before the 25-dim run. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Add a per-trial spike-count floor to the two-point envelope gate
to catch biologically implausible passes</strong> (S-0020-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Plan Risks & Fallbacks explicitly anticipated this scenario: DSI can land inside the envelope
while absolute firing rates stay unrealistically low (t0020 recorded DSI 0.7838 / peak 14.85
Hz exactly here). The current gate checks (mean_PD in [40, 80] Hz, DSI in [0.70, 0.85]) but
does not enforce biological plausibility at the trial level: the gate could pass with, say,
one trial firing 80 Hz and nineteen firing 0 Hz. Extend the envelope gate (in
tuning_curve_loss or the t0020 scorer) to add a trial-level floor: require that at least
N_pd_pass PD trials fire above a biological minimum threshold (e.g., 5 Hz). Report the
per-trial floor result alongside the mean-based envelope. Rerun scoring over t0020's existing
40-trial CSV to verify the new gate flags the current run as failed on the floor (baseline
expectation). Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>Add a slow Kv-mediated AHP mechanism to Bed B and quantify its
effect on the firing-rate ceiling and DSI</strong> (S-0076-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0076-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0076 high-rate Pareto extreme (iter 319, 127.75 Hz) exceeds biological mean PD rates
(30-80 Hz) precisely because Bed B lacks a slow-adaptation mechanism. The vendored SK and BK
mechanisms (from cortical/Purkinje sources) and the single-shell `cad` Ca pool (taur=5 ms)
collectively fail to cap firing on the timescale real RGCs use. Vendor a slow-AHP (e.g., SK_E2
with longer Ca-binding time, or a dedicated KAHP mechanism) and re-evaluate a 5-cell subsample
of the t0076 Pareto front: does the high-rate end of the Pareto front contract toward
physiological rates? Does a slow AHP open a new DSI>=0.4 + rate>=30 Hz region? This is a
focussed mechanism-addition test, not a full MOBO re-run. Recommended task types:
experiment-run.

</details>

<details>
<summary>📚 <strong>Add a Starburst Amacrine Cell feedforward layer to drive
inhibition physiologically</strong> (S-0022-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1038_nature00931`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1038_nature00931/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 driver schedules GABA directly onto each DSGC dendrite, skipping the SAC (Starburst
Amacrine Cell) layer that shapes DS inhibition in vivo (Euler-Detwiler-Denk 2002). Extend the
modeldb_189347_dsgc_dendritic library with a configurable SAC layer: an array of simplified
SAC models (single-compartment or 2-compartment) whose dendritic output drives DSGC GABA
synapses via NetCon, with SAC dendrites themselves direction-tuned per Euler2002. Expected
outcome: DSI becomes graded rather than saturated (real SAC output is not a hard half-plane
step) and peak firing rate may rise because SAC inhibition is timed to bar arrival not to a
global half-plane rule. This is a library extension not just a channel swap; produces a fourth
DSGC library asset modeldb_189347_dsgc_sac. Dependencies: t0022 library asset, Euler2002
paper. Effort ~40 hours. Recommended task type: write-library, code-reproduction.

</details>

<details>
<summary>📚 <strong>Add combined-report function that renders all four plot types
into one multi-page PDF/HTML per model</strong> (S-0011-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-03` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The four tuning_curve_viz functions currently produce seven standalone PNGs per model. A
combined per-model report (one PDF with matplotlib.backends.backend_pdf.PdfPages or an HTML
file embedding the PNGs plus a parameter header) would give a single shareable artefact for
reviewers, brainstorm sessions, and any future project paper draft. Add
tuning_curve_viz.report.build_model_report(curve_csv, out_path, *, target_csv=None,
spike_times_csv=None, title=None, params=None) that collects the existing four plots plus a
header block of model metadata (name, git SHA, DSI, peak, null, HWHM from tuning_curve_loss)
and emits either PDF (default) or HTML (--format html). Exercise in the smoke test by
rendering a report for the target curve and for t0008. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Add NMDA-block and TTX-sensitivity sweeps at each V_rest to
isolate biophysical mechanism</strong> (S-0026-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | [`10.1016_j.neuron.2016.04.041`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/paper/10.1016_j.neuron.2016.04.041/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Our V_rest sweep shows t0022 loses tuning at depolarised V_rest (DSI 0.046 at V=-30 mV) while
t0024 stays flat (DSI>=0.36). Two candidate mechanisms are Na channel inactivation and NMDA
Mg-block relief. Run the sweep once with TTX-like Na-block (g_Na=0) and once with NMDA-block
(g_NMDA=0) to isolate which channel class drives each model's V_rest sensitivity.

</details>

<details>
<summary>📚 <strong>Add statistical-comparison overlays (paired bootstrap, DSI/HWHM
annotations) to multi-model plots</strong> (S-0011-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-04` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

plot_multi_model_overlay currently draws every model as a coloured line with a shared legend
but provides no quantitative comparison on the figure itself. Extend the overlay to optionally
annotate each model with its DSI, peak rate, null rate, and HWHM (computed via
tuning_curve_loss.metrics) in the legend, and add a plot_model_comparison(model_a_csv,
model_b_csv, target_csv, out_png) function that computes a paired bootstrap
difference-of-means between two models at every angle, draws the difference curve with a
shaded 95 percent CI, and shades angles where the CI excludes zero. This turns qualitative
overlay comparisons into formally comparable figures suitable for the headline DSI-residual
reporting in S-0002-01 / S-0008-04 calibration sweeps. Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Add strict angle-grid validation mode to
tuning_curve_viz.loaders.validate_angle_grid</strong> (S-0011-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-02` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The current validate_angle_grid is permissive: it accepts 8/12/16 uniformly-spaced angle
counts and only warns on non-uniform grids. Downstream optimisation and scoring tasks (e.g.,
S-0002-01 g_Na/g_K grid search, S-0012-03 tuning_curve_loss integration) need hard guarantees
that every CSV is on the project-canonical 12-angle 30-degree grid before plots are compared.
Add a strict_mode=False parameter to validate_angle_grid that, when True, raises ValueError
unless angles exactly match np.arange(0, 360, 30.0) to within 1e-6 degree. Add a matching
--strict-angle-grid CLI flag to tuning_curve_viz.cli. Ship unit tests covering:
strict+canonical (pass), strict+8-angle (raise), strict+12-angle-shifted-by-1-degree (raise),
permissive (current behaviour preserved). Recommended task types: write-library.

</details>

<details>
<summary>🔧 <strong>Adopt exptype=2 (Voff_bipNMDA=1) as the canonical DSGC control
for downstream tasks via correction overlay</strong> (S-0048-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-02` |
| **Kind** | technique |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0048 establishes that the deposited code's exptype=1 (voltage-dependent NMDA) does not match
the paper's biological NMDA, while exptype=2 (Voff_bipNMDA=1, voltage-independent) is closer
to the paper's text statement and the deposited 0 Mg2+ condition. Per t0048's
compare_literature.md: the deposited control choice for the project's DSGC simulations should
be exptype=2, not exptype=1. Implement this as a project-wide convention change: (a) write a
corrections-overlay note attached to t0046 documenting that ExperimentType.CONTROL is
reinterpreted as ExperimentType.ZERO_MG for paper-faithful DSGC reproduction; (b) add a
project-level constant CANONICAL_DSGC_EXPTYPE = 2 in a shared module that downstream tasks
import; (c) update the project's description.md / library asset README for
modeldb_189347_dsgc_exact to record the convention. This is correction work, not an
experiment, but it gates every downstream DSGC task that compares to the paper. Recommended
task types: correction.

</details>

<details>
<summary>🧪 <strong>AIS-localised NaP placement test: distal-dendrite NaP vs AIS
NaP on cells 767 / 637 / 762</strong> (S-0084-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0084-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The de Rosenroll 2026 schema places NaP on the AIS but the v3 substrate (t0080) places NaP on
terminal dendrites instead. t0084 found NaP-dominant attribution at the terminal dendrite, but
the dominant-mechanism story may differ if NaP were instead on the AIS. Test by holding cells
767 / 637 / 762 parameters fixed but moving NaP from terminal_dends to ais_distal at the same
density, and re-evaluating DSI / PD rate / fractional contribution. Hypothesis: AIS-localised
NaP would shift dominance toward Nav1.6 or NMDA at the dendrite. Local CPU; 48 runs. Cost ~$0.
Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Alternative loss formulations (L1, max-residual,
weighted-L-infinity) benchmarked against the Euclidean default</strong>
(S-0012-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-04` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

tuning_curve_loss currently computes loss_scalar as a weighted Euclidean (L2) norm of four
normalised residuals. Downstream optimisers may prefer L1 (more robust to a single bad metric,
sub-gradient at zero), max-residual / L-infinity (guarantees every individual target is within
a budget), or Huber (quadratic near zero, linear in the tails). Add pluggable
loss_kind='l2'|'l1'|'linf'|'huber' to score and score_curves, keep 'l2' as the default to
preserve the identity contract, and add parametrised tests that exercise each norm on the same
synthetic inputs used by test_envelope.py. Once downstream grid searches (S-0002-01,
S-0002-04, S-0002-05) have produced O(1000) points, compare how each loss norm ranks the top-k
configurations and whether ranking changes meaningfully. Recommended task types:
write-library, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>AMPA conductance scan at Voff_bipNMDA=1 as a secondary check
on the residual DSI gap</strong> (S-0048-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Complementary to S-0048-01's GABA scan: re-run the same 7-point gNMDA sweep at exptype=2 with
the AMPA conductance scaled across {1.0, 0.5, 0.25, 0.125} of the deposited b2gampa = 0.25 nS
value. t0048's per-class conductance comparison shows AMPA summed conductance is similar
between PD/ND (~11 nS each), so AMPA changes alone cannot create direction selectivity, but
lowering AMPA at fixed GABA could shift the AMPA/GABA balance enough to amplify whatever
residual selectivity GABA provides. This is an essential negative control for S-0048-01: if
AMPA reduction matches GABA reduction in DSI effect, the gap is symmetric and not purely GABA.
4 trials per direction x 7 gNMDA x 4 AMPA scales = 224 trials, ~30 min CPU. Recommended task
types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Analytic Mg-block-vs-gabaMOD operating-point map: predict the
gAMPA/gGABA ratio that opens the unblock window</strong> (S-0055-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-04` |
| **Kind** | technique |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The bit-identical DSI = 0.7464 across all gNMDA values in t0055 FULL mode is mechanistically
explained by a single inequality: peak EPSP Vm under inhibition < Mg-unblock voltage (~-40 to
-20 mV). Derive a closed-form (or numeric) prediction from a single-compartment cable-theory
model: given AMPA peak conductance gAMPA, GABA peak conductance gGABA, gabaMOD direction
modulation, and the Jahr-Stevens Boltzmann (n=0.25, gamma=0.08, Vset, e=-65), what (gAMPA,
gGABA) ratio places the preferred-direction peak Vm right at the unblock knee? Validate
against the t0055 numbers (gAMPA = 0.5 nS, gGABA = 2 nS x 0.33, peak Vm ~= -55 mV — below
knee, predicting NMDA does not contribute). The output is a 2D heat-map predicting the
operating point that S-0055-03 / S-0054-02 should target empirically. Pass criterion:
theoretical prediction matches the t0055 NMDA-inert regime within +/-5 mV at the preferred
direction. Recommended task type: answer-question, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Anchor-distance lineage trace: quantify t0091 joint-pass cell as
one-mutation descendant of alt_topology anchor</strong> (S-0102-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

creative_analysis.md Section 2 reframes t0091's joint-pass cell (DSI=0.511, PD=35.1 Hz,
rob=0.79, source_generation=2) as a one-mutation descendant of alt_topology anchor row 84 --
not a de novo NSGA-II discovery. The cell sits 3.55 normalised units from row 84 vs >= 11
units to any other anchor; expected mutated dims per offspring ~1.0. Load-bearing
methodological reframing for any paper draft. Formalise as analysis: (i) pairwise Euclidean
distance from each t0091/t0099/t0102 Pareto cell to every t0091 warm-start anchor and every
t0083 anchor; (ii) classify each joint-pass-adjacent cell as 'anchor-near' (< 5 units) vs
'GA-discovered' (>= 10 units); (iii) histogram + scatter of distance vs source_generation.
Outcome: empirical answer to 'how much of NSGA-II output is searched vs preserved-from-init'
across t0080-t0102. Recommended task types: data-analysis, comparative-analysis. Cost: ~$0
(offline analysis on stored JSONLs).

</details>

<details>
<summary>🧪 <strong>AR(2) rho sweep at t0024 baseline morphology to isolate
stochastic-release smoothing from cable biophysics</strong> (S-0034-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Creative-thinking (alternative 5) proposed that AR(2)-correlated release with rho=0.6
temporally smooths the null-direction noise floor, potentially contributing to the observed
primary-DSI non-monotonicity independently of cable filtering. This hypothesis must be ruled
in or out before the cable-filtering interpretation is credible. Run the 12-direction x
10-trial protocol on t0024 at baseline morphology (length=1.0x, diameter=1.0x) with rho in
{0.0, 0.3, 0.6, 0.9} (four points) and compare primary-DSI, vector-sum DSI, null Hz, and HWHM
trajectories. If DSI is flat across rho, stochastic-release smoothing is not the driver; if
DSI varies with rho, the effect is release-noise-mediated. Distinct from S-0026-02 (which
crosses rho with V_rest to disambiguate noise vs depolarisation) because this sweeps rho at
fixed V_rest and fixed morphology to isolate the release-noise-vs-cable-biophysics axis.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Bar-locked window-length sweep (window_ms in {100, 200, 300,
500}) on t0059 substrate</strong> (S-0059-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0059-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0059 fixes window_ms = 200 (midpoint of the published 100-300 ms SAC->DSGC IPSC envelope
range). Compare-literature Limitations flags this as untested; PolegPolsky2016 [p. 1280] uses
tau ~50-150 ms and deRosenroll2026 implies shorter envelopes match in vitro better. The 8.5 ms
IPSP centre-of-mass shift demonstrated at window_ms = 200 may sharpen substantially at
window_ms = 100 (more direction-tuned suppression) or smear out at window_ms = 500 (back
toward t0057 global behaviour). Fork minimal_dsgc_bar_locked_gaba_ampa_sweep, sweep window_ms
in {100, 200, 300, 500} ms x GABA_BASE_NS in {0.10, 0.50, 1.0} nS at fixed gAMPA = 2.0 nS (12
cells, 4320 trials). Pass criterion: detect a non-monotonic vector-sum DSI vs window_ms
relationship (i.e., the 200 ms midpoint is not a local optimum), OR confirm the 200 ms choice
is robust. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Bed A cross-bed validation: re-run NSGA-II on the t0080 Bed A
morphology with the same v3 substrate</strong> (S-0086-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0086-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0086 identified 6 Genuine cells in t0080's Bed B morphology, but the v3 substrate has not
been tested on Bed A. Run NSGA-II for 8 generations at population 96 on Bed A with the same v3
substrate and the same constraint (AIS-to-soma Nav ratio >= 5). Compare: (a) does Bed A
produce more or fewer joint-pass cells than Bed B? (b) do the Bed A joint-pass cells cluster
into the same 2 phenotypes (high-NMDA + high-NaP vs high-NMDA + extended-GABA) or do they
discover a third? (c) does Bed A allow biologically-plausible NMDA solutions where Bed B does
not? Expected cost: ~$2.50 USD on Vast.ai EPYC 7B13 (8 gens x 96 cells x 60 s = 13 h x
$0.35/hr). Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Benchmark NSGA-III + restart strategies vs NSGA-II at small pop
in high-d biophysics MOBO</strong> (S-0080-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-08` |
| **Kind** | evaluation |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0080's 5-cell Pareto front is sparse (4 of 5 cells from gen 1; only cell 58 from gen 0);
inspection of the all_evaluations.json shows many cells in similar parameter clusters across
gen 0 -> 1, suggesting NSGA-II's selection pressure converged the small pop=24 prematurely.
Test three diversity-preserving alternatives at the same evaluation budget (192 cells): (a)
NSGA-III with reference-point-based survival (better for >=3-objective MOBO and high-d); (b)
NSGA-II with restart-on-stagnation (re-LHS half the population every 4 generations of HV
plateau); (c) larger pop=64 / gen=3 (same total cells but much wider parent pool). Compare
Pareto-front diversity, HV at termination, and DSI/PD reach. Cost ~$0.75 per variant; ~$2.25
total or run as one bundled task. Recommended task types: experiment-run,
comparative-analysis.

</details>

<details>
<summary>📊 <strong>Build a Baden-grounded null distribution of DSI/OSI for
t0091/t0099/t0102 Pareto evaluation</strong> (S-0103-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0103-08` |
| **Kind** | evaluation |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0103_extract_baden_2016_ds_morphologies`](../../../overview/tasks/task_pages/t0103_extract_baden_2016_ds_morphologies.md) |
| **Source paper** | [`10.1038_nature16468`](../../../tasks/t0103_extract_baden_2016_ds_morphologies/assets/paper/10.1038_nature16468/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0103 extracted DSI and OSI per cell for 1,238 DS cells across 8 Baden DS groups (DSI mean
~0.40-0.46, max ~0.73-0.76, OSI mean ~0.15-0.20). The NSGA-II Pareto fronts from
t0091/t0099/t0102 currently lack a biological null distribution to compare DSI/OSI against --
they are evaluated only against the t0024 canonical reference. Build a small task that
produces a per-Baden-group DSI/OSI empirical CDF chart, overlays the Pareto-front DSI/OSI
distributions, and reports the percentile of each Pareto cell relative to its presumed Baden
cluster. This is a cheap, high-value sanity check on whether the optimised cells fall inside
the biological envelope. Recommended task types: data-analysis, comparative-analysis.

</details>

<details>
<summary>📚 <strong>Build a headless-port scaffold library that wraps upstream NEURON
models</strong> (S-0010-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-05` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The three P2 failures all share the same root cause: upstream drivers assume a headful NEURON
GUI and hardcode paths/angles. A small library in assets/library/ that provides (a) a headless
NEURON loader that stubs out 'from neuron import gui', (b) a configurable output-path layer,
and (c) a canonical 12-angle stimulus generator would let future port tasks skip the
driver-rewrite step and go straight to P2/P3 scoring.

</details>

<details>
<summary>📚 <strong>Build a reusable DSI-objective evaluation-harness library
separating scoring from the optimiser loop</strong> (S-0033-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-06` |
| **Kind** | library |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0033 plan repeatedly treats evaluate(parameter_vector) -> DSI_scalar as the atomic unit
across CMA-ES / BO / surrogate-NN-GA strategies, but no library asset exposes this signature.
t0012 tuning_curve_loss scores full 12-angle rate vectors, not a DSI-objective scalar. Build a
library asset dsgc_dsi_objective that (a) wraps the t0022 or t0024 port behind a pure-function
evaluate_dsi(parameters, protocol, n_trials) -> DsiResult API, (b) batches (angle, trial)
pairs across an embarrassingly parallel pool, (c) returns a frozen dataclass with DSI, peak
Hz, null Hz, HWHM and a provenance dict, and (d) ships a thin CLI that accepts a parameter
JSON and emits a results JSON. Every strategy row in the t0033 cost model can then call a
single evaluator. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary>📚 <strong>Build a unified model-bed-runner library exposing Bed A and Bed
B behind one Python API</strong> (S-0070-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0070-02` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Every downstream task touching both beds (t0065, t0066, future cross-bed ports of
t0067/t0068/t0069) re-implements its own builder, override path, and trial-mode toggle. Bed A
uses HOC globals (`h.exptype`, `h.gabaMOD`, `h.s2ggaba`) via
`tasks/t0008_port_modeldb_189347/code/build_cell.py:apply_params`. Bed B uses Python overrides
on the constructed cell via `_snapshot_canonical_state` / `_apply_mode_overrides` and
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:_configure_soma`/`_configure_dends`.
Build a library asset `dsgc_model_bed_runner` exposing one `build_bed(bed, mode,
direction_deg, **overrides) -> CellBundle` API returning a uniformly-shaped bundle (cell,
synapse handles, recordings, mode metadata). The library must internally translate the FULL /
EPSP_PASSIVE / IPSP_PASSIVE trio into bed-specific implementations using the t0070 writeup as
its specification. Recommended task types: write-library, infrastructure-setup.

</details>

<details>
<summary>🧪 <strong>Calcium-clearance perturbation sweep on the 27 silenced-cell
DSI=1.0 vectors to test silence-as-mechanism hypothesis</strong>
(S-0102-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

creative_analysis.md Section 7 proposes a mechanistic reading: the 27 t0102 cells with DSI >=
0.99 / PD < 0.1 are not bugs but the GA's discovery of a lateral-inhibition silencing regime
(slow Ca clearance, strong sAHP, weak ACh drive) consistent with Poleg-Polsky 2026 SAC gating.
Take each of the 27 cells, fix the 68-d vector except CAD_TAUR_MS (Ca clearance tau, dim 38),
sweep that dim from ~65 ms down to 5 ms in 10 logarithmic steps, re-evaluate DSI/PD/rob at
N_EVAL_SEEDS=8. Question: when Ca clearance is restored, do these cells collapse to the
high-PD low-DSI corner (silence was the only DSI mechanism), or do some land in the joint
corner (Ca clearance is the active constraint and the rest of the vector is joint-viable)?
Outcome: 27 x 10 grid mapping silence-to-joint escape paths. Doubles as slice-physiology
prediction (BAPTA Ca chelation should disinhibit SAC/DSGC firing). Recommended task types:
experiment-run, data-analysis. Cost: < $0.50 (270 evaluations, no GA).

</details>

<details>
<summary>📊 <strong>Cell-767-anchored parameter-space pruning to identify well-tuned
dims that can be clamped in future Bed B optimisation</strong> (S-0081-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Compare cell 767's 54-d natural-unit parameter vector to (a) the high-DSI rail cells (699,
744, 112) and (b) the high-PD rail cells (627, 664, 730) on the t0081 Pareto front. Identify
dims whose values converge across these clusters (candidates for clamping at the median value)
versus dims that vary substantially (must remain free). Pure data analysis on
`results/data/all_evaluations.json`; no compute cost. Distinct from S-0080-04 which proposed
generic 30-40d pruning before re-running NSGA-II — this is anchored to the joint-pass cell
rather than to the t0080 Pareto. Output: a candidate clamped-parameter list and a re-run
sub-task proposal. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Co-insert Nav1.6 + Kv3 on the AIS at biological
densities</strong> (S-0069-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0069-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

S-0068-04 already proposed AIS Nav1.6 + Kv3 co-insertion. t0069's baseline-quenching means a
naive co-insertion sweep on the unweakened soma will likely also be inert. So this should run
AFTER S-0069-01 (somatic Na halved). Test 4 conditions on the t0069 substrate with halved
somatic Na: {Nav1.6_med + Kv3_med, Nav1.6_med + Kv3_high, Nav1.6_high + Kv3_med, Nav1.6_high +
Kv3_high} on AIS × PD/ND × 5 seeds = 40 trials. Hypothesis: with a weakened soma and the
natural fast-spiking AIS recipe (Nav1.6 + Kv3), the cell becomes more like a real fast-firing
RGC and DSI becomes higher (or more controllable) than the t0067 single-channel sweep showed.

</details>

<details>
<summary>📊 <strong>Conductance-matched t0052 vs t0053 comparison at fixed mean GABA
mass per trial</strong> (S-0053-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

S-0052-04 proposes a t0052 vs t0053 side-by-side comparison at matched placement, but does not
control for total GABA mass (t0052 = 66 nS mean / trial, t0053 = 100 nS mean / trial; 1.5x
difference fully accounts for t0053's flat-zero result). Run a dedicated comparative task at
conductance-matched mean GABA mass: e.g., t0052 standard gabaMOD (66 nS) vs t0053 at 1.32 nS x
50 active = 66 nS, or matched at 100 nS. Use placement_seed0.json shared between tasks. Report
all six output classes (V(t), EPSP, IPSP, PSTH, tuning curve, active-fraction) plus
per-direction trial-for-trial diffs in soma V(t). Goal: isolate the spatial-vs-amplitude
mechanism contribution to DSI from the GABA-mass confound, settling the graded-vs-binary
question at matched mean drive. Recommended task types: comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Constrained channel-only NSGA-II on fixed t0093 morphology to
disambiguate channel-side from morphology-side priors</strong> (S-0091-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-08` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | [`10.1038_nn.3565`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1038_nn.3565/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0091's 0/57 plausible-cell verdict is universally driven by channel-side priors (NMDA
per-spine, NaP density, GABA spatial gradient); morphology priors mostly pass. S-0086-01
already proposes a tighter-NMDA re-run but does not specify morphology configuration nor
combine with hard-constraint formulation. Hold morphology fixed at the t0093 verified
BedB-equivalent (PD-rate 43.6 Hz post-fix) and run NSGA-II on a 27-d channel-only space (12
channel densities + 9 NMDA/NaP-related + 6 GABA spatial) with all biological priors as hard
constraints (per S-0091-05) and tightened NMDA bounds (Sivyer 2013 5e-4 uS upper cap). Tests
whether the v3 substrate has any biologically-plausible joint-pass region in channel space
alone with verified morphology, independent of S-0086-01's broader question. If no, the
substrate is incompatible with priors regardless of morphology, motivating S-0091-06's
real-cell library. Cost ~$1.50 on Vast.ai EPYC 7B13. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Continue t0091 NSGA-II for 6 more generations (gen 3-8) to test
whether HV plateau or biological-plausibility shifts</strong> (S-0091-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0091 stopped at gen 2 of 8 when REQ-10 (>=8-cell Pareto) was satisfied 7x over (57 cells);
cost watchdog never fired ($0.65 of $4.00 cap). The HV trajectory was still climbing at +68
percent per generation (14.07 to 23.71) and plateau detection requires >=4 generations of
history before it can fire. Run pop=96 x 6 more generations on a single Vast.ai EPYC 7B13
64-core resume from t0091's gen-2 final population (snapshot the population from
results/data/all_evaluations.json). Tests three open questions: (a) does HV plateau before gen
8? (b) does any gen 3+ cell pass biological plausibility, or is universal channel-side
violation robust to generation depth? (c) does the PD vs ND anchor count shift toward
significance with more generations? Cost estimate: ~$1.80 (6 gens x ~12 min/gen wall-clock x
60 parallel workers x $0.23/hr); fits remaining $3.80 project buffer. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary>📊 <strong>Correction: replace t0051 brainstorm Park2014 DSI band 0.40-0.60
with paper-verified 0.65 / 0.73</strong> (S-0052-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The t0051 brainstorm session and the orchestrator hand-off message for t0052 cited a Park2014
in vivo DSGC DSI band of 0.40-0.60. t0052's compare_literature.md verified the original
Park2014 paper text directly (10.1523/JNEUROSCI.4038-13.2014, p. 3978): CART-Cre cells DSI =
0.65 +/- 0.05 (n=14) and TRHR-GFP / wild-type cells DSI = 0.73 +/- 0.03 (n=38). The 0.40-0.60
band is not attributable to Park2014 from the paper text. File a correction against the t0051
brainstorm results document(s) that quoted the 0.40-0.60 band, using the corrections mechanism
(corrections_specification.md), to set the canonical Park2014 DSI band to 0.65 / 0.73 +/- 0.05
across the project so downstream tasks do not inherit the wrong target. Recommended task
types: correction.

</details>

<details>
<summary>🧪 <strong>Cross-bed validation: re-run warm-start NSGA-II on Bed A with
the v3 dendritic-spike additions</strong> (S-0081-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0081 confirms that v3 dendritic-spike machinery + warm-start NSGA-II yields joint-pass DSI/PD
on Bed B. Test whether the same architecture generalises to Bed A (the t0067-t0074 substrate,
modelDB 189347 lineage with bio-realistic AIS). Port the 5 v3 dendritic-spike dims
(`gnmda_dend`, `mg_conc_mm`, `voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`) onto Bed A's
dendrites, warm-start from the closest-to-joint Bed A cells (e.g., t0074 / t0075 outputs), run
NSGA-II at pop=96 / gen=8 = 768 cells. Cost ~$3 (mirroring t0081). Recommended task types:
build-model, experiment-run.

</details>

<details>
<summary>📊 <strong>Cross-comparison task: t0052 (scalar gabaMOD) vs t0053 (spatial
PD/ND-asymmetric inhibition) once t0053 finishes</strong> (S-0052-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0053 (not_started, dependencies = same morphology + library-asset substrate as t0052)
implements spatial PD/ND-asymmetric SAC inhibition rather than scalar gabaMOD. Once t0053 is
completed, run a comparison task that side-by-side analyses the two minimal DSGCs at matched
100 E + 100 I synapse counts: peak Hz, primary and vector-sum DSI, HWHM, reliability, ND/PD
IPSP voltage ratio, ND/PD IPSP conductance ratio (where applicable), per-direction soma V(t)
overlays, and polar tuning overlays. Use the same placement seed (PLACEMENT_SEED = 0, recorded
in tasks/t0052_minimal_dsgc_scalar_gaba/results/placement_seed0.json) so synapse placement is
exactly matched. Goal: quantify the DS / firing-rate / IPSP-saturation differences
attributable to the inhibition-mechanism choice (scalar mod vs spatial asymmetry) on an
otherwise identical from-scratch substrate. Recommended task types: comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Cross-seed parameter-vector clustering of joint-pass cells:
shared archetypes vs divergent basins</strong> (S-0112-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-08` |
| **Kind** | experiment |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0106 (seed 44) produced 123 joint-pass cells; t0112 (seed 77) produced 7. Whether the two
seeds find the same archetype, overlapping basins, or independent basins is unknown because
the raw L2 metric is uninterpretable (see S-0112-04). Combine joint-pass cohorts from t0106,
t0112, and any new S-0112-01 multi-seed runs, normalise per-dimension via S-0112-04, and run
K-means / hierarchical clustering on the 68-d vectors with seed-of-origin as covariate.
Decision: if cells cluster by seed-of-origin (NMI(cluster, seed) > 0.5), each GA seed finds a
private basin; if cells cluster by morphology archetype (ND-soma / central / PD-soma per
t0108) with seed mixed within clusters, the substrate supports an archetype-conserved basin
and t0108/t0110 findings extend across seeds. Recommended task types: data-analysis,
comparative-analysis. Cost: <$0.50.

</details>

<details>
<summary>🧪 <strong>Cross-testbed DSI comparison: t0022 at 4 nS GABA vs t0024 AR(2)
noise</strong> (S-0037-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0034/t0035 already produce measurable primary DSI on t0024 via AR(2) stochastic release
(rho=0.6). t0037 now shows that t0022 at 4 nS GABA is a second valid substrate. A dedicated
comparison task should run matched 7-diameter and 5-length sweeps on both substrates with
identical stimulus schedules and report whether the two discriminators agree on
Schachter2010-vs-passive identification. If they disagree, that itself is a finding worth
investigating.

</details>

<details>
<summary>📊 <strong>Decide the fate of t0042/t0043/t0044: rewrite motivation or
cancel based on t0046 findings</strong> (S-0046-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0042 (fine-grained null-GABA ladder), t0043 (Nav1.6 + Kv3 + NMDA restoration), and t0044
(Schachter re-test on t0043) are currently `intervention_blocked` pending t0046's outcome.
t0046 establishes that the systematic peak-rate gap previously seen in t0008/t0020/t0022
(which motivated t0043's channel-inventory framing) is inherent to the deposited ModelDB code,
not a modification artefact. This invalidates t0043's stated motivation. Run a
brainstorm-style triage that (a) explicitly cancels or (b) rewrites motivations for each of
the three blocked tasks, replacing the discredited peak-rate-gap framing with t0046's
confirmed findings (synapse-count overcount; AP5-vs-iMK801 substitution; PSP amplitude
inflation). Apply corrections-overlay updates to record the decisions. Recommended task types:
brainstorming, correction.

</details>

<details>
<summary>🧪 <strong>Dense distal-length sweep at {1.0, 1.05, 1.10, 1.15, 1.20, 1.25,
1.30} to localize the peak-Hz cliff</strong> (S-0029-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1038_nn.3565`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1038_nn.3565/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Peak somatic firing rate in t0029 steps from 15 Hz at multipliers <= 1.0x to 14 Hz at
multipliers >= 1.25x with no intermediate value, and mean peak membrane voltage drifts
linearly from -4.81 mV (1.0x) to -5.23 mV (2.0x) - a 0.42 mV loss scaling linearly with length
rather than as exp(-L/lambda). A linear drop is inconsistent with passive cable attenuation
but consistent with distal synapses sitting beyond an active boosting region whose gain
depends on spatial proximity (Poleg-Polsky2016 distal Nav/Cav contribution). Add a dense
7-point sweep at {1.00, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30} to resolve whether the 15->14 Hz
step is smooth (passive) or sharp (local threshold crossing, i.e. Sivyer-like signature).
Record both peak Hz and mean peak somatic voltage at each point. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Dense morphology sweep around the t0106 winning archetype
(soma_offset ~ -130 um, elong ~ 1.2)</strong> (S-0106-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-07` |
| **Kind** | experiment |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The classical Tukker-Taylor ND-soma archetype dominates t0106's top 50 (35/50 cells with
soma_offset in [-132, -107] um and elong in [1.18, 1.25]). The second viable archetype is the
PD-soma configuration (4/50, gen 19 cell #23 at DSI = 0.96 / PD = 83 Hz) consistent with
Poleg-Polsky 2026's GABAergic synaptic-asymmetry mechanism. Hold the top t0106 cell's 54-d
electrophys subvector fixed and densely sweep the 14-d morphology subvector in a tight box
(soma_offset_pd_um in [-150, -100] um, elongation in [1.10, 1.35], 13 other dims in a 0.8-1.2
x current-value box) at N_EVAL_SEEDS = 4. Expected outcome: a high-density map of joint-pass
cell counts vs morphology coordinates that distinguishes (a) a wide basin centred on the
dominant archetype from (b) a narrow lucky-draw peak. Recommended task types: experiment-run,
data-analysis. Cost: ~$3 (200-300 cells x N = 4, no GA overhead; single Vast.ai instance, ~6-8
hours).

</details>

<details>
<summary>🧪 <strong>Denser 2-D sweep of L x d to map DSI response surface on
t0024</strong> (S-0041-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0041-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0041 overlap region contained only n=3 paired points. Run a 2-D sweep varying length and
diameter independently across a 5x5 or 7x7 grid on t0024 (at GABA operational baseline) to map
the DSI response surface rather than test collapse on two 1-D slices. Outcome would feed
directly into t0033's morphology parameterisation and quantify the interaction term that the
collapse test implied exists.

</details>

<details>
<summary>🔧 <strong>Deprioritise distal-diameter parameters in the t0033 DSI
optimiser search space</strong> (S-0035-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-06` |
| **Kind** | technique |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The t0033 DSGC optimisation plan treats distal length and distal diameter as co-equal
morphology parameters. t0034 (p=0.038 on length) and t0035 (p=0.88 on diameter) together show
that distal diameter has DSI leverage below the noise floor on the t0024 substrate, while
length is a strong discriminator. Concrete action: reduce distal-diameter weight in the
optimiser search space (smaller range, coarser grid, or drop it entirely) so the GPU budget
concentrates on axes that actually move DSI. Distinct from S-0034-07 which focuses on the
primary-vs-vector-sum objective; this one concerns the parameter search space itself.
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Distal Nav ablation crossed with distal-dendrite length sweep
on t0022</strong> (S-0029-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1038_nn.3565`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1038_nn.3565/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

HWHM in t0029 oscillates non-monotonically across length multipliers (71.7 deg at 1.5x vs
115.8 deg at 1.75-2.0x), inconsistent with any passive cable theory and consistent with distal
Nav channels crossing or failing to cross dendritic-spike threshold at a critical length.
Rerun the 7-point length sweep with distal Nav channels ablated (`forsec DEND_CHANNELS {
gnabar_HHst = 0 }`) while keeping somatic and AIS Nav intact. If HWHM becomes monotonic with
length, the non-monotonicity is a Sivyer2013 dendritic-spike signature and active boosting is
the dominant mechanism. If HWHM still oscillates, the non-monotonicity is passive cable
resonance and Sivyer2013 can be provisionally rejected on this morphology. Pairs naturally
with S-0029-01 to form a 2x2 design (Nav ablation x Poisson noise). One-line HOC overlay. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Distal voltage-trace capture at null direction on t0022 to
confirm sub-threshold-clamp hypothesis</strong> (S-0036-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0036 recorded per-trial scalar distal peak_mv only (~-55 mV at null direction) but did not
export the full distal membrane time course. Creative_thinking hypothesis 4 (distal Nav
channels sub-threshold at null regardless of diameter amplification) and limitation bullet 5
both flag missing voltage traces as blocking direct mechanistic confirmation. Extend the t0022
trial driver to save a 200-sample time-course of the most-distal compartment voltage (one
trial per direction at diameter 1.0x, GABA_NULL = 6 nS and 12 nS, 24 traces total, ~5 min
CPU). Plot v_distal(t) across directions and annotate Nav activation threshold (~-55 mV) and
AMPA/GABA event onsets. Expected: at null the distal membrane never crosses Nav threshold for
the whole AMPA window on either 6 nS or 12 nS; at preferred it crosses and fires. Closes
creative_thinking hypothesis 4 and confirms the sub-threshold-clamp failure mode. Recommended
task types: experiment-run, data-analysis.

</details>

<details>
<summary>📂 <strong>Download additional Feller-archive DSGC reconstructions to enable
cross-cell variability sensitivity analysis</strong> (S-0005-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The current dsgc-baseline-morphology commits the project to a single reconstructed cell
(141009_Pair1DSGC). Cell-to-cell variability in branching pattern, total path length, and
arbor extent is a known source of variance in DSGC tuning curves (RQ2), and the Feller archive
on NeuroMorpho hosts several sibling ON-OFF DSGC reconstructions from the same lab (e.g.,
141009_Pair2DSGC and other 2014 Pair* records). Download 3-5 additional Feller-archive ON-OFF
DSGC SWCs as separate dataset assets (each with its own NeuroMorpho neuron_id and provenance),
validate each with the existing validate_swc.py parser, and tabulate per-cell compartment
count, branch points, and total dendritic path length so a downstream morphology-sweep task
can quantify cross-cell variability without committing a priori to a specific morphology.
Recommended task types: download-dataset.

</details>

<details>
<summary>📂 <strong>Download the four discovered papers not included in the 20-paper
budget (Sivyer2017, Euler2002, Enciso2010, Webvision)</strong> (S-0002-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

research_internet.md catalogues 22 peer-reviewed candidates but only 20 became paper assets.
The held-back items are Sivyer2017 (dendro-dendritic cholinergic control of dendritic spike
initiation, Nat Commun), Euler2002 (SAC dendritic Ca signals are themselves directional,
Nature), Enciso2010 (SAC-network compartmental model, J Comp Neurosci), and the Webvision-DSGC
review. Sivyer2017 and Euler2002 directly constrain RQ4 and the presynaptic drive for RQ3, and
Enciso2010 provides a compartmental SAC-network model that could seed the presynaptic GABA
input for the DSGC model. Download them via /add-paper in a dedicated task and extend the
corpus to 24 papers. Recommended task types: download-paper, literature-survey.

</details>

<details>
<summary>📂 <strong>Download the Morrie & Feller 2018 SAC reconstructions from
NeuroMorpho and build a paired SAC+DSGC morphology asset</strong>
(S-0013-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | [`10.1016_j.cub.2018.03.001`](../../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

This task attributed the dsgc-baseline-morphology reconstruction (NeuroMorpho neuron 102976,
141009_Pair1DSGC) to Morrie & Feller 2018 Current Biology (PMID 29606419). That paper's
Methods describe paired SAC-DSGC patch recordings with 2-photon stacks of both cells
post-recording, and the SAC partner of the 141009_Pair1 recording is likely deposited in
NeuroMorpho alongside the DSGC. Search NeuroMorpho by reference_pmid=29606419 to list all
reconstructions linked to the paper, download the 141009_Pair1SAC companion SWC (and any
neighbouring Pair2/Pair3 SAC+DSGC pairs), validate with validate_swc.py, and register them as
dataset assets so downstream modelling tasks can drive dsgc-baseline-morphology with
anatomically paired SAC presynaptic input. Strengthens the SAC presynaptic drive asset of
S-0002-08. Recommended task types: download-dataset.

</details>

<details>
<summary>📚 <strong>Driving-force-corrected gabaMOD: calibrate conductance ratio to
target somatic-voltage IPSP modulation depth</strong> (S-0052-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-05` |
| **Kind** | library |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0052 establishes that scalar gabaMOD models systematically over-promise somatic IPSP
suppression: the nominal conductance ratio 3.0x (gabaMOD(180)/gabaMOD(0)) produces only a
1.54x somatic IPSP voltage ratio under realistic 100-synapse crowding, because driving force
(V - E_GABA) saturates locally. Define and document a corrected `gabaMOD_eff(theta)` whose
conductance ratio is calibrated to produce the intended somatic-voltage IPSP modulation depth
(e.g., 3.0x somatic IPSP requires ~5-7x conductance ratio under crowding). Add a small library
helper that, given target voltage modulation depth and synapse count, returns the calibrated
gabaMOD curve via a one-time calibration run on the placement, and recommends using that curve
in downstream tasks (this would be applied via correction overlay or as a successor library
asset). Goal: future scalar-gabaMOD reports do not silently confuse conductance modulation
with voltage modulation. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Excitation-side sensitivity sweep under gabaMOD-swap to close
the 25 Hz peak-firing-rate gap</strong> (S-0020-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Under the native gabaMOD-swap protocol, DSI (0.7838) sits inside the [0.70, 0.85] envelope but
PD peak (14.85 Hz) is 25.15 Hz below the 40 Hz floor. Protocol is now ruled out, so the
shortfall must live on the excitation side. Run a factorial sweep over (a) BIP synapse count
{88, 177, 354}, (b) excMOD on AMPA+NMDA in {0.5, 1.0, 1.5, 2.0, 3.0}, (c) stimulus drive
{baseline, +50%, +100%}, holding gabaMOD at the 0.33/0.99 PD/ND pair. Report the smallest
config shift that moves peak into [40, 80] Hz without dragging DSI outside [0.70, 0.85].
Distinct from S-0008-04 (sweeps all parameters including GABA side under the rotation-proxy
protocol); this is excitation-only under the native driver, addressable only now that t0020
localised the gap. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Extend DSGC model corpus to Arbor and NetPyNE
reimplementations</strong> (S-0010-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

All three candidates hunted in t0010 use NEURON; t0010's DROP list includes Schachter2010
(NeuronC). A follow-up survey task should hunt for Arbor-based and NetPyNE-based DSGC
compartmental models specifically, since those simulators are becoming standard for
large-scale retinal circuit work. Extends REQ-1 of t0010 to a second simulator axis.

</details>

<details>
<summary>🧪 <strong>Extend NSGA-II from t0083's gen-17 to gen 25 with 1.5x larger
population (144) and parameter-clustering analysis</strong> (S-0083-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0083-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0083 terminated at gen 17 on the MaxGenerationTermination(10) hard cap with HV still growing
strongly (gen 16 -> 17: +3.1%, gen 15 -> 16: +49%). The HV-plateau watchdog never fired,
indicating the search had not converged. Run NSGA-II from t0083's gen-17 final population for
an additional 8 generations at population 144 (vs t0083's 96) to test (a) whether the high-PD
joint-pass region (cells 1559, 1677) continues to expand, (b) whether new high-DSI joint-pass
cells appear above 0.77 (cell 1304's headline DSI), and (c) whether the 18-cell Pareto front
grows or saturates. Expected cost: ~$8-12 USD on Vast.ai EPYC 7B13 (8 gens x 144 cells x 64 s
= 20.5 h x $0.40/hr); requires the cost watchdog parameterisation fix from S-0083-04.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Extend patch-clamp survey to DSGC-specific dynamic-clamp, Ih/HCN
biophysics, and AIS measurements</strong> (S-0017-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0017-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0017_literature_survey_patch_clamp`](../../../overview/tasks/task_pages/t0017_literature_survey_patch_clamp.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the four DSGC-modelling sub-areas identified in the plan
(space-clamp, AIS, NMDARs, maintained activity) but leaves several high-priority follow-on
topics uncovered: (a) DSGC-specific dynamic-clamp studies that use injected conductance
waveforms to test direction selectivity mechanisms, (b) DSGC Ih/HCN biophysics and resonance
properties, (c) DSGC-specific AIS measurements (the Werginz2020 paper is on OFF-alpha T cells,
not on ON-OFF DSGCs directly), and (d) large-scale compartmental-model fitting pipelines for
RGCs. A follow-up survey task should add ~5 papers across these four sub-areas to close the
gap.

</details>

<details>
<summary>🧪 <strong>Extend synaptic-integration survey with DSGC-specific
receptor-kinetic, dynamic-clamp, and connectomic SAC-DSGC papers</strong>
(S-0018-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0018-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0018_literature_survey_synaptic_integration`](../../../overview/tasks/task_pages/t0018_literature_survey_synaptic_integration.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the five canonical themes (AMPA/NMDA/GABA kinetics,
shunting inhibition, E-I balance, dendritic-location integration, SAC-to-DSGC asymmetry) but
with one paper per theme, selected from the most-cited classical literature. A follow-up
survey task should add ~5 DSGC-targeted papers across: (a) modern DSGC-specific AMPA and NMDA
kinetic measurements at near-physiological temperature, (b) DSGC dynamic-clamp studies that
inject measured conductance waveforms, (c) connectomic reconstructions of SAC-to-DSGC wiring
(Briggman et al. 2011, Kim et al. 2014), (d) recent E-I temporal co-tuning studies in retina
(rather than auditory cortex), and (e) DSGC dendritic computation (Oesch, Euler, Taylor,
Sivyer). This closes the gap between canonical theory and DSGC-specific parameters.

</details>

<details>
<summary>📚 <strong>Extend tuning_curve_loss with a two-point (PD/ND) scoring API to
make t0012 usable under the native protocol</strong> (S-0020-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-04` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

research_code.md records that t0012's high-level score() entry point rejects the two-condition
CSV because its loader's _validate_angle_grid requires exactly 12 angles on a 30-degree
spacing. t0020 worked around this by re-implementing the DSI formula inline in
score_envelope.py. Every future gabaMOD-swap task (including S-0020-01 and S-0020-03 above)
will hit the same wall. Add a score_two_point(pd_rates: np.ndarray, nd_rates: np.ndarray, *,
dsi_envelope, peak_envelope) -> TwoPointScore API to tuning_curve_loss that returns DSI, mean
PD, mean ND, per-condition stderr, gate.passed, plus optional per-trial CIs via bootstrap.
Keep the 12-angle score() untouched; the new API is an additional entry point. Register it in
the tuning_curve_loss library details.json entry_points. Recommended task types:
write-library.

</details>

<details>
<summary>🧪 <strong>Extend voltage-gated-channel survey with recent DSGC-specific
Nav/Kv patch-clamp and super-resolution AIS microdomain papers</strong>
(S-0019-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The scaled-down 5-paper survey covers the five canonical themes (Nav subunit localisation at
AIS, Kv1 subunit expression at AIS, RGC HH-family kinetic rate functions, Nav1.6 vs Nav1.2
co-expression kinetics, AIS Nav conductance density) but with one classical paper per theme. A
follow-up survey task should add ~5 DSGC-targeted papers across: (a) DSGC-specific Nav/Kv
patch-clamp measurements at near-physiological temperature, (b) super-resolution microscopy of
AIS microdomains (panNav vs subtype-specific antibodies, STED/STORM), (c) developmental Nav/Kv
channel trajectory studies in RGC AIS, (d) M-current/Kv7/KCNQ channels at RGC AIS, (e) Kv3
fast-delayed-rectifier measurements in RGC. This closes the gap between canonical
voltage-gated-channel theory and DSGC-specific parameters.

</details>

<details>
<summary>🧪 <strong>Extended distal-dendrite length sweep (1.0x to 4.0x, 8.0x) to
reach Dan2018's critical regime</strong> (S-0029-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1038_s41598-018-23998-9`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1038_s41598-018-23998-9/) |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Dan2018 reports monotonic DSI-vs-length over 50-400 um distal branches; Sivyer2013's critical
length sits at ~150 um. The t0022 distal-leaf baseline is on the order of tens of um, so the
0.5-2.0x sweep likely spans only ~15-160 um, overlapping only the tail of Sivyer2013's range
and sitting entirely below Dan2018's critical length. Add three extreme sweep points at 3.0x,
5.0x, and 8.0x while keeping the rest of the t0022 testbed fixed. Watch for `d_lambda`
violations at extreme lengths (fallback: adaptive `nseg` at each point). Possible outcomes:
(a) DSI stays at 1.000 and peak Hz continues linear decline - testbed is cable-dominated at
the soma and no resolution is possible; (b) DSI drops at a specific high multiplier with
monotonic HWHM broadening - Dan2018 passive-TR regime emerges; (c) DSI drops with HWHM
narrowing at a specific multiplier - Sivyer2013 dendritic-spike-failure regime emerges. ~45
min CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-diameter sweep on t0024 (0.25x to 4.0x, 9 points)
to probe non-linear extremes</strong> (S-0035-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`cable-theory`](../../../meta/categories/cable-theory/) |

Push the diameter multiplier beyond t0035's narrow 0.5x-2.0x range into a wider 0.25x-4.0x
sweep (nine multipliers) on the t0024 DSGC substrate to look for non-linear DSI effects that
the 4x range missed. Specifically targets two possibilities: (a) input-impedance saturation at
baseline may break at extreme thinning/thickening and (b) the cable-theory 1/sqrt(d)
prediction implies a detectable DSI shift over a 16x diameter range even if a 4x range is
inside the noise floor. Distinct from S-0030-03 which targets t0022. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Extended distal-length sweep on t0024 (0.25x to 4.0x, 9 points)
to characterise the electrotonic-length optimum</strong> (S-0034-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0034 covered 0.5x-2.0x (7 points) and found the primary-DSI peak at 0.75x (0.774) with a
non-monotonic decline beyond. To fit Tukker2004's intermediate-electrotonic-length optimum
quantitatively and to test whether the curve continues falling or saturates beyond 2.0x,
extend the sweep to 0.25x, 0.375x, 0.5x, 0.75x, 1.0x, 1.5x, 2.0x, 3.0x, 4.0x (9 points). Keep
the standard 12-direction x 10-trial protocol and AR(2) rho=0.6. Expected outcomes: (a) a
clear DSI peak at intermediate length with symmetric falloff on both sides (supports
Tukker2004 optimum); (b) preferred-angle instability across 3.0x-4.0x (supports Schachter2010
local-spike-failure); (c) d_lambda violations at extreme lengths (engineering concern - apply
adaptive nseg at each point). Distinct from S-0029-03 (same approach on t0022 testbed which
was pinned at DSI=1.000). Recommended task types: experiment-run.

</details>

<details>
<summary>📚 <strong>Extract the t0022 GABA-override monkey-patch into a reusable
library asset for downstream tasks</strong> (S-0036-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-04` |
| **Kind** | library |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0036 introduced code/gaba_override.py which monkey-patches
_t0022_constants.GABA_CONDUCTANCE_NULL_NS at import time and re-binds the local name inside
trial_runner_diameter.py so the schedule_ei_onsets ratio is computed against the overridden
value. This pattern is immediately needed for S-0036-01 (further null-GABA reductions) and
S-0036-02 (GABA-AMPA timing offset). Rather than each task reimplementing the monkey-patch,
lift it into a library asset (working name: dsgc_t0022_schedule_overrides) exposing a typed
context-manager or setup function accepting gaba_null_ns, gaba_preferred_ns,
gaba_to_ampa_lead_ms, returning a provenance dict logged at task start. Ships a smoke test
asserting the override survived a fresh import and that the null/preferred ratio matches the
requested value. Distinct from S-0033-06 (DSI objective evaluator) which wraps the scoring
side - this wraps the schedule-parameter side. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Factorial (g_Na, g_K) grid search on a DSGC compartmental model
to locate the DSI-maximising conductance ridge</strong> (S-0002-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1152_jn.00123.2009`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1152_jn.00123.2009/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

No paper in the 20-paper corpus (including Fohlmeister2010, Schachter2010, PolegPolsky2016,
Vaney2012) reports a factorial grid search over somatic (g_Na, g_K) pairs for a DSGC — this is
the central gap identified for RQ1 by the survey. Run a grid with g_Na swept across 0.02-0.20
S/cm^2 and g_K (delayed rectifier) swept across 0.003-0.050 S/cm^2 on the baseline DSGC
morphology and 177+177 synaptic budget, record DSI, preferred peak, null residual, and
tuning-curve HWHM at each point, and publish the ridge of combinations that hit DSI 0.7-0.85
with peak 40-80 Hz and null < 10 Hz. This directly supplies the RQ1 answer the project needs.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Find the NaP density at which vector-sum DSI crosses 0.1</strong>
(S-0074-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-07` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

NaP_low gives vector-sum DSI = 0.227 (delta +0.034). NaP_med gives 0.226 (delta +0.033).
NaP_high gives 0.050 (delta -0.143). The DSI-loss transition between NaP_med (0.01 mS/cm²) and
NaP_high (0.05 mS/cm²) is sharp; the exact threshold density is between 0.01 and 0.05. Run a
5-density sweep (e.g., 0.01, 0.015, 0.02, 0.03, 0.05 mS/cm²) × 12 angles × 5 seeds × 5
conditions = 300 trials, ~12 min compute. Hypothesis: there's a critical density d* in (0.01,
0.03) above which vector-sum DSI drops sharply; characterising d* exactly is needed for any
future NaP-modulation experiments. Updated version of S-0067-01 using vector-sum DSI rather
than legacy DSI as the metric.

</details>

<details>
<summary>🧪 <strong>Fine-grained thin-end diameter sweep D in {0.3, 0.4, 0.5, 0.6,
0.7} at GABA=4 nS on t0022</strong> (S-0039-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`cable-theory`](../../../meta/categories/cable-theory/) |

t0039 found DSI saturates at 0.429 for D in {0.5, 0.75, 1.0}, matching the t0037 4 nS ceiling.
This is the discriminator's upper bound at this GABA level. A finer sweep thinner than 0.5x
would locate the saturation edge and bound the headroom available to any morphology optimiser
on t0022. 5 diameters x 12 angles x 10 trials = 600 trials, ~25 min local CPU, $0.00.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan at Voff_bipNMDA=1 to close the residual
DSI gap to paper's 0.30 line</strong> (S-0048-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0048 confirmed that switching to voltage-independent NMDA (exptype=2) flattens the DSI vs
gNMDA curve to 0.04-0.10 but never reaches the paper's claimed flat ~0.30. The residual gap
must come from non-NMDA mechanisms; the leading candidate is GABA, where t0047 measured
deposited PD ~106 / ND ~216 nS summed conductance vs paper's PD ~12.5 / ND ~30 nS (8x over) at
gNMDA = 0.5 nS. Run a parameter sweep at exptype=2 over a GABA scale factor in {1.0, 0.5,
0.25, 0.125, 0.06} (ratios chosen to bracket paper's 12.5x reduction toward biological values)
at the same 7 gNMDA grid points x 4 trials per direction used here. Track DSI vs (gNMDA, GABA
scale) and report whether any GABA setting produces flat DSI ~0.30 across the gNMDA range.
Pass criterion: identify a GABA scale (if any) that simultaneously satisfies the H1
range/slope thresholds and a mean-DSI > 0.20 target. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA conductance scan under SEClamp toward paper PD 12.5 / ND
30 nS at fixed gNMDA = 0.5 nS</strong> (S-0049-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

SEClamp at -65 mV yielded GABA PD = 47.47 / ND = 48.04 nS vs paper's 12.5 / 30 nS. Run a
`gabaMOD` (or per-synapse GABA) scan under SEClamp at gNMDA = 0.5 nS, exptype = control, with
multiplier values across {1.0, 0.5, 0.25, 0.125} of the deposited base, and additionally test
introducing PD/ND spatial asymmetry (e.g., scale ND-side GABA up by 2-3x and PD-side GABA
down) to see whether the paper's ND-bias DSI -0.41 is recoverable by a spatial redistribution
at the soma. Distinct from S-0048-01 which scans GABA at exptype = 2 across a gNMDA sweep
without SEClamp; this task uses SEClamp modality at single gNMDA. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA spatial-gradient ablation: does GABA shape
direction-asymmetry causally?</strong> (S-0088-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0088-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Source paper** | [`de_rosenroll_2026`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/paper/de_rosenroll_2026/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0088 found GABA rho0 exotic (>+5 sigma) in all 4 clusters and GABA lambda exotic in 3 of 4
clusters. The model exploits exotic GABA spatial scale to shape direction-asymmetry. Test
causally: set rho_0_gaba = 1.0 (Rosenroll baseline) or lambda_gaba_um = 80 (Rosenroll mean)
per representative cell and re-measure DSI at 16 directions. Expected effect: if GABA spatial
gradient is causal for direction selectivity, DSI degrades; if NaP alone explains DSI, DSI is
preserved. 4 cells x 2 GABA-knockout variants x 16 directions = 128 sims; ~2 hours local CPU,
$0 cost. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>GABA-to-AMPA timing offset sweep on t0022 diameter testbed to
test timing-dominates-conductance hypothesis</strong> (S-0036-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0036's creative_thinking cited 'timing dominates conductance' as the second-leading
explanation for why halving null-GABA from 12 nS to 6 nS did not unpin null firing: the t0022
schedule delivers GABA 10 ms BEFORE AMPA on null trials, and the integrated kinetic profile
(not the peak) may clamp the distal membrane below Nav threshold for the whole AMPA window.
Sweep the GABA-leads-AMPA offset across {10 ms (default), 5 ms, 0 ms, -5 ms (AMPA leads GABA)}
at two fixed GABA conductances (12 nS baseline and 6 nS) at diameter 1.0x only (12 angles x 10
trials x 4 offsets x 2 GABA = 960 trials, ~35 min CPU). Primary outcome: find the offset at
which null firing first exceeds 0.1 Hz, isolating timing as an independent rescue axis
orthogonal to S-0036-01's conductance axis. Distinct from S-0030-02 (Poisson) and S-0036-01
(conductance) - this targets the GABA-AMPA offset specifically. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>GABA/AMPA density ratio scan at fixed 3-5x null/preferred IPSC
asymmetry</strong> (S-0002-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

PolegPolsky2016 sets GABA/AMPA at 1:1 (177/177), while Park2014 and Taylor2002 constrain the
null/preferred IPSC ratio to 3-5x but not the total GABA density. Scan the GABA/AMPA density
ratio from 0.5 to 4.0 (keeping the 3-5x null asymmetry fixed, the 40-80 Hz preferred peak
fixed by the Na/K ridge, and the morphology and dendritic conductances fixed) and report how
tuning-curve HWHM and preferred peak rate co-vary. The expected pattern (sharper tuning at the
cost of lower peak rate) is stated in research_internet.md as hypothesis H4 but is not yet
tested in the literature. This directly refines the RQ3 answer. Recommended task types:
experiment-run.

</details>

<details>
<summary>📂 <strong>Generate weaker-DSI variant target tuning curves</strong>
(S-0004-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0004-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Create sibling dataset assets (e.g., target-tuning-curve-weak-dsi,
target-tuning-curve-mid-dsi) with the same generator but r_peak values chosen so DSI lands at
~0.65 and ~0.75. Lets downstream fitting tasks test whether the optimisation pipeline is
robust across the 0.6-0.9 band instead of only the upper end.

</details>

<details>
<summary>🧪 <strong>Hand-port deRosenroll2026 ds-circuit-ei model and remap 8-angle
grid to 12 angles</strong> (S-0010-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Port geoffder/ds-circuit-ei-microarchitecture (Zenodo 10.5281/zenodo.17666157, MIT LICENSE).
Requires adding statsmodels, h5py, fastparquet, oiffile as optional deps (or extracting a
minimal driver subset without them), then extending the hardcoded 8-direction ANGLES_DEG list
to the canonical 12-angle protocol before scoring. t0010 exited at P2 within the 90-min cap;
budget 4-6 hours for full P3.

</details>

<details>
<summary>🧪 <strong>Hand-port Hanson2019 Spatial-Offset-DSGC model to headless
12-angle sweep</strong> (S-0010-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1038_s41467-019-09147-4`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-019-09147-4/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Rewrite the upstream run.py driver from geoffder/Spatial-Offset-DSGC-NEURON-Model to remove
the headful 'from neuron import h, gui' import and the hardcoded C:\Users\geoff\NEURONoutput
path, then adapt it to the canonical 12-angle x 20-trial sweep scored against the t0012
tuning-curve API. t0010 exited at P2 within the 90-min per-candidate cap; a dedicated port
task can budget 3-4 hours and reach P3.

</details>

<details>
<summary>📊 <strong>Harmonised cross-comparison of the three ModelDB 189347 sibling
ports (t0008, t0020, t0022)</strong> (S-0022-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-07` |
| **Kind** | evaluation |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The project now has three independent implementations of DS on the same Poleg-Polsky & Diamond
2016 skeleton: t0008 (per-angle BIP rotation, DSI 0.316), t0020 (global gabaMOD scalar swap,
DSI 0.7838), and t0022 (per-dendrite E-I scheduling, DSI 1.0). Each used slightly different
scoring paths, trial counts, and metric key sets. Produce a shared analysis module that loads
each port's tuning_curves.csv, recomputes DSI / peak / null / HWHM / reliability under one
harmonised scorer (t0012 score() where applicable plus S-0020-04's score_two_point for t0020),
and produces one side-by-side comparison chart (polar plot overlay plus bar chart of headline
metrics). Outputs a consolidated comparison_report.md plus an overview/llm-context/ snapshot.
Dependencies: t0008, t0020, t0022 library assets, t0012 scorer. Effort ~12 hours. Recommended
task type: data-analysis, write-library.

</details>

<details>
<summary>🧪 <strong>Higher-N (12-19 trials) rerun of t0048's Voff_bipNMDA=1 gNMDA
sweep to tighten H2 verdict bands</strong> (S-0048-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0048 used 4 trials per direction per gNMDA value. SD on PSP amplitudes was 0.16-1.02 mV,
which is below the trial-to-trial PD/ND difference at most grid points, but the H2-vs-H1
boundary at the slope test (-0.024 vs |slope| < 0.020 cutoff) is close enough that more trials
might tip the verdict. Re-run this same Voff_bipNMDA=1 sweep at the paper's reported N (12-19
trials per direction per gNMDA value) using the existing code/run_voff1_sweep.py with extended
trial seed ranges. This is distinct from S-0046-01 which targets the Voff_bipNMDA=0 baseline;
S-0048-04 specifically tightens t0048's Voff=1 H2 finding. Pass criterion: report whether the
slope test verdict changes from H2 to H1 with paper-N. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Higher-statistics re-run of t0034 at 1.5x and 2.0x (30+ trials
per angle) to confirm the preferred-angle jumps</strong> (S-0034-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0034's non-monotonicity hinges on two preferred-angle jumps: 0 deg -> 330 deg at 1.5x (DSI
dip to 0.623) and 0 deg -> 30 deg at 2.0x (DSI collapse to 0.545). These are based on only 10
trials per angle, and the compare-literature analysis notes the 95% CI on a 10-trial DSI is
~+/-0.1 - comparable to the 0.23 observed DSI spread. Re-run the protocol at 1.5x and 2.0x
with 30-50 trials per angle (3-5x the baseline count) and recompute bootstrap CIs on DSI and
preferred-angle estimates at each point. If the jumps persist, Schachter2010
local-spike-failure is strengthened; if they collapse to a single preferred direction, they
were small-N artefacts and the cable-filtering story becomes more parsimonious. Listed in
compare-literature.md as a concrete limitation. Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Hybrid BoTorch-warmup + NSGA-II-refinement optimiser for high-d
MOBO on biophysics</strong> (S-0080-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-05` |
| **Kind** | technique |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0078 hit O(N^3) GP-fit scaling at ~480 cells; t0080's NSGA-II at pop=24 was
sample-inefficient in 54-d. A hybrid approach exploits both methods' strengths: run BoTorch
qLogNEHVI for the first 50 cells (where the GP scales fine) to generate a sample-efficient
seed population, then switch to NSGA-II at pop=50 / gen=20 starting from those 50 BoTorch
cells plus 50 LHS cells. The BoTorch warmup biases the initial population toward
Pareto-relevant regions; NSGA-II then explores without the GP-fit blow-up. Implement as a
wrapper around the t0080 `nsga2_loop.py` and t0078's BoTorch driver. Cost ~$1.50 on Vast.ai
64-core. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🔧 <strong>Hybrid spatial-gating + amplitude-scaling inhibition mechanism
on minimal DSGC</strong> (S-0053-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-05` |
| **Kind** | technique |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0053_minimal_dsgc_spatial_gaba/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0052 scales all 100 I synapses by a graded gabaMOD(theta); t0053 binary-gates a subset at
full amplitude. A biologically motivated hybrid gates which I synapses fire (t0053's
per-synapse centripetal threshold) AND scales their amplitude by a global gabaMOD(theta)
factor (t0052's amplitude curve). This decomposition matches the SAC network's
centrifugal-release preference (spatial gating) layered on top of any global drive modulation.
Build a variant library `minimal_dsgc_hybrid_gaba` implementing both rules, sweep the gabaMOD
amplitude floor in {0.33, 0.5, 0.66, 1.0} at fixed centripetal threshold cos < 0, and report
DSI, peak Hz, HWHM, IPSP modulation, and active-fraction per floor. Goal: test whether
combining the two mechanisms produces a tuning curve closer to Park2014 / deRosenroll2026
bands than either alone. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>Hybrid tonic + transient GABA envelope on minimal DSGC to model
multi-event SAC release</strong> (S-0057-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0057-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Real SAC->DSGC IPSCs envelope over 100-300 ms via multiple GABA release events per varicosity,
between t0057's single 1300 ms pulse and t0053's single ~80 ms decay tail. Build a hybrid
mechanism whose conductance envelope is the sum of a low-amplitude tonic floor (g_tonic over
[t_on, t_off]) and a sequence of transient Exp2Syn events (rise 1 ms, decay 20 ms) at rate r
in {25, 50, 100} Hz over the same window. Keep the t0053 spatial centripetal gating rule and
t0057 placement seed unchanged so this isolates envelope-shape effects. Sweep g_tonic in {0.0,
0.05, 0.1, 0.2} nS x g_event in {0.5, 1.0, 2.0} nS x rate r in {25, 50, 100} Hz (36 grid
cells, 12960 trials). Report peak Hz, primary and vector-sum DSI, IPSP envelope variance, and
IPSP autocorrelation timescale. Pass criterion: locate at least one (g_tonic, g_event, r)
triple with peak Hz != null Hz in FULL mode AND IPSP envelope tau within 100-300 ms biological
band. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>IBEA vs SMS-EMOA comparison on the 2-direction substrate (renews
S-0104-04 on working substrate)</strong> (S-0106-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0106_long_pdnd_nsga2_300gen/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

S-0102-03 and S-0104-04 proposed IBEA on the 16-direction substrate where NSGA-II returned
zero joint-pass cells; that comparison conflated algorithm choice with metric choice. t0106
now provides a working substrate (2-direction ratio DSI, 123 joint-pass cells from NSGA-II) on
which to isolate the algorithm dimension. Run pymoo IBEA and SMS-EMOA at matched budget to
t0106 (pop = 96, n_gen = 40, N_EVAL_SEEDS = 3, single GA seed) on the same 68-d substrate with
the 2-direction ratio DSI + PD-rate objectives. Decision: if IBEA / SMS-EMOA produce more
diverse interior fronts than NSGA-II's L-shape (hypervolume + spacing), Mohacsi 2024's IBEA
recommendation generalises. If NSGA-II remains competitive, the working-substrate finding is
algorithm-agnostic and prior IBEA suggestions can be downgraded. Recommended task types:
experiment-run, comparative-analysis. Cost: ~$20.

</details>

<details>
<summary>🧪 <strong>Inject Poisson background rate on the t0022 driver to moderate
DSI from 1.0 toward the 0.5-0.8 published band</strong> (S-0022-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1016_j.neuron.2005.06.036`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1016_j.neuron.2005.06.036/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 NetStim burst driver uses noise = 0 and baseline synapses are silenced, so DSI
saturates at 1.0 across all 60 null-direction trials. Park2014, Oesch2005, and Poleg-Polsky &
Diamond 2016 all report DSI in the 0.5-0.8 range because real DSGCs have 2-5 Hz per-trial
spike jitter from stochastic bipolar release. Extend the driver with a configurable background
Poisson process (1, 2, 3, 5 Hz baseline rate on all synapses) and rerun the 12-angle x
10-trial sweep at each noise level. Expected outcome: DSI curve drops from 1.0 to ~0.8 at 2 Hz
bg to ~0.6 at 5 Hz bg, bracketing the literature envelope, with per-angle std rising from 0 Hz
to ~2-4 Hz matching Schachter2010 trial-to-trial variability. Dependencies: t0022 library
asset. Effort ~8 hours. Recommended task type: experiment-run.

</details>

<details>
<summary>📚 <strong>Instantiate AIS_PROXIMAL / AIS_DISTAL / THIN_AXON channel sets on
t0022 as a t0033 optimiser prerequisite</strong> (S-0033-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-02` |
| **Kind** | library |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0022 testbed exposes AIS_PROXIMAL, AIS_DISTAL, and THIN_AXON channel-set hooks in its
modular architecture, but all three are empty because the Poleg-Polsky 2026 backbone has no
axon. The t0033 joint optimiser plans per-region gbar for Nav1.1, Nav1.6, Kv1.2, Kv2.1,
Kv3.1/3.2 and Km/KCNQ across these regions, which is impossible until the hooks are live.
Build a task that (a) adds a short axon hillock + AIS + thin-axon trunk to t0022 using Werginz
2020 / Van Wart 2007 geometry, (b) populates AIS_PROXIMAL with Nav1.1+Kv1.2, AIS_DISTAL with
Nav1.6+Kv3, and THIN_AXON with Nav1.6+Kdr at literature-consensus densities, (c) reruns the
t0022 12-angle sweep and checks DSI and peak rate do not regress, and (d) registers a new
sibling library asset. Recommended task types: infrastructure-setup, build-model,
write-library.

</details>

<details>
<summary>🧪 <strong>Intermediate-gabaMOD sensitivity sweep to map the PD-ND
transition curve</strong> (S-0020-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The canonical protocol uses only the two endpoints gabaMOD = 0.33 (PD) and 0.99 (ND).
Task_description Scope explicitly deferred intermediate values as follow-up work. Run 20
trials per condition at gabaMOD in {0.20, 0.33, 0.50, 0.66, 0.83, 0.99} and plot firing rate
vs gabaMOD plus DSI computed as (rate_at_0.33 - rate_at_X)/(rate_at_0.33 + rate_at_X).
Outputs: (1) a firing-rate-vs-gabaMOD curve that shows whether the 0.33 -> 0.99 transition is
sigmoidal, threshold-like, or linear; (2) the critical gabaMOD value at which DSI crosses 0.5
(useful for later calibration); (3) a CSV with schema (gabamod, trial_seed, firing_rate_hz).
Probes whether the paper's two-point choice lies on a plateau or a steep-response region of
the inhibition axis, directly informing the inhibition-strength free parameter for later
optimisation. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Investigate the 4 PD-rate=0 cells: do morphology variants shift
direction-tuning peak away from 0 deg?</strong> (S-0093-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0093-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

4/60 post-fix cells (different/morph_18, _25, _29, similar/morph_17) fire spikes only at
non-PD directions (e.g. morph_18: 0 spikes at 0 deg, 1 each at 45/90/135/180 deg, DSI=-1.0).
t0083 channels were calibrated on the BedB hand-coded morphology, so it is unknown whether
morphology variants intrinsically shift the direction-tuning peak. Re-run those 4 morphologies
at fine angular resolution (every 15 deg) under the t0083 best-cell vector, plus 5 cells
nearest the BedB symmetric anchor as control, and fit the angular position of the firing-rate
peak per cell. Output: `peak_direction_per_morph.json` mapping morph_id -> peak_direction_deg,
plus a polar-tuning-curve panel. If peaks shift systematically with asymmetry knobs, this
resolves t0091's design question of whether per-cell PD must be re-discovered after morphology
changes. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Investigate the symmetric high-DSI outlier pocket: cells with
DSI > 0.2 AND asym_score < 0.5</strong> (S-0105-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

All 20 symmetric cells in the t0105 primary cohort come from t0091's warm-start (asym_score =
0 exactly), but two of them have DSI > 0.2 (cells #2 from t0091 gen 1 with DSI = 0.329 / PD =
12.86 Hz; cell from t0091 with DSI = 0.198 / PD = 46.14 Hz). These are 'symmetric high-DSI'
outliers that contradict the simple 'asymmetric morphology required for DSI' reading. Inspect
their full 68-d parameter vectors, check whether their high DSI is silence-artifact-adjacent
(PD < 5 Hz with small spike count), and if not, run a small perturbation grid around their
parameter neighbourhood to see whether a symmetric-morphology DSI > 0.2 plateau exists. This
would significantly alter the project's understanding of which substrate features are required
for direction selectivity. Recommended task type: data-analysis + experiment-run. Cost:
~$0.5-1.

</details>

<details>
<summary>🧪 <strong>Investigate the synapse-XY symmetry residual (Phase D Candidate
C) under neutral asymmetry knobs</strong> (S-0092-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0092-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The post-fix BedB-equivalent meets PD-rate>0 (43.6 Hz) but DSI=0.034, missing the >0.1
criterion. Phase D root-cause analysis traced this to Candidate C: under neutral asymmetry
knobs (soma_offset_pd_um=0, field_elongation_pd=1.0, branch_density_gradient_pd=0,
primary_branch_pd_concentration=0) primary stems extend symmetrically around the soma and 41%
of synapses fall outside the bar's [0, 1400] ms window for the PD direction. Quantify the
relationship between each of the 4 asymmetry knobs and post-fix DSI by sweeping each one while
holding the others neutral, then identify a slightly-asymmetric variant of BEDB_BASE_POINT
(e.g. soma_offset_pd_um=+30 um or field_elongation_pd=1.2) that produces DSI>0.1 by
construction without losing the BedB topology. The result feeds t0091's warm-start anchor
selection. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Joint (GABA, diameter) sweep to separate passive filtering from
GABA-suppressed active amplification</strong> (S-0039-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0022 shows passive_filtering at 4 nS. Two explanations: (a) t0022 lacks active machinery, or
(b) 4 nS GABA shunts regenerative events that would otherwise produce Schachter2010
concave-down. A joint sweep GABA in {5, 4, 3, 2} x D in {0.5, 1.0, 2.0} = 12 conditions x 12
angles x 10 trials = 1440 trials (~60 min) would distinguish: if lower-GABA runs produce
concave-down curves, mechanism (b) is right; if all GABA levels show passive signatures,
mechanism (a) is right.

</details>

<details>
<summary>🧪 <strong>Joint distal length x diameter 2-D sweep on t0022 to catch
interactions the marginal sweeps miss</strong> (S-0030-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

t0029 (distal-length sweep) and t0030 (distal-diameter sweep) both produced flat vector-sum
DSI curves when run in isolation on the t0022 E-I schedule. Marginal sweeps cannot reveal
interactions: Schachter2010's active amplification depends on length (number of Nav-bearing
segments) AND diameter (Nav substrate per unit length) jointly, and the cable space constant
lambda = sqrt(d * Rm / (4 * Ra)) couples them nonlinearly. Run a focused 2-D grid (e.g., 5
length x 5 diameter = 25 configurations x 12 angles x 10 trials = 3000 trials) on the
schedule-fixed testbed (S-0030-01 prerequisite). Distinct from S-0002-04 (broad factorial
including branch orders at fixed synapse count) because it is 2-D, focused, and scheduled
after the desaturation fix. Expected local CPU wall time ~7 h. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Kv3 + NaP co-expression: high-rate firing regime</strong>
(S-0074-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Kv3 was inert at all 3 densities at our peak rates (~20 Hz baseline). Literature (Rudy &
McBain 2001) says Kv3 engages strongly above 100 Hz. NaP_high produced a 74 Hz peak rate — the
highest in the sweep. Co-expression of Kv3 with NaP should put us in Kv3's effective regime.
Test: 4 conditions {NaP_high, NaP_high + Kv3_low, NaP_high + Kv3_med, NaP_high + Kv3_high} ×
12 angles × 5 seeds = 240 trials, ~10 min compute. Hypothesis: Kv3 co-expression with NaP_high
partially rescues DSI by providing fast repolarisation, allowing the cell to recover between
PD spikes and reducing the depolarisation block we hypothesised in creative-thinking.

</details>

<details>
<summary>🧪 <strong>Localise the GABA unpinning threshold with a fine sweep (5.0,
4.5, 4.0, 3.5, 3.0 nS)</strong> (S-0037-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The current sweep places the unpinning threshold between 6 nS (t0036 pinned) and 4 nS (t0037
unpinned). A 0.5 nS-spaced sweep over {5.0, 4.5, 4.0, 3.5, 3.0} nS at baseline diameter on
t0022 (5 levels x 12 angles x 10 trials = 600 trials, ~20 min local CPU) would localise the
threshold to within 0.5 nS and reveal whether the DSI vs GABA curve is sharp or gradual.
Important for characterising how fragile the operational window really is.

</details>

<details>
<summary>🔧 <strong>MAP-Elites quality-diversity search on Bed B + morphology
substrate to find off-axis joint-corner cells</strong> (S-0105-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-07` |
| **Kind** | technique |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0105 finds no joint DSI-PD factor — no single low-d axis carries both outcomes. NSGA-II (any
objective vector size or noise budget) cannot ride a non-existent axis. MAP-Elites maintains a
diversity grid over user-specified behavioural descriptors (e.g., asym_score x morphology_seed
bins), promotes corner exploration over Pareto crowding, and may find isolated joint-corner
cells that lie off any continuous axis. Run MAP-Elites at matched budget to t0104 seed 44
(~$5) on the same Bed B + morphology substrate with behavioural descriptors (asym_score,
source_lineage_marker), compare the resulting joint-corner yield. Complements S-0102-03 /
S-0104-04 IBEA suggestions but with a stronger diversity prior. Recommended task type:
experiment-run. Cost: ~$5-8.

</details>

<details>
<summary>🔧 <strong>Morinaga 2024 sign-averaging objective formulation to handle
heavy-tailed DSI noise (alpha close to 1) at fixed budget</strong>
(S-0102-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-07` |
| **Kind** | technique |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | [`10.48550_arXiv.2401.14014`](../../../tasks/t0102_seedscale_n4_gen20/assets/paper/10.48550_arXiv.2401.14014/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Morinaga 2024 (arXiv 2401.14014) Theorem 3 shows explicit averaging is only effective when the
per-objective noise stability index alpha > 1. compare_literature.md argues our DSI vector-sum
near zero-spike cells is heavy-tailed with alpha ~1, making K=4 averaging 'nearly inert'.
Theorem 9 proposes sign-averaging as a comparison-based alternative robust under heavy tails
at the same compute cost. Steps: (i) compute per-objective alpha on the t0093 anchor library
at N=20 (offline); (ii) if alpha < 1 for DSI, reformulate NSGA-II selection via sign-averaging
(count replicates favouring A over B) instead of mean ranking; (iii) run a 1-seed NSGA-II at
matched budget with sign-averaging. Complementary to S-0102-01 (DSI fix targets the
floating-point bug; this targets noise-handling theory). Recommended task types:
write-library, experiment-run. Cost: ~$3-5 (one pop=96 run plus offline analysis).

</details>

<details>
<summary>🧪 <strong>Multi-angle synaptic-current protocol on Bed A and Bed B for a
true polar synaptic tuning curve</strong> (S-0105-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-13 |
| **Source task** | [`t0105_preliminary_figures_report`](../../../overview/tasks/task_pages/t0105_preliminary_figures_report.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Figure 4 of t0105 had to fall back to a two-point polar (PD at 0 deg, ND at 180 deg) because
neither t0046 (Bed A) nor t0066 (Bed B) recorded synaptic currents at intermediate stimulus
angles. Run an EPSC + IPSC peak-amplitude protocol at the standard 12-angle grid for both beds
(re-using the bar-stimulus generator from t0046 / t0066), record AMPA + NMDA + GABA peak
conductances and peak post-synaptic currents per angle, and save a CSV per bed compatible with
the t0011 plot_polar_tuning_curve loader. Output: two new polar plots that replace t0105's
two-point fallback in any successor figure pack. Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Multi-fidelity surrogate-NN prototype to reduce the $41.56
training burn on the recommended optimiser cell</strong> (S-0033-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-03` |
| **Kind** | technique |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The recommended Surrogate-NN-GA cell in t0033 has central cost $50.54, of which $41.56 is the
one-shot 5,000-sample training burn. Creative-thinking alternative #1 argued that a
multi-fidelity surrogate (train on coarse-dt or shallow-AR(2), filter, re-score top decile on
full fidelity) should cut training USD 2-3x. Build a prototype task that (a) defines two
fidelities on the existing t0022 or t0024 port — full (dt=0.1 ms, AR(2) rho=0.6, 10 trials) vs
coarse (dt=0.25 ms, deterministic or AR(1), 3 trials) — while keeping the Jain 2020 5-10 um
compartment floor, (b) trains a 3-layer MLP surrogate on a 500-sample Latin-hypercube over the
25 committed parameters at coarse fidelity, (c) measures regret between coarse-filtered top-k
and full-fidelity top-k, and (d) reports realised training-USD reduction. Recommended task
types: experiment-run, feature-engineering.

</details>

<details>
<summary>📊 <strong>Multi-seed smoke-gate baseline -- replace
single-deterministic-reproduction with 3-5 seed reference range</strong>
(S-0083-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0083-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The pre-launch substrate-consistency smoke gate in t0081 / t0083 uses a single reference DSI /
PD value per cell with fixed tolerances (DSI 0.05, PD 1.0 Hz). t0083's smoke gate failed 1/5
(cell 767 PD 9.25 Hz vs 11.39 Hz reference, 1.14 Hz over tolerance), diagnosed as Monte-Carlo
seed-consumption variance, not substrate drift. The acceptable-negative decision was validated
by t0083's productive 14-new-joint-pass-cell run, but the design is fragile. Replace the
deterministic reference with a 3-5 seed multi-replicate range: for each smoke-gate cell, run
the simulator under 5 LHS RNG seeds, record (DSI mean +/- SD, PD mean +/- SD), and accept if
the on-instance reproduction lands within 2 SD. Recommended task types: write-library,
experiment-run.

</details>

<details>
<summary>🧪 <strong>Multi-trial t0072 extension to decompose SD bands into
across-trial vs across-synapse variance</strong> (S-0072-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0072-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0072's Limitations section flags single-seed-per-direction as the main caveat: the SD bands
in the Bed A 4x2 and Bed B 2x2 figures conflate across-synapse spatial heterogeneity with
across-trial stochastic-release variability. Re-run the t0072 protocol at N = 20 trials per
direction per bed (matching t0020 and t0066 cadence), keep the per-synapse g(t) + v_local(t)
recorders, and decompose sigma2_total = sigma2_across_trials_per_synapse +
sigma2_across_synapses_at_fixed_trial. Produce updated figures with thin SD band for
across-trial variance at the median synapse and thicker SD band for across-synapse variance at
the median trial. Expected: Bed A SDs dominated by across-synapse heterogeneity; Bed B SDs
dominated by across-trial Bernoulli stochastics. Cost: ~10 min wall-clock. Distinct from
S-0065-04 (t0065 spike-count multi-seed) and S-0055-06 (t0055 placement-seed sweep).
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>📊 <strong>N_EVAL_SEEDS>=20 robustness retest of the 7 t0112 joint-pass
cells (mirrors S-0106-02 on t0112 cells)</strong> (S-0112-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0112's 7 joint-pass cells were each evaluated at N_EVAL_SEEDS=3 inside the NSGA-II loop. The
best cell at DSI=0.9535 and the highest-PD cell at 114.76 Hz are 3-seed point estimates and
may be noise-undersampling artefacts in the same way S-0106-02 hypothesised for t0106's 3
DSI=1.0 cells. Re-evaluate all 7 t0112 joint-pass cells at N_EVAL_SEEDS=20 using the same
evaluator and silence guard. Decision: if any cell's DSI collapses by >=0.1 absolute or
PD-rate by >=15 Hz at N_EVAL_SEEDS=20, mark as noise-sensitive and exclude from the project's
reportable joint-pass cohort; if DSI and PD hold to within +/- 0.05 and +/- 5 Hz, the cells
are robust and join the substrate's reportable best cohort with t0106's 10. Distinct from
S-0106-02 which is scoped to t0106 cells only. Recommended task types: experiment-run,
data-analysis. Cost: <$0.50 (7 cells x 20 seeds, ~10 min on one Vast.ai instance).

</details>

<details>
<summary>🧪 <strong>NaP-density knockout sweep on cells 767 / 637 / 762 to test
causal necessity of NaP-dominant attribution</strong> (S-0084-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0084-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0084 attributed cells 767/637/762 PD-vs-ND integrated dendritic current asymmetry to NaP
sustained depolarisation (93.0% / 98.5% / 99.9% fractional contributions) but the metric is
correlative. Test causality by sweeping `nap_dend_distal` from its measured value down through
0 in 5 logarithmic steps for each of the three cells while holding all other 53 parameters
fixed; re-evaluate per-direction spike counts and DSI. If joint-pass DSI collapses when
nap_dend_distal=0, NaP is causally necessary; if DSI is preserved, NaP is correlative only.
Reuse t0084's run_deepdive driver. ~45 runs locally on CPU. Cost ~$0. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Narrow-bar stimulus sweep (50, 100, 150 um) on minimal DSGC to
break the synchronous-firing regime</strong> (S-0053-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Both t0052 and t0053 use a 200 um bar that crosses the entire dendritic field in one stimulus
epoch, so synapses fire near-synchronously and the cell sees a single dense
excitation+inhibition pulse per trial. This produces single-spike-per-trial behaviour (peak Hz
= 0.667 in AMPA-only) and binary on/off DSI dynamics in t0052, plus the full inhibition
pile-up that suppresses t0053. Re-run both minimal DSGCs (t0052 scalar gabaMOD and t0053
spatial centripetal at any non-suppressing g_GABA, e.g. 1.0 nS) under bar widths W in {50,
100, 150, 200} um at the same 1000 um/s velocity, so synapses fire sequentially over a longer
trial epoch. Report peak Hz, DSI, HWHM, reliability, and per-direction PSTH bin width. Goal:
test whether a narrower stimulus produces graded firing rates (multiple spikes per trial) and
a more biologically informative tuning curve under both inhibition mechanisms, decoupling DSI
dynamics from synchronous-volley artefacts. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Nav1.1 proximal-AIS knockout channel-swap on the t0022
testbed</strong> (S-0022-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1016_j.neuron.2007.07.031`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1016_j.neuron.2007.07.031/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Use the t0022 modeldb_189347_dsgc_dendritic library's AIS_PROXIMAL forsec block to append a
proximal axon segment populated with Nav1.1 at ~7x somatic density, then knock it out (set
gbar to 0) and rerun the canonical 12-angle x 10-trial sweep. VanWart2006 reports Nav1.1
dominates the proximal AIS while Nav1.6 dominates the distal AIS; removing proximal Nav1.1
should drop excitability and test whether DSI survives reduced spike-initiation margin.
Expected outcome: peak rate drops below 10 Hz while DSI holds above 0.5 (inhibitory shunt
intact, spike threshold only moved). Dependencies: t0022 library asset. Effort ~6 hours.
Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>Nav1.6 distal-AIS density sweep to close the 15 Hz -> 30-40 Hz
peak-rate gap</strong> (S-0022-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_jneurosci.0130-07.2007`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_jneurosci.0130-07.2007/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

Sweep Nav1.6 density in the AIS_DISTAL forsec block over {4, 6, 8, 10, 12, 14, 16} S/cm^2
(centred on the Kole-Stuart 2008 ~8 S/cm^2 published anchor) with Kv1.2 held constant, rerun
the 12-angle x 10-trial sweep at each setting, and report peak firing rate vs Nav1.6 density.
Peak-rate cap at 10-20 Hz is shared across t0008 (18.1 Hz), t0020 (14.85 Hz), and t0022 (15
Hz) and is inherited from the unchanged t0008 HHst Na/K density, so the fix lives in the
distal AIS. Expected outcome: peak rate scales monotonically with Nav1.6 density and lands
inside 30-40 Hz at ~8 S/cm^2, matching Poleg-Polsky & Diamond 2016 and Oesch2005.
Dependencies: t0022 library asset. Effort ~12 hours. Recommended task type: experiment-run,
comparative-analysis.

</details>

<details>
<summary>🧪 <strong>NMDA decay-time tau2 sweep at fixed gNMDA on t0054 to disentangle
conductance amplitude from kinetic time constant</strong> (S-0054-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0054 fixed NMDA tau2 at 80 ms and varied only gNMDA, conflating conductance amplitude with
kinetic time constant. Biological NMDA decay tau spans 50-200 ms across DSGC literature
(PolegPolsky2016 reports tau1NMDA = 50 ms; t0018 cites 100-200 ms). Hold gNMDA fixed at 0.25
nS (the 12x peak-rate-boost point) and sweep tau2 in {30, 60, 80, 120, 200} ms x 12 directions
x 10 trials x 2 modes (FULL, E_ONLY) = 1200 trials, on the t0054 minimal architecture with
placement seed 0, voltage-independent NMDA kept. Report per-tau2 EPSP decay tau (using the
improved metric from S-0054-03), peak Hz, and vector-sum DSI. Pass criterion: identify whether
tau2 alone (independent of gNMDA) drives the DSI collapse, or whether the collapse is
dominated by gNMDA. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>NMDA multiplicative-gain ablation to isolate its contribution
to DSI</strong> (S-0002-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

PolegPolsky2016 reports that NMDA receptors multiplicatively scale excitatory drive by ~2x and
sharpen directional discrimination, but the survey did not find a published ablation that
isolates the NMDA contribution independently of the AMPA+GABA core. Run three configurations
on the reproduced DSGC baseline (AMPA+GABA only, AMPA+GABA+NMDA with PolegPolsky2016 NMDA
parameters, AMPA+GABA+NMDA with NMDA_gain swept 1-4x) and report the DSI, peak rate, and HWHM
trajectories. This answers a specific open RQ3/RQ4-adjacent question that the literature
states but does not isolate experimentally. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Non-uniform proximal-to-distal diameter taper sweep on t0022 to
match Schachter2010 impedance gradient</strong> (S-0030-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0030 applied a single multiplier uniformly to every distal leaf, producing a 4x range that
Schachter2010's 150-200 MOhm proximal -> >1 GOhm distal (5-7x) impedance gradient indicates is
too narrow and the wrong shape. Real DSGC dendrites taper from thick primary branches to thin
terminal tips; the uniform multiplier scales all terminals together without recreating that
gradient. Implement a taper parameter k such that a segment's diameter scales by (1 + k *
path_distance / L_max), sweep k in {-0.5, -0.25, 0, 0.25, 0.5, 0.75} to produce flattened,
nominal, and exaggerated tapers, and run the standard 12-direction x 10-trial protocol at each
k (after the S-0030-01 schedule fix). Expected outcome: the exaggerated-taper cell (high k,
very thin distal) maximises distal input impedance and should exhibit the Schachter2010
amplification signature if the mechanism is active on this morphology. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary>📚 <strong>Normalised parameter-space distance metric (z-scored per
dimension) for cross-seed Pareto overlap</strong> (S-0112-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-04` |
| **Kind** | library |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0112's pareto_front_overlap.csv reports raw 68-d L2 distances of 3.5e7 - 1.9e8 between t0112
Pareto cells and their nearest t0106 neighbours. These values are dominated by
conductance-scale parameters spanning 6 orders of magnitude (S/cm^2), so the metric does not
support 'same vs different solutions' claims. Build a small analysis library (or extend
tasks/t0106 plotting code) that computes (a) per-dimension z-scored L2 over the union of t0106
+ t0112 evaluated cells, and (b) Spearman rank-correlation distance. Apply to the t0106 and
t0112 strict Pareto fronts and the broader joint-pass cohorts. Output: a normalised overlap
CSV per task and a project-level scatter of z-score NN distance vs DSI rank that reveals
whether the two seeds find the same parameter-space basin or independent basins. Reusable
downstream by S-0112-01 multi-seed analysis and S-0112-08 cross-seed clustering. Recommended
task types: data-analysis, write-library. Cost: <$0.20 (local only).

</details>

<details>
<summary>🧪 <strong>Null-GABA conductance sweep (3, 6, 9, 12 nS) to release the
deterministic ceiling on t0022</strong> (S-0029-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The t0022 scheduler uses GABA_CONDUCTANCE_NULL_NS = 12 nS applied 10 ms before AMPA on
null-direction trials - about 4x the preferred value (3 nS) and 2x Schachter2010's measured
compound null inhibition (~6 nS). This oversized early shunt forces null-direction firing to
exactly 0 Hz, pinning the pref/null DSI denominator and the ratio at 1.000 before cable
mechanics have any effect. Sweep GABA_CONDUCTANCE_NULL_NS across {3, 6, 9, 12} nS at a fixed
length multiplier of 1.0x and locate the conductance at which null-direction firing first
exceeds 1 Hz. That value is the testbed's sensitivity edge. Prerequisite for S-0029-01 and
S-0029-02: rerunning the length sweep at 6 nS instead of 12 nS gives the
mechanism-discrimination experiment a fighting chance without needing to inject noise. ~30 min
CPU. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Parameter-space pruning to ~30-40 d before re-running NSGA-II
on the Bed B substrate</strong> (S-0080-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0078's 49-d run revealed that several parameters consistently land at floors or ceilings
across the full BoTorch trajectory, suggesting they carry little Pareto information. Audit
t0078's per-parameter posterior-quantile distributions and t0080's per-parameter Pareto-cell
values; drop the 10-15 parameters with the narrowest effective ranges (e.g., parameters whose
5th-95th percentile across feasible cells spans <10% of bounded range). Re-run NSGA-II on the
pruned 30-40 d substrate at pop=24 / gen=8 to confirm that the dimensionality-vs-budget
mismatch is the dominant negative-result driver. Cost ~$0.75 (similar budget to t0080 but
smaller search space should converge faster). Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary>🧪 <strong>Parameter-sweep calibration of bundled 189347 toward the envelope
targets</strong> (S-0008-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Systematically vary the main free parameters of the 189347 HOC (bipolar-to-RGC synaptic
weight, SAC inhibition gain, NMDA/AMPA ratio, HHst gbar_ scaling) to find a parameter point
where the rotation-based protocol hits the envelope (DSI 0.7-0.85, peak 40-80 Hz, null <10 Hz,
HWHM 60-90 deg). Would produce a calibration_results.json and a mapping between
envelope-passing parameters and the paper's default values. Recommended task types:
code-reproduction.

</details>

<details>
<summary>🔧 <strong>Parametric curve fitting (von Mises / wrapped Gaussian) for
sub-degree HWHM estimates on sparse 12-angle grids</strong> (S-0012-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-02` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The current compute_hwhm_deg interpolates linearly between the two 30 deg samples bracketing
the half-maximum on each flank, limiting HWHM resolution to about 1 deg and producing a 5.5
deg deficit versus the closed-form 65.5 deg (measured 60.0 deg on the t0004 target). Add a
fit_parametric_tuning_curve helper to tuning_curve_loss.metrics that fits a von Mises or
wrapped Gaussian to the 12 angles via scipy.optimize.curve_fit, derives an analytic HWHM from
the fitted kappa or sigma, and exposes hwhm_deg_parametric and parametric_fit_residual_rms on
ScoreReport. Compare parametric HWHM against interpolated HWHM on t0004, t0008 (ModelDB
189347), and S-0002-01 grid-search points; document when interpolation suffices and when the
parametric fit is required. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>📊 <strong>Peak-rate re-analysis of cells 1559 / 1677 for direct comparison
with Trenholm 2013 / Oesch 2005</strong> (S-0083-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0083-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

Cells 1559 (DSI 0.706 / PD 39.18 Hz) and 1677 (DSI 0.657 / PD 40.71 Hz) are the project's
first cells to combine biologically-plausible DSI with PD firing rates above 30 Hz mean.
Published `[Trenholm2013, Results p. 14064]` and `[Oesch2005, Results p. 754]` report peak
rather than mean PD rates: 198 Hz Gaussian-convolved peak (Trenholm) and 148 Hz modal peak
(Oesch). The current PD-rate metric is mean rate over 1400 ms; converting cells 1559 / 1677 to
peak rate would resolve the mean-vs-peak metric mismatch and enable direct numerical
comparison with Trenholm / Oesch. Re-run cells 1559 and 1677 in subprocess with
full-resolution voltage / spike traces preserved, compute Gaussian-convolved instantaneous
rates with sigma = 25 ms over a 1400 ms window, report peak rate over the PD direction.
Recommended task types: data-analysis (no new simulator runs needed if traces from t0083 are
preserved; otherwise experiment-run with 2-cell budget < $0.20).

</details>

<details>
<summary>📊 <strong>Per-cell decoded morphology CSV dump for HM-3 follow-up</strong>
(S-0098-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0098-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0098_visualise_pareto_morphologies`](../../../overview/tasks/task_pages/t0098_visualise_pareto_morphologies.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0098 produced morphology charts but no per-cell decoded knob values. S-0091-04 (alt_topology
basin deep-dive) and S-0091-07 (PCA on Pareto morph vectors) both need a CSV with one row per
Pareto cell containing (cell_id, anchor, DSI, PD-rate, robustness, num_primary_branches,
branch_prob_per_um, max_strahler_depth, mean_branching_angle_deg, rall_exponent,
soma_offset_pd_um, field_elongation_pd, branch_density_gradient_pd,
primary_branch_pd_concentration, mean_segment_length_um, soma_diameter_um, ais_length_um,
branch_length_cv). Trivial extension of t0098's _params_from_14d helper. Also covers HM-3's
per-cell field_elongation_pd vs DSI test which Spearman length-vs-DSI did not directly answer.
Recommended task type: data-analysis. Cost: $0.

</details>

<details>
<summary>🧪 <strong>Per-compartment distal-spike detector on t0024 length sweep to
verify Schachter2010 local-spike-failure at 1.5x and 2.0x</strong>
(S-0034-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0034_distal_dendrite_length_sweep_t0024/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0034 attributed the primary-DSI non-monotonicity and preferred-angle jumps (to 330 deg at
1.5x, to 30 deg at 2.0x) to Schachter2010 local-spike-failure in distal compartments, based
only on the somatic readout and the angular-instability fingerprint. This interpretation is
currently suggestive but not confirmed. Re-run the t0034 sweep with per-compartment V
recording at every distal terminal (177 sections) and compute the distal-to-soma spike-count
ratio per trial per angle. Under Schachter2010 local-spike-failure, the ratio should be >1 at
baseline (reliable distal spikes) and drop below 1 at 1.5x and 2.0x where cable length
decouples distal tips. If the ratio stays constant, the angle jumps are not a
local-spike-failure signature and another mechanism (NMDA recruitment, Kv3 rectification)
should be explored. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Per-dendrite E-I parameter sweep to map the DSI response
surface</strong> (S-0022-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 driver has three free per-dendrite parameters fixed at single points:
EI_OFFSET_PREFERRED_MS = 10 ms, GABA_NULL/GABA_PREF ratio = 4x (12 nS / 3 nS), AMPA
conductance = 6 nS. Run a factorial sweep over EI_OFFSET in {5, 10, 15} ms, GABA ratio in {2,
3, 4, 6}, and AMPA in {0.15, 0.3, 0.6} nS (the last anchored to Park2014's 0.31 nS somatic
measurement) to quantify mechanism robustness. Expected outcome: a (3 x 4 x 3) = 36-point DSI
response surface showing which E-I corner of the parameter space saturates DSI at 1.0 (driver
is too deterministic) vs produces a graded DSI in the Park2014 0.65 +/- 0.05 band (mechanism
tracks continuous inhibition as real DSGCs do). Dependencies: t0022 library asset. Effort ~20
hours with the existing process-pool orchestrator. Recommended task type: experiment-run,
data-analysis.

</details>

<details>
<summary>🧪 <strong>Per-lineage PCA decomposition: quantify how much cross-lineage
heterogeneity contributes to PC1 separation</strong> (S-0105-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0105's pooled cohort spans four lineages with different settings (warm-start vs random-init,
N_EVAL=4 vs 20, 2-obj vs 3-obj). PC1's separation of symmetric from asymmetric cells is
confounded with the lineage source (all 20 symmetric cells come from t0091). Run PCA
independently per lineage (t0099 alone, t0102 alone, t0104 alone) and compare the top-5 PC1
loadings; if they match across lineages despite no symmetric cells, the Ca-K / NAP_PRIMARY
signature is lineage-robust rather than a t0091-warm-start artifact. Quantify cross-lineage
PC1-loading correlation to put a number on cross-lineage heterogeneity. Recommended task type:
data-analysis. Cost: $0 (pure local re-analysis).

</details>

<details>
<summary>🧪 <strong>Per-seed mechanism decomposition of cell 767 across 5 t0081
evaluation seeds to find joint-pass-supporting seeds</strong> (S-0084-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0084-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0084 ran cell 767 with a single seed (1000) and measured DSI = 0.000 vs t0081's 5-seed mean
of 0.494, indicating joint-pass depends on a subset of seeds. Re-run cell 767 across the 5
t0081 evaluation seeds (0-4), apply the same fractional-channel-contribution attribution per
seed, and report per-seed DSI plus per-seed NMDA / Nav1.6 / NaP contributions. Hypothesis:
high-DSI seeds will show non-zero NMDA contribution (Mg-unblocking gain on PD depolarisation);
low-DSI seeds will look like seed 1000. Local CPU; ~40 runs. Distinct from S-0081-01 which
varies LHS/warm-start RNG seeds at the NSGA-II population level; S-0084-02 fixes the parameter
vector and varies only per-seed evaluation noise. Recommended task types: experiment-run,
data-analysis.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite diameter
sweep on t0022</strong> (S-0030-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Sibling of S-0029-01 (Poisson + length sweep) targeting the diameter axis. The t0030
deterministic testbed yields reliability = 1.000 and null firing 0 Hz at every diameter, which
collapses the rate-code noise floor that Schachter2010's dendritic-spike-threshold mechanism
and Dan2018's passive-TR derivation both assume. Add an independent 5 Hz background Poisson
NetStim per distal dendrite (independent seed, no direction bias) to the t0022 scheduler and
rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials).
Expected: DSI drops from 1.000 into the 0.6-0.8 Park2014 envelope, reliability drops below
1.0, and diameter regains discrimination power between Schachter2010 active amplification
(+slope) and passive filtering (-slope). Distinct from S-0022-05 (Poisson at a single
length/diameter) and S-0029-01 (length axis). Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Poisson-noise desaturation rerun of the distal-dendrite length
sweep on t0022</strong> (S-0029-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0029_distal_dendrite_length_sweep_dsgc/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The t0029 sweep failed as a mechanism discriminator because pref/null DSI is pinned at 1.000
at every multiplier from 0.5x to 2.0x (null firing = 0 Hz on every trial, reliability =
1.000). Dan2018's passive-TR derivation and Schachter2010's compartmental DSGC both assume
stochastic Poisson drive with a rate-code noise floor; removing noise collapses the
mechanism-distinguishing regime. Add an independent 5 Hz background Poisson NetStim per distal
dendrite (independent seed, no direction bias) to the t0022 scheduler and rerun the full
7-point length sweep (12 angles x 10 trials x 7 lengths = 840 trials). Expected: DSI drops
from 1.000 to the 0.6-0.8 Park2014 envelope, reliability drops below 1.0, and length regains
discrimination power between Dan2018's monotonic-decrease and Sivyer2013's saturation
predictions. Distinct from S-0022-05 which runs at a single length only. Recommended task
types: experiment-run.

</details>

<details>
<summary>📊 <strong>Polar attribution decomposition: integrate fractional
contributions over the direction-tuning curve</strong> (S-0088-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0088-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0088's mechanism attribution uses only PD (0 deg) - ND (180 deg) integrated current. This
discards information from the 14 other directions recorded at 22.5-deg spacing. Compute
per-direction fractional NMDA / Nav1.6 / NaP integrals and weight by the direction-tuning
curve (the AIS spike-onset polar histogram) to get a richer cross-direction attribution. Test
whether the NaP-dominant verdict holds across all directions or only at PD-flanking
directions. Pure data analysis on existing .npz files; ~1 hour wall-clock, $0 cost.
Recommended task types: data-analysis.

</details>

<details>
<summary>📊 <strong>Pool t0091 + t0099 anchor counts to confirm HM-2 (PD-asymmetric
> ND-asymmetric) at higher n</strong> (S-0099-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0099-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-10 |
| **Source task** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0099 revised HM-2 from REFUTED to CONFIRMED by pooling 3 random-init seed counts (PD-asymm 20
vs ND-asymm 7, p~0.013). Add t0091's 12 vs 9 to get full sample: 32 vs 16 (p~0.02). Confirms
Schachter 2010 / Briggman 2011 prediction at n=4 datasets. Pure data-analysis; could form the
basis for an answer asset on the soma-displacement-toward-PD mechanism.

</details>

<details>
<summary>🧪 <strong>Port additional DSGC models from t0010 hunt and exercise
plot_multi_model_overlay with >2 models</strong> (S-0011-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0011-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0011_response_visualization_library`](../../../overview/tasks/task_pages/t0011_response_visualization_library.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

plot_multi_model_overlay caps at 6 models and was smoke-tested with only two (t0004 target +
t0008 ModelDB 189347). The t0010 hunt identified Hanson 2019 Spatial-Offset-DSGC, deRosenroll
2026 ds-circuit-ei, and other DSGC compartmental models but none have been ported to runnable
headless form yet. Run the headless-port scaffold proposed in S-0010-05 to produce
tuning-curve CSVs for 3-5 additional DSGC models, then regenerate the multi-model overlay
smoke test. This will surface any layout bugs (legend clipping, colour collisions,
preferred-direction arrow overlap) that single- or double-model overlays never exercise and
will give the project a real cross-model comparison figure. Recommended task types:
code-reproduction, write-library.

</details>

<details>
<summary>📚 <strong>Port Hanson 2019 Spatial-Offset-DSGC as a second DSGC
library</strong> (S-0008-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-01` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | [`10.7554_eLife.42392`](../../../tasks/t0008_port_modeldb_189347/assets/paper/10.7554_eLife.42392/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Port the Hanson et al. 2019 Spatial-Offset-DSGC-NEURON-Model
(github.com/geoffder/Spatial-Offset-DSGC-NEURON-Model) using the same HOC-driver pattern
proven in t0008. Hanson 2019 shares RGCmodel.hoc and HHst.mod with ModelDB 189347 and already
ships a Python driver (offsetDSGC.py); it implements DS via an explicit spatial-offset
mechanism that matches the rotation-based protocol used in t0008 more directly than
Poleg-Polsky's gabaMOD parameter swap. Expected effort ~8 hours; outcome is a second library
asset and a sanity comparison of the envelope miss pattern across two DSGC models. Recommended
task types: code-reproduction, write-library.

</details>

<details>
<summary>🧪 <strong>Port Hanson2019 DSGC model and repeat V_rest sweep to test
starburst-independent DS hypothesis</strong> (S-0026-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | [`10.7554_eLife.42392`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/paper/10.7554_eLife.42392/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Hanson2019 reports DSI 0.33 in the absence of asymmetric starburst amacrine cell responses,
suggesting an alternative mechanism. If the Hanson model is ported and swept over the same
eight V_rest values, we can compare its V_rest sensitivity against our t0022 (strongly
V_rest-dependent) and t0024 (U-shaped) results. Would clarify whether V_rest-dependence of DSI
is a universal signature or specific to starburst-driven models.

</details>

<details>
<summary>🔧 <strong>Port the full upstream SacNetwork with bp_locs/probs/deltas to
reproduce the deRosenroll correlation-drop effect</strong> (S-0024-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-01` |
| **Kind** | technique |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0024 port misses REQ-5 on all three sub-criteria (corr DSI 0.82 vs paper target
[0.30,0.50]; uncorr DSI 0.84 vs [0.18,0.35]; drop fraction 0.000 vs >=0.20) because the AR(2)
correlation was applied at per-terminal Exp2Syn drivers rather than across the
spatially-distributed SAC varicosity release network that the paper identifies as the causal
substrate. Port the upstream SacNetwork class (bp_locs, probs, deltas) from
geoffder/ds-circuit-ei-microarchitecture into a new sibling library asset, drive the same
cell, and rerun the 8-direction correlated/uncorrelated sweep. Target: reproduce the ~0.39 ->
~0.25 DSI drop.

</details>

<details>
<summary>📚 <strong>Port the Poleg-Polsky & Diamond 2016 DSGC ModelDB 189347 into
the project as a library asset</strong> (S-0003-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-02` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Download ModelDB 189347 (the only public DSGC NEURON model), re-run its included demo, and
register the resulting Python package as a library asset under `assets/library/`. This makes
the DSGC reference implementation available to every downstream simulation task without
re-download.

</details>

<details>
<summary>🧪 <strong>PP-style ablation: budget-matched comparison of
few-seeds-many-gens vs many-seeds-few-gens on 68-d substrate</strong>
(S-0101-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0101-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-11 |
| **Source task** | [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md) |
| **Source paper** | [`10.1038_s41467-026-70288-4`](../../../tasks/t0101_brainstorm_results_21/assets/paper/10.1038_s41467-026-70288-4/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Poleg-Polsky 2026 uses 50-100 GA seeds at pop=10, 300-1000 generations. Our convention is 1-2
GA seeds at pop=96, 8-17 generations. Hold total candidate budget fixed (e.g., 20 000
evaluations) and compare two configurations on the same 68-d substrate: (a) 2 seeds x pop=96 x
100 gens (closer to our convention, extreme generations), (b) 20 seeds x pop=10 x 100 gens (PP
convention). Score: number of unique Pareto cells discovered, hypervolume, joint-pass cells,
anchor diversity. Cost ~$10 at $0.24/hr Vast.ai for ~40 hours (one instance, both
configurations sequentially). Could revise our future MOBO design from BoTorch-style large-pop
NSGA-II toward PP-style many-seed (1+9)-ES if (b) wins on diversity.

</details>

<details>
<summary>🧪 <strong>Probe the AIS+axon's electrical-sink contribution by varying
axon length</strong> (S-0069-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0069-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The AIS+axon attachment dropped baseline PD spikes from 14.2 to 6.4 — a 55% reduction caused
by passive sink, not channel pharmacology. To characterise the sink contribution, sweep axon
length L_axon ∈ {0, 100, 300, 1000, 3000} μm at fixed AIS (30 μm × 1 μm), no extra channels,
and measure baseline PD/ND firing and DSI. Hypothesis: PD spike count and DSI are monotonic
functions of L_axon (more axon → more sink → fewer spikes → ND collapses to 0 first, then PD
follows). This will both calibrate the t0069 baseline against axon geometry and tell us how
much of the t0069 null result is sink-driven rather than insertion-site-driven. Compute: 5
axon-length conditions × 2 directions × 5 seeds = 50 trials, ~3 min.

</details>

<details>
<summary>📚 <strong>Promote the t0076 BoTorch MOBO + ProcessPoolExecutor trial-driver
harness into a reusable optimisation library</strong> (S-0076-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0076-06` |
| **Kind** | library |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0076 produced ~1,200 LOC of MOBO infrastructure (`mobo_loop.py`, `parametric_placer.py`,
`trial_driver.py`, `apply_params.py`, `plot_pareto.py`, `recorder.py`, checkpointing) that
worked end-to-end on Vast.ai. Future MOBO tasks (S-0076-01 tier-stratification, S-0076-02
AIS-on-Bed-B, hypothetical Bed A MOBO) will reuse 80% of this code. Promote it into a
project-level library asset `dsgc_mobo` with: (i) substrate-agnostic trial driver that accepts
any DSGC bed; (ii) pluggable parameter-space spec (Pydantic model with bounds and log/linear
flags); (iii) BoTorch wrapper supporting qLogNEHVI + Normalize transform + checkpoint-resume;
(iv) Vast.ai launch helper. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Quantify Bed A NMDA ND-suppression as a function of joint
(gabaMOD, Mg2+) on the t0072 substrate</strong> (S-0072-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0072-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0072's per-synapse recordings surfaced a counter-intuitive Bed A finding: mean peak g_NMDA is
0.30 nS at PD vs 0.19 nS at ND (~37% drop) despite identical BIPsyn release envelopes between
directions. The mechanism is the Jahr-Stevens Mg block: stronger ND inhibition keeps dendritic
v more hyperpolarised, deepening the voltage-dependent block and lowering realised gNMDA. Run
a focused 2-D sweep on the Bed A substrate (t0008/t0020 builder) varying (gabaMOD, [Mg2+]_o)
over a 5x5 grid at fixed PD/ND bar geometry, recording per-synapse g_NMDA and v_local with the
same recorder pattern as t0072, and producing the surface (g_NMDA_ND - g_NMDA_PD) vs (gabaMOD
ratio, [Mg2+]_o). Cross-check against a Voff_bipNMDA = 1 control (voltage-independent NMDA
from t0048) which should flatten the surface to ~0. Distinct from S-0026-06 (V_rest
TTX/NMDA-block sweep on t0022/t0024) and S-0048-* (DSI-vs-gNMDA at fixed Mg2+). Recommended
task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Quantify Bed A vs Bed B `celsius` and `v_init` divergence
revealed by the side-by-side equation table</strong> (S-0071-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0071-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0071_t0070_synaptic_eqs_pdf`](../../../overview/tasks/task_pages/t0071_t0070_synaptic_eqs_pdf.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Authoring all equations side-by-side in one document made four numeric divergences between Bed
A and Bed B unambiguous (rows 7, 9, 16, 17 of the comparison table in
`results_detailed.md:L778-L799`): `celsius` 32 vs 36.9 deg C (HHst gating tau differs ~2x via
Q10), `v_init` -65 vs -60 mV (shifts Mg-block operating point and Na inactivation), NMDA
on/off (S-0070-04 wires it on but does NOT pick a target value), CaL+CaT zeroed/default
(S-0070-03 turns Bed A's Ca on but does NOT pick a target). Run a 4-condition factorial sweep
on Bed A's t0065 protocol toggling `celsius in {32, 36.9}` x `v_init in {-65, -60}` to
quantify how much of the observed Bed A vs Bed B DSI / peak-Hz / EPSP-envelope difference is
attributable to these two non-Ca, non-NMDA conventions alone — the result decides whether
project-wide convention harmonisation is needed before S-0070-01..04 can be interpreted.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📊 <strong>Quantitative cable-theory fit of t0034 DSI-vs-length curve
against Rall 1/d^(3/2) and Tukker2004 predictions</strong> (S-0034-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0034's classify_shape.py assigns a categorical label (monotonic/saturating/non-monotonic) but
does not fit a parametric cable-theory model to the observed DSI vs length curve. Vector-sum
DSI declines monotonically from 0.507 (0.5x) to 0.357 (2.0x) with R^2=0.91, and peak firing
declines 40% across the sweep - both quantitative cable-filtering signatures. Write a
dedicated analysis task that fits (a) the Rall 1/d^(3/2) impedance-matching rule to the
peak-Hz decline, (b) Tukker2004's lambda-optimum function to the DSI vs length curve (extract
the fitted lambda at peak DSI), and (c) Hausselt2007's cable-length-to-DSI scaling. Output a
fitted parameter set with 95% CIs and a residual plot. This converts t0034's categorical
'cable-filtering best fit' into a falsifiable quantitative claim and enables direct
cross-paper comparison. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Random terminal-branch ablation (25%) on t0022 to test branch
independence</strong> (S-0027-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Ablate 25% of randomly-chosen terminal dendritic branches on t0022 (10 random seeds) and
measure global DSI. Prediction (creative_thinking.md #4): if [Sivyer2013, 10.1038_nn.3565]
dendritic-spike branch independence holds, global DSI drops by <15%; if global
transfer-resistance summation dominates, DSI drops by >40%. Also yields the first
DSI-vs-stochastic-pruning curve in the corpus, which would speak to in vivo robustness under
aging or disease perturbations and complement the broader factorial morphology sweep already
proposed in S-0002-04.

</details>

<details>
<summary>📊 <strong>Re-compute t0076 / t0078 / t0080 / t0081 hypervolume under a
single reference-point convention including t0081</strong> (S-0081-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Extends S-0080-06 (which scoped t0076/t0078/t0080) to include t0081. t0076/t0078 used
reference (0,0); t0080/t0081 used utopia (0.7, 80) — values are not numerically comparable
across the four tasks. Re-compute HV on the saved Pareto fronts of all four tasks under both
conventions and publish a single comparable HV trajectory plot. Pure data analysis, no
compute. Distinct from S-0080-06 in scope: t0081's Pareto front (16 cells) was not in
existence when S-0080-06 was filed. Recommended task types: data-analysis.

</details>

<details>
<summary>🔧 <strong>Re-distribute SACinhib synapses asymmetrically across PD-side and
ND-side dendrites in RGCmodel.hoc</strong> (S-0050-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0050-02` |
| **Kind** | technique |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0050_audit_syn_distribution/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Alternative 'fix path B' to S-0050-01: instead of modulating gabaMOD per synapse, modify the
construction loop in RGCmodel.hoc:11839-11857 so SACinhib synapses are placed asymmetrically
across the dendritic field (more on the ND-side, fewer on the PD-side) while leaving BIPsyn
and SACexcsyn at the deposited 282-symmetric distribution. t0050 found total dendritic length
per side is essentially identical (2311 vs 2296 um) so the dendritic substrate supports an
asymmetric placement at construction. Test whether the somatic SEClamp PD/ND asymmetry reaches
paper Fig 3C targets without changing per-synapse gabaMOD. This decouples the deposited 'three
channels share parent sections per index' design and is a more invasive but mechanistically
cleaner option. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-enable Bed A L-type and T-type Ca currents and quantify the
effect on tuning curves and DSI</strong> (S-0070-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0070-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0070 writeup documents that Bed A's `init_active` zeros `RGCcaL` and `RGCcaT`
(`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/main.hoc:L155-L156`),
removing the L-type and T-type Ca currents that are present in the original Poleg-Polsky 2016
paper. Bed B inherits the same `glbar_HHst = 3e-4` and `gtbar_HHst = 3e-4 S/cm^2` PARAMETER
defaults (`HHst_noiseless.mod:L57-L58`) on every section because its Python builder never
overrides them. This is the single most visible biophysical divergence between the two beds.
Run a controlled experiment: re-enable Bed A's Ca currents at the `HHst.mod` defaults (and at
the Bed B densities), re-run the t0065 EPSP/IPSP/FULL protocol, and report changes in DSI,
peak firing rate, and EPSP/IPSP envelopes. The result either justifies harmonising the two
beds on the same Ca configuration or documents a biophysically motivated reason to keep them
divergent. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Re-enable NMDA (b2gnmda nonzero) crossed with distal-dendrite
length sweep on t0022</strong> (S-0029-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 `_silence_baseline_hoc_synapses` sets b2gnmda = 0 and installs single-component
AMPA-only E-I pairs, removing the Espinosa2010 AMPA/NMDA kinetic-tiling mechanism from the
testable space entirely. Espinosa2010 proposes that DSGC DS arises from different activation
time courses of AMPA and NMDA interacting with cable propagation delay - predicting
non-monotonic DSI-vs-length because NMDA's 50-150 ms time constant resonates with propagation
delay at specific lengths. Modify `_silence_baseline_hoc_synapses` to restore b2gnmda at 30%
of the 189347 baseline and rerun the 7-point length sweep. If DSI drops below 1.000 with
non-monotonic length dependence, kinetic tiling is a real third mechanism and the current null
result was partially a function of NMDA silencing. Requires a sibling library asset (clone of
t0022 with NMDA enabled) to preserve t0022's immutability. ~1 hour CPU plus ~1 hour coding.
Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>🔧 <strong>Re-implement placeBIP() to spatially gate gabaMOD by per-synapse
locx</strong> (S-0050-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0050-01` |
| **Kind** | technique |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0050_audit_syn_distribution/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0050 confirmed deposited PD/ND swap is a single global scalar gabaMOD = 0.33 + 0.66*direction
applied uniformly to every SAC inhibitory synapse with no spatial threshold
(dsgc_model_exact.hoc:316-334). Modify placeBIP() (or wrap it in a helper) so gabaMOD is
computed per synapse from each synapse's locx relative to the BIPsyn-locx median (88.77 um) or
soma_x (104.58 um), scaling up ND-side synapses and down PD-side synapses while preserving the
population mean. Re-run t0049's somatic SEClamp protocol to test whether somatic GABA recovers
an ND-bias toward paper Fig 3C (PD ~12.5 / ND ~30 nS, DSI ~ -0.41). This is the primary 'fix
path A' identified by t0050's mechanism analysis. Recommended task types: feature-engineering,
experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-run Bed B MOBO with tau_ca_multiplier upper bound increased
from [1, 20x] to [1, 200x] to test the slow-Kv AHP regime</strong>
(S-0078-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0078 high-DSI rail's PD ceiling at 2.86 Hz held flat across 109 acquisitions despite
optimiser exploration, the signature of a saturated negative-feedback loop. The 20x upper
bound corresponds to tau_ca ~ 100 ms; Larsson 2013 reports mammalian sAHP decay on the 1-3 s
timescale, equivalent to multiplier values of ~ 100-300x. The originally-proposed [1, 200x]
bound was reduced to [1, 20x] by researcher decision pre-launch as a simulation-budget safety
margin. Hypothesis: at multiplier > 20x the slow-Kv regime engages and may (a) free the PD
ceiling on the high-DSI rail or (b) not change behaviour (confirming saturation is
mechanistic, not parametric). Bundle with S-0078-01 if NSGA-II is run, or run as a focused
5-cell re-evaluation of t0078 high-DSI Pareto cells (iter 290, 283, 442, 371, 380) with
multiplier expanded to 200x. Cost: $0.20-$0.50 focused or rolled into S-0078-01. Recommended
task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-run t0046 figure sweeps at paper-N (12-19 trials per
condition, full 8-direction sweep)</strong> (S-0046-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

Re-execute every figure-reproduction sweep in t0046 (`code/run_all_figures.py`) at the paper's
reported N (12-19 trials per condition) and the full 8-direction sweep instead of the
wall-clock-budget-reduced 2-4 trials and PD/ND-only collapse used in t0046. This will (a)
tighten the SD bands on PSP and AP-rate distributions, (b) replace the `atan2(mean PD PSP,
mean ND PSP)` slope approximation with a fit to the 8-direction tuning curve as the paper
does, and (c) reveal the true Fig 7 0 Mg2+ ROC AUC instead of the small-N saturation at 1.00
(paper reports 0.83). Recommended task types: experiment-run.

</details>

<details>
<summary>📂 <strong>Real-cell DSGC morphology library from NeuroMorpho: test whether
observed morphologies escape prior-violation ceiling</strong> (S-0091-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-06` |
| **Kind** | dataset |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0091 confirmed HM-1 (morphology asymmetry necessary; symmetric anchor count = 0) but refuted
HM-2 (PD vs ND direction blind, p=0.331). The procedural 14-knob generator covers a parametric
box that biological DSGCs may or may not occupy; t0091's 57-cell Pareto stays inside that box
but cannot escape the channel-side prior-violation ceiling. Brainstorm 18 'Option G' is the
next move: build a NeuroMorpho.org-anchored real DSGC cell library (10-20 mouse / rabbit
reconstructions from Briggman 2011, Wei 2011, Morrie & Feller 2018), implement a categorical
selector + parametric deformation knobs (diameter scaling, branch pruning, soma offset), then
re-run t0091's NSGA-II with the real-cell library replacing the procedural generator. Tests
whether observed DSGC morphologies escape the prior-violation ceiling that procedural ones
cannot. Larger task: needs planning first. Cost ~$2-3 for the optimisation pass. Recommended
task types: download-dataset, build-model, write-library.

</details>

<details>
<summary>🧪 <strong>Rebuild ModelDB 189347 port on the calibrated Horton-Strahler
SWC from t0009</strong> (S-0008-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Replace the bundled 1-soma + 350-dend topology in RGCmodel.hoc with the calibrated SWC from
t0009 (6,736 compartments) and rewrite placeBIP()'s section-ordering-dependent synapse
placement. This was deferred in t0008 because the bundled HOC hardcodes 3D-point placement and
section indices. Outcome is a third variant of the port asset running on a morphology that
actually matches the measured dendritic diameter profile. Recommended task types:
code-reproduction.

</details>

<details>
<summary>📊 <strong>Redefine the ROC AUC negative class (off-direction or
jitter-isolated trials) so the metric does not saturate at 1.000</strong>
(S-0047-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0047 reproduces the paper's qualitative DSI-declines-with-noise shape across all three
conditions but ROC AUC saturates at 1.000 in every (condition, flickerVAR) cell. Root cause:
t0046's `_roc_auc_pd_vs_baseline` uses pre-stimulus baseline mean (5-6 mV above v_init) as the
negative class while PD PSP peaks (18-25 mV) dwarf baselines. Paper's Fig 7 shows AUC
declining toward 0.7 under noise. Concrete actions: (a) re-implement AUC using off-direction
(ND) PSP peaks as the negative class (PD-vs-ND PSP overlap framing); (b) alternatively sample
jitter-isolated trials as the no-stimulus distribution; (c) add unit tests on a synthetic
two-Gaussian distribution with controllable overlap. Recorded as discrepancy entry 15 in
t0047's catalogue. Once redefined, re-evaluate the t0047 noise-extension trial CSVs (96 trials
on disk) without re-simulating. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🔧 <strong>Reformulate NSGA-II with biological priors as additional
objectives or hard constraints</strong> (S-0091-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-05` |
| **Kind** | technique |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | [`10.1371_journal.pcbi.1002107`](../../../tasks/t0091_morphology_extended_nsga2_v1/assets/paper/10.1371_journal.pcbi.1002107/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0091 used 3-objective NSGA-II minimising (-DSI, -PD-rate, -robustness) with biological priors
applied as a post-hoc filter (0/57 Pareto cells pass). The optimiser drifts to the upper rail
of NMDA / NaP / GABA bounds without paying any cost. Reformulate as either (a) 4+ objective
NSGA-II adding worst-case prior-violation sigma as a fourth objective, or (b) hard-constrained
NSGA-II using pymoo's constraint handling with each prior as a g(x) <= 0 inequality. Hay 2011
is direct precedent for (a). Run a small-scale pass (pop=64, 4 gens, ~$1.00) on the t0091
substrate and compare the reformulated Pareto's biological-plausibility distribution against
t0091's post-hoc-filter Pareto. If the reformulated Pareto includes any biologically-plausible
joint-pass cells, the 'morphology cannot rescue priors' verdict was driven by formulation, not
substrate. Cost ~$1.00 on Vast.ai EPYC 7B13. Recommended task types: experiment-run,
build-model.

</details>

<details>
<summary>📚 <strong>Register SAC presynaptic drive model as an asset for downstream
DSGC input construction</strong> (S-0002-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-08` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1038_nature09818`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1038_nature09818/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Briggman2011 (SBEM wiring) and Ding2016 (cross-species comparison) supply the structural E/I
bias; Park2014 and Taylor2002 supply the 3-5x null/preferred IPSC amplitudes;
Sethuramanujam2016 adds ACh/GABA co-release; Hanson2019 challenges the pure SAC-asymmetry
model. Consolidate these findings into a pre-built SAC presynaptic drive asset (a reusable
library or dataset: angle-dependent GABA conductance time courses, AMPA time courses, and
their spatial distributions on a DSGC) so downstream DSGC simulation tasks do not each
re-implement the presynaptic waveform construction. The asset should expose a pure-function
API that takes (stimulus angle, velocity, asymmetry parameter) and returns per-synapse
conductance time courses. Recommended task types: write-library, feature-engineering.

</details>

<details>
<summary>📊 <strong>Render figure 7b -- 5-cell DSI+PD 2-obj NSGA-II Pareto panel
from t0104 once t0104 completes</strong> (S-0105-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-01` |
| **Kind** | evaluation |
| **Date added** | 2026-05-13 |
| **Source task** | [`t0105_preliminary_figures_report`](../../../overview/tasks/task_pages/t0105_preliminary_figures_report.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

REQ-9 (REQ-DEFERRED-PANEL) of t0105 was deferred because t0104_nsga2_2obj_dsi_pdrate_3seeds
was still in_progress. Once t0104 reaches status completed, render the figure-7 counterpart
(top-5 Pareto cells under DSI+PD 2-objective NSGA-II) using the same selection rule as figure
7a: filter pd_rate_hz >= 5.0 to drop silenced spurious-Pareto-anchor cells, then pick the top
5 by joint Pareto rank, and render a 2-panel mini-figure per cell (morphology schematic +
two-point polar tuning). Append the rendered panel as a new slide in t0105's
preliminary_figures_slides.pptx via a follow-up task (do not mutate t0105 -- create a new task
or a correction overlay). Reuse the renderer in
tasks/t0105_preliminary_figures_report/code/render_pareto_top5.py and read pareto-front JSON
from tasks/t0104_nsga2_2obj_dsi_pdrate_3seeds/results/data/. Priority: medium-high because it
gates presentation/report completeness. Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Repeat SEClamp Fig 3A-E re-measurement at exptype=2
(Voff_bipNMDA=1) for canonical-control baseline</strong> (S-0049-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0049 ran the SEClamp re-measurement at exptype=control (Voff_bipNMDA=0). t0048 established
that exptype=2 (Voff_bipNMDA=1, voltage-independent NMDA) is the paper-faithful canonical
control. Repeat the same 32-trial SEClamp sweep (2 directions x 4 channel-isolations x 4
trials at gNMDA = 0.5 nS, V_clamp = -65 mV) under exptype=2 to establish whether the residual
NMDA over-amplification (SEClamp PD 13.89 vs paper 7.0) and direction-asymmetry collapse
persist under voltage-independent NMDA. This locks the canonical SEClamp baseline alongside
the canonical exptype convention before downstream parameter-tuning work begins. Recommended
task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Repeat t0074 sweep on Bed B (de-Rosenroll DSGC)</strong>
(S-0074-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-08` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0074 covered Bed A only. Bed B (de-Rosenroll 2026, t0024 library) has different morphology,
different synapse placement, and a built-in Ca pool — meaning the channel-level findings here
may not generalise to Bed B. Repeat the same 25-condition × 12-angle × 5-seed sweep on Bed B.
Cost: same ~70 min compute as t0074. Comparison points: which channels remain inert; whether
NaP-induced DSI loss reproduces; whether SK_high HWHM narrowing reproduces (or is a
Bed-A-specific artefact); whether the with-cad baseline DSI shift seen in Bed A is also seen
in Bed B (where cad is native). This is a cross-substrate validation that strengthens any
conclusions drawn from t0074.

</details>

<details>
<summary>📊 <strong>Reproduce Poleg-Polsky 2016 Fig 1D/H subthreshold validation
targets (PSP amplitude, NMDAR slope angle)</strong> (S-0020-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-02` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0020_port_modeldb_189347_gabamod/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

compare_literature.md flags that the paper reports concrete subthreshold validation targets
that this task did not measure: PD NMDAR-mediated PSP component 5.8 +/- 3.1 mV and ND 3.3 +/-
2.8 mV (Fig 1D, n=19), and NMDAR multiplicative scaling slope angle 62.5 +/- 14.2 deg (Fig 1H,
additive baseline 45 deg). Extend the gabaMOD-swap driver to record somatic whole-cell voltage
traces (v_soma, not just spike count) across the 40-trial sweep, compute (1) the peak PSP
amplitude in a 0-200 ms post-stimulus window per condition and (2) the slope-angle regression
over a scan of AMPA vs NMDA drive ratios, then gate each against the paper's n=19 mean +/- SD
intervals. This turns a single spike-output check into a multi-level subthreshold validation
that exercises the cell's passive and NMDA-block biophysics independently of spike
thresholding. Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>📂 <strong>Reproduce the Park2014 mouse ON-OFF DSGC tuning-curve dataset
as a validation benchmark</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Park2014 (paper 10.1523_JNEUROSCI.5017-13.2014) and Chen2009 (paper
10.1113_jphysiol.2008.161240) are the two papers that set the mouse ON-OFF DSGC RQ5 targets
(DSI 0.6-0.9, peak 40-80 Hz, HWHM 60-90 deg). Park2014 is available open-access. Digitise the
published tuning-curve figure(s) into a reusable dataset asset (angle in degrees, spike rate
in Hz, error bars, cell counts) so the model can be scored against measured data rather than
only against the analytic target in t0004. This gives the project a literature-grounded
validation benchmark distinct from the canonical analytic target. Recommended task types:
download-dataset, data-analysis.

</details>

<details>
<summary>🧪 <strong>Rerun t0039 7-diameter sweep on t0024 for active-vs-passive
testbed comparison</strong> (S-0039-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0039 on t0022 at GABA=4 nS produced a passive_filtering signature (slope=-0.034, p=0.008).
Rerun the same 7-diameter sweep on t0024 (de_rosenroll_2026_dsgc, richer channel inventory,
AR(2) stochastic release) at its equivalent operational GABA level to test whether the
Schachter2010 concave-down signature emerges when active dendritic machinery is available. If
t0024 shows concave-down and t0022 shows monotonic decrease, that is the cleanest
testbed-level discrimination between the two mechanisms the project has produced. If both show
passive_filtering, that rules out Schachter2010 across the substrates the project has
available.

</details>

<details>
<summary>🧪 <strong>Resolve inhibitory conductance time-course via SEClamp on the
deposited cell</strong> (S-0065-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0065-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0065 IPSP_PASSIVE traces are flat at e_SACinhib = -60 mV because the cell sits at the
inhibitory reversal under no excitation. The voltage trace cannot reveal the inhibitory
conductance time-course; only a voltage clamp can resolve g_inh(t). t0049 already has SEClamp
infrastructure for this cell. Combining the t0065 channel-isolation pattern (zero excitatory
drives via b2gampa = b2gnmda = s2gach = achMOD = 0) with a SEClamp at -65 mV (or any
non-equilibrium voltage offset from e_SACinhib) would resolve the inhibitory conductance in nS
as a function of time, separately for PD (gabaMOD = 0.33) and ND (gabaMOD = 0.99). This is
essential for quantifying the differential shunting magnitude that drives FULL-mode DSI: the
integral of g_inh(t) should be ~3x larger in ND than in PD. Expected output: two conductance
time-courses showing g_inhibitory(t) over the 1000 ms trial in PD vs ND, with peak g_inh and
integrated charge per direction.

</details>

<details>
<summary>📊 <strong>Revisit envelope widening (DSI upper 0.85 to 0.9, peak lower 40
to 30 Hz) once real simulation results are in</strong> (S-0012-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

REQ-7 was satisfied by widening two envelope bounds away from the t0002 literature values: DSI
upper raised from 0.85 to 0.9 to admit t0004's DSI 0.8824, and peak lower lowered from 40 Hz
to 30 Hz to admit t0004's 32 Hz peak. This is explicit but anchored to the t0004 generator,
not to measured DSGC variability. After t0008 (ModelDB 189347) and the Na/K grid search
(S-0002-01) produce real simulated curves, re-evaluate: (a) re-parameterise t0004 so its curve
lands inside the literature envelope (reducing DSI_MAX from 0.9 to 0.83 would drop DSI to 0.8
and peak to about 37 Hz), or (b) formally widen the envelope with a citation justifying the
wider bounds. Deliverable: an answer asset recommending a resolution, with corresponding
corrections file. Recommended task types: answer-question, correction.

</details>

<details>
<summary>📚 <strong>Scaffold a NetPyNE `Batch` sweep harness for DSGC parameter
studies</strong> (S-0003-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-04` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Build a small library that wraps NetPyNE's `Batch` class with the project's preferred sweep
axes (morphology scale, channel densities, synaptic weights) and an Optuna backend. Output: an
`assets/library/` entry plus a one-page usage example. This unblocks every downstream
tuning-curve experiment that needs to run more than one parameter combination.

</details>

<details>
<summary>🧪 <strong>SEClamp inhibitory conductance measurement on de Rosenroll
cell</strong> (S-0066-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0066-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Voltage trace cannot resolve g_inh(t) when e_GABA = v_rest (zero current at rest regardless of
g). For the de Rosenroll cell specifically, combine the t0066 channel-isolation pattern (set
ach NetCon weights = 0; HHst zeroed) with a SEClamp at -65 mV (or any non-equilibrium offset
from e_GABA = -60). This will read inhibitory current in pA across the trial separately for PD
(gaba_release_prob = 0.05) and ND (gaba_release_prob = 0.80). Expected: the time-integrated
charge in ND should be ~3-16x larger than in PD depending on how synapse-level release prob
translates to mean conductance. Reuses t0049's SEClamp infrastructure (which was developed for
the deposited cell — would need a small port for the de Rosenroll synapse model). Parallel to
S-0065-03 for the deposited cell; together they give cross-model conductance benchmarks.

</details>

<details>
<summary>🧪 <strong>Single-compartment collapse of t0024 to test whether T4-style
geometry-nullity extends to DSGCs</strong> (S-0027-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Collapse t0024 (de Rosenroll 2026 port) to a single isopotential compartment that retains full
synaptic input drive and biophysics, and re-run the DSI-vs-speed protocol. Prediction
(creative_thinking.md #5): if T4-style geometry-nullity [Gruntman2018] extends to mammalian
DSGCs, the collapsed model reproduces full-model DSI-vs-speed; if the de Rosenroll local-DSI
mechanism is load-bearing, it fails. Cheapest of the five testbed experiments and a strong
null-hypothesis test for the necessity of dendritic geometry.

</details>

<details>
<summary>🧪 <strong>Single-objective scalarised BO comparison on the 49-d Bed B
substrate (qLogNEI with DSI - lambda x max(0, 10 - PD))</strong>
(S-0078-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | [`no-doi_Ament2023_logei-bo`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/no-doi_Ament2023_logei-bo/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Methodological comparison motivated by the t0078 Pareto-front geometry. The 17 t0078 Pareto
cells exhibit a clean monotonic concave-down DSI-vs-PD trade-off with no obvious knee,
suggesting cells lie on a 1-D manifold in 49-d parameter space. If true, scalarised
single-objective BO using qLogNoisyExpectedImprovement with `DSI - lambda x max(0, 10 -
PD_rate)` and lambda in [0.001, 0.01, 0.1, 1.0] could explore the same Pareto coverage at
O(N^2) instead of O(N^3) and complete 700 acquisitions within the $4 envelope. Run lambda scan
as 4 independent BO chains of 175 acquisitions each (total 700 cells) on the existing 49-d
substrate. Pass criterion: union of the 4 single-objective fronts achieves HV >= 11.41
(matching t0078) and ideally HV > 12.62 (1.5x rule-out). Document whether the scalarised front
crosses the joint pass criterion that t0078 missed. Cost: $1.00-$2.00 on Vast.ai 64-core CPU.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Spatial hot-spot analysis of Bed B GABA Bernoulli release vs
bar-arrival projection</strong> (S-0072-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0072-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0072's Example 9 single-synapse Bed B GABA peak (10.21 nS at synapse_idx=13, ND) is over 60x
the population mean peak (0.16 nS PD; 1.25 nS ND). The Bernoulli release model means most of
177 GABA terminals fire 0-1 events per trial; a handful of high-rate terminals near the bar's
arrival window summate to large momentary conductances. Test whether these hot-spots cluster
spatially: project each terminal's centroid onto the bar-projection axis (0 deg vs 180 deg),
bin into N=10 bands. For each band compute (a) Bernoulli release probability per trial
(analytic from _gaba_prob_for_direction sigmoid + AR(2) envelope), (b) realised mean peak g
from t0072 raw .npz, (c) band-mean to population-mean ratio. Plot peak-g-band vs
projected-distance for PD and ND. Expected: ND smooth gradient (high p engages all bands); PD
sharp leading-edge peak (low p only engages early-arrival terminals). Pure post-hoc on
existing data plus t0024 morphology; ~1 hour. Recommended task types: data-analysis.

</details>

<details>
<summary>📊 <strong>Specify primary DSI as t0033 optimiser objective on t0024
substrate (not vector-sum) and drop monotonic-length priors</strong>
(S-0034-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0034-07` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0034_distal_dendrite_length_sweep_t0024`](../../../overview/tasks/task_pages/t0034_distal_dendrite_length_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0034 establishes two facts that directly constrain the t0033 joint morphology+VGC optimiser
design: (1) primary DSI on t0024 has measurable dynamic range (0.545-0.774, spread 0.229,
p=0.038), so the optimiser CAN use primary DSI as the objective - no need to fall back to
vector-sum DSI as S-0030-06 proposed for t0022; (2) the DSI-vs-length curve is non-monotonic
with a net negative slope, opposite to Dan2018's monotonic-increase prior - the optimiser must
NOT assume longer distal dendrites yield higher DSI. Register as a t0033 planning correction:
pick t0024 as the optimisation testbed, use primary DSI as the objective, and seed the
length-axis initial distribution near 0.75x-1.0x (observed peak). Distinct from S-0030-06
(vector-sum DSI on t0022) - this clarifies that t0024 is the correct substrate. Recommended
task types: comparative-analysis, answer-question.

</details>

<details>
<summary>📊 <strong>Standardise hypervolume reference-point convention across t0076
/ t0078 / t0080 MOBO runs</strong> (S-0080-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0080's `nsga2_loop.py` uses `utopia_point = (0.7, 80)` for HV scaling; t0076 and t0078 used
`[0, 0]` reference points. HV values across the three tasks are on different scales and not
directly numerically comparable, breaking cross-task progress narratives. Pick a single
convention (recommended: reference point [0, 0] matching the t0076/t0078 baseline;
alternative: nadir-based reference point recomputed per run) and document it in a project
methodology note. Re-compute HV on the t0080 stored cells under the chosen convention and
amend `results/metrics.json` via a correction. Apply the convention prospectively to all
future MOBO tasks. No new compute needed. Recommended task types: data-analysis,
infrastructure-setup.

</details>

<details>
<summary>🧪 <strong>Stricter AMPA escape range (gAMPA in {5, 7, 10} nS) and sub-0.1
nS bar-locked GABA on t0059 substrate</strong> (S-0059-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0059-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0059 sweep limits gAMPA to {0.5, 1.0, 2.0, 3.0, 4.0} nS (trimmed from 5 nS by researcher
decision). The compare-literature Limitations section flags the diminishing-returns shape
suggests extending to 6-10 nS is unlikely to break the multi-spike wall but should be
confirmed. Symmetrically, 10 of 25 cells already at GABA_BASE_NS = 0.10 nS show no escape, but
sub-0.1 nS values (0.025, 0.05) were not tested. Fork minimal_dsgc_bar_locked_gaba_ampa_sweep,
run gAMPA in {5.0, 7.0, 10.0} nS x GABA_BASE_NS in {0.025, 0.05, 0.10} nS (9 cells, 3240
trials). Pass criterion: locate at least one operating point with peak Hz >= 5 Hz AND
vector-sum DSI > 0.3, OR confirm the 4 nS / 0.1 nS ceiling rules out the AMPA-only path on
this substrate. Lowest-cost extension of the t0059 sweep on already-validated machinery.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Stricter centripetal-gating threshold sweep (cos < -0.5, -0.7) to
halve active-fraction on t0053</strong> (S-0053-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0053's centripetal-gating rule fires every I synapse whose centrifugal vector is anywhere on
the bar-incoming hemisphere (cos(theta_stim - theta_centrifugal) < 0), giving a roughly 50%
active fraction averaged over directions and a 0.34-0.66 per-direction spread. With 2 nS GABA
per active synapse this is enough to fully suppress spiking. Tighten the threshold to T in
{-0.3, -0.5, -0.7, -0.866} so only synapses whose centrifugal vector is within (90 - acos|T|)
of being directly anti-aligned with the bar fire. T = -0.5 reduces mean active fraction to
~0.33; T = -0.866 to ~0.17. Re-run the 12-direction x 10-trial FULL sweep at fixed 2 nS GABA
per synapse and report peak Hz, DSI, HWHM, active-fraction polar curve, and aggregate IPSP per
T. Goal: test whether a stricter threshold recovers a measurable DSI without changing
per-synapse conductance, isolating the active-fraction-vs-amplitude contributions to
suppression. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Sub-0.25 nS tonic GABA finer sweep on t0057 to test
graded-suppression hypothesis</strong> (S-0057-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0057-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0057 swept GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0} nS and found a binary regime: gaba <=
1.0 nS produces uniform 0.667 Hz single-spike-per-trial (tonic too weak to override AMPA
spike) and gaba >= 1.5 nS produces 0 Hz full suppression. The sub-0.25 nS regime is
uncharacterised and may host a graded-suppression operating point where the tonic envelope
partially vetoes the AMPA spike on subset of trials, producing a probabilistic firing-rate
signal that could carry direction information. Run a finer sweep at GABA_BASE_NS in {0.05,
0.10, 0.125, 0.15, 0.175, 0.20, 0.225} nS on the t0057 minimal_dsgc_tonic_gaba_sweep library
at 12 directions x 10 trials x 3 modes (2520 trials, ~75 min wall-clock). Pass criterion:
identify any conductance with FULL-mode peak Hz != null Hz (i.e., non-degenerate primary DSI),
or rule out the existence of such a graded operating point in the sub-AMPA-spike-veto regime.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Substrate regression check: re-evaluate t0076 iter-424 parameters
on the AIS-augmented 49-d Bed B substrate</strong> (S-0078-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Closes the t0078 deferred REQ-16. The compare_literature step flagged a substrate regression:
iter 81 on the augmented substrate produces DSI 0.316 vs t0076 iter-424's DSI 0.42 at
comparable PD rate, but no t0076 parameter vector was ever evaluated on the augmented
substrate. Without this check we cannot disentangle (a) substrate regression of high-rail DSI
from (b) qLogNEHVI 49-d exploration not finding t0076's best-joint operating point in 491
cells. Cheap: 1 cell x 8 dirs x 20 seeds at TSTOP_MS 1400 is ~50 s on local CPU. Re-run
_worker_run_trial with the t0076 iter-424 vector extended to 49-d (tier-stratified channels at
uniform t0076-matching values, AIS Nav at Kole prior centre 0.375 S/cm^2, AIS geometry at
midpoint, tau_ca_multiplier=1). Pass criterion: reproduce DSI within +/- 0.05 of t0076's 0.42
at PD ~ 8.34 Hz, or document substrate regression delta. Cost: < $0.05 local CPU or
$0.05-$0.10 Vast.ai. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Surface-density-rescaled Nav diameter sweep on t0024 to test
surface-vs-volume compensation</strong> (S-0035-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Re-run a small diameter sweep (0.5x, 1.0x, 2.0x) on the t0024 DSGC with gnabar_HHst rescaled
by 1/d in the distal compartments so the total per-section Nav count is held fixed as diameter
varies. Creative_thinking hypothesis 2 proposes that the flat DSI-vs-diameter result (t0035)
arises because NEURON's surface-density gbar scales total channel current by d while axial
load scales by d^2, cancelling the net effect. If density rescaling produces a non-flat DSI
trend, the compensation confound is confirmed; if still flat, rule out this hypothesis.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Sustained-envelope gabaMOD on t0052 minimal scalar architecture
(tonic-mechanism back-port)</strong> (S-0057-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0057-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0057 introduced a sustained (1300 ms) tonic envelope on the t0053 spatial substrate; the
back-port question is whether applying the same envelope to t0052's scalar gabaMOD inhibition
(graded amplitude, all 100 synapses fire) breaks t0052's binary single-spike DSI usefully.
Build a t0052 variant that replaces per-event Exp2Syn(rise=1, decay=20 ms) inhibition with a
sustained gabaMOD-envelope using gaba_tonic.mod from t0057, holding g(theta) = gabaMOD(theta)
* GABA_BASE_NS over (t_on, t_off) = (100, 1400) ms per synapse. Sweep GABA_BASE_NS in {0.05,
0.1, 0.25, 0.5, 1.0, 2.0} nS at gabaMOD_PD = 0.33, gabaMOD_ND = 0.99 (matching t0052). Run 12
dir x 10 trials x 3 modes per conductance (2160 trials, ~2 h). Pass criterion: identify a
GABA_BASE_NS where FULL-mode peak Hz is non-zero AND primary DSI is non-degenerate, or rule it
out. Decomposes inhibition-envelope-shape from spatial-pattern. Recommended task types:
build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>Swap bipolar-cell sustained vs transient kinetics on t0024 to
discriminate kinetic tiling from cable delay</strong> (S-0027-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Run t0024 (de Rosenroll 2026 port) with bipolar-cell kinetic identities swapped: assign
sustained kinetics to distal terminals and transient kinetics to proximal terminals, opposite
to the wild-type tiling. Prediction (creative_thinking.md #2): if [Srivastava2022]
kinetic-tiling is causally responsible for SAC DS, the swap reverses preferred direction; if
[Kim2014] cable delay is causal, the swap only reduces DSI magnitude without flipping
preferred direction. Critical for choosing between two competing centrifugal-DS mechanisms
before committing to a morphology sweep design.

</details>

<details>
<summary>🧪 <strong>Sweep AR(2) rho x V_rest for t0024 to separate noise correlation
from depolarisation effects</strong> (S-0026-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0024 V_rest sweep ran only at rho=0.6 and showed a 1.9x U-shaped DSI curve with HWHM
pinned at 65-83 deg. Repeat the sweep at rho in {0.0, 0.3, 0.6, 0.9} to test whether the
tuning-smoothing is dominated by AR(2) correlation or by the depolarisation itself. Expected
outcome: rho=0.0 should recover tuning sharpness closer to t0022 while preserving the
Na-inactivation-independent peak firing behaviour.

</details>

<details>
<summary>🧪 <strong>Sweep bar velocity x V_rest on both DSGC ports to test
velocity-V_rest interaction</strong> (S-0026-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | [`10.1113_jphysiol.2010.192716`](../../../tasks/t0026_vrest_sweep_tuning_curves_dsgc/assets/paper/10.1113_jphysiol.2010.192716/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Sivyer2010 reports DSI varies with velocity (0.45-0.57) at natural V_rest. Our current sweep
fixed velocity at the t0022/t0024 defaults. Repeat the 8-value V_rest sweep at 3-5 bar
velocities to check whether V_rest modulates the velocity-tuning curve or only the
direction-tuning curve. Expected runtime: ~4x current (t0022) and ~4x current (t0024) if 4
velocities are tested.

</details>

<details>
<summary>🧪 <strong>Synaptic noise (NetStim jitter + AR(2) correlated release) on
t0059 substrate for trial-to-trial DSI characterisation</strong>
(S-0059-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0059-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-29 |
| **Source task** | [`t0059_bar_locked_gaba_ampa_sweep_t0057`](../../../overview/tasks/task_pages/t0059_bar_locked_gaba_ampa_sweep_t0057.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0059 has reliability = 1.0 across all FULL cells because each NetStim emits a single
deterministic event per direction. deRosenroll2026 [p. 6] requires AR(2) correlated release
with rho = 0.6 to match in vitro DSGC reliability and reaches vector-sum DSI = 0.39 (3.1x our
0.209). Determinism may be the dominant DSI suppressor. Fork
minimal_dsgc_bar_locked_gaba_ampa_sweep, add (1) per-trial NetStim noise = 0.1 (~1 ms jitter)
on each AMPA and tonic-GABA driver, then (2) implement the deRosenroll2026 AR(2) correlated
release schedule (rho in {0.0, 0.6}, n=20 trials per direction). Operate at the t0059 optimum
(gAMPA=1.0/gaba=0.10) across 4 noise cells. Pass criterion: vector-sum DSI > 0.3 in at least
one noise configuration, OR rule out with CIs over n=20 trials. Recommended task types:
build-model, experiment-run.

</details>

<details>
<summary>🧪 <strong>Synaptic re-tuning: scale s2ggaba up proportionally with Nav1.6
density</strong> (S-0068-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0068-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0068 makes clear that channel-level rescue may not be possible — the GABA shunt's leverage is
fundamentally bounded when Nav1.6 boosts the depolarising drive. The natural alternative is to
scale the GABA conductance up proportionally. Test: at Nav1.6_med (s2ggaba x 1.5x, 2.0x, 3.0x)
and Nav1.6_high (s2ggaba x 1.5x, 2.0x, 3.0x). Hypothesis: a coordinated 2x synaptic upscale
restores DSI to baseline. This isn't a 'rescue' in the channel-pharmacology sense, but it
shows what would be required to compensate for a Nav-side gain change at the network level —
relevant for understanding RGC robustness to channel-density variation. Implementation: 1-line
patch to t0065's apply_params, then 6 conditions x 2 directions x 5 seeds = 60 trials, ~3 min.

</details>

<details>
<summary>🧪 <strong>Targeted morphology sweep around the high-DSI region of the
seed-55 Pareto front</strong> (S-0104-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0104-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Hold the seed-55 best-DSI cell's 54-d electrophys subvector fixed and sweep the 14-d
morphology subvector across a Latin-Hypercube sample of ~200 cells, all evaluated at
N_EVAL_SEEDS = 4 with the DSI guard active. The question: does the high-DSI cell's electrophys
signature generalise across morphologies, or is the DSI = 0.54 reading specific to one
parametric tree topology? If DSI stays above 0.4 across most morphologies, the electrophys
subvector is the lever and morphology is secondary; if DSI collapses, the seed-55 cell is a
morphology-specific lucky draw. Recommended task types: experiment-run, comparative-analysis.
Cost: ~$2-3 (200 cells x N=4, no GA overhead, single Vast.ai instance for ~6 hours).

</details>

<details>
<summary>🧪 <strong>Test M-current (KCNQ / Kv7) co-expression with Nav1.6</strong>
(S-0068-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0068-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Another rescue candidate: M-current is a slowly-activating, non-inactivating K+ current with
V_half around -40 to -45 mV. Unlike Kv3 it doesn't repolarise fast APs; it provides a tonic
outward current that opposes sustained depolarisation. In a Nav1.6-driven high-firing regime,
M-current would provide steady hyperpolarisation that reduces the cell's mean depolarisation,
possibly restoring the regime where the GABA shunt has more leverage. Implementation: write a
simple m^1 MOD with V_half = -45 mV, tau ~50 ms, sweep at Nav1.6_med + Nav1.6_high.

</details>

<details>
<summary>🧪 <strong>Test whether a Larkum-style Ca2+ plateau zone can be localised
in DSGC dendritic trees</strong> (S-0016-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0016-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0016_literature_survey_dendritic_computation`](../../../overview/tasks/task_pages/t0016_literature_survey_dendritic_computation.md) |
| **Source paper** | [`10.1038_18686`](../../../tasks/t0016_literature_survey_dendritic_computation/assets/paper/10.1038_18686/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

The answer asset identifies the cortical-style Ca2+-plateau initiation zone (Larkum 1999) as a
plausible but uncertain motif for DSGCs (caveat: DSGC dendritic trees lack the tuft / basal
two-compartment layout of cortical pyramidals). Build a compartmental DSGC model with
spatially-varying L-type / T-type Ca2+-channel densities to identify candidate initiation-zone
compartments, then test whether asymmetric inhibition at principal-branch bifurcations can
selectively enable Ca2+ plateaus during preferred-direction motion and suppress them during
null-direction motion. Report preferred-direction burst firing rate versus null-direction
burst rate and compare with published DSGC spiking statistics.

</details>

<details>
<summary>🔧 <strong>Transfer-learning surrogate warm-start from t0022 and t0024
V_rest-sweep evaluations</strong> (S-0033-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-04` |
| **Kind** | technique |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Creative-thinking alternative #3 in t0033 noted that t0022, t0024 and the t0026 V_rest sweep
already produced thousands of (gbar-subset, DSI) evaluations on the 16-parameter HHst
topology. If half of the 5,000-sample surrogate training burn is replaced by these as
warm-start, the $41.56 training cost plausibly drops to ~$20, pulling the recommended cell to
~$30. Build a task that (a) reads t0026 V_rest-sweep and t0022 baseline outputs, (b) encodes
them as (parameter-vector, DSI) tuples in the 25-dim joint space by imputing the 9 unvaried
dimensions at Poleg-Polsky defaults with tagged uncertainty, (c) pre-trains the surrogate NN
on this warm-start set before the 2,500-sample cold-start burn, and (d) measures whether the
half-dataset warm-start matches the 5,000-sample cold-start surrogate. Recommended task types:
experiment-run, feature-engineering.

</details>

<details>
<summary>📊 <strong>Trial-count power analysis for the PD/ND DSI estimator (bootstrap
CI vs N_trials)</strong> (S-0020-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0020 reports DSI 0.7838 from 20 trials per condition but quotes no confidence interval.
Before launching sensitivity sweeps (S-0020-01, S-0020-03), future tasks need to know how many
trials per condition are needed to resolve, say, a 0.05-DSI difference at 95% CI. Compute
bootstrap 95% CIs on DSI for N_trials per condition in {5, 10, 20, 40, 80} by resampling with
replacement (10,000 resamples) from a single long run (80 trials per condition, reusing
run_gabamod_sweep.py with --n-trials 80). Output: (1) a CSV
trial_count,dsi_mean,dsi_ci_low,dsi_ci_high,peak_mean,peak_ci_low,peak_ci_high; (2) a plot of
DSI CI width vs trial count; (3) a recommended N_trials for each sensitivity-analysis budget
tier. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Unblock t0023 Hanson 2019 port so REQ-6 cross-comparison can
include 5/5 DSGC models instead of 4/5</strong> (S-0024-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.7554_eLife.42392`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.7554_eLife.42392/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0024 step 12 records t0023_port_hanson_2019_dsgc as intervention_blocked
(intervention/deferred_pending_t0022.md). The t0022 task has since completed (DSI 1.000, HWHM
116.25, RMSE 10.48) so the original blocking dependency is resolved. Triage t0023's
intervention file, resume the port, and then retrofit a Hanson 2019 row into the cross-model
comparison table in results_detailed.md of both t0024 and any subsequent DSGC port. Closes the
REQ-6 partial-coverage caveat.

</details>

<details>
<summary>🔧 <strong>Update t0033 optimiser headroom estimate to reflect narrow (0.06
DSI) morphology dynamic range on t0022</strong> (S-0039-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-05` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0039 shows the t0022 discriminator's total DSI spread across a 4x diameter range is only
0.061 (0.368 to 0.429). Any pure-morphology optimiser running at GABA=4 nS on t0022 has a
ceiling of 0.429 (the 4 nS saturation value). If t0033's planned optimiser is scoped to
maximise DSI via morphology alone, the maximum achievable lift from the baseline is ~0.06 -
the headroom is much smaller than originally planned. Consider adding a channel-density
dimension to the optimiser search space, since DSI has more potential room through Nav/Cav
density than through morphology alone.

</details>

<details>
<summary>🧪 <strong>Voff_NMDA = 1 ablation on t0055 architecture as a controlled
regression vs voltage-dependent (Voff = 0) Mg-block</strong> (S-0055-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0055 NMDA_MgBlock.mod has a Voff parameter (default 0 = voltage-dependent) that, when set
to 1 with Vset = -60, fixes the Mg factor at a constant value and effectively reproduces the
t0054 voltage-independent regime within the new MOD. Re-run the gNMDA = {0, 0.25, 0.5, 1.0} nS
sweep with Voff = 1 to confirm: (a) DSI collapses to ~0.082 at gNMDA = 0.25 (matching t0054
within rounding), (b) peak Hz does NOT remain at 0.667 Hz in FULL mode (NMDA contributes,
unlike t0055 Voff = 0 case). This isolates the Mg-block voltage-gating as the sole cause of
the t0055 NMDA-inert behavior and gives a controlled within-task ablation. Pass criterion: DSI
at gNMDA = 0.25, FULL with Voff = 1 matches t0054 within +/-0.05; peak Hz exceeds 0.667 Hz at
gNMDA >= 0.25. Recommended task type: experiment-run.

</details>

<details>
<summary>🧪 <strong>Widen soma_offset_pd_um morphology bound from [-150, +150] to
[-200, +200] um and re-run 2-direction NSGA-II</strong> (S-0106-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

35 of t0106's top 50 cells cluster at soma_offset_pd_um in [-132, -107] um. The morphology
generator's lower bound is -150 um. NSGA-II is pushing toward the bound, suggesting the true
optimum may sit beyond it. Re-run the 2-direction NSGA-II configuration (pop = 96,
N_EVAL_SEEDS = 3, n_gen = 40, single GA seed) with soma_offset_pd_um widened to [-200, +200]
um, all other bounds fixed. If the current bounds were extracted from real DSGC
reconstructions in t0091, document the biological plausibility of the wider bound before
launching. Decision: if median soma_offset for top 50 falls below -150 um, the prior bound was
capping the optimum and a downstream task should reground the bound in measured DSGC anatomy.
If the population remains within the prior bound, the cluster at [-132, -107] um is the true
substrate optimum. Recommended task types: experiment-run, comparative-analysis. Cost: ~$10.

</details>

<details>
<summary>🧪 <strong>Wider distal-diameter sweep (0.25x to 4.0x) after the schedule
fix to probe extreme impedance regimes</strong> (S-0030-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0030 sweep used multipliers 0.5x-2.0x (a 4x range) and found vector-sum DSI moved by only
0.030 absolute, with Wu2023 reporting distal-diameter DSI saturation above ~0.8 um on primate
SAC - our baseline distal seg.diam straddles that threshold so our sweep likely sat in the
saturated regime throughout. Once the S-0030-01/S-0030-02 schedule fix has removed the DSI
ceiling, rerun the diameter sweep over a wider range {0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0,
4.0}x at the same 12-direction x 10-trial protocol. Provides the impedance-gradient dynamic
range Schachter2010's 5-7x proximal-to-distal input-resistance measurement implies, and tests
whether Wu2023's saturation threshold applies to mouse ON-OFF DSGC. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Wire Exp2NMDA into Bed B's tuning-curve and EPSP/IPSP/FULL
drivers and re-run t0066</strong> (S-0070-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0070-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0070 writeup confirms Bed B vendors `Exp2NMDA.mod` (103 lines) and parameterises NMDA in
`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L57-L61` (NMDA_TAU1_MS=2,
NMDA_TAU2_MS=7, NMDA_E_MV=0, NMDA_N_PER_MM=0.25, NMDA_GAMA_PER_MV=0.08, NMDA_WEIGHT_US=0.0015)
but `_setup_synapses` (`run_tuning_curve.py:L189-L226`) never instantiates an Exp2NMDA point
process. Bed A always runs with NMDA, Bed B never does. Project literature (Poleg-Polsky 2016,
t0048, t0054, t0055, t0057) identifies voltage-dependent NMDA Mg-block as a critical
multiplicative-gain mechanism for DS. Extend `_setup_synapses` to place one Exp2NMDA per
terminal dendrite paired with the existing Exp2Syn ACh, wire it into the Poisson event queue,
and re-run the t0066 EPSP/IPSP/FULL protocol with NMDA on vs off. Report DSI, peak Hz, and
EPSP/IPSP envelope changes. Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Write forward-only driver for PolegPolsky2026 DS-mechanisms model
and pursue LICENSE</strong> (S-0010-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0010-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0010_hunt_missed_dsgc_models`](../../../overview/tasks/task_pages/t0010_hunt_missed_dsgc_models.md) |
| **Source paper** | [`10.1038_s41467-026-70288-4`](../../../tasks/t0010_hunt_missed_dsgc_models/assets/paper/10.1038_s41467-026-70288-4/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

PolegPolskyLab/DS-mechanisms ships only a GA-training harness (numGen=300, popSize=50) and has
no LICENSE file, which blocks library-asset registration under this project's rules. A
follow-up task should (a) email the authors to request a LICENSE addition, and (b) extract a
single-parameter-set forward-only 'simulate at angle theta' driver from the GA inner loop so
the model can be scored against the canonical 12-angle sweep without running the full GA.

</details>

<details>
<summary>📊 <strong>Zero-cost meta-analysis of primary-DSI vs vector-sum-DSI
discrepancy across t0029, t0030, t0034, t0035</strong> (S-0035-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Combine metrics.json outputs from all four completed morphology sweeps (t0029 length t0022,
t0030 diameter t0022, t0034 length t0024, t0035 diameter t0024) into a single cross-task table
correlating primary DSI against vector-sum DSI. Key questions: when primary DSI is flat or at
ceiling, does vector-sum DSI pick up signal? Does the rank-order of variants agree between the
two metrics? This supports the t0033 optimiser choice and a standing evaluation-methodology
recommendation (compare against S-0029-07, S-0030-06, S-0034-07). No simulations needed; pure
re-analysis of existing CSVs. Recommended task types: data-analysis.

</details>

## Low Priority

<details>
<summary>🧪 <strong>12-angle EPSP/IPSP/FULL tuning curve on de Rosenroll
cell</strong> (S-0066-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0066-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0066 only tested PD (0°) and ND (180°). The de Rosenroll model's bar-geometry direction
encoding produces continuous tuning across angles. Running EPSP_PASSIVE / IPSP_PASSIVE / FULL
at all 12 angles (0°, 30°, 60°, ..., 330°) would produce an EPSP/IPSP decomposition for the
entire tuning curve, showing how the bar-geometry contribution to direction sensitivity
(visible as ~1.6 mV PD-vs-ND difference in EPSP_PASSIVE) varies with angle. Most informative
for: identifying the angle where the bar-geometry contribution maximises (probably ~90° from
preferred), and characterising whether the GABA shunt-driven DS scales linearly across angles
or has a threshold. Sweep cost: 12 angles x 3 modes x 20 trials x ~30 s/trial = ~6 hours.
Could parallelise across CPU cores (each angle independent) to reduce wall-clock to ~1.5
hours.

</details>

<details>
<summary>🧪 <strong>20-generation single-seed random-init NSGA-II to test whether
longer search bridges the joint-pass gap</strong> (S-0099-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0099-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-10 |
| **Source task** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0099 capped at 8 gens per seed. Hay 2011 used 1000 gens for similar problems. Test: one
random-init seed at 20 gens with $10 cap to see if random-init can eventually bridge the
joint-pass corner that warm-start reached at gen 2. If yes, warm-start was a 10x speedup not a
fundamental enabler. If no after 20 gens, warm-start remains essential. Cost ~$10 single seed.

</details>

<details>
<summary>📂 <strong>Add a Poisson-noise variant of the target trials</strong>
(S-0004-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0004-02` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0004_generate_target_tuning_curve`](../../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Replace the current Gaussian-noise trial replicates with Poisson counts converted to rates
(Fano factor ~1) and register it as a separate dataset asset. This would give
tuning_curve_reliability a noise model closer to real spike statistics while keeping the
closed-form mean curve unchanged.

</details>

<details>
<summary>🔧 <strong>Add preferred-direction GABA asymmetry to t0022 (cartwheel SAC
offset)</strong> (S-0037-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-06` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0022 applies only null-direction GABA. Published DSGC models (Park2014, Schachter2010)
include a directionally-offset SAC inhibition where preferred-direction trials see much lower
GABA than null. Implement the cartwheel asymmetry as a new parameter
`GABA_CONDUCTANCE_PREF_NS` (probably 0-1 nS based on t0037's over-excitation regime below 2
nS), and measure whether primary DSI improves toward the 0.5-0.6 Park2014 centre. This moves
t0022 closer to the canonical DSGC E-I motif rather than relying on a single null-only scalar.

</details>

<details>
<summary>📊 <strong>Cross-validate compute_reliability against independent split-half
implementations (odd-even, bootstrap, Spearman-Brown)</strong> (S-0012-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0012-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0012_tuning_curve_scoring_loss_library`](../../../overview/tasks/task_pages/t0012_tuning_curve_scoring_loss_library.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

compute_reliability implements one split-half estimator: partition trials into even/odd
indices, per-angle means, Pearson r, clamped to [0, 1]. Canonical alternatives differ in
defensible ways: (a) random-draw split rather than parity, (b) Spearman-Brown prophecy
correction to project split-half r back to full-length reliability, (c) Spearman rank
correlation for ordinal robustness, (d) bootstrap resampling to produce a confidence interval.
Build compute_reliability_variants returning all four on the same TuningCurve, run it on
t0004's trials.csv and downstream simulated trials, and write an answer asset documenting
where the estimates agree or diverge. If a variant is systematically preferred for our
approximately 20 trials per angle, promote it to the default via a corrections-aware revision.
Recommended task types: comparative-analysis, answer-question.

</details>

<details>
<summary>🧪 <strong>Eight-direction EPSP/IPSP/FULL tuning curve on the deposited
cell</strong> (S-0065-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0065-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0065 only tests gabaMOD = 0.33 (PD) and 0.99 (ND). The Poleg-Polsky 2016 paper has a smooth
tuning curve over 8 directions, which the deposited model simulates by sweeping gabaMOD across
[0.33, 0.99]. Running EPSP_PASSIVE / IPSP_PASSIVE / FULL at all 8 directions would produce an
EPSP/IPSP decomposition for the entire tuning curve, not just the two anchor points. Most
informative for understanding how shunting modulates the EPSP envelope at intermediate
directions: does the relationship between gabaMOD and FULL-mode envelope compression scale
linearly, or is there a threshold around gabaMOD ~ 0.6 where the cell transitions from spiking
to non-spiking? Sweep cost: 24 trials (3 modes x 8 directions x 1 seed) ≈ 75 s. Expected
output: 24-trial dataset with gabaMOD-modulated tuning curve in spike counts and the
corresponding (constant) EPSP_PASSIVE and (constant-flat) IPSP_PASSIVE traces.

</details>

<details>
<summary>📊 <strong>Email the Feller lab to map the 141009_Pair1DSGC session to a
specific pair in Morrie & Feller 2018 CB</strong> (S-0013-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0013-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0013_resolve_morphology_provenance`](../../../overview/tasks/task_pages/t0013_resolve_morphology_provenance.md) |
| **Source paper** | [`10.1016_j.cub.2018.03.001`](../../../tasks/t0013_resolve_morphology_provenance/assets/paper/10.1016_j.cub.2018.03.001/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The provenance decision in this task (source_paper_id = 10.1016_j.cub.2018.03.001) is grounded
in methodological consistency plus the NeuroMorpho.org curated attribution, not in an
exact-quote match: Morrie & Feller 2018 CB does not literally print 141009, Pair1DSGC,
biocytin, or Neurolucida in its Methods, and the paper publishes only SAC (not DSGC)
reconstructions. A downstream task should email the Feller lab (Murphy-Baum at
murphy-baum@berkeley.edu or Morrie at rmorrie@berkeley.edu) asking which specific paired
recording in the paper's Figure 2 cohort (n = 12 Control + 9 Sema6A-/- null + 6 Sema6A-/-
preferred) produced the 141009_Pair1DSGC reconstruction, and whether the companion SAC
reconstruction is deposited at NeuroMorpho. A one-sentence email-reply quote converts the
current 'methodologically consistent' attribution into a citeable exact-quote provenance, and
directly informs S-0013-03. Recommended task types: answer-question.

</details>

<details>
<summary>📚 <strong>Extend t0011 response-visualisation library with a
condition-based (PD/ND) raster+PSTH plot</strong> (S-0020-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0020-07` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0020_port_modeldb_189347_gabamod`](../../../overview/tasks/task_pages/t0020_port_modeldb_189347_gabamod.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0011's tuning_curve_viz library supports angle-based rasters (one column per angle) but the
two-condition CSV produced by t0020 has no angle axis; only the bar chart (plot_pd_vs_nd.py,
t0020 local code) currently visualises it. Extend t0011 with
plot_condition_raster_psth(spike_times_df, *, conditions=('PD','ND'), out_png) that draws a
two-column raster (one per condition) above a PSTH panel. Requires t0020 (or a follow-up) to
first record per-trial spike times (not just rates) from run_gabamod_sweep.py. Complements
S-0011-01 (angle-based raster on the rotation-proxy port); this is the condition-based
analogue for the native-protocol port. Once merged, back-apply to t0020's existing sweep to
produce a publication-quality raster. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🧪 <strong>Generate per-direction Vm-trace deep-dive PNGs for the three
closest-to-joint t0078 Pareto cells (iter 81, 320, 290)</strong>
(S-0078-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

REQ-14 partial: the t0078 plot_pareto.py was run with --skip-deep-dives because the t0078 MOD
library was not compiled on the local Windows machine. The per-direction Vm-trace deep-dive
PNGs are needed to (a) interpret the iter-81 closest-to-joint cell mechanistically, (b)
document the iter-290 max-DSI sub-threshold extreme, and (c) inspect the iter-320 high-PD-rate
cell that misses joint pass on DSI only. Re-run plot_pareto.py with the existing 49-d
substrate library on a fresh Vast.ai 16-core CPU instance (~$0.05/hr, < 30 min total) or
compile the 13 t78 MOD files locally on the researcher's Windows machine. Output: 3 deep-dive
PNGs (one per cell) with 8 per-direction Vm traces from soma + AIS distal + 3 dendritic
recording sites. Cost estimate: < $0.10 (Vast.ai small instance) or zero (local). Recommended
task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Investigate biological NaP overexpression as a
directional-selectivity disorder model</strong> (S-0067-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0067-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0067 showed that NaP at 2.4 mS/cm² INVERTS direction selectivity in the deposited DSGC.
Persistent sodium currents are dysregulated in several pathologies: epilepsy (SCN1A
gain-of-function increases NaP), motor neuron disease (NaP downregulation in ALS), and chronic
pain (NaP upregulation in DRG neurons). Survey the literature for clinical/preclinical reports
of altered NaP in retinal pathologies or DSGCs specifically. If found, this t0067 finding
becomes a candidate computational model for a real disease state. Output: an answer asset
summarising the literature on NaP dysregulation in DSGCs / retinal disease.

</details>

<details>
<summary>🧪 <strong>Investigate whether the t0069 NaP_high AIS effect (DSI = 0.22)
is robust to AIS geometry</strong> (S-0069-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0069-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

NaP at high density on the AIS gave the largest signal (-0.78 ΔDSI), 80% of the soma version's
effect. Persistent Na is interesting because it survives the AIS+axon's electrical sink — its
non-inactivating depolarisation accumulates over the trial duration, so even a small AIS can
pump enough current. Question: does the AIS NaP effect scale predictably with AIS geometry, or
does it saturate? Test NaP at {1.0, 1.5, 2.4, 3.5, 5.0} mS/cm² on AIS at fixed (L=30 μm,
diam=1 μm); also test 2.4 mS/cm² at diam ∈ {0.5, 0.7, 1.0, 1.5} μm. Hypothesis: NaP gnabar ×
AIS surface area ≈ constant for a fixed DSI effect (i.e., the cell sees the integrated NaP
current). 9 conditions × 2 directions × 5 seeds = 90 trials, ~5 min.

</details>

<details>
<summary>📊 <strong>Multi-replicate Sobol seed and BO chain replication to estimate
Pareto-front HV uncertainty on the 49-d substrate</strong> (S-0078-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The t0078 +36% HV improvement over t0076 (8.41 -> 11.41) is a single-replicate observation:
one Sobol DoE seed, one BoTorch chain. The Pareto-front structure (17 cells, bimodal
trade-off) and the hypervolume value may shift materially with a different RNG seed. Run 3-5
independent Sobol seeds + qLogNEHVI chains (75 Sobol + 100 acquisitions each, smaller budget
per replicate) on the same 49-d substrate to produce an HV mean +/- SD across replicates. This
quantifies the BO methodology's contribution to apparent improvement vs the architectural
contribution of REQ-2 through REQ-6. Pass criterion: report HV across replicates with 95%
bootstrap CI; rule out the +36% improvement being a single-seed artefact (lower CI bound >
t0076's 8.41). Cost estimate: $1.00-$2.00 on a Vast.ai 64-core CPU. Recommended task types:
experiment-run, evaluation.

</details>

<details>
<summary>🧪 <strong>Multi-seed average of the t0065 protocol to add error bars on
FULL spike counts</strong> (S-0065-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0065-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0065_t0020_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0065_t0020_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0065 ran one seed per (mode, direction) cell. The FULL-mode 15-PD vs 1-ND spike count is
consistent with t0020's 20-trial mean (14.85 vs 1.80 Hz) but has no statistical band of its
own. Running 10-20 seeds per cell would give SD/SE on each metric and let us state the DSI
with a confidence interval. EPSP_PASSIVE and IPSP_PASSIVE traces are deterministic given seed
(verified bit-identicality of EPSP_PASSIVE PD vs ND in t0065), so multi-seed for those modes
is unnecessary - only FULL needs the seed sweep. Sweep cost: ~40 trials x 3 s ≈ 2 minutes
additional, no new infrastructure. Expected output: FULL-mode spike-count distribution per
direction (mean ± SD across 20 seeds) and DSI 95% confidence interval.

</details>

<details>
<summary>🧪 <strong>Multi-seed placement variability sweep on t0055 Mg-block
architecture (10 seeds at gNMDA = 0.5)</strong> (S-0055-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0055 used a single placement seed (= 0) for cross-task regression with t0054. The
bit-identical DSI = 0.7464 across all gNMDA is mechanistically interpretable but rests on a
single placement. Re-run the FULL/EPSP_PASSIVE/IPSP_PASSIVE trio at gNMDA = 0.5 nS for 10
placement seeds {0..9} and report mean +/- SD of vector-sum DSI, peak Hz, EPSP peak, and
Mg-block g(v) summary. This hardens the t0055 conclusion by showing the NMDA-inert regime is a
structural property of the architecture, not a coincidence of one synapse layout. Pass
criterion: DSI mean - SD remains > 0.50 (i.e., the Mg-block DSI recovery is robust across
placement seeds). Recommended task type: experiment-run.

</details>

<details>
<summary>📚 <strong>Port Jain 2020 DSGC (ModelDB 267001) as a sibling DSGC
asset</strong> (S-0008-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-05` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | [`10.7554_eLife.52949`](../../../tasks/t0008_port_modeldb_189347/assets/paper/10.7554_eLife.52949/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Clone ModelDB 267001 (Jain et al. 2020 eLife 56404) and port under the same HOC-driver pattern
as t0008. Jain 2020 extends the Poleg-Polsky architecture with bipolar delays and likely
shares MOD mechanisms with 189347. Medium effort (~20 hours) because the morphology and
stimulus logic are separate from 189347. Recommended task types: code-reproduction,
write-library.

</details>

<details>
<summary>📊 <strong>Promote peak-Hz and HWHM to co-primary outcomes when DSI is at
ceiling (evaluation methodology)</strong> (S-0029-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0029-07` |
| **Kind** | evaluation |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0029_distal_dendrite_length_sweep_dsgc`](../../../overview/tasks/task_pages/t0029_distal_dendrite_length_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0029 null result exposes a systematic evaluation weakness: whenever the t0022-lineage
testbed drives null firing to exactly 0 Hz, pref/null DSI is structurally pinned at 1.000
regardless of the manipulated variable, yet the secondary metrics (peak somatic firing rate,
HWHM, mean peak soma voltage, vector-sum DSI) contain usable length-dependent signal (e.g.,
the non-monotonic HWHM oscillation 71.7-116.3 deg and the 15->14 Hz peak-Hz cliff at 1.25x).
Adopt a co-primary-metric convention: whenever DSI is at ceiling (range across sweep points <
0.01 or null firing = 0 Hz on > 90% of trials), elevate peak-Hz, HWHM, and vector-sum DSI to
co-primary outcome variables and require all three to be reported alongside DSI in
results_summary.md and compare_literature.md. Encode the rule as an extension to the
task-results specification, add a verificator check for the DSI-ceiling condition, and
document the convention in arf/specifications. Recommended task types: infrastructure-setup.

</details>

<details>
<summary>📚 <strong>Promote the t0078 BoTorch qLogNEHVI + 49-d AIS-augmented
substrate harness into a reusable dsgc_mobo_v2 library asset</strong>
(S-0078-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-07` |
| **Kind** | library |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Builds on t0076's S-0076-06 (dsgc_mobo library promotion) which targets the t0076 25-d
harness. t0078 added approximately 1,300 LOC of net new optimisation infrastructure:
qLogNoisyExpectedHypervolumeImprovement migration, Normalize(d=49) input transform,
ProcessPoolExecutor with NEURON-fresh-subprocess workers, AIS-extended substrate builder
(extend_with_ais.py / build_cell_ais.py), 5-tier channel stratification engine, slow-AHP MOD
vendoring (skahpt78.mod with tau_ca_multiplier PARAMETER), checkpointing every 10 cells,
plot_pareto.py with --skip-deep-dives, render_pdf.py. Promote into a substrate-agnostic
library that supports either qLogNEHVI (BoTorch) or NSGA-II (pymoo) optimisers behind a
unified ParameterSpec API, parameterised compartment-tier definitions, and Vast.ai launch
helper. Bundles with S-0076-06; this is the v2 follow-up. Cost estimate: zero compute
(refactor only). Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Promote the t0081 warm-start NSGA-II harness into a reusable
bedb_warmstart_nsga2_harness library asset</strong> (S-0081-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-07` |
| **Kind** | library |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0081's harness combines (a) verbatim copying of prior-task Pareto cells, (b)
dimension-projection of lower-d Pareto cells into the current-d space with random fill on new
dims, (c) fresh LHS for diversity, and (d) pymoo NSGA-II with cost-cap watchdog. Promote this
combination into a versioned library asset (`bedb_warmstart_nsga2_harness`) under the asset
library type with documented APIs for the warm-start composition function and the NSGA-II
driver. Refactor only — no new compute. Distinct from S-0078-07 (BoTorch qLogNEHVI 49-d
harness) and S-0076-06 (BoTorch + ProcessPoolExecutor 25-d harness) — those are different
optimisers. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Re-calibrate t0083 channel densities to the post-fix procedural
cell's 707 um^2 cylinder soma</strong> (S-0092-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0092-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The post-fix BedB-equivalent fires 61 spikes vs the hand-coded Bed B's 41 spikes under the
same t0083 vector, because the channel densities were optimised on the 287 um^2 hand-coded
soma but the post-fix procedural soma is 707 um^2. Rather than tightening the soma area to
match t0024 (S-0092-02's path), the alternative is to re-run a small-scale NSGA-II pass on the
25 channel-density parameters (indices 0-24 + the dendritic-spike block 49-53) holding
morphology fixed at the post-fix BedB-equivalent, to find a 30-cell Pareto front under the
larger soma. The chosen winner becomes the new t0091 channel-side warm-start anchor. ~$1-2
cost on a single A10G; pure follow-up to t0083 with the new substrate. Recommended task types:
experiment-run.

</details>

<details>
<summary>🧪 <strong>Re-run t0047's noise (flickerVAR) sweep at Voff_bipNMDA=1 to test
noise-DSI behavior under voltage-independent NMDA</strong> (S-0048-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0048-05` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0048_voff_nmda1_dsi_test`](../../../overview/tasks/task_pages/t0048_voff_nmda1_dsi_test.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0048_voff_nmda1_dsi_test/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0047 ran a noise sweep at exptype=1 (Voff_bipNMDA=0). Now that t0048 establishes
Voff_bipNMDA=1 as the paper-faithful NMDA condition, the corresponding question is whether
t0047's noise vs DSI relationship (DSI declining with flickerVAR across the three gNMDA
conditions) holds under the voltage-independent setting. Re-run the same flickerVAR x gNMDA
grid t0047 used (or a reduced 3 x 3 grid to bound CPU) at exptype=2 and compare the
noise-vs-DSI shape. Useful corollary to t0048's gNMDA finding because it tells us whether the
noise sensitivity is dominated by NMDA voltage-dependence or by AMPA/GABA balance. Lower
priority because (a) t0047 already provides the qualitative noise-vs-DSI shape and (b) the H2
verdict for the Voff=1 DSI baseline is unlikely to be qualitatively different under noise.
Recommended task types: experiment-run.

</details>

<details>
<summary>🧪 <strong>Sensitivity sweep: re-run t0066 with paper-text e_LEAK = -70
mV</strong> (S-0066-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0066-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

The t0024 constants file documents that the de Rosenroll 2026 paper text specifies
ELEAK_PAPER_TEXT = -70 mV (a true hyperpolarising rest below e_GABA = -60), but the upstream
code authority used -60 mV. Re-run the t0066 EPSP/IPSP/FULL protocol with ELEAK = -70 mV (and
V_INIT = -70 mV) to test the paper-text variant. Prediction: IPSP_PASSIVE will become a real
hyperpolarising trace (PD ~-65 mV, ND ~-69 mV — closer to e_GABA = -60 mV with proportional
displacement); FULL DSI may change because the cell now sits 5 mV further from spike
threshold. This both quantifies the paper-vs-code discrepancy and gives us a reference
'hyperpolarising IPSP' DSGC for cross-comparison. Cost: re-run the same 120-trial sweep with
two constants changed = 1 line of code + 1 hour compute.

</details>

<details>
<summary>🧪 <strong>Sweep dendritic spine density on t0022 distal terminals as an
unconventional morphology variable</strong> (S-0027-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-07` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

No paper in the t0027 corpus sweeps dendritic spines on DSGCs; all 20 papers treat distal
terminals as smooth cables. Add explicit spine compartments (varying spine density 0, 0.5,
1.0, 2.0 spines/um on distal branches) on t0022 and measure DSI. Tests whether spine-head
capacitance shifts the dendritic-spike threshold gradient in a DS-relevant way, complementing
predictions from [Schachter2010] and [Sivyer2013]. Lower priority than the five predictive
sweeps but uniquely fills a corpus-wide blindspot identified in creative_thinking.md.

</details>

## Closed

<details>
<summary>✅ <s>16-direction vector-sum DSI re-evaluation of top 50 t0106 cells to
bridge t0106 <-> t0104 metric</s> — covered by <a
href="../../../tasks/t0107_t0106_polar_8dir_recheck/"><code>t0107_t0106_polar_8dir_recheck</code></a>
(S-0106-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0106 used 2-direction ratio DSI (PD = 0 deg, ND = 180 deg) and found 123 joint-pass cells;
t0099 / t0102 / t0104 used 16-direction vector-sum DSI on the same 68-d substrate and found
zero. Headline interpretation: the 2-direction reformulation surfaced cells the 16-direction
metric hid. To confirm this is a metric artefact and not a t0106-specific lucky cluster,
re-evaluate the top 50 t0106 cells under the full 16-direction protocol (every 22.5 deg).
Decision: if 16-direction DSI correlates strongly with 2-direction DSI (Spearman r > 0.7), the
reformulation surfaced genuine high-DSI cells; if correlation collapses, the 2-direction
metric is producing false positives that disappear at higher direction count. Optional bridge:
also evaluate at 8 directions to locate the metric phase transition. Recommended task types:
experiment-run, data-analysis, comparative-analysis. Cost: ~$1.50 (50 cells x 16 dirs x 3
trials).

</details>

<details>
<summary>✅ <s>Add dendritic-spike machinery to AIS-augmented Bed B and re-optimise
with NSGA-II under an AIS Nav lower-bound prior</s> — covered by <a
href="../../../tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/"><code>t0080_bedb_mobo_v3_dendritic_spike_nsga2</code></a>
(S-0078-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Bundled follow-up to the t0078 architectural diagnostic. The 49-d MOBO grazed the joint pass
(iter 81: DSI 0.316 / PD 9.68 Hz) but the high-DSI rail's PD ceiling held at 2.86 Hz across
109 acquisitions: passive dendrites are the bottleneck. Add: (a) Mg-block NMDA at active
densities on dendrites; (b) Nav1.6 / NaP at distal-dendrite densities sufficient for
back-propagating APs and dendritic spikes (Sivyer 2013, Oesch 2005). Hard lower-bound AIS Nav
at 0.25 S/cm^2 (Kole 2008 prior) so the optimiser cannot exploit the AIS-disabled corner (iter
81 nav16_ais 1e-5, four orders below prior). Use NSGA-II via pymoo (pop 64-128, 30-50 gens,
64-core CPU) not BoTorch qLogNEHVI to avoid O(N^3) GP-fit scaling that pushed t0078 to $3.93
at 60% of planned acquisitions. Pass: at least one Pareto cell with DSI >= 0.4 AND PD >= 10
Hz. Cost: $0.50-$1.00 on Vast.ai 64-core CPU. Recommended task types: build-model,
experiment-run.

</details>

<details>
<summary>✅ <s>Add NMDA component to t0052 minimal DSGC and measure DSI / peak-rate
response</s> — covered by <a
href="../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/"><code>t0054_minimal_dsgc_ampa_nmda_scalar_gaba</code></a>
(S-0052-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0052-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0052_minimal_dsgc_scalar_gaba`](../../../overview/tasks/task_pages/t0052_minimal_dsgc_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0052_minimal_dsgc_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0052 is AMPA-only by design; PolegPolsky2016 attributes ~35% of PD PSP magnitude to NMDA (5.8
mV / 16.5 mV total) and shows NMDARs contribute multiplicatively at depolarised potentials.
Add a NEURON Exp2Syn-based NMDA component (rise 5 ms, decay 50 ms, e=0, Mg-block via
voltage-dependent gating or a simplified gating function) co-located with each AMPA synapse,
and sweep gNMDA in {0, 0.1, 0.25, 0.5, 1.0, 1.5} nS at the t0052 baseline (100 E + 100 I,
gAMPA = 0.5 nS, scalar gabaMOD). Report peak Hz, primary and vector-sum DSI, HWHM, and PD/ND
PSP magnitudes per gNMDA. Goal: test whether NMDA addition closes the peak-rate gap toward the
t0004 30 Hz target without breaking the DSI = 1.0 design from gabaMOD, in a
minimal-from-scratch substrate (not the deposited 189347 paper-port substrate of t0046-t0049).
Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Add voltage-dependent NMDA Mg block to recover DSI in the t0054
minimal AMPA + NMDA + scalar gabaMOD architecture</s> — covered by <a
href="../../../tasks/t0055_nmda_mg_block_dsi_recovery/"><code>t0055_nmda_mg_block_dsi_recovery</code></a>
(S-0054-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0054_minimal_dsgc_ampa_nmda_scalar_gaba/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0054 demonstrated that voltage-independent NMDA (Exp2Syn, no Mg block) collapses vector-sum
DSI from 0.746 (gNMDA=0) to 0.082 (gNMDA=0.25) to 0.017 (gNMDA=1.0), confirming
PolegPolsky2016's prediction [Fig 5] that the Boltzmann Mg block is required for
multiplicative DSI scaling. Replace the NMDA Exp2Syn with a Jahr-Stevens Mg-block point
process (e.g., bipolarNMDA.mod from PolegPolsky2016 or an equivalent NMDA_Mg2 MOD), keeping
all other t0054 parameters fixed (placement seed 0, AMPA tau1=0.5/tau2=2.5/0.5 nS, scalar
gabaMOD with PD=0.33 ND=0.99 base 2 nS, soma+AIS HH). Re-run the {0, 0.25, 0.5, 1.0} nS gNMDA
sweep with the same 12 dirs x 10 trials x 3 modes protocol. Pass criterion: vector-sum DSI at
gNMDA=0.25 must exceed 0.50 and peak Hz must reach >= 5 Hz. This directly addresses the
headline negative result of t0054. Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>✅ <s>Audit deposited GABA and NMDA spatial synapse coordinates against
Poleg-Polsky 2016 paper text</s> — covered by <a
href="../../../tasks/t0050_audit_syn_distribution/"><code>t0050_audit_syn_distribution</code></a>
(S-0049-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Under SEClamp at -65 mV, the deposited code's GABA shows PD/ND symmetry (47.47 vs 48.04 nS,
DSI -0.006) instead of the paper's clear ND-bias (12.5 vs 30 nS, DSI -0.41). NMDA also
collapses to symmetry (DSI 0.006 vs paper +0.17). Modality alone does not reconcile this.
Audit `placeBIP()` and any GABA-placement HOC code in the deposited DSGC: extract per-synapse
3D coordinates and section assignments, classify each synapse by PD-side vs ND-side dendrite,
and compare the distribution against paper text and figure descriptions. This explains the
somatic asymmetry collapse and informs whether the deposited model needs a spatial
redistribution correction or a per-side conductance scaling. Recommended task types:
data-analysis.

</details>

<details>
<summary>✅ <s>Deep-dive Vm-trace analysis of cell 767 to identify which
dendritic-spike machinery drives the joint pass</s> — covered by <a
href="../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/"><code>t0084_t0081_cell_767_vm_trace_deepdive</code></a>
(S-0081-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Cell 767 crosses the joint pass threshold (DSI 0.494 / PD 11.39 Hz) but the biophysical
mechanism is unattributed: it could be NMDA Mg-block recruitment, distal Nav1.6 dendritic
spikes, persistent Na (NaP) sustained depolarisation, or a combination. Generate per-direction
(8 angles) Vm traces from the proximal soma, mid dendrite, and distal dendrite for cell 767
and the two neighbouring near-pass cells (637 and 762). Plot dendritic-spike onset times, NMDA
conductance trajectories, and AIS spike correlation per direction. Local CPU run on a single
cell + 8 directions takes ~10 min; no remote machine needed. Recommended task types:
experiment-run, data-analysis.

</details>

<details>
<summary>✅ <s>Download both candidate Feller-lab 2018 source papers to resolve the
dsgc-baseline-morphology provenance ambiguity</s> — covered by <a
href="../../../tasks/t0013_resolve_morphology_provenance/"><code>t0013_resolve_morphology_provenance</code></a>
(S-0005-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-01` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The dsgc-baseline-morphology asset (NeuroMorpho neuron 102976, 141009_Pair1DSGC) currently has
source_paper_id=null because two Feller-lab papers from 2018 are plausibly the source: the
plan-nominated Morrie & Feller 2018 Neuron (DOI 10.1016/j.neuron.2018.05.028) and the
NeuroMorpho-reported Murphy-Baum & Feller 2018 Current Biology (DOI
10.1016/j.cub.2018.03.001). Run /add-paper for both DOIs in a dedicated download-paper task,
read each paper's Methods to confirm which one introduced the 141009_Pair1DSGC reconstruction,
then file a corrections asset that updates dsgc-baseline-morphology source_paper_id to the
correct paper_id slug. This unblocks correct citation of the morphology in every downstream
paper-comparison task. Recommended task types: download-paper.

</details>

<details>
<summary>✅ <s>Extend t0081 NSGA-II to gen 12-15 (1,152-1,440 cells) to characterise
the joint-passing region</s> — covered by <a
href="../../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/"><code>t0083_bedb_v3_extend_nsga2_gen8plus</code></a>
(S-0081-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0081-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Hypervolume grew monotonically from 6.59 (gen 0) to 16.33 (gen 7) with no plateau, and the
gen-7 Pareto front contains a near-pass cluster (cell 637 at distance 0.063, cell 762 at
0.086, cell 767 at 0.000). The joint-pass region is therefore discovered but not
characterised. Re-run NSGA-II from the t0081 warm-start initial population for 12-15
generations (1,152-1,440 cells) and report the count of joint-pass cells, Pareto-front
composition in the (DSI >= 0.4, PD >= 10 Hz) box, and final HV. Reuse the t0081 harness with
`n_gen` increased. Cost ~$3-4 (incremental ~5-7 hours at $0.2382/hr). Recommended task types:
experiment-run.

</details>

<details>
<summary>✅ <s>GABA peak-conductance sweep on t0053 spatial DSGC to recover a
non-zero FULL tuning curve</s> — covered by <a
href="../../../tasks/t0057_tonic_gaba_sweep_t0053/"><code>t0057_tonic_gaba_sweep_t0053</code></a>
(S-0053-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0053 reports DSI = 0.0 / peak Hz = 0.0 in FULL mode because 2 nS GABA on ~50% of 100 synapses
(100 nS mean total per trial) fully suppresses spiking on the t0009-calibrated morphology.
AMPA-only fires at 0.667 Hz uniformly, so excitation is at threshold and any inhibition
crosses below threshold. Re-run the 12-direction x 10-trial FULL sweep on the t0053 substrate
(same placement seed 0, same centripetal-gating rule) at GABA peak conductances g_GABA in
{0.5, 1.0, 1.32, 1.5, 2.0} nS while holding everything else fixed. The 1.32 nS point is
conductance-matched to t0052's 66 nS mean total per trial. Report peak Hz, primary and
vector-sum DSI, HWHM, and reliability per g_GABA. Goal: locate the operating point where
spatial gating produces a measurable DSI on this morphology so it can be compared meaningfully
to t0052 and to in vivo / in vitro DSGC bands. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Implement gabaMOD parameter-swap protocol for ModelDB 189347</s> —
covered by <a
href="../../../tasks/t0020_port_modeldb_189347_gabamod/"><code>t0020_port_modeldb_189347_gabamod</code></a>
(S-0008-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0008-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0008_port_modeldb_189347/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Re-run the ModelDB 189347 port under the paper's native DS protocol: sweep gabaMOD between PD
(0.33) and ND (0.99) instead of rotating BIP synapse coordinates. This is expected to
reproduce the paper's headline DSI (~0.8) and peak firing (~32-40 Hz) that the rotation-based
proxy in t0008 cannot reach. Would be a small extension (new trial-protocol branch in
run_one_trial) with a separate tuning_curves CSV and score_report for comparison with the
rotation protocol. Recommended task types: code-reproduction.

</details>

<details>
<summary>✅ <s>Implement Nav1.6/Nav1.2/Kv1/Kv3 channel mechanisms with AIS-specific
conductance densities in downstream DSGC model</s> — covered by <a
href="../../../tasks/t0043_nav16_kv3_nmda_restoration_t0022/"><code>t0043_nav16_kv3_nmda_restoration_t0022</code></a>
(S-0019-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0019-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0019_literature_survey_voltage_gated_channels`](../../../overview/tasks/task_pages/t0019_literature_survey_voltage_gated_channels.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

The answer asset nav-kv-combinations-for-dsgc-modelling produces a 6-point specification for
DSGC voltage-gated-channel distribution in NEURON extending the synaptic-integration
constraints from t0018. The downstream DSGC compartmental-model build task must implement: (1)
Nav1.6 with V_half around -45 mV and fast kinetics at distal AIS (densities 2500-5000 pS/um2),
(2) Nav1.2 with V_half around -32 mV at proximal AIS and soma (lower density around 100-500
pS/um2), (3) Kv1.1/Kv1.2 delayed-rectifier with V_half -40 to -50 mV at AIS (density 100-500
pS/um2), (4) Fohlmeister-Miller HH rate functions with Q10 near 3 for temperature scaling (all
mechanisms tested at 22 and 32 degC), (5) passive soma/dendrite compartments with no Nav
except for low-density Nav1.2 co-expression on proximal dendrites, (6) named fitting
objectives for AP threshold (AIS initiation at -55 mV +/- 5 mV), AP width (0.5-1.0 ms at 32
degC), and backpropagation attenuation (50% by 100 um into dendrite) to reproduce
Fohlmeister-Miller RGC firing properties.

</details>

<details>
<summary>✅ <s>Implement the tuning-curve scoring loss combining DSI, peak rate, null
residual, and HWHM targets</s> — covered by <a
href="../../../tasks/t0012_tuning_curve_scoring_loss_library/"><code>t0012_tuning_curve_scoring_loss_library</code></a>
(S-0002-09)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-09` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1113_jphysiol.2008.161240`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1113_jphysiol.2008.161240/) |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The survey surfaces four concurrent numerical targets an optimised DSGC model must hit (DSI
0.7-0.85, preferred peak 40-80 Hz, null residual < 10 Hz, HWHM 60-90 deg), and the project has
four registered metrics (direction_selectivity_index, tuning_curve_hwhm_deg,
tuning_curve_reliability, tuning_curve_rmse). Build a scoring library that takes a simulated
angle-to-AP-rate tuning curve plus the canonical target curve from t0004 and returns a single
scalar loss combining all four targets with documented weights (e.g., weighted Euclidean
distance in normalised space), plus per-metric residuals. This is the tool every downstream
optimisation task (Na/K grid, morphology sweep, E/I ratio scan) will depend on. Recommended
task types: write-library.

</details>

<details>
<summary>✅ <s>Paired active-vs-passive dendrite experiment to reproduce the
Schachter2010 DSI gain (~0.3 -> ~0.7)</s> — covered by <a
href="../../../tasks/t0044_schachter_retest_on_t0043/"><code>t0044_schachter_retest_on_t0043</code></a>
(S-0002-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Schachter2010 reports that switching DSGC dendrites from passive to active (adding
Fohlmeister-like g_Na and g_K) raises DSI from ~0.3 to ~0.7 on the same morphology and
synaptic input, and Oesch2005 provides the TTX-sensitive dendritic Na+ spike patch-clamp data
that anchor this claim. Run two paired simulations that differ only in dendritic g_Na (0 vs
Schachter2010 density), holding morphology, synapse placement, and stimulus identical, and
report the DSI delta with 95% CI across synapse-placement seeds. This directly answers RQ4 and
isolates the dendritic-conductance contribution from morphology and synaptic effects.
Recommended task types: experiment-run, comparative-analysis.

</details>

<details>
<summary>✅ <s>Parameter-cluster analysis of t0083's 15 joint-pass and 18 Pareto
cells to identify distinct biophysical motifs</s> — covered by <a
href="../../../tasks/t0086_robustness_cluster_bio_comparison/"><code>t0086_robustness_cluster_bio_comparison</code></a>
(S-0083-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0083-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The 15 joint-pass cells (DSI >= 0.4 AND PD >= 10 Hz) and 18 Pareto cells span a wide (DSI, PD)
range from cell 1304 (0.77 / 14 Hz) through cell 1559 (0.71 / 39 Hz) to cell 1723 (1.00 / 7
Hz). Comparison of the first 6 parameter dimensions (e.g. cell 1304 [0.006, 0.001, 0.999,
0.995, 0.876, 0.992] vs cell 767 [0.008, 0.018, 1.000, 1.000, 0.250, 0.000]) suggests >=2
distinct biophysical motifs. Cluster the 18 Pareto cells in 54-d space via hierarchical
clustering (Ward linkage on standardised parameters); identify 2-4 motif clusters; for each
report the mean parameter vector, dominant mechanism (NaP_dend / NMDA / Nav_dend_distal), and
Pareto position. Output: motif table + cluster heatmap PNG + per-motif Vm trace. Critical for
t0084 follow-up: t0084 found NaP_dend dominant for cell 767 -- is the same true for cell
1304's motif? Recommended task types: data-analysis.

</details>

<details>
<summary>✅ <s>Patched-generator full 60-morph re-sweep to validate the t0092 soma
fix at scale</s> — covered by <a
href="../../../tasks/t0093_resweep_and_t0090_correction/"><code>t0093_resweep_and_t0090_correction</code></a>
(S-0092-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0092-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0090's diversity sweep produced 51/60 NAN_VOLTAGE cells and 9/60 STABLE-but-silent cells
under the t0083 best-cell channels. The t0092 diagnostic confirmed the soma pt3d-collapse bug
as the load-bearing cause and validated the fix on only 5 STABLE-from-t0090 cells. Re-run the
full 60-morphology Phase D verification under the t0083 vector with the patched
generate_fixed_morphology to confirm that (a) the 51 NAN_VOLTAGE-pre-fix cells now reach
STABLE, and (b) more than the current 5 cells produce non-zero PD-rate. This produces the
project-level evidence that the bug is fully fixed and surfaces any remaining failure modes
(e.g. asymmetry-knob extreme values that survive the soma fix). Pure simulation; ~30 min on
local 64-core. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>✅ <s>Per-cluster Vm trace deep-dive (extension of t0084 to all 6 Genuine
cells)</s> — covered by <a
href="../../../tasks/t0088_recluster_marginals_and_vm_motifs/"><code>t0088_recluster_marginals_and_vm_motifs</code></a>
(S-0086-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0086-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0084 produced a Vm-trace mechanism attribution for cell 767 only. t0086 found that cell 767
was Marginal (3/5 reps pass) and that 6 different cells (1517, 1604, 1634, 1639, 1663, 1677)
are Genuine and partition into 2 clusters. Extend t0084's deep-dive methodology (24-direction
NEURON simulations with extended Vm + NMDA conductance + Nav1.6 / NaP current density
recording at soma / mid-dendrite / distal dendrite / AIS) to all 6 Genuine cells. Compare
per-cluster Vm dynamics (Cluster 0 high-NaP+high-AIS vs Cluster 1 high-GABA-lambda). Produce
one cluster-specific mechanism attribution figure plus a comparative table. Expected cost:
~$1.20 USD on Vast.ai EPYC 7B13 (6 cells x 24 directions x 60 s = 2.4 h x $0.35/hr).
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>✅ <s>Per-synapse stimulus-window-tied (t_on, t_off) tonic GABA on t0057 to
model bar-arrival-locked inhibition</s> — covered by <a
href="../../../tasks/t0059_bar_locked_gaba_ampa_sweep_t0057/"><code>t0059_bar_locked_gaba_ampa_sweep_t0057</code></a>
(S-0057-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0057-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0057_tonic_gaba_sweep_t0053`](../../../overview/tasks/task_pages/t0057_tonic_gaba_sweep_t0053.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0057 used a global (t_on, t_off) = (100 ms, 1400 ms) for every active synapse regardless of
dendritic position. Biological SAC inhibition is bar-arrival-locked: each SAC outputs GABA
only as the bar passes its dendritic field, producing a synapse-specific window of width
~100-300 ms. On t0057's minimal_dsgc_tonic_gaba_sweep substrate, modify schedule_ei_onsets so
each centripetally-active I synapse gets t_on = (x*cos(theta) + y*sin(theta))/v + offset_ms
and t_off = t_on + window_ms, where (x, y) is synapse coordinate, theta is bar direction, v is
bar velocity, and window_ms is swept in {50, 100, 200, 400} ms. Keep GABA_BASE_NS at 1.0 nS
(borderline single-spike regime). Run 12 dir x 10 trials x 3 modes per window (1440 trials,
~85 min). Pass criterion: locate at least one window where the per-synapse onset gradient
produces direction-dependent IPSP timing that breaks the FULL-mode degeneracy (peak Hz != null
Hz). Recommended task types: build-model, experiment-run.

</details>

<details>
<summary>✅ <s>Re-run Bed B MOBO with an AIS section added, to test whether AIS
unlocks the DSI>=0.4 + rate>=30Hz operating point</s> — covered by <a
href="../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/"><code>t0078_bedb_mobo_v2_ais_tiered_ahp</code></a>
(S-0076-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0076-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0076 demonstrated the bare 25-d Bed B substrate cannot reach DSI>=0.4 AND PD rate>=30 Hz
simultaneously. Compare-literature concluded the substrate is missing dendritic-spike
machinery and there is no AIS. After S-0024-03 (add AIS to Bed B as a library asset) is
delivered, re-run the t0076 25-d MOBO on the AIS-equipped Bed B with 2 extra channel-density
parameters for the AIS tier (Nav1.6_AIS, Kv3_AIS) -> 27-d search. Hypothesis: AIS-localised
spike initiation will let high-Nav cells reach physiological rates without quenching DSI. This
complements t0075 (AIS sweep on Bed A) by porting the question to the second substrate under
joint optimisation rather than one-axis-at-a-time. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Re-run NSGA-II on the v3 54-d Bed B substrate at the full plan scope
(pop=96 / gen=40 = 3,840 cells)</s> — covered by <a
href="../../../tasks/t0081_bedb_v3_warmstart_nsga2/"><code>t0081_bedb_v3_warmstart_nsga2</code></a>
(S-0080-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0080 missed the joint pass criterion (DSI>=0.4 AND PD>=10 Hz) by a wide margin (best Pareto
cell 141 at DSI 0.127 / PD 2.54 Hz; closest-to-joint cell 188 at DSI 0.000 / PD 9.25 Hz) on a
192-cell run that was 5% of the plan's 3,840-cell scope. NSGA-II at pop=24 is below the
practical floor for 54-d (Hay 2011 used pop=1000 for 22-d; pop=100 is the de-facto floor for
50+ d). Re-run on a longer Vast.ai 64-core EPYC 7B13 allocation at pop=96 / gen=40 to
determine whether the negative architectural result holds at the planned budget. Estimated
cost ~$1.50-$2.00 over 8-10 wall-clock hours given that t0080 cells run sequentially
saturating 64 cores at ~45 s each. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Re-run t0046 gNMDA sweep at exptype=2 (Voff_bipNMDA=1) to test whether
voltage-independent NMDA flattens DSI vs gNMDA</s> — covered by <a
href="../../../tasks/t0048_voff_nmda1_dsi_test/"><code>t0048_voff_nmda1_dsi_test</code></a>
(S-0047-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0047 confirms DSI vs gNMDA peaks at 0.19 near b2gnmda = 0.5 nS and decays to 0.018 by 3.0 nS,
never reaching the paper's claimed flat ~0.30. Most plausible source: the deposited control's
`Voff_bipNMDA = 0` (voltage-dependent NMDA with Mg block). As gNMDA rises, ND dendrites
depolarise enough to relieve Mg block and ND NMDA catches up to PD, collapsing DSI. The
paper's biological NMDA is voltage-INDEPENDENT. Direct test: re-execute the same 7-point sweep
(PD/ND, 4+ trials) at `exptype = 2` (sets `Voff_bipNMDA = 1`, the same setting used by 0Mg)
instead of `exptype = 1`. Expected: DSI flattens toward ~0.20-0.30 across the sweep. Not a
model modification — only an exptype choice. Re-uses t0046 library and t0047's
`code/run_with_conductances.py` directly. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Reproduce the PolegPolsky2016 baseline DSGC model from ModelDB 189347
as the project's starting compartmental simulation</s> — covered by <a
href="../../../tasks/t0008_port_modeldb_189347/"><code>t0008_port_modeldb_189347</code></a>
(S-0002-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-03` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

PolegPolsky2016 (paper 10.1016_j.neuron.2016.02.013) is the closest published match to this
project's goal — a NEURON multi-compartmental mouse ON-OFF DSGC model with 177 AMPA + 177 GABA
synapses and NMDA multiplicative gain — with public code at ModelDB entry 189347. Download the
ModelDB code, run the original published stimulus, and verify the reproduced tuning curve
lands inside the published DSI 0.7-0.85 / peak 40-80 Hz / null < 10 Hz / HWHM 60-90 deg
envelope. This creates the reference implementation the later parameter-variation tasks (Na/K
grid, morphology sweep, E/I ratio scan) will fork from. Recommended task types:
code-reproduction.

</details>

<details>
<summary>✅ <s>Rerun t0030's 7-diameter sweep at GABA=4 nS on t0022</s> — covered by
<a
href="../../../tasks/t0039_distal_dendrite_diameter_sweep_t0022_gaba4/"><code>t0039_distal_dendrite_diameter_sweep_t0022_gaba4</code></a>
(S-0037-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

t0030's diameter sweep was uninformative because DSI was pinned at 1.000 (null firing = 0 Hz
at 12 nS GABA). With 4 nS, the t0037 sweet spot, the t0022 testbed produces biologically
realistic DSI (0.429) and preferred direction (40 deg). Rerun the original 7-diameter sweep
(0.2, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0 um) with GABA_CONDUCTANCE_NULL_NS=4.0 to measure the
Schachter2010-vs-passive-filtering slope that has been the project's headline discriminator
target since t0030.

</details>

<details>
<summary>✅ <s>Rerun the distal-diameter sweep on t0022 with null-GABA conductance
reduced from 12 nS to 6 nS</s> — covered by <a
href="../../../tasks/t0036_rerun_t0030_halved_null_gaba/"><code>t0036_rerun_t0030_halved_null_gaba</code></a>
(S-0030-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0030-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0030_distal_dendrite_diameter_sweep_dsgc`](../../../overview/tasks/task_pages/t0030_distal_dendrite_diameter_sweep_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The t0030 sweep failed as a Schachter2010-vs-passive-filtering discriminator because primary
DSI is pinned at 1.000 at every diameter multiplier (null firing 0 Hz under the t0022 E-I
schedule). compare_literature.md traces the ceiling to GABA_CONDUCTANCE_NULL_NS = 12 nS
delivered 10 ms before AMPA on null trials, about 2x Schachter2010's compound null inhibition
(~6 nS). Rerun the full 7-point diameter sweep (0.5x-2.0x, 12 angles x 10 trials = 840 trials)
with GABA_CONDUCTANCE_NULL_NS lowered to 6 nS so null firing becomes non-zero and primary DSI
regains dynamic range. Distinct from S-0029-04 (null-GABA sweep at fixed length 1.0x) and
S-0029-01 (Poisson + length sweep): this targets the diameter axis specifically. Expected
cost: local CPU, ~2 h wall time. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Retrieve paywalled Kim2014 and Sivyer2013 PDFs via Sheffield SSO and
upgrade their summaries to full-text grounding</s> — covered by <a
href="../../../tasks/t0031_fetch_paywalled_morphology_papers/"><code>t0031_fetch_paywalled_morphology_papers</code></a>
(S-0027-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Two papers (Kim2014, Sivyer2013) were flagged in t0027 intervention/ folder as paywalled and
summarised from abstract + secondary citations only. Both are load-bearing for predictions
S-0027-01 and S-0027-02. Resolve by retrieving full PDFs through Sheffield institutional SSO
(Cell Press, Nature Neuroscience), upgrading their summaries to full-text level, and updating
the t0027 synthesis answer asset citations from abstract-only to full-text grounding. Low-cost
prerequisite for confidently running S-0027-01 and S-0027-02.

</details>

<details>
<summary>✅ <s>Retune BEDB_BASE_POINT so the procedural Bed-B cell elicits spikes
under the t0083 channel set</s> — covered by <a
href="../../../tasks/t0092_diagnose_morphology_generator_silence/"><code>t0092_diagnose_morphology_generator_silence</code></a>
(S-0090-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The procedural Bed-B-equivalent cell paired with the t0083 best-cell parameter vector is
STABLE but silent (DSI=0, peak Vm=-70.0 mV at PD); this single failure cascades into the
partial verdicts on REQ-9 (Phase F Bed-B reproducibility), REQ-11 (G.2 NMDA calibration
produced 0/7 valid recordings due to stimulus-time divergence), and REQ-12 (G.3 NaP knockout
deferred). Sweep the two most likely culprits identified in the t0090 results_detailed.md
analysis, mean_segment_length_um and branch_prob_per_um, on a small grid (e.g. 5x5) around the
current Bed-B base point and pick the (params, seed) combination whose procedural cell most
closely reproduces the de Rosenroll 2026 / t0024 Bed B port's DSI and PD firing rate under the
t0083 best-cell channel set. Then re-run Phase F, G.2, and G.3 on the corrected base point.
Recommended task types: correction, experiment-run.

</details>

<details>
<summary>✅ <s>Sequential further null-GABA reductions (4, 2, 1 nS) on the t0022
distal-diameter sweep</s> — covered by <a
href="../../../tasks/t0037_null_gaba_reduction_ladder_t0022/"><code>t0037_null_gaba_reduction_ladder_t0022</code></a>
(S-0036-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0036-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0036_rerun_t0030_halved_null_gaba`](../../../overview/tasks/task_pages/t0036_rerun_t0030_halved_null_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0036 halved GABA_CONDUCTANCE_NULL_NS from 12 nS to 6 nS and null firing stayed pinned at 0.0
Hz at every diameter multiplier, falsifying the Schachter2010 ~6 nS compound-inhibition
rescue. The classifier auto-recommendation was 'reduce null-GABA further to ~4 nS'. Rerun the
t0036 diameter sweep at 4 nS, 2 nS, and 1 nS (stop as soon as mean null firing exceeds 0.1 Hz
at 1.0x); each rerun is ~30 min CPU so worst case ~1.5 h. If null firing unpins at 4 or 2 nS,
primary DSI becomes measurable and the Schachter2010-vs-passive slope discriminator is rescued
on deterministic t0022. If it stays 0 Hz down to 1 nS, the testbed is structurally
incompatible with primary DSI on morphology axes and the project must adopt Poisson rescue
(S-0030-02) or migrate the optimiser substrate to t0024 (S-0034-07). Distinct from S-0029-04
(3-12 nS at fixed length on t0029 code) - this extends below the 3 nS floor on the t0036
diameter-sweep code path. Recommended task types: experiment-run.

</details>

<details>
<summary>✅ <s>Sweep distal-dendrite scale on t0022 to discriminate passive TR
weighting vs dendritic-spike branch independence</s> — covered by <a
href="../../../tasks/t0034_distal_dendrite_length_sweep_t0024/"><code>t0034_distal_dendrite_length_sweep_t0024</code></a>
(S-0027-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Run t0022 with distal dendritic segments scaled by 1.0x, 1.25x, and 1.5x at fixed synapse
count and biophysics. Prediction (creative_thinking.md #1): if passive transfer-resistance
weighting [Dan2018, 10.1101_2024.07.10.602901] dominates, DSI drops by >30% at 1.5x; if
dendritic-spike branch independence [Sivyer2013, 10.1038_nn.3565] dominates, DSI stays within
10%. High-information-gain experiment that resolves a core mechanism ambiguity in the surveyed
corpus and directly informs whether morphology-sweep design must preserve cable geometry or
only branch topology.

</details>

<details>
<summary>✅ <s>Test BK / SK calcium-activated K+ co-expression with Nav1.6</s> —
covered by <a
href="../../../tasks/t0074_channel_tuning_width_bed_a/"><code>t0074_channel_tuning_width_bed_a</code></a>
(S-0068-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0068-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0068 falsified the Nav1.6 + Kv3 rescue hypothesis: Kv3 doesn't differentially suppress firing
at high rates because its activation depends on V, not on cumulative Ca2+. The natural
alternative is a Ca2+-activated K+ channel (BK / KCa1.1 or SK / KCa2). These channels' open
probability scales with intracellular [Ca2+], which itself scales with cumulative AP firing.
Therefore: ND (low firing, low [Ca2+]) → BK/SK barely active → cell fires normally. PD (high
firing, high [Ca2+]) → BK/SK strongly activated → cell is clamped down → PD firing reduced
more than ND firing → DSI restored. This is mechanistically coherent and biologically
plausible (DSGCs express both BK and SK in vivo). Implementation: vendor a BK MOD (e.g., from
Hines & Carnevale's Purkinje model) AND a Ca2+ pool mechanism, then sweep BK density at fixed
Nav1.6 = high. Cost: 1-2 hours code + ~5 min compute per density.

</details>

<details>
<summary>✅ <s>Test channel co-expression: Nav1.6 + Kv3 jointly</s> — covered by <a
href="../../../tasks/t0068_t0067_nav16_kv3_coexpression_rescue/"><code>t0068_t0067_nav16_kv3_coexpression_rescue</code></a>
(S-0067-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0067-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0067 tested each channel in isolation. Real fast-spiking neurons co-express Nav1.6 (fast-Na
with low threshold) AND Kv3 (fast K+ for rapid repolarisation) — the joint expression enables
sustained 100+ Hz firing without fatigue. Test co-insertion: 4 conditions on the t0065
substrate ({Nav1.6_med, Nav1.6_med + Kv3_med, Nav1.6_high, Nav1.6_high + Kv3_high}) × PD/ND ×
5 seeds = 40 trials. Hypothesis: Kv3 co-insertion will RESCUE DSI by allowing the cell to
recover from Nav1.6's depolarising drive faster, restoring the inhibitory shunt's modulatory
power. If true, this is a proof-of-concept that biological 'fast-spiking design' is
intrinsically DS-friendly.

</details>

<details>
<summary>✅ <s>Thicken distal branches on t0022 (halve distal input resistance) to
separate active amplification from passive filtering</s> — covered by <a
href="../../../tasks/t0035_distal_dendrite_diameter_sweep_t0024/"><code>t0035_distal_dendrite_diameter_sweep_t0024</code></a>
(S-0027-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0027-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0027_literature_survey_morphology_ds_modeling`](../../../overview/tasks/task_pages/t0027_literature_survey_morphology_ds_modeling.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0027_literature_survey_morphology_ds_modeling/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Halve the input resistance of distal dendritic branches on t0022 by doubling their diameter
and re-running the DSI protocol with active conductances (a) intact and (b) ablated.
Prediction (creative_thinking.md #3): if [Schachter2010, 10.1371_journal.pcbi.1000899]
dendritic-spike gain is essential, thickening abolishes active gain but preserves subthreshold
DSI; if passive filtering carries DSI, thickening preserves both. Disambiguates the active vs
passive contribution that the corpus does not separate cleanly.

</details>

<details>
<summary>✅ <s>Update t0033 optimiser base GABA on t0022 variant to 4.0 nS</s> —
covered by <a
href="../../../tasks/t0038_correct_t0033_base_gaba_to_4ns/"><code>t0038_correct_t0033_base_gaba_to_4ns</code></a>
(S-0037-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-02` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0033 is scoped to sweep t0022 parameters against a primary-DSI objective. With
GABA_CONDUCTANCE_NULL_NS=12 the objective is pinned and the optimiser sees no gradient. Update
t0033's t0022 variant to set GABA_CONDUCTANCE_NULL_NS=4.0 as the base parameter; this is the
first point at which the t0022 primary-DSI landscape can be optimised meaningfully. Without
this change the Vast.ai optimisation runs on t0022 will be wasted compute.

</details>

<details>
<summary>✅ <s>Zero-cost L/lambda collapse analysis of all t0034 length and t0035
diameter data</s> — covered by <a
href="../../../tasks/t0041_electrotonic_length_collapse_t0034_t0035/"><code>t0041_electrotonic_length_collapse_t0034_t0035</code></a>
(S-0035-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Re-plot DSI from all existing t0034 (length sweep) and t0035 (diameter sweep) trials against
the computed distal electrotonic length L/lambda, using morphology and passive parameters
already stored in each task's outputs. If the length and diameter data collapse onto a single
curve, this confirms creative_thinking.md's primary hypothesis: the length/diameter asymmetry
is a consequence of cable theory (L/lambda is linear in length but scales as 1/sqrt(d)). No
new simulations required; ~1-2 hours of re-analysis work only. Recommended task types:
data-analysis.

</details>
