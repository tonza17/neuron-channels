# Results Summary: Test t0020 deposited DSGC under EPSP/IPSP/FULL protocol

## Summary

The deposited Poleg-Polsky & Diamond 2016 DSGC was driven through the EPSP_PASSIVE / IPSP_PASSIVE /
FULL trial-mode protocol — six trials (3 modes × 2 directions × 1 seed) — decomposing the
somatic Vm into pure-excitatory and pure-inhibitory components. Headline finding: **the model's
direction selectivity is produced almost entirely by shunting inhibition, not hyperpolarising
inhibition**. The IPSP_PASSIVE traces stay flat at the inhibitory reversal potential e_SACinhib =
-60 mV in both PD and ND, while the EPSP_PASSIVE traces are bit-identical between directions
(gabaMOD = 0). The FULL trace shows a 15× spike count difference (15 PD vs 1 ND) driven entirely by
the PD-vs-ND difference in the inhibitory *conductance* (gabaMOD 0.33 vs 0.99) shunting away the
otherwise direction-invariant excitatory drive.

## Metrics

* **FULL PD spike count**: **15** (firing rate ≈ **15.0 Hz** over 1000 ms)
* **FULL ND spike count**: **1** (firing rate ≈ **1.0 Hz** over 1000 ms)
* **DSI (single-seed point estimate, spike-count-based)**: **0.875** ((15 − 1) / (15 + 1))
* **EPSP_PASSIVE peak Vm**: **-29.8 mV** (PD = ND, bit-identical, +28.6 mV above baseline)
* **IPSP_PASSIVE peak Vm**: **-60.0 mV** (PD), **-60.0 mV** (ND) — flat at e_SACinhib
* **IPSP_PASSIVE peak − baseline**: **+0.10 mV** (PD), **+0.11 mV** (ND) — noise floor
* **FULL peak Vm**: **+43.2 mV** (PD), **+43.3 mV** (ND) — both reach Na+-spike peak
* **FULL baseline Vm**: **-58.9 mV** (PD), **-59.3 mV** (ND)
* **Trials run**: 6 (PD × ND for each of FULL / EPSP_PASSIVE / IPSP_PASSIVE)
* **Wall-clock**: **18.7 s** for the sweep, ~1 s for plotting (local Windows workstation)
* **Sample count per trial**: 10,001 (dt = 0.1 ms × tstop = 1000 ms)

## Verification

* `verify_research_code` — PASSED (0 errors, 0 warnings) on `research_code.md`.
* `verify_plan` — PASSED (0 errors, 0 warnings) on `plan/plan.md`.
* `verify_task_dependencies` — PASSED (0 errors, 0 warnings) at check-deps step (t0020 completed).
* Per-trial `_assert_bip_positions_baseline` — PASSED in all six trials. BIP synapse positions
  remained at their canonical baseline coordinates throughout, confirming the t0008 spatial rotation
  logic was not silently re-engaged.
* Single-seed sanity gate vs t0020 reference: t0020 reported peak PD firing rate **14.85 Hz**
  averaged across 20 PD trials. The t0065 single PD trial yields **15.0 Hz** — within the 1-trial
  Poisson uncertainty band of t0020's mean.
* Mypy and ruff pass on all code in `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/`.

## Conclusion

Two-line summary for follow-on tasks:

* **EPSP_PASSIVE shows direction-invariant +28.6 mV depolarising envelope** in this model; direction
  selectivity is not encoded on the excitatory side.
* **IPSP_PASSIVE shows zero membrane deflection** because the cell's resting potential coincides
  with e_SACinhib = -60 mV; the inhibitory drive's effect is therefore purely shunting (changing
  input resistance), and the FULL-mode PD/ND difference must come entirely from this shunt.
