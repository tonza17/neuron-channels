# Machine Provisioning (13 machines)

**13** machines provisioned across **13** tasks. Total cost: **$59.08**.

**8** failed provisioning attempts wasted **$0.06** (38.1% failure rate).

## Summary

| Field | Value |
|-------|-------|
| Total machines | 13 |
| Total failed attempts | 8 |
| Failure rate | 38.1% |
| Avg provisioning time | 665s |
| Total cost | $59.08 |
| Total wasted cost | $0.06 |

## Cost by GPU Tier

| GPU | Total Cost (USD) |
|-----|-----------------|
| RTX 5060 Ti (idle, unused; CPU-only NEURON workload) | $18.08 |
| RTX 4090 (idle, unused; CPU-only NEURON workload) | $12.07 |
| RTX 3060 Ti (idle, unused; CPU-only NEURON workload) | $10.30 |
| RTX 4060 Ti (idle, unused) | $5.83 |
| RTX 5060 Ti (idle, unused) | $3.93 |
| RTX PRO 4000 (idle, unused) | $3.14 |
| RTX 3090 (idle, unused; CPU-only NEURON workload) | $1.99 |
| (idle, unused; CPU-only NEURON workload) | $1.59 |
| Quadro P4000 | $1.06 |
| RTX PRO 4000 (idle, unused; CPU-only NEURON workload) | $0.65 |
| RTX 4060 Ti (idle, unused; CPU-only NEURON workload) | $0.43 |

## Failure Reasons

| Reason | Count |
|--------|-------|
| Duplicate creation - first vastai create call returned no JSON to stdout under PowerShell, leading to a second create that succeeded; the first instance came up in stopped state (auto-cleaned via vastai destroy 36068056 -y). Same root cause as t0076's create-duplicate issue. | 1 |
| Duplicate creation - the first vastai create call returned exit 0 with empty stdout under the run_with_logs subprocess pipe (no JSON visible to the caller), so a second create call was made which also returned empty stdout. Both create calls actually succeeded server-side, producing two instances on the same offer 31639237. Instance 36137287 came up running on ssh2.vast.ai:17286 (kept); instance 36137292 came up stopped on ssh7.vast.ai:17292 and was destroyed via 'vastai destroy instance 36137292 -y'. Same root cause as t0078's create-duplicate issue; the bug is in run_with_logs swallowing vastai's stdout when invoked under PowerShell or Bash on Windows. | 1 |
| Vast.ai SSH proxy persistently failed to bind listen port 10284 (errno from logs: 'Error: remote port forwarding failed for listen port 10284'). Reboot did not resolve. Instance destroyed; provisioning retried on offer 34391256. | 1 |
| Duplicate creation: the orchestration accidentally issued two `vastai create instance 31574004 ...` calls back-to-back; both succeeded and Vast.ai returned two instance IDs (36372909 in actual_status=running and 36372913 in actual_status=loading). The second instance was destroyed via `vastai destroy instance 36372913 -y` within ~1 minute of creation, before it ever reached running state. This was an orchestration-level mistake, not a real provisioning failure of the offer or machine. | 1 |
| Duplicate-create artefact: the first 'vastai create instance 34391260' call returned exit 0 with empty stdout (no contract JSON), which masked the success; a retry created a second instance at the same offer. The 36908259 instance was destroyed before any environment setup ran. No code or data was placed on it. | 1 |
| Duplicate-create artefact: second retry of 'vastai create instance 34391260' after the silent first success. Destroyed before any environment setup ran. No code or data was placed on it. | 1 |
| Vast.ai create-instance API responded with empty stdout/exit 0 for the first call but created a duplicate instance shortly afterwards (37106446); both 37106446 and 37106453 were created from the same offer ID. 37106446 was destroyed via the API (returned 404 'Instance not found' on destroy probe -- it was already removed Vast.ai-side, likely a transient phantom from the create-instance race). | 1 |
| SSH authentication rejected the registered key (id 801863 with comment 'shefuniad\md1avn@TEN00BE4360B45A'). After 5 retries on ssh4.vast.ai:26452 (proxy) and one attempt on 76.64.86.119:47399 (direct), all 6 returned 'Permission denied (publickey)' despite the key being attached to the instance per Vast.ai API. Root cause: the literal backslash in the key comment field appears to corrupt key parsing in the Vast.ai SSH proxy (the key was stored with double-escaped backslash 'shefuniad\\md1avn'). Resolution: registered a new SSH key entry (id 855344) using the same key material but a clean ASCII comment 'md1avn-t0113', attached to the next instance, and SSH connected successfully on the first attempt. | 1 |

## Tasks

| Task | Machines | Cost (USD) | Failed | GPUs |
|------|----------|------------|--------|------|
| [`t0076_bedb_dsi_firing_rate_mobo`](../../overview/tasks/task_pages/t0076_bedb_dsi_firing_rate_mobo.md) | 1 | $1.06 | 0 | Quadro P4000 |
| [`t0078_bedb_mobo_v2_ais_tiered_ahp`](../../overview/tasks/task_pages/t0078_bedb_mobo_v2_ais_tiered_ahp.md) | 1 | $3.93 | 1 | RTX 5060 Ti (idle, unused) |
| [`t0080_bedb_mobo_v3_dendritic_spike_nsga2`](../../overview/tasks/task_pages/t0080_bedb_mobo_v3_dendritic_spike_nsga2.md) | 1 | $0.75 | 1 | RTX PRO 4000 (idle, unused) |
| [`t0081_bedb_v3_warmstart_nsga2`](../../overview/tasks/task_pages/t0081_bedb_v3_warmstart_nsga2.md) | 1 | $2.39 | 0 | RTX PRO 4000 (idle, unused) |
| [`t0083_bedb_v3_extend_nsga2_gen8plus`](../../overview/tasks/task_pages/t0083_bedb_v3_extend_nsga2_gen8plus.md) | 1 | $5.83 | 0 | RTX 4060 Ti (idle, unused) |
| [`t0086_robustness_cluster_bio_comparison`](../../overview/tasks/task_pages/t0086_robustness_cluster_bio_comparison.md) | 1 | $1.59 | 1 | (idle, unused; CPU-only NEURON workload) |
| [`t0091_morphology_extended_nsga2_v1`](../../overview/tasks/task_pages/t0091_morphology_extended_nsga2_v1.md) | 1 | $0.65 | 0 | RTX PRO 4000 (idle, unused; CPU-only NEURON workload) |
| [`t0099_random_init_pareto_robustness`](../../overview/tasks/task_pages/t0099_random_init_pareto_robustness.md) | 1 | $7.71 | 1 | RTX 5060 Ti (idle, unused; CPU-only NEURON workload) |
| [`t0102_seedscale_n4_gen20`](../../overview/tasks/task_pages/t0102_seedscale_n4_gen20.md) | 1 | $12.07 | 0 | RTX 4090 (idle, unused; CPU-only NEURON workload) |
| [`t0104_nsga2_2obj_dsi_pdrate_3seeds`](../../overview/tasks/task_pages/t0104_nsga2_2obj_dsi_pdrate_3seeds.md) | 1 | $10.30 | 0 | RTX 3060 Ti (idle, unused; CPU-only NEURON workload) |
| [`t0106_long_pdnd_nsga2_300gen`](../../overview/tasks/task_pages/t0106_long_pdnd_nsga2_300gen.md) | 1 | $10.37 | 2 | RTX 5060 Ti (idle, unused; CPU-only NEURON workload) |
| [`t0112_t0106_seed77_replicate`](../../overview/tasks/task_pages/t0112_t0106_seed77_replicate.md) | 1 | $1.99 | 0 | RTX 3090 (idle, unused; CPU-only NEURON workload) |
| [`t0113_t0106_seed2247_replicate`](../../overview/tasks/task_pages/t0113_t0106_seed2247_replicate.md) | 1 | $0.43 | 2 | RTX 4060 Ti (idle, unused; CPU-only NEURON workload) |
