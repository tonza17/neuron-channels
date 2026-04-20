# Pass A: ModelDB Full Sweep (2026-04-20)

## Queries executed

1. `https://modeldb.science/ModelList?search=direction+selective`
2. `https://modeldb.science/ModelList?id=270` (category browse: Retina ganglion GLU cell)
3. `https://modeldb.science/ModelList?search=DSGC`
4. `https://modeldb.science/ModelList?search=starburst`
5. `https://modeldb.science/ModelList?search=retina`
6. `https://modeldb.science/ModelList?search=amacrine`
7. `https://modeldb.science/ModelList?search=ganglion`
8. `https://modeldb.science/ModelList?search=retinal+ganglion`
9. `https://modeldb.science/ModelList?search=RGC`
10. `https://modeldb.science/ModelList?search=direction`
11. `https://modeldb.science/ModelList?search=motion`
12. Direct GETs of ModelDB entries 189347, 223890, 267391, 267646, 2018247, 262452, 2019896, 260653,
    18501 to verify metadata.

## Candidates catalogued

| Accession | Title | First author | Year | Simulator | DSGC? | Relevance |
| --- | --- | --- | --- | --- | --- | --- |
| 189347 | Multiplication by NMDA receptors in Direction Selective Ganglion cells | Poleg-Polsky & Diamond | 2016 | NEURON | YES (ON-OFF mouse DSGC) | Already ported by t0008. The canonical DSGC compartmental model. |
| 223890 | Species-specific wiring for direction selectivity | Ding et al. | 2016 | NeuronC | NO (SAC network, not DSGC) | t0002 corpus; out of scope for a DSGC port. |
| 267391 | 3D population model of midget retinal ganglion cells at the human fovea | Italiano et al. | 2022 | NEURON | NO (midget RGC, electrical stimulation) | Adjacent — NEURON RGC models with morphology, no DS. |
| 267646 | Biophysically Realistic Network Model of the Wild-Type and Degenerate Retina | Ly et al. | 2022 | NEURON | UNCLEAR — includes ON/OFF RGCs but DS not mentioned | Worth checking code to see whether any ON-OFF DSGC cell class is in the network. |
| 2018247 | Virtual Human Retina | Ly et al. | 2025 | NEURON | NO (midget + parasol, no DSGC) | Post-2020 NEURON retina network model; no DSGC. |
| 262452 | Gap junction network of Amacrine Cells controls Nitric Oxide release | Jacoby et al. | 2018 | MATLAB + NEURON | NO (nNOS-1 amacrine cell, not SAC/DSGC) | Adjacent amacrine-cell work. |
| 2019896 | Inner retina pathological spontaneous oscillation | Horie et al. | 2025 | NEURON | NO (bipolar + AII + RGC, no DS) | Degeneration-oscillation model, not DS. |
| 260653 | Retinal ganglion cells responses and activity | Tsai et al. / Guo et al. | 2012 / 2016 | NEURON | NO (generic RGC, electrical stimulation) | Adjacent — non-DS RGC. |
| 156781 | Bursting and oscillations in RD1 Retina driven by AII Amacrine Neuron | Choi et al. | 2014 | Unspec | NO (AII + network) | Adjacent. |
| 150240 | Thalamocortical Convergence | Behuret et al. | 2013 | - | NO | Out of scope (thalamocortical, not retina). |
| 124063 | A network model of the vertebrate retina | Publio et al. | 2009 | - | NO | Pre-2010 retina network; no DSGC. |
| 125378 | Availability of low-threshold Ca2+ current in retinal ganglion cells | Lee SC et al. | 2003 | - | NO | Single-channel RGC study; adjacent to [Fohlmeister2010]. |
| 225095 | COREM: configurable retina simulator | Martinez-Canada et al. | 2016 | Custom | NO | Rate-coded retina simulator — out of the compartmental inclusion bar. |
| 267026 | M1 and M4 intrinsically photosensitive retinal ganglion cells | Stinchcombe et al. | 2021 | - | NO (ipRGC) | Adjacent; non-DS subtype. |
| 188423 | Microsaccades and synchrony coding in the retina | Masquelier et al. | 2016 | - | NO | Rate-coded. |
| 154192 | Nonlinear neuronal computation based on physiologically plausible inputs | McFarland et al. | 2013 | - | NO | Out of scope. |
| 141062 | STDP orientation selectivity in V1 | Masquelier 2012 | 2012 | - | NO | Out of scope (V1, not retina). |
| 3488 | Retinal Ganglion Cell: I-A | Benison et al. | 2001 | - | NO | Single-channel RGC study. |
| 3457 | Retinal Ganglion Cell: I-CaN and I-CaL | Benison et al. | 2001 | - | NO | Single-channel RGC study. |
| 3491 | Retinal Ganglion Cell: I-K | Skaliora et al. | 1995 | - | NO | Single-channel RGC study. |
| 3483 | Retinal Ganglion Cell: I-Na,t | Benison et al. | 2001 | - | NO | Single-channel RGC study. |
| 50997 | Ribbon Synapse | Sikora et al. | 2005 | - | NO | Pre-synaptic only. |
| 18501 | Salamander retinal ganglion cells: morphology influences firing | Sheasby, Fohlmeister | 1999 | NEURON | NO (generic salamander RGC) | Not DS-specific. |
| 3673 | Salamander retinal ganglion cell: ion channels | Fohlmeister, Miller | 1997 | - | NO | Single-channel fit. |
| 244202 | Biophysical model of vestibular ganglion neurons | Hight & Kalluri | 2016 | - | NO | Vestibular, not retinal. |
| 190261 | Dorsal root ganglion (DRG) neurons | Rho & Prescott | 2012 | - | NO | Off-target. |
| 691 | E-I-E direction-selective motion discrimination visual cortex traveling waves | Heitmann | 2020 | - | NO (V1, not retina) | Cortex, not retina. |

## Verdict for Pass A

ModelDB contains exactly **one** DSGC compartmental model matching this project's inclusion bar:
189347 (Poleg-Polsky & Diamond 2016), already ported as `modeldb_189347_dsgc` by t0008.

One **possibly adjacent** model needs a closer look: 267646 (Ly et al. 2022), which includes ON/OFF
RGCs in a whole-retina network but does not advertise direction selectivity. A post-2020 network
model of this size could include a DSGC cell class in its code even if its paper does not foreground
that class.

**Everything else** on ModelDB is either (a) already in the t0002 corpus / ported by t0008, (b) a
single-channel RGC study feeding Fohlmeister-style kinetics, (c) an ipRGC / midget / parasol /
salamander RGC model without direction selectivity, or (d) off-target (V1, vestibular, DRG).

The Ding 2016 NeuronC SAC network (223890) is confirmed to remain out of this task's scope because
NeuronC → NEURON rewriting is outside the automatic-port bar agreed in `research_papers.md`.
