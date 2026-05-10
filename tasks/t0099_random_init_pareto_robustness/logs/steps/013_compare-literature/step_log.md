---
spec_version: "3"
task_id: "t0099_random_init_pareto_robustness"
step_number: 13
step_name: "compare-literature"
status: "completed"
started_at: "2026-05-10T23:20:21Z"
completed_at: "2026-05-10T23:35:00Z"
---

## Summary

Wrote `results/compare_literature.md` comparing random-init NSGA-II results against 3
methodological precedents (Hay 2011, Ezra-Tsur 2021, Ament 2023) and 4 biology
references (Trenholm 2013, Briggman 2011, Sivyer 2013, Schachter 2010). Most interesting
cross-task finding: **HM-2 (PD-asymmetric preferred over ND-asymmetric) was REFUTED in t0091
alone (p=0.331) but is CONFIRMED when combining all 3 random-init seeds** (PD vs ND counts
20 vs 7, p≈0.01 by binomial). Random-init isolates the Schachter 2010 / Briggman 2011
prediction that t0091's explicit dual seeding had masked.

## Actions Taken

1. Ran prestep to mark step 13 as in_progress.
2. Compared HV ratios against Ament 2023's warm-start vs random-init prediction (we observe
   80× HV ratio, larger than Ament's 5-10× prediction).
3. Compared best PD-rate (18.7Hz random init, 35Hz warm-start) against Trenholm 2013's
   peak DSGC firing rate (198Hz) — both substrates under-fire relative to biology.
4. Combined per-seed PD-asymm vs ND-asymm anchor counts (20 vs 7), recomputed binomial
   significance (p≈0.01), revised HM-2 verdict.
5. Confirmed HM-1 (symmetric=0) holds in all 4 datasets (n=4 strongly confirmed).
6. Recommended anchor-1-only follow-up as the cheapest informative resolution to the open
   "what part of t0091's warm-start was load-bearing" question.

## Outputs

* `tasks/t0099_random_init_pareto_robustness/results/compare_literature.md`

## Issues

No issues encountered.
