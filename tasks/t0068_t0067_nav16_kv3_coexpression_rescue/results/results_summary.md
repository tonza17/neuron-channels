# Results Summary: Nav1.6 + Kv3 co-expression rescue test

## Summary

Tested whether co-inserting Kv3 with Nav1.6 on the deposited Poleg-Polsky DSGC soma rescues the
direction selectivity that Nav1.6 alone erodes (t0067 anchors: DSI = 0.48 at Nav1.6_med, 0.23 at
Nav1.6_high). 9 conditions × 2 directions × 5 seeds = 90 FULL trials, ~~10 min compute.
**Hypothesis FALSIFIED**: Kv3 does NOT rescue DSI. Across all 8 co-expression conditions DSI changes
by less than ±0.025 from the Nav1.6-only anchor. Instead, Kv3 slightly *boosts* firing rate (~~+10%
at high Kv3), scaling PD and ND equally.

## Metrics

| Condition | PD spikes (mean ± SD) | ND spikes (mean ± SD) | DSI | ΔDSI vs Nav1.6 anchor |
| --- | --- | --- | --- | --- |
| baseline | 14.2 ± 1.9 | 1.6 ± 1.3 | 0.797 | (vs no Nav1.6) |
| nav16_med (anchor) | 26.8 ± 3.6 | 9.4 ± 2.6 | 0.481 | (reference) |
| nav16_med + kv3_low | 27.2 ± 3.3 | 9.4 ± 2.6 | 0.486 | +0.005 (noise) |
| nav16_med + kv3_med | 28.6 ± 3.6 | 9.4 ± 2.6 | 0.505 | +0.024 (tiny) |
| nav16_med + kv3_high | 30.2 ± 4.3 | 10.4 ± 2.6 | 0.488 | +0.007 (noise) |
| nav16_high (anchor) | 57.4 ± 2.9 | 36.0 ± 3.1 | 0.229 | (reference) |
| nav16_high + kv3_low | 58.4 ± 3.0 | 36.6 ± 2.3 | 0.229 | +0.000 |
| nav16_high + kv3_med | 58.8 ± 3.3 | 37.0 ± 2.5 | 0.228 | -0.001 |
| nav16_high + kv3_high | 63.4 ± 4.2 | 39.4 ± 3.0 | 0.233 | +0.004 |

* **Largest DSI change from co-expression**: +0.024 (nav16_med + kv3_med); within sampling noise.
* **Firing-rate effect**: Kv3_high adds ~6 PD + ~3.4 ND spikes at Nav1.6_high — both directions
  scale up proportionally, so DSI is unchanged.
* **Trials with instability flags**: **0/90**.

## Verification

* `verify_research_code` — PASSED.
* `verify_plan` — PASSED.
* `verify_task_dependencies` — PASSED (t0008, t0065, t0067 all completed).
* `verify_task_metrics` — PASSED (registered DSI metric only).
* `verify_task_results` — PASSED (mandatory sections present).
* mypy + ruff PASSED on all task code.

## Conclusion

The S-0067-02 hypothesis (Kv3 rescues DSI by enabling faster recovery from Nav1.6's depolarising
drive) is **falsified** by these data. Two clean takeaways:

* **Kv3 doesn't change the inhibitory-to-excitatory conductance ratio**: Kv3 is a delayed rectifier,
  so it speeds *repolarisation* but doesn't reduce the depolarising drive that the GABA shunt has to
  fight against. The shunt's effectiveness — and hence DSI — is determined by
  `g_inhib / g_total`, which Kv3 doesn't alter.
* **Kv3 actually amplifies firing**: faster repolarisation → faster Na+ recovery from inactivation
  → next AP fires sooner. At Kv3_high + Nav1.6_high we see ~+10% firing in both directions,
  scaling PD and ND equally — DSI invariant.

DSI rescue would require something that breaks the symmetry: e.g., a channel that selectively
suppresses the cell at high firing rates (spike-frequency adaptation), or a synaptic-level
intervention that boosts inhibition. Suggestions S-0068-01 through S-0068-04 explore these
alternatives.
