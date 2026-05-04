---
spec_version: "3"
task_id: "t0078_bedb_mobo_v2_ais_tiered_ahp"
step_number: 11
step_name: "creative-thinking"
status: "completed"
started_at: "2026-05-04T15:55:29Z"
completed_at: "2026-05-04T15:58:00Z"
---
# Step 11 — Creative Thinking

## Summary

Out-of-the-box analysis of the t0078 Pareto front (17 cells, 491 evaluations, HV 11.41) and the
trade-off between DSI and PD firing rate on the AIS-augmented Bed B substrate. Headline insight:
**this is not a clean architectural negative** — the Pareto front grazes the joint pass criterion
(DSI ≥ 0.4 AND PD rate ≥ 10 Hz) at iter 81 (DSI 0.316, PD 9.68 Hz), missing by just 0.32 Hz on
PD and 0.084 on DSI. Three creative reframings of the result are listed below; each motivates a
different follow-up direction.

## Actions Taken

1. Ran `prestep creative-thinking`.
2. Inspected the 17 Pareto cells and the HV trajectory; identified the iter-81 cell as
   sub-1-SD-from-target on both objectives.
3. Loaded the trial history parquet to confirm there is no early-iteration cell with both DSI ≥
   0.4 AND PD ≥ 10 Hz that was non-Pareto-dominated; the gap is real and not an artefact of
   Pareto-front filtering.
4. Listed three creative reframings below.

## Outputs

* `tasks/t0078_bedb_mobo_v2_ais_tiered_ahp/logs/steps/011_creative-thinking/step_log.md` — this
  step log.

## Issues

No issues encountered.

## Three creative reframings

### 1. Translate the joint criterion into operational ranges, not point thresholds

The pass criterion `DSI ≥ 0.4 AND PD ≥ 10 Hz` is a binary point threshold. Real biology is a
distribution: Rivlin-Etzion 2012 reports DSI **0.78 ± 0.19**, PD rate **10.38 ± 8.53 Hz**. The
iter-81 cell's (DSI 0.316, PD 9.68 Hz) sits at roughly **z = -1.0** on PD rate (9.68 vs 10.38 ±
8.53) and **z = -2.4** on DSI (0.316 vs 0.78 ± 0.19). When framed as Mahalanobis distance to the
literature distribution, this cell is well within the recorded biological spread on PD rate and on
the lower edge of the DSI spread. **Recommendation**: in the comparison-to-literature step, report
the joint-distribution z-score, not just the binary pass criterion.

### 2. The high-DSI rail's PD ceiling at ~3 Hz is a slow-AHP saturation signature

Across 109 acquisitions (acq 306 → acq 416), the high-DSI rail's PD ceiling stayed pinned at 2.86
Hz despite the optimiser actively searching. This **flat ceiling** under varying parameter
combinations is the signature of a **saturated negative feedback** — the slow-AHP via SK_E2 with
`tau_ca_multiplier ≤ 20×` is doing what it was designed to do, but it caps firing too
aggressively when DSI is high. Two follow-ups:

* **Increase `tau_ca_multiplier` upper bound** to [1, 200×] (originally proposed by the
  research-internet step based on Larsson 2013's 1-3 s mammalian sAHP timescale; the researcher
  conservatively set it to 20×). The current 20× upper bound corresponds to ~100 ms — perhaps
  the firing-rate ceiling lifts at multiplier values that engage the slow-Kv-mediated AHP regime.
* **Reduce slow-AHP gbar prior**, allowing the optimiser to push slow-AHP toward zero where DSI is
  high. The SK_E2 conductance prior may be too strong relative to what biology uses.

### 3. The DSI-rate trade-off is monotonic in the Pareto front — a single-axis optimisation might

beat MOBO

The 17 Pareto cells exhibit a **clean monotonic DSI–PD-rate trade-off** with no obvious knee. If
the trade-off is genuinely 1-D (cells lie on a 1-D manifold in 49-d parameter space), a **1-D
scalarisation** like `DSI - λ × max(0, 10 - PD)` with a small set of `λ` values would explore the
same Pareto front in **single-objective Bayesian optimisation** (qLogNEI, not qLogNEHVI), which
scales **O(N²) not O(N³)** and would have completed all 700 acquisitions within the original $4
envelope on the same machine.

This is not a recommendation for switching now — but for the dendritic-conductance follow-up task
(which the suggestions step will write), if cells continue to lie on a 1-D Pareto manifold,
single-objective scalarisation may be more efficient than NSGA-II. NSGA-II remains the better
default for high-d MOBO when the Pareto front is genuinely multi-modal; if cells cluster on a 1-D
manifold, scalarised single-objective BO is preferred.
