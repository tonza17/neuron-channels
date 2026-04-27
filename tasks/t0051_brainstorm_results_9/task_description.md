# Brainstorm Session 9: From-Scratch Minimal DSGC Wave

Ninth brainstorming session. Run after the t0046–t0050 reproduction wave revealed that the
deposited Poleg-Polsky 2016 ModelDB 189347 code does not match the paper's Fig 3A-E claims (282 vs
177 synapses; per-channel conductances 6-9x over paper; DSI vs gNMDA peaks at 0.19 not the paper's
flat 0.30; spatially-symmetric SAC inhibition mechanically incapable of producing the paper's GABA
PD/ND asymmetry).

## Strategic Pivot

The researcher decided to step away from modifying the deposited code and from the t0022
channel-testbed lineage, and instead build a new minimal DSGC model from scratch on the project's
calibrated baseline morphology. The new model uses 100 excitatory and 100 inhibitory synapses,
position-gated AMPA-only excitation with classical EPSP kinetics, deRosenroll-style
direction-dependent inhibition, and standard Hodgkin-Huxley spike generation on soma + AIS only.
Because there are two natural ways to implement "deRosenroll-style direction-dependent inhibition"
(scalar `gabaMOD` per synapse vs true spatial PD/ND asymmetry), the researcher asked for both to be
implemented in two parallel tasks.

## Decisions

* **Create t0052** — minimal DSGC with scalar `gabaMOD = 0.33 + 0.66*(1-cos(theta-theta_ND))/2`
  per-synapse inhibition.
* **Create t0053** — minimal DSGC with spatial PD/ND-asymmetric inhibition; each I synapse fires
  only when `cos(theta_stim - theta_centrifugal_synapse) < 0` (centripetal-only firing).
* **Cancel t0042, t0043, t0044** — all `intervention_blocked` on the t0022 testbed; the
  reproduction wave reframes that substrate as non-canonical and the new minimal model supersedes
  their motivation.
* **Reprioritise six t0046–t0050 follow-up suggestions** from high to medium (S-0046-01,
  S-0046-03, S-0048-02, S-0049-02, S-0050-01, S-0050-02) — all become non-urgent now that the
  from-scratch model is the primary substrate.
* **Keep deferred** t0023, t0031, t0045 — none on critical path.

## Assets Produced

No assets in this brainstorm task. The two new tasks (t0052, t0053) will each produce a library
asset and an experiment-results bundle when executed.
