# Brainstorm Session 22: Seed-77 Replicate of t0106 Joint-Pass Breakthrough

## Context

t0106 achieved the first joint-pass cells (DSI >= 0.5 AND PD-rate >= 30 Hz) in the entire t0080 ->
t0104 NSGA-II lineage: 123 unique cells across 3,744 evaluations from a single random-init GA seed
(44) over 40 generations on the 68-d Bed B + 14-d morphology substrate. The breakthrough was driven
by switching from 16-direction vector-sum DSI to 2-direction ratio DSI rather than by additional
compute. t0107 immediately followed with an 8-direction polar re-evaluation of 10 random top-50
cells, showing that the absolute DSI numbers fall sharply under the conventional 8-direction
protocol (mean t0106 ratio DSI = 0.939 vs t0107 8-dir vector-sum DSI = 0.519) while rank order is
preserved (Spearman rho = 0.758).

The open question this brainstorm addresses: is the t0106 result a seed-specific lucky run, or is
the joint-pass corner genuinely populated on this substrate? Without seed-replication, the headline
"123 unique joint-pass cells" cannot be claimed in any writeup as a substrate property; it is at
best a single-realisation point estimate.

## Decisions

A single new task `t0112_t0106_seed77_replicate` is commissioned: a minimum-change t0106 replicate
that varies only the GA seed (44 -> 77) and the multiprocessing pool restart cadence
(`_POOL_RESTART_EVERY` 25 -> 10 generations, motivated by NEURON's known memory creep). All other
parameters are held identical to t0106: pop=96, N_EVAL_SEEDS=3, N_DIRECTIONS=2, ratio DSI objective,
random LHS init, HV-plateau operator-stop criterion. Gen ceiling raised to 60 (from t0106's 300) so
a slower plateau is not artificially cut while keeping the budget bounded.

No suggestion rejections, reprioritisations, or task cancellations were applied in this session. The
325 uncovered suggestions remain at their current priorities pending the t0112 outcome, which will
either promote the suggestion backlog (if the replicate confirms substrate population) or trigger a
different next-wave plan (if it does not).

## Expected Outcomes

Two qualitatively distinct outcomes are possible from t0112:

1. **Replicate succeeds** (>= 40 unique joint-pass cells at the strict DSI >= 0.5 AND PD >= 30 Hz
   threshold): t0106 is confirmed as a substrate-population effect, not a seed-specific artefact.
   This promotes downstream analysis tasks (8-dir polar re-evaluation of all joint-pass cells,
   cluster + factor analysis extension, mechanism dissection) to high priority.

2. **Replicate fails** (substantially fewer joint-pass cells, or zero): the joint-pass acceptance
   rate has wide seed-variance; multi-seed replication and / or alternative optimiser (IBEA,
   Dang2023 mu = n log n NSGA-II) must precede any literature claim.

In either case, the result feeds the next brainstorm session's strategic direction.

## Budget

* This brainstorm task: $0 (planning only)
* Commissioned task t0112: $25 cost cap; expected actual ~$10-11 mirroring t0106
* Project envelope: $18.20 remaining of $75 prior to this session; ~$7-8 reserve after t0112 spend
