---
spec_version: "2"
answer_id: "nav-kv-combinations-for-dsgc-modelling"
answered_by_task: "t0019_literature_survey_voltage_gated_channels"
date_answered: "2026-04-20"
---
## Question

What quantitative priors does the voltage-gated-channels literature supply for the DSGC
compartmental model on (1) Nav subunit localisation at the RGC AIS, (2) Kv1 subunit expression at
the AIS, (3) RGC HH-family kinetic rate functions, (4) Nav1.6 vs Nav1.2 subunit co-expression
kinetics, and (5) Nav conductance density at the AIS?

## Answer

RGC AIS Nav subunits segregate into microdomains with Nav1.6 concentrated distally and Nav1.2
enriched proximally, and Kv1.1/Kv1.2 co-localising with Nav1.6 in the distal AIS. AIS-localised Kv1
channels activate near threshold (V_half around -40 to -50 mV) with sub-millisecond kinetics and
control AP waveform and somatic repolarisation. The Fohlmeister-Miller RGC HH kinetics provide
canonical alpha/beta rate functions for Nav and Kv at 22 degC with Nav activation V_half near -40 mV
and a Q10 near 3 for warming to 37 degC. Nav1.6 activates about 10-15 mV more negative than Nav1.2,
so distal Nav1.6 initiates the AP while proximal Nav1.2 supports backpropagation into the soma. Peak
AIS Nav conductance density is about 2500-5000 pS/um2 (roughly 50x somatic density), an
order-of-magnitude prior essential for reproducing fast, reliable AP initiation in compartmental
models.

## Sources

* Paper: `10.1002_cne.21173` (Van Wart, Trimmer, Matthews 2006)
* Paper: `10.1016_j.neuron.2007.07.031` (Kole, Letzkus, Stuart 2007)
* Paper: `10.1152_jn.1997.78.4.1948` (Fohlmeister & Miller 1997)
* Paper: `10.1038_nn.2359` (Hu, Tian, Li, Shu et al. 2009)
* Paper: `10.1038_nn2040` (Kole, Ilschner, Kampa, Williams et al. 2008)
