# Research: Code (Brainstorm Session 21)

## Objective

No research required for brainstorming session.

## Background

Brainstorm sessions do not perform code research. The session did inspect one project code constant
during the discussion (recorded here for the audit trail).

## Methodology Review

`tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py:43` defines `N_SEEDS: int = 20`,
the noise-replicate count per direction reused by every downstream NSGA-II / MOBO task (t0081,
t0083, t0091, t0099, the proposed t0102). This constant is the per-cell trial count; the GA-level
"seed" count is implicit and equal to 1 in every task except t0099 (3 seeds).

## Key Findings

* Our per-cell evaluation cost is `8 directions x 20 trials = 160 NEURON sims per parameter vector`,
  vs. Poleg-Polsky's `12 directions x 5 speeds x 1 trial = 60 sims per parameter vector`.
* Dropping `N_SEEDS` from 20 to 4 (factor of 5) is the cheapest single knob to free budget for more
  GA-level seeds or more generations.

## Recommended Approach

Use the new constant only inside the new task (`t0102`) for now; do not propagate the lower default
into `t0080`'s code until t0102 shows the DSI/PD scatter remains acceptable. Tracked as
medium-priority suggestion S-0101-02.

## References

* `tasks/t0080_bedb_mobo_v3_dendritic_spike_nsga2/code/constants.py:43`
* `tasks/t0099_random_init_pareto_robustness/results/results_summary.md`
* `tasks/t0091_morphology_extended_nsga2_v1/results/results_summary.md`
