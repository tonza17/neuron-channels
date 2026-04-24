---
spec_version: "2"
answer_id: "electrotonic-length-collapse-of-length-and-diameter-sweeps"
answered_by_task: "t0041_electrotonic_length_collapse_t0034_t0035"
date_answered: "2026-04-24"
---
# Do length and diameter sweeps collapse onto a single L/lambda curve?

## Question

Do the t0034 distal-length sweep and the t0035 distal-diameter sweep collapse onto a single
DSI-vs-L/lambda curve under Rall's cable theory, and should t0033 parameterise dendritic morphology
in 1-D (electrotonic length L/lambda) or 2-D (raw length x raw diameter)?

## Answer

No. The two sweeps do not collapse onto a single DSI-vs-L/lambda curve: in the overlapping L/lambda
interval (0.058-0.116) the Pearson r between the paired sweeps is **+0.42** for primary DSI and
**-0.68** for vector-sum DSI, both well below the 0.9 confirmation threshold, and the sign of the
vector-sum r is opposite to the prediction. Pooled degree-2 polynomial fits leave residual RMSE of
**0.040** (primary) and **0.024** (vector-sum), indicating that non-cable effects dominate the
DSI-vs-L/lambda response. t0033 should retain the 2-D (raw length x raw diameter) morphology
parameterisation rather than compress to 1-D L/lambda, because the direction of the DSI response is
not determined by L/lambda alone.

## Sources

* Task: `t0034_distal_dendrite_length_sweep_t0024`
* Task: `t0035_distal_dendrite_diameter_sweep_t0024`
* Task: `t0024_port_de_rosenroll_2026_dsgc`
* Task: `t0033_plan_dsgc_morphology_channel_optimisation`
