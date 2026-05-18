---
spec_version: "3"
task_id: "t0108_t0106_cluster_factor_dsi05_pd10"
step_number: 6
step_name: "research-code"
status: "completed"
started_at: "2026-05-18T13:02:00Z"
completed_at: "2026-05-18T13:05:00Z"
---

# Step 6: research-code

## Summary

Reviewed the t0105 implementation as the closest prior art (constants.py, paths.py, factor_analysis.py, schemas.py) and confirmed the reusable patterns: explicit electrophys + morphology param names, varimax rotation, dedupe by 68-d vector. Verified t0106 evaluation file schema is compatible.

## Actions Taken

* Read t0105 code/constants.py and code/factor_analysis.py.
* Loaded t0106 evaluation file gzipped JSON; confirmed top-level dict with evaluations list of dicts containing dsi_vector_sum, pd_rate_hz, vector_68d, generation, objective_F_minimised keys.

## Outputs

* Confirmed t0105 patterns reusable for cohort load, dedupe, factor analysis.
* Confirmed t0106 schema: 68-d vector with 54 electrophys + 14 morphology in canonical order.

## Issues

* Discovered factor_analyzer 0.5.1 is incompatible with scikit-learn 1.8.0 (force_all_finite renamed). Fallback to sklearn FactorAnalysis + manual varimax rotation in factor_analysis.py.
