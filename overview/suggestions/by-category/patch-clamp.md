# Suggestions: `patch-clamp`

2 suggestion(s) in category [`patch-clamp`](../../../meta/categories/patch-clamp/) **1 open**
(1 medium), **1 closed**.

[Back to all suggestions](../README.md)

---

## Medium Priority

<details>
<summary>📂 <strong>Reproduce the Park2014 mouse ON-OFF DSGC tuning-curve dataset
as a validation benchmark</strong> (S-0002-10)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0002-10` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0002_literature_survey_dsgc_compartmental_models`](../../../overview/tasks/task_pages/t0002_literature_survey_dsgc_compartmental_models.md) |
| **Source paper** | [`10.1523_JNEUROSCI.5017-13.2014`](../../../tasks/t0002_literature_survey_dsgc_compartmental_models/assets/paper/10.1523_JNEUROSCI.5017-13.2014/) |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/), [`direction-selectivity`](../../../meta/categories/direction-selectivity/), [`retinal-ganglion-cell`](../../../meta/categories/retinal-ganglion-cell/) |

Park2014 (paper 10.1523_JNEUROSCI.5017-13.2014) and Chen2009 (paper
10.1113_jphysiol.2008.161240) are the two papers that set the mouse ON-OFF DSGC RQ5 targets
(DSI 0.6-0.9, peak 40-80 Hz, HWHM 60-90 deg). Park2014 is available open-access. Digitise the
published tuning-curve figure(s) into a reusable dataset asset (angle in degrees, spike rate
in Hz, error bars, cell counts) so the model can be scored against measured data rather than
only against the analytic target in t0004. This gives the project a literature-grounded
validation benchmark distinct from the canonical analytic target. Recommended task types:
download-dataset, data-analysis.

</details>

## Closed

<details>
<summary>✅ <s>Literature survey: patch-clamp recordings of RGCs and DSGCs (target
~25 papers)</s> — covered by <a
href="../../../tasks/t0017_literature_survey_patch_clamp/"><code>t0017_literature_survey_patch_clamp</code></a>
(S-0014-03)</summary>

| Field | Value |
|---|---|
| **ID** | `S-0014-03` |
| **Kind** | dataset |
| **Date added** | 2026-04-19 |
| **Source task** | [`t0014_brainstorm_results_3`](../../../overview/tasks/task_pages/t0014_brainstorm_results_3.md) |
| **Source paper** | — |
| **Categories** | [`patch-clamp`](../../../meta/categories/patch-clamp/) |

Systematically survey patch-clamp recording literature relevant to validating DSGC
compartmental models. Target ~25 category-relevant papers covering somatic whole-cell
recordings of RGCs, voltage-clamp conductance dissections, space-clamp error analyses,
spike-train tuning-curve measurements, and in-vitro stimulus protocols. Exclude the 20 DOIs
already in the t0002 corpus. Output: paper assets + synthesis mapping each paper to the model
validation targets (AP rate, IPSC asymmetry, EPSP kinetics, null/preferred ratios).

</details>
