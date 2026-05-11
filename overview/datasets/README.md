# Datasets (4)

4 dataset(s).

**Browse by view**: By category: [`cable-theory`](by-category/cable-theory.md),
[`compartmental-modeling`](by-category/compartmental-modeling.md),
[`dendritic-computation`](by-category/dendritic-computation.md),
[`direction-selectivity`](by-category/direction-selectivity.md),
[`retinal-ganglion-cell`](by-category/retinal-ganglion-cell.md); [By date
added](by-date-added/README.md)

---

<details>
<summary>📂 <strong>Baden 2016 RGC direction-selective subset vv1</strong></summary>

| Field | Value |
|---|---|
| **ID** | `baden-2016-ds-cells` |
| **Year** | 2016 |
| **Authors** | Tom Baden, Philipp Berens, Katrin Franke, Miroslav Román Rosón, Matthias Bethge, Thomas Euler |
| **URL** | https://datadryad.org/dataset/doi:10.5061/dryad.d9v38 |
| **License** | CC0-1.0 |
| **Access** | public |
| **Size** | 1238 retinal ganglion / displaced amacrine cells from the 8 paper-authoritative DS-containing groups (G2/G6/G12/G13/G16/G25/G26/G29) of Baden 2016, one row per cell with functional traces (chirp 249 samples, moving-bar 32 samples, moving-bar by 8 directions 256 samples, colour 96 samples, RF temporal kernel 80 samples) and per-cell selectivity indices, soma area/volume, RF Gaussian fit, immuno (ChAT, GAD, melanopsin, SMI-32) and genetics (PV, PCP2) flags. NO per-cell IPL stratification depth and NO morphology in the Dryad release. |
| **Date added** | 2026-05-12 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0103_extract_baden_2016_ds_morphologies`](../../overview/tasks/task_pages/t0103_extract_baden_2016_ds_morphologies.md) |
| **Description** | [`description.md`](../../tasks\t0103_extract_baden_2016_ds_morphologies\assets\dataset\baden-2016-ds-cells\description.md) |
| **Summary** | Per-cell functional fingerprints (chirp, moving-bar, colour, RF) and metadata for 1,238 cells from the 8 paper-authoritative direction-selective groups of Baden et al. 2016. No morphologies — Baden 2016 is a functional dataset. |

</details>

<details>
<summary>📂 <strong>DSGC Baseline Morphology (141009_Pair1DSGC), Diameter-Calibrated
v1</strong></summary>

| Field | Value |
|---|---|
| **ID** | `dsgc-baseline-morphology-calibrated` |
| **Year** | 2026 |
| **Authors** | t0009_calibrate_dendritic_diameters |
| **URL** | — |
| **License** | CC-BY-4.0 |
| **Access** | public |
| **Size** | 6,736 compartments (19 soma + 6,717 dendrite), 129 branch points, 131 leaves, 1,536.25 um total dendritic length; Strahler-order-calibrated diameters from Poleg-Polsky & Diamond 2016 ModelDB 189347 (Hanson geoffder/Spatial-Offset-DSGC-NEURON-Model mirror). Four distinct radii: soma 4.118 um, primary 3.694 um, mid 1.653 um, terminal 0.439 um. |
| **Date added** | 2026-04-20 |
| **Categories** | [`compartmental-modeling`](../../meta/categories/compartmental-modeling/), [`dendritic-computation`](../../meta/categories/dendritic-computation/), [`cable-theory`](../../meta/categories/cable-theory/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0009_calibrate_dendritic_diameters`](../../overview/tasks/task_pages/t0009_calibrate_dendritic_diameters.md) |
| **Description** | [`description.md`](../../tasks\t0009_calibrate_dendritic_diameters\assets\dataset\dsgc-baseline-morphology-calibrated\description.md) |
| **Summary** | Diameter-calibrated mouse ON-OFF DSGC morphology: topology from dsgc-baseline-morphology, per-Strahler-order radii from Poleg-Polsky & Diamond 2016. |

</details>

<details>
<summary>📂 <strong>DSGC Baseline Morphology (Feller 141009_Pair1DSGC) v1.0</strong></summary>

| Field | Value |
|---|---|
| **ID** | `dsgc-baseline-morphology` |
| **Year** | 2018 |
| **Authors** | Benjamin L. Murphy-Baum, Marla B. Feller |
| **URL** | https://neuromorpho.org/neuron_info.jsp?neuron_name=141009_Pair1DSGC |
| **License** | CC-BY-4.0 |
| **Access** | public |
| **Size** | 6,736 compartments (19 soma, 6,717 dendrite, 0 axon) with 129 branch points and 131 leaves; ~1.54 mm total dendritic path length. CNG-standardized SWC, ~227 KB. |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../meta/categories/retinal-ganglion-cell/) |
| **Added by** | [`t0005_download_dsgc_morphology`](../../overview/tasks/task_pages/t0005_download_dsgc_morphology.md) |
| **Description** | [`description.md`](../../tasks\t0005_download_dsgc_morphology\assets\dataset\dsgc-baseline-morphology\description.md) |
| **Summary** | CNG-curated SWC reconstruction of a mouse ON-OFF direction-selective retinal ganglion cell from the Feller-lab NeuroMorpho.org archive (neuron 102976, 141009_Pair1DSGC), used as the baseline morphology for all downstream DSGC compartmental-modeling tasks in this project. |

</details>

<details>
<summary>📂 <strong>Target Direction Tuning Curve (synthetic) v1.0.0</strong></summary>

| Field | Value |
|---|---|
| **ID** | `target-tuning-curve` |
| **Year** | 2026 |
| **Authors** | Anton Nikolaev |
| **URL** | — |
| **License** | CC0-1.0 |
| **Access** | public |
| **Size** | 12 angles (30 deg spacing) with 20 synthetic noisy trials per angle = 12 mean rates and 240 per-trial rates. |
| **Date added** | 2026-04-19 |
| **Categories** | [`direction-selectivity`](../../meta/categories/direction-selectivity/) |
| **Added by** | [`t0004_generate_target_tuning_curve`](../../overview/tasks/task_pages/t0004_generate_target_tuning_curve.md) |
| **Description** | [`description.md`](../../tasks\t0004_generate_target_tuning_curve\assets\dataset\target-tuning-curve\description.md) |
| **Summary** | Synthetic cosine-raised-to-power direction tuning curve sampled at 12 angles with 20 noisy trials per angle, used as the canonical optimisation target for every later tuning-curve fit in this project. |

</details>
