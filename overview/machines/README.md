# Machine Provisioning (3 machines)

**3** machines provisioned across **3** tasks. Total cost: **$5.74**.

**2** failed provisioning attempts wasted **$0.00** (40.0% failure rate).

## Summary

| Field | Value |
|-------|-------|
| Total machines | 3 |
| Total failed attempts | 2 |
| Failure rate | 40.0% |
| Avg provisioning time | 720s |
| Total cost | $5.74 |
| Total wasted cost | $0.00 |

## Cost by GPU Tier

| GPU | Total Cost (USD) |
|-----|-----------------|
| RTX 5060 Ti (idle, unused) | $3.93 |
| Quadro P4000 | $1.06 |
| RTX PRO 4000 (idle, unused) | $0.75 |

## Failure Reasons

| Reason | Count |
|--------|-------|
| Duplicate creation - first vastai create call returned no JSON to stdout under PowerShell, leading to a second create that succeeded; the first instance came up in stopped state (auto-cleaned via vastai destroy 36068056 -y). Same root cause as t0076's create-duplicate issue. | 1 |
| Duplicate creation - the first vastai create call returned exit 0 with empty stdout under the run_with_logs subprocess pipe (no JSON visible to the caller), so a second create call was made which also returned empty stdout. Both create calls actually succeeded server-side, producing two instances on the same offer 31639237. Instance 36137287 came up running on ssh2.vast.ai:17286 (kept); instance 36137292 came up stopped on ssh7.vast.ai:17292 and was destroyed via 'vastai destroy instance 36137292 -y'. Same root cause as t0078's create-duplicate issue; the bug is in run_with_logs swallowing vastai's stdout when invoked under PowerShell or Bash on Windows. | 1 |

## Tasks

| Task | Machines | Cost (USD) | Failed | GPUs |
|------|----------|------------|--------|------|
| [`t0076_bedb_dsi_firing_rate_mobo`](../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) | 1 | $1.06 | 0 | Quadro P4000 |
| [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) | 1 | $3.93 | 1 | RTX 5060 Ti (idle, unused) |
| [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) | 1 | $0.75 | 1 | RTX PRO 4000 (idle, unused) |
