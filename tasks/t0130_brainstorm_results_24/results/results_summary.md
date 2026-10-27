# Results Summary: Brainstorm Session 24

## Summary

One new task was commissioned, `t0131_rd1_na_k_remodelling_dsgc_dsi`, to test whether rd1-like Na/K
remodelling of the DSGC model reproduces the researcher's rd1 vs WT phenotype and what it does to
direction selectivity. Suggestion cleanup was deferred to the next session at the researcher's
request, so **0** corrections were written.

## Session Overview

* **Date**: 2026-10-27.
* **Context**: the researcher supplied `SomeResults.pdf` (panels A-D): rd1 RGCs show higher
  spontaneous firing (~7 Hz vs near silent), almost no evoked spiking at +60 pA, a ~1.7x larger
  sustained K current and a smaller Na transient. Panel D is a preliminary toy input-output model.
* **Project state at start**: 130 tasks (121 completed, 1 in progress), 412 uncovered suggestions
  (35 high), $67.16 of $100 spent.

## Decisions

1. **Create `t0131_rd1_na_k_remodelling_dsgc_dsi`** (standalone, local simulation, $0). Four parts:
   voltage-clamp calibration (panel C), current-clamp prediction (panels A and B), signed-DSI
   protocol, and reproduce-or-refute of panel D. Rationale: the researcher asked for a simple test
   of the rd1 finding and chose a standalone task.
2. **Soma and AIS scaling first, dendrites as fallback.** Rationale: researcher preference; the
   dendritic arm is added only if the phenotype is not reproduced.
3. **Spontaneous activity modelled by an exploratory tonic bias or noise.** Rationale: a single-cell
   model has no presynaptic network; the researcher said any approach that works is fine.
4. **Defer suggestion cleanup** (proposed rejections S-0113-01, S-0114-02, S-0116-06; downgrade
   S-0124-02; promotions S-0129-03/05/06 and S-0122-02). Rationale: the researcher asked to do these
   next time.
5. **t0128 left untouched.** Rationale: in progress, cannot be modified.

## Metrics

| Item | Count |
| --- | --- |
| Tasks created | 1 |
| Suggestions covered | 0 |
| Suggestions rejected | 0 |
| Suggestions reprioritized | 0 |
| Corrections written | 0 |
| New suggestions | 0 |

## Verification

* `verify_task_file`, `verify_corrections`, `verify_suggestions` and `verify_logs` for this task,
  and `verify_task_file` for t0131: see the PR description for final results.

## Next Steps

Execute `t0131_rd1_na_k_remodelling_dsgc_dsi`. Hold the suggestion cleanup for brainstorm session
25\.
