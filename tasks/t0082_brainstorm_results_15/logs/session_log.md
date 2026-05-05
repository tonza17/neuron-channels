# Brainstorm Session 15 -- Full Transcript

## Project State Presented

Headline: t0081 (`bedb_v3_warmstart_nsga2`) delivered the **project's first joint-pass cell** at gen
7 cell 767 (DSI 0.494 / PD 11.39 Hz on a 16-cell Pareto front, 768 evaluations, $2.39 on Vast.ai).
Pass criterion `DSI >= 0.4 AND PD >= 10 Hz` satisfied simultaneously for the first time in the
project lineage; decisively answers research question Q4 (do active dendritic conductances enable
joint DSI / PD pass on Bed B?) as **yes** when given an adequate NSGA-II budget plus combined
warm-start.

Recent task results presented:

* t0080 (192 cells, fresh LHS, 54-d v3 substrate, $0.7458): negative; closest-to-joint cell 188 at
  DSI 0.000 / PD 9.25 Hz (distance 0.85); architectural diagnostic flagged budget + warm-start as
  the limiters.
* t0081 (768 cells, t0078+t0080 warm-start, same 54-d v3 substrate, $2.39): positive; cell 767 at
  DSI 0.494 / PD 11.39 Hz crosses both thresholds; +56% DSI and +1.71 Hz PD over t0078
  closest-to-joint; monotonic HV growth 6.59 -> 16.33 with no plateau. Cell 767 also exceeds the de
  Rosenroll 2026 correlated-SAC baseline (0.39 -> +27%) and Sivyer 2010 rabbit ON range (0.45).
  Joint z-score against RivlinEtzion 2012 stable cells: DSI -1.50 sigma (was -2.44 in t0078, -4.11
  in t0080), PD +0.12 sigma -- DSI deficit narrowed by 2.6 sigma in two tasks.

Project state inventory:

* 81 tasks total; all completed.
* 14 prior brainstorm sessions; this is session 15.
* 240 active uncovered suggestions: 11 high-priority, 187 medium, 42 low.
* Substrates: Bed A (ModelDB 189347 / Poleg-Polsky 2016 lineage with gabaMOD scalar inhibition); Bed
  B v3 (de Rosenroll 2026 + AIS hard floors + dendritic-spike machinery, 54-d, established by t0081
  as the project's working substrate).
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued; no compute requirement; deferred
  from session 14.

Budget pre-session:

* Spent: $8.13 / $10.00 (81.3%). Past 80% warn threshold.
* Remaining: $1.87 before stop threshold.
* Of the 11 high-priority suggestions, only S-0081-03 (Vm-trace deep-dive cell 767) fits in the
  remaining budget without an increase. S-0081-01 ($5-10) and S-0081-02 ($3-4) are out of budget.

Independent priority reassessment of the 11 high-priority suggestions:

| Suggestion | Stored | Reassessed | Reason |
| --- | --- | --- | --- |
| S-0080-01 (full-scope re-run on v3 54-d) | high | REJECT | t0081 ran 768 cells = pop=96/gen=8 with warm-start = full plan scope; achieved pass. |
| S-0080-02 (substrate regression check) | high | REJECT | t0081's positive result rules out the substrate-regression hypothesis directly. |
| S-0080-03 (warm-start NSGA-II from t0078) | high | REJECT | t0081 IS this approach; combined warm-start was the deciding ingredient. |

Remaining 8 high-priority bucketed:

* t0081 follow-ups (1 cheap, 2 expensive): S-0081-03 (Vm-trace, $0, highest immediate yield);
  S-0081-01 (multi-replicate, $5-10, out of budget); S-0081-02 (extend NSGA-II, $3-4, out of
  budget).
* Deferred-but-cheap analyses on t0067 / t0074 data: S-0067-01, S-0074-01, S-0074-02, S-0074-03.
* Cross-substrate / cross-bed: S-0076-04, S-0070-01.

## Clarification Questions

AI:
1. Notes / steering for this session?
2. Will you raise the $10 budget cap, or plan strictly within $1.87? (Decides whether
   multi-replicate / gen-extension are on the table.)
3. Mechanism vs replication priority?
4. t0075 disposition (cancel / execute / leave deferred)?
5. Scope appetite (one bundled task or a small wave)?

Researcher: "I topped up $10 so we have more available budget. I would like you to implement
s0081-02 and s0081-03. s0081-02: we can do some longer. It still shows a raise in HV so let's do no
3 more generations are suggested but at least 5 and then check if it is still raising and decide
when to stop. suggestion 03 can do while you wait for optimisation results."

## Discussion -- Round 1: New Tasks

AI proposed two tasks:

**Task A (t0083): extend t0081 NSGA-II** (S-0081-02)

Asked the researcher to confirm two interpretation choices:

1. Continuation strategy: continue NSGA-II from t0081's final gen-7 population (96 surviving
   individuals) vs re-launch from warm-start init for longer. AI recommended continuation; preserves
   t0081's evolutionary trajectory and cell 767.
2. Adaptive stop rule: run >=5 more generations (gen 8-12), evaluate HV growth, stop when HV
   relative improvement averaged over the last 3 generations falls below 1%
   (`(HV(N) - HV(N-3)) / HV(N-3) < 0.01`). Hard cap +10 generations (gen 8-17). Hard cost cap $5.00
   (5 gens at ~$0.30/gen ~= $1.50; 10 gens ~= $3; $5 leaves ~50% safety margin).

**Task B (t0084): Vm-trace deep-dive** (S-0081-03)

Per-direction (8 angles * 3 cells: 767, 637, 762) Vm traces from proximal soma, mid dendrite, distal
dendrite. Plot dendritic-spike onset times, NMDA conductance trajectories, AIS spike correlation per
direction. Local CPU only, no remote machine, ~10 min runtime, $0 compute cost. Output: 12 figure
assets and one answer asset attributing cell 767's DSI to specific dendritic-spike machinery (NMDA
Mg-block recruitment vs distal Nav1.6 dendritic spikes vs NaP sustained depolarisation, or a
combination).

Both tasks depend on t0081. Each runs in its own worktree; they execute in parallel as researcher
requested.

## Discussion -- Round 2: Suggestion Cleanup

AI proposed three rejections superseded by t0081:

1. **Reject S-0080-01** (re-run NSGA-II at full plan scope) -- covered by t0081 (768 cells =
   pop=96/gen=8 = full plan scope at warm-start; pass criterion crossed).
2. **Reject S-0080-02** (substrate regression check) -- t0081's positive result rules out
   substrate-regression hypothesis directly.
3. **Reject S-0080-03** (warm-start NSGA-II from t0078) -- t0081 IS this. Combined t0078+t0080
   warm-start was the deciding ingredient.

AI defaulted to keeping all other suggestions unless researcher specifically flagged any.

## Discussion -- Round 3: Confirmation

AI asked three open questions before the confirmation gate:

* t0075 disposition (queued through 3 sessions): leave / cancel / include?
* Hard cost cap on Task A: is $5.00 acceptable?
* Task A continuation vs re-launch: confirm continuation from gen-7 final state.

Researcher: "Round 1 Task A - 1. Continuation 2. confirm Task B: Confirm Round 2: Confirm Round 3:
leave, $5 acceptable, continuation".

The Round 3 confirmation authorises the entire remaining lifecycle through PR merge.

## Decisions Summary

1. **Create t0083** (`bedb_v3_extend_nsga2_gen8plus`). Continue NSGA-II from t0081's gen-7 final
   population for >=5 more generations (gen 8-12 minimum). Adaptive HV-plateau stop rule: terminate
   when relative HV improvement averaged over last 3 generations falls below 1% starting at gen 11.
   Hard cap on additional generations: 10 (gen 8-17 maximum). Reuse t0081 harness and t0080 v3
   substrate library verbatim. Pass criterion: at least one additional joint-pass cell beyond
   t0081's cell 767, OR final HV > 16.33 with HV-plateau detected before gen 17. Compute estimate
   $1.50 - $3.00 over 6-12 wall-clock hours on Vast.ai 64-core EPYC 7B13 ($0.2382/hr); hard cost cap
   $5.00. Source suggestion: S-0081-02. Dependencies: t0081, t0080, t0078, t0024.

2. **Create t0084** (`t0081_cell_767_vm_trace_deepdive`). Local-CPU per-direction Vm-trace deep-dive
   of cells 767, 637, 762. Proximal-soma, mid-dendrite, distal-dendrite Vm; per-segment NMDA
   conductance trajectories; per-segment Nav1.6 / NaP current decomposition; per-direction AIS spike
   onset times. Generate 12 figure assets. Produce one answer asset at
   `assets/answer/cell-767-dendritic-spike-mechanism-attribution/` attributing cell 767's DSI to
   NMDA Mg-block / distal Nav1.6 / NaP / combination using fractional-channel-contribution metric.
   Local CPU only, $0, ~15-30 min runtime. Source suggestion: S-0081-03. Dependencies: t0081, t0080.

3. **Reject S-0080-01** -- covered by t0081.

4. **Reject S-0080-02** -- substrate-regression hypothesis ruled out by t0081's positive result.

5. **Reject S-0080-03** -- t0081 IS this approach.

6. **t0075** -- leave queued (no action).

7. No reprioritisations, no answer assets in this brainstorm task, no new suggestions in this
   brainstorm task.
