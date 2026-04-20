# Paywalled Papers - t0018_literature_survey_synaptic_integration

Papers cited as essential for the synaptic-integration survey but not retrievable via automated
download. Each needs researcher action to retrieve the full PDF through institutional access
(Sheffield) and drop the file into the asset's `files/` directory.

## How to resolve

For each DOI below:

1. Open the paper landing page via your institutional proxy
2. Download the PDF
3. Save the PDF as
   `tasks/t0018_literature_survey_synaptic_integration/assets/paper/<paper_id>/files/<first_author>_<year>_<slug>.pdf`
4. Update `details.json` in the same folder: set `download_status` to `"success"`, clear
   `download_failure_reason` to `null`, and append the filename to `files`.

## Paywalled DOIs

| # | DOI | Paper | Venue | Why paywalled |
| --- | --- | --- | --- | --- |
| 1 | `10.1038/346565a0` | Lester, Clements, Westbrook, Jahr 1990 "Channel kinetics determine the time course of NMDA receptor-mediated synaptic currents" | Nature | Nature / Springer Nature paywall; Sheffield institutional access required |
| 2 | `10.1073/pnas.80.9.2799` | Koch, Poggio, Torre 1983 "Nonlinear interactions in a dendritic tree: localization, timing, and role in information processing" | PNAS | PNAS articles before 1995 are not fully open; PDF behind publisher endpoint protected against automated fetchers |
| 3 | `10.1038/nature02116` | Wehr & Zador 2003 "Balanced inhibition underlies tuning and sharpens spike timing in auditory cortex" | Nature | Nature / Springer Nature paywall; Sheffield institutional access required |
| 4 | `10.1016/s0959-4388(03)00075-8` | Hausser & Mel 2003 "Dendrites: bug or feature?" | Current Opinion in Neurobiology (Elsevier) | Elsevier ScienceDirect paywall / cookie wall on automated fetchers; Sheffield institutional access required |
| 5 | `10.1038/nature00931` | Euler, Detwiler, Denk 2002 "Directionally selective calcium signals in dendrites of starburst amacrine cells" | Nature | Nature / Springer Nature paywall; Sheffield institutional access required |

## Priority

All five are essential for DSGC compartmental-model synaptic-integration priors. Priorities for
retrieval:

1. **EulerDetwilerDenk2002** - direct substrate of DSGC direction selectivity at the SAC-to-DSGC
   synapse; quantitative SAC dendritic Ca2+ DS index is the primary experimental target for the DSGC
   inhibitory-asymmetry mechanism in the model.
2. **Lester1990** - canonical NMDAR kinetics and Mg2+ block parameters used as priors for AMPA/
   NMDA/GABA mechanisms in the DSGC model.
3. **KochPoggio1983** - analytical expressions for shunting inhibition geometry; directly
   parameterises the DSGC-model null-side-inhibition placement.
4. **WehrZador2003** - in-vivo voltage-clamp methodology and E-I lag prior; methodological template
   for DSGC voltage-clamp fitting and timing validation.
5. **HausserMel2003** - review with canonical lambda_DC bounds and dendritic-non-linearity
   compensation priors; overview of the active-vs-passive compensation literature.

## Notes

Summaries for all five papers have been written using Crossref metadata abstracts (where available)
and training knowledge of the synaptic-integration and retinal-neuroscience literature. Each
Overview section carries an explicit disclaimer that the content has not been verified against the
actual PDF. Full-text retrieval will let a follow-up task verify and refine the summaries and
numerical claims (NMDAR kinetic constants, lambda_DC for RGC dendrites, E-I lag distributions, SAC
DS index) against the actual paper contents.
