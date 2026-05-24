# Intervention: Vast.ai account balance is $0

## Problem

`vastai show user` reports balance = $0 on the configured Vast.ai account (1 May 2026 / 2026-05-24).

t0122 requires an EPYC instance to run the 2-objective NSGA-II (DSI vs cytoplasm volume) for
~6-12 hours. The brainstorm-23 plan budgeted $4-8 of the project's remaining $37.10 ARF
budget envelope; the per-task hard cap is $8.

Even though the project ARF budget tracker allows the spend, the upstream cloud account cannot
provision an instance with zero balance.

## Required Action

Top up the Vast.ai account by at least $10 (covers the $8 cap with margin for instance
startup / teardown costs).

Alternatives if Vast.ai top-up is not possible:

1. Switch to a different provider (Lambda Labs, RunPod, Paperspace) — would require porting
   the t0115 setup-remote-machine skill to the new provider.
2. Run the NSGA-II locally — slow (single-machine throughput ~24-48 hours); may exceed the
   wall-clock that was planned.
3. Cancel t0122 entirely and write a correction file in a future task or brainstorm session.

## Status

t0122 is blocked at the setup-machines step. Preflight (create-branch, check-deps,
init-folders, skip research-papers/internet) has not yet completed. Once Vast.ai is topped up,
re-run `execute-task t0122_dsi_cytoplasm_volume_nsga2` to resume from where it stopped (the
task branch exists at `task/t0122_dsi_cytoplasm_volume_nsga2`).

## Recorded By

Orchestrator during the brainstorm-23 wave-3 execution. The preceding tasks t0120 and t0121
merged successfully (PRs #147 and #148 on main).
