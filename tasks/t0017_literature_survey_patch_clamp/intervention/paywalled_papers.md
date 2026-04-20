# Paywalled Papers - t0017_literature_survey_patch_clamp

Papers cited as essential for the patch-clamp / voltage-clamp dissection / space-clamp survey but
not retrievable via automated download. Each needs researcher action to retrieve the full PDF
through institutional access (Sheffield) and drop the file into the asset's `files/` directory.

## How to resolve

For each DOI below:

1. Open the paper landing page via your institutional proxy
2. Download the PDF
3. Save the PDF as
   `tasks/t0017_literature_survey_patch_clamp/assets/paper/<paper_id>/files/<first_author>_<year>_<slug>.pdf`
4. Update `details.json` in the same folder: set `download_status` to `"success"`, clear
   `download_failure_reason` to `null`, and append the filename to `files`.

## Paywalled DOIs

| # | DOI | Paper | Venue | Why paywalled |
| --- | --- | --- | --- | --- |
| 1 | `10.1371/journal.pone.0019463` | Poleg-Polsky & Diamond 2011 "Imperfect Space Clamp Permits Electrotonic Interactions between Inhibitory and Excitatory Synaptic Conductances, Distorting Voltage Clamp Recordings" | PLoS ONE | Open access on PLoS ONE but PDF not downloaded in this task run; manual browser fetch will succeed without institutional access |
| 2 | `10.1016/j.neuroscience.2021.08.024` | To, Honnuraiah, Stuart 2022 "Voltage Clamp Errors During Estimation of Concurrent Excitatory and Inhibitory Synaptic Input to Neurons with Dendrites" | Neuroscience (Elsevier) | Elsevier ScienceDirect paywall / cookie wall on automated fetchers; Sheffield institutional access required |
| 3 | `10.1126/sciadv.abb6642` | Werginz, Raghuram, Fried 2020 "Tailoring of the axon initial segment shapes the conversion of synaptic inputs into spiking output in OFF-alpha T retinal ganglion cells" | Science Advances | Nominally open access on Science Advances but the publisher PDF endpoint is protected by an AAAS/Cloudflare bot challenge returning an interstitial HTML page |
| 4 | `10.1016/j.neuron.2017.09.058` | Sethuramanujam et al. 2017 "Silent NMDA Synapses Enhance Motion Sensitivity in a Mature Retinal Circuit" | Neuron (Cell Press) | Cell Press paywall / cookie wall on automated fetchers; Sheffield institutional access required |
| 5 | `10.1523/jneurosci.0130-07.2007` | Margolis & Detwiler 2007 "Different Mechanisms Generate Maintained Activity in ON and OFF Retinal Ganglion Cells" | J Neurosci | Society for Neuroscience paywall with Cloudflare interstitial on the direct publisher PDF URL; Sheffield institutional access required |

## Priority

All five are essential for DSGC compartmental-model calibration against patch-clamp data. Priorities
for retrieval:

1. **PolegPolsky2011** - quantifies the space-clamp error bound for passive dendrites; directly
   constrains how published voltage-clamp E/I traces should be used as model-fitting targets.
2. **To2022** - extends PolegPolsky2011 to active dendrites; directly constrains error estimates
   when matching simulated voltage-clamp output to experimental traces in DSGC models with
   voltage-gated dendritic channels.
3. **Sethuramanujam2017** - provides quantitative AMPA/NMDA charge ratios during preferred and null
   motion in DSGCs; primary experimental target for DSGC synaptic-receptor complement in the model.
4. **Werginz2020** - provides AIS length, Nav1.6 density, and depolarisation-block thresholds for
   alpha-type RGCs; constrains DSGC AIS compartment parameters.
5. **MargolisDetwiler2007** - distinguishes synaptic from intrinsic drive of RGC maintained
   activity; constrains whether DSGC resting activity should be modelled as pacemaker-like or
   synaptically-driven.

## Notes

Summaries for all five papers have been written using Crossref metadata abstracts (where available)
and training knowledge of the patch-clamp / voltage-clamp / space-clamp / DSGC literature. Each
Overview section carries an explicit disclaimer that the content has not been verified against the
actual PDF. Full-text retrieval will let a follow-up task verify and refine the summaries and
numerical claims (e.g., "~80% signal loss on thin distal dendrites", "7x AIS-to-soma Na+ density
ratio") against the actual paper contents.
