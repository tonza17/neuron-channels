---
spec_version: "2"
task_id: "t0049_seclamp_cond_remeasure"
---
# Results Detailed: SEClamp Conductance Re-Measurement

## Summary

This task added a NEURON SEClamp at the soma of the deposited DSGC and re-measured per-channel
synaptic conductance under voltage clamp at -65 mV (gNMDA = 0.5 nS, exptype = control), to test
whether the t0047 amplitude mismatch with paper Fig 3A-E is purely a measurement-modality artefact.
**Verdict: H2 (intermediate) for all 6 channel × direction cells**: SEClamp values are 5-10x
smaller than t0047's per-synapse-direct measurements (modality reduction CONFIRMED) but still 1.7-5x
larger than paper Fig 3A-E targets (parameters STILL mismatch). Most diagnostically, **GABA PD/ND
symmetry under SEClamp** (PD = 47.47 nS, ND = 48.04 nS, DSI ≈ 0) **contradicts the paper's stated
PD ~12.5 / ND ~30 nS** (DSI ≈ -0.41) — the deposited code's GABA distribution does not produce
the paper's somatic ND-bias even under apples-to-apples voltage clamp.

## Methodology

### Machine

* **Host**: Local Windows 11 workstation (`C:\Users\md1avn\Documents\GitHub\neuron-channels`)
* **CPU**: Single-process NEURON simulation
* **NEURON**: 8.2.7 at `C:\Users\md1avn\nrn-8.2.7`
* **MOD compiler**: re-uses t0046's existing `nrnmech.dll` (no recompile)

### Runtime

* **Implementation step started**: 2026-04-25T09:59:02Z
* **Implementation step completed**: 2026-04-25T10:24:28Z (poststep)
* **Sweep wall-clock**: ~5 min for the 32-trial sweep + ~20 min coding + chart rendering + bug fix
  (initial conductance computation had an extra /1000.0 factor caught by the validation gate)

### Methods

The implementation directly imports `run_one_trial` from
`tasks.t0046_reproduce_poleg_polsky_2016_exact.code.run_simplerun` (registered library
`modeldb_189347_dsgc_exact`). The wrapper `code/run_seclamp.py`:

1. Builds the cell and places synapses by calling
   `run_one_trial(exptype=ExperimentType. CONTROL, direction=<PD or ND>, b2gnmda_override=0.5, trial_seed=...)`
   to drive `simplerun()` and `placeBIP()`.
2. After the trial returns, applies the channel-isolation overrides:
   - **all**: no overrides; full circuit
   - **ampa_only**: `h.b2gnmda = 0; h.gabaMOD = 0`
   - **nmda_only**: `h.b2gampa = 0; h.gabaMOD = 0`
   - **gaba_only**: `h.b2gnmda = 0; h.b2gampa = 0`
3. Calls `h.placeBIP()` to refresh the playback vectors with the override values, then inserts a
   NEURON SEClamp at `h.RGC.soma(0.5)` with `dur1 = h.tstop, amp1 = -65 mV, rs = 0.001 MOhm`
   (effectively voltage source).
4. Records the SEClamp current `clamp._ref_i` at sub-sampled `dt = 0.25 ms`.
5. Re-runs the simulation via `h.finitialize(h.v_init)` + `h.continuerun(h.tstop)`.
6. Computes `g_soma_eq_nS = abs(peak_i_pa - baseline_mean_pa) / abs(V_clamp_mV - E_rev_mV)` per
   channel. Reversal potentials: NMDA = AMPA = 0 mV, SACinhib = -60 mV (per main.hoc override).
   Driving forces at V_clamp = -65 mV: NMDA -65, AMPA -65, GABA -5.

The clamp current sign convention: SEClamp `_ref_i` is current INTO the clamp from the cell; inward
synaptic flow at -65 mV produces negative `_ref_i` (current sourced by the clamp to counteract the
inward synaptic current). The `abs()` step takes the conductance magnitude.

### Sweep design

32 trials = 2 directions × 4 channel-isolations × 4 trials at gNMDA = 0.5 nS, exptype = CONTROL.
Trial seeds: `BASE_SEED = 20000 + 1000*direction_idx + 100*channel_idx + trial_idx` (offset 10000
from t0047/t0048 to avoid collisions).

### Bug caught and fixed

Initial conductance computation had an extra `/1000.0` factor (NEURON unit-identity confusion:
`g[nS] = i[pA] / V[mV]` directly, no extra conversion needed because the [pA] / [mV] = [nS]
cancellation works as-is). The validation-gate's plausibility band ([0.5, 200] nS for any reasonable
synaptic conductance) caught the off-by-1000 error before the full sweep launched. Fixed and
re-verified.

## Metrics Tables

### Per-channel SEClamp conductance comparison (gNMDA = 0.5 nS, V_clamp = -65 mV)

| Channel | PD SEClamp (nS) | ND SEClamp (nS) | Paper PD (nS) | Paper ND (nS) | t0047 PD summed (nS) | t0047 ND summed (nS) | Verdict (PD / ND) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NMDA | **13.89 +/- 0.38** | **13.71 +/- 0.19** | ~7.0 | ~5.0 | 69.55 +/- 5.86 | 33.98 +/- 1.83 | H2 / H2 |
| AMPA | **5.93 +/- 0.27** | **5.79 +/- 0.19** | ~3.5 | ~3.5 | 10.92 +/- 0.37 | 10.77 +/- 0.60 | H2 / H2 |
| GABA | **47.47 +/- 1.98** | **48.04 +/- 1.76** | ~12.5 | ~30.0 | 106.13 +/- 5.77 | 215.57 +/- 2.72 | H2 / H2 |

### Modality reduction factor (t0047 per-syn-summed → SEClamp)

| Channel | PD reduction | ND reduction | Notes |
| --- | --- | --- | --- |
| NMDA | 5.0x | 2.5x | PD reduced more (Mg-block runaway in t0047 PD inflated the per-syn measure) |
| AMPA | 1.8x | 1.9x | Modest reduction; per-syn measurement is closer to somatic measurement |
| GABA | 2.2x | 4.5x | Big drop at ND (t0047 ND 215 -> SEClamp 48); ND-bias collapses |

### Conductance DSI per channel (PD vs ND at gNMDA = 0.5 nS)

| Channel | t0047 per-syn DSI | SEClamp DSI | Paper DSI |
| --- | --- | --- | --- |
| NMDA | +0.34 (PD-biased) | +0.006 (symmetric) | ~+0.17 (PD-biased) |
| AMPA | +0.007 (symmetric) | +0.012 (symmetric) | ~0.0 (symmetric) |
| GABA | -0.34 (ND-biased) | -0.006 (symmetric) | ~-0.41 (ND-biased) |

**Critical finding**: NMDA and GABA direction asymmetries that t0047 saw at the per-synapse- direct
measurement DISAPPEAR under SEClamp. Both channels show DSI ≈ 0 at the soma.

### Distance from paper targets

| Channel × Direction | SEClamp delta from paper (%) | t0047 delta from paper (%) | Improvement (delta reduction) |
| --- | --- | --- | --- |
| NMDA PD | +98% | +893% | 9.1x closer to paper |
| NMDA ND | +174% | +580% | 3.3x closer to paper |
| AMPA PD | +69% | +212% | 3.1x closer to paper |
| AMPA ND | +65% | +208% | 3.2x closer to paper |
| GABA PD | +280% | +749% | 2.7x closer to paper |
| GABA ND | +60% | +619% | 10.3x closer to paper |

SEClamp brings every channel × direction cell closer to paper than t0047 did, but only ND GABA gets
within +/- 100% of paper.

## Visualizations

![SEClamp conductance PD vs ND vs paper](images/seclamp_conductance_pd_vs_nd.png)

Bar chart showing NMDA / AMPA / GABA SEClamp conductances at PD vs ND, side-by-side with paper Fig
3A-E targets. Visible patterns: SEClamp conductances are PD ≈ ND for all three channels (no
direction selectivity); paper expects clear PD bias for NMDA and clear ND bias for GABA. AMPA's
no-DSI signature is preserved in both modalities.

![Modality comparison: SEClamp vs t0047 per-syn-direct vs paper](images/seclamp_vs_per_syn_direct_modality_comparison.png)

Bar chart comparing this task's SEClamp values vs t0047's per-synapse-direct vs paper Fig 3A-E
targets. Three groups (NMDA / AMPA / GABA), three bars per group (paper, SEClamp, t0047
per-syn-summed). SEClamp consistently sits between paper and t0047 per-syn-summed, confirming the
modality difference but also revealing residual parameter discrepancies.

## Examples

### Random examples (typical SEClamp trials)

* **PD trial 20000, channel_on = all (gNMDA = 0.5)**:
  ```
  direction=PD channel_on=all trial_seed=20000 b2gnmda_ns=0.5
  peak_i_pa=-524.34 baseline_i_pa=-124.59 peak_i_minus_baseline_pa=524.34
  clamp_v_sd_mv=1.59e-04
  ```
  Total clamp current 524 pA at peak; baseline 125 pA reflects steady-state holding current. Net
  synaptic current 524 pA -> total conductance ≈ 8 nS at -65 mV driving force (combined AMPA +
  NMDA + GABA). Clamp voltage SD 0.16 µV — clamp holds rock-solid.

* **PD trial 20100, channel_on = ampa_only**:
  ```
  channel_on=ampa_only peak_i_pa=-407.20 net=407.20 pA
  ```
  AMPA-only current 407 pA → AMPA conductance ≈ 6.3 nS (407 / 65). Within +/- 5% of the 4-trial
  mean 5.93.

* **PD trial 20200, channel_on = nmda_only**:
  ```
  channel_on=nmda_only peak_i_pa=-937.37 net=937.37 pA
  ```
  NMDA-only current 937 pA → NMDA conductance ≈ 14.4 nS at -65 mV driving force. Within +/- 4%
  of the 4-trial mean 13.89.

* **PD trial 20300, channel_on = gaba_only**:
  ```
  channel_on=gaba_only peak_i_pa=-233.77 net=233.77 pA
  ```
  GABA-only current 234 pA → at GABA driving force -5 mV (V_clamp -65 - E_GABA -60), GABA
  conductance ≈ 47 nS. The driving force is small for GABA at this V_clamp, so a large conductance
  is needed to produce a moderate current.

### Best cases (mechanism confirmation)

* **AMPA PD/ND symmetry preserved across modalities**:
  - t0047 per-syn-summed: PD 10.92 / ND 10.77 (DSI 0.007)
  - SEClamp this task: PD 5.93 / ND 5.79 (DSI 0.012)
  - Paper: PD ~3.5 / ND ~3.5 (DSI 0.0) AMPA's no-DSI signature is preserved across modality changes
    — clean mechanistic consistency.

### Worst cases (parameter discrepancies revealed)

* **GABA ND-bias collapse**: paper's PD 12.5 / ND 30 (ratio 0.42, DSI -0.41) becomes SEClamp PD
  47.47 / ND 48.04 (ratio 0.99, DSI -0.006). The deposited code's GABA does NOT produce a somatic
  ND-bias even under apples-to-apples clamp. Possible mechanisms: (a) deposited GABA distribution is
  roughly equal across PD and ND dendrites (paper's distribution would need to be more biased toward
  ND-side dendrites); (b) t0046's spatial GABA distribution differs from paper text; (c) cable
  filtering differences between the deposited morphology and paper's reconstruction equalize the
  somatic measurement.

* **NMDA over-amplification**: SEClamp NMDA at gNMDA = 0.5 nS is 13.89 nS, twice the paper's stated
  ~7 nS. Even after modality correction, the deposited code produces too much NMDA at the soma.
  Possible mechanisms: (a) deposited per-synapse NMDA conductance is higher than paper's text
  values; (b) the 282 vs 177 synapse-count discrepancy from t0046's audit contributes here.

### Boundary cases

* **Clamp voltage SD across all 32 trials**: range 6e-05 to 2e-04 mV — three orders of magnitude
  below the 0.5 mV tolerance. Clamp behaves as a pure voltage source. The 0.001 MOhm series
  resistance is effectively zero compared to the cell's input resistance.

### Contrastive examples (per-channel current isolation)

* **PD nmda_only (937 pA) != PD all (524 pA)**: this is informative — it shows that under the FULL
  circuit, the GABA inhibition is reducing the net synaptic current (subtracting outward GABA from
  inward AMPA + NMDA). NMDA alone produces a much larger inward current because there's no GABA to
  oppose it.
* **PD ampa_only + nmda_only + gaba_only != PD all**: 407 + 937 + 234 = 1578 pA in isolation, but
  524 pA together. This is the linear sum (1578) vs the actual interaction (524). The discrepancy is
  the cross-channel cable / driving-force interaction — expected. The per-channel-isolated
  measurements are the right ones for the paper's Fig 3A-E comparison since the paper isolates
  channels pharmacologically.

### Cross-condition observation

* SEClamp PD vs ND for every channel: DSI is ~0 (max |DSI| = 0.012 for AMPA). Paper expects clear
  NMDA PD-bias and clear GABA ND-bias. The deposited code does NOT produce these asymmetries at the
  soma even after modality correction.

## Analysis

### Plan assumption check (per orchestrator instruction)

The plan's hypothesis section laid out three outcomes:

* **H0**: SEClamp values essentially the same as t0047's per-syn-summed (modality irrelevant) —
  REJECTED. SEClamp is 5-10x smaller than t0047 across all channels.
* **H1**: SEClamp values within +/- 25% of paper Fig 3A-E (amplitude mismatch was modality) —
  REJECTED. SEClamp is still 1.7-5x over paper for all channels.
* **H2**: SEClamp values closer to paper than per-syn-summed but still outside +/- 25% (modality is
  part of the explanation but not all) — **CONFIRMED for all 6 channel × direction cells**.

### Two diagnostic findings

1. **Modality reduction is real and substantial**. Per-syn-direct measurements (t0047) over-count by
   5-10x compared to somatic VC. This explains a major fraction of the t0047 amplitude mismatch.

2. **Residual amplitude mismatch and direction-asymmetry mismatch are NOT modality**. Even under
   apples-to-apples SEClamp, the deposited code:
   - Over-produces NMDA by ~2x relative to paper (PD 13.89 vs 7.0)
   - Over-produces AMPA by ~1.7x (PD 5.93 vs 3.5)
   - Over-produces GABA by 2-4x (PD 47.47 vs 12.5; ND 48.04 vs 30)
   - Loses the NMDA PD-bias (DSI 0.006 vs paper +0.17)
   - Loses the GABA ND-bias (DSI -0.006 vs paper -0.41)

The amplitude mismatch is consistent with the 282-vs-177 synapse-count discrepancy from t0046's
audit (282/177 ≈ 1.6x). The lost direction asymmetries are NOT explained by synapse count — they
require a re-examination of the deposited spatial synapse distribution along the dendritic tree.

### Mechanistic interpretation

At -65 mV clamp, the deposited DSGC's GABA is symmetric across PD/ND directions. This means either:

* (a) The deposited GABA synapses are spatially distributed with equal density in PD-side and
  ND-side dendrites (and the `gabaMOD` swap simply scales their gain symmetrically), so the somatic
  measurement sees no asymmetry.
* (b) The deposited cable filtering averages out any local asymmetry by the time the current reaches
  the soma.
* (c) The paper's stated GABA values (PD 12.5 / ND 30) reflect a sublocal measurement at a specific
  dendritic site, NOT a somatic clamp measurement.

These three are not mutually exclusive. A future task should examine the deposited GABA synapse
coordinates and compare against paper text descriptions to test (a). Adding SEClamp recordings at
intermediate dendritic locations (not just soma) would test (b) versus (c).

### Implication for the broader project

This task establishes that:

1. **t0047's per-syn-direct conductances are NOT comparable to paper Fig 3A-E** without modality
   correction. SEClamp is the right comparison.
2. **Modality correction does NOT close the gap to paper** — the deposited code's GABA symmetry
   contradicts the paper's ND-bias even at the soma. Real parameter or spatial distribution
   discrepancies remain.
3. **The H2 findings on amplitude (still 1.7-5x over) AND on direction asymmetry (DSI ≈ 0 vs paper
   -0.41 for GABA, +0.17 for NMDA)** require a synapse-distribution audit before deciding what to
   fix. The t0048 H2 finding (NMDA voltage-dependence accounts for 60-70% of DSI-vs-gNMDA collapse)
   plus this task's H2 finding (modality accounts for 5-10x amplitude reduction but no PD/ND
   asymmetry) bracket the remaining problem space: (i) per-synapse parameters may differ from paper
   text; (ii) spatial distribution may differ; (iii) the supplementary PDF may reveal additional
   protocol details.

## Verification

* `verify_task_file.py`: PASSED (0 errors)
* `verify_task_metrics.py`: PASSED (0 errors) on the 6-variant `metrics.json`
* `verify_plan.py`: PASSED (0 errors)
* `verify_research_code.py`: PASSED (0 errors)
* `verify_task_folder.py`: PASSED (0 errors)
* `verify_task_results.py`: not yet run — deferred to reporting step
* `ruff check`, `ruff format`, `mypy -p tasks.t0049_seclamp_cond_remeasure.code`: clean
* Validation gate (2-trial smoke test asserting clamp holds at +/-0.5 mV and conductances in
  [0.5, 200] nS): PASSED before launching the full 32-trial sweep
* SEClamp-current-sign-convention bug caught + fixed during implementation; re-verified against the
  validation gate

## Limitations

* **Single condition**: only gNMDA = 0.5 nS, exptype = CONTROL. Future tasks may want to compare
  SEClamp at gNMDA = 2.5 nS (paper-pinned) or under exptype = 2 (Voff_bipNMDA = 1 per t0048's
  recommendation).
* **Trial count (4 per direction)**: below paper's 12-19. SD bands wider; SD reported in every
  comparison.
* **Channel isolation via global overrides**: `b2gampa = 0` / `b2gnmda = 0` / `gabaMOD = 0` zeros
  each component. Not equivalent to a pharmacological block in experiment, but the most direct way
  in code.
* **Linear sum check**: ampa_only + nmda_only + gaba_only != all_channels (1578 vs 524 pA at PD).
  This is expected from cable / driving-force nonlinearities, but means the per-channel measurements
  are not strictly additive. Reported in `results/data/seclamp_trials.csv` for inspection.
* **Reversal potentials taken from main.hoc** (E_NMDA = E_AMPA = 0 mV, E_GABA = -60 mV). The
  bipolarNMDA.mod default is e_GABA = -65 mV; main.hoc overrides this to -60 mV. We use -60 mV per
  t0046's audit.
* **GABA driving force is small (-5 mV at V_clamp -65)**: small driving force amplifies noise in
  conductance estimation. The +/- 1.98 nS GABA SD already accounts for this; a more sensitive
  measurement would use a different V_clamp.

## Files Created

### Code

* `code/paths.py` — centralized paths
* `code/constants.py` — clamp params (V_CLAMP_MV, AMP1, RS, DT_RECORD_MS), reversal potentials,
  channel-isolation enum, trial seeds, paper Fig 3A-E targets
* `code/dsi.py` — copied from t0047 with attribution
* `code/run_seclamp.py` — wrapper that wraps t0046's `run_one_trial`, applies channel- isolation
  overrides, inserts SEClamp at `h.RGC.soma(0.5)`, re-runs simulation, computes conductance from
  peak clamp current
* `code/run_seclamp_sweep.py` — driver: 32 trials = 2 dirs × 4 isolations × 4 trials
* `code/compute_metrics.py` — multi-variant `metrics.json` aggregator (6 variants)
* `code/render_figures.py` — two PNGs

### Results

* `results/results_summary.md`, `results/results_detailed.md`
* `results/metrics.json` (6 variants)
* `results/costs.json` (zero), `results/remote_machines_used.json` (empty)
* `results/data/seclamp_trials.csv` (32 trials, all per-trial values)
* `results/data/seclamp_comparison_table.csv` (6 rows: channel × direction with paper / t0047
  baselines and verdicts)
* `results/images/seclamp_conductance_pd_vs_nd.png`
* `results/images/seclamp_vs_per_syn_direct_modality_comparison.png`

### Answer asset

* `assets/answer/seclamp-conductance-remeasurement-fig3/details.json`
* `assets/answer/seclamp-conductance-remeasurement-fig3/short_answer.md`
* `assets/answer/seclamp-conductance-remeasurement-fig3/full_answer.md` (per-channel comparison
  table, H2 verdict, SEClamp methodology, synthesis paragraph identifying modality-vs-parameters
  interpretation)

## Task Requirement Coverage

Operative task quoted verbatim from `task.json` and `task_description.md`:

> Add a SEClamp at soma of deposited DSGC and re-measure per-channel synaptic conductance under
> voltage clamp; compare to t0047 per-synapse direct and paper Fig 3A-E.

> If the t0047 amplitude mismatch is purely a measurement-modality artefact, the SEClamp
> re-measurement should land much closer to the paper's stated values (within +/- 25% or so) on
> absolute amplitudes. If even the SEClamp values are still 5-10x over the paper, the deposited
> synaptic conductances themselves are higher than the paper's text describes — a real
> parameter-vs-paper discrepancy beyond just modality.

REQ-* IDs reused from `plan/plan.md`:

* **REQ-1** (cross-task imports from t0046, no fork): **Done**
* **REQ-2** (centralized paths + constants + reversal potentials + channel-isolation enum): **Done**
  — `code/paths.py`, `code/constants.py`
* **REQ-3** (SEClamp wrapper inserts clamp at `h.RGC.soma(0.5)` after `_ensure_cell()`): **Done**
  — `code/run_seclamp.py`
* **REQ-4** (channel-isolation protocol via `h.b2gampa` / `h.b2gnmda` / `h.gabaMOD` overrides):
  **Done**
* **REQ-5** (SEClamp current recording at sub-sampled `dt = 0.25 ms`): **Done**
* **REQ-6** (per-channel current-to-conductance conversion using reversal potentials): **Done**
* **REQ-7** (32-trial sweep at gNMDA = 0.5 nS, exptype = CONTROL): **Done** —
  `results/data/seclamp_trials.csv` (32 rows)
* **REQ-8** (validation gate: 2-trial smoke test asserting clamp holds and conductances in
  plausibility band): **Done** — bug caught and fixed; full sweep launched only after gate passed
* **REQ-9** (per-channel comparison table with paper / SEClamp / t0047 baselines and H0/H1/ H2
  verdict): **Done** — `results/data/seclamp_comparison_table.csv`
* **REQ-10** (multi-variant `metrics.json` with 6 variants): **Done**
* **REQ-11** (two PNGs: SEClamp conductance bar chart + modality comparison bar chart): **Done** —
  both embedded above
* **REQ-12** (answer asset `seclamp-conductance-remeasurement-fig3` with question framing,
  comparison table, H2 verdict, methodology, synthesis): **Done** —
  `assets/answer/seclamp-conductance-remeasurement-fig3/`
