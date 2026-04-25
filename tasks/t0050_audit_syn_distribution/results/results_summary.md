# Results Summary: Synapse-Distribution Audit (Deposited DSGC vs Paper)

## Summary

Confirms t0049's spatial-distribution hypothesis (H1) at both the structural and numerical levels:
the deposited ModelDB 189347 PD/ND condition swap is implemented as a pure scalar
`gabaMOD = 0.33 + 0.66*direction` applied uniformly to ALL 282 SAC inhibitory synapses with NO
spatial threshold. The underlying synapse spatial distribution is symmetric around the synapse
population's own median (count_pd / count_nd = 139 / 143 = 0.972, within the [0.9, 1.1] symmetric
band). The deposited code therefore cannot produce the paper's somatic GABA PD/ND asymmetry — the
t0049 SEClamp symmetry collapse (PD = 47.47, ND = 48.04 nS) is the direct mechanical consequence of
(1) a non-spatial gabaMOD protocol and (2) a spatially-symmetric underlying SAC inhibitory synapse
distribution.

## Metrics

* **Per-channel synapse counts**: BIPsyn = SACexcsyn = SACinhibsyn = **282** synapses each. All
  three channels share identical parent sections per index (asserted in the extraction wrapper).
* **Side-a vs side-b at synapse-population median midline (x = 88.77 µm)**: **139 / 143** (ratio
  **0.972**, symmetric per [0.9, 1.1] threshold).
* **Side-a vs side-b at soma_x midline (x = 104.58 µm)**: **171 / 111** (ratio **1.541**,
  asymmetric — but this is the soma being off-center within the dendritic field, not a genuine
  PD/ND distribution asymmetry).
* **Per-side density at synapse-median midline**: **0.060 / 0.062 synapses/µm** (essentially
  identical density per side).
* **Mean radial distance from soma**: side_a 69.08 +/- 21.56 µm, side_b 48.00 +/- 23.90 µm.
  Slightly larger reach on side_a (the dendritic side opposite the soma's offset).
* **Mean path distance from soma along cable**: side_a 140.95 +/- 40.38 µm, side_b 103.09 +/- 47.84
  µm. Same offset pattern.
* **Total dendritic length per side**: side_a 2311 µm, side_b 2296 µm (essentially identical;
  total dendritic length 4607 µm).
* **H1 verdict**: **SUPPORTED** on both structural (no spatial PD/ND threshold in protocol) and
  numerical (synapse distribution symmetric around its own median, density per side identical)
  grounds.
* **Bonus finding**: NEURON 8.2.7 Python's legacy `h.distance(0, sec(0.5))` form does NOT reliably
  set the path-distance origin. The audit uses the more robust two-segment form
  `h.distance(soma_seg, syn_seg)` instead — flagged for other DSGC tasks computing path distances.

## Verification

* `verify_task_file.py` — PASSED (0 errors)
* `verify_task_metrics.py` — PASSED (0 errors) on `metrics.json = {}` (no registered metrics apply
  to a static-coordinate audit; documented in plan)
* `verify_plan.py` — PASSED (0 errors)
* `verify_research_code.py` — PASSED (0 errors)
* `ruff check`, `ruff format`, `mypy -p tasks.t0050_audit_syn_distribution.code` — clean across
  all 4 Python modules
* Synapse-count assertion (282 per channel): PASSED
* Parent-section identity per index (BIPsyn[i].section == SACexcsyn[i].section ==
  SACinhibsyn[i].section): PASSED
