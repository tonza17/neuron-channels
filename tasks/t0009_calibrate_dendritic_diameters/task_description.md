# Calibrate dendritic diameters for dsgc-baseline-morphology

## Motivation

Every compartment in the downloaded `dsgc-baseline-morphology` CNG-curated SWC (NeuroMorpho neuron
102976, 141009_Pair1DSGC) carries the placeholder radius **0.125 µm** because the original Simple
Neurite Tracer reconstruction did not record diameters. Cable theory predicts that segment diameter
is the single most influential *local-electrotonic* knob on axial resistance, spatial attenuation
and spike-initiation threshold, so leaving a uniform placeholder in place will silently bias every
downstream biophysical simulation. This task replaces the placeholder with a literature-derived
order-dependent taper keyed on Strahler order or path distance from the soma, and registers the
calibrated morphology as a new dataset asset that downstream tasks (t0008 reproduction, t0011
visualisation smoke-test, and the experiment tasks) will load instead of the raw placeholder SWC.

Covers suggestion **S-0005-02**.

## Scope

1. **Research stage**: survey the published mouse ON-OFF DSGC morphometric literature for a
   defensible diameter taper rule. Candidate sources explicitly identified as plausible:
   * Vaney / Sivyer / Taylor 2012 review + original figures
   * Poleg-Polsky & Diamond 2016 (ModelDB 189347) per-order diameter profile
   * Other published Feller-lab / Briggman-lineage DSGC reconstructions with diameters recorded.
     Pick one primary source and one fallback source; document the choice and the per-order
     distribution in `research/research_papers.md`.
2. **Implementation**:
   * Parse the CNG-curated SWC with a stdlib parser (can reuse
     `tasks/t0005_download_dsgc_morphology/code/validate_swc.py` approach).
   * Compute per-compartment Strahler order and path distance from the soma.
   * Apply the chosen taper rule to assign a realistic radius to every dendritic compartment.
     Preserve the 19 soma compartments' original (non-placeholder) radii.
   * Write the new SWC to `assets/dataset/dsgc-baseline-morphology-calibrated/files/`.
3. **Register** the calibrated morphology as a v2 dataset asset
   (`assets/dataset/dsgc-baseline-morphology-calibrated/`) with a `details.json`, a
   `description.md`, and the calibrated SWC file. The `details.json` must reference
   `dsgc-baseline-morphology` as the raw source and cite the chosen taper-source paper.
4. **Validation**:
   * Plot per-Strahler-order radius distributions (original placeholder vs calibrated) and save as
     PNG to `results/images/`.
   * Recompute total surface area and axial resistance per branch; report the change vs the
     placeholder baseline.
   * Confirm compartment count, branch points and connectivity are unchanged from the source SWC.

## Dependencies

* **t0005_download_dsgc_morphology** — source of `dsgc-baseline-morphology` raw SWC and the stdlib
  parser.

## Expected Outputs

* **1 dataset asset** (`assets/dataset/dsgc-baseline-morphology-calibrated/`) — calibrated SWC.
* Per-order diameter distribution plots in `results/images/` (original vs calibrated).
* Brief answer-style report embedded in `results/results_detailed.md` summarising the chosen taper
  rule, the rationale, and the change in surface area / axial resistance vs the placeholder.

## Questions the task answers

1. Which published taper source is most faithful for mouse ON-OFF DSGCs of the 141009_Pair1DSGC
   lineage?
2. What is the Strahler-order-to-radius (or path-distance-to-radius) mapping used in the
   calibration?
3. How does total dendritic surface area change from the placeholder baseline to the calibrated
   morphology?
4. How does axial resistance along the preferred-to-null dendritic axis change, and what does that
   predict for spike-attenuation at the soma?

## Risks and Fallbacks

* **No published source gives a cell-matched per-order taper**: fall back to the Poleg-Polsky
  ModelDB distribution and clearly label the calibrated asset as "Poleg-Polsky-profile calibrated"
  rather than "literature-grounded".
* **The chosen taper makes distal tips implausibly thin (< 0.1 µm)**: clamp the radius floor at 0.15
  µm and document the clamp.
* **Calibration collapses spatial detail (uniform assignment)**: treat as a bug, not a feature;
  re-derive the taper until per-order variability survives.
