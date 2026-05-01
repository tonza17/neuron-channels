# Writeup of two standard DSGC model beds in HH-equation research-paper format

## Motivation

The project routinely runs experiments on two distinct DSGC model substrates:

* **Bed A — t0008 deposited Poleg-Polsky 2016 DSGC** (ModelDB 189347), used as the substrate for
  t0020 (gabaMOD-swap protocol), t0065 (EPSP/IPSP/FULL Vm protocol), t0067 (soma channel sweep),
  t0068 (Nav1.6 + Kv3 co-expression rescue), and t0069 (AIS-localised channel sweep).
* **Bed B — t0024 de Rosenroll 2026 DSGC port**, used as the substrate for t0066 (EPSP/IPSP/FULL Vm
  protocol on de Rosenroll cell).

A single canonical writeup of both beds — with the standard Hodgkin-Huxley membrane equation up
front and every conductance defined explicitly, plus the excitation and inhibition models for PD and
ND directions — does not exist in one place in the project. Each task references its substrate but
assumes prior familiarity. The user needs this writeup as both a self-contained report and as the
basis for a presentation; the writeup must therefore stand alone, be printable, and avoid implicit
assumptions about which task did what.

## Scope

* Two model beds, treated symmetrically: same section structure, same equation conventions, same
  level of detail.
* For each bed:
  1. **Cell morphology** — section list, lengths, diameters, electrotonic structure, and source of
     the morphology (deposited file, generated, scaled, etc.).
  2. **Membrane equation** — start with the canonical HH form and then enumerate every current term
     Iᵢ that appears in the model, with V_half, time constants, and gbar values where applicable.
     Use the same notation in both beds for cross-comparison.
  3. **Synaptic excitation in PD vs ND** — bipolar drive (AMPA + NMDA where present), Mg-block
     parameters, peak conductance, timing pattern, source of asymmetry between PD and ND.
  4. **Synaptic inhibition in PD vs ND** — SAC GABA model, spatial pattern, gabaMOD or equivalent
     direction-encoding mechanism, e_GABA, peak conductance, timing pattern.
* A short side-by-side comparison table at the end, summarising the headline differences (e.g.,
  number of compartments, presence of NMDA, AIS or no AIS, gabaMOD vs spatial inhibition).
* Output is a single research-paper-format document under
  `tasks/t0070_writeup_two_model_beds/results/results_detailed.md` plus a brief
  `results/results_summary.md` (per the standard task file structure).

## Approach

1. Read the t0008, t0020, t0024 task code (NEURON `.hoc`, MOD files, Python wrappers) and confirm
   every conductance with cited file/line references.
2. Read the t0065, t0066 protocol code to extract the exact PD vs ND encoding for each bed
   (gabaMOD-swap for bed A; whatever t0066 uses for bed B).
3. Cross-check against the original papers (Poleg-Polsky 2016 and de Rosenroll 2026) where available
   in the project's paper assets — but the canonical source for the writeup is the project's own
   ported code, not the original papers.
4. Write the document section by section, alternating per bed for parallel structure. Use LaTeX-
   style equations rendered as fenced inline blocks (GitHub markdown tolerates `$...$` math).
5. Include a small morphology diagram per bed (axial schematic of compartments, not 3D), saved as
   PNG under `results/images/`. Use NEURON's section topology to generate or hand-draw the
   schematic.
6. Cross-reference every quoted parameter back to a file path and (where stable) a line number, so
   the writeup is auditable.

## Expected outputs

* `results/results_detailed.md` — the full writeup, research-paper format, all mandatory sections
  from `arf/specifications/results_specification.md` plus the bed-by-bed equation blocks.
* `results/results_summary.md` — 2-3 paragraph summary suitable as a presentation abstract.
* `results/images/bed_a_morphology.png`, `results/images/bed_b_morphology.png` — schematic
  morphology diagrams.
* `results/images/bed_a_synaptic_diagram.png`, `results/images/bed_b_synaptic_diagram.png` — PD vs
  ND excitation / inhibition timing diagrams.
* `results/metrics.json`, `results/costs.json`, `results/remote_machines_used.json` — standard
  bookkeeping (no external costs, no remote machines, no registered metrics produced).
* `results/suggestions.json` — follow-on tasks (e.g., a unified model-bed-runner library).

## Document format

Each bed section follows this template:

```markdown
## Bed X: <name>

### Morphology

* Compartment list with L (μm), diam (μm), nseg
* Electrotonic length and connectivity diagram

### Membrane equation

The Hodgkin-Huxley membrane equation governs each compartment:

C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj

where Iᵢ enumerates the active conductances:

I_Na    = g_Na · m³ · h · (V - E_Na)        -- HHst Na
I_K     = g_K  · n⁴   · (V - E_K)            -- HHst K (delayed rectifier)
I_Km    = g_Km · w    · (V - E_K)            -- HHst K_m
I_leak  = g_leak      · (V - E_leak)
... (one line per channel, with parameters in a separate table)

### Conductance table

| Channel | gbar (S/cm²) | E_rev (mV) | V_half_act (mV) | τ_m (ms) | V_half_inact (mV) | τ_h (ms) | Source |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... | ... | code/HHst.mod L<n> |

### Synaptic excitation (PD vs ND)

* AMPA: peak g_AMPA, τ_rise, τ_decay, E_rev = 0 mV
* NMDA: peak g_NMDA, τ_rise, τ_decay, Mg-block parameters, V_off
* Bipolar drive: timing of activations, spatial pattern across dendrites
* PD encoding: <how PD is set>
* ND encoding: <how ND is set>

### Synaptic inhibition (PD vs ND)

* SAC GABA: peak g_GABA, τ, E_rev = e_GABA
* Spatial pattern across dendrites
* PD encoding: gabaMOD = ... or asymmetric SAC drive
* ND encoding: gabaMOD = ... or asymmetric SAC drive

### Differences from the original paper

(brief notes on simplifications, missing features, known divergences)
```

## Stages

* `research-code` — read both beds' code in full, extract every conductance and synapse parameter
  with file:line citations.
* `planning` — write `plan/plan.md` with the section-by-section outline.
* `implementation` — produce the schematic PNGs and write the `results/*` documents.
* `results` + `suggestions` + `reporting` — finalise.

## Compute and budget

* Local Windows workstation. No remote machines, no external API costs.
* Time estimate: 2-3 hours total. No simulation runs (the data is read from existing code).

## Dependencies

The five dependencies above are needed because the writeup *describes* them. None of these are "data
dependencies" in the experiment sense — they are source dependencies: the writeup must reference
their committed code.

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Bed B (t0024) uses different mechanism naming than bed A; cross-bed table doesn't align cleanly. | The bed-A and bed-B conductance tables don't share a column structure. | Use two separate tables with explicit column headers, then a third "shared parameters" table. |
| 2 | NMDA / GABA peak conductance values aren't directly readable from the code (set via HOC params). | grep for `gNMDA`, `s2gampa`, `s2ggaba`, `gabaMOD` returns ambiguous results. | Trace via t0008.code.build_cell.apply_params and t0024 equivalent; cite the params dict. |
| 3 | Morphology PNGs require a NEURON GUI session that doesn't run in headless mode. | matplotlib can't fall back. | Produce a hand-drawn schematic in matplotlib (rectangles + lines) showing the topology, not the 3D morphology. |

## Verification criteria

* Both `results_summary.md` and `results_detailed.md` exist and pass `verify_task_results`.
* Every conductance / synapse parameter has a `code/<file>:<line>` citation.
* The HH membrane equation appears as the first equation in each bed's section.
* Side-by-side comparison table is present.
* All standard verificators pass.
