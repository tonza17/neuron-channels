# Pass C: Google Scholar / bioRxiv Forward-Citation Walk (2026-04-20)

## Queries executed

1. `"Poleg-Polsky" 2025 OR 2026 direction-selective ganglion cell compartmental model NEURON`
2. `"deRosenroll" OR "Awatramani" 2024 2025 DSGC direction-selective NEURON compartmental model`
3. `Poleg-Polsky 2025 "Nature Communications" OR "nat commun" motion detection retinal direction selective ganglion cell`
4. `"Sethuramanujam" 2021 2022 2023 direction selective ganglion compartmental NEURON`
5. `biorxiv 2024 2025 2026 DSGC direction selective retinal ganglion cell compartmental NEURON model`
6. `"Wei Wei" retina DSGC 2022 2023 2024 compartmental model ganglion cell`
7. `"Park" OR "Demb" OR "Borghuis" DSGC direction selective retina 2022 2023 2024 2025 compartmental model`
8. `DSGC NEURON Arbor NetPyNE compartmental model 2024 2025 github retina direction selective`
9. `"RSME" "retinal stimulation modeling environment" direction-selective 2021 2022 compartmental NEURON`
10. `"Taylor" Oregon retina direction selective 2023 2024 2025 ganglion cell compartmental NEURON`
11. `"deRosenroll" "Cell Reports" 2026 "10.1016/j.celrep.2025.116833" synaptic microarchitecture`
12. `"10.1038/s41467-026-70288-4" Poleg-Polsky motion direction selective`

## Forward citations of the six seed papers

### Poleg-Polsky & Diamond 2016 (NMDA-receptors DSGC)

* **deRosenroll et al. 2026 Cell Reports** (DOI 10.1016/j.celrep.2025.116833) — directly cites the
  Poleg-Polsky 2016 NEURON model as the template for its own multi-compartmental ON-OFF DSGC. NEW
  candidate.
* **Poleg-Polsky 2026 Nat Commun** (DOI 10.1038/s41467-026-70288-4) — new compartmental-ish
  explorations of motion-detection primitives; self-citation. NEW candidate.
* **Fransen et al. 2021 eNeuro** (`ENEURO.0261-21.2021`, "Dendrite Morphology Minimally Influences
  the Synaptic Distribution..."). Cites Poleg-Polsky 2016 but is an imaging + statistical study
  without a new compartmental model. Adjacent; not a new model.
* **Tran-Van-Minh et al. 2025-2026** (Poleg-Polsky PNAS 2025 mapping paper, DOI
  10.1073/pnas.2515449122) — spatial-map / gene-expression study; cites Poleg-Polsky 2016; does not
  publish a new compartmental model.

### Schachter et al. 2010 (rabbit DSGC, NeuronC)

* **Sethuramanujam et al. 2021 Neuron** ("Direction selectivity in retinal bipolar cell axon
  terminals") — cites Schachter 2010 but models bipolar-terminal DS, not the DSGC itself. Adjacent.
* **Ankri et al. 2020 Curr Biol** — RSME / Rivlin-Etzion group, cites Schachter 2010 but builds a
  SAC-centric compartmental model (bioRxiv `2021.06.22.449374`, PLOS Comp Bio
  `10.1371/journal.pcbi.1009754`). **Out of scope** — SAC, not DSGC.
* No post-2020 NEURON rewrite of Schachter 2010 found. The gap identified in `research_papers.md`
  recommendation 7 (hand-porting Schachter from NeuronC) remains open.

### Park et al. 2014 (untuned excitation)

* **Awatramani / deRosenroll lineage** (Hanson 2019 → Jain 2020 → deRosenroll 2026) all cite it. No
  new DSGC compartmental model from Park / Demb / Borghuis post-2014 beyond the existing corpus.
* **Riccitelli et al. 2025** (Weizmann / Rivlin-Etzion) — data paper on DSGC motion-direction
  encoding, uses previously published rabbit recordings; no new compartmental model.

### Sethuramanujam et al. 2016 (ACh/GABA mixed transmission)

* **deRosenroll 2026 Cell Reports** — core citation; the 2026 paper is the direct compartmental
  follow-up. NEW candidate (same as above).
* **Sethuramanujam et al. 2021 Neuron** — BCT-DS study, adjacent.

### Hanson et al. 2019 (spatial-offset DSGC, NEURON)

* **Jain et al. 2020 eLife** — already in corpus (10.7554/eLife.52949).
* **deRosenroll et al. 2026 Cell Reports** — primary citing model.
* **geoffder/Spatial-Offset-DSGC-NEURON-Model** GitHub repo — already flagged as the Phase B
  carry-over.

### Jain et al. 2020 eLife

* **deRosenroll 2026 Cell Reports** cites heavily; no other post-2020 compartmental models built on
  top of it.
* **Ankri 2024 (OFF arbors asymmetry)** — Awatramani lab, anatomical, not a new compartmental model.

## Additional bioRxiv / preprint hits (2024-2026)

| Preprint | DOI / URL | Relevance | In scope? |
| --- | --- | --- | --- |
| Direction-selective RGCs encode motion direction uniformly (Riccitelli et al., bioRxiv 2025) | `2025.07.23.666360` | Information-theoretic analysis on rabbit recordings. No new compartmental model. | NO (out-of-scope analysis) |
| Semaphorin 6A in RGCs (bioRxiv 2023) | `2023.11.18.567662` | Developmental asymmetric-wiring mechanism paper. No compartmental model. | NO |
| Molecular/spatial ganglion-cell flatmounts (Riccitelli et al., bioRxiv 2024 → Neuron 2025) | `2024.12.15.628587` / `10.1016/j.neuron.2025.05.525` | Transcriptomic RGC atlas; mentions DSGCs but is not a model paper. | NO |
| RSME — Realistic retinal modeling (Ankri et al. 2022 PLOS Comp Bio) | `10.1371/journal.pcbi.1009754` | SAC-centric NEURON + Python framework; the DSGC in the model is a simple integrate-and-fire attached to the SAC output. Does include a compartmental SAC but not a compartmental DSGC matching the inclusion bar. | MARGINAL — tool of record, not a DSGC model |
| Machine learning motion primitives (Poleg-Polsky 2026 Nat Commun) | `10.1038/s41467-026-70288-4` | Explores ML-discovered motion-detection architectures with NEURON back-end. Code at `PolegPolskyLab/DS-mechanisms`. | YES — new DSGC compartmental model (same as Pass B HIGH PRIORITY entry) |
| Uncovering 'hidden' synaptic microarchitecture (deRosenroll et al. 2026 Cell Reports) | `10.1016/j.celrep.2025.116833` | ON-OFF DSGC NEURON compartmental model with distinct GABA and ACh inputs. Code at `geoffder/ds-circuit-ei-microarchitecture`. | YES — NEW DSGC compartmental model |

## Verdict for Pass C

The forward-citation walks of the six seed papers converge on the same two NEW DSGC compartmental
models already identified in Pass B:

1. **deRosenroll et al. 2026 Cell Reports** (`10.1016/j.celrep.2025.116833`) — ON-OFF DSGC NEURON
   compartmental model with GABA/ACh microarchitecture.
2. **Poleg-Polsky 2026 Nat Commun** (`10.1038/s41467-026-70288-4`) — ML-driven motion-primitive
   compartmental exploration.

Neither paper is currently in the project's corpus. Both have public NEURON + Python code in Pass
B's GitHub/Zenodo entries.

Adjacent but out-of-scope forward citations:
* **RSME** (Ankri 2022 PLOS Comp Bio) — strong framework hit; its DSGC is phenomenological, not
  compartmental, so it fails the inclusion bar. However, the *SAC* compartmental model inside RSME
  is highly relevant as presynaptic circuitry and should be noted as a potential integration target
  for future tasks.
* **Riccitelli 2025** — population motion-coding analysis, no new model.
* **Ankri 2024** — OFF-arbor asymmetry anatomy paper, no new model.

No pre-2020 DSGC compartmental model papers surfaced in forward-citation walks that are not already
in the corpus. The post-2020 gap noted in `research_papers.md` is closed by the two papers above; no
third DSGC compartmental model exists in the public literature as of 2026-04-20 that the project has
missed.
