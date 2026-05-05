# ⏹ Tasks: Not Started

4 tasks. ⏹ **4 not_started**.

[Back to all tasks](../README.md)

---

## ⏹ Not Started

<details>
<summary>⏹ 0084 — <strong>Vm-trace deep-dive of t0081 cell 767 to attribute the
joint-pass DSI mechanism</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0084_t0081_cell_767_vm_trace_deepdive` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Expected assets** | 1 answer |
| **Source suggestion** | `S-0081-03` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/), [`data-analysis`](../../../meta/task_types/data-analysis/), [`answer-question`](../../../meta/task_types/answer-question/) |
| **Task page** | [Vm-trace deep-dive of t0081 cell 767 to attribute the joint-pass DSI mechanism](../../../overview/tasks/task_pages/t0084_t0081_cell_767_vm_trace_deepdive.md) |
| **Task folder** | [`t0084_t0081_cell_767_vm_trace_deepdive/`](../../../tasks/t0084_t0081_cell_767_vm_trace_deepdive/) |

# Vm-Trace Deep-Dive of t0081 Cell 767 to Attribute the Joint-Pass DSI Mechanism

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell: **gen 7 cell
767 at DSI 0.494 / PD 11.39 Hz** on the v3 dendritic- spike-augmented Bed B substrate. This is
a major architectural milestone -- the first single-cell substrate in the project lineage to
satisfy `DSI >= 0.4 AND PD >= 10 Hz` simultaneously. However, the **biophysical mechanism for
the DSI improvement is unattributed**: cell 767's parameter vector contains non-zero values
for all five dendritic-spike machinery dimensions added in t0080 (`gnmda_dend`, `mg_conc_mm`,
`voff_nmda`, `nav16_dend_distal`, `nap_dend_distal`), and the joint-pass result could
plausibly arise from any one of three mechanisms or a combination:

1. **NMDA Mg-block recruitment.** Active dendritic NMDA receptors with Mg-block produce
   voltage-dependent multiplicative gain that supercharges ND-suppressed but PD-active
   synaptic input. This is the Sivyer 2013 / Branco-Hausser 2010 mechanism.
2. **Distal Nav1.6 dendritic spikes.** Backpropagating APs and locally initiated dendritic
   spikes from distal Nav1.6 produce non-linear amplification of PD-correlated input. This is
   the Oesch 2005 mechanism.
3. **NaP sustained depolarisation.** Persistent Na current at distal dendrites produces a
   sustained depolarising plateau that enhances PD firing without proportionally enhancing ND
   firing (assuming GABA asymmetry suppresses ND-direction NaP recruitment). This is the
   Goldfinger 2000 / Stuart 1999 mechanism.

Without per-direction Vm traces and per-channel current-flow analysis, we cannot distinguish
which mechanism (or combination) drives cell 767's DSI improvement. The attribution matters
strategically: it determines which mechanism to optimise first if t0083's extension finds
additional joint- pass cells, and which to test on Bed A in S-0081-05's cross-bed validation.

This task addresses project research question **Q4** (do active dendritic voltage-gated
conductances improve, degrade, or have no effect on the match to the target angle-frequency
curve compared with passive dendrites?) by mechanistically dissecting the first cell in the
project to deliver a positive answer to Q4 in joint form. Source suggestion: **S-0081-03**.

## Scope

### In scope

* Re-evaluate three cells from t0081's Pareto front in subprocess (eval-mode, no NSGA-II loop)
  on the v3 substrate (`de_rosenroll_2026_dsgc_ais_dendritic_spike`):
  * Cell 767 (joint-pass; DSI 0.494 / PD 11.39 Hz; gen 7).
  * Cell 637 (near-pass; distance 0.063; gen 6).
  * Cell 762 (near-pass; distance 0.086; gen 7).
* For each cell and each of 8 stimulus directions (0, 45, 90, 135, 180, 225, 270, 315 deg),
  record:
  * Vm at proximal soma.
  * Vm at one mid-dendrite section.
  * Vm at one distal-dendrite section (the same one that carries nav16_dend_distal and
    nap_dend_distal channel insertions).
  * Per-segment NMDA conductance trajectories (`gnmda` over time) at the distal dendrite
    synapses recruited during the simulation window.
  * Per-segment Nav1.6 and NaP currents at the distal dendrite (`ina` decomposed by
    mechanism).
  * Per-direction AIS spike onset times (zero-crossing of Vm at the AIS threshold trigger).
* Generate four figure assets per cell (12 figures total):
  1. **Per-direction Vm traces** at proximal soma, mid dendrite, distal dendrite (3-row
     stacked, 8-column grid).
  2. **NMDA conductance trajectories** at distal dendrite per direction (8-line plot).
  3. **Nav1.6 / NaP current decomposition** at distal dendrite per direction (8-direction
     stacked plot).
  4. **AIS spike onset histogram** per direction (polar plot or 8-bin bar chart).
* Identify, per cell, which mechanism dominates the DSI difference between PD (gen direction
  with peak rate) and ND (gen direction with minimum rate). Use a quantitative attribution
  metric: the **fractional contribution of each channel to the integrated dendritic
  depolarisation during the PD response window minus the same during the ND response window**.
* Produce one **answer asset** at
  `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` with short and full answer
  documents per the answer-asset specification, attributing cell 767's DSI mechanism to one
  (or a combination) of the three candidates.

### Out of scope

* Re-running NSGA-II or any optimisation (use cell 767/637/762 parameters verbatim).
* Modifying the substrate library asset.
* Bed A cross-bed comparisons (S-0081-05).
* Statistical multi-replicate confirmation across seeds (S-0081-01).
* Comparing alternative dendritic mechanisms (Ca2+ plateau, Ih, HCN) -- scope limited to the
  three machinery components present in the v3 substrate.

## Pass Criteria

* All 24 simulations (3 cells * 8 directions) complete with stable Vm traces (no numerical
  instabilities, no NaN values).
* All 12 figures generated and embedded in `results/results_detailed.md`.
* The answer asset clearly identifies the dominant mechanism (or combination, with relative
  weights) for cell 767's DSI improvement.
* The mechanism attribution for cells 637 and 762 (near-pass neighbours) is consistent with
  cell 767's attribution -- if not, the discrepancy is documented as a "near-pass cluster
  heterogeneity" finding.

## Estimated Compute Cost

* Local CPU only. No remote machine.
* Per-cell wall-clock: 8 directions * ~30-45 s/direction = ~3-6 min, plus per-segment
  recording overhead = ~5-10 min per cell.
* Total runtime: ~15-30 min for 3 cells.
* **Compute cost: $0**.

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides cell 767, 637, 762 parameter vectors (54-d
  natural-unit vectors from `results/data/all_evaluations.json`), the v3 substrate evaluation
  harness (`evaluate_cell.py` or equivalent), and the recording infrastructure for per-segment
  Vm / conductance / current trajectories.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset and its channel-insertion API
  (Nav1.6, NaP, NMDA Mg-block per dendritic section).

## Recommended Task Types

* `experiment-run` -- 24 single-cell NEURON simulations with extended recording.
* `data-analysis` -- per-channel current decomposition and figure generation.
* `answer-question` -- mechanism-attribution answer asset.

## Notes

The recording infrastructure for per-segment Vm, NMDA conductance, and Nav1.6 / NaP currents
must be added to or wrapped around t0081's eval harness. The harness currently records spike
counts per direction; this task adds full Vm traces and per-mechanism current decomposition.
Keep the recording additive -- the eval harness must remain backwards-compatible with t0081's
NSGA-II loop in case t0083 needs to re-use it.

The answer asset's confidence level should reflect the single-cell-replicate nature of the
analysis: cell 767's mechanism is attributed for that specific cell, but generalisation to
"all joint-pass cells in the v3 substrate" requires t0083's additional joint-pass cells (or
S-0081-01's multi-replicate study). The answer asset should state this explicitly in its `##
Limitations` section.

</details>

<details>
<summary>⏹ 0083 — <strong>Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau
stop</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0083_bedb_v3_extend_nsga2_gen8plus` |
| **Status** | not_started |
| **Effective date** | — |
| **Dependencies** | [`t0024_port_de_rosenroll_2026_dsgc`](../../../overview/tasks/task_pages/t0024_port_de_rosenroll_2026_dsgc.md), [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md), [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md), [`t0081_bedb_v3_warmstart_nsga2`](../../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) |
| **Expected assets** | — |
| **Source suggestion** | `S-0081-02` |
| **Task types** | [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Extend t0081 NSGA-II from gen-7 with adaptive HV-plateau stop](../../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) |
| **Task folder** | [`t0083_bedb_v3_extend_nsga2_gen8plus/`](../../../tasks/t0083_bedb_v3_extend_nsga2_gen8plus/) |

# Extend t0081 NSGA-II from gen-7 with Adaptive HV-Plateau Stop

## Motivation

t0081 (`bedb_v3_warmstart_nsga2`) delivered the project's first joint-pass cell at gen 7 cell
767 (DSI 0.494 / PD 11.39 Hz) on a 16-cell Pareto front across 768 evaluations ($2.39 on
Vast.ai 64-core EPYC 7B13, $0.2382/hr). Three observations from t0081's results motivate
continuing the run:

1. **Hypervolume grew monotonically with no plateau**: 6.59 (gen 0) -> 8.99 (gen 1) -> 9.24
   (gen 2) -> 11.08 (gen 3) -> 11.57 (gen 4) -> 13.14 (gen 5) -> 15.22 (gen 6) -> 16.33 (gen
   7). The 7.4% increase from gen 6 to gen 7 indicates the Pareto front is still actively
   expanding; the optimiser stopped not because it converged but because the planned gen=8
   budget ran out.

2. **Single joint-pass cell out of 768 evaluations.** Cell 767 is the only cell in the (DSI >=
   0.4 AND PD >= 10 Hz) box. The pass region of the parameter space is **discovered but not
   characterised**. A neighbourhood cluster (cell 637 at distance 0.063, cell 762 at distance
   0.086) sits just outside the box. Additional generations should populate this cluster and
   produce more joint-pass cells.

3. **The natural extension preserves t0081's evolutionary trajectory.** Continuing from
   t0081's gen-7 final population (96 surviving individuals after RankAndCrowding survival)
   avoids the cost of re-evaluating the warm-start initial population and lets NSGA-II
   continue evolving from a known good state.

This task addresses project research question **Q4** (active vs passive dendritic conductances
on directional tuning sharpness) by extending the search budget on the v3
dendritic-spike-augmented Bed B substrate that t0081 established as the project's working
substrate. Source suggestion: **S-0081-02** (extend t0081 NSGA-II to gen 12-15).

## Scope

### In scope

* Reuse t0081's harness (`tasks/t0081_bedb_v3_warmstart_nsga2/code/`) verbatim with two
  modifications:
  * Replace the Sobol/LHS + projected-Pareto warm-start init with a direct load of t0081's
    gen-7 final population (96 individuals, with objective values pre-computed and re-injected
    into pymoo's `Algorithm` state to skip re-evaluation).
  * Add an **adaptive HV-plateau watchdog** that terminates NSGA-II when `(HV(gen N) - HV(gen
    N-3)) / HV(gen N-3) < 0.01` averaged over the last 3 generations, AND only after a minimum
    of **5 additional generations** has been run (i.e., earliest possible stop is gen 12). The
    watchdog evaluates after every generation starting at gen 11 (so gen 11 needs HV from gens
    8, 9, 10, 11 -- a 3-gen lookback window starting at gen 8 is the first eligible window).
* Hard cap on total additional generations: **10** (gen 8 through gen 17 maximum). If the
  watchdog never fires, terminate at gen 17.
* Hard cost cap: **$5.00**. Spawn a budget watchdog identical to t0081's that monitors
  `instance_lifetime_hr * $0.2382/hr` and forces graceful termination if the projected
  end-of-generation cost would exceed $5.00.
* Reuse the `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset from t0080 unchanged.
  No substrate changes.
* Same Vast.ai instance class as t0081 (AMD EPYC 7B13 64-core, 503 GB RAM, $0.2382/hr).
* Compare final Pareto front, joint-pass cell count, HV trajectory, and per-generation
  parameter-distribution diagnostics against t0081 and t0080 baselines.

### Out of scope

* Substrate changes (no new dendritic-spike parameters; no new channels; no AIS
  modifications).
* Optimiser changes (NSGA-II via pymoo only; no NSGA-III, hybrid, or BO comparison).
* Multi-replicate confirmation (S-0081-01 covers that; deferred to a later task).
* Vm-trace analysis of cell 767 (S-0081-03 covers that; addressed in t0084 in parallel with
  this task).
* Bed A cross-bed replication (S-0081-05).

## Pass Criteria

* **Primary**: at least one **additional** Pareto cell with `DSI >= 0.4 AND PD >= 10 Hz`
  beyond t0081's cell 767 (i.e., total joint-pass cells
  > = 2). Characterises the joint-passing region by populating the near-pass cluster (cells 637 and
  > 762 from t0081 should evolve into the joint-pass box if the cluster is robust).

* **Secondary**: HV trajectory continues monotonically; final HV > t0081's 16.33; HV-plateau
  stop rule fires before the gen-17 hard cap OR the budget watchdog fires.

* **Acceptable negative**: zero additional joint-pass cells but final HV
  > t0081's 16.33 with HV-plateau detected before gen 17 -- documented as evidence that t0081's cell
  > 767 is an isolated point in the parameter space rather than a cluster, with implications for
  > downstream multi-replicate strategy.

## Estimated Compute Cost

* Per-cell wall-clock on t0081's instance: ~30 s (768 cells / 10.045 h instance lifetime ~= 47
  s/cell including overhead; NSGA-II gen 7 cells averaged ~30 s each).
* 5 additional generations at pop 96 = 480 cells @ 30 s = 4.0 h optimiser time; with 30 min
  Vast.ai instance overhead = 4.5 h * $0.2382 = ~$1.07.
* 10 additional generations at pop 96 = 960 cells @ 30 s = 8.0 h optimiser time; with overhead
  = 8.5 h * $0.2382 = ~$2.02.
* Most-likely range: **$1.50 - $3.00** depending on when the HV-plateau rule fires.
* **Hard cost cap: $5.00** (allows up to ~21 hours of instance lifetime, enough to absorb any
  per-cell wall-clock variance from the v3 substrate's dendritic-spike machinery).

## Dependencies

* **t0081_bedb_v3_warmstart_nsga2**: provides gen-7 final population (96 individuals with
  parameter vectors and objective values), the NSGA-II harness to extend, and the warm-start
  projection logic to inherit unchanged.
* **t0080_bedb_mobo_v3_dendritic_spike_nsga2**: provides the
  `de_rosenroll_2026_dsgc_ais_dendritic_spike` library asset (54-d v3 substrate) used
  unchanged.
* **t0078_bedb_mobo_v2_ais_tiered_ahp**: provides the AIS-augmented parent substrate from
  which t0080 derived the v3 substrate.
* **t0024_port_de_rosenroll_2026_dsgc**: provides the de Rosenroll 2026 DSGC NEURON port (Bed
  B base substrate before AIS / dendritic-spike augmentation).

## Recommended Task Types

* `experiment-run` -- the primary mode (NSGA-II continuation).

## Notes

The watchdog logic must be additive, not destructive: each new generation appends to t0081's
saved evaluation history rather than overwriting it. The final `all_evaluations.json` should
contain the union of t0081's 768 cells plus this task's additional cells (480-960), with
consistent generation numbering (t0081 ends at gen 7; this task starts at gen 8).

</details>

<details>
<summary>⏹ 0075 — <strong>Biologically-realistic AIS one-axis-at-a-time parameter
sweep on Bed A</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0075_bio_realistic_ais_param_sweep` |
| **Status** | not_started |
| **Effective date** | 2026-05-01 |
| **Dependencies** | [`t0008_port_modeldb_189347`](../../../overview/tasks/task_pages/t0008_port_modeldb_189347.md), [`t0067_t0065_soma_channel_addition_sweep`](../../../overview/tasks/task_pages/t0067_t0065_soma_channel_addition_sweep.md), [`t0069_t0067_ais_localised_channel_sweep`](../../../overview/tasks/task_pages/t0069_t0067_ais_localised_channel_sweep.md), [`t0074_channel_tuning_width_bed_a`](../../../overview/tasks/task_pages/t0074_channel_tuning_width_bed_a.md) |
| **Expected assets** | 1 library |
| **Source suggestion** | `S-0069-01` |
| **Task types** | [`build-model`](../../../meta/task_types/build-model/), [`experiment-run`](../../../meta/task_types/experiment-run/) |
| **Task page** | [Biologically-realistic AIS one-axis-at-a-time parameter sweep on Bed A](../../../overview/tasks/task_pages/t0075_bio_realistic_ais_param_sweep.md) |
| **Task folder** | [`t0075_bio_realistic_ais_param_sweep/`](../../../tasks/t0075_bio_realistic_ais_param_sweep/) |

# Biologically-Realistic AIS Parameter Sweep on Bed A

## Motivation

t0069 attached a virtual AIS plus 1 mm axon stub to Bed A (deposited Poleg-Polsky DSGC) and
re-ran the t0067 channel-addition sweep with each of {Nav1.6, NaP, NaR, Kv3, Kv4} on the AIS
instead of the soma. The sweep falsified S-0067-03's prediction (AIS-localised channels show
*larger* DSI effects than soma-localised) — it actually showed the opposite, with 11 of 15
channel conditions producing zero detectable DSI change. The cause was identified clearly: the
AIS+axon halved baseline PD firing (14.2 → 6.4 spikes) and silenced ND firing (1.6 → 0.0),
pushing baseline DSI to the trivial computational ceiling 1.0. The passive AIS+axon adds an
electrical sink that quenches the cell rather than relocating spike initiation; AIS-localised
channels at our densities cannot overcome the somatic 400 mS/cm² HHst Na drive.

The follow-up question this task answers: is there *any* DSGC + AIS configuration that
simultaneously contains all the channels biologically present in a vertebrate AIS (HHst basal
Na+K, Nav1.6, Kv3, Kv7 — the canonical RGC AIS quartet) and produces non-trivial DSI at a
biologically reasonable peak rate? "Decent DSI, not 1, and reasonable firing rate" maps to the
operational pass band {DSI in [0.3, 0.95], peak Hz in [5, 50]}. The right tool is not
optimisation — it is one axis at a time. NaP is excluded from the AIS channel set on two
grounds: (a) AIS NaP expression in RGCs is controversial; (b) the t0067 NaP-high finding (DSI
sign flip) suggests NaP destabilises the DSI mechanism rather than supporting it. BK and SK
are excluded because they localise primarily to soma and dendrites in RGCs, not to the AIS.

This task addresses RQ1 (somatic + AIS VGC combinations) and RQ4 (active vs passive
components). Source suggestions covered: S-0068-04 (move Nav1.6 + Kv3 to AIS), S-0069-01
(halve somatic gnabar before AIS), S-0069-02 (shrink AIS diameter to 0.5 micrometre),
S-0069-03 (vary axon length to probe sink), S-0069-04 (Nav1.6 + Kv3 on AIS at biological
densities).

## Scope

* Substrate: Bed A only (deposited Poleg-Polsky DSGC) plus virtual AIS + axon stub.
* AIS channel set: **{HHst basal Na + K, Nav1.6, Kv3, Kv7}**. NaP, BK, SK explicitly excluded.
* Encoding: 12-angle bar-rotation protocol (same as t0074 — cross-task comparable).
* Two-stage design: Stage 1 baseline calibration; Stage 2 per-axis sweep.

### Stage 1 — Baseline calibration

* Literature-informed AIS configuration (Wang et al. 2011, Carter et al. 2008 on mouse RGC
  AIS): AIS diameter 0.8 micrometre, AIS length 30 micrometre, axon stub 1.0 mm, AIS
  gnabar_HHst 4 0 0 mS/cm^2, AIS Nav1.6 medium density (~0.3 S/cm^2 from t0067 medium), AIS
  Kv3 medium density (~0.3 S/cm^2), AIS Kv7 low density (~0.1 S/cm^2; distal AIS, weaker than
  Nav and Kv3).
* Sweep soma `gnabar_HHst` across 6 candidates: {100, 150, 200, 250, 300, 400} mS/cm^2 (the
  t0069 baseline = 400).
* 6 candidates x 12 angles x 1 seed = 72 trials, ~5 min wall-clock.
* Pick the candidate that lands inside {peak Hz in [5, 50], DSI in [0.3, 0.95]}. If multiple
  candidates qualify, pick the one closest to the centre of the band ({peak ~ 20 Hz, DSI ~
  0.6}).
* If no candidate qualifies, the task halts at Stage 1 and reports a negative result with a
  recommendation for a follow-up that loosens the AIS configuration further (e.g., reduce AIS
  Nav1.6 density first, then re-attempt).

### Stage 2 — Per-axis sweep

From the Stage-1 baseline, vary one parameter at a time with all others held at baseline:

| # | Axis | Values | Non-baseline points |
| --- | --- | --- | --- |
| 1 | Soma `gnabar_HHst` (mS / cm^2) | {100, 200, 300, 400} | 3 |
| 2 | AIS `gnabar_HHst` (mS / cm^2) | {0, 100, 200, 400, 800} | 4 |
| 3 | AIS diameter (micrometre) | {0.4, 0.6, 0.8, 1.0, 1.5} | 4 |
| 4 | AIS length (micrometre) | {15, 30, 45, 60} | 3 |
| 5 | AIS Nav1.6 density | {0, low, medium, high} | 3 |
| 6 | AIS Kv3 density | {0, low, medium, high} | 3 |
| 7 | AIS Kv7 density | {0, low, medium, high} | 3 |
| 8 | Axon length (mm) | {0.1, 0.5, 1.0, 2.0} | 3 |

Total Stage-2 conditions: 1 baseline + 26 non-baseline = **27 conditions x 12 angles x 5 seeds
= 1620 FULL trials**, ~100 min wall-clock at the t0067 measured ~3.75 s / trial under CVODE.

### Width metrics per axis (cross-comparable with t0074)

For each condition, compute:

* **HWHM** in degrees from the 12-angle tuning curve.
* **Vector-sum DSI** (circular concentration).
* **Peak rate (Hz)** at the angle with maximum mean rate.
* Rate at PD (axis-1 peak angle) and at the opposite angle.
* RMSE vs the t0004 cosine target.

### Outputs

* **Library asset**: `bed_a_with_bio_realistic_ais` — Bed A + AIS + axon model variant with
  the {HHst, Nav1.6, Kv3, Kv7} channel set wired in. Reusable by future tasks that need a
  working DSGC + AIS substrate.
* **Stage 1 candidate table** (`results/baseline_candidates.csv`) with 6 rows showing
  soma_gnabar_HHst, peak Hz, DSI, in-band y/n.
* **Stage 2 per-axis sensitivity plots** (8 PNGs in `results/images/`): HWHM, vector-sum DSI,
  peak rate, RMSE vs cosine target, plotted against axis values.
* **Biologically-plausible AIS recommendation table**
  (`results/biological_ais_recommendation.md`): the band-constrained range for each axis (the
  values that keep the cell inside {DSI [0.3, 0.95], peak [5, 50] Hz}), plus a recommended
  canonical configuration.
* `results/metrics.json` with registered project metrics per condition.

## Approach

1. Fork t0069's AIS-attachment code into this task's `code/`. Replace the t0069
   channel-addition loop with the {HHst, Nav1.6, Kv3, Kv7} baseline channel set (with
   t0074-vendored Kv7).
2. Implement Stage 1 calibration as a 6-candidate sweep with explicit pass-band check and
   automated baseline selection.
3. Implement Stage 2 as 8 per-axis sweep functions sharing a common driver.
4. Run Stage 1, log selected baseline, run Stage 2.
5. Compute width metrics, generate per-axis plots, write the recommendation table.
6. Validate against t0069 sanity checks: trials with instability flags = 0, peak Vm bounded.

## Pass Criteria

* Stage 1 finds at least one in-band baseline (peak Hz in [5, 50] AND DSI in [0.3, 0.95]).
* All 1620 + 72 trials complete with no instability flags.
* Per-axis sensitivity plots show monotonic or unimodal sensitivity for at least 6 of the 8
  axes (the axes that don't are flagged as candidates for re-investigation; not a hard fail).
* Recommendation table produced with the band-constrained range for each axis.

## Compute Estimate

* ~2 h wall-clock on local CPU. 72 trials Stage 1 (~5 min) + 1620 trials Stage 2 (~100 min) +
  ~10 min plotting / metrics extraction.
* Local-CPU only. No remote machine. No paid API.

## Dependencies

* `t0008_port_modeldb_189347` — Bed A library.
* `t0067_t0065_soma_channel_addition_sweep` — channel-insertion code (Nav1.6, Kv3
  implementation patterns).
* `t0069_t0067_ais_localised_channel_sweep` — AIS attachment code; baseline characterisation
  of the passive-AIS sink effect.
* `t0074_channel_tuning_width_bed_a` — Kv7 MOD vendoring lands in t0074. This task inherits
  the vendored Kv7 mechanism and the calcium-pool unification (the latter is not actively used
  here but must remain compatible).

## Risks and Fallbacks

* **Stage 1 finds no in-band baseline**: the task halts after Stage 1 and reports a negative
  result with a follow-up recommendation. Time-cheap (~5 min). The follow-up would probably be
  a 2D Stage 1.5 sweep over {soma gnabar, AIS gnabar} or a baseline that further reduces AIS
  Nav1.6 density.
* **Stage 1 is over-fitted to soma_gnabar**: if the baseline soma_gnabar value is borderline
  (e.g., exactly at the edge of the in-band region), small parameter changes in Stage 2 may
  push the cell out of band rapidly. Mitigation: pick the Stage-1 baseline closest to the band
  centre, not the band edge.
* **Axes interact strongly**: the one-axis-at-a-time design assumes weak interactions. If a
  Stage-2 axis sweep produces non-monotonic behaviour (e.g., DSI rises then falls), report the
  non-monotonicity explicitly and flag the axis for a future joint sweep with one neighbouring
  axis.
* **AIS+axon discretisation artefacts**: if the segment count along the AIS or axon is too
  low, spike initiation and propagation may be artefactual. Mitigation: use NEURON's
  `lambda_f`-based segment-count rule (`d_lambda = 0.1` at 100 Hz) and validate that the
  chosen segment count doubles without changing peak Vm by more than 1 mV at the t0069
  baseline.

## Out of Scope

* Bed B (de Rosenroll) — explicitly out of scope per researcher decision; this task is Bed A
  only.
* Joint multi-axis optimisation — explicitly excluded; this is one-axis-at-a-time only.
* Other AIS channel candidates (Nav1.2, Kv1, Kv4 alpha-DTX-sensitive subtype) — out of scope;
  the channel set is fixed at {HHst, Nav1.6, Kv3, Kv7}. Future follow-ups may extend the
  channel set.

</details>

<details>
<summary>⏹ 0031 — <strong>Fetch paywalled morphology papers: Kim2014 and
Sivyer2013</strong></summary>

| Field | Value |
|---|---|
| **ID** | `t0031_fetch_paywalled_morphology_papers` |
| **Status** | not_started |
| **Effective date** | 2026-04-22 |
| **Dependencies** | — |
| **Expected assets** | 2 paper |
| **Source suggestion** | `S-0027-06` |
| **Task types** | [`download-paper`](../../../meta/task_types/download-paper/) |
| **Task page** | [Fetch paywalled morphology papers: Kim2014 and Sivyer2013](../../../overview/tasks/task_pages/t0031_fetch_paywalled_morphology_papers.md) |
| **Task folder** | [`t0031_fetch_paywalled_morphology_papers/`](../../../tasks/t0031_fetch_paywalled_morphology_papers/) |

# Fetch Paywalled Morphology Papers: Kim2014 and Sivyer2013

## Motivation

During t0027 (literature survey on computational modeling of cell morphology effects on
direction selectivity), two papers that met the inclusion criteria could not be retrieved
through the normal open-access and Sheffield institutional routes:

* **Kim et al. 2014** — flagged as intervention in t0027 when the direct download chain
  failed; the paper is relevant because it builds a compartmental model tying distal dendritic
  geometry to DS outcome.
* **Sivyer et al. 2013** — paywalled on J Physiol, Sheffield SSO did not recognise the DOI at
  the time; highly relevant because it grounds the dendritic-spike branch-independence
  mechanism that t0029 will discriminate against Dan2018 passive-TR.

A dedicated task with explicit intervention allowance (manual SSO retry, inter-library-loan,
or corresponding-author email) is the clean path to complete the literature coverage. Source
suggestion **S-0027-06** (medium priority).

## Scope

1. For each of the two papers, attempt retrieval in order: open-access via pdf_url → Sheffield
   institutional SSO → ResearchGate / author website → inter-library loan →
   corresponding-author email.
2. If one or more retrieval paths fail, create an intervention file documenting what was tried
   and what is still needed (human follow-up).
3. When a PDF is obtained, add the paper as a standard paper asset under
   `tasks/t0031_fetch_paywalled_morphology_papers/assets/paper/<paper_id>/` following
   `meta/asset_types/paper/specification.md` — `details.json` + canonical summary document +
   `files/<filename>.pdf`.
4. Summarise each paper with full detail per the spec (including all 9 mandatory sections in
   the summary).

## Approach

* Local Windows workstation. No remote compute, no paid API.
* The `/add-paper` skill (if present) handles the mechanical download + summary workflow.
  Otherwise follow the paper asset specification manually.
* If any PDF cannot be retrieved after all attempts, mark `download_status: "failed"` in
  `details.json` with a detailed `download_failure_reason`, and keep the metadata +
  abstract-only summary for searchability.

## Expected Outputs

* 2 paper assets under `assets/paper/<paper_id>/`, each with `details.json`, the canonical
  summary document, and `files/<filename>.pdf` (or a `.gitkeep` if retrieval failed).
* If any retrieval fails, an intervention file under `intervention/` documenting the failure.
* `results/results_summary.md` summarising what was retrieved and any remaining gaps.

## Compute and Budget

* Local only. No compute cost. No paid API. If ILL charges apply, ask researcher before
  proceeding (typically free via Sheffield).

## Measurement

* Binary outcome per paper: retrieved (PDF + summary) or failed (metadata + abstract-only
  summary + intervention file).

## Key Questions

1. Can both PDFs be retrieved via any combination of open-access / institutional / author
   routes?
2. If the full PDFs are obtained, does Sivyer2013 actually support the dendritic-spike branch-
   independence mechanism as the t0027 synthesis assumes, or does the paper make a more
   nuanced claim that changes the t0029 discriminator interpretation?

## Dependencies

None — this task runs independently of all sweeps and of t0023.

## Scientific Context

Source suggestion **S-0027-06** (medium priority). Closes the literature-coverage gap left by
t0027. Completing this coverage strengthens the interpretation of t0029 and t0030 sweep
results, especially for the Sivyer2013 mechanism which currently rests on the synthesis's
second-hand summary of that paper.

## Execution Notes

* Follow standard /execute-task flow.
* Include `planning` step (lightweight: which source to try first for each paper, how to
  handle failure).
* Skip `research-papers`, `research-internet`, `research-code` — this task IS the download
  work.
* Skip `setup-machines` / `teardown` (local only).
* Skip `compare-literature` (no quantitative results).
* Run paper asset verificator on each downloaded paper before committing.

</details>
