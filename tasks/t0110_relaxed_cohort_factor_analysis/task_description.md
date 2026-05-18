# t0110 — Factor Analysis at Relaxed Cohort (DSI > 0.2 AND PD > 3)

## Context

t0108 found that **all 10 varimax factor-score correlations with PD-rate were negative** in the
strict cohort (DSI > 0.5 AND PD > 10, N=150). Our working hypothesis is that this is a
truncated-cohort artifact: the strict filter places cells near the top corner of the DSI/PD
objective space, leaving no "go further up" direction for factors to align with.

The hypothesis is testable: at a less-truncated cohort, some PD correlations should flip
positive — particularly factors that align with "more axonal Na → more firing" should now show
up.

t0106 cohort sizes at candidate thresholds (raw → unique after 6-decimal dedupe):

* `DSI > 0.5 AND PD > 10` — 784 → 150 (t0108).
* `DSI > 0.3 AND PD > 5` — 986 → 195.
* `DSI > 0.2 AND PD > 3` — 1209 → **247** (this task).
* `DSI > 0.1 AND PD > 2` — 1525 → 312 (t0105's primary threshold).

DSI > 0.2 AND PD > 3 gives 247 unique cells — 65 % more than t0108 and a substantially better
sample/feature ratio for FA on 68 parameters.

## Goal

Re-run the same varimax FA pipeline as t0108 on 247 cells from t0106 at DSI > 0.2 AND PD > 3,
and compare directly to t0108's strict cohort. Answer one question: **does the all-negative PD
column persist under a less-truncated cohort?**

## Approach

* Load t0106 evaluations from
  `tasks/t0106_long_pdnd_nsga2_300gen/results/data/all_evaluations_seed44.json.gz`.
* Apply DSI > 0.2 AND PD > 3; dedupe by 68-d vector at 6 decimals.
* Same varimax FA pipeline as t0108: sklearn FactorAnalysis (rotation=None) + manual Kaiser
  varimax rotation; factor count by Kaiser eigenvalues > 1 capped at 10.
* Pearson r between each factor score and DSI / PD-rate.
* Render a side-by-side comparison chart: t0108 strict (left) vs t0110 relaxed (right) — same
  10-factor x-axis layout, same y-axis scale.

## Out of Scope

* New cluster analyses (already answered by t0108).
* New morphology gallery.
* New cohorts beyond DSI > 0.2 AND PD > 3.
* Re-running NSGA-II or new evaluations.
