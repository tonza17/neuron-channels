# Results Summary: Voff_bipNMDA=1 DSI vs gNMDA Test

## Summary

Switching the deposited DSGC's NMDA model from voltage-dependent (`Voff_bipNMDA = 0`, exptype = 1)
to voltage-independent (`Voff_bipNMDA = 1`, exptype = 2) flattens the DSI vs gNMDA curve
substantially — verdict **H2 (intermediate)**: max-min DSI range drops from 0.174 to **0.066**
(within H1's 0.10 cutoff), but the linear-fit slope is still **-0.024 per nS** (above H1's 0.02
cutoff and below t0047's reference -0.058 per nS). The absolute DSI values stay between **0.04 and
0.10** — never reaching the paper's claimed flat ~0.30 line. Mechanism confirmed: NMDA PD/ND ratio
collapses from 2.05 (Voff=0 Mg-block runaway) to 1.00 (Voff=1 symmetric) at gNMDA = 0.5 nS, exactly
as predicted.

## Metrics

* **DSI vs gNMDA at Voff=1**: 0.103 (gNMDA=0), **0.102** (gNMDA=0.5), 0.078 (gNMDA=1.0), 0.057
  (gNMDA=1.5), 0.053 (gNMDA=2.0), 0.044 (gNMDA=2.5), 0.037 (gNMDA=3.0).
* **Range test**: max-min DSI = **0.066** vs H1 threshold 0.10 → **H1 passes** (curve is flatter
  than 0.10 in absolute range).
* **Slope test**: linear-fit slope = **-0.024 per nS** vs H1 threshold |slope| < 0.02 → **H1
  fails** (still trending downward, though much less than t0047's -0.058 per nS).
* **Combined verdict**: **H2** — flatter than t0047 baseline by 2.6x on range and 2.4x on slope,
  but never reaches the paper's flat 0.30 line.
* **NMDA conductance PD/ND ratio at gNMDA = 0.5 nS**: collapses from 2.05 (Voff=0, t0047) to
  **1.00** (Voff=1, this task). Voltage-driven asymmetry removed.
* **NMDA summed conductance at gNMDA = 0.5 nS**: PD **50.18 +/- 1.91 nS**, ND **50.05 +/- 2.46 nS**
  (Voff=1) vs t0047's PD 69.55 / ND 33.98 nS (Voff=0).
* **AMPA and GABA conductances unchanged** between Voff=0 and Voff=1 (as expected — Voff only
  affects NMDA Mg-block kinetics).
* **Residual DSI at Voff=1**: bounded by AMPA/GABA balance (~0.04-0.10), not NMDA.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on the 7-variant `metrics.json`
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `ruff check`, `ruff format`, `mypy -p tasks.t0048_voff_nmda1_dsi_test.code` — clean
* Smoke test (4-trial validation gate at gNMDA = 0.5 and 3.0): PASSED before launching full sweep
