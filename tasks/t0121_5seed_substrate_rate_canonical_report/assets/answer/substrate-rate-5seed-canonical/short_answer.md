---
spec_version: "2"
answer_id: "substrate-rate-5seed-canonical"
answered_by_task: "t0121_5seed_substrate_rate_canonical_report"
date_answered: "2026-05-24"
---
## Question

What is the LEGIT joint-pass acceptance rate on the 68-d Bed B + 14-d morphology NSGA-II substrate,
estimated from a 5-seed random-init batch, and how does it compare to Hay 2011 and Druckmann 2007?

## Answer

The 5-seed mean LEGIT joint-pass acceptance rate is 2.58% with sample SE 1.50%, a normal-approx 95%
CI of (-0.35%, 5.51%), and a bootstrap 95% CI of (0.38%, 5.53%); the point estimate is roughly 6.5x
Hay 2011's 0.40% envelope and 25.8x Druckmann 2007's 0.10% baseline, and 3 of 5 seeds individually
exceed the Hay envelope. Both 95% CIs bracket zero and both literature baselines, so this batch
cannot statistically reject the literature rates despite the elevated point estimate.

## Sources

* Paper: `10.1371_journal.pcbi.1002107`
* Paper: `10.3389_neuro.01.1.1.001.2007`
* Paper: `10.1371_journal.pcbi.1012039`
* Task: `t0106_long_pdnd_nsga2_300gen`
* Task: `t0112_t0106_seed77_replicate`
* Task: `t0113_t0106_seed2247_replicate`
* Task: `t0114_seed7755_no_autostop`
* Task: `t0115_seed9354_no_autostop`
* Task: `t0078_bedb_mobo_v2_ais_tiered_ahp`
* Task: `t0097_multi_obj_optim`
* Task: `t0102_seedscale_n4_gen20`
