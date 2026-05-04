# Machine Provisioning (2 machines)

**2** machines provisioned across **2** tasks. Total cost: **$4.99**.

**1** failed provisioning attempts wasted **$0.00** (33.3% failure rate).

## Summary

| Field | Value |
|-------|-------|
| Total machines | 2 |
| Total failed attempts | 1 |
| Failure rate | 33.3% |
| Avg provisioning time | 710s |
| Total cost | $4.99 |
| Total wasted cost | $0.00 |

## Cost by GPU Tier

| GPU | Total Cost (USD) |
|-----|-----------------|
| RTX 5060 Ti (idle, unused) | $3.93 |
| Quadro P4000 | $1.06 |

## Failure Reasons

| Reason | Count |
|--------|-------|
| Duplicate creation - first vastai create call returned no JSON to stdout under PowerShell, leading to a second create that succeeded; the first instance came up in stopped state (auto-cleaned via vastai destroy 36068056 -y). Same root cause as t0076's create-duplicate issue. | 1 |

## Tasks

| Task | Machines | Cost (USD) | Failed | GPUs |
|------|----------|------------|--------|------|
| [`t0076_bedb_dsi_firing_rate_mobo`](../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) | 1 | $1.06 | 0 | Quadro P4000 |
| [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) | 1 | $3.93 | 1 | RTX 5060 Ti (idle, unused) |
