# Results Summary: Download candidate DSGC morphology

## Summary

Downloaded the Feller-lab ON-OFF mouse DSGC reconstruction `141009_Pair1DSGC` (NeuroMorpho neuron
102976\) from Morrie & Feller-associated archives as a CNG-curated SWC, validated the compartment
tree with a stdlib Python parser, and registered it as the project's baseline DSGC dataset asset
`dsgc-baseline-morphology` (v2 spec-compliant). The morphology is now the single reconstructed cell
that every downstream compartmental-modelling task in this project will load.

## Metrics

* **Compartments**: **6,736** (19 soma, 6,717 dendrite, 0 axon)
* **Branch points (≥2 children)**: **129**
* **Leaf tips**: **131**
* **Total dendritic path length**: **1,536.25 µm**
* **SWC file size**: **232,470 bytes** (CNG-curated)
* **Download cost**: **$0** (CC-BY-4.0 public data)

## Verification

* `verify_task_folder.py` — PASSED (0 errors, 1 warning: `FD-W002` empty `logs/searches/` —
  expected for a download-dataset task).
* `verify_plan.py` — PASSED (0 errors, 0 warnings).
* `verify_task_dependencies.py` — PASSED (0 errors, 0 warnings) during check-deps.
* Manual `DA-*` spec-v2 check on `assets/dataset/dsgc-baseline-morphology/` — PASSED (0 errors, 0
  warnings). The framework's `verify_dataset_asset.py` script is not implemented, so the check was
  done by applying each rule from `meta/asset_types/dataset/specification.md` directly.
* Stdlib SWC tree check in `code/validate_swc.py` — emitted `VALID` (single root, connected tree,
  non-negative radii, ≥1 soma, 6,717 ≥ 100 dendrite compartments).
