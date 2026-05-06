---
spec_version: "2"
task_id: "t0086_robustness_cluster_bio_comparison"
date_completed: "2026-05-06"
---
# Results Summary -- t0086_robustness_cluster_bio_comparison

## Summary

Re-evaluated the top 20 cells from t0083 (15 joint-pass + 5 closest near-pass) at 24 directions x 30
inner seeds x 5 outer-seed replications on Vast.ai EPYC 7B13. **6 cells were Genuine** (5/5 reps
pass DSI >= 0.4 AND PD >= 10 Hz), **7 Marginal** (3-4/5), **7 Stochastic** (<=2/5). k-means
clustering on the 6 Genuine cells in 54-d parameter space selected **best_k=2**; both clusters were
classified **exotic** by the biological scorecard, driven by extreme NMDA per-synapse conductance
(>85 sigma above Sivyer 2013) and elevated distal NaP density (>7 sigma above Stuart 1999) common to
both clusters.

## Metrics

* **Genuine cells: 6 / 20** (cells 1517, 1604, 1634, 1639, 1663, 1677). Project pass criterion of
  > =3 Genuine cells for cluster analysis is **met**.
* **Marginal cells: 7 / 20** (cells 767, 1304, 1379, 1504, 1559, 1624, 1721). Cell 767 (the original
  t0081 joint-pass) is Marginal at 3/5; cell 1304 (t0083's headline highest-DSI 0.765) is Marginal
  at 3/5.
* **Stochastic cells: 7 / 20** (cells 1238, 1457, 1482, 1484, 1548, 1710, 1723). Cell 1723 had
  highest DSI=1.0 but PD=6.14 Hz consistently below the 10 Hz threshold.
* **Best k = 2** by silhouette score 0.155; k-means + hierarchical-cosine + hierarchical-euclidean
  all agree (ARI = 1.0). 50-sample bootstrap stability ARI mean **0.597** (sd 0.387) -- moderate
  given small Genuine pool (n=6).
* **Cluster 0** (cells 1634, 1639, 1663): aggregate verdict **exotic**. NMDA conductance at **+122
  sigma** above Sivyer 2013 prior, NaP distal at **+24 sigma** above Stuart 1999, GABA rho0 at **+7
  sigma** above de Rosenroll 2026. AIS-to-soma Nav ratio 30.5 (+4 sigma vs Werginz 2024's 17.3).
* **Cluster 1** (cells 1517, 1604, 1677): aggregate verdict **exotic**. NMDA conductance at **+85
  sigma**, NaP distal at **+7 sigma**, GABA lambda at **+6 sigma** above de Rosenroll 2026.
  AIS-to-soma Nav ratio 11.5 (within Werginz 2024 plausible range).
* **Final cost $1.595 / 4.59 hours** wall-clock at $0.3474/hr (resolved from
  selected_offer.price_per_hour, NOT a hard-coded constant). Under the **$3.50 hard cap**. REQ-X
  cost-watchdog rate-fix verified end-to-end.

## Verification

* `verify_research_code`: PASSED (0 errors).
* `verify_plan`: PASSED (0 errors).
* `verify_logs`: PASSED (0 errors, 5 warnings -- benign command-log non-zero exit codes from
  research-code experiments and missing session-capture files; addressed in reporting step).
* `verify_machines_destroyed`: PASSED (0 errors, 3 warnings -- API unreachable warning is expected
  since the instance was already destroyed; missing failure_phase/timestamp on the failed_attempts
  entry is a known v2-spec gap; missing checkpoint_path is acceptable for a 4.6-hour run).
* `verify_task_file`, `verify_task_dependencies`, `verify_task_folder`: PASSED.
