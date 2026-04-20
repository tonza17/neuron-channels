# Paywalled Papers - t0019_literature_survey_voltage_gated_channels

Papers cited as essential for the voltage-gated-channels survey but not retrievable via automated
download. Each needs researcher action to retrieve the full PDF through institutional access
(Sheffield) and drop the file into the asset's `files/` directory.

## How to resolve

For each DOI below:

1. Open the paper landing page via your institutional proxy
2. Download the PDF
3. Save the PDF as
   `tasks/t0019_literature_survey_voltage_gated_channels/assets/paper/<paper_id>/files/<first_author>_<year>_<slug>.pdf`
4. Update `details.json` in the same folder: set `download_status` to `"success"`, clear
   `download_failure_reason` to `null`, and append the filename to `files`.

## Paywalled DOIs

| # | DOI | Paper | Venue | Why paywalled |
| --- | --- | --- | --- | --- |
| 1 | `10.1002/cne.21173` | Van Wart, Trimmer, Matthews 2006 "Polarized distribution of ion channels within microdomains of the axon initial segment" | Journal of Comparative Neurology (Wiley) | Wiley publisher paywall; Sheffield institutional access required |
| 2 | `10.1016/j.neuron.2007.07.031` | Kole, Letzkus, Stuart 2007 "Axon initial segment Kv1 channels control axonal action potential waveform and synaptic efficacy" | Neuron (Cell Press / Elsevier) | Elsevier ScienceDirect paywall; Sheffield institutional access required |
| 3 | `10.1152/jn.1997.78.4.1948` | Fohlmeister & Miller 1997 "Impulse encoding mechanisms of ganglion cells in the tiger salamander retina" | Journal of Neurophysiology (American Physiological Society) | APS paywall for pre-2010 content; Sheffield institutional access required |
| 4 | `10.1038/nn.2359` | Hu, Tian, Li, Shu, Jonas, Shu 2009 "Distinct contributions of Na(v)1.6 and Na(v)1.2 in action potential initiation and backpropagation" | Nature Neuroscience | Nature / Springer Nature paywall; Sheffield institutional access required |
| 5 | `10.1038/nn2040` | Kole, Ilschner, Kampa, Williams, Ruben, Stuart 2008 "Action potential generation requires a high sodium channel density in the axon initial segment" | Nature Neuroscience | Nature / Springer Nature paywall; Sheffield institutional access required |

## Priority

All five are essential for DSGC compartmental-model voltage-gated-channel priors. Priorities for
retrieval:

1. **Kole2008** - canonical AIS Na+ conductance-density estimate; direct prior for the
   `na16_ais_gbar` parameter in the DSGC model.
2. **Hu2009** - Nav1.6 / Nav1.2 separation of AP initiation vs. backpropagation; kinetic priors for
   two Nav populations co-expressed in the RGC AIS.
3. **VanWart2006** - direct RGC-specific ion-channel microdomain mapping; Na+, Kv1, Kv2 subunit
   layout at the RGC AIS is the spatial template for DSGC AIS compartmentalisation.
4. **Fohlmeister1997** - RGC-specific Hodgkin-Huxley rate constants (alpha_m, beta_m, alpha_h,
   beta_h) validated against real RGC recordings; the canonical RGC HH kinetics for NEURON.
5. **Kole2007** - Kv1 kinetics at AIS; prior for AP shape and repolarisation in the DSGC AIS model.

## Notes

Summaries for all five papers have been written using Crossref metadata abstracts (where available)
and training knowledge of the voltage-gated-channel and RGC literature. Each Overview section
carries an explicit disclaimer that the content has not been verified against the actual PDF.
Full-text retrieval will let a follow-up task verify and refine the summaries and numerical claims
(Na+ conductance density at AIS, Nav1.6/Nav1.2 activation half-voltage split, Fohlmeister-Miller
alpha/beta coefficients, Kv1 time constants) against the actual paper contents.
