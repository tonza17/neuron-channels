---
spec_version: "3"
task_id: "t0131_rd1_na_k_remodelling_dsgc_dsi"
step_number: 9
step_name: "implementation"
status: "completed"
started_at: "2026-10-27T10:35:35Z"
completed_at: "2026-10-27T16:30:35Z"
---
# Step 9: Implementation

## Summary

Ran the four-part rd1 experiment on 8 reference cells. Only the panel C sustained-current ratio was reproduced; rd1-like cells never spike, so signed DSI is undefined for them, and panel D was disproved in NEURON.

## Actions Taken

1. Screened 28 candidate cells and kept 8
2. Calibrated soma and AIS gNa and gK scaling on voltage clamp only
3. Ran current-clamp, spontaneous and bias tests, then the dendritic fallback arm
4. Ran signed-DSI protocol and heatmap
5. Fitted the panel D toy model and tested it in NEURON
6. Wrote the answer asset, metrics and 13 charts

## Outputs

* tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/code/*
* tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/data/*
* tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/results/images/*.png
* tasks/t0131_rd1_na_k_remodelling_dsgc_dsi/assets/answer/*

## Issues

WT-like reference cells are intrinsic pacemakers, so panels A and B have no valid WT baseline. The transient was fitted from the isolated soma and AIS Na current, a deviation from the plan. data/traces is about 68 MB across 194 files.
