# Brainstorm Session 10 — Full Transcript

## Project State Presented

**Budget**: $1.00 total, $0.00 spent (all local CPU). No paid services in play.

**Tasks** (55 total): 48 completed, 1 in-progress (t0055), 2 not-started (t0031, t0045), 1
intervention-blocked (t0023), 3 cancelled (t0042/43/44).

**Suggestions backlog**: 187 uncovered (50 high, 111 medium, 26 low).

### What's been done since brainstorm 9 (t0051)

**t0052 — scalar gabaMOD (AMPA-only)**

* Primary DSI = 1.000, vector-sum DSI = 0.746, peak rate 0.667 Hz (1 spike/trial)
* Single-spike-per-trial regime → DSI = 1 trivially. HWHM 82.5°.
* Headline mechanistic finding: driving-force saturation — 1.54x somatic IPSP voltage from a 3.0x
  conductance ratio
* Peak rate 22-50x below t0004 target / in vivo (30-100 Hz)

**t0053 — spatial centripetal-only GABA (AMPA-only)** — *negative result*

* FULL-mode tuning curve identically 0 Hz across all 12 directions; primary DSI = 0
* Spatial mechanism mechanically correct (active fraction modulates 0.34 → 0.66) but 2 nS GABA x
  50% of 100 synapses = 100 nS mean total fully suppresses spiking
* AMPA-only fires bit-identically to t0052 (0.667 Hz) — confirms DSI collapse is purely an
  inhibition-amplitude calibration issue
* IPSP voltage modulation only 1.24x despite 1.94x active-count ratio — same saturation as t0052,
  hits ceiling sooner

**t0054 — AMPA + voltage-independent NMDA + scalar gabaMOD**

* gNMDA=0 regression-gate matches t0052 exactly (0e+00 Hz max diff)
* gNMDA=0.25 closes peak-rate gap (0.667 → 8.0 Hz) but DSI collapses 0.746 → 0.082 → 0.029 →
  0.017
* Confirms PolegPolsky2016 prediction: voltage-independent NMDA → additive gain → DSI loss
* EPSP doesn't decay within trial window — stacked NMDA keeps cell depolarised

**t0055 — Mg-block NMDA recovery test** — *in flight, started today*

* Replaces voltage-independent Exp2Syn NMDA with Jahr-Stevens Mg-block point process
* Tests directly whether voltage-dependent Mg-block restores DSI under gNMDA={0,0.25,0.5,1.0} sweep
* Source = S-0054-01

### Independent priority reassessment

After reading these results, my read on the 50 high-priority suggestions:

**Still high-priority and on critical path**:

* S-0053-01 — GABA conductance sweep on t0053 to recover non-zero tuning. Direct fix for t0053's
  negative result.
* S-0053-02 — stricter centripetal threshold (cos < -0.5 / -0.7) sweep. Halves active fraction.
* S-0053-03 — conductance-matched (1.32 nS) t0052 vs t0053 comparison — isolates
  graded-vs-binary mechanism distinction at matched mean GABA mass.
* S-0052-01 — AMPA per-synapse sweep on t0052 to escape single-spike regime / close peak-rate gap.
* S-0052-02 — GABA-synapse-count sweep on t0052 to characterise driving-force saturation.
* S-0054-02 — joint (gAMPA, gNMDA, gGABA) sweep on t0054 to find DSI-preserving operating point.
  **Should wait on t0055 results** — if Mg-block fixes it, the joint sweep moves to t0055
  architecture instead.

**Should be deprioritised — t0022/t0024 testbed lineage was de-emphasised in brainstorm 9**:

* S-0022-01, S-0022-02, S-0022-03 — Nav1.1/Nav1.6/E-I sweeps on the t0022 testbed. The
  from-scratch wave supersedes this.
* S-0026-02, S-0026-06 — t0024 V_rest x rho x NMDA-block sweeps. Old lineage.
* S-0034-01, S-0034-02, S-0034-07 — t0034 length-diameter follow-ups.
* S-0035-02, S-0039-01 — t0024 surface-density / passive-vs-active diameter retest.

**Already covered / superseded — recommend reject**:

* S-0015-04 — "build minimal DSGC implementing 6-point spec". This is exactly what t0052 does.
* S-0016-03 — "experimentally test NMDA-spike contribution to DSGC DS". t0054 + t0055 cover this
  end-to-end.
* S-0017-03 — "implement AIS, NMDARs, voltage-clamp block in DSGC model". AIS + NMDA done in
  t0052/t0054. Voltage-clamp block was a t0049 target, already addressed.
* S-0018-03 — "AMPA + NMDA + GABA_A with E-I temporal co-tuning + asymmetric inhibition". The
  AMPA+NMDA+GABA part is t0054; spatial asymmetric inhibition is t0053. Only the temporal co-tuning
  piece is missing — better to write a new, focused suggestion than keep this stale one.
* S-0033-02, S-0033-03, S-0033-06 — t0033 optimiser prerequisites. The optimiser stays deferred
  per brainstorm 9 until from-scratch substrate is mature.
* S-0048-01 — GABA scan at Voff_bipNMDA=1 on the deposited DSGC. The deposited DSGC line was
  retired.

**Library / tooling — keep but no urgency**:

* S-0012-01 (verify_library_asset.py framework verificator) — t0052's ad-hoc verificator could
  become canonical. Medium.
* S-0013-01, S-0013-02 — DOI-resolution helper / verificator. Medium.
* S-0010-05 (headless-port scaffold) — nice-to-have. Medium.

**Paywalled-paper retrieval (S-0015-01, S-0016-01, S-0017-01, S-0018-01, S-0019-01)** — five
high-priority suggestions all asking to retrieve paywalled PDFs via Sheffield access. These are
bundled into the existing not_started t0031 task. Recommend dropping all five to medium — t0031
covers them institutionally.

**Unmodified — research questions Q1 (Na/K combinations) and Q4 (active dendrites) still untouched
in the from-scratch wave**:

* S-0002-01 (factorial g_Na x g_K grid search) — Q1 is the project's first stated research
  question and has NOT been executed in the from-scratch wave. Hot candidate.
* S-0009-03 — calibrate Nav/Kv/Ih to match Poleg-Polsky spike shape and distal Ih sag. Useful for
  active-dendrite track.
* S-0002-04 (factorial morphology sweep) — Q2; not yet done.

## Clarification Questions

AI: Before proposing tasks, a few questions:

1. Notes / context to guide this session? Anything strategic on your mind that I should fold in?
2. t0055 dependency — t0055 just started. Should I plan tasks that explicitly chain off its result
   (and only kick off after merge), or treat t0055 as a black box and plan independent next steps in
   parallel?
3. Scope appetite — looking to commission a tight 2-3 task wave, or a broader batch of 5-8?
4. Active dendrites and Na/K (Q1, Q4) — these are core project research questions and the
   from-scratch wave hasn't touched them yet. Should we open one of those tracks now, or stay on the
   AMPA/NMDA/GABA balance work that's currently in flight?
5. Anything from the t0052-t0054 results that surprised you or shifted your thinking?

Researcher: S-0053-01 sounds interesting. One think I noticed that it only acts between 100 and 200
milliseconds. Why is that? It needs to be longer so that it stops spiking after 200 ms which
currently doesn't happen.

## Diagnosis

AI: Confirmed — that's a real issue baked into both t0052 and t0053.

In `t0053/code/synapses.py:170-181` (and t0052 identical), each GABA synapse fires exactly once at:

```
t_onset = (x*cos(theta) + y*sin(theta)) / velocity + 100 ms
```

With bar speed = 1 um/ms sweeping a dendritic field roughly ±100 um wide, the spread of onset times
across the 100 GABA synapses is ~100-200 ms wide centred on the BASE_OFFSET (100 ms).

GABA Exp2Syn decay (`GABA_TAU2_MS = 20 ms`) means each event is essentially gone within ~100 ms.
After the last synapse fires (~250-300 ms in trial time) and another ~100 ms of decay, the cell is
uninhibited for the remaining ~1100 ms of the 1500 ms trial. Anything that fires after ~350 ms gets
no GABA help.

This is biologically wrong: real SAC→DSGC IPSCs envelope over 100-300 ms via multiple GABA release
events per varicosity during the stimulus passage (per the t0017/t0018 answers). The single Exp2Syn
event is a simplification that loses the sustained component.

### Three ways to fix

**Option A — lengthen `GABA_TAU2_MS`** (tau2 = 20 → 50-100 ms). One-line change. Stretches each
event's tail to better match biological IPSC duration. Downside: still a single event, not
biologically faithful.

**Option B — multiple events per synapse** (`NetStim.number > 1`, e.g. 5-10 events at 5-10 ms
intervals during the bar dwell). Models the SAC's ~5-10 spikes during stimulus passage. Most
biologically realistic; introduces a realistic sustained envelope. Downside: more parameters to set
(number, interval).

**Option C — tonic GABA gated by stimulus window** (replace Exp2Syn with a sustained conductance
turned on at first synapse onset, off N ms after the last). Simplest "always-on during stimulus"
model; least biological.

### Same-issue scope

This affects t0052, t0053, t0054. t0055 (in flight, Mg-block NMDA test) inherits t0054's GABA timing
— so if we fix it, t0055 will likely want to be re-run on the new architecture once it lands.

### Proposed task shape

I'd combine the timing fix with S-0053-01's amplitude sweep into one task on t0053, since the
optimal amplitude depends on the timing window. Something like:

> t00XX — GABA timing + amplitude rescue on t0053 spatial DSGC. Fix GABA active-window collapse
> (currently ~100-300 ms), then sweep peak conductance to find the operating point that produces
> non-zero FULL-mode tuning curves. Specifically: change [Option A/B/C], then sweep
> `GABA_BASE_NS in {0.5, 1.0, 1.5, 2.0}` and report DSI, peak Hz, HWHM, and the GABA active-window
> duration per direction.

A few questions:

1. Which option (A/B/C) do you prefer?
2. Should the timing fix also propagate back to t0052 (a parallel task), or just land on t0053 first
   and let t0052 follow if t0053 results are interesting?
3. About t0055 — it's in flight using t0054's GABA timing. Let it complete as-is (results are
   still informative for the Mg-block question), or should we cancel/restart it after the timing
   fix?
4. Anything else from t0052-t0054 traces you want me to design a fix for in parallel?

Researcher: Option C. 2. just t0053 3. Complete as is. 4. No But implements the suggestion 0053-01

## Discussion — Round 1: New Tasks (Recap)

AI: t0057 — Tonic GABA + amplitude sweep on t0053 spatial DSGC (covers S-0053-01).

Replace per-event Exp2Syn GABA with a tonic conductance gated by stimulus window, then sweep the
per-synapse peak conductance to find the operating point that produces non-zero FULL-mode tuning
curves. The new mechanism preserves t0053's spatial centripetal-gating rule (only synapses with
`cos(theta_stim - theta_centrifugal) < 0` are active) but holds the conductance constant over the
trial window instead of decaying with τ₂ = 20 ms.

**Implementation**

* Add a small NEURON MOD point process `gaba_tonic.mod` exposing `(g, e, t_on, t_off)` — sustained
  conductance `g` between `t_on` and `t_off`, zero elsewhere; reversal `e = -75 mV`.
* Per-synapse: gated synapses get `g = GABA_BASE_NS` and `t_on = 100 ms`, `t_off = 1400 ms` (full
  trial window minus the 100 ms BASE_OFFSET buffer); silent synapses get `g = 0`.
* Same morphology (`dsgc-baseline-morphology-calibrated`), same E synapses, same fixed placement
  seed as t0053 — only the GABA mechanism changes. Bit-identical AMPA path verified by
  `test_placement_seed0_match.py`-style fixture.

**Sweep**

* `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS — five values. 12 directions x 10 trials x 3
  modes (FULL / AMPA_ONLY / GABA_ONLY) x 5 conductances = 1800 trials. Estimated ~25-30 min on local
  CPU per the t0052/t0053 wall-clock.

**Reports**

* Primary + vector-sum DSI vs `GABA_BASE_NS`
* Peak Hz, null Hz, HWHM per conductance
* IPSP voltage envelope per direction (the new headline observable — should now span the full
  trial, not collapse at 200 ms)
* Active-fraction curve (carried over from t0053; should be unchanged at 0.34-0.66)
* RMSE vs t0004 target curve

**Dependencies**: `t0053_minimal_dsgc_spatial_gaba`, `t0009_calibrate_dendritic_diameters`,
`t0011_response_visualization_library`, `t0012_tuning_curve_scoring_loss_library`. Local CPU. $0.

**Source suggestion**: S-0053-01 (covered).

## Discussion — Round 2: Suggestion Cleanup

AI: Per Phase 1 reassessment, recommended:

**Reject as covered/superseded** (4 high-priority): S-0015-04, S-0016-03, S-0017-03, S-0018-03.

**Reprioritise to medium** (19 high-priority): t0022 testbed (S-0022-01, S-0022-02, S-0022-03);
t0024 testbed follow-ups (S-0026-02, S-0026-06, S-0034-01, S-0034-02, S-0034-07, S-0035-02,
S-0039-01); t0033 optimiser prerequisites (S-0033-02, S-0033-03, S-0033-06); paywalled-paper
retrievals (S-0015-01, S-0016-01, S-0017-01, S-0018-01, S-0019-01); retired deposited-DSGC line
(S-0048-01).

**Keep at high priority** the from-scratch wave's natural next steps not covered by t0057:
S-0052-01, S-0052-02, S-0052-04, S-0053-02, S-0053-03, S-0054-02, S-0002-01.

### Questions before Round 3

1. Suggestion cleanup — agree with the 4 rejections and 19 reprioritisations?
2. Anything to add to t0057 — confirm the sweep values `{0.25, 0.5, 1.0, 1.5, 2.0}` nS are right,
   or want a finer grid? Confirm `t_on = 100 ms`, `t_off = 1400 ms` window?
3. Source suggestion — just S-0053-01, or should I also mark S-0053-02 (centripetal threshold
   sweep) as covered since the tonic-GABA fix may make threshold tuning unnecessary?

Researcher: 1. agree 2. confirm all 3. just s0053-1

## Discussion — Round 3: Confirmation

AI: Final decisions to apply, in order:

### Brainstorm task

* t0056_brainstorm_results_10 — this brainstorm session itself.

### New task (created after the brainstorm task lands)

* t0057_tonic_gaba_sweep_t0053 — Tonic GABA + amplitude sweep on t0053 spatial DSGC
  * Replace Exp2Syn GABA with `gaba_tonic.mod` point process (sustained `g` between `t_on=100 ms`
    and `t_off=1400 ms`)
  * Sweep `GABA_BASE_NS in {0.25, 0.5, 1.0, 1.5, 2.0}` nS
  * Dependencies: t0053, t0009, t0011, t0012
  * Source: S-0053-01 (covered)
  * Local CPU, $0

### Suggestions: reject (4)

| ID | Reason |
| --- | --- |
| S-0015-04 | Covered by t0052 (minimal DSGC implementing 6-point spec) |
| S-0016-03 | Covered by t0054 + t0055 (NMDA-spike DS contribution test) |
| S-0017-03 | AIS+NMDA done in t0052/t0054, voltage-clamp block in t0049 |
| S-0018-03 | AMPA+NMDA+GABA done in t0053+t0054; temporal co-tuning belongs in a fresh suggestion |

### Suggestions: reprioritise high → medium (19)

| Group | IDs |
| --- | --- |
| t0022 testbed | S-0022-01, S-0022-02, S-0022-03 |
| t0024 testbed follow-ups | S-0026-02, S-0026-06, S-0034-01, S-0034-02, S-0034-07, S-0035-02, S-0039-01 |
| t0033 optimiser prerequisites | S-0033-02, S-0033-03, S-0033-06 |
| Paywalled-paper retrievals (bundled into t0031) | S-0015-01, S-0016-01, S-0017-01, S-0018-01, S-0019-01 |
| Retired deposited-DSGC line | S-0048-01 |

### Tasks: cancel / update — none

### New suggestions — none

**Totals**: 1 new task, 4 rejections, 19 reprioritisations, 23 correction files.

**Please confirm with an explicit "go" or "approved"** so I can apply Phases 3-6 without further
prompting.

Researcher: approved.

## Decisions Summary

1. Create t0057 (`tonic_gaba_sweep_t0053`) covering S-0053-01.
2. Reject S-0015-04, S-0016-03, S-0017-03, S-0018-03 as covered.
3. Reprioritise to medium: S-0022-01/02/03, S-0026-02/06, S-0034-01/02/07, S-0035-02, S-0039-01,
   S-0033-02/03/06, S-0015-01, S-0016-01, S-0017-01, S-0018-01, S-0019-01, S-0048-01.
4. No tasks cancelled or updated.
5. No new suggestions produced.
6. Let t0055 complete as-is on existing GABA timing.
7. Apply Phases 3-6 without further confirmation.
