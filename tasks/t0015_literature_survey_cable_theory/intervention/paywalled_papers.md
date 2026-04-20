# Paywalled Papers — t0015_literature_survey_cable_theory

Papers cited as essential for the cable-theory / dendritic-filtering survey but not retrievable via
automated download. Each needs researcher action to retrieve the full PDF through institutional
access (Sheffield) and drop the file into the asset's `files/` directory.

## How to resolve

For each DOI below:

1. Open the paper landing page via your institutional proxy
2. Download the PDF
3. Save the PDF as
   `tasks/t0015_literature_survey_cable_theory/assets/paper/<paper_id>/files/<first_author>_<year>_<slug>.pdf`
4. Update `details.json` in the same folder: set `download_status` to `"success"`, clear
   `download_failure_reason` to `null`, and append the filename to `files`.

## Paywalled DOIs

| # | DOI | Paper | Venue | Why paywalled |
| --- | --- | --- | --- | --- |
| 1 | `10.1152/jn.1967.30.5.1138` | Rall 1967 "Distinguishing theoretical synaptic potentials computed for different soma-dendritic distributions of synaptic input" | J Neurophysiol (APS) | APS paywall, OpenAlex `is_oa: false` |
| 2 | `10.1098/rstb.1982.0084` | Koch, Poggio, Torre 1982 "Retinal ganglion cells: a functional interpretation of dendritic morphology" | Phil Trans R Soc B | Royal Society paywall, OpenAlex `is_oa: false` |
| 3 | `10.1038/382363a0` | Mainen & Sejnowski 1996 "Influence of dendritic structure on firing pattern in model neocortical neurons" | Nature | Springer Nature paywall, OpenAlex `is_oa: false` |
| 4 | `10.1126/science.289.5488.2347` | Taylor, He, Levick, Vaney 2000 "Dendritic Computation of Direction Selectivity by Retinal Ganglion Cells" | Science | AAAS paywall, OpenAlex `is_oa: false` |
| 5 | `10.1523/jneurosci.5346-03.2004` | Dhingra & Smith 2004 "Spike Generator Limits Efficiency of Information Transfer in a Retinal Ganglion Cell" | J Neurosci | OpenAlex flags `is_oa: true` but the publisher PDF URL is behind a Cloudflare bot challenge; manual browser download works |

## Priority

All five are classics in cable theory and DSGC biophysics. Priorities for retrieval:

1. **Taylor2000** — the single most important experimental constraint on DSGC modelling; needed to
   validate asymmetric-inhibition DS mechanism
2. **KochPoggio1982** — theoretical backbone of DSGC dendritic computation; needed to reproduce
   "on-the-path" shunting direction-selectivity mechanism
3. **Mainen1996** — justifies morphological fidelity requirement for DSGC compartmental models;
   provides `d_lambda` discretization reference
4. **Rall1967** — defines shape-index diagnostic used to validate compartmental models against
   somatic EPSP recordings
5. **Dhingra2004** — quantifies spike-generator information loss; needed to interpret DSGC
   spike-train predictions vs. graded-potential signal

## Notes

Summaries for all five papers have been written using Crossref/OpenAlex metadata and training
knowledge of the cable-theory and DSGC literature. Full-text retrieval will let a follow-up task
verify and refine the summaries against the actual paper content.
