# Suggestions: `compartmental-modeling`

418 suggestion(s) in category
[`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) **376 open** (67
high, 266 medium, 43 low), **42 closed**.

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
<summary>🧪 <strong>3-objective NSGA-II extension: maximise DSI, maximise PD-rate,
minimise cytoplasm volume</strong> (S-0122-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000877`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/paper/10.1371_journal.pcbi.1000877/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0122's 2-objective Pareto front is L-shaped (volume dominates because it is easy to minimise)
and top-DSI cells have PD-rate 23-26 Hz, just below the 30 Hz strict-LEGIT floor; only the
strict-LEGIT cohort (10 cells, distinct from top-10 by DSI) cleared the floor. Action: extend
the t0122 evaluator to emit out['F'] = [-dsi, -pd_rate_hz, +cytoplasm_volume_um3] (n_obj=3),
keep other hard constants identical, draw a fresh non-round GA seed, run NSGA-II 60 gens on
the same Vast.ai EPYC substrate; adjust REF_POINT_HV and HV_UTOPIA to 3 entries (DSI=0, PD=0,
V=50000). Prediction: adding max-PD-rate shifts the Pareto frontier upward in PD, populates
the strict-LEGIT cohort denser than t0122's 10 cells, and resolves the top-10-by-DSI vs
strict-LEGIT cohort mismatch. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>5-seed pooled re-analysis adding t0113 (seed 2247) via correction
to the t0116 pipeline</strong> (S-0116-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0116-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0116's 4-seed pool (44/77/7755/9354) was a deliberate first cut; seed 2247 (t0113) was
excluded because its joint-pass cells are silence-guard DSI=1.0 saturations (per
S-0113-04/S-0113-06). Re-run the t0116 pipeline end-to-end with t0113 added as the fifth
source (5-seed pool, same strict filter DSI>0.7 AND PD>10, silence-guard tightened to >=3 PD
spikes per S-0113-06), regenerate every chart and CSV, and write a corrections/ overlay that
points consumers at the 5-seed artefacts. Decision rule: if seed-aligned cluster pattern
survives (NMI > 0.7 on both partitions), the basin-isolation finding is robust; if NMI drops
below 0.5, the 4-seed result was an artefact of seed choice. Recommended task types:
data-analysis, correction. Cost: <$0.20.

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
<summary>🧪 <strong>Add 2-3 further random-init GA seeds to upgrade the
substrate-rate estimate from 5-seed to 7-8 seed</strong> (S-0121-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0121-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0121_5seed_substrate_rate_canonical_report`](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The 5-seed bootstrap 95% CI (+0.38%, +5.53%) excludes 0% but still brackets both Hay 2011
(0.40%) and Druckmann 2007 (0.10%) baselines; the normal-approx CI (-0.35%, +5.51%) straddles
0. With n=5 the resampling pool is small and the CI is sensitive to seed 7755's 8.13% draw and
seed 2247's 0% draw. Concrete action: draw 2-3 further random GA seeds via
secrets.randbelow(10000) (avoiding the already-used 44, 77, 2247, 7755, 9354), run each as a
minimum-change replicate of t0115 (auto-stop disabled, cadence 10, gen ceiling 300, budget cap
~$3 per seed), then re-run the t0121 pipeline against the expanded 7-8 seed sample. Decision:
if both CIs clear the Hay envelope upper bound at 7-8 seeds, the substrate-density claim can
be made at p < 0.05 without the censoring caveat. Distinct from S-0113-01 (closed by t0114 +
t0115). Recommended task types: experiment-run.

</details>

<details>
<summary>🔧 <strong>Adopt (WINDOW=3, REL_THRESHOLD=0.015) as new project-default
HV-plateau detector constants</strong> (S-0114-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-01` |
| **Kind** | technique |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0114_seed7755_no_autostop/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0114's offline detector replay (4 windows x 6 thresholds x 4 HV trajectories = 96 cells)
selects (W*, T*) = (3, 0.015) as the smallest deviation from current (W=2, T=0.01) that (a)
fires on t0106 at gen 39 within [20, 60], (b) does NOT fire prematurely on t0113's recorded 14
gens (eliminates the gen-13 false positive), and (c) fires on t0114 at gen 26, inside
Mohacsi2024's 20-60 gen convergence band. Concrete action: update the HV-plateau detector
constants in the NSGA-II driver / skill template from (WINDOW=2, REL_THRESHOLD=0.01) to
(WINDOW=3, REL_THRESHOLD=0.015); cite the 4-trajectory replay as design justification. Formal
realisation of the recommendation prepared but not adopted in S-0113-03. Recommended task
types: infrastructure-setup, data-analysis. Cost: <$0.10.

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
<summary>📊 <strong>Audit AIS-to-soma Nav ratio computation in cluster 1 (116x is
+33 sigma exotic)</strong> (S-0088-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0088-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Source paper** | [`werginz_2024`](../../../tasks/t0088_recluster_marginals_and_vm_motifs/assets/paper/werginz_2024/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0088 cluster 1 (cells 1304, 1504, 1624, 1634) has centroid AIS-to-soma Nav ratio = 116.04,
deviating +32.92 sigma from Werginz 2024's published 17.3 +/- 3. This is the most extreme
single-prior violation in t0086 + t0088. Audit the ratio computation: (a) confirm
centroid_unnormalised[NAV16_AIS_GBAR] / centroid_unnormalised[NAV16_SOMA_GBAR] is in matching
units (S/cm^2 / S/cm^2 = dimensionless); (b) check the soma Nav lower bound is not pinning the
centroid soma value to a near-zero value, inflating the ratio; (c) check whether the 4 cells
in cluster 1 individually have AIS-to-soma ratios near 116 or whether the centroid is
averaging across heterogeneous values. Pure data analysis on existing JSON outputs; ~30 min
wall-clock, $0 cost. Recommended task types: data-analysis, correction.

</details>

<details>
<summary>🧪 <strong>Audit morphology generator for balancing-factor degeneracy: do
all parameter combinations yield bf=0.500?</strong> (S-0122-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000877`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/paper/10.1371_journal.pcbi.1000877/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0122's top-10 cells all reported Cuntz bf = 0.500 (exact midpoint), raising the question of
whether the t0090/t0092 procedural morphology generator produces topologically balanced trees
by construction across its 14-d parameter space, irrespective of optimiser selection. Action:
take a quasi-random LHS sample of N=200-500 morphology vectors spanning the full 14-d bounds
in constants_morphology.py, build each cell via generate_fixed_morphology (no NEURON sim),
compute Cuntz bf via the t0122 compute_balancing_factor function, and plot the marginal bf
distribution + per-knob bf vs parameter scatter. Verdict: if >95% of cells fall in [0.49,
0.51] the generator is degenerate-balanced and the t0122 Cuntz prediction is generator-driven;
otherwise the bf=0.500 clustering is genuinely selected for by the cytoplasm cost. Recommended
task types: experiment-run, data-analysis, answer-question.

</details>

<details>
<summary>🧪 <strong>Bed B NSGA-II maximising DSI and robustness under +/-10%
channel-density perturbation</strong> (S-0097-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0097-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Source paper** | [`10.1038_nrn1949`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1038_nrn1949/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Directly addresses the researcher's recurring biological-plausibility concern with pure-DSI
maximisation (Marder-style population-statistic robustness is the field-standard treatment).
Falsifiable prediction: high-DSI / high-robustness corner lies along compensatory hyperplanes,
refuting the hypothesis that DSI maximisation drives the optimiser to fragile parameter-space
extremes. Recipe: K=50-200 +/-10% perturbations per Pareto point; minimise SD of DSI. Budget:
36-72 h Vast.ai EPYC at $0.30/h, total $11-22 (multiplies t0091's per-individual cost by
K=50-200) — request explicit $25 budget cap or reduce population/generations.

</details>

<details>
<summary>📊 <strong>Bootstrap loading stability and oblique-rotation sensitivity for
the unfiltered-pool F1 joint factor</strong> (S-0117-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0117-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0117's headline finding is a single factor (F1, 12.6% variance, r_DSI=+0.421, r_PD=+0.352)
and the truncated-cohort verdict rides on it. Total variance dropped from 65.3% (t0116) to
34.9% (t0117), so F1 may be less stable. Draw B=200 bootstrap resamples of the 4431-cell pool,
refit FA(n=10)+varimax, align factors to t0117 by max-cosine, report median +/- IQR of F1's
r_DSI, r_PD, variance, and top-7 loadings. Also rerun with oblique promax (kappa=4) and
n_components=11. Distinct from S-0116-05 (strict cohort where no joint factor existed); this
validates the unfiltered-pool joint factor. Decision: if F1's r_DSI/r_PD 95% CIs straddle 0.3,
the verdict needs softening; if both stay clear of 0.3, the verdict is robust. Recommended
task types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

<details>
<summary>🧪 <strong>Bracketed-cohort sweep at DSI>0.3/0.5/0.7/0.9 to map where the
joint DSI-PD factor disappears</strong> (S-0117-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0117-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0117 confirmed the truncated-cohort artefact: F1 is a joint DSI-PD factor (r_DSI=+0.421,
r_PD=+0.352) at the unfiltered pool, while t0116 (DSI>0.7 AND PD>10) had zero joint factors.
S-0116-02 covers a single point at DSI>0.5; this suggestion is a parametric sweep. Re-run the
t0117 pipeline at four DSI thresholds {0.3, 0.5, 0.7, 0.9} on the same pooled all-cells
parquet, fit varimax FA at each, and plot (a) joint-factor count vs threshold and (b) F1's
r_DSI/r_PD vs threshold. Decision: monotonic crossover between 0.5 and 0.7 means smooth
range-restriction; a sharp cliff means a specific cell class dominates the joint variance.
Recommended task types: data-analysis, comparative-analysis. Cost: <$0.30.

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
<summary>🧪 <strong>Complete S-0112-01: two further random-draw GA seeds at
cadence-10 to lift substrate-rate from 3-seed to 5-seed</strong>
(S-0113-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

S-0112-01 requires >=3 additional GA seeds at cadence-10 to upgrade the substrate-rate
estimate from a 2-point sample to a 5-point sample. t0113 contributed one (random seed 2247)
yielding 0 LEGIT joint-pass cells; the 3-seed sample (44/77/2247) now spans 0.15%-3.29% with
mean 1.26% +/- 1.01% SE, and the 95% CI (-0.73%, 3.25%) brackets BOTH Hay2011 (0.40%) and
Druckmann2007 (0.10%) baselines and cannot reject either. Draw two further random seeds via
secrets.randbelow(10000) (avoid the round-ish-low-number bias of seeds 44, 77 and the curated
set 33/88/99) and run each as a minimum-change replicate of t0113 (same cadence-10, N_GEN=60,
HV-plateau detector, evaluator). Each new seed = one task = one folder = one PR; pool the
5-seed sample for the final substrate-rate report. Recommended task types: experiment-run.
Cost: ~$5 (2 seeds x ~$2-3 each).

</details>

<details>
<summary>🧪 <strong>Connected-component topological basin test (vs KMeans+NMI) on
the t0116 pooled pool</strong> (S-0116-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0116-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0116's basin-connectivity answer rests on KMeans (k=3) silhouette + NMI(cluster,
seed)=0.929/0.889. KMeans forces a partition even on a connected manifold and NMI inflates
with small per-seed counts (seed 77 n=10). A topology-aware test asks the stronger question:
is there any continuous path between seeds' cells in 68-d, or are they genuinely disconnected?
Build a k-NN graph on the standardised 869x68 matrix (k in {5, 10, 20}), extract connected
components via scipy.sparse.csgraph.connected_components, and report (a) component count vs
k_nn, (b) per-component seed composition, (c) persistence of seed-isolation across k_nn
values. Decision: if at k_nn=10 the pool has one giant component containing all 4 seeds,
seed-aligned KMeans clusters are clusters-of-a-connected-manifold (weakens basin-isolation);
if 4+ components each dominated by one seed, basin-isolation is corroborated. Distinct from
S-0112-08 and S-0115-07. Recommended task types: data-analysis. Cost: <$0.20.

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
<summary>🔧 <strong>Correction task to fix three t0076 implementation issues: NEURON
re-init, qNEHVI deprecation, GP input normalisation</strong> (S-0076-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0076-03` |
| **Kind** | technique |
| **Date added** | 2026-05-03 |
| **Source task** | [`t0076_bedb_dsi_firing_rate_mobo`](../../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Three concrete defects identified in the t0076 implementation block additional value from the
existing artefacts. (a) plot_pareto.py calls build_dsgc_cell() multiple times in one Python
process, hitting NEURON's `Exp2NMDA name already exists` non-idempotent loader bug; only 1 of
3 deep-dive PNGs was produced. Fix: subprocess-per-deep-dive. (b) bootstrap.py path resolution
requires the script to run from the project root, not the task folder. Fix: anchor paths via
`arf.scripts.utils.paths`. (c) The MOBO loop used the deprecated
qNoisyExpectedHypervolumeImprovement and passed natural-units bounds to the GP without a
Normalize input transform -- BoTorch warned the fit is suboptimal. Fix: migrate to qLogNEHVI
and wrap inputs in [0, 1]^d. Replay the 430-cell history through the corrected stack and
confirm Pareto front is unchanged or expands. Recommended task types: correction.

</details>

<details>
<summary>📊 <strong>Diagnose evaluator-disagreement bug for cell 77_15_1356: t0117
DSI = 0.93, t0118 canonical protocol = 0 spikes</strong> (S-0118-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0118-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0118 found cell 77_15_1356 (cluster 0, seed 77) was assigned DSI = 0.93 by t0117's NSGA-II
evaluator but produces 0 spikes in either direction under the canonical 1400 ms / -10 mV
threshold protocol (FULL V_m peaks at -51 mV); g_I/g_E ratio = 3.87 (extreme inhibition
dominance). The t0117 DSI score appears to be a finite-sample-noise artefact, unconfirmed.
Investigate: (a) re-run t0117's evaluator on this cell, log per-trial PD and ND spike counts;
(b) re-run with 10 eval-seed pairs and check stability; (c) trace the DSI formula for
PD=1/ND=0 edge cases; (d) report whether other pool cells share this 'high-DSI-but-silent'
pattern. Decision: if >= 1% of pool exhibits this disagreement, t0117/t0116 DSI columns need a
corrections overlay. Recommended task types: data-analysis, correction. Cost: <$0.10.

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
<summary>🧪 <strong>Execute t0115 seed-9354 NSGA-II run as the 5th seed completing
the S-0112-01 substrate-rate batch</strong> (S-0114-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

S-0112-01 requires a 5-seed sample at cadence-10 with auto-stop disabled to upgrade the
substrate-rate estimate from 4-seed (44/77/2247/7755) to 5-seed. t0114 advanced this from 3 to
4 seeds (mean 2.93%, SE 1.86%, 95% CI -0.71% to +6.56% still brackets Hay 2011's 0.40% and
Druckmann 2007's 0.10%). The 5th seed is needed to tighten the SE below the 0.40% Hay
envelope; without it, the substrate-rate point estimate (currently 7.3x above the Hay 2011
envelope) cannot be claimed at p<0.05 significance. Concrete action: execute the
already-scaffolded t0115_seed9354_no_autostop task (seed 9354, auto-stop disabled, cadence-10,
gen ceiling 300, $25 cap), pool the 5-seed results, write the canonical substrate-rate report.
The task scaffold already exists on main with source_suggestion=S-0112-01; this suggestion is
the formal record that the 5th seed is being executed via t0115. Recommended task types:
experiment-run. Cost: ~$1-3 (one Vast.ai EPYC run, matching t0114's $1.13 spend).

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
<summary>🔧 <strong>Finalise (WINDOW=3, REL_THRESHOLD=0.015) HV-plateau detector
defaults across the project</strong> (S-0115-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-01` |
| **Kind** | technique |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0115_seed9354_no_autostop/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0115's 55-gen unstopped HV trajectory adds a fifth datapoint to the offline detector-replay
sweep proposed in S-0113-03 and refined in S-0114-01. The recommended (W*, T*) = (3, 0.015)
pair would fire on t0115 around gen 30-45, inside Mohacsi2024's 20-60 gen convergence band,
and would NOT fire prematurely on t0113's gen-14 trace. Concrete action: globally rewrite the
HV-plateau detector constants in the NSGA-II driver template and the t0024 cell-build
pipeline; document the new defaults in arf/skills/setup-remote-machine and
arf/skills/implementation. Recommended task types: infrastructure-setup. Cost: <$0.05.

</details>

<details>
<summary>📚 <strong>Fix dill checkpoint pool-pickling failure in nsga2_driver.py:
every gen across t0113 failed to dill-pickle</strong> (S-0113-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-02` |
| **Kind** | library |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0113's per-generation dill checkpoint failed on all 14 gens with `NotImplementedError: pool
objects cannot be passed between processes or pickled`. Root cause: pymoo's
`StarmapParallelization` wrapper holds a live `multiprocessing.Pool` reference inside the
Algorithm object that dill cannot serialise. JSON-side resume worked, so runs were not lost,
but the dill resume channel is broken across t0106/t0112/t0113. Fix options: (a) strip
`problem.elementwise_runner` via `__getstate__/__setstate__` and re-attach on restore, (b)
replace dill with cloudpickle, or (c) deprecate the dill checkpoint and make JSON checkpoint
the sole resume mechanism (cleanest). Local-only, reusable across all downstream NSGA-II
tasks. Recommended task types: write-library, infrastructure-setup. Cost: <$0.10.

</details>

<details>
<summary>🧪 <strong>g_I sensitivity sweep on cluster-2 DSGC-competent cells: how does
DSI vary with inhibition strength?</strong> (S-0118-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0118-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0118 found g_I / g_E ratio at peak g_E is the most variable cell-level metric (6 orders of
magnitude, 0.03 to 440), and cluster 2 (s7755) is the only cluster where re-simulated traces
show the DSGC asymmetry mechanism. Take the 5 highest-DSI cluster-2 cells, hold every other
parameter fixed, and sweep global GABA NetCon weight (w_gaba_us) in 7 log steps from 0.1x to
10x (plus symmetric w_ach control). For each (cell, w_gaba_factor) re-run the FULL mode in
PD+ND, extract DSI, peak g_I, g_I/g_E ratio. Plot DSI vs w_gaba per cell. Decision: if DSI
peaks at the same w_gaba factor across cells, the cohort shares a canonical E-I balance; if
optimum varies, the optimiser found cell-specific compensation. ~140 NEURON runs. Recommended
task types: experiment-run, data-analysis. Cost: <$0.20.

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
<summary>📚 <strong>Issue a correction overlay against t0090 marking the procedural
generator as superseded by the t0092 fix</strong> (S-0092-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0092-03` |
| **Kind** | library |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0090 is completed and immutable, but the soma pt3d-collapse bug was committed in t0090's
library asset procedural_dsgc_morphology_generator. The t0092 fix lives in
tasks/t0092_../code/morphology_generator_fix.py as a thin shim. To prevent downstream tasks
(t0091, future Bed-A morph-extended runs, the t0086/t0088 cluster re-score work) from
importing the unpatched t0090 generator and re-introducing the bug, write a correction file
under tasks/t0092_../corrections/ that flags t0090's generator as superseded and points
consumers to t0092's generate_fixed_morphology as the canonical entry point. Aggregator output
should reflect the supersession overlay. Recommended task types: correction.

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
<summary>🧪 <strong>Multi-seed MI/ATP NSGA-II replicate to test seed dependence of
the zero-joint-factor verdict</strong> (S-0125-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0125-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-25 |
| **Source task** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0125's zero-joint MI x ATP varimax verdict is derived from a SINGLE NSGA-II seed (441).
Precedent: t0116 (single seed) found no joint DSI x PD factor; t0117 (4 seeds) recovered one.
The verdict is known to be seed-sensitive on this substrate. Action: replicate t0123 on 2-3
additional non-round GA seeds (POP_SIZE=96, N_EVAL_SEEDS=3, N_GEN_MAX=60, COST_CAP_USD=6,
HV-plateau auto-stop DISABLED per memory feedback_disable_hv_plateau_autostop,
_POOL_RESTART_EVERY=10) and rerun the t0125 cluster + Kaiser-cap varimax pipeline on the
pooled 4-seed pool. Predicted outcome: either F1's ATP loading crosses 0.30 (joint factor
reappears) or stays decoupled (objective-pair-specific verdict confirmed). Budget ~$15-25
Vast.ai EPYC. Recommended task types: experiment-run, data-analysis, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Patch t0080 with an explicit myelinated axon to fix the
soma-vs-axon ATP-share inversion vs Attwell 2001</strong> (S-0125-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0125-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-25 |
| **Source task** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |
| **Source paper** | [`10.1097_00004647-200110000-00001`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/paper/10.1097_00004647-200110000-00001/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0125 finds 76.7% soma / 5.5% AIS / 17.8% dendrite ATP share -- inverted from Attwell &
Laughlin 2001's 4% soma / 82% axon / 14% dendrite rodent-cortical breakdown. methodology_notes
and compare_literature attribute this to t0080 lacking an explicit myelinated axon (only a
procedural AIS). Action: extend the t0080 cell builder with one or two nodes of Ranvier +
myelin segments at realistic R_m (~50 kOhm cm^2), C_m (~0.04 uF/cm^2), and Na/K channel
densities; re-run t0123's MI vs ATP-per-spike NSGA-II at matched compute; re-check
soma/AIS/axon/dendrite ATP shares against Attwell 2001 Table 4 and Sengupta 2010. Test whether
the Pareto front shifts and whether compartment-ATP diversity broadens to match the rodent
picture. Budget ~$10-15 Vast.ai EPYC. Recommended task types: build-model, experiment-run,
comparative-analysis.

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
<summary>🧪 <strong>Per-seed factor analysis on the unfiltered pool: do the 4 seeds
share F1, or are loadings seed-dependent?</strong> (S-0117-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0117-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0117's pooled F1 is the central joint DSI-PD driver (r_DSI=+0.421, r_PD=+0.352, 12.6%
variance). Basin-connectivity (ephys NMI=0.562, morph NMI=0.313) shows seeds still partly
cluster; F1 could be (a) a shared substrate property or (b) a cross-basin confound where
DSI/PD co-vary with seed identity. Refit FA(n=10) + varimax independently on each seed's
unfiltered slice (s44 n=1065, s77 n=654, s7755 n=1686, s9354 n=1026 - all well powered,
n>10*features=680), align factors to t0117 F1 by max-cosine, report per-seed top-10 loadings +
r_DSI/r_PD. Distinct from S-0116-04 (strict cohort where only s7755 had enough cells).
Decision: if all four per-seed analogues hit |r|>0.3 on both axes with the same top loadings,
F1 is a true substrate property; if loadings diverge, F1 is partly a between-seed confound.
Recommended task types: data-analysis. Cost: <$0.20.

</details>

<details>
<summary>📚 <strong>Project-wide DSGC measurement-protocol fix: EPSP_PASSIVE /
IPSP_PASSIVE / FULL trial modes with HH save-and-zero</strong> (S-0055-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-01` |
| **Kind** | library |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Refactor the minimal-DSGC trial code (forked across t0052/t0053/t0054/t0055) to replace the
legacy FULL/E_ONLY/GABA_ONLY trio with a FULL/EPSP_PASSIVE/IPSP_PASSIVE trio. EPSP_PASSIVE and
IPSP_PASSIVE must save-and-zero soma+AIS gnabar_hh and gkbar_hh so the recorded EPSP and IPSP
traces are clean synaptic envelopes, not spike-contaminated traces (the user-flagged bug that
made t0054 REQ-20 and t0055 REQ-20 return null at every gNMDA). Drop the per-synapse
activation-time histogram. Confirm and standardize the trial length with the user (1400 vs
1500 ms vs longer window for EPSP-decay metrics; 3000-5000 ms recommended by S-0054-03). Pass
criterion: EPSP/IPSP traces from a representative gNMDA value show no Na+ spikes; HH-on FULL
trace is unchanged within 1e-6 mV vs current code. Recommended task types: write-library,
infrastructure-setup. This is a project-wide infrastructure fix that benefits every future
DSGC task.

</details>

<details>
<summary>🧪 <strong>Re-run seeds 77 and 2247 with HV-plateau auto-stop DISABLED to
test the censoring-artefact hypothesis</strong> (S-0121-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0121-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0121_5seed_substrate_rate_canonical_report`](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The 5-seed canonical estimate's lower tail is dominated by seed 77 (7 LEGIT, gen 21 stop) and
seed 2247 (0 LEGIT, gen 14 stop, 6 gens below Mohacsi 2024's 20-60 convergence band). Both ran
under legacy auto-stop-enabled; t0121 flags both as plausible censoring artefacts. The
project's now-current policy (memory note 'Disable HV-plateau auto-stop') is to DISABLE
auto-stop. Concrete action: replicate t0112 (seed 77) and t0113 (seed 2247) with auto-stop
DISABLED, _POOL_RESTART_EVERY=10, gen ceiling 300, budget cap matching t0114 / t0115.
Decision: if either seed crosses the Hay 0.40% envelope, re-estimate the canonical 5-seed mean
and close the censoring caveat. If both stay below 0.40% at full budget, the seeds are
substrate-sparse not censored. Distinct from S-0114-08 (which tests the offline '(W=3,
T=0.015)' detector, not disable-auto-stop). Recommended task types: experiment-run.

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
<summary>🧪 <strong>Re-simulate t0118 stratified sample on t0116 strict cohort (DSI >
0.7 AND PD > 10) for a good-DSGC trace gallery</strong> (S-0118-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0118-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0118 found the unfiltered pool is heavily DSI ~ 0; only cluster 2 (s7755) supplied DSI >= 0.2
cells, so the per-cluster trace grids do not show good DSGC behaviour for clusters 0/1/3.
Apply the identical 10-per-cluster stratified-by-DSI-x-PD sampler and 3-mode trio protocol to
t0116's strict 869-cell cohort, then re-cluster those cells with t0116's k=3 partition.
Outcome: 30 cells (10 per t0116 cluster) whose traces actually show the canonical DSGC
asymmetry mechanism across multiple clusters, not just one. Distinct from t0118 (unfiltered
pool) and from S-0116-* (which stay in FA/clustering space without re-simulating). Recommended
task types: experiment-run, data-analysis. Cost: <$0.20.

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
<summary>🔧 <strong>Refresh t0091 task description + dependencies to reference t0092
fix and t0093 correction overlay</strong> (S-0093-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0093-01` |
| **Kind** | technique |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0091_morphology_extended_nsga2_v1 is currently `not_started` with status referencing t0090's
procedural_dsgc_morphology_generator directly (task_description.md lines 6, 32, 88, 190, 208)
and dependencies={t0024,t0078,t0080,t0081,t0083,t0086,t0088,t0090} -- no t0092 or t0093
dependency. Since t0093 issues a `replace` correction redirecting that library to t0092's
procedural_dsgc_morphology_generator_fix, t0091 must be updated before launch: (a) add
`t0092_diagnose_morphology_generator_silence` and `t0093_resweep_and_t0090_correction` to its
`dependencies` list; (b) replace import references to
`tasks.t0090_..code.generator.generate_morphology` with
`tasks.t0092_..code.morphology_generator_fix.generate_fixed_morphology`; (c) document in the
task description that the procedural cell is canonically the t0092 fix per C-0093-01. Without
this, t0091 would re-import the unpatched generator and re-introduce the soma-pt3d collapse
bug. Recommended task types: correction.

</details>

<details>
<summary>🧪 <strong>Relaxed-cohort (DSI > 0.5) pooled re-analysis to test
truncated-cohort artefact on joint-factor decoupling</strong> (S-0116-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0116-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0116's strict DSI>0.7 cohort produced no joint factor (|r|>0.3 on both DSI and PD). t0110
documented that strict-cohort filters truncate joint variance (restriction-of-range); t0108's
strict cohort identified F10 as a joint factor, t0110's relaxed cohort found a different sign
pattern. Re-run the t0116 pipeline (4 or 5 seeds, depending on S-0116-01) with the cohort
filter relaxed from DSI>0.7 to DSI>0.5 (matching t0108/t0110); regenerate the factor heatmap
and per-factor DSI/PD correlations. Decision: if a joint factor emerges at the relaxed
threshold, t0116's 'no joint factor' is a truncated-cohort artefact and the latent-drivers
answer must be re-interpreted conditional on cohort definition; if no joint factor emerges
even at DSI>0.5, the multi-seed pool truly lacks a shared trade-off axis. Recommended task
types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

<details>
<summary>🧪 <strong>Replicate t0122 cytoplasm-volume NSGA-II on 2-3 additional GA
seeds for substrate-rate estimate</strong> (S-0122-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000877`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/paper/10.1371_journal.pcbi.1000877/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0122 ran one GA seed (1524) and reported 0.17% LEGIT acceptance (10/5760) with 10/10 top-DSI
cells in the Cuntz [0.2, 0.7] band. Mirroring the S-0112-01 pattern, the headline must be
replicated on 2-3 more random GA seeds drawn via secrets.randbelow(10000) (non-round) before
drawing population-statistic conclusions. Action: launch 2-3 independent runs of the t0122
substrate (same 68-d Bed B + 14-d morph, F=[-dsi, +volume_um3], hard constants POP_SIZE=96,
N_EVAL_SEEDS=3, N_GEN_MAX=60, COST_CAP_USD=6.0, tightened guard pd_spikes_sum<3), aggregate
per-seed LEGIT rates and Cuntz top-10 bf distributions, and compute a 3-seed mean +- SD
comparable to t0121's 5-seed PD-rate estimate. Outcome: substrate-rate central estimate for
the cytoplasm-volume axis, and answers whether bf=0.500 clustering is seed-invariant.
Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Rerun MI-ATP NSGA-II with richer stimulus + PD-rate floor to
fix Strong-Bialek bits/s = 0</strong> (S-0123-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0123-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **Source paper** | [`10.1103_PhysRevLett.80.197`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/paper/10.1103_PhysRevLett.80.197/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0123's post-hoc Strong-Bialek bits/s = 0 for all 10 top-Pareto cells traces to a protocol
mismatch: count-MI converged on cells producing ~3 PD spikes per 1400 ms trial (silence-guard
boundary) where binary spike-time words are degenerate at every T <= 100 ms; Niven 2007
comparison returns Insufficient evidence. Action: fork the t0123 substrate (same 68-d Bed B +
14-d morph, same two-tier MI + Sengupta ATP recipe) with three upgrades: (a) extend trial
length to 3000-5000 ms so the 1/T extrapolation populates non-trivial spike-time words; (b)
tighten the silence guard to a PD-rate floor pd_rate_hz>=10 Hz so count-MI cannot exploit the
silence boundary; (c) optionally add NMDA-mediated burst priming (t0062-style) to lift
baseline firing into the spike-time-informative regime. Predict bits/s becomes positive and
the Niven comparison becomes testable. Budget ~$5-8 Vast.ai EPYC. Recommended task types:
experiment-run, data-analysis, comparative-analysis.

</details>

<details>
<summary>📚 <strong>Resolve recurring dill-checkpoint pool-pickling failure: fix or
formally retire dill resume channel</strong> (S-0114-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-07` |
| **Kind** | library |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0114's per-generation dill checkpoint failed on all 62 gens with the same NotImplementedError
('pool objects cannot be passed between processes or pickled') documented in S-0113-02.
JSON-side resume works end-to-end so no runs were lost, but every gen logs a multi-line dill
traceback polluting the step log. Root cause: pymoo's StarmapParallelization wrapper holds a
live multiprocessing.Pool that dill cannot serialise. Choose one: (a)
__getstate__/__setstate__ on the wrapper to strip and re-attach problem.elementwise_runner,
(b) swap dill for cloudpickle, or (c) deprecate the dill channel entirely and document JSON as
the sole resume mechanism — removes log noise at zero risk. RECOMMENDED: (c) — JSON has been
the only working resume channel across t0106/t0112/t0113/t0114; dill has produced zero
successful resumes. Distinct from S-0113-02: t0114 confirms recurrence. Recommended task
types: write-library, infrastructure-setup. Cost: <$0.10.

</details>

<details>
<summary>📊 <strong>Resolve units mismatch between t0080 gnmda_dend NetCon weight and
Sivyer 2013 per-spine conductance</strong> (S-0086-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0086-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0086_robustness_cluster_bio_comparison`](../../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) |
| **Source paper** | [`sivyer_2013`](../../../tasks/t0086_robustness_cluster_bio_comparison/assets/paper/sivyer_2013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0086's NMDA exotic verdict (>85 sigma above Sivyer 2013) is so extreme that it likely
partially reflects a units / scope mismatch rather than a genuinely outlier biological
mechanism. The t0080 ParameterVector encoding `gnmda_dend` is the NetCon weight used in the
t0080 Exp2NMDA mechanism, while Sivyer 2013's value is a per-spine synaptic conductance
measured in voltage-clamp on RGC dendritic spines. These may differ by a per-cell area
normalisation or by an effective open-channel-fraction factor. Run a calibration ablation:
take a single t0080 cell, vary `gnmda_dend` from 1e-5 to 1e-2 uS, measure the per-spine
effective open conductance (from the NEURON state during a stimulus), and produce a
calibration curve mapping NetCon weight to per-spine conductance. Then re-score the t0086
clusters against Sivyer 2013 in the corrected units. Expected cost: ~$0.30 USD (1 hour CPU).
Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Shrink AIS diameter to 0.5 μm and re-test channel
insertions</strong> (S-0069-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0069-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

Real RGC AIS diameters cluster around 0.4-0.8 μm; t0069 used 1 μm. A narrower AIS has higher
input resistance per unit area, so the same gbar of an AIS-localised Nav or Kv channel
produces a much larger local depolarisation. Test: rebuild the AIS at diam=0.5 μm (keep L=30
μm), keep all other parameters identical to t0069, re-run the 16-condition × 2-direction ×
5-seed sweep. Combined with S-0069-01 (halved somatic Na), this should be the configuration
that finally exposes AIS-localised Kv3 / Kv4 effects. Compute: ~10 min.

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
<summary>🧪 <strong>3-objective NSGA-II maximising (MI, DSI) and minimising
ATP-per-spike on same 68-d substrate</strong> (S-0123-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0123-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000840`](../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/assets/paper/10.1371_journal.pcbi.1000840/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0123 decoupled function (MI) from selectivity (DSI) to make the Pareto front comparable to
Niven 2007; side effect: Pareto-front DSI = 0.13-0.40, well below t0122's high-DSI front (DSI
= 0.97), so the project's first-question DSGC selectivity mission is not served. Distinct from
S-0097-04 (2-obj DSI + MI without ATP): this is a 3-objective extension that asks whether MI,
DSI, and ATP-per-spike are mutually compatible or fundamentally trade off. Action: fork the
t0123 evaluator to emit out['F'] = [-mi_count_bits, -dsi_vector_sum, +atp_per_spike_molecules]
(n_obj=3); keep all hard constants (POP_SIZE=96, N_EVAL_SEEDS=3, N_GEN_MAX=60, N_DIRECTIONS=4,
COST_CAP_USD=6.0, _POOL_RESTART_EVERY=10, HV_PLATEAU_AUTO_STOP=False); adjust REF_POINT_HV /
HV_UTOPIA to 3 entries; draw a fresh non-round GA seed; run on Vast.ai EPYC. Predict the
surface either separates high-DSI / low-ATP and high-MI / low-ATP clusters or collapses to a
2-d ridge. Recommended task types: experiment-run, data-analysis.

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
<summary>🧪 <strong>5-seed unfiltered-pool re-analysis (adding t0113 seed 2247) to
test joint-factor robustness</strong> (S-0117-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0117-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0117 used the same 4 seeds as t0116 (44/77/7755/9354) and deliberately excluded t0113 (seed
2247) to isolate the cohort-filter effect. With the joint factor now confirmed, the next
question is whether F1 survives the addition of a fifth independent seed. Re-run t0117's
pipeline end-to-end with t0113 as the fifth source (no DSI/PD filter, dedup at 6-decimal
vector convention, union-pool standardiser), regenerate the loadings heatmap and
factor_correlations.csv. Distinct from S-0116-01 (5-seed on the strict cohort, addresses basin
isolation); this 5-seed run addresses joint-factor robustness. Decision: if F1 still passes
|r|>0.3 on both axes with the same top loadings, the truncated-cohort verdict is seed-robust;
if F1 collapses or shuffles, the joint factor is partly 4-seed-specific. Recommended task
types: data-analysis, comparative-analysis. Cost: <$0.25.

</details>

<details>
<summary>📊 <strong>8-direction polar re-evaluation of t0113's 2 silence-guard
DSI=1.0 cells (mirrors S-0112-05 for t0113)</strong> (S-0113-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0113's 2 asset-declared joint-pass cells are both silence-guard DSI=1.0 saturations (1 PD
spike / 0 ND spikes at PD=35.0 Hz and PD=45.24 Hz; the latter is also a strict Pareto cell).
t0107 established that 2-direction ratio DSI overstates 8-direction vector-sum DSI by ~0.42
absolute on t0106 high-DSI cells, but that offset was measured on legit cells not
silence-guard saturations. Re-evaluate both t0113 cells at 8 directions (every 45 deg) using
t0107's protocol with N_EVAL_SEEDS matched. Decision: if the cells fire >=1 spike in >=2
non-PD directions, they are not silence-only and the silence-guard threshold needs revisiting;
otherwise they are confirmed artefacts and should be excluded from the substrate-rate
denominator. Distinct from S-0112-05 (t0112 cells) and S-0106-03 (t0106 cells). Recommended
task types: experiment-run, comparative-analysis. Cost: <$0.50.

</details>

<details>
<summary>📊 <strong>8-direction polar re-evaluation of t0114's 6 strict Pareto cells
(mirrors S-0112-05 / S-0113-04)</strong> (S-0114-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0114's 6 strict Pareto cells span the DSI/PD-rate frontier corner: best LEGIT DSI=0.9926 at
PD=63.81 Hz (cell_id 1), best PD=112.86 Hz at DSI=0.0271 (cell_id 5), and DSI=0.9873 /
PD=111.67 Hz (cell_id 2) — the first 4-seed run to produce DSI~0.99 AND PD>100 Hz
simultaneously. t0107 found 2-direction ratio DSI overstates 8-direction vector-sum DSI by
~0.42 absolute on t0106 high-DSI cells; applied here yields ~0.57 (vs Trenholm2013's 0.76 /
Oesch2005's 0.74 baselines). Concrete action: re-evaluate all 6 strict Pareto cells (plus 2
silence-guard ceiling cells for completeness) at 8 directions every 45 deg using t0107's
protocol with matched N_EVAL_SEEDS. Decision: confirm whether the 4-seed best legit cell is
biologically plausible under 8-direction vector-sum DSI. Distinct from S-0112-05 / S-0113-04 /
S-0106-03. Recommended task types: experiment-run, comparative-analysis. Cost: <$0.50.

</details>

<details>
<summary>📊 <strong>8-direction polar re-evaluation of t0115's strict Pareto cells
(mirrors S-0114-03 / S-0112-05)</strong> (S-0115-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | [`10.1167_jov.13.7.2`](../../../tasks/t0115_seed9354_no_autostop/assets/paper/10.1167_jov.13.7.2/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0115's 23 strict Pareto cells span the DSI/PD-rate frontier: best LEGIT DSI=0.9833 at
PD=28.33 Hz, best PD=89.29 Hz at DSI~0, and DSI=0.7899 / PD=50.71 Hz (best combined). t0107
found 2-direction ratio DSI overstates 8-direction vector-sum DSI by ~0.42 absolute on t0106
high-DSI cells; applied here yields ~0.56 (vs Trenholm2013's 0.76 / Oesch2005's 0.74
baselines). Concrete action: re-evaluate all 23 t0115 strict Pareto cells at 8 directions
every 45 deg using t0107's protocol. Distinct from S-0114-03 (t0114 Pareto cells), S-0112-05
(t0112 cells), and S-0106-03 (t0106 cells); together these would cover the full 4-rich-seed
cohort. Recommended task types: experiment-run, comparative-analysis. Cost: <$1.00.

</details>

<details>
<summary>📚 <strong>Add a generator-side regression test battery covering
coincident-pt3d edge cases beyond the BedB base point</strong> (S-0092-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0092-05` |
| **Kind** | library |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0092 unit-test suite (4 tests) covers determinism, no-NaN on the BedB base point, soma
area, and pt3d z-axis. It does not exercise the broader space of generator inputs that could
trigger coincident-pt3d collapses elsewhere in the cell (e.g. degenerate dendrite stubs at
extreme branch_prob_per_um values, AIS sections with zero asymmetry-induced offset, or
interaction between negative branch_length_cv and the asymmetry transform). Author a
regression test battery that calls generate_fixed_morphology on a Latin-hypercube sample of
~50 points across the 14-knob space and asserts that every section has sec.L>1 um and
sec.area()>10 um^2 in NEURON. This catches future bugs in the generator before they cascade
through t0091's NSGA-II loop. Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Add a path-distance helper to t0046's modeldb_189347_dsgc_exact
library using the two-segment h.distance form</strong> (S-0050-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0050-03` |
| **Kind** | library |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

Bonus finding from t0050: NEURON 8.2.7 Python's legacy single-arg form h.distance(0, sec(0.5))
does NOT reliably set the path-distance origin (returns 0.5 instead of resetting). The audit
worked around this using the two-segment form h.distance(soma_seg, syn_seg). Add a small
path_distance_um(soma_seg, target_seg) helper to t0046's library (modeldb_189347_dsgc_exact)
wrapping the robust form, plus a docstring note explaining the API quirk. Other DSGC tasks
computing path distances (e.g., S-0049-05's intermediate SEClamp dendritic locations, future
spatial audits) will then avoid silent miscomputation. Pure code/library task; no experiments
required. Recommended task types: write-library.

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
<summary>📚 <strong>Add a project-wide python-pptx slide-deck builder library so
figure packs reuse a common deck assembler</strong> (S-0105-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-04` |
| **Kind** | library |
| **Date added** | 2026-05-13 |
| **Source task** | [`t0105_preliminary_figures_report`](../../../overview/tasks/task_pages/t0105_preliminary_figures_report.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0105 introduced python-pptx>=1.0 and implemented
tasks/t0105_preliminary_figures_report/code/build_slides.py as a task-local
one-figure-per-slide deck assembler with caption + source-task citation in slide notes.
Multiple downstream tasks (per-report figure packs, brainstorm decks, t0104 follow-up, future
MOBO writeups) will want the same machinery. Package build_slides.py as a reusable library
asset under a host task -- expose build_deck(slides: list[SlideSpec], output_path: Path) and a
SlideSpec dataclass (image_path, caption, notes, layout), register a details.json under
assets/library/, and document the import path. Downstream tasks then call the library instead
of re-implementing python-pptx layout per task. Recommended task types: write-library.

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
<summary>📚 <strong>Add an iMK801 analogue MOD modification (selective dendritic
NMDAR block) to enable Fig 8 AP5 reproduction</strong> (S-0046-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-03` |
| **Kind** | library |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Author a new MOD mechanism (or extend `bipolarNMDA.mod`) that selectively blocks NMDAR
conductance in dendritic compartments while leaving somatic NMDAR + AMPA intact, mirroring the
paper's intracellular MK801 (iMK801) protocol. The current AP5 analogue used in t0046
(`b2gnmda = 0`) removes ALL NMDAR contribution and silences the cell entirely (DSI = 0 under
AP5); the paper's iMK801 leaves PD spiking, allowing the qualitative 'DSI preserved under AP5'
Fig 8 claim to be reproduced. This unblocks a faithful Fig 8 AP5 reproduction and resolves the
AP5-vs-iMK801 mechanistic divergence catalogued as discrepancy 1 of 12 in t0046's audit.
Recommended task types: write-library, experiment-run.

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
<summary>📚 <strong>Adopt t0112 pool_restart_every=10 as the default for all
downstream NEURON-pymoo NSGA-II tasks</strong> (S-0112-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0112-07` |
| **Kind** | library |
| **Date added** | 2026-05-19 |
| **Source task** | [`t0112_t0106_seed77_replicate`](../../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0112 demonstrated a 3.5x per-generation wall-clock speedup (620s/gen vs t0106's 2,167s/gen)
at no algorithmic cost to frontier geometry: best DSI 0.9535 vs t0106's 0.9606 (within noise)
and best PD 114.76 Hz vs 122.62 Hz (94%). The change is one line (_POOL_RESTART_EVERY: int =
10) in nsga2_driver.py. Promote it from a t0112-only override to the project default once
S-0112-02 isolates the cadence effect from seed variance. Concretely: update the canonical
NSGA-II driver template (or the PerGenerationPoolRestart library asset proposed by S-0106-05)
to default to cadence=10 with cadence=25 retained as an opt-in legacy mode. Document the
speedup in the driver docstring and reference S-0112-02 as the validation evidence.
Recommended task types: write-library, infrastructure-setup. Cost: <$0.10 (local code change +
docs; gated on S-0112-02 passing).

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
<summary>📊 <strong>alt_topology basin deep-dive: identify morphology features
distinguishing alt_topology vs bedb_like Pareto cells</strong> (S-0091-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

16 alt_topology cells survived in the 57-cell Pareto (parity with bedb_like's 20), and the
only strict joint-pass cell (DSI 0.51, PD 35 Hz, robust 0.79) is nearest to alt_topology in
14-d morphology space. creative_thinking.md flags this as evidence for at least two distinct
morphological basins of joint-pass-adjacency, but the 14-d signature distinguishing
alt_topology from bedb_like has not been quantified. Pure data analysis on pareto_front.json +
warm_start_population.json: PCA + UMAP on the 14-d morph vectors restricted to Pareto cells
colour-coded by anchor; per-feature Mann-Whitney U tests on each of the 14 knobs; identify the
top 3-5 discriminative features (likely num_primary_branches, max_strahler_depth,
mean_branching_angle); cross-reference with biological scorecard rows. Cost: $0. Recommended
task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Alternative biological-cost NSGA-II: replace cytoplasm volume
with membrane area as the second objective</strong> (S-0122-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-06` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000877`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/paper/10.1371_journal.pcbi.1000877/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0122's cytoplasm volume (sum(pi*(diam/2)^2 * L)) is a proxy for Cuntz 2010's wiring cost
(total wiring length), tight only when diameters are uniform. A more biologically motivated
cost is membrane area (sum(pi * diam * L)), which dominates ion-channel-density-driven ATP
cost via Na+/K+ pump count. Action: fork the t0122 substrate, add compute_membrane_area_um2
(one-line variation on compute_cytoplasm_volume_um3), set out['F'] = [-dsi,
+membrane_area_um2], keep other constants identical, draw a fresh non-round GA seed, run
NSGA-II 60 gens on the same EPYC substrate. Prediction: membrane-area minimisation produces a
DIFFERENT cell cohort (smaller diameter / longer length trade-off vs t0122's small diameter
AND small length) but a SIMILAR DSI ceiling (within 0.01 absolute of t0122's 0.9753).
Recommended task types: experiment-run, data-analysis.

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
<summary>📊 <strong>Audit project DSGC family for systemic e_GABA = v_rest design
choice</strong> (S-0066-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0066-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-30 |
| **Source task** | [`t0066_t0024_epsp_ipsp_vm_protocol`](../../../overview/tasks/task_pages/t0066_t0024_epsp_ipsp_vm_protocol.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0066 confirmed that both deposited Poleg-Polsky 2016 (t0065) and de Rosenroll 2026 (t0066)
DSGC implementations independently use e_GABA = v_rest = -60 mV, producing pure shunting
inhibition. This is a recurring DSGC modelling pattern, not an idiosyncrasy. Conduct a
project-wide audit: read constants/parameter files for ALL DSGC ports (t0008, t0023 if
completed, the from-scratch family t0052-t0059) and record (V_INIT, ELEAK, GABA_EREV) tuples.
Map the design choice across ports. If any port uses e_GABA != v_rest, that becomes a useful
comparison point for testing whether direction selectivity persists when inhibition is
hyperpolarising. Output: a single answer asset summarising the audit with recommendations on
which port (if any) implements biologically realistic Cl- reversal physics.

</details>

<details>
<summary>🔧 <strong>Backport: regenerate t0114's top50_morphologies_seed7755.png with
full dendrite trees (correction task)</strong> (S-0115-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-05` |
| **Kind** | technique |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0114's top50_morphologies_seed7755.png drew only the soma points, not the full dendrite tree,
making the chart visually useless for characterising the morphology distribution of high-yield
cells. t0115 used the corrected build_top50_morphologies.py helper that walks every section in
the NEURON cell object via generate_fixed_morphology -> result.section_endpoints_xy ->
matplotlib LineCollection. Concrete action: create a small correction task that regenerates
the t0114 chart using the t0115 helper, files a corrections/ overlay updating the t0114 chart
path, and verifies via Read tool that subplots show branching trees, not dots. Recommended
task types: correction. Cost: <$0.05.

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
<summary>🧪 <strong>Bed B NSGA-II maximising DSI and information transfer
rate</strong> (S-0097-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0097-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Source paper** | [`10.1103_PhysRevLett.80.197`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Recipe is well-established (Strong-Bialek direct method with 1/T extrapolation) and validates
against Dhingra & Smith 2004's ~60% gray-level loss benchmark. Caveat: the project's
8-direction protocol has only 3 bits of stimulus uncertainty, so the MI estimator's ceiling is
3 bits per trial regardless of spike train. Validate the recipe against existing DSGC trial
output before launching the full MOBO. Budget: 18-36 h Vast.ai EPYC at $0.30/h, total $5-11.
MI is post-hoc on simulation output, so cost overhead is mostly in extra population to
populate the MI Pareto direction. Priority dropped to medium pending recipe validation.

</details>

<details>
<summary>📊 <strong>Benchmark NetPyNE harness overhead vs raw NEURON across problem
sizes</strong> (S-0007-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

At the single-compartment size, NetPyNE's setup is ~6× slower than raw NEURON (38.7 ms vs 6.7
ms) but runtime is indistinguishable. Scan both harnesses across realistic retinal network
sizes (1, 10, 100, 1000 cells; dense and sparse connectivity) to quantify where NetPyNE's cost
becomes significant for downstream t0008 / t0010 / t0011 runs, and decide whether any hot-loop
experiments should stay in raw NEURON.

</details>

<details>
<summary>🧪 <strong>Benchmark NEURON vs Arbor on the project's actual DSGC
morphology</strong> (S-0003-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Once a DSGC model runs in NEURON (via S-0003-02), port the same morphology and channel set to
Arbor 0.12.0 and measure single-cell simulation wall-clock on the project's workstation.
Third-party benchmarks claim Arbor is 7-12x faster; this task validates that claim on our
actual use case and records the real cost of the NMODL `modcc` translation that t0003 flagged
as the main Arbor adoption risk.

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
<summary>🧪 <strong>BK + SK co-expression sweep: linear-add vs saturation</strong>
(S-0074-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

BK and SK produced very similar narrowing patterns at low / med densities (delta_HWHM ~ -0.2
to -7 deg, delta_vec_DSI ~ -0.02 to -0.05 — within 1 SD of each other). Creative-thinking
proposed they may share a Ca-pool-driven mechanism. Test: 4-condition co-expression sweep —
{BK_med, SK_med, BK_med + SK_med, baseline} × 12 angles × 5 seeds = 240 trials, ~10 min
compute. If BK + SK co-expression delta equals the linear sum of single-channel deltas, the
channels are non-interacting (different downstream effects); if the combined delta saturates
near the larger single-channel delta, they share a Ca-pool-driven mechanism. Either outcome
teaches us about BK / SK co-expression in DSGCs and informs the t0075 dendritic-active
follow-up.

</details>

<details>
<summary>📊 <strong>Bootstrap loading stability for the single-seed MI factors to
bracket the 0.358 / 0.205 joint-threshold gap</strong> (S-0125-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0125-08` |
| **Kind** | evaluation |
| **Date added** | 2026-05-25 |
| **Source task** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0125's zero-joint verdict rides on F1's r_MI = -0.358 (above threshold) paired with r_ATP =
+0.205 (below threshold) -- ATP only 0.095 below the 0.30 cutoff. Verdict could flip under
resampling. Distinct from S-0117-03 (bootstrap on t0117 4-seed DSI x PD F1): this is the MI x
ATP single-seed analogue. Action: on the existing t0125 standardiser and 5760-cell parquet,
draw B = 500 bootstrap resamples, refit FA(n=10) + varimax, report (a) per-factor 5/50/95
percentile loadings on every 68-d parameter; (b) per-factor 5/50/95 percentile r vs MI and
ATP; (c) probability that >=1 factor crosses |r| > 0.30 on both axes per resample; (d)
threshold sensitivity at 0.20, 0.25, 0.30, 0.35. Bounds the joint-factor verdict and produces
the threshold-sensitivity curve flagged in compare_literature. CPU-only. Recommended task
types: data-analysis, answer-question.

</details>

<details>
<summary>📊 <strong>Bootstrap loading-stability and oblique-rotation sensitivity for
the t0116 10-factor varimax solution</strong> (S-0116-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0116-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The latent-drivers answer's Limitations lists three FA-stability concerns: (a) n=869 with 68
features is borderline for FA-loading stability, (b) varimax forces orthogonal factors so F1
and F3 cannot share loadings, (c) the Kaiser cap at 10 left one eigenvalue>1 unmodelled
(11-10=1). t0105 ran bootstrap loading recovery; t0116 did not. Concrete action: (i) draw
B=200 bootstrap resamples of the 869-cell pool with replacement, refit FA(n=10) + varimax on
each, align factors to t0116 by max-cosine-similarity, and report median +/- IQR loadings per
factor x feature in a stability heatmap; (ii) rerun with oblique promax rotation (kappa=4) and
report new top-7 loadings and joint-factor flags; (iii) refit with n_components=11. Decision:
if F1/F3 top loadings change rank under bootstrap or promax (e.g., morphology drops out of
F1), the t0116 mixed/pure classification should be downgraded; if structure persists, it is
robust. Recommended task types: data-analysis. Cost: <$0.20.

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
<summary>📚 <strong>Build a reusable SWC -> NEURON/NetPyNE/Arbor section-translator
library for dsgc-baseline-morphology</strong> (S-0005-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-04` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Every downstream compartmental-modelling task in this project will need to load the
dsgc-baseline-morphology SWC into a simulator and produce a section/segment graph indexed by
SWC compartment id, soma reference, and per-section parent links. NEURON's built-in Import3d
handling of CNG SWCs is fragile (soma-3point convention, branch-point splitting, axon stubs)
and other simulators have their own quirks (NetPyNE's netParams.cellParams, Arbor's morphology
builder). Write a small library asset that exposes a pure-function
load_dsgc_morphology(simulator: str) -> SimulatorMorphology API with verified-equivalent
loaders for NEURON, NetPyNE, and Arbor, plus a smoke test that compares total path length and
compartment count across loaders against validate_swc.py. This eliminates per-task SWC-loading
bugs and keeps morphology choice swappable when S-0005-03 lands. Recommended task types:
write-library.

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
<summary>🔧 <strong>Calibrate active Nav / Kv / Ih densities to match Poleg-Polsky
2016 spike shape and distal Ih sag</strong> (S-0009-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-03` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Geometry alone does not recover the Schachter Rin targets; the residual gap needs active and
passive membrane parameters. On dsgc-baseline-morphology-calibrated, install Fohlmeister-like
Nav, delayed-rectifier Kv, and Ih channels and fit their densities (somatic vs dendritic) so
that (1) the somatic action-potential shape (halfwidth, peak, afterhyperpolarisation) matches
Poleg-Polsky 2016 Figure 2, and (2) the voltage-sag response to hyperpolarising current at
distal tips matches the Ih-driven sag amplitude reported in Schachter 2010. This is distinct
from S-0002-01 (DSI-maximising g_Na/g_K grid) and S-0002-02 (passive-vs-active DSI ablation):
it tunes channel densities against single-cell electrophysiological waveforms, not tuning
curves. Output: a library asset exposing the fitted mechanism list for reuse in the DSI
experiments. Recommended task types: experiment-run, feature-engineering.

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
<summary>🧪 <strong>Characterise t0114's high-DSI high-PD Pareto cluster:
morphologies, basin shape, ancestry</strong> (S-0114-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0114's strict Pareto front and top-50 LEGIT joint-pass set show a notable cluster (gen 47-61)
with DSI in [0.987, 0.993] and PD in [59, 112] Hz — bracketed by Pareto cell_id 1 (DSI=0.9926,
PD=63.81 Hz) and cell_id 2 (DSI=0.9873, PD=111.67 Hz). The cluster looks like a Pareto-front
'fissure': simultaneously high-DSI AND high-PD configurations absent from t0106 (best legit
DSI at PD=49 Hz, not 100+). Concrete action: extract cluster cells (LEGIT joint-pass with DSI
> 0.95 AND PD > 60 Hz, ~30-50 expected), compute (a) z-scored 68-d nearest-neighbour distances
within the cluster, (b) NSGA-II ancestry / lineage from generation provenance, (c)
per-parameter median +/- IQR to find tightly-constrained vs free dimensions. Decision: if 5+
parameters are tightly constrained, name the cluster as a 'high-PD high-DSI basin' for seeded
re-exploration. Distinct from S-0112-08 and S-0113-08. Recommended task types: data-analysis,
comparative-analysis. Cost: <$0.30.

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
<summary>📊 <strong>Correct t0033 answer asset: confirm 2-D morphology
parameterisation</strong> (S-0041-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0041-03` |
| **Kind** | evaluation |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0041 falsified the 1-D L/lambda collapse hypothesis; t0033's answer asset should incorporate
the finding that morphology requires 2-D (raw length x raw diameter) parameterisation rather
than a 1-D compression. Create a lightweight correction task that writes a correction file
against t0033 answering: yes the 25-free-parameter design is appropriate; no the morphology
dimension cannot be reduced to 1-D.

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
<summary>📊 <strong>Decompose t0122's cytoplasm volume into soma vs dendrites vs AIS
contributions across the Pareto front</strong> (S-0122-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-05` |
| **Kind** | evaluation |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0122 computes cytoplasm volume as the sum over [soma, *all_dends, ais_proximal, ais_distal]
and reports only the scalar total. The t0122 compute_per_section_volume_breakdown function
returns {soma_um3, dendrites_um3, ais_um3} per cell but the breakdown was not surfaced.
Whether the optimiser shrinks soma, dendrites, or AIS to drive volume down is unresolved, and
the answer interacts with the bf=0.500 finding (if dendrite volume dominates, bf reflects
dendritic geometry; if soma/AIS dominate, bf is decoupled from the optimised cost). Action:
re-run compute_per_section_volume_breakdown on every cell in all_evaluations_seed1524.json.gz,
write a 3-panel violin plot (soma/dendrites/ais) split by LEGIT vs silence-corner vs
non-LEGIT, and report the per-section fractions for the top-10 cells. Recommended task types:
data-analysis.

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
<summary>🧪 <strong>Diagnose and fix t0022's 15 Hz peak-firing cap (inherited
AMPA-only drive issue)</strong> (S-0039-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Peak firing at the preferred direction is 15 Hz across the diameter sweep, well below
Schachter2010's 40-80 Hz baseline. The same 15 Hz ceiling appeared in t0030 at 12 nS GABA, so
it is a pre-existing t0022 drive issue, not a diameter or GABA artefact. Duplicate of
S-0037-04 but now blocking quantitative literature comparisons for the discriminator task too.
Likely fix: add NMDA back into the E-I schedule, or boost AMPA conductance, or both. Run a
diagnostic trace of soma voltage at preferred direction and compare to Schachter2010's
published traces.

</details>

<details>
<summary>🧪 <strong>Diagnose and fix the low peak firing rate in t0022 (15 Hz vs
40-80 Hz Schachter2010)</strong> (S-0037-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0037-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0037_null_gaba_reduction_ladder_t0022`](../../../overview/tasks/task_pages/t0037_null_gaba_reduction_ladder_t0022.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

At the 4 nS sweet spot the preferred-direction peak firing is 15 Hz, an order of magnitude
below Schachter2010's 40-80 Hz baseline. The same low rate was observed in t0030 at 12 nS
GABA, so this is a pre-existing t0022 drive issue (likely the AMPA-only schedule lacking NMDA
or compensatory excitation), not a GABA ladder artefact. A task should add NMDA back into the
t0022 E-I schedule (or increase AMPA gain) and verify peak firing reaches 40+ Hz without
re-pinning DSI. Until this is fixed, any cross-testbed peak-rate comparison is invalid.

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
<summary>📚 <strong>Disambiguate the silently-overloaded HHst mechanism name across
the two libraries via SUFFIX rename</strong> (S-0070-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0070-05` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0070_writeup_two_model_beds`](../../../overview/tasks/task_pages/t0070_writeup_two_model_beds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

The t0070 research_code.md and writeup both flag a cross-library namespace collision: both
`tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/HHst.mod`
(Linaro-Storace-Giugliano stochastic) and
`tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/HHst_noiseless.mod`
(deterministic) declare `SUFFIX HHst`. Any code that says `seg.HHst.gnabar` references
different mechanisms depending on which `nrnivmodl` directory was loaded last, with no
warning. The kinetics happen to be identical so the bug is currently latent, but mid-flight
library swaps in cross-bed runners (S-0070-02) will silently change noise behaviour. Rename
Bed B's SUFFIX (e.g., to `HHst_det`) via corrections on the t0024 library, recompile, update
`build_cell.py` and downstream protocol code, and add a verificator scanning
`tasks/*/assets/library/*/sources/*.mod` for duplicate SUFFIX. Recommended task types:
write-library, infrastructure-setup, correction.

</details>

<details>
<summary>🧪 <strong>Disjoint parameter-basin enumeration of high-MI cells to quantify
Achard 2006 degeneracy on the t0123 substrate</strong> (S-0125-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0125-07` |
| **Kind** | experiment |
| **Date added** | 2026-05-25 |
| **Source task** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |
| **Source paper** | [`10.1371_journal.pcbi.0020094`](../../../tasks/t0125_t0123_cluster_factor_mi_atp/assets/paper/10.1371_journal.pcbi.0020094/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0125's electrophys silhouette = 0.083 (low) paired with chi-square p = 1e-236 (highly
significant) is the signature of Achard 2006's 'loosely connected hyperplane' geometry. t0125
confirmed the qualitative pattern (5 of 68 parameters with |Cliff's delta| > 0.6 for MI
groups, ~7%) but did NOT count DISJOINT parameter basins producing mi_count_bits > 1.0.
Action: on the spiking-cohort parquet, restrict to cells with MI > 1.0 (n ~ 600-800), apply
single-linkage hierarchical clustering in the standardised 54-d electrophys subspace tuned to
3-10 connected components, report per-component median pairwise distance, per-parameter range,
and cross-component nearest-neighbour distance. Replicate in morphology and full-68-d. Tests
Marder 2006 'many models, one behaviour' on t0123; motivates per-basin re-seeded NSGA-II.
CPU-only. Recommended task types: data-analysis, answer-question.

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
<summary>📊 <strong>Document silence-guard convention drift (t0115 total<10 vs t0122
pd_spikes<3) and recompute t0115 rate under t0122 guard</strong>
(S-0122-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-07` |
| **Kind** | evaluation |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0122 tightened the silence guard from t0115's 'total_mean_spikes < 10' to 'pd_spikes_sum < 3'
to handle the cytoplasm-minimisation tiny-cell regime. This makes the t0122 0.17% vs t0121
2.58% LEGIT comparison a lower bound on the substrate-tightness delta because of convention
drift; the true delta could differ depending on how many t0121 cells the tighter guard would
have excluded. Action: (1) document each task's silence-guard convention in the t0102-t0122
lineage with file:line refs; (2) re-score t0115 seed-9354's all_evaluations.json.gz under
t0122's guard, recompute the LEGIT acceptance rate, and report the delta vs t0115's original
1.19%; (3) decide and document the canonical project-default guard going forward. Pure
post-hoc analysis on existing assets, no new NSGA-II run. Recommended task types:
data-analysis, answer-question.

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
<summary>🔧 <strong>Examine NEURON memory accumulation; recommend per-N-gen worker
pool restart</strong> (S-0104-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0104-06` |
| **Kind** | technique |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Per-generation wall-clock doubled over both t0104 seeds (~15 min/gen at gen 1 to ~120 min/gen
at gen 11-12) despite worker-restart-between-generations being active in the inherited
nsga2_driver.py. The extra leak surface is likely inside per-cell evaluation: HOC namespace
allocations, NEURON mechanism state in non-RAM-tracked C memory, or matplotlib-figure handle
leaks in the morphology generator's chart-writing branch. Action: instrument
psutil.Process().memory_info().rss before and after each cell evaluation across one full
generation; identify which call-site grows. Then add a full
multiprocessing.Pool.terminate()/recreate() every N generations (N = 3 baseline) in
nsga2_driver.py. Predict: per-gen wall-clock holds within 2x of gen 1 instead of 8x by gen 11.
Recommended task types: write-library, experiment-run. Cost: ~$1 (instrumentation runs
locally; one verification run on Vast.ai).

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
<summary>🧪 <strong>Factor-axis trace gallery: sample cells along t0117 F1/F3/F5
loading axes and re-simulate the 3-mode trio</strong> (S-0118-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0118-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0118 establishes a clean re-simulation pipeline (3-mode trio, g_E / g_I / V_m, PD+ND, 1400
ms). t0117's salient factors are F1 (joint DSI-PD, 12.6% var), F3 (pure-ephys PD), F5
(depolarisation-block axis hypothesised in t0118 analysis). Link from factor space to
biophysics is currently inferential. Concrete action: project all 4431 t0117 cells onto F1,
F3, F5 individually; bin cells into 7 quantiles along each factor score, sample 3 cells per
bin (21 cells x 3 factors = 63 cells), re-simulate the t0118 protocol. For each factor produce
a 7-row x 3-column grid showing how g_E/g_I/V_m signatures change along the factor axis.
Decision: monotonic variation = biophysically meaningful factor; unrelated = statistical
artefact. Distinct from S-0117-06 (interprets F1 loadings statically). Recommended task types:
experiment-run, data-analysis. Cost: <$0.30.

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
<summary>🧪 <strong>Factorial morphology sweep (branch orders, segment length,
segment diameter) at fixed synapse count</strong> (S-0002-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_ENEURO.0261-21.2021`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_ENEURO.0261-21.2021/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

ElQuessny2021 concludes that global DSGC morphology has only a minor effect on the synaptic
E/I distribution, but the survey finds no paper that runs a clean factorial sweep over the
three local-electrotonic knobs separately. With synaptic count fixed at the PolegPolsky
177+177 baseline and dendrites set to active (Schachter2010 densities), vary (number of branch
orders, mean segment length, mean segment diameter) on an orthogonal grid, record DSI and HWHM
per point, and test whether segment diameter has the largest effect (as cable theory
predicts). This directly answers RQ2 and provides the morphology-sensitivity map the project
currently lacks. Recommended task types: experiment-run.

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
<summary>🔧 <strong>Fix pymoo NSGA-II dill checkpoint failure to enable
resume-from-checkpoint across the lineage</strong> (S-0123-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0123-05` |
| **Kind** | technique |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Every generation of t0123 emitted a 'dill checkpoint failed' warning from the pymoo NSGA-II
driver's pool-pickling path. JSON cell_trace + all_evaluations are still written each gen so
no data is lost, but resume-from-checkpoint is non-functional: a Vast.ai preemption at gen 47
cannot be resumed. Affects every NSGA-II task in the t0102-t0123 lineage. Action: (1)
reproduce locally on a 1-gen pop=8 mini-run; (2) identify the un-picklable object (likely a
NEURON HOC handle in the ProcessPoolExecutor worker or a closure in _evaluate); (3) implement
either (a) a custom Algorithm.serialize that strips un-picklable fields before dill, or (b) a
JSON-based checkpoint storing population genotypes + per-cell eval cache that rehydrates a
fresh Algorithm on resume; (4) add a resume_from_checkpoint integration test. Infrastructure
task touching arf/scripts plus the shared NSGA-II driver. Recommended task types:
infrastructure-setup, write-library.

</details>

<details>
<summary>🧪 <strong>Frontier-cell analysis: characterise cells the strict t0116
filter excluded but which carry the joint factor</strong> (S-0117-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0117-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0117 admits 4431 cells; t0116 admits 869. The 3562 excluded cells split into 'frontier' (just
below one threshold: DSI in (0.5, 0.7] OR PD in (5, 10]) and 'bulk' (deep-below). The frontier
cells are most informative for why the joint factor only appears when they are admitted.
Steps: (1) extract frontier cells from pooled_all_cells.parquet, (2) project them onto t0117
F1 scores, (3) compare F1-score distributions of frontier vs bulk vs t0116-included via KS +
means, (4) refit varimax FA on frontier-only cells (n approx 1500-2000) and check whether F1
reappears alone. Decision: if frontier-only FA also yields joint F1 with r_DSI/r_PD > 0.3, the
joint factor lives in the frontier band; if not, the joint factor requires the full mixed
pool. Recommended task types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

<details>
<summary>📊 <strong>g_I/g_E balance classifier: can a single E-I ratio scalar predict
t0117 cluster identity?</strong> (S-0118-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0118-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0118 identifies g_I / g_E ratio at peak g_E as the dominant cross-cell axis (6 orders of
magnitude, 0.03 to 440). The cluster-by-cluster interpretation proposes a categorical mapping:
cluster 1 < 0.5 (excitation-dominated), 0/2 in 0.5-5 (balanced), 3 > 10
(inhibition-dominated). Currently qualitative. Build a quantitative classifier: fit a
single-feature logistic regression and KNN predicting cluster_id from g_I/g_E ratio
(per_cell_metrics.csv); report accuracy + per-cluster precision/recall. Stretch: train a
linear regressor from t0118's 40-cell 68-d -> g_I/g_E pairs, predict ratio for the full t0117
4431-cell pool, map back to cluster IDs, report agreement vs t0117's KMeans labels. Decision:
if a single g_I/g_E feature explains > 70% of cluster identity, the t0117 cluster structure
reduces to one biophysical scalar. Recommended task types: data-analysis. Cost: <$0.10.

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
<summary>🧪 <strong>Ih (HCN) conductance ablation sweep on t0024 distal dendrites to
test h-current role in distal cable behaviour</strong> (S-0035-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0035-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-23 |
| **Source task** | [`t0035_distal_dendrite_diameter_sweep_t0024`](../../../overview/tasks/task_pages/t0035_distal_dendrite_diameter_sweep_t0024.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Sweep distal Ih (HCN) gbar from 0 to 2x baseline (five points) on the t0024 DSGC while holding
all other parameters fixed, and measure primary DSI, HWHM, and distal-compartment voltage. Ih
is a known resonance and input-impedance shaper that could partly explain why distal diameter
reads flat on both t0022 and t0024 (t0030 and t0035 both null). If ablation of Ih causes the
diameter sweep to become non-flat, h-current is masking the mechanism. Distinct from S-0009-03
which targeted Ih calibration, not ablation. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Impedance-loading-corrected electrotonic-length collapse
re-test</strong> (S-0041-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0041-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0041 falsified the simple lambda = sqrt(d * Rm / (4 * Ra)) collapse prediction for t0024
distal morphology (primary r=0.42, vector-sum r=-0.68). Re-run the collapse test with an
impedance-loading-corrected electrotonic length that accounts for sealed-end vs open-end
boundary conditions and tapered branching. If the corrected formula recovers r > 0.9, the 1-D
parameterisation could still be feasible with a slightly more sophisticated single scalar.

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
<summary>🔧 <strong>Interpolate soma pt3dadd diameters along the principal axis to
replace the uniform 4.118 um soma radius</strong> (S-0009-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-02` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

All 19 CNG soma rows currently receive the same averaged 4.118 um radius, flattening the
bell-shaped taper (~3.07 um to 5.31 um) visible in the five central Poleg-Polsky pt3dadd soma
contour points. Run PCA on the 19 soma xyz coordinates, project each row onto the first
principal component, and assign a radius by linear interpolation over the 7 Poleg-Polsky
pt3dadd values mapped onto the same axis. Emit a corrections file that overrides the 19
soma-row radii in dsgc-baseline-morphology-calibrated. Fixes the on-soma current-density
distribution for downstream spike-initiation simulations without changing the mean soma radius
or any dendritic row. Creative_thinking.md section F4. Recommended task types:
feature-engineering, correction.

</details>

<details>
<summary>📊 <strong>Interpret F1's biological meaning: top-loading features of the
joint DSI-PD factor in the unfiltered pool</strong> (S-0117-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0117-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0117_pooled_pca_cluster_factor_all_cells_4_seeds`](../../../overview/tasks/task_pages/t0117_pooled_pca_cluster_factor_all_cells_4_seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0117 confirms F1 is a joint DSI-PD axis but stops short of biological interpretation - it
reports F1's r_DSI/r_PD but not its top loadings on the 68-d feature vector (54-d electrophys
+ 14-d morphology). The latent-drivers question is only partially answered. Read
results/data/factor_loadings.csv, rank F1's loadings by absolute value, and identify the top-7
ephys parameters and top-3 morphology parameters loading on F1. Cross-reference t0116's pooled
F1 top loadings (SK_AIS + primary_branch_pd_concentration) and to t0108/t0110 strict/relaxed
comparison. Write a focused answer asset 'pooled-all-cells-f1-biological-interpretation' with
the loading table plus a 4-sentence biological interpretation: which channels and morphology
parameters jointly drive both DSI and PD when the full quality range is admitted? Recommended
task types: data-analysis, answer-question. Cost: <$0.10.

</details>

<details>
<summary>🔧 <strong>Inverse-fit three-bin dendritic radii against the Schachter 2010
proximal/distal input-resistance gradient</strong> (S-0009-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-01` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000899`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1371_journal.pcbi.1000899/) |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The calibrated proximal Rin (0.52 MOhm) and distal Rin (54 MOhm) are far below Schachter
2010's 150-200 MOhm proximal and >1 GOhm distal targets because the pure-literature
Poleg-Polsky three-bin radii are not tuned to our cell. Keep the three-bin (primary / mid /
terminal) structure but treat the three radii as free parameters; fit them in a NEURON
passive-properties simulation (Ra=100 Ohm-cm, Rm fit jointly) so that soma Rin lands in
150-200 MOhm and distal-tip Rin >= 1 GOhm. Seed the optimiser with the Poleg-Polsky means
(3.694/1.653/0.439 um) and emit a corrections file that overrides
dsgc-baseline-morphology-calibrated with the fitted radii. Blocks downstream DSI reproductions
against Schachter's tree. Recommended task types: feature-engineering, experiment-run.

</details>

<details>
<summary>📊 <strong>Investigate AIS-disabled-corner exploitation as a general
MOBO-on-biophysics failure mode</strong> (S-0078-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0078-08` |
| **Kind** | evaluation |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) |
| **Source paper** | [`10.1523_JNEUROSCI.1592-24.2024`](../../../tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/assets/paper/10.1523_JNEUROSCI.1592-24.2024/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0078 compare_literature step found iter 81's nav16_ais collapsed to the search floor
(1e-5 S/cm^2), four orders below Kole 2008's [0.25, 0.5] S/cm^2 prior and five orders below
Werginz 2024's mouse alpha-RGC value of 1.3 S/cm^2. AIS-to-soma Nav ratio at iter 81 was
5.5e-5 vs Werginz 2024's measured 17.3. The optimiser found a configuration where the AIS
contributes nothing to spike initiation, contradicting REQ-2 / REQ-3 / REQ-4's biological
intent. This may be a generalisable MOBO-on-biophysics failure mode. Document: (a) audit t0076
+ t0078 Pareto fronts for similar collapse-to-floor patterns on biologically-priored
parameters; (b) propose log-uniform priors with hard biological lower bounds as default for
future MOBO tasks; (c) write up as an answer asset. Pass: produce an answer asset with a
checklist of biological priors to enforce as hard constraints in future MOBO tasks.
Recommended task types: answer-question, comparative-analysis.

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
<summary>🧪 <strong>Investigate the seed-44 / seed-7755 / seed-9354 'rich-yield'
parameter signature</strong> (S-0115-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-07` |
| **Kind** | experiment |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

Three of the five S-0112-01 batch seeds (44, 7755, 9354) all exceeded the Hay 2011 0.40%
acceptance envelope, while seeds 77 and 2247 sat at or below it. The 484 vs 7 vs 63 LEGIT
joint-pass cell count spread is much larger than the t0106/t0112/t0113 protocol diff implies,
suggesting seed-specific search-basin attractors. Concrete action: compute the pairwise
normalised L2 distance between every t0106 / t0114 / t0115 strict Pareto cell in 68-d
parameter space; identify any cluster signatures that distinguish 'rich-yield' from
'sparse-yield' seeds; report whether the rich-yield Pareto fronts share a common parameter
sub-volume vs each occupying a distinct sub-volume. Recommended task types: data-analysis.
Cost: <$0.10.

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
<summary>🧪 <strong>Investigate why seed 9354 took 25 gens to find the joint-pass
corner (vs t0114's 8 gens)</strong> (S-0115-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0115's late corner-find (joint-pass cells emerging at gen 25) vs t0114's early corner-find
(gen 8) is the most striking seed-to-seed protocol difference at fixed substrate + algorithm.
The 17-gen lag corresponds to ~3 full pool-restart cycles, suggesting the random-init basin or
LHS sampling distribution for seed 9354 was systematically further from the joint-pass region.
Concrete action: compare t0115's gen-1 LHS-init population against t0114's by computing (a)
nearest-distance from each init cell to the eventual joint-pass corner in normalised 68-d
parameter space, (b) the distribution of init-cell DSI and PD values, and (c) the genetic
operators' (SBX/PM) effective step size in the first 10 gens. Outcome: identify the
basin-attractor signature that distinguishes rich-yield seeds (44, 7755) from slow-yield seeds
(9354) and dead-end seeds (2247). Recommended task types: data-analysis. Cost: <$0.10.

</details>

<details>
<summary>📊 <strong>Investigate why t0086 / t0088 cluster 1 converges to extreme
AIS-to-soma Nav ratios (per-cell range 42.6-270.7)</strong> (S-0090-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-06` |
| **Kind** | evaluation |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0090 Phase G.1 audit ruled out floor-pinning and centroid-averaging artifacts: cluster-1
cells 1304 / 1504 / 1624 / 1634 individually have AIS-to-soma Nav ratios of 139.4 / 42.6 /
270.7 / 141.2 (all above 2.5x the Werginz 2024 mean of 17.3). Verdict: real_signal. Probe the
loss landscape around these 4 cells: in the t0083 archive's 54-d parameter space, restrict to
cluster-1 morph variants and visualise the DSI / PD-rate / robustness slice along (Nav_AIS,
Nav_soma) at fixed values of all other dimensions. Either the optimiser is rationally finding
an extreme-but-functional regime that should motivate revising the prior (a la S-0086-05's
RGC-specific-NaP-density argument), or the loss surface is multi-modal and a tightened upper
bound on Nav_AIS would still find joint-pass cells. Recommended task types: data-analysis.

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
<summary>🧪 <strong>Kv3 vs Kv1 AIS placement swap to test the Kole-Letzkus 2007
repolarisation prior</strong> (S-0022-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-06` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | [`10.1523_jneurosci.0130-07.2007`](../../../tasks/t0022_modify_dsgc_channel_testbed/assets/paper/10.1523_jneurosci.0130-07.2007/) |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`patch-clamp`](../../../meta/categories/patch-clamp/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Kole & Letzkus 2007 report that Kv1 in the proximal AIS sets spike threshold while Kv3 in the
distal AIS sets repolarisation speed and thus maximum sustained firing rate. Use the t0022
AIS_PROXIMAL and AIS_DISTAL forsec blocks to implement four conditions: (a) Kv1 proximal + Kv3
distal (canonical), (b) Kv1 distal + Kv3 proximal (swap), (c) Kv1 both (no Kv3), (d) Kv3 both
(no Kv1), each with Nav1.6 held at 8 S/cm^2 in the distal AIS. Rerun the 12-angle x 10-trial
sweep for each condition. Expected outcome: condition (a) peaks near 30-40 Hz; condition (b)
drops peak because distal Kv1 fails to fast-repolarise; conditions (c) and (d) test whether
either K-channel alone suffices. Dependencies: t0022 library asset. Effort ~16 hours.
Recommended task type: experiment-run, comparative-analysis.

</details>

<details>
<summary>🧪 <strong>Kv4 retest with hyperpolarising prepulse to remove
inactivation</strong> (S-0074-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Kv4 / IA was inert at all 3 densities. Compare-literature: Kv4's V_half_h is -50 mV; the
DSGC's resting potential is -60 mV, which is below V_half_h, so Kv4 sits inactivated at rest.
To engage Kv4, a brief hyperpolarising prepulse (~50 ms at -80 mV) before the bar-rotation
stimulus would remove inactivation. Modify the run_sweep.py protocol to include a 50 ms
pre-pulse window; re-run the 3-density Kv4 sweep (3 conditions × 12 angles × 5 seeds = 180
trials, ~6 min compute). Hypothesis: with the prepulse, Kv4 produces measurable HWHM narrowing
and peak-rate suppression at high density. If confirmed, Kv4 is biologically active in DSGCs
but only after recent hyperpolarisation — relevant for understanding ON-OFF DSGCs that
experience hyperpolarising rebounds between stimulus presentations.

</details>

<details>
<summary>📚 <strong>Lock N_SEEDS=4 as project-wide default if t0102 reproduces t0099
DSI/PD scatter</strong> (S-0101-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0101-02` |
| **Kind** | library |
| **Date added** | 2026-05-11 |
| **Source task** | [`t0101_brainstorm_results_21`](../../../overview/tasks/task_pages/t0101_brainstorm_results_21.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

N_SEEDS=20 in tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py:43 is
propagated as the noise-replicate count into every downstream NSGA-II task (t0081, t0083,
t0091, t0099). If t0102's DSI/PD per-cell estimates at N_SEEDS=4 fall within +/- 1 std of
t0099's matched cells at N_SEEDS=20, lower the project-wide default to 4 (5x cheaper per
evaluation). Implementation: corrections/library_modeldb_189347_dsgc_dendritic.json or a small
library-update task; document the empirical comparison in a results table. Cost $0 if the
comparison data is already in t0102.

</details>

<details>
<summary>📂 <strong>Manually fetch and attach the Poleg-Polsky 2016 supplementary
PDF (NIHMS766337, PMC4795984)</strong> (S-0046-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-05` |
| **Kind** | dataset |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The supplementary PDF
(`https://pmc.ncbi.nlm.nih.gov/articles/instance/4795984/bin/NIHMS766337-supplement.pdf`) was
blocked by PMC's JS-only interstitial during t0046 implementation; a metadata-only correction
overlay records the citation but the binary file is not attached. Manually download the PDF
via a browser session and attach it to the existing `10.1016_j.neuron.2016.02.013` paper
asset, then update the corrections overlay to a full-binary-attached state. The supplementary
text is the only authoritative source for any Methods parameters not stated in the published
main text and is needed to fully audit the synapse-count discrepancy (S-0046-02). Recommended
task types: download-paper, correction.

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
<summary>🧪 <strong>Matched-evaluation-budget substrate-rate comparison against Hay
2011 and Druckmann 2007 (extrapolation experiment)</strong> (S-0121-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0121-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0121_5seed_substrate_rate_canonical_report`](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md) |
| **Source paper** | [`10.1371_journal.pcbi.1002107`](../../../tasks/t0121_5seed_substrate_rate_canonical_report/assets/paper/10.1371_journal.pcbi.1002107/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0121's per-seed budget spans 1344-5952 evaluations vs Hay 2011's 500,000 and Druckmann 2007's
300,000 - this work runs 50x-372x fewer evals per seed than published references. The
point-estimate comparison (6.45x above Hay envelope, 25.8x above Druckmann) is therefore made
at very different sample sizes; whether the per-seed rate converges, decays, or oscillates at
matched spend is open. Concrete action: take the highest-yield seed (7755), re-run NSGA-II to
a 50,000-evaluation budget (~10x current spend, ~$15-25), record the per-1000-eval running
rate trajectory, and test whether the asymptote stays above or drops below Hay's 0.40% as
budget grows. Decision: if the running rate stays > 1% at 50K evals, the substrate-density
claim is budget-robust. If it decays below 0.40%, t0121's headline is an early-NSGA-II
transient. Recommended task types: experiment-run.

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
<summary>🧪 <strong>Move Nav1.6 + Kv3 to a virtual AIS instead of soma</strong>
(S-0068-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0068-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

Real RGCs concentrate Nav1.6 and Kv3 at the AIS at ~50x somatic densities. The Nav1.6 + Kv3
co-localisation we modelled here is somatic, which the t0067 / t0068 limitations document as
understating the joint effect. Add a 30-um AIS section to the deposited cell, place Nav1.6 +
Kv3 there at 30 / 90 mS/cm^2 (and a wider Kv3 density grid up to ~200 mS/cm^2), re-run the
rescue sweep. Expected: AIS-localised Kv3 at very high density may finally show DSI rescue
because the AIS's smaller diameter makes per-segment conductance changes leverage the AP shape
more strongly. If still no rescue, the channel-pharmacology approach to DSI rescue is null
across substrates.

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
<summary>🧪 <strong>Multi-channel-set diversity re-test of t0090 morphologies to
disentangle morphology vs channel-set sensitivity</strong> (S-0090-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

The t0090 finding that 51/60 morphologies fail NAN_VOLTAGE rests on a single channel set
(t0083 best-cell). To confirm Mainen 1996 morphology-determines-firing-pattern as the cause
(rather than the t0083 channel set being uniquely fragile), re-run the 60-morphology
verification on 3 different t0083 Pareto cells' channel sets (e.g. cells 1559, 1639, 767
spanning the t0086 cluster representatives). If the STABLE / NAN_VOLTAGE flag is consistent
across channel sets per morphology, the failure is morphology-specific and S-0090-04's
tightened LHS bounds are the right fix; if STABLE-or-not depends on channel set, the joint
68-d NSGA-II must accept that warm-start anchors are channel-set-conditional. Pure simulation;
no remote machine; ~30 min on local 64-core. Recommended task types: experiment-run,
data-analysis.

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
<summary>🧪 <strong>Multi-section NaP/Nav1.6 decomposition across all 177 terminal
dendrites of cell 767</strong> (S-0084-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0084-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0084's attribution metric records Nav1.6 and NaP currents only at `cell.terminal_dends[0]`
(representative section). Test whether this is representative by extending recording to all
177 terminal dendrite sections of cell 767 and recomputing per-section fractional
contribution. If per-section spread is small (all > 80% NaP-dominant), single-section
attribution is robust; if some sections show NMDA-dominant or Nav1.6-dominant local
contributions, there is dendrite-tree spatial heterogeneity that the single-section metric
obscures, reframing t0084 from 'NaP-dominant cell-wide' to 'NaP-dominant on average with
possible NMDA hotspots'. Local CPU; runtime increase ~10 minutes. Cost ~$0. Recommended task
types: experiment-run, data-analysis.

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
<summary>📚 <strong>NEURON worker process restart between gens to test if memory
accumulation explains per-gen wall-clock doubling</strong> (S-0099-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0099-04` |
| **Kind** | library |
| **Date added** | 2026-05-10 |
| **Source task** | [`t0099_random_init_pareto_robustness`](../../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0099 observed gen 1 = 38-52 min, gen 8 = 167+ min for the same workload. Hypothesis: NEURON
state accumulation across pop=96 cell builds per gen. Test: modify nsga2_driver to spawn fresh
worker pool every 2 gens. If late-gen wall-clock improves by >20%, the memory-accumulation
hypothesis is confirmed. Cost $1-2 single seed.

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
<summary>🧪 <strong>Off-diagonal-corner-constrained NSGA-II to sample the
undersampled high-MI/high-ATP and low-MI/low-ATP corners</strong>
(S-0125-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0125-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-25 |
| **Source task** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0125 finds a 3.6x diagonal-vs-off-diagonal corner imbalance: 1221 high_MI/low_ATP + 1220
low_MI/high_ATP vs only 343 high_MI/high_ATP + 341 low_MI/low_ATP cells. Off-diagonal corners
are real -- cell (19, 1816) hits MI=1.459 at ATP=4.97e7 (8.7x more expensive than equivalent
(30, 2828)) -- but undersampled because NSGA-II exploited the cheap-and-informative half.
Action: rerun the t0123 NSGA-II twice with constrained objectives (a) maximise BOTH MI and ATP
(forces high_MI/high_ATP corner); (b) minimise BOTH (forces low_MI/low_ATP corner). Sample 96
cells per corner; rerun the t0125 cluster + factor pipeline on the union plus the original
t0123 pool. Tests whether off-diagonal corners share or have private latent drivers. Budget
~$8-12 Vast.ai EPYC. Recommended task types: experiment-run, data-analysis.

</details>

<details>
<summary>🧪 <strong>Online validation of (W=3, T=0.015): re-run t0106 / t0113 / t0114
seeds with new detector live</strong> (S-0114-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-08` |
| **Kind** | experiment |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0114_seed7755_no_autostop/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

The S-0114-01 (W*, T*) = (3, 0.015) recommendation is computed offline from 4 HV trajectories.
It has NOT been validated by running NSGA-II online with the new constants. Concrete action:
re-run two seeds end-to-end with the new detector active: (a) seed 44 (t0106) — should fire at
gen 39 and stop, matching offline prediction; (b) seed 2247 (t0113) — should NOT fire within
gen 14 (eliminating premature stop) and run to a longer plateau. Optional third: seed 7755
(t0114) — should fire at gen 26 instead of operator-stop at gen 62. Decision: if all match
offline replay, formally close S-0114-01 and declare (W=3, T=0.015) the default. If any
diverge, treat replay as biased and reopen (W*, T*) search with new live HV traces. Bonus: the
live runs contribute additional seeds to the substrate-rate sample. Recommended task types:
experiment-run, comparative-analysis. Cost: ~$3-6.

</details>

<details>
<summary>🧪 <strong>Overlay a Van Wart + Werginz AIS on the deRosenroll morphology
to test peak-rate recovery</strong> (S-0024-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-03` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Research-internet gap 2 showed that the upstream repository has no explicit AIS section, but
research-papers (Werginz 2020, Van Wart 2007) pins the AIS-to-soma Na ratio at ~7x and names
AIS length as the dominant predictor of maximum sustained firing rate. Fork t0024 into a new
library asset, add a two-subsegment AIS (proximal Nav1.2/Nav1.1, distal Nav1.6 + Kv1.2) with
Na ratio 7x and AIS length 25-50 um, rerun the 8-direction correlated/uncorrelated protocol,
and compare peak firing rate and HWHM to the t0024 baseline. Does not require rebuilding the
SAC network.

</details>

<details>
<summary>📚 <strong>Parallelise the t0024 sweep across CPU cores to cut wall time
from 3.21 h to under 1 h</strong> (S-0026-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0024 sweep took 11,562 s (3.21 h) because NEURON ran single-threaded on one CPU. Each
(V_rest, direction, trial) combination is embarrassingly parallel. Build a ProcessPoolExecutor
wrapper that farms out trials across cores; with 8 workers we expect wall time to drop below 1
h. This will make V_rest x rho and V_rest x velocity sweeps practical.

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
<summary>📚 <strong>Parameterise the in-loop budget watchdog hourly rate so cost
tracking matches the actual Vast.ai offer rate</strong> (S-0083-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0083-04` |
| **Kind** | library |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The watchdog used by t0080 / t0081 / t0083 reads `_HOURLY_RATE_USD = 0.2382` from
`arf.libraries.t0080_loop`, hard-coded to t0080's Norway EPYC 7B13 rate. t0083 ran on a
$0.3209/hr Texas offer; the watchdog tracked $4.115 at gen-17 termination while the true
charge was ~$5.55, climbing to $5.828 at instance destruction -- a $0.83 ex-post breach of the
$5.00 cap. Fix: add `--hourly-rate-usd` to `run_loop.py` overriding `_HOURLY_RATE_USD` at
startup; or auto-read from `logs/steps/*setup-machines*/machine_log.json`
`selected_offer.price_per_hour`. Verify with a 1-gen smoke test on a non-default-rate offer
matching post-run charges within 5 percent. Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Parameterize t0011/t0012 tuning-curve plotter and scorer to
support N_ANGLES != 12</strong> (S-0024-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-04` |
| **Kind** | library |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0011 tuning_curve_viz library and the t0012 tuning_curve_loss scorer both hardcode
N_ANGLES=12, which blocks native 8-direction visualisation and scoring for the deRosenroll
port (and any future paper that uses 4/6/8/16/24 directions). Refactor both libraries to
accept an N_ANGLES argument (default 12 for backward compatibility) and rerun the t0024
8-direction conditions through the plotter to produce polar/Cartesian PNGs for
results_detailed.md. Small infrastructure change with broad reuse benefit across the DSGC
lineage.

</details>

<details>
<summary>🔧 <strong>Parametric-bootstrap factor analysis at N>=300 synthetic cells
to test if F3-F10 stabilise</strong> (S-0105-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-06` |
| **Kind** | technique |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0105_cluster_factor_analysis_dsi_pd`](../../../overview/tasks/task_pages/t0105_cluster_factor_analysis_dsi_pd.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Only F1 and F2 pass the t0105 bootstrap stability test (>= 90 % sign consistency in top-5
loadings, median |loading| >= 0.4) at N=85. The 5xp = 340 conventional floor for factor
analysis on 68 dimensions would need N >= 340 cells. Generate a parametric bootstrap from the
t0105 cohort (fit a multivariate Gaussian or copula on the 68-d data, sample N=400 synthetic
cells, refit varimax FA) and check whether F3-F10 stabilise at the inflated N. If they do, the
under-power is the limiter; if they do not, the factors are genuinely unstable in the
substrate. Recommended task type: data-analysis. Cost: $0 (pure local synthesis +
re-analysis).

</details>

<details>
<summary>📊 <strong>Pareto-cell PCA + feature-importance analysis on the 14-d morph
vectors to rank Pareto-inclusion drivers</strong> (S-0091-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0091-07` |
| **Kind** | evaluation |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0091_morphology_extended_nsga2_v1`](../../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0091 reports anchor-level Pareto counts (bedb_like 20, symmetric 0, pd_asymmetric 12,
nd_asymmetric 9, alt_topology 16) but does not report which of the 14 morphology knobs
individually drive Pareto inclusion. Pure data-analysis on results/data/pareto_front.json +
all_evaluations.json: train a logistic regression / random forest classifier with the 14-d
morph vector as input and is_in_pareto as binary label, using the 187 evaluations as the
training set; report per-feature coefficients / SHAP values; cross-validate via
leave-one-anchor-out splits; visualise via per-feature partial dependence plots. Goal: rank
the 14 knobs by their causal importance for joint Pareto inclusion, beyond the anchor-level
aggregation. This complements S-0091-01 (which is single-feature Spearman) and S-0091-04
(which is alt-topology vs bedb-like comparison) with an exhaustive feature-importance audit.
Cost: $0 (local CPU). Recommended task types: data-analysis.

</details>

<details>
<summary>🧪 <strong>Partial-correlation analysis of MI vs electrophys (control
morphology) and ATP vs morphology (control electrophys)</strong>
(S-0125-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0125-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-25 |
| **Source task** | [`t0125_t0123_cluster_factor_mi_atp`](../../../overview/tasks/task_pages/t0125_t0123_cluster_factor_mi_atp.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0125's PCA colourings make the separation visible: high-MI cells cluster in the electrophys
PCA but are absent from the morphology PCA; log10(ATP) shows a gradient in the morphology PCA,
flatter in electrophys. NMI table corroborates (electrophys-vs-MI 0.178, electrophys-vs-ATP
0.186, morphology-vs-MI 0.121, morphology-vs-ATP 0.176). These are pairwise correlations and
could share a common cause. Action: on the existing spiking-cohort parquet, compute Spearman
partial r for (a) MI vs each of 54 electrophys params partialling out 14 morphology params;
(b) ATP vs each of 14 morphology params partialling out 54 electrophys params; (c) MI vs ATP
partialling out morphology; (d) MI vs ATP partialling out electrophys. Report top-10 with
bootstrap CI; compare to t0125 group_comparison.csv. Single CPU-only follow-up. Recommended
task types: data-analysis, answer-question.

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
<summary>📚 <strong>Per-cell HV-contribution analysis to identify silence-guard cells
inflating HV beyond their biological value</strong> (S-0113-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-05` |
| **Kind** | library |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0113's gen 13->14 HV jump of +26% (35.98 -> 45.62) was driven by a single silence-guard
DSI=1.0 cell joining the archive. The HV-plateau detector tolerated this jump as saturation
onset, but the cell contributes ~zero biological selectivity (8-direction DSI ~0). Build an
analysis script that, per generation across t0106/t0112/t0113, decomposes the HV increment
into per-archive-member contributions and flags silence-guard cells (DSI=1.0 OR <=1 PD spike)
separately. Output: per-task `hv_contribution_by_cell.csv` and cross-task
`silence_guard_hv_share.png`. Decision: if silence-guard cells contribute >=20% of final HV in
any seed, replace 2-D HV with a 'legit-only HV' that excludes silence-guard saturations for
the substrate-rate paper. Reusable across S-0112-01 / S-0113-01 multi-seed batch. Recommended
task types: data-analysis, write-library. Cost: <$0.20.

</details>

<details>
<summary>🧪 <strong>Per-cluster ND-leading g_I latency analysis: is the SAC-like
inhibitory-veto signature present across clusters?</strong> (S-0118-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0118-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-22 |
| **Source task** | [`t0118_resimulate_t0117_cluster_samples_ge_gi_vm`](../../../overview/tasks/task_pages/t0118_resimulate_t0117_cluster_samples_ge_gi_vm.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0118's per-cluster panels show ND g_I peaks earlier than PD g_I in cluster 1 (all-s44, DSI ~
0) traces - the classic Vaney/Taylor inhibitory-veto signature - even though firing asymmetry
is absent. This suggests the inhibitory-timing mechanism is partially present in cells the
NSGA-II selected as low-DSI. Action: extract per-cell PD and ND g_I onset latency from t0118's
per_cell_metrics.csv, plot (latency_ND - latency_PD) per cluster, test (a) is the ND-leads-PD
pattern significant per cluster, (b) does the magnitude correlate with DSI within cluster, (c)
is there a critical latency threshold above which firing asymmetry emerges? Re-simulate top-5
latency-difference cells per cluster at RECORD_DT = 0.1 ms to confirm timing isn't aliased.
Distinct from S-0118-02 (sweeps inhibition strength, not timing). Recommended task types:
data-analysis, experiment-run. Cost: <$0.10.

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
<summary>🧪 <strong>Per-seed factor analysis on each sub-basin: do basins share
latent drivers or have private ones?</strong> (S-0116-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0116-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0116_pooled_pca_cluster_factor_dsi07_pd10`](../../../overview/tasks/task_pages/t0116_pooled_pca_cluster_factor_dsi07_pd10.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0116's pooled FA (n=869) found F1 mixed DSI driver (SK_AIS + primary_branch_pd_concentration
co-vary) and F3 pure-electrophys PD driver. The basin-connectivity answer shows the pool
fragments by seed; F1's mixed loadings could reflect (a) a single mixed axis within every
basin or (b) two separate axes (one ephys, one morph) that co-vary because seed-of-origin
confounds them. The latent-drivers answer's Limitations section flags this as a candidate
correction task. Run independent varimax FAs on each per-seed slice with sufficient n: seed
7755 (n=675), seed 44 (n=121), seed 9354 (n=63); skip seed 77 (n=10). For each per-seed FA,
report top-1 DSI factor and top-1 PD factor. Decision: if all three rich seeds produce a mixed
ephys+morph DSI factor with the SK_AIS + morph co-loading, pooled F1 is intrinsic; if some
produce pure-ephys and others pure-morph, pooled F1 is a cross-basin confound. Distinct from
S-0113-08 and S-0114-05. Recommended task types: data-analysis. Cost: <$0.20.

</details>

<details>
<summary>📚 <strong>Per-trial ProcessPool parallelisation for the minimal-DSGC sweep
runner (t0052/t0053/t0054)</strong> (S-0054-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-06` |
| **Kind** | library |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0054's 1440-trial sweep took 4 h 19 min wall-clock on a single CPU thread (~10.8 s/trial),
3.5x over the 75-minute plan target. Adding Mg-block NMDA (S-0054-01), the joint conductance
sweep (S-0054-02), and the tau2 sweep (S-0054-05) will each be 5-15x larger and infeasible on
a single thread. Each (gNMDA, direction, trial, mode) combination is embarrassingly parallel
because NEURON state is rebuilt per trial. Build a ProcessPoolExecutor wrapper for the
minimal-DSGC sweep loop in t0054/code/run_tuning_curve.py (and equivalent t0052/t0053 paths)
that farms trials across N_workers = max(1, cpu_count - 2). Validate: gNMDA=0 regression gate
against t0052 still passes at 0e+00 Hz max diff. Distinct from t0045 (CoreNEURON-on-GPU for
t0022) and S-0026-04 (t0024-specific) because it targets the CPU runner shared by
t0052/t0053/t0054. Recommended task types: write-library, baseline-evaluation.

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
<summary>🧪 <strong>Pool-restart cadence sweep _POOL_RESTART_EVERY in {5, 15, 20} for
wall-clock vs exploration tradeoff</strong> (S-0114-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0114 confirmed _POOL_RESTART_EVERY=10 delivers stable wall-clock (198 s/gen on 128-thread
EPYC, 484 LEGIT joint-pass cells in 62 gens) on the 68-d substrate. Cadence-10 was inherited
from t0112 / t0113 without an isolated sensitivity study. Concrete action: replicate t0114's
exact protocol (seed 7755, auto-stop disabled, 60-gen ceiling) at _POOL_RESTART_EVERY in {5,
15, 20} — three runs at the same seed isolates the cadence effect. Report per-cadence: (a)
wall-clock per gen, (b) LEGIT joint-pass yield at gen 60, (c) HV trajectory shape, (d) total
spend. Hypothesis: cadence 5 increases worker-init overhead but may reduce silence-guard
accumulation; cadence 20 speeds wall-clock but risks worker-memory drift. Decision: adopt the
cadence that maximises (LEGIT cells per dollar). Recommended task types: experiment-run,
comparative-analysis. Cost: ~$3-5.

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
<summary>📚 <strong>Port the TREES-toolbox Rall 3/2 quaddiameter rule to a
pure-Python calibrator and compare against the Strahler bins</strong>
(S-0009-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-08` |
| **Kind** | library |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Rall's 3/2 power rule (r_parent^(3/2) = sum r_child^(3/2)) is the only biophysically
principled way to match impedance across a binary tree; our max-child Strahler bins have no
such guarantee. Implement TREES-toolbox's quaddiameter algorithm as ~80 lines of pure Python,
solve the system bottom-up from the 131 terminals with the Poleg-Polsky terminal mean fixed,
and produce a sibling asset dsgc-baseline-morphology-rall. Compare against the
Strahler-calibrated asset by per-branch axial resistance, total surface area, and
per-compartment radius deltas. Expected primary-radius shift ~15% (3.69 to ~3.1 um) at the
measured 2-way branching ratio. Creative_thinking.md section A2. Recommended task types:
write-library, comparative-analysis.

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
<summary>📚 <strong>Pre-register the 5-seed canonical substrate-rate numbers as a
project metric registered via meta/metrics/</strong> (S-0121-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0121-05` |
| **Kind** | library |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0121_5seed_substrate_rate_canonical_report`](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0121's headline numbers - 5-seed mean LEGIT acceptance 2.58%, normal-approx 95% CI (-0.35%,
+5.51%), bootstrap 95% CI (+0.38%, +5.53%), n_seeds_above_hay_envelope = 3 - currently live
only in this task's results files. Per ARF design they are not yet a registered project
metric, so no aggregator can track them or compare them against future runs. Concrete action:
register a new metric `legit_substrate_rate_pct` (unit: percent, scope: project-wide) in
`meta/metrics/`, with the per-seed convention (`n_legit_joint_pass_unique / n_total_evals *
100`) baked into the metric definition. Backfill metric_results from t0106 / t0112 / t0113 /
t0114 / t0115 / t0121 using the canonical convention so any future seed can be aggregated
against the baseline. Distinct from S-0121-03 (which is about CI methodology, not the headline
metric itself). Recommended task types: infrastructure-setup, data-analysis.

</details>

<details>
<summary>📚 <strong>Pre-warm NEURON DLL + parameter-vector apply in
ProcessPoolExecutor workers to halve sweep wall-clock</strong> (S-0093-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0093-03` |
| **Kind** | library |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0093 16-worker re-sweep took ~50 min vs the planned ~14 min on a 64-core EPYC -- a 3.5x
slowdown almost entirely attributable to per-worker NEURON DLL load + first-trial
parameter-vector apply (each worker pays the full warm-up cost on every sub-batch). Implement
a `worker_init` callable for ProcessPoolExecutor that (a) imports neuron + h.load_file once,
(b) compiles + loads the t0080 channel mechanism DLL, (c) runs one throwaway 50-ms stim trial
to warm up the channel-mechanism kernels and the SciPy/NumPy inits, then signals readiness.
Benchmark a 60-cell sweep with vs without warm-up; expected savings ~30 min on this scale.
Bake the helper into a small `arf/scripts/utils/neuron_pool.py` library so all future sweeps
(t0091's per-generation 96-cell evaluations, future Bed-A sweeps, the 4-channel-set sweep from
S-0090-05) inherit the speedup. Recommended task types: write-library, infrastructure-setup.

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
<summary>📚 <strong>Promote t0072's cross-bed per-synapse (g, v_local) recorder +
post-hoc current pipeline into a library</strong> (S-0072-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0072-04` |
| **Kind** | library |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0072_synaptic_traces_pd_nd`](../../../overview/tasks/task_pages/t0072_synaptic_traces_pd_nd.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/) |

t0072 produced a recording infrastructure that works across both Bed A (HOC-driven BIPsyn /
SACinhib / SACexc) and Bed B (Python-driven Exp2Syn ACh / GABA via NetStim+NetCon). Extends
t0048's BIPsyn-only attach_conductance_recorders (proposed as S-0047-04 for Bed A only) along
three new axes: (1) per-synapse local v via point_process.get_segment()._ref_v rather than
only g, (2) automatic uS->nS unit conversion when the mechanism uses uS (Bed B Exp2Syn
convention), (3) post-hoc per-synapse current I = g_nS * (v_local_mV - E_rev_mV) in pA with
E_rev sourced from MOD PARAMETERs. Package: (a) attach_g_v_recorders(cell, synapse_lists,
dt_record_ms, e_rev_per_kind_mV), (b) compute_currents_pA and aggregate_population helpers,
(c) uS->nS boundary helper, (d) smoke tests on both bed builder fixtures. Distinct from
S-0047-04 (Bed A only, no v_local, no uS->nS, no I) and S-0070-02 (bed-runner library covers
builders, not trace recording). Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Promote t0084 attribution-metric pipeline into a reusable
mechanism_attribution_v3 library asset</strong> (S-0084-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0084-06` |
| **Kind** | library |
| **Date added** | 2026-05-05 |
| **Source task** | [`t0084_t0081_cell_767_vm_trace_deepdive`](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

t0084 produced six well-tested code modules implementing a per-cell extended-recording
pipeline plus fractional-channel-contribution attribution metric. The pipeline is reusable for
any v3 substrate cell (and trivially extensible to v4 substrates) and should not have to be
rebuilt for each follow-up task. Promote it to a library asset under
`assets/library/mechanism_attribution_v3/` with public entry points:
`run_deepdive_for_cell(cell_id, parameter_vector, directions, seed)`,
`compute_fractional_attribution(traces_dir, cell_id, response_window_ms)`,
`plot_attribution_figures(cell_id)`. Pure refactor; no new compute. Cost ~$0. Will accelerate
follow-ups S-0084-01 / S-0084-02 / S-0084-03 / S-0084-05. Recommended task types:
write-library, data-analysis.

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
<summary>📚 <strong>Promote the t0098 morphology renderer (with t0100 vector_68d[54:]
slice fix) into a reusable library asset</strong> (S-0105-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0105-03` |
| **Kind** | library |
| **Date added** | 2026-05-13 |
| **Source task** | [`t0105_preliminary_figures_report`](../../../overview/tasks/task_pages/t0105_preliminary_figures_report.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Figure 7 in t0105 had to copy the morphology renderer code from
tasks/t0098_visualise_pareto_morphologies/code/build_charts.py into
tasks/t0105_preliminary_figures_report/code/render_pareto_top5.py with the vector_68d[54:]
morphology-slice fix from t0100 patched in manually. The t0104 follow-up panel (S-0105-01),
and any future optimisation-result report task, will need the same renderer. Package this
renderer as a top-level library asset (e.g., dsgc_morphology_renderer) under a host task --
expose a clean Python API (render_morphology(vector_68d, ax) plus a multi-cell grid helper),
include the t0100 slice fix as the default behaviour, register a details.json under
assets/library/, and document import path tasks.<host_task>.code.dsgc_morphology_renderer.
Downstream tasks then import instead of copying. Recommended task types: write-library.

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
<summary>🔧 <strong>Re-calibrate using a Poleg-Polsky xyz-registered 1:1 per-section
diameter lookup to drop Strahler binning entirely</strong> (S-0009-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-04` |
| **Kind** | technique |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0009_calibrate_dendritic_diameters/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Our three-bin heuristic collapses 170 Poleg-Polsky mid-role sections into one 1.653 um radius
(section F1 of creative_thinking.md). A lossless alternative is to Procrustes-align the CNG
xyz points with the Poleg-Polsky RGCmodel.hoc pt3dadd points, then for each CNG compartment
copy the diameter of the nearest registered source section. Preserves all 350 source diameters
and eliminates both the tie-break-induced primary bin boundary (section F3) and the
bin-collapse interior variability. Deliverable: a sibling dataset asset
dsgc-baseline-morphology-registered with a registration-quality report (residual xyz distance
per compartment). Emit corrections if registration succeeds with sub-micron residuals.
Recommended task types: feature-engineering, data-analysis.

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
<summary>🔧 <strong>Re-render t0112 / t0114 / t0115 top-50 morphology grids with
t0120's rendering conventions (correction)</strong> (S-0120-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0120-01` |
| **Kind** | technique |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0120 confirmed the soma-disconnect visual artefact in t0115's top50_morphologies_seed9354.png
(and the seed-44/77/7755 analogues from t0106/t0112/t0114) is rendering-only, driven by three
conventions in build_top50_morphologies.py: fixed Circle(radius=6.0) soma (too small vs
typical 100-150 um soma_offset_pd_um), LineCollection(linewidths=0.4) primary stems (visually
negligible), and auto-zoom that amplifies asymmetry. Concrete action: regenerate the four PNGs
using t0120's conventions (Circle(radius=soma_diameter_um/2), tab:red primary stems at
linewidth 2.0, optional debug line from origin_xy to each primary-stem tip), file corrections/
overlays at the new chart paths, and add a README noting the originals were not
geometry-wrong. Broader than S-0115-05 (which targets only t0114's dots-only artefact); the
two can be merged into one correction task. Recommended task types: correction.

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
<summary>📊 <strong>Re-run G.2 NMDA units calibration after BEDB_BASE_POINT retune
to land the cluster re-score</strong> (S-0090-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-03` |
| **Kind** | evaluation |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0090 Phase G.2 ran the 7-point gnmda_dend sweep (1e-5 to 1e-2 uS) but every level returned
NaN per-spine peak conductance because the procedural Bed-B cell diverges during stimulus
simulation. After S-0090-01 corrects the silent-cell blocker, re-run the 7-point sweep, build
the calibration curve mapping NetCon weight to per-spine conductance, and re-score the t0086 /
t0088 cluster centroids' NMDA per-synapse exotic-ness against Sivyer 2013's published 0.1 nS
in the corrected units. The output is a definitive verdict on whether t0086 / t0088's NMDA
~85-122 sigma exotic flag is driven by a units / scope mismatch or by a genuinely outlier
biological mechanism. Recommended task types: experiment-run, data-analysis.

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
<summary>📂 <strong>Re-type SWC by section role (soma / primary / mid / terminal)
as a sibling dataset asset</strong> (S-0009-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-06` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The calibrated SWC uses only SWC type codes 1 (soma) and 3 (dendrite); downstream NEURON tasks
that set section-specific conductance densities (e.g., Na 150/150/30 mS/cm^2, K 70/70/35) must
re-derive Strahler order every time. Produce a sibling dataset asset
dsgc-baseline-morphology-calibrated-typed that re-types each row to 1 (soma), 5 (primary), 3
(mid), or 6 (terminal) using the calibration's bin labels. Topology, xyz, and parent_id are
preserved; only type_code changes. Add a conversion script and a smoke test that confirms
NEURON's Import3d loader accepts the extended type codes. Cuts duplicated Strahler
recomputation from every downstream channel-placement task. Creative_thinking.md section A3.
Recommended task types: feature-engineering.

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
<summary>📊 <strong>Recompute Cuntz balancing factor on t0122's strict-LEGIT cohort
(10 cells, PD>=30Hz) as a sanity check</strong> (S-0122-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0122-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0122_dsi_cytoplasm_volume_nsga2`](../../../overview/tasks/task_pages/t0122_dsi_cytoplasm_volume_nsga2.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000877`](../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/assets/paper/10.1371_journal.pcbi.1000877/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0122's Cuntz [0.2, 0.7] prediction was tested on the top-10 cells ranked by DSI WITHOUT
enforcing the strict-LEGIT PD-rate >= 30 Hz floor (those cells have PD-rate 23-26 Hz). The
strict-LEGIT cohort (10 cells, DSI<0.9999 AND PD>=30 Hz AND volume<=50000) is a distinct cell
set with potentially different morphological profile; whether they also fall in the Cuntz band
is unknown. Action: re-run compute_balancing_factor from t0122 code on each of the 10
strict-LEGIT cells (re-build morphology via generate_fixed_morphology from each cell's 68-d
vector in pareto_front_seed1524.json's legit_bool subset), report the bf distribution, and
compare to the top-10-by-DSI bf=0.500 finding. No new NSGA-II run; pure local-CPU post-hoc
analysis on the existing t0122 predictions asset. Recommended task types: data-analysis,
answer-question.

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
<summary>🔧 <strong>Register dsi_at_vrest and peak_hz_at_vrest metric keys in
meta/metrics/</strong> (S-0026-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0026-01` |
| **Kind** | technique |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0026_vrest_sweep_tuning_curves_dsgc`](../../../overview/tasks/task_pages/t0026_vrest_sweep_tuning_curves_dsgc.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

This task produced direction_selectivity_index and peak firing rate per V_rest but the keys
dsi_at_vrest_<value> and peak_hz_at_vrest_<value> are not registered under meta/metrics/. Add
metric definitions so future V_rest sweeps can report through the registered key registry and
appear in aggregate_metric_results output. Also reshape t0026 metrics.json variants from the
current map form to the array form required by task_results_specification.md multi-variant
format.

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
<summary>📊 <strong>Render and QA-check 2D/3D visualisations of
dsgc-baseline-morphology for documentation and synapse placement</strong>
(S-0005-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

The dsgc-baseline-morphology asset is currently described only by tabulated statistics (6,736
compartments, 129 branch points, 1,536.25 um path length). Downstream tasks that place
AMPA/GABA synapses by spatial rule (e.g., Park2014 3-5x null/preferred IPSC asymmetry,
S-0002-05 GABA/AMPA density scan) need a visual reference for the dendritic arbor,
branch-order map, and soma orientation; reviewers also need a figure for any project paper.
Render three QA visualisations (2D top-down dendrogram coloured by Strahler order, 2D xy
projection coloured by path distance from soma, 3D rotating xyz scatter) using neurom +
matplotlib (or NEURON's PlotShape) and register the figures plus the rendering script as an
answer asset describing what was checked. Flag any visible reconstruction artefacts (dangling
branches, axon stubs, soma asymmetry) for downstream tasks. Recommended task types:
data-analysis, answer-question.

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
<summary>📚 <strong>Replace lineage `_section_midpoint_xy` silent-(0,0) fallback with
t0120's strict raise-on-n3d==0 version</strong> (S-0120-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0120-02` |
| **Kind** | library |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0120 ships a strict `_section_midpoint_xy_strict` in `code/dump_helpers.py` that raises
`RuntimeError('degenerate section: h.n3d() == 0')` instead of silently returning `(0.0, 0.0)`
(lineage behaviour in `tasks/t0091_morphology_extended_nsga2_v1/code/trial_helpers.py` lines
160-178, copied into every NSGA-II task t0091-t0118). The silent fallback is dangerous: if a
degenerate dendrite section ever appears, every synapse on that section would be placed at the
world origin and the bar arrival-time projection would be silently wrong by tens of
micrometres. The 20-cell t0120 audit never tripped the strict raise but covers only 0.5% of
the t0117 pool. Concrete action: package the strict version as a shared library (or extend
S-0090-07's generator-promotion path) with a deprecation shim on lineage callsites so future
NSGA-II tasks (incl. t0122) raise loudly. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Replace simplified MOD kinetics with ModelDB-sourced canonical
implementations</strong> (S-0067-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0067-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0067's 5 MOD files use simplified HH-style m/h gates with V_half and time constants from
published values, but lose features specific to each channel: NaR's blocking-particle
mechanism (Khaliq-Raman 2003 uses a 5-state Markov scheme), Kv3 inactivation kinetics
(Wang-Buzsaki 1996 has a two-component decay), Kv4 voltage-dependent recovery (Hoffman 1997
has a recovery time constant tau_h(v) that varies 5-fold across V). NaR/Kv3/Kv4 in particular
showed almost no effect in t0067, possibly because the simplified kinetics miss their
distinctive features. Vendor the canonical ModelDB MOD files for these 3 channels (matching
the deposited cell's USEION conventions or wrapping in NONSPECIFIC_CURRENT shells) and re-run
the sweep. Expected: NaR/Kv3/Kv4 show real DSI effects, especially at high firing rates (>40
Hz).

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
<summary>🧪 <strong>Root-cause the 282-vs-177 synapse-count discrepancy in ModelDB
189347 vs Poleg-Polsky 2016 paper text</strong> (S-0046-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0046_reproduce_poleg_polsky_2016_exact/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Inspect `RGCmodel.hoc`'s ON/OFF cut plane (`z >= -0.16 * y + 46`) and `placeBIP()` to
determine why the deposited code instantiates 282 BIP/SACinhib/SACexc terminals when the paper
Methods text states 177 synapses. Test alternative cut-plane thresholds, density-based
sub-sampling, or supplementary-text geometry rules to find a code configuration that matches
the paper count. The 1.6x synapse overcount is the leading mechanistic hypothesis for the ~4x
PSP amplitude inflation observed in t0046 (PD PSP 23.25 mV vs paper 5.8 +/- 3.1 mV);
reconciling the count is a prerequisite for a quantitatively faithful Fig 1 reproduction.
Recommended task types: experiment-run, code-reproduction.

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
<summary>📚 <strong>Script the full NEURON + NetPyNE install for clean-machine
reproduction</strong> (S-0007-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-02` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The NSIS installer's /S flag ignored the /D= prefix, forcing an interactive GUI step. Ship a
PowerShell / bash installer script that (a) downloads nrn-8.2.7-setup.exe to a known path, (b)
drives the install with the correct prefix (either by default-install-then-move or by a
chocolatey recipe), (c) writes the .pth file into the uv venv, and (d) runs nrnivmodl + both
sanity sims end-to-end. This unblocks automated reproduction on a fresh Windows machine and
Linux / macOS CI runners.

</details>

<details>
<summary>🧪 <strong>SEClamp Fig 3A-E re-measurement across multiple V_clamp levels
(-85, -65, -45 mV) to vary GABA driving force</strong> (S-0049-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0049-04` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0049_seclamp_cond_remeasure`](../../../overview/tasks/task_pages/t0049_seclamp_cond_remeasure.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0049_seclamp_cond_remeasure/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0049 ran SEClamp at the single V_clamp = -65 mV which yields a small GABA driving force (-5
mV vs E_GABA = -60 mV) and amplifies noise on the GABA conductance estimate (SD +/- 1.98 nS at
PD). Repeat the per-channel isolation sweep at V_clamp in {-85, -65, -45} mV. The -85 mV
condition gives a 25 mV GABA driving force (5x improvement in GABA SNR) and inverts the
AMPA/NMDA driving force; the -45 mV condition reverses the GABA driving force sign and
increases NMDA Mg-block relief. Tests (a) whether the GABA PD/ND symmetry persists across
V_clamp (ruling out driving-force noise), (b) whether NMDA over-amplification depends on
holding voltage. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Sensitivity analysis: re-run DSGC simulations under alternative
Strahler tie-break rules and bin boundaries</strong> (S-0009-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

The primary bin (33 compartments) is set by max_strahler_order = 5 under a max-child
tie-break; a min-child or NeuroM section-based convention can push max_order to 6 and
reclassify the current 33 primary compartments as mid, jumping proximal Rin by ~15%
(creative_thinking.md section F3, E1). Produce 3-4 sibling calibrated SWCs under alternative
tie-break rules (max-child, min-child, NeuroM section_strahler_orders, two-bin collapse) and
run the downstream DSGC passive simulation from S-0009-01 on each. Report DSI, preferred peak,
HWHM, and proximal/distal Rin per variant; quantify the sensitivity of downstream metrics to
the heuristic choice. This makes the tie-break choice reviewable rather than arbitrary.
Recommended task types: experiment-run, comparative-analysis.

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
<summary>🔧 <strong>Stratified / per-seed-weighted bootstrap CI to replace t0121's
flat-resample 5-number bootstrap</strong> (S-0121-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0121-03` |
| **Kind** | technique |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0121_5seed_substrate_rate_canonical_report`](../../../overview/tasks/task_pages/t0121_5seed_substrate_rate_canonical_report.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0121's bootstrap CI is an unstratified resample of 5 per-seed rates with equal weight. With
per-seed denominators ranging 1344-5952 (4.4x spread), flat weighting under-weights the
more-precise seeds. Defensible alternatives: (a) cell-level resample stratified by seed
(preserve per-seed denominators, resample cells within each seed before averaging), or (b)
inverse-variance weighting with within-seed SE = sqrt(p*(1-p)/n_total). Concrete action:
implement both in a small `weighted_bootstrap.py` library, report all three CI variants (flat,
cell-stratified, inverse-variance) on the existing 5-seed data, and decide which is canonical
for downstream substrate-rate citations. Decision: if the cell-stratified CI excludes 0% and
is tighter than the flat CI, adopt as canonical and update t0121 numbers via correction.
Recommended task types: data-analysis, write-library.

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
<summary>🧪 <strong>Sweep paper-text biophysics (Ra 200, eleak -65, Na 200/70/35) to
test peak firing-rate shortfall</strong> (S-0024-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0024-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md) |
| **Source paper** | [`10.1016_j.celrep.2025.116833`](../../../tasks/t0024_port_de_rosenroll_2026_dsgc/assets/paper/10.1016_j.celrep.2025.116833/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Peak firing rate is 5.15 Hz in t0024 versus the paper's qualitative ~30-40 Hz and the t0004
envelope of 40-80 Hz. The paper text and the companion repository disagree on Ra, eleak, and
Na/K densities; the repository values were used as authoritative. Run a 2x2x3 sensitivity
sweep varying Ra (100/200), eleak (-60/-65), and Na density regime (code/paper/intermediate)
with 10 trials per condition at PD/ND to isolate which single parameter change recovers peak
rate without destroying DS. Scorer: t0012 tuning_curve_loss against the t0004 envelope.

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
<summary>📚 <strong>Tighten post-fix procedural soma to match the t0024 hand-coded
287 um^2 reference area</strong> (S-0092-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0092-02` |
| **Kind** | library |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0092_diagnose_morphology_generator_silence`](../../../overview/tasks/task_pages/t0092_diagnose_morphology_generator_silence.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

The shipped t0092 fix preserves the procedural cylinder geometry: post-fix soma area is ~707
um^2 vs t0024's hand-coded reference 287 um^2 (2.5x mismatch). Because t0083 channel densities
were calibrated on the smaller hand-coded soma, the post-fix BedB-equivalent overshoots the
original Bed B (peak Vm +11 mV vs +4.65 mV; 61 vs 41 spikes). Refine the fix to emit either
(a) a 7-pt3d frustum stack reproducing t0024's profile, or (b) a single cylinder with sec.L=15
um, sec.diam=15/3.2 um chosen so pi*d*L matches 287 um^2 exactly. Ship as a v2 of
generate_fixed_morphology; validate that the patched cell now produces ~41 spikes and peak Vm
~+5 mV under the unmodified t0083 vector. This eliminates a known second-order discrepancy
before t0091 launches. Recommended task types: write-library, experiment-run.

</details>

<details>
<summary>🔧 <strong>Tighten silence-guard threshold from
SILENCE_SPIKE_COUNT_THRESHOLD=10 to >=3 PD spikes minimum</strong>
(S-0113-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-06` |
| **Kind** | technique |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0113's 2 joint-pass cells are both silence-guard DSI=1.0 saturations with exactly 1 PD spike
and 0 ND spikes. The current guard (`SILENCE_SPIKE_COUNT_THRESHOLD = 10`) accepts these
single-spike configurations as legitimate, inflating both joint-pass count and the HV archive.
t0106 had 1 such cell (in 123); t0112 had 0; t0113 has 2 of 2 - silence-guard contamination
dominates at sparse seeds. Modify `evaluator.py` to require >=3 PD spikes (or a minimum
non-zero ND-spike floor) before computing ratio DSI; cells below the floor return DSI=NaN and
are excluded from the archive. Reanalyse the existing t0106/t0112/t0113 predictions assets
offline. Decision: if corrected t0113 joint-pass count is 0 but t0106/t0112 counts drop by
<=5%, adopt as project default. Recommended task types: data-analysis, infrastructure-setup.
Cost: <$0.20.

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
<summary>📚 <strong>Two-point driving-force saturation calibration library from t0052
+ t0053 IPSP data</strong> (S-0053-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0053-06` |
| **Kind** | library |
| **Date added** | 2026-04-27 |
| **Source task** | [`t0053_minimal_dsgc_spatial_gaba`](../../../overview/tasks/task_pages/t0053_minimal_dsgc_spatial_gaba.md) |
| **Source paper** | — |
| **Categories** | [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`cable-theory`](../../../meta/categories/cable-theory/) |

S-0052-05 proposes a single-task library to translate nominal gabaMOD conductance ratios into
somatic-voltage IPSP modulation using t0052's observation alone (3.0x conductance -> 1.54x
voltage). t0053 provides a second calibration point on the same morphology and placement:
1.94x active-count ratio -> 1.24x voltage ratio at fixed 2 nS per synapse. Build a calibration
library `gaba_drive_saturation` taking both t0052 and t0053 IPSP data and fitting a two-point
(extensible via S-0052-02 GABA-count sweep) voltage-vs-conductance saturation curve, exposing
`gaba_eff(n_active_synapses, peak_g_per_syn)` returning predicted somatic IPSP modulation
depth. Future scalar / spatial / hybrid inhibition models call this during design to check
whether their nominal parameters land in the saturating regime. Sharpens S-0052-05 with a
two-point dataset. Recommended task types: write-library.

</details>

<details>
<summary>🧪 <strong>Validate custom khhchan.mod biophysics with a dedicated sanity
simulation</strong> (S-0007-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0007-01` |
| **Kind** | experiment |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0007_install_neuron_netpyne`](../../../overview/tasks/task_pages/t0007_install_neuron_netpyne.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0007 sanity sims only exercise NEURON's built-in hh mechanism. khhchan.mod is compiled as
a smoke test but its biophysics are never run. Add a short task that inserts khhchan on a
1-compartment soma, drives it with the same IClamp protocol, and compares the resulting trace
against the built-in hh to confirm the custom mechanism produces physiologically plausible
spikes before downstream retinal tasks depend on it.

</details>

<details>
<summary>📚 <strong>Vast.ai cost-watchdog parameterisation: idle-timeout teardown and
post-watchdog termination to prevent $3+ idle overrun</strong> (S-0102-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0102-08` |
| **Kind** | library |
| **Date added** | 2026-05-12 |
| **Source task** | [`t0102_seedscale_n4_gen20`](../../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0102 cost overrun ($12.07 vs $8 plan cap) decomposed as $8.46 productive NSGA-II compute
(per-seed $4 watchdog behaved as designed) plus $3.51 idle uptime: $0.11 setup, ~$1.5 from a
dead initial subagent before recovery, ~$2 post-watchdog billing before teardown.
results_detailed.md Limitations records this. Harden the cost-watchdog infrastructure: (i)
idle-CPU watchdog that destroys the instance if no NEURON worker processes have run for > 15
minutes; (ii) chain the per-seed cost watchdog directly into instance teardown rather than
just terminating the NSGA-II loop; (iii) standardise the offer-rate hourly-price source (t0102
billed $0.4852/hr while the watchdog read $0.4690/hr base, drift ~$0.1/hr over 24 h). Small
library change in arf/scripts/utils plus task-level orchestration. Recommended task types:
write-library, infrastructure-setup. Cost: ~$0 development + recovered ~$3/task in subsequent
runs.

</details>

<details>
<summary>📊 <strong>Verify Carter-Bean 2009 ATP/AP/cm benchmark and replace
plan-quoted 2.41e21 ATP/cm typo</strong> (S-0123-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0123-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0123's plan quoted the Carter-Bean 2009 Purkinje-cell ATP/AP/cm benchmark as 2.41e21 ATP/cm
-- 13 orders off plausible physics. Back-of-envelope (peak seg.ina ~ 100 mA/cm^2, segment area
~ 1e-8 cm^2, 2 ms AP window, e = 1.602e-19 C, 3 Na+/ATP) gives ~3e9 ATP/AP/cm; t0123's
observed 6.15e8 ATP/cm on the canonical Bed B cell is within an order of magnitude of that
estimate. The smoke gate fell back to the plausibility band [1e6, 1e14] ATP/cm rather than the
strict +/-30% Carter-Bean band; intervention/carter_bean_benchmark_mismatch.md was filed.
Carter and Bean 2009 (DOI 10.1016/j.neuron.2009.12.011) is NOT in the project corpus. Action:
(1) download the paper via /add-paper; (2) extract the correct ATP/AP/cm value; (3) write a
t0097-style correction overlay updating the metabolic_energy_atp_per_spike entry; (4) update
the smoke-gate strict band in future ATP NSGA-II templates. Recommended task types:
download-paper, correction.

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
<summary>🧪 <strong>Vm-trace deep-dive of t0123 cell 2 (MI=1.459, PD=2.86 Hz) to
explain near-silent count-MI mechanism</strong> (S-0123-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0123-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0123_bedb_mi_atp_per_spike_nsga2`](../../../overview/tasks/task_pages/t0123_bedb_mi_atp_per_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Cell 2 on the t0123 Pareto front reaches the highest mi_count_bits = 1.459 (73% of the log2(4)
= 2.0 ceiling) at PD-rate 2.86 Hz, DSI 0.316. How does a near-silent cell produce a clean
spike-count direction signal across 4 antipodal directions? Mirroring the t0084 cell-767
deep-dive, this task should single-cell-resimulate cell 2 from its 68-d vector under the
EPSP_PASSIVE / IPSP_PASSIVE / FULL standard mode trio (memory
`feedback_dsgc_measurement_protocol.md`), record somatic Vm and per-compartment g_E / g_I at
each direction, identify which subset of (channel densities, synapse placement, morphology
bf=0.236, soma-share 94.5%) is driving the across-direction spike-count variance, and produce
a one-cell mechanism narrative. Single-cell, no NSGA-II; local-CPU runtime <2 h. Output: one
answer asset on the mechanism plus a Vm / g_E / g_I trace figure pack. Recommended task types:
experiment-run, data-analysis, answer-question.

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
<summary>📚 <strong>Add a degenerate-section detector to the NSGA-II evaluation loop
(flag cells with any h.n3d() == 0 section)</strong> (S-0120-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0120-03` |
| **Kind** | library |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Out of scope for t0120 but flagged during it: the procedural DSGC generator could in principle
produce dendrite sections whose pt3d count is zero (degenerate stubs) under combinations of
asymmetry knobs not covered by existing t0092 / t0120 tests. Such sections would silently
corrupt synapse placement and bar arrival timing under the lineage `_section_midpoint_xy` (see
S-0120-02). Concrete action: extend the NSGA-II eval loop (used by t0122 and future NSGA-II
tasks) with a one-line check after `generate_fixed_morphology`: `for sec in cell.all_dends:
assert int(cell.h.n3d(sec=sec)) > 0`. If the assertion fires, mark the individual as
infeasible (constraint violation) and record the failing 14-d morphology vector so the
generator can be patched. Pairs naturally with S-0092-05 (generator regression battery) and
S-0120-02. Recommended task types: write-library, infrastructure-setup.

</details>

<details>
<summary>🧪 <strong>Add Ih (HCN) channel to dendrites and measure its effect on E-I
integration window</strong> (S-0022-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0022-08` |
| **Kind** | experiment |
| **Date added** | 2026-04-21 |
| **Source task** | [`t0022_modify_dsgc_channel_testbed`](../../../overview/tasks/task_pages/t0022_modify_dsgc_channel_testbed.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0022 testbed currently has no Ih (HCN) channels in DEND_CHANNELS. Literature prior from
t0019 (voltage-gated-channels survey) flags Ih as a common dendritic modulator: it lowers
input resistance and shortens the E-I temporal window over which coincidence matters. Add Ih
at a realistic dendritic density (e.g., 1e-5 S/cm^2 following hippocampal CA1 values as a
start) to the DEND_CHANNELS forsec block and rerun the canonical 12-angle x 10-trial sweep
plus an EI_OFFSET sweep in {5, 10, 15, 20, 30} ms. Expected outcome: the E-I integration
window narrows (only tight E-I offsets produce DSI, long offsets stop working), quantifying
the dendritic-integration timescale imposed by Ih. Dependencies: t0022 library asset,
S-0022-03 infrastructure for EI offset sweeps if already done. Effort ~10 hours. Recommended
task type: experiment-run.

</details>

<details>
<summary>📚 <strong>Add NMDA_MgBlock voltage-clamp sanity test as a reusable
verificator across all NMDA-bearing DSGC tasks</strong> (S-0055-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0055-07` |
| **Kind** | library |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0055_nmda_mg_block_dsi_recovery`](../../../overview/tasks/task_pages/t0055_nmda_mg_block_dsi_recovery.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

t0055 introduced a single-synapse SEClamp sanity test (`test_nmda_mg_block_voltage_dep.py`)
that validated the Jahr-Stevens Boltzmann at v in {-80, -60, -40, -20, 0, +20} mV (peak g
monotonic; peak g(-80)/peak g(-20) = 0.0167). Promote this into a reusable
arf/scripts/verificators/ check that any DSGC task using NMDA_MgBlock can invoke as a
precondition. The check loads the task's compiled NMDA mechanism, runs the 6-voltage clamp,
and asserts the monotonicity + threshold pattern within tolerance. Companion to S-0054-04
(gNMDA = 0 baseline-equivalence verificator). Pass criterion: verificator script exists, runs
against t0055 and passes; documentation describes when downstream tasks should invoke it.
Recommended task type: write-library, infrastructure-setup.

</details>

<details>
<summary>📚 <strong>Add UMAP to project dependencies; re-visualise t0086 + t0088
clusters</strong> (S-0088-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0088-06` |
| **Kind** | library |
| **Date added** | 2026-05-06 |
| **Source task** | [`t0088_recluster_marginals_and_vm_motifs`](../../../overview/tasks/task_pages/t0088_recluster_marginals_and_vm_motifs.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0088 fell back to PCA(n=2) for cluster visualisation because umap-learn is not in the
project's pyproject.toml. UMAP would likely show different (potentially clearer) cluster
structure for the small 13-cell pool. Add `umap-learn>=0.5` to pyproject.toml; re-run
select_representatives.py (already imports umap inside try/except); re-publish
cluster_umap.png. Apply the same to t0086's cluster_pca.png if relevant. Pure tooling change;
<30 min wall-clock, $0 cost. Recommended task types: infrastructure-setup, data-analysis.

</details>

<details>
<summary>📚 <strong>Backport t0046's GUI-free `dsgc_model_exact.hoc` driver as a
reusable library used by t0008/t0020/t0022 successors</strong> (S-0046-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0046-06` |
| **Kind** | library |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0046_reproduce_poleg_polsky_2016_exact`](../../../overview/tasks/task_pages/t0046_reproduce_poleg_polsky_2016_exact.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0046's `dsgc_model_exact.hoc` is a from-scratch GUI-free derivative of `main.hoc` that wraps
`simplerun(exptype, dir)` and exposes `b2gnmda`, `flickerVAR`, and `stimnoiseVAR` as post-call
overrides honouring the silent `achMOD = 0.33` rebind. Package this driver (plus
`code/run_simplerun.py`) into a separate reusable library asset that t0008, t0020, t0022, and
downstream optimisation tasks can import directly, replacing their bespoke headless driver
scaffolding. This eliminates duplicated bootstrap code and gives every downstream port a
single audited entry point with the noise-globals override mechanism already wired.
Recommended task types: write-library.

</details>

<details>
<summary>📚 <strong>Build nsga2-stop CLI helper or SIGTERM handler to replace awkward
intervention/stop.md UX</strong> (S-0114-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0114-06` |
| **Kind** | library |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0114_seed7755_no_autostop`](../../../overview/tasks/task_pages/t0114_seed7755_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0114's run was terminated by operator stop via the intervention/stop.md sentinel file: the
operator must SSH into the Vast.ai instance, create a magic file in the task folder, and the
next polling cycle picks it up. This works but is awkward over high-latency SSH and requires
remembering the exact filename. Concrete action: build a small CLI nsga2-stop that writes the
sentinel file in one command (e.g., `nsga2-stop --task t0114_seed7755_no_autostop`), and / or
wire a SIGTERM handler into nsga2_driver.py that triggers the same graceful-shutdown path
(current SIGTERM behaviour is abrupt kill, losing in-progress generation). Reduces
operator-stop latency from ~30 s to ~2 s. Reusable across all NSGA-II tasks. Recommended task
types: write-library, infrastructure-setup. Cost: <$0.10.

</details>

<details>
<summary>🧪 <strong>Cross-seed 68-d signature of silence-guard cells: same parameter
basin or seed-specific artefacts?</strong> (S-0113-08)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-08` |
| **Kind** | experiment |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0106 had 1 silence-guard DSI=1.0 cell, t0112 had 0, t0113 has 2. If silence-guard cells
cluster in a specific 68-d region (e.g., low somatic Nav + high Kv4 + central soma), they
represent a reproducible 'pathological basin' the NSGA-II driver should avoid. If scattered
randomly, they are seed-specific artefacts and no driver change is needed. Pool the 3
silence-guard cells from t0106 and t0113 plus a control set of 50 high-PD-low-DSI cells from
each task; run hierarchical clustering on z-scored 68-d vectors (using S-0112-04's metric if
available). Decision: if silence-guard cells cluster together with NMI > 0.7 vs random
samples, add a 'silence-pathology penalty' to the NSGA-II objective; otherwise no driver
change. DISTINCT from S-0112-08 (clusters JOINT-PASS cells across seeds, not silence-guard
cells). Recommended task types: data-analysis, comparative-analysis. Cost: <$0.20.

</details>

<details>
<summary>🧪 <strong>Diagnose NEURON single-process state-leak that hung t0093
sequential validation gate</strong> (S-0093-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0093-04` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0093_resweep_and_t0090_correction`](../../../overview/tasks/task_pages/t0093_resweep_and_t0090_correction.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0093 implementation initially attempted a 5-cell validation gate in `--max-workers 1`
(sequential) mode; the run hung beyond the wall-clock window and had to be killed and
restarted in parallel mode (which completed in 7m44s). Hypothesis: NEURON state-leak between
cells in the same Python process -- residual Section / NetCon / Vector references pile up in
`h` despite t0090's `_LIVE_CELLS` defense, eventually slowing or stalling `h.run()`. Reproduce
on a 5-cell sequential run, instrument `len(h.allsec())` and `len(h.List('NetCon'))` between
cells, and try (a) explicit `for sec in list(h.allsec()): h.delete_section(sec=sec)`, (b)
`h('forall delete_section()')`, or (c) creating a fresh `neuron.h` namespace per cell. Output:
fix in t0080's library or documented note + minimal reproducer. Matters for single-process
debugging and low-parallelism interactive runs. Recommended task types: experiment-run.

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
<summary>📊 <strong>Evaluate NEURON 9.0.x C++ MOD-file migration readiness for
project adoption</strong> (S-0003-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-05` |
| **Kind** | evaluation |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

NEURON 9.0.0 and 9.0.1 (Sep-Nov 2025) migrate MOD-file semantics to C++ and add Python 3.14
wheels. The t0003 survey picked 8.2.7 for conservatism. Create a task that (1) installs 9.0.1
into a sandbox venv, (2) rebuilds the Poleg-Polsky 189347 DSGC model from S-0003-02 under
9.0.x, (3) runs the existing DSGC simulations under both 8.2.7 and 9.0.1, and (4) records any
behavioural differences. This decides whether the project should upgrade before or after the
first round of tuning-curve experiments.

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
<summary>📚 <strong>Extract PerGenerationPoolRestart into a shared library asset for
future NEURON-pymoo NSGA-II tasks</strong> (S-0106-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0106-05` |
| **Kind** | library |
| **Date added** | 2026-05-18 |
| **Source task** | [`t0106_long_pdnd_nsga2_300gen`](../../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0106's nsga2_driver.py adds a PerGenerationPoolRestart class that calls
multiprocessing.Pool.terminate() + recreate() at the start of every generation; this dropped
gen 26's wall-clock from 110 min to 3 min by clearing NEURON HOC namespace leaks and C-side
mechanism state that the per-cell evaluator could not free. This is reusable infrastructure
for every future long-horizon NEURON-pymoo NSGA-II task and complements S-0104-06
(instrumentation of the leak) by providing the concrete mitigation. Package the class as a
library asset under tasks/<libtask>/assets/library/per_generation_pool_restart/ with
details.json, a description.md, and the importable module. Downstream tasks (multi-seed
confirmation S-0106-01, soma-offset sweep S-0106-04, IBEA on 2-direction substrate S-0106-06,
dense morphology sweep S-0106-07) import the library instead of re-implementing it.
Recommended task types: write-library. Cost: < $0.20 (local only; no Vast.ai).

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
<summary>📊 <strong>Introduce per-trial spike-count distribution metric to
distinguish failures from timing shifts</strong> (S-0039-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0039-06` |
| **Kind** | evaluation |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0039_distal_dendrite_diameter_sweep_t0022_gaba4`](../../../overview/tasks/task_pages/t0039_distal_dendrite_diameter_sweep_t0022_gaba4.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0039's peak firing drops from 15 Hz at D=0.5x to 13 Hz at D=2.0x - a 2 Hz difference could be
2 fewer spikes per trial at the same timing, or a shift in the spike-count DISTRIBUTION (e.g.,
bimodal failures). Currently metrics_per_diameter.csv reports only the mean; adding per-trial
spike-count histograms would separate 'failure rate' from 'timing shift' in cable-theory
interpretation. Low effort: reuse existing sweep_results.csv, add a standalone analysis script
that writes a histogram per diameter.

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
<summary>📚 <strong>Latin-hypercube quasi-random GA-seed sampling for substrate-rate
confirmation (replaces ad-hoc seed picks)</strong> (S-0113-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-07` |
| **Kind** | library |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The current 3-seed sample (44, 77, 2247) uses three independent draws (curated, semi-random,
fully random) which does not guarantee good coverage of the seed-space [0, 9999]. For the
final 5-seed substrate-rate report, draw the GA seeds via a 1-d Latin hypercube over [0, 9999]
(or a Sobol' sequence) to ensure stratified coverage. This is methodologically defensible
against reviewer pushback that the seed sample is too small to characterise substrate
variance. The two further seeds for S-0113-01 / S-0112-01 should be drawn from the LH/Sobol'
sequence conditional on the 3 already-used (44, 77, 2247) being part of the sequence. Output:
a small `gaseed_sampler.py` library asset plus a one-line update to the seed-selection comment
in `task_description.md` templates. Recommended task types: write-library,
infrastructure-setup. Cost: <$0.10 (local only).

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
<summary>📚 <strong>Package per-synapse conductance recorder and qualitative-shape
verdict helpers as a reusable library</strong> (S-0047-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-04` |
| **Kind** | library |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0047's `code/run_with_conductances.py` attaches `Vector.record(syn._ref_gAMPA / _ref_gNMDA /
_ref_g)` to every BIPsyn, SACexcsyn, and SACinhibsyn at cell-build time. It is the only
audited per-channel conductance recorder in the project and a prerequisite for any future Fig
3A-E reproduction (including S-0047-02's SEClamp variant). Package it as a reusable library
asset with: (a) `attach_conductance_recorders(cell, dt_record_ms)` that operates on any
t0046-derived cell; (b) qualitative-shape verdict helpers from `code/compute_metrics.py`
reporting PD/ND ratios per channel as a positive finding (AMPA flat across gNMDA, GABA ND ~2x
PD reproduce paper qualitative claims even though absolute amplitudes do not match); (c) a
single-trial smoke test. Distinct from S-0046-06 which packages the GUI-free `simplerun()`
driver. Recommended task types: write-library.

</details>

<details>
<summary>📊 <strong>Per-anchor strip layout of the morphology grid as a complement
to DSI-sorted layout</strong> (S-0098-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0098-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0098_visualise_pareto_morphologies`](../../../overview/tasks/task_pages/t0098_visualise_pareto_morphologies.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The current 8x8 grid sorted by DSI mixes anchors visually. A complementary layout with one row
per anchor (4 rows: bedb_like / pd_asymmetric / nd_asymmetric / alt_topology, sorted within
each by DSI) would make anchor-versus-anchor comparison easier to read and would highlight the
alt_topology vs bedb_like basin separation more directly. Trivial extension of t0098's
_plot_grid using groupby. Recommended task type: data-analysis. Cost: $0.

</details>

<details>
<summary>📂 <strong>Per-cell ex-vivo two-photon image segmentation of
141009_Pair1DSGC to produce a cell-specific diameter ground truth</strong>
(S-0009-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0009-07` |
| **Kind** | dataset |
| **Date added** | 2026-04-20 |
| **Source task** | [`t0009_calibrate_dendritic_diameters`](../../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Source paper** | — |
| **Categories** | [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The calibration imposes a nearby cell's diameters on our topology; a cell-specific ground
truth would validate or refute the transfer. The 141009_Pair1DSGC reconstruction came from the
Murphy-Baum / Feller two-photon rig; contact the original authors to obtain the raw image
stack and run a segmentation + radius-estimation pipeline (e.g., Vaa3D or neuTube) to recover
per-compartment diameters. Register the result as dsgc-baseline-morphology-imaged and use it
as the authoritative reference for sensitivity analyses like S-0009-05. Depends on external
data availability; likely requires an intervention for author contact. Recommended task types:
download-dataset, data-analysis.

</details>

<details>
<summary>🔧 <strong>Per-section L/lambda rather than mean-based for collapse
tests</strong> (S-0041-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0041-04` |
| **Kind** | technique |
| **Date added** | 2026-04-24 |
| **Source task** | [`t0041_electrotonic_length_collapse_t0034_t0035`](../../../overview/tasks/task_pages/t0041_electrotonic_length_collapse_t0034_t0035.md) |
| **Source paper** | — |
| **Categories** | [`cable-theory`](../../../meta/categories/cable-theory/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0041 used the 177-dendrite mean L (22.63 um) as the baseline for all L/lambda points. A more
accurate test would compute L/lambda per distal section and aggregate, rather than computing
L/lambda from an aggregate L. Small refactor of t0041 code; would be free to run since the
simulation data is already in hand.

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
<summary>📚 <strong>Project memory: re-pulling all_evaluations.json over SCP is slow;
build a streaming /tail variant</strong> (S-0115-06)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-06` |
| **Kind** | library |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

Across t0114 + t0115 the operator triggered ~12 SCP re-pulls of the all_evaluations_seed*.json
file (mean ~5 MB each). Each pull took 15-30 s SSH overhead, in total ~5 minutes of wasted
wall-clock just for fetches. A streaming variant (write a small remote helper that emits only
the new evaluations since the last fetch, indexed by generation; client maintains a local
accumulator) would reduce per-pull cost to <2 s. Concrete action: add `tail_evaluations.py` to
the t0114/t0115 family code; expose via a remote SSH alias `nsga2-tail`. Recommended task
types: write-library. Cost: <$0.05.

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
<summary>📊 <strong>Promote the t0052<->t0054 gNMDA=0 regression gate into a reusable
cross-task baseline-equivalence verificator</strong> (S-0054-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0054-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-28 |
| **Source task** | [`t0054_minimal_dsgc_ampa_nmda_scalar_gaba`](../../../overview/tasks/task_pages/t0054_minimal_dsgc_ampa_nmda_scalar_gaba.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0054's compute_metrics.py contains an ad-hoc hard-fail gate that compares the gNMDA=0 FULL
tuning_curve_full.csv row-by-row against t0052's tuning_curve_full.csv (passed at max |rate
diff| = 0.000e+00 Hz across 120 rows). This validates that placement, AMPA, GABA, and HH
soma+AIS are bit-identical between t0052 and t0054 baselines. Promote this comparison to a
reusable utility in arf/scripts/utils that takes (task_a_id, task_b_id, csv_filename,
parameter-equivalence-config) and produces a structured pass/fail report. Wire it into a
verificator-style entry point so downstream minimal-DSGC tasks (Mg-block follow-up S-0054-01,
joint sweep S-0054-02, tau2 sweep S-0054-05) can declare 'this task's gNMDA=0 baseline must
equal t0052' as a CI prerequisite. Acceptance: the helper exists in arf/scripts/utils,
reproduces the t0054 0e+00 Hz max-diff verdict, and is invoked in the new task's compute step.
Recommended task types: write-library.

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
<summary>📚 <strong>Promote the t0090 procedural morphology generator into a
top-level project library asset</strong> (S-0090-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0090-07` |
| **Kind** | library |
| **Date added** | 2026-05-07 |
| **Source task** | [`t0090_morphology_generator_diversity_test`](../../../overview/tasks/task_pages/t0090_morphology_generator_diversity_test.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The 14-knob procedural DSGC morphology generator is committed under
tasks/t0090_morphology_generator_diversity_test/code/ as a task-folder library asset. Once
t0091 confirms the generator works inside an NSGA-II eval loop, promote it into a top-level
reusable library (e.g. arf/libraries/dsgc_procedural_morphology) with a stable import path,
packaged unit tests, and a versioned release tag. This avoids the chronic problem of
downstream tasks (t0091, the future Option G real-cell library task, future Bed-A
morph-extended runs) needing to import from a deeply-nested task-folder path. Recommended task
types: write-library, infrastructure-setup.

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
<summary>📊 <strong>Refine spatial audit with dendritic-branch identity
classification (proximal-PD / proximal-ND / distal)</strong> (S-0050-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0050-04` |
| **Kind** | evaluation |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0050_audit_syn_distribution`](../../../overview/tasks/task_pages/t0050_audit_syn_distribution.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0050 used three midline-x conventions (soma_x, zero, BIPsyn-locx-median) to classify synapses
as side_a / side_b. A more biophysically meaningful classification partitions synapses by
dendritic branch identity: walk the section tree from soma, label each first-order branch as
proximal-PD or proximal-ND based on its dendritic-field axis, then label deeper segments as
distal. This finer partition would reveal whether the 282-synapse population has
within-PD-branch or within-ND-branch density gradients invisible to a single x-midline split,
and would provide the substrate-level data needed to design any future per-branch synaptic
modification (cf. S-0050-01 / S-0050-02). Pure post-hoc analysis on existing
extract_coordinates outputs. Recommended task types: data-analysis.

</details>

<details>
<summary>🔧 <strong>Remove the dead ANGLES_8DIR_DEG constant from
constants_electrophys.py</strong> (S-0104-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0104-03` |
| **Kind** | technique |
| **Date added** | 2026-05-14 |
| **Source task** | [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0080-era 8-direction angle constant ANGLES_8DIR_DEG remains in
tasks/t0080_*/code/constants_electrophys.py and is still re-exported into downstream task
forks despite t0091 onwards using the 16-direction ANGLES_16DIR_DEG vector exclusively. The
8-direction code path is dead; the constant pollutes the namespace and is a recurring source
of confusion in code reviews. Action: write a small correction task that records a
corrections/<id>.json file removing ANGLES_8DIR_DEG from the t0080 constants module's
effective namespace, plus a downstream task that imports the corrected constants and confirms
no module under tasks/ resolves the symbol. Recommended task types: write-library. Cost: <
$0.10 (local-only, no Vast.ai).

</details>

<details>
<summary>📚 <strong>Render AIS endpoints in the morphology grid</strong> (S-0098-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0098-03` |
| **Kind** | library |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0098_visualise_pareto_morphologies`](../../../overview/tasks/task_pages/t0098_visualise_pareto_morphologies.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0090's MorphologyResult.section_endpoints_xy does not register AIS endpoints, so t0098 omits
AIS in the grid panels. A small generator extension to populate the AIS xy entries would let
t0098's grid show the AIS as a distinct colored line per panel, enabling visual cross-checks
of ais_length_um across the Pareto. Either extend the generator or compute the AIS endpoint
locally from soma + ais_length_um direction in t0098's plotting code. Recommended task type:
write-library. Cost: $0.

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

<details>
<summary>🧪 <strong>Sweep Kv3 alone (no Nav1.6) to validate the kinetic-model
effect</strong> (S-0068-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0068-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0068_t0067_nav16_kv3_coexpression_rescue`](../../../overview/tasks/task_pages/t0068_t0067_nav16_kv3_coexpression_rescue.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0067 sweep showed Kv3 alone (without Nav1.6) had essentially no effect on firing rate or DSI
(DSI = 0.80 → 0.82 across low/med/high). t0068 shows Kv3 also has no rescue effect on top of
Nav1.6. To confirm that this isn't a model artefact (e.g., Kv3 not engaging because of an MOD
bug), run a finer Kv3-only sweep with very high densities (60, 200, 500 mS/cm^2) and check
whether SOME density level produces a measurable firing-rate effect. If Kv3 at 500 mS/cm^2
still does nothing, our simplified Kv3 MOD likely needs revision to a richer kinetic scheme
(e.g., Wang-Buzsaki with two-component decay).

</details>

<details>
<summary>🧪 <strong>Test cad insertion on dendrites only (not soma)</strong>
(S-0074-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-10` |
| **Kind** | experiment |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Inserting cad on the soma shifted Bed A's baseline DSI from 0.7975 (no-cad regression) to
0.308 legacy / 0.193 vector-sum (with-cad). This shift is a structural artefact of soma-only
Ca-pool insertion. Real DSGCs have distributed Ca channels and Ca pools throughout the
dendrites. Test: insert cad on the dendritic compartments (not the soma), then re-run a small
validation sweep (baseline + 3 BK densities × 12 angles × 5 seeds = 240 trials). Hypothesis:
dendritic cad insertion preserves the no-cad baseline DSI more closely while still providing
functional Ca for BK / SK channels in the dendrites. If confirmed, this is the right substrate
design for t0075 active-dendrite work and improves t0074's biological plausibility post-hoc.

</details>

<details>
<summary>🧪 <strong>Tighten AIS-to-soma Nav ratio hard floor from >=5 to >=7
(matching Werginz 2020 RGC point estimate)</strong> (S-0080-07)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0080-07` |
| **Kind** | experiment |
| **Date added** | 2026-05-04 |
| **Source task** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

t0080 enforces an AIS-to-soma Nav ratio >= 5 hard floor, justified primarily by Werginz 2024's
measured 17.3x for mouse alpha-ON-sustained RGCs and a conservative interpretation of Werginz
2020's RGC ratio (~7x for mouse OFF-alpha-T RGCs, in metadata only because the PDF is
paywalled). Tighten the floor to >=7 to match the Werginz 2020 point estimate and re-run
NSGA-II at the same pop=24 / gen=8 budget. The hypothesis is that the >=5 floor still permits
configurations near the AIS-disabled corner that contribute to the t0080 Pareto compression.
Compare Pareto-front geometry and joint-closest distance against t0080's >=5 result. Cost
~$0.75. Recommended task types: experiment-run.

</details>

<details>
<summary>📊 <strong>Validate vendored BK/SK MOD kinetics against published RGC
patch-clamp data</strong> (S-0074-09)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0074-09` |
| **Kind** | evaluation |
| **Date added** | 2026-05-02 |
| **Source task** | [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

The vendored BK MOD comes from Mainen-Sejnowski 1996 (cortical pyramidal); SK from Hay 2011
(L5 pyramidal). Their kinetics may not match RGC patch-clamp recordings. Run voltage-clamp
simulations on a single soma in NEURON for each MOD (step protocol from -90 to +40 mV in 10 mV
steps, 100 ms duration) and compare resulting current traces against Pfeiffer-Friedrich 2012
(mouse RGC BK) and Wang 2014 (mouse RGC SK). If the activation V_half or time constants
deviate by > 20%, retune the MOD parameters or vendor an RGC-specific MOD instead. Cost: ~1
hour coding + 10 min sim + 30 min comparison plotting. Outcome: either a validation note in
the library description, or a v0.2.0 of the channel pack with retuned RGC-specific kinetics.

</details>

<details>
<summary>📊 <strong>Whole-pool geometry audit: scale t0120's 20-cell sample up to all
4431 t0117 cells (background batch)</strong> (S-0120-04)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0120-04` |
| **Kind** | evaluation |
| **Date added** | 2026-05-24 |
| **Source task** | [`t0120_morph_generator_geometry_audit`](../../../overview/tasks/task_pages/t0120_morph_generator_geometry_audit.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

t0120 verified geometry consistency on 20 cells stratified across asymmetry-parameter extremes
plus symmetric controls (0.5% of the t0117 pooled pool); 60 / 60 checks passed with max errors
four orders below threshold. A whole-pool audit would surface any rare combination of the 14
morphology knobs that triggers a frame mismatch outside the sampled strata. Concrete action:
reuse `code/dump_cells.py` and `code/run_checks.py` from t0120; iterate over all 4431 t0117
cells (skip per-cell pt3d JSON dump to keep disk bounded; retain only the per-cell check
pass/fail row); write a single coordinate_consistency_checks_full.csv and a short summary
stating the count of any cell failing any check. Runs in background (~12 CPU hours
single-process); cost effectively $0. Low priority because the stratified sample already
covers realistic failure modes; this is defence-in-depth. Recommended task types:
data-analysis.

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
<summary>✅ <s>5-seed substrate-rate batch (S-0112-01) is now complete; write
canonical report</s> — covered by <a
href="../../../tasks/t0121_5seed_substrate_rate_canonical_report/"><code>t0121_5seed_substrate_rate_canonical_report</code></a>
(S-0115-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0115-02` |
| **Kind** | evaluation |
| **Date added** | 2026-05-21 |
| **Source task** | [`t0115_seed9354_no_autostop`](../../../overview/tasks/task_pages/t0115_seed9354_no_autostop.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0115 closes the S-0112-01 batch with 5 seeds (44, 77, 2247, 7755, 9354) on the identical 68-d
Bed B + 14-d morphology substrate. Final 5-seed mean LEGIT-joint-pass acceptance rate is 2.58%
+/- SE 1.50% (SD 3.35%, 95% CI -0.36% to +5.52%). Point estimate is 6.45x above Hay 2011
(0.40%) and 25.8x above Druckmann 2007 (0.10%), but the 95% CI brackets both literature
references. Three of five seeds (44, 7755, 9354) independently exceed Hay. Concrete action:
write a canonical substrate-rate report consolidating all five tasks' results into a single
comparable document with consistent metric conventions, embeddable in the project overview.
Recommended task types: data-analysis, answer-question. Cost: <$0.20.

</details>

<details>
<summary>✅ <s>Add a virtual AIS to the deposited cell and re-run the channel
sweep</s> — covered by <a
href="../../../tasks/t0069_t0067_ais_localised_channel_sweep/"><code>t0069_t0067_ais_localised_channel_sweep</code></a>
(S-0067-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0067-03` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

The deposited Poleg-Polsky cell has no axon initial segment (AIS). Real RGCs concentrate
Nav1.6 / Kv1 at the AIS at ~50× somatic densities (per t0019 priors: 2500-5000 pS/μm² for
Nav1.6 at distal AIS). Putting these channels on the soma in t0067 is a simplification that
almost certainly understates their effect on AP initiation timing and shape. Add a 30 μm AIS
section between soma and a virtual axon (1 mm passive cable) to the build_dsgc, then re-run
the t0067 channel sweep with insertion on the AIS instead of the soma. Expected: same channels
show much larger DSI effects (because the AIS, being smaller and electrically isolated, is
more sensitive to gnabar additions). Cost: ~1 hour code + ~10 min compute.

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
<summary>✅ <s>Bed B NSGA-II maximising DSI and minimising ATP-per-spike</s> —
covered by <a
href="../../../tasks/t0124_bedb_dsi_atp_per_spike_nsga2/"><code>t0124_bedb_dsi_atp_per_spike_nsga2</code></a>
(S-0097-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0097-02` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Source paper** | [`10.1371_journal.pcbi.1000840`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1000840/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/) |

Anchored to the canonical Attwell-Laughlin energy budget (47% of cortical signalling ATP per
spike). Remme et al. 2018's MSO function-vs-energy MOBO provides a direct methodology template
generalising to NEURON. DSGC's GABAergic-style fast-spiking should produce
Carter-Bean-2009-style Na/K-overlap penalty; the front should expand toward dramatically lower
energy as Na+ density and overlap are jointly reduced. Recipe: `(1/3) sum int(I_Na) dt / e`
per compartment per AP. Budget: 24-48 h Vast.ai EPYC at $0.30/h, total $8-15 — may exceed
per-task default; flag for explicit budget approval.

</details>

<details>
<summary>✅ <s>Bed B NSGA-II maximising DSI and minimising cytoplasm volume</s> —
covered by <a
href="../../../tasks/t0122_dsi_cytoplasm_volume_nsga2/"><code>t0122_dsi_cytoplasm_volume_nsga2</code></a>
(S-0097-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0097-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Source paper** | [`10.1371_journal.pcbi.1002107`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1371_journal.pcbi.1002107/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/) |

Highest biological-plausibility ranking in the t0097 catalogue. Cytoplasm volume is the most
evolutionarily grounded cost objective (Cajal cytoplasm-conservation; Cuntz et al. 2010's `bf`
in [0.2, 0.7] band; Chklovskii et al. 2002's 3/5-of-grey-matter wiring rule). Infrastructure
already in place via the t0093-validated procedural morphology generator. Falsifiable
prediction: high-DSI corner clusters at `bf` in [0.2, 0.7]. Budget feasibility: 12-24 h on
Vast.ai EPYC 7763 64-core at $0.30/h, total $4-8 (within the per-task $5 default; flag for $8
budget bump if needed). Same population/generation budget as t0091.

</details>

<details>
<summary>✅ <s>Bed B NSGA-II maximising MI and minimising ATP-per-spike (bits-per-ATP
front)</s> — covered by <a
href="../../../tasks/t0123_bedb_mi_atp_per_spike_nsga2/"><code>t0123_bedb_mi_atp_per_spike_nsga2</code></a>
(S-0097-05)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0097-05` |
| **Kind** | experiment |
| **Date added** | 2026-05-08 |
| **Source task** | [`t0097_multi_obj_optim`](../../../overview/tasks/task_pages/t0097_multi_obj_optim.md) |
| **Source paper** | [`10.1103_PhysRevLett.80.197`](../../../tasks/t0097_multi_obj_optim/assets/paper/10.1103_PhysRevLett.80.197/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Decouples function (information) from selectivity (DSI). Produces a bits-per-ATP Pareto front
directly comparable to Niven et al. 2007's empirical fly-photoreceptor 200-1000 bits/s
super-linear cost-vs-information curve. The DSGC bits-per-ATP ratio is unmeasured in the
literature, so the experiment closes a genuine open question. Tradeoff: this experiment does
not directly serve the project's first-question DSGC mission (DSI is not optimised); ranked
medium because it serves a broader scientific question rather than the project's specific
deliverable. Budget: 24-48 h Vast.ai EPYC at $0.30/h, total $8-15 — comparable to S-0097-02.

</details>

<details>
<summary>✅ <s>Calibrate realistic dendritic diameters for dsgc-baseline-morphology
to replace the 0.125 um placeholder radii</s> — covered by <a
href="../../../tasks/t0009_calibrate_dendritic_diameters/"><code>t0009_calibrate_dendritic_diameters</code></a>
(S-0005-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0005-02` |
| **Kind** | technique |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0005_download_dsgc_morphology`](../../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../../meta/categories/dendritic-computation/), [`cable-theory`](../../../meta/categories/cable-theory/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Every compartment in the downloaded CNG SWC carries the placeholder radius 0.125 um because
the original Simple Neurite Tracer reconstruction did not record diameters. Cable-theory
predicts segment diameter is the single most influential local-electrotonic knob (see
S-0002-04), so leaving the uniform placeholder in place will silently bias every downstream
biophysical simulation (axial resistance, attenuation, spike initiation threshold). Build a
diameter-calibration pipeline that applies a literature-derived order-dependent diameter taper
(e.g., Vaney/Sivyer/Taylor 2012 mouse ON-OFF DSGC profile, or the Poleg-Polsky 2016
distribution) keyed on Strahler order or path distance from the soma, write the calibrated SWC
as a new dataset asset (e.g., dsgc-baseline-morphology-calibrated), and report the per-order
diameter distribution against the original placeholder. Recommended task types:
feature-engineering, data-analysis.

</details>

<details>
<summary>✅ <s>CoreNEURON Vast.ai RTX 4090 benchmark to validate or replace the
assumed 5x speedup in the t0033 cost model</s> — covered by <a
href="../../../tasks/t0045_coreneuron_vastai_speedup_benchmark/"><code>t0045_coreneuron_vastai_speedup_benchmark</code></a>
(S-0033-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0033-01` |
| **Kind** | evaluation |
| **Date added** | 2026-04-22 |
| **Source task** | [`t0033_plan_dsgc_morphology_channel_optimisation`](../../../overview/tasks/task_pages/t0033_plan_dsgc_morphology_channel_optimisation.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/) |

The t0033 cost envelope rests on an unvalidated 5x CoreNEURON-over-stock-CPU-NEURON speedup
(91 s deterministic sim on RTX 4090 vs 456 s on single CPU core). The corpus documents Hines
1997 O(N) cable-solver scaling but predates GPU NEURON variants, so the 5x figure is a
literature-less guess that drives the largest sensitivity-band column. Run a short task that
(a) provisions one Vast.ai RTX 4090 under the existing filters, (b) builds CoreNEURON against
NEURON 8.2.7 with OpenACC/CUDA, (c) runs the t0022 deterministic 12-angle x 10-trial protocol
under stock NEURON and under CoreNEURON back-to-back, and (d) reports measured speedup and
per-sim USD. Outcome replaces the assumed 5x with a measured value and tightens or widens the
$23-$119 sensitivity band before the joint optimiser is commissioned. Recommended task types:
experiment-run, baseline-evaluation.

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
<summary>✅ <s>Halve somatic gnabar_HHst before attaching the AIS, then re-run the
sweep</s> — covered by <a
href="../../../tasks/t0075_bio_realistic_ais_param_sweep/"><code>t0075_bio_realistic_ais_param_sweep</code></a>
(S-0069-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0069-01` |
| **Kind** | experiment |
| **Date added** | 2026-05-01 |
| **Source task** | [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md) |
| **Source paper** | — |
| **Categories** | [`voltage-gated-channels`](../../../meta/categories/voltage-gated-channels/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`patch-clamp`](../../../meta/categories/patch-clamp/) |

t0069 falsified S-0067-03 because the AIS+axon couldn't dominate spike initiation against the
deposited cell's 400 mS/cm² somatic gnabar_HHst. The natural fix: reduce somatic gnabar to 200
mS/cm² (or 100), re-attach the same AIS+axon, and re-run the t0069 sweep. Hypothesis: with a
weakened soma, the AIS becomes the dominant spike-initiation zone and AIS-localised Nav1.6 /
NaP / NaR / Kv3 / Kv4 show ≥2× larger |ΔDSI| than at the unweakened-soma baseline.
Implementation is a 1-line patch to apply_params (or a new HOC override) plus the existing
t0069 sweep code; ~10 min compute. This is the prerequisite for any meaningful AIS channel
test on this cell.

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
<summary>✅ <s>Install and validate NEURON 8.2.7 + NetPyNE 1.1.1 toolchain on the
local workstation</s> — covered by <a
href="../../../tasks/t0007_install_neuron_netpyne/"><code>t0007_install_neuron_netpyne</code></a>
(S-0003-01)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0003-01` |
| **Kind** | library |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0003_simulator_library_survey`](../../../overview/tasks/task_pages/t0003_simulator_library_survey.md) |
| **Source paper** | — |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Create a task that `uv pip install neuron==8.2.7 netpyne==1.1.1` into the project's
virtualenv, compiles the bundled Hodgkin-Huxley MOD files with `nrnivmodl`, runs a
1-compartment sanity simulation, and records the installed versions, install-time warnings,
and simulation wall-clock in a task asset. Rationale: the t0003 survey selected this toolchain
but did not install it; the next simulation task needs a validated environment.

</details>

<details>
<summary>✅ <s>Multi-seed substrate-rate confirmation at restart cadence 10: N>=3 new
GA seeds on the t0106 substrate</s> — covered by <a
href="../../../tasks/t0115_seed9354_no_autostop/"><code>t0115_seed9354_no_autostop</code></a>
(S-0112-01)</summary>

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
<summary>✅ <s>Re-measure per-channel conductances under a somatic SEClamp on the
deposited DSGC to match paper Fig 3A-E modality</s> — covered by <a
href="../../../tasks/t0049_seclamp_cond_remeasure/"><code>t0049_seclamp_cond_remeasure</code></a>
(S-0047-02)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0047-02` |
| **Kind** | experiment |
| **Date added** | 2026-04-25 |
| **Source task** | [`t0047_validate_pp16_fig3_cond_noise`](../../../overview/tasks/task_pages/t0047_validate_pp16_fig3_cond_noise.md) |
| **Source paper** | [`10.1016_j.neuron.2016.02.013`](../../../tasks/t0047_validate_pp16_fig3_cond_noise/assets/paper/10.1016_j.neuron.2016.02.013/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`synaptic-integration`](../../../meta/categories/synaptic-integration/), [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

t0047 records `_ref_g` directly at each synapse and obtains summed peak conductances 6-9x the
paper's Fig 3A-E targets and per-synapse-mean values 28-90x under. Neither interpretation
reconciles. The paper's Fig 3A-E most likely reports a somatic voltage-clamp-recorded compound
conductance — a third quantity not measured here. Implement a NEURON SEClamp at the soma held
at -65 mV across the same 7-point gNMDA sweep, record `_ref_i` on the clamp, and deconvolve
per-channel conductance via `g(t) = i(t) / (V_clamp - e_rev)` with `e_NMDA = e_AMPA = 0` and
`e_SACinhib = -60 mV`. Compare against paper targets within +/- 25%. Distinct from S-0046-02
(synapse-count) and S-0046-05 (supplementary PDF); also distinct from S-0019-XX which targets
a downstream model build, not the deposited code. Recommended task types: experiment-run.

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
<summary>✅ <s>Widen HV-plateau detector window from 2 to 4-5 gens to prevent
premature trigger by single-cell HV jumps</s> — covered by <a
href="../../../tasks/t0114_seed7755_no_autostop/"><code>t0114_seed7755_no_autostop</code></a>
(S-0113-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0113-03` |
| **Kind** | technique |
| **Date added** | 2026-05-20 |
| **Source task** | [`t0113_t0106_seed2247_replicate`](../../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) |
| **Source paper** | [`10.1371_journal.pcbi.1012039`](../../../tasks/t0113_t0106_seed2247_replicate/assets/paper/10.1371_journal.pcbi.1012039/) |
| **Categories** | [`compartmental-modeling`](../../../meta/categories/compartmental-modeling/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/) |

t0113's HV-plateau detector fired at gen 14 (earliest of the 3-seed sample; t0112=21,
t0106=40) and BELOW Mohacsi2024's published 20-60 gen NSGA-II convergence range. The soft gen
11-12 transition (HV 35.98 -> 36.07 = +0.24%) satisfied the 1%-over-2-gens condition BEFORE
the gen 13-14 jump (+26% from a single silence-guard cell joining the archive). Current
constants (WINDOW=2, REL_THRESHOLD=0.01) are too aggressive when a single cell can inflate HV
>20% in one step. Widen WINDOW to 4-5 gens (matches Mohacsi2024 lower bound) and/or tighten
REL_THRESHOLD to 0.005. Validate by replaying the detector offline on the existing
t0106/t0112/t0113 HV traces. DISTINCT from S-0112-03 (single-seed re-run with auto-stop
disabled); this is a parameter-sweep + literature-grounded reparameterisation that becomes the
new project default. Recommended task types: data-analysis, infrastructure-setup. Cost:
<$0.20.

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
