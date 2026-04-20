# Results Summary: Calibrate Dendritic Diameters

## Summary

Replaced the uniform **0.125 µm** placeholder radius on every compartment of
`dsgc-baseline-morphology` with a Poleg-Polsky & Diamond 2016 per-Strahler-order taper, registered
as the new dataset asset `dsgc-baseline-morphology-calibrated`. Topology is preserved byte-for-byte
(**6,736** compartments, **129** branch points, **131** leaves, **1,536.25 µm** dendritic length)
while total dendritic surface area grows **7.99x** and total dendritic axial resistance drops to
**~4.8%** of the placeholder baseline.

## Metrics

* **Distinct radii (calibrated)**: 4 — soma **4.118 µm**, primary **3.694 µm** (Strahler order
  5), mid **1.653 µm** (orders 2-4), terminal **0.439 µm** (order 1)
* **Max Strahler order**: 5 (max-child tie-break, 33 order-5 compartments, 3,915 terminals)
* **Terminal clamps at 0.15 µm floor**: **0** (Poleg-Polsky terminal mean is 2.9x the floor)
* **Surface area**: placeholder **1,213.43 µm²** -> calibrated **9,700.10 µm²** (**+7.99x**)
* **Dendritic axial resistance**: placeholder **3.13e10 Ohm** -> calibrated **1.50e9 Ohm**
  (**4.79%**, a **20.9x** drop)
* **Proximal input resistance**: placeholder **90.8 MOhm** -> calibrated **0.52 MOhm**
* **Topology integrity**: 6,736 / 6,736 compartments, 129 / 129 branch points, 131 / 131 leaves,
  1,536.254 µm vs target 1,536.25 µm (delta < 1e-3 µm)

## Verification

* `pytest tasks/t0009_calibrate_dendritic_diameters/code/ -v` — PASSED (6/6 topology-equality
  tests, plan Verification Criteria gate 1)
* Radius sanity check (>= 3 distinct radii, min >= 0.15 µm) — PASSED (4 distinct radii, min
  **0.439 µm** dendrite / **4.118 µm** soma)
* Per-order outputs present check — PASSED (`per_order_radii.csv`,
  `per_branch_axial_resistance.csv`, three PNGs in `results/images/`)
* Dataset asset structural check — PASSED (`spec_version="2"`, `source_paper_id` cites
  Poleg-Polsky 2016, exactly one SWC file)
* `verify_task_results` — run by orchestrator after this step
