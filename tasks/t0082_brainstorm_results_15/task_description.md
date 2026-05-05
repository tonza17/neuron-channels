# Brainstorm Session 15: Extend t0081 NSGA-II + Vm-Trace Deep-Dive of Cell 767

Fifteenth brainstorming session. Run on 2026-05-05 after t0081 (`bedb_v3_warmstart_nsga2`) completed
and **delivered the project's first joint-pass cell**: gen 7 cell 767 at **DSI 0.494 / PD 11.39 Hz**
on a 16-cell Pareto front (768 evaluations, $2.39 on Vast.ai). t0081 satisfied the project's working
pass criterion `DSI >= 0.4 AND PD >= 10 Hz` simultaneously for the first time in the project
lineage, decisively answering research question Q4 (do active dendritic conductances enable joint
DSI/PD pass on Bed B?) as **yes** when given an adequate NSGA-II budget plus combined t0078 + t0080
warm-start. Hypervolume grew monotonically from 6.59 (gen 0) to 16.33 (gen 7) with **no plateau**,
suggesting more generations can both characterise the joint-passing region and potentially find
additional joint-pass cells. The researcher topped up the project budget by $10 (now $11.87
remaining out of an effective $20 cap) to enable t0081 follow-ups.

## Decisions

* **Create t0083** -- `bedb_v3_extend_nsga2_gen8plus`. Continue NSGA-II from t0081's gen-7 final
  population (96 surviving individuals) for **at least 5 more generations** (gen 8-12) with an
  **adaptive HV-plateau stop rule**: terminate when relative HV improvement averaged over the last 3
  generations falls below **1%** (i.e., `(HV(gen N) - HV(gen N-3)) / HV(gen N-3) < 0.01`). Hard cap
  on total additional generations: **10** (gen 8-17 maximum). Reuse the t0081 harness verbatim with
  `n_gen` parameterised and a HV-plateau watchdog added. Pass criterion: characterise the
  joint-passing region (count of Pareto cells with `DSI >= 0.4 AND PD >= 10 Hz`; final HV; HV
  trajectory). Compute estimate ~$1.50 - $3.00 over ~6-12 wall-clock hours on Vast.ai 64-core EPYC
  7B13 at $0.2382/hr; **hard cost cap $5.00**. Source suggestion: S-0081-02. Dependencies: t0081
  (provides gen-7 final population), t0080 (substrate library), t0078, t0024.

* **Create t0084** -- `t0081_cell_767_vm_trace_deepdive`. Local-CPU per-direction (8 angles)
  Vm-trace deep-dive of cell 767 (joint-pass) plus the two neighbouring near-pass cells 637
  (distance 0.063) and 762 (distance 0.086) on the t0081 v3 substrate. Record proximal-soma,
  mid-dendrite, and distal-dendrite traces; plot dendritic-spike onset times, NMDA conductance
  trajectories per dendritic site, and AIS spike correlation per direction. Output: figure assets
  and an answer asset attributing cell 767's DSI improvement to specific dendritic-spike machinery
  (NMDA Mg-block recruitment vs distal Nav1.6 dendritic spikes vs NaP sustained depolarisation, or a
  combination). Local CPU only, **no remote machine, $0 compute cost**, ~10 min runtime per cell.
  Source suggestion: S-0081-03. Dependencies: t0081 (cell 767/637/762 parameter vectors and v3
  substrate library reference), t0080 (substrate library
  `de_rosenroll_2026_dsgc_ais_dendritic_spike`).

## Suggestion Cleanup

* **Reject three suggestions** as covered by t0081 (the prior-task analogue of session 14's
  S-0078-01/02/08 cleanup):

  * **S-0080-01** (high) -- Re-run NSGA-II at the full plan scope (pop=96, gen=40 = 3,840 cells) on
    the v3 54-d Bed B substrate. **Covered by t0081**, which ran 768 cells at pop=96 / gen=8 with
    combined warm-start and **achieved the joint pass criterion**. The full-scope re-run was
    successful at 4x t0080's evaluation budget; further extension is addressed by t0083.

  * **S-0080-02** (high) -- Substrate regression check on the t0076 iter-424 vector mapped to the v3
    54-d parameter space. **Covered by t0081's positive result**: t0081's compare-literature
    analysis explicitly states "the v3 substrate is not regressed -- it admits joint-pass cells when
    given an adequate budget plus warm-start". The regression hypothesis is ruled out by direct
    demonstration.

  * **S-0080-03** (high) -- Warm-start NSGA-II from t0078 Pareto cells mapped into the v3 54-d
    parameter space. **Covered by t0081**, which is exactly this approach: 5 t0080 Pareto cells
    verbatim + 17 t0078 Pareto cells projected from 49-d to 54-d + 74 fresh LHS = pop=96 warm-start.
    The deciding ingredient that produced cell 767.

## Reprioritisations

None.

## Tasks Cancelled or Updated

* **Cancelled**: none.
* **Updated**: none.
* t0075 (Bed A bio-realistic AIS one-axis sweep) remains queued for later opportunistic pickup;
  researcher confirmed "leave queued" disposition. Different substrate (Bed A) from t0083 / t0084
  (Bed B v3) and provides complementary one-axis sensitivity analysis.

## Assets Produced

No assets in this brainstorm task. The two new tasks t0083 / t0084 will produce: t0083 -- one
Pareto-front result bundle (extended HV trajectory, joint-pass cell count, cost record, machine
log); t0084 -- Vm-trace figure assets and one answer asset attributing the cell-767 DSI mechanism,
all under the t0084 task folder.

## Budget Context

The researcher topped up the project budget by $10 mid-session, raising the effective cap from $10
to $20 with $1.87 + $10 = **$11.87 remaining**. This unlocked S-0081-02 (estimated $1.50 - $3.00
with $5.00 hard cap) and S-0081-03 (estimated $0). Combined estimated total $1.50 - $3.00; combined
hard cap $5.00. Both fit comfortably in the topped-up $11.87 envelope while preserving runway for at
least one further follow-up (e.g., S-0081-01 multi-replicate confirmation at $5-10 across 3-5
replicates).
