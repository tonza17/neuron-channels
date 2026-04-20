# Results Summary: Port ModelDB 189347 DSGC under native gabaMOD parameter-swap protocol

## Summary

Built a new sibling library asset `modeldb_189347_dsgc_gabamod` that drives the Poleg-Polsky &
Diamond 2016 DSGC under the paper's native two-condition `gabaMOD` swap protocol (PD = 0.33, ND =
0.99) instead of t0008's spatial-rotation proxy. The canonical 2 × 20 = 40-trial sweep reproduces
the direction-selectivity contrast (**DSI 0.7838** inside the literature envelope **[0.70, 0.85]**)
but the absolute firing rates remain depressed (**peak 14.85 Hz** vs envelope **[40, 80] Hz**), so
the combined two-point gate fails. This matches the Risk-3 scenario anticipated in the plan and is
recorded as a genuine experimental finding, not an implementation defect.

## Metrics

* **Direction Selectivity Index (DSI)**: **0.7838** — inside envelope [0.70, 0.85] ✓
* **Peak firing rate (mean PD)**: **14.85 Hz** — below envelope [40, 80] Hz ✗
* **Null firing rate (mean ND)**: **1.80 Hz**
* **PD firing rate stddev**: **1.59 Hz** across 20 trials
* **ND firing rate stddev**: **1.03 Hz** across 20 trials
* **Two-point envelope gate**: **failed** (DSI passes, peak fails)
* **vs t0008 rotation-proxy DSI (0.316)**: gabaMOD-swap DSI is **+0.468** higher — 2.48× the
  rotation-proxy value
* **Trials run**: 40 (20 PD + 20 ND), local runtime ~1.5 minutes on the Windows workstation

## Verification

* `verify_task_file.py` — PASSED (0 errors) at init-folders step
* `verify_task_dependencies.py` — PASSED (both t0008 and t0012 completed) at check-deps step
* `verify_library_asset.py` — N/A (script not present in `arf/scripts/verificators/`); structural
  validity confirmed manually: `details.json` has `spec_version "2"` and all required fields;
  `description.md` has YAML frontmatter, exceeds the 500-word minimum, and is flowmark-normalized
* Per-trial BIP-position assertion (REQ-3 critical guard) — PASSED across all 40 trials; BIP
  synapses stayed at baseline coordinates throughout, confirming the rotation logic was not silently
  re-engaged
