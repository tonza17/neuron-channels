---
spec_version: "2"
answer_id: "synapse-distribution-audit-deposited-vs-paper"
answered_by_task: "t0050_audit_syn_distribution"
date_answered: "2026-04-25"
---
# Synapse distribution audit: deposited DSGC vs Poleg-Polsky 2016

## Question

Does the deposited Poleg-Polsky 2016 DSGC's spatial distribution of NMDA, AMPA, and GABA synapses
match the paper's text descriptions, and does it explain the t0049 GABA PD/ND symmetry collapse
under somatic SEClamp?

## Answer

The spatial-distribution hypothesis (H1) is SUPPORTED on both structural and numerical grounds.
Structurally, the deposited PD/ND swap is a single uniform scalar `gabaMOD = 0.33 + 0.66*direction`
applied to every SAC inhibitory synapse with no spatial threshold, so the somatic SEClamp cannot
detect any spatial GABA asymmetry by construction. Numerically, all three channels (BIP, SACexc,
SACinhib) share identical parent sections and are spatially symmetric around the BIPsyn-locx median
(side_a/side_b = 0.972 at midline 88.77 μm) and only appear asymmetric (ratio 1.541) when split at
the off-center soma_x = 104.6 μm. Therefore the t0049 GABA PD ~47.5 / ND ~48.0 nS collapse is the
direct consequence of (1) a non-spatial gabaMOD protocol and (2) a symmetric underlying GABA
distribution, exactly as H1 predicts.

## Sources

* Task: `t0046_reproduce_poleg_polsky_2016_exact`
* Task: `t0047_validate_pp16_fig3_cond_noise`
* Task: `t0049_seclamp_cond_remeasure`
