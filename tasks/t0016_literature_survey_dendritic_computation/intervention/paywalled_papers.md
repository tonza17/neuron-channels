# Paywalled Papers: t0016_literature_survey_dendritic_computation

Papers selected for the dendritic-computation survey but not retrievable via automated download.
Each needs researcher action to retrieve the full PDF through institutional access (Sheffield) and
drop the file into the asset''s `files/` directory.

## How to resolve

For each DOI below:

1. Open the paper landing page via your institutional proxy
2. Download the PDF
3. Save the PDF as
   `tasks/t0016_literature_survey_dendritic_computation/assets/paper/<paper_id>/files/<first_author>_<year>_<slug>.pdf`
4. Update `details.json` in the same folder: set `download_status` to `"success"`, change
   `download_failure_reason` to `null`, and append the filename to `files`.

## Paywalled DOIs

| # | DOI | Paper | Venue | Why paywalled |
| --- | --- | --- | --- | --- |
| 1 | `10.1038/35005094` | Schiller, Major, Koester, Schiller 2000 "NMDA spikes in basal dendrites of cortical pyramidal neurons" | Nature | Springer Nature paywall; PDF fetch returned 403 |
| 2 | `10.1038/nn1253` | Polsky, Mel, Schiller 2004 "Computational subunits in thin dendrites of pyramidal cells" | Nature Neuroscience | Springer Nature paywall; PDF fetch returned 403 |
| 3 | `10.1038/18686` | Larkum, Zhu, Sakmann 1999 "A new cellular mechanism for coupling inputs arriving at different cortical layers" | Nature | Springer Nature paywall; PDF fetch returned 403 |
| 4 | `10.1126/science.aan3846` | Bittner, Milstein, Grienberger, Romani, Magee 2017 "Behavioral time scale synaptic plasticity underlies CA1 place fields" | Science | AAAS paywall; PDF fetch returned 403 |
| 5 | `10.1146/annurev.neuro.28.061604.135703` | London and Hausser 2005 "Dendritic Computation" | Annual Review of Neuroscience | Annual Reviews paywall; PDF fetch returned 403 |

## Priority

All five papers are canonical sources for dendritic computation. Priorities for retrieval:

1. **LondonHausser2005** - the canonical review; verifies cross-cell-type quantitative claims
   (electrotonic length ranges, NMDA spike thresholds, shunting inhibition effect sizes) used across
   the answer synthesis
2. **Larkum1999** - BAC-firing mechanism; verifies Ca2+ plateau threshold (~-50 mV), duration (30-50
   ms), and 3-4 spike burst frequency numbers used in the answer
3. **Schiller2000** - NMDA-spike primary evidence; verifies the 40-50 mV NMDA plateau amplitude and
   tens-of-milliseconds duration
4. **Polsky2004** - on-branch vs off-branch dissociation; verifies the 150-300% supralinear boost
   and 4-8 clustered-input threshold
5. **Bittner2017** - behavioral-timescale plasticity; verifies the plus-or-minus 1-2 second BTSP
   window and plateau amplitude/duration (30-60 mV, 50-300 ms)

## Notes

Summaries for all five papers have been written using Crossref abstracts plus training knowledge of
the canonical treatment of each paper in the dendritic-computation literature. Four of the five
(Schiller2000, Polsky2004, Bittner2017, LondonHausser2005) have a full abstract in Crossref that is
quoted verbatim in the summary; Larkum1999 has no abstract in Crossref, and the summary is more
explicit about the training-knowledge basis. Full-text retrieval will let a follow-up task verify
and refine the summaries against the actual paper content, especially the quantitative values used
in the DSGC transferability answer.
