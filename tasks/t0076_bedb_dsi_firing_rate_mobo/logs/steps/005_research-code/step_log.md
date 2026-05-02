---
spec_version: "3"
task_id: "t0076_bedb_dsi_firing_rate_mobo"
step_number: 5
step_name: "research-code"
status: "completed"
started_at: "2026-05-02T20:47:34Z"
completed_at: "2026-05-02T21:00:00Z"
---
## Summary

Spawned a /research-code subagent that produced research/research_code.md. Surfaced a major scope
reduction: t0074 already vendored BK/SK/Kv7 (3 of 7 new MODs); t0024 already includes the `cad`
calcium-pool mechanism. So t0076 only needs 4 truly new MODs (Kdr, HCN, CaL, CaT) plus 8
SUFFIX-renamed copies (5 from t0067 + 3 from t0074). Also identified `pyproject.toml` additions
(botorch, gpytorch, torch+cpu, pyarrow) and a CPU-only adaptation needed for the GPU-oriented
setup-remote-machine SKILL.md (this is the project's first Vast.ai run). Verifier PASSED with 0
errors and 0 warnings.

## Actions Taken

1. Ran prestep research-code.
2. Spawned a general-purpose subagent with the /research-code SKILL.md.
3. Subagent reviewed t0008, t0011, t0012, t0019, t0024, t0050, t0066, t0067, t0070, t0072, t0074.
4. Subagent identified ~700 LOC of reusable code and ~1,200 LOC of new code, plus the 4 new MODs.
5. Subagent ran verify_research_code via run_with_logs — PASSED.

## Outputs

* `research/research_code.md` (PASS verifier; reusable items table, new-code table, NEURON
  deployment-on-Vast.ai subsection)

## Issues

None blocking. Two scope tweaks vs the original task description:

* MOD vendoring scope reduces from 7 new (Kdr, KM, HCN, CaL, CaT, BK, SK) to 4 new (Kdr, HCN, CaL,
  CaT) because t0074 already provided BK/SK/Kv7 via its `dsgc_active_channel_pack` library. The
  total channel count (12) is unchanged.
* `cad` mechanism is already in t0024's library, no need to vendor separately. Task's Approach step
  2 is already satisfied at the dependency level.
* No prior Vast.ai usage in the project — setup-remote-machine SKILL is GPU-oriented and needs
  CPU-only adaptation (image `python:3.12-bookworm`, `num_gpus=0 cpu_cores>=64`, pip-install
  `neuron==8.2.7` Linux wheel). This will be the planning step's burden to spec.
