# Brainstorm results session 5

Brainstorming session 5 covering project state after the t0024 de Rosenroll 2026 DSGC port merged in
PR #23. The research environment now contains four DSGC compartmental-model ports
(`modeldb_189347_dsgc`, `modeldb_189347_dsgc_gabamod`, `modeldb_189347_dsgc_channel_testbed`,
`de_rosenroll_2026_dsgc`) all sharing the t0004 target tuning-curve envelope and the t0012
tuning-curve scoring library. The session answered the researcher's three inline questions
(effective model count, why t0022 returns DSI = 1, HWHM definition, individual stimulus length and
firing-rate window) and then planned a single concrete next experiment.

## Decision

Create **one** new experimental task (`t0026`): sweep the resting potential of the t0022 and t0024
ports from `-90 mV` to `-20 mV` in `10 mV` steps, holding both `v_init` and `eleak` together to the
sweep value (true resting-potential shift, not just initial-condition tweak), and report the
resulting tuning curves in polar coordinates.

## Context captured for the next task

* t0022 driver uses deterministic per-dendrite E-I scheduling; a single trial per angle is adequate.
  Total: 1 trial × 12 angles × 8 V_rest values = 96 trials (~25 min wall time).
* t0024 driver uses AR(2)-correlated stochastic release; keep 10 trials per angle to retain
  trial-to-trial variance. Total: 10 trials × 12 angles × 8 V_rest values = 960 trials (~4 h wall
  time).
* Both ports already return tuning curves via the t0012 `tuning_curve_loss` API; the sweep only
  varies `v_init` and `eleak` at driver setup.
* Expected assets: 2 predictions assets (one per model) plus polar-coordinate plots per V_rest plus
  overlay plots per model.

No new suggestions created, no suggestion rejections or reprioritizations this session — the focus
was a single researcher-directed experiment rather than backlog pruning.
