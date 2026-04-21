# Session Log: t0025_brainstorm_results_5

## 2026-04-21 12:30 UTC — Session start

Researcher continued from `/loop` session that completed t0024 (PR #23 merged). Invoked
`/brainstorm` then gave a specific experimental directive rather than asking for broad backlog
review.

## 2026-04-21 12:30 UTC — Q&A preamble

Three researcher questions answered before brainstorming proper:

1. Model count — four DSGC ports (t0008, t0020, t0022, t0024).
2. Why DSI = 1 in t0022 — ND firing rate is exactly 0 Hz due to deterministic inhibitory lead.
   Defined HWHM (Half-Width at Half-Maximum).
3. Stimulus length — TSTOP_MS = 1000 ms; bar sweep ~240 ms; firing rate computed over full 1 s
   window (Hz).

## 2026-04-21 12:32 UTC — Task captured

Researcher directive: V_rest sweep of t0022 and t0024 from -90 to -20 mV in 10 mV steps, polar
coordinate output.

Clarifications agreed:

* Move both `v_init` and `eleak` to each sweep value (true V_rest shift).
* t0022 uses 1 trial × 12 angles × 8 V_rest; t0024 uses 10 trials × 12 angles × 8 V_rest.

## 2026-04-21 12:35 UTC — Follow-up task creation

`/create-task` invoked to produce `t0026` V_rest sweep task.
