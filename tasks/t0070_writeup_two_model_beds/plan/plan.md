---
spec_version: "2"
task_id: "t0070_writeup_two_model_beds"
date_completed: "2026-05-01"
status: "complete"
---
# Plan: Writeup of Two Standard DSGC Model Beds in HH-Equation Research-Paper Format

## Objective

Produce a self-contained, presentation-ready research-paper document that describes the project's
two canonical DSGC (direction-selective retinal ganglion cell) model substrates side-by-side: **Bed
A** — the Poleg-Polsky 2016 deposited DSGC ported in t0008 (ModelDB 189347) and used in t0020,
t0065, t0067, t0068, t0069; and **Bed B** — the de Rosenroll 2026 DSGC ported in t0024 and used in
t0066. The writeup must lead each bed with the canonical Hodgkin-Huxley membrane equation, then
enumerate every active conductance with `gbar`, `V_half`, time constants, and reversal potentials,
then define the synaptic excitation and inhibition models for the preferred direction (PD) and null
direction (ND). A side-by-side comparison table at the end summarises the headline differences.
Every numerical parameter must carry a `file:line` citation back to the committed code (no
secondary-source values, no abstracted parameters). "Done" means `results/results_detailed.md` and
`results/results_summary.md` exist, four schematic PNGs (two morphology, two synaptic-timing) live
in `results/images/`, and the standard verificators (`verify_task_results`, `verify_paper_assets`,
etc.) pass with zero errors.

## Task Requirement Checklist

The operative task text from `tasks/t0070_writeup_two_model_beds/task.json` (name +
`short_description`) plus `task_description.md`:

```text
Name: Writeup of two standard DSGC model beds in HH-equation research-paper format.

Short description: Write a research-paper / presentation-ready document describing the project's two
standard DSGC model beds (t0008 deposited Poleg-Polsky 2016 and t0024 de Rosenroll 2026 port). Start
each bed with the canonical Hodgkin-Huxley membrane equation, then enumerate every conductance and
define excitation and inhibition for PD and ND directions.

Long description (excerpts from task_description.md):
* Two model beds, treated symmetrically: same section structure, same equation conventions, same
  level of detail.
* For each bed: cell morphology, membrane equation (canonical HH form, then enumerate every current
  Iᵢ with V_half, τ, gbar), synaptic excitation in PD vs ND (AMPA + NMDA where present, Mg-block
  parameters, peak conductance, timing, source of asymmetry), synaptic inhibition in PD vs ND (SAC
  GABA model, spatial pattern, gabaMOD or equivalent direction-encoding mechanism, e_GABA, peak
  conductance, timing).
* A short side-by-side comparison table at the end summarising headline differences (number of
  compartments, presence of NMDA, AIS or no AIS, gabaMOD vs spatial inhibition).
* Output is a single research-paper-format document under
  tasks/t0070_writeup_two_model_beds/results/results_detailed.md plus a brief
  results/results_summary.md.
* Include a small morphology diagram per bed (axial schematic of compartments, not 3D), saved as
  PNG under results/images/.
* Cross-reference every quoted parameter back to a file path and (where stable) a line number, so
  the writeup is auditable.
```

| ID | Requirement | Satisfied by step(s) | Evidence of completion |
| --- | --- | --- | --- |
| REQ-1 | Each bed's section opens with the canonical Hodgkin-Huxley membrane equation `C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj` rendered consistently in both beds. | Steps 6, 7 | `grep -c 'C_m\\\\|C_{m}'` in both bed sections of `results_detailed.md` returns ≥ 2 matches, one in each bed section. |
| REQ-2 | Every active conductance present in the model is enumerated as a current term Iᵢ in the membrane-equation expansion (Bed A: I_Na, I_Kdr, I_Km, I_leak; Bed B: I_Na, I_Kdr, I_Km, I_leak, I_CaL, I_CaT, plus cad ion accumulation). | Steps 6, 7 | The conductance table in each bed section lists every channel, with no `n/a` rows for the project-default channels. Each row carries a `file:line` citation. |
| REQ-3 | Synaptic excitation in PD vs ND is defined for each bed: peak conductance, kinetics, reversal, and the encoding mechanism that distinguishes PD from ND. | Steps 6, 7, 9 | The "Synaptic excitation (PD vs ND)" subsection in each bed section names every parameter with `file:line` citation and includes a `bed_*_synaptic_diagram.png` showing PD vs ND timing. |
| REQ-4 | Synaptic inhibition in PD vs ND is defined for each bed: peak conductance, kinetics, reversal, and the encoding mechanism (Bed A: gabaMOD scalar 0.33/0.99; Bed B: bar direction 0°/180° + sigmoidal release-probability). | Steps 6, 7, 9 | The "Synaptic inhibition (PD vs ND)" subsection in each bed section names every parameter with `file:line` citation and the synaptic diagram visualises the direction-encoded inhibition. |
| REQ-5 | A side-by-side comparison table at the end summarises the headline differences (compartment counts, NMDA presence, Ca currents, HH variant, PD/ND encoding mechanism, etc.). | Step 8 | `results_detailed.md` ends with a `## Side-by-side comparison` section containing a markdown table with at least 14 rows (one per dimension from research_code.md § 8 of `Recommendations for This Task`). |
| REQ-6 | Schematic morphology PNGs exist for both beds, drawn as axial-schematic compartment diagrams (not 3D), saved under `results/images/`. | Steps 4, 5 | `results/images/bed_a_morphology.png` and `results/images/bed_b_morphology.png` exist, each at least 30 KB, generated by `code/plot_morphology.py`, referenced from `results_detailed.md`. |
| REQ-7 | PD-vs-ND synaptic-timing diagrams exist for both beds, saved under `results/images/`. | Steps 4, 5 | `results/images/bed_a_synaptic_diagram.png` and `results/images/bed_b_synaptic_diagram.png` exist, each at least 20 KB, generated by `code/plot_synaptic_diagram.py`, referenced from `results_detailed.md`. |
| REQ-8 | Every quoted numerical parameter (gbar, τ, V_half, e_rev, peak conductance, kinetics) carries a `file:line` citation back to the committed code. | Steps 6, 7, plus verification step 10 | `grep -E '\\.(mod\|hoc\|py):L?[0-9]+'` across `results_detailed.md` returns ≥ 60 unique citations covering every parameter row in every conductance / synapse table. |
| REQ-9 | Bed A and Bed B sections use parallel structure: same heading order (Morphology → Membrane equation → Conductance table → Synaptic excitation → Synaptic inhibition → Differences from original paper), same notation, same column structure. | Step 6 | Heading-by-heading visual diff between the two bed sections shows identical `### ` heading text (modulo the bed name). |
| REQ-10 | A brief `results/results_summary.md` (2-3 paragraph abstract) exists alongside the full `results_detailed.md`. | Step 7 | `results/results_summary.md` exists with at least 200 words and the standard frontmatter required by `arf/specifications/task_results_specification.md`. |

## Approach

This is a documentation-only **comparative-analysis** task with no simulations, no model training,
no inference, and no remote compute. The recommended task type from `meta/task_types/` is
`comparative-analysis`, which is already set in `task.json`. The Planning Guidelines for
`comparative-analysis` (see `meta/task_types/comparative-analysis/instruction.md`) call for fair
comparison criteria, structured comparison tables, and visualisations of the comparison — all of
which apply here, but in their *documentation* form (no quantitative metrics are measured because no
experiments are run).

The writeup synthesises the file-by-file inventory already produced by the research-code stage
(`research/research_code.md`, 671 lines) into a research-paper-format document. The research-code
stage has already enumerated every conductance, synapse, kinetic equation, and PD/ND-encoding
mechanism with `file:line` citations for both beds — including the cross-bed differences (Ca
currents zeroed in Bed A but not Bed B; stochastic vs deterministic HH variant; modulation-envelope
scalar vs bar-direction encoding). The implementation step's job is to translate that inventory into
a parallel-structured research-paper document and produce four illustrative schematic PNGs.

**Key research-code findings that drive the writeup**:

1. **Both beds insert a mechanism named `HHst` but the source `.mod` files differ**: Bed A uses
   `HHst.mod` (stochastic, Linaro-Storace-Giugliano OU noise, 416 lines, in
   `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/sources/`); Bed B uses
   `HHst_noiseless.mod` (deterministic, 397 lines, in
   `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/sources/`). The
   kinetics are byte-identical (Na: `α=-0.6·vtrap(V+30,-10)`, `β=20·exp(-(V+55)/18)`; Kdr:
   `α=-0.02·vtrap(V+40,-10)`, `β=0.4·exp(-(V+50)/80)`; Km: `α=-0.001·vtrap(V+30,-9)`; etc.). The
   writeup must label them `HHst (stochastic)` and `HHst (noiseless)` to avoid reader confusion.

2. **Bed A holds Ca currents at zero; Bed B leaves them at the `.mod` PARAMETER defaults
   (`glbar=0.0003`, `gtbar=0.0003 S/cm²`)**. Bed A's `init_active()` proc explicitly sets
   `RGCcaL=RGCcaT=0` (`main.hoc` L155-156) and the `update()` proc writes those zeros into every
   section. Bed B's Python `_configure_soma`/`_configure_dends` never write `glbar_HHst` or
   `gtbar_HHst`, so the defaults remain. This is a non-trivial biophysical difference that the
   writeup must call out explicitly.

3. **PD/ND encoding mechanism is fundamentally different between beds, not a different
   parameterisation of the same mechanism**:
   * Bed A keeps the bar geometry fixed and swaps `gabaMOD` (modulation-envelope scalar applied
     inside `placeBIP()` at `mulnoise.fill(VampT*gabaMOD,...)`, `dsgc_model.hoc` L242). PD ⇒
     `gabaMOD = 0.33`; ND ⇒ `gabaMOD = 0.99`. Per-vesicle GABA peak (`s2ggaba = 0.5 nS`) is
     constant.
   * Bed B keeps the GABA conductance fixed and changes the bar's spatial direction (PD = 0°, ND =
     180°), which simultaneously changes per-synapse arrival times via `_bar_arrival_times` and the
     GABA release probability via the sigmoid `_gaba_prob_for_direction` (PD ⇒ ~0.05, ND ⇒ ~0.80).
     The writeup presents these as fundamentally different encoding strategies.

4. **Bed A always uses NMDA (`bipNMDA.mod` AMPA+NMDA point process); Bed B vendors `Exp2NMDA.mod`
   but does not wire it into either `run_tuning_curve.py` or the Vm protocol** — only ACh
   (`Exp2Syn`, `tau1=0.1 ms`, `tau2=4 ms`) and GABA (`Exp2Syn`, `tau1=0.5 ms`, `tau2=12 ms`,
   `e=-60 mV`) are placed. This asymmetry must be stated.

5. **Both beds share the same 350-section morphology** (`create soma, dend[350]`) with identical
   `topol()` and `shape3d_*()` procedures. What differs is which sections receive which mechanisms
   and which sections host synapses (Bed A: 282 ON dendrites carry one BIPsyn + one SACinhibsyn +
   one SACexcsyn each, all 846 placed in HOC; Bed B: ~177 terminal dendrites, derived in Python via
   `_map_tree`, each carries one `Exp2Syn` ACh + one `Exp2Syn` GABA, all placed in Python).

**Document organisation**: parallel per-bed sections (Morphology → Membrane equation → Conductance
table → Synaptic excitation PD/ND → Synaptic inhibition PD/ND → Differences from original paper),
then a single side-by-side comparison table at the end. Equation conventions are shared across beds
(LaTeX-style `$...$` math inside fenced markdown blocks; same symbols `g_X` for peak conductance,
`E_X` for reversal, `τ_X` for kinetics; same units S/cm² for densities, nS for synapse peaks, mV for
reversals, ms for time constants).

**Code to write**: two short matplotlib scripts in `code/`:

* `code/plot_morphology.py` — produces `bed_a_morphology.png` and `bed_b_morphology.png`. Each PNG
  is a hand-drawn axial schematic (rectangles for soma, lines for dendrites, dots for synapse
  positions) showing compartment topology — not a 3D NEURON morphology rendering. Bed A: soma + 350
  dends (282 ON-typed, 68 OFF), with bipolar/SAC synapse triple-markers on the ON dends. Bed B: soma
  \+ 350 dends with the three-tier highlight (primary, non-terminal, terminal) and ACh + GABA
  markers on terminals. Use `matplotlib.patches.Rectangle` for soma and `matplotlib.lines` for
  dendrites; do not import NEURON.
* `code/plot_synaptic_diagram.py` — produces `bed_a_synaptic_diagram.png` and
  `bed_b_synaptic_diagram.png`. Each PNG is a 2-row diagram (PD on top, ND on bottom) showing the
  conductance time-course for excitation (orange) and inhibition (blue) over a representative trial
  window. For Bed A, the inhibition trace is scaled by `gabaMOD = 0.33` (PD) vs `0.99` (ND); for Bed
  B, the GABA trace scales by release-prob `~0.05` (PD) vs `~0.80` (ND) and excitation arrives at
  staggered times along the dendrite. Trace shapes are illustrative (single-exponential decays for
  ACh/GABA, bi-exponential for AMPA/NMDA), not from a NEURON run.

**Alternatives considered**:

* *Run actual NEURON simulations to populate the synaptic-timing PNGs with measured traces.*
  Rejected — task description explicitly states "no simulation runs (the data is read from existing
  code)" and the schematic illustrations serve the writeup's documentation purpose without requiring
  expensive NEURON setup. A side benefit: the schematic decouples the writeup from potential
  simulator changes.
* *Use NEURON's `PlotShape` to render 3D morphology images.* Rejected — task description's risk
  register flags this as needing a NEURON GUI session that doesn't run headless; matplotlib
  schematics are safer and more portable. The morphology numerical content (lengths, diameters,
  topology) lives in the prose, not the figure.
* *Write Bed A and Bed B as two separate documents.* Rejected — the entire point is a single
  side-by-side reference. Two documents would duplicate the equation conventions and lose the
  cross-bed comparison.
* *Skip the schematic PNGs and rely on prose-only description.* Rejected — task description
  explicitly mandates four PNG outputs (`bed_a_morphology.png`, `bed_b_morphology.png`,
  `bed_a_synaptic_diagram.png`, `bed_b_synaptic_diagram.png`) and a "presentation-ready" document
  needs visual aids.

## Cost Estimation

* External API calls: **$0**. No LLM API calls, no paid datasets, no paid services.
* Remote compute: **$0**. Local Windows workstation only; no NEURON runs, no GPU.
* Paid storage: **$0**. All outputs sit in the local repo.
* **Total: $0.00**, well under the project budget of $1.00 total / $1.00 per-task limit
  (`project/budget.json` L2-4). The task is documentation-only — there are no quantitative
  experiments and the four PNGs are produced by short matplotlib scripts that run in seconds on a
  laptop.

## Step by Step

### Milestone 1 — Build matplotlib scripts and PNGs (steps 1-5)

1. **Create `code/paths.py`.** Define `Path` constants:
   * `TASK_ROOT = Path(__file__).resolve().parent.parent`
   * `RESULTS_DIR = TASK_ROOT / "results"`
   * `IMAGES_DIR = RESULTS_DIR / "images"`
   * `BED_A_MORPH_PNG = IMAGES_DIR / "bed_a_morphology.png"`
   * `BED_B_MORPH_PNG = IMAGES_DIR / "bed_b_morphology.png"`
   * `BED_A_SYNDIAG_PNG = IMAGES_DIR / "bed_a_synaptic_diagram.png"`
   * `BED_B_SYNDIAG_PNG = IMAGES_DIR / "bed_b_synaptic_diagram.png"`
   * `RESULTS_DETAILED_MD = RESULTS_DIR / "results_detailed.md"`
   * `RESULTS_SUMMARY_MD = RESULTS_DIR / "results_summary.md"`
   * `IMAGES_DIR.mkdir(parents=True, exist_ok=True)` is called by the plotting scripts at runtime,
     not in `paths.py` (paths.py must be import-side-effect-free). Expected output: `code/paths.py`
     exists, importable. Satisfies infrastructure for REQ-6, REQ-7.

2. **Create `code/constants.py`.** Define:
   * Plotting constants: `FIG_DPI = 150`, `FIG_WIDTH_IN = 10.0`, `FIG_HEIGHT_IN = 6.0`.
   * Trace timing: `TRACE_DURATION_MS = 200.0`, `TRACE_DT_MS = 0.1`,
     `BAR_ARRIVAL_BASELINE_MS = 50.0`.
   * Bed A synaptic kinetics for the schematic: `BED_A_AMPA_TAU_MS = 2.0`,
     `BED_A_NMDA_TAU_RISE_MS = 2.0`, `BED_A_NMDA_TAU_DECAY_MS = 60.0`, `BED_A_GABA_TAU_MS = 30.0`,
     `BED_A_GABAMOD_PD = 0.33`, `BED_A_GABAMOD_ND = 0.99`, `BED_A_AMPA_PEAK_NS = 0.25`,
     `BED_A_NMDA_PEAK_NS = 0.5`, `BED_A_GABA_PEAK_NS = 0.5`.
   * Bed B synaptic kinetics: `BED_B_ACH_TAU_RISE_MS = 0.1`, `BED_B_ACH_TAU_DECAY_MS = 4.0`,
     `BED_B_GABA_TAU_RISE_MS = 0.5`, `BED_B_GABA_TAU_DECAY_MS = 12.0`, `BED_B_GABA_PROB_PD = 0.05`,
     `BED_B_GABA_PROB_ND = 0.80`, `BED_B_ACH_WEIGHT_US = 0.001`, `BED_B_GABA_WEIGHT_US = 0.003`.
   * Morphology counts: `BED_A_N_DEND = 350`, `BED_A_N_ON_DEND = 282`, `BED_B_N_DEND = 350`,
     `BED_B_N_TERMINAL_DEND_APPROX = 177`, `BED_B_N_PRIMARY_DEND_APPROX = 10`.
   * Colour scheme: `COLOR_EXC = "tab:orange"`, `COLOR_INH = "tab:blue"`, `COLOR_SOMA = "tab:gray"`,
     `COLOR_DEND_ON = "tab:green"`, `COLOR_DEND_OFF = "lightgray"`. Use `Final` type annotation and
     follow the project Python style guide (centralised constants). Expected output:
     `code/constants.py` exists, importable. Satisfies infrastructure for REQ-3, REQ-4, REQ-6,
     REQ-7.

3. **Create `code/schematic_helpers.py`.** Define small pure helper functions used by both plotting
   scripts:
   * `bi_exponential_trace(t_ms: np.ndarray, t0_ms: float, tau_rise_ms: float, tau_decay_ms: float, peak: float) -> np.ndarray`
     — returns a normalised difference-of- exponentials trace scaled to peak amplitude.
   * `single_exponential_trace(t_ms: np.ndarray, t0_ms: float, tau_ms: float, peak: float) -> np.ndarray`
     — returns an instantaneous-rise / single-exp-decay trace.
   * `draw_dendritic_tree(ax: Axes, *, n_branches: int, branch_color: str, soma_color: str, synapse_xy: list[tuple[float, float]] | None, synapse_color: str | None) -> None`
     — draws a fan-shaped axial schematic with the soma at origin and `n_branches` lines radiating
     outward, plus optional synapse markers. Use `matplotlib.patches.Circle` for the soma, `ax.plot`
     for dendrites, `ax.scatter` for synapse markers. Functions take all arguments as keyword
     arguments (project style guide). No I/O, no NEURON imports, no top-level mutable state.
     Expected output: `code/schematic_helpers.py` exists, importable. Satisfies infrastructure for
     REQ-6, REQ-7.

4. **Write `code/plot_morphology.py`.** This script produces the two morphology PNGs.
   * Bed A subplot: 1 soma circle (radius scaled by `BED_A_N_DEND/350`), 282 short green lines
     fanning outward (`COLOR_DEND_ON`) representing ON dendrites, 68 light-grey lines representing
     OFF dendrites, plus three synapse markers per ON dendrite (orange dot for BIPsyn, dark-blue dot
     for SACinhibsyn, light-orange dot for SACexcsyn) placed at the dendrite midpoint. Title: "Bed
     A: Poleg-Polsky 2016 (t0008) — 1 soma + 350 dends, 282 ON, 846 point processes".
   * Bed B subplot: 1 soma circle, 350 dendrite lines colour-coded by tier (`primary` = darker
     green, `non_terminal` = mid green, `terminal` = light green); ACh + GABA markers (orange, blue)
     on terminal-tier dendrite tips only. Title: "Bed B: de Rosenroll 2026 (t0024) — 1 soma + 350
     dends, ~10 primary / mid / ~177 terminal, ~354 Exp2Syn point processes".
   * Save to `BED_A_MORPH_PNG` and `BED_B_MORPH_PNG` at `FIG_DPI`.
   * The script is invoked via
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0070_writeup_two_model_beds -- uv run python -u -m tasks.t0070_writeup_two_model_beds.code.plot_morphology`.
   * Expected output: both PNGs exist, each at least 30 KB. Satisfies REQ-6.

5. **Write `code/plot_synaptic_diagram.py`.** This script produces the two synaptic-diagram PNGs,
   each a 2-row figure (top row PD, bottom row ND) showing illustrative conductance time courses
   over a 200 ms window.
   * Bed A figure: top row plots `g_AMPA(t)` (single-exp decay, `BED_A_AMPA_TAU_MS = 2.0`),
     `g_NMDA(t)` (bi-exponential, rise 2 ms, decay 60 ms, with Mg-block annotation), and
     `g_GABA(t) * BED_A_GABAMOD_PD` (single-exp, `BED_A_GABA_TAU_MS = 30.0`). Bottom row identical
     except `g_GABA(t)` is scaled by `BED_A_GABAMOD_ND = 0.99`. Annotate the gabaMOD swap.
     Excitation timing is identical between PD and ND (the Bed A encoding is purely
     inhibitory-scalar).
   * Bed B figure: top row plots `g_ACh(t)` (Exp2Syn, rise 0.1 ms, decay 4 ms) at staggered arrival
     times across 5 representative terminal dendrites (PD wave, sweeping left-to-right at
     `BAR_VELOCITY_UM_PER_MS = 1.0`), and `g_GABA(t)` (Exp2Syn, rise 0.5 ms, decay 12 ms) scaled by
     `BED_B_GABA_PROB_PD = 0.05`. Bottom row reverses arrival ordering (ND wave, right-to-left) and
     scales GABA by `BED_B_GABA_PROB_ND = 0.80`. Annotate the bar-direction swap.
   * Save to `BED_A_SYNDIAG_PNG` and `BED_B_SYNDIAG_PNG` at `FIG_DPI`.
   * Invoked via
     `uv run python -m arf.scripts.utils.run_with_logs --task-id t0070_writeup_two_model_beds -- uv run python -u -m tasks.t0070_writeup_two_model_beds.code.plot_synaptic_diagram`.
   * Expected output: both PNGs exist, each at least 20 KB. Satisfies REQ-3, REQ-4, REQ-7.

### Milestone 2 — Write the research-paper document (steps 6-9)

6. **Write `results/results_detailed.md` (Bed A section).** Begin with the YAML frontmatter and
   `# Title` heading required by `arf/specifications/task_results_specification.md`. Then write the
   mandatory results-specification sections (Methodology, Inputs, etc.) followed by the bed-by-bed
   content. The Bed A section follows this exact structure (parallel to Bed B in step 7):

   * `## Bed A: Poleg-Polsky 2016 (t0008 + t0020)` — opening paragraph naming the source library
     `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/`, upstream commit
     `87d669dcef18e9966e29c88520ede78bc16d36ff`, and the protocol task t0020 that established the
     gabaMOD-swap PD/ND convention.
   * `### Morphology` — soma + 350 dendrites (`RGCmodel.hoc:L14`), 282 ON dendrites identified by
     `z3d ≥ -0.16·y3d + 46` (`RGCmodel.hoc:L11801-11803`), per-dendrite diameter formula
     `diam = 0.5 + 2.58·exp(-(distance(0.5)-10)/10)` (`RGCmodel.hoc:L11814`), `nseg = 1` per section
     (`RGCmodel.hoc:L11818`), `Ra = 100 Ω·cm` (`dsgc_model.hoc:L317`), `cm = 1 µF/cm²` (NEURON
     default), `celsius = 32°C` (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L284`).
     Reference `bed_a_morphology.png`.
   * `### Membrane equation` — write the canonical HH equation as a fenced math block:
     ```
     C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj
     ```
     then expand `Σᵢ Iᵢ` with one current per line: `I_Na`, `I_Kdr`, `I_Km`, `I_leak`. Note that
     `I_CaL` and `I_CaT` are present in the `HHst.mod` source but are **explicitly zeroed** by
     `init_active()` (`main.hoc:L155-156` setting `RGCcaL=RGCcaT=0`, then `update()` writing those
     into `glbar_HHst`/`gtbar_HHst` per section, `main.hoc:L302-303`). Cite `HHst.mod:L190-222` for
     the `BREAKPOINT` block.
   * `### Conductance table` — markdown table with columns:
     `Channel | Gating | V_half_act (mV) | τ_act (ms) | V_half_inact (mV) | τ_inact (ms) | gbar (S/cm²) | E_rev (mV) | Source`.
     Two sub-rows per channel: soma + dend (use `use_active=0` is the project default; cite
     `main.hoc:L36`). Channels:
     * `Na` (m³h, `m_inf` from `α=-0.6·vtrap(V+30,-10), β=20·exp(-(V+55)/18)`, `HHst.mod:L249-251`;
       `h_inf = 1/(1+exp((V+44)/4))`, `HHst.mod:L265`; soma gNa = 0.4 (`main.hoc:L148`), dend gNa =
       0.0002 (`main.hoc:L152`)).
     * `Kdr` (n⁴, `α=-0.02·vtrap(V+40,-10), β=0.4·exp(-(V+50)/80)`, `HHst.mod:L294-297`; soma gKdr =
       0.07 (`main.hoc:L149`), dend gKdr = 0.007 (`main.hoc:L153`)).
     * `Km` (linear gating in nm, `HHst.mod:L315-318`, `taukm=1`, `HHst.mod:L70`; soma gKm = 0.0005
       (`main.hoc:L150`), dend gKm = 0 (`main.hoc:L154`)).
     * `Leak` (gleak = 5e-5 passive / 5.5e-4 active (`main.hoc:L161`), eleak = -60
       (`main.hoc:L162`)).
     * `vshift = -4 mV` global shift on every gating variable (`main.hoc:L91`,
       `tasks/t0008_port_modeldb_189347/code/build_cell.py:L312`).
   * `### Synaptic excitation (PD vs ND)` — describe the `bipNMDA` POINT_PROCESS in
     `bipolarNMDA.mod` (282 instances, one per ON dendrite, placed by `RGCmodel.hoc:L11841-11843`).
     Tabulate AMPA + NMDA parameters with citations to `bipolarNMDA.mod` lines 35-42 and
     `tasks/t0008_port_modeldb_189347/code/build_cell.py:L294-316` for the runtime overrides.
     Include the NMDA Mg-block formula `gNMDA = (A-B)/(1 + n·exp(-gama·V))` (`bipolarNMDA.mod:L102`)
     and the vesicular-release model (`bipolarNMDA.mod:L131-152`). Subsection "PD vs ND for
     excitation": no asymmetry — bipolar drive is symmetric across PD and ND. The asymmetry lives in
     inhibition (next subsection). Reference `bed_a_synaptic_diagram.png`.
   * `### Synaptic inhibition (PD vs ND)` — describe the `SACinhib` POINT_PROCESS in
     `SAC2RGCinhib.mod` (282 instances, placed by `RGCmodel.hoc:L11835-11838`). Per-vesicle
     `gsingle = 0.5 nS` (`s2ggaba`, `tasks/t0008_port_modeldb_189347/code/build_cell.py:L296`),
     decay `tau = 30 ms` (effective; the GLOBAL `tau_SACinhib` in HOC overrides the per-instance
     mechanism `tau`, `main.hoc:L90`), reversal `e = -60 mV` (`E_SAC_INHIB_MV`,
     `tasks/t0008_port_modeldb_189347/code/build_cell.py:L314`). PD/ND encoding via `gabaMOD`
     modulation-envelope scalar in `placeBIP()` (`mulnoise.fill(VampT*gabaMOD,...)`,
     `dsgc_model.hoc:L242`): PD ⇒ `gabaMOD = 0.33`, ND ⇒ `gabaMOD = 0.99` (canonical values from
     `tasks/t0020_port_modeldb_189347_gabamod/code/constants.py:L37-38`). Explicitly note that
     `gabaMOD` scales the *presynaptic envelope*, not the postsynaptic conductance. Also describe
     the parallel cholinergic SAC pathway (`SACexcsyn`, `SAC2RGCexc.mod`, `achMOD = 0.25` constant
     across PD/ND).
   * `### Differences from the original paper` — bullet list of known divergences from Poleg-Polsky
     2016: Ca currents zeroed (vs paper's L/T-Ca enabled); `tau1NMDA = 60 ms` overridden from `.mod`
     default 50 ms (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L313`); `n = 0.3`,
     `gama = 0.07` overridden from defaults `0.25 / 0.08`
     (`tasks/t0008_port_modeldb_189347/code/build_cell.py:L315-316`); HHst is the stochastic variant
     but the project drivers set `NF=0` (`dsgc_model.hoc:L85`) so noise is disabled by default.
     Satisfies REQ-1, REQ-2, REQ-3, REQ-4, REQ-8, REQ-9.

7. **Continue `results/results_detailed.md` (Bed B section).** Same heading order, same equation
   notation as Bed A.

   * `## Bed B: de Rosenroll 2026 (t0024)` — opening paragraph naming the source library
     `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/`, upstream
     commit `a23f642aa6557a23a51bf76f51e420e8149773fa`, and the protocol task t0066 that established
     the bar-direction PD/ND convention.
   * `### Morphology` — same 350-section template (`RGCmodelGD.hoc:L12`) as Bed A, with the same
     `topol()` and `shape3d_*` (verbatim from Bed A; cite `RGCmodelGD.hoc:L11801-11803` for the
     ON/OFF sort; `RGCmodelGD.hoc:L11814` for the diameter formula). Three Python-derived dendrite
     tiers: `primary_dends` (~10), `non_terminal_dends` (intermediate), `terminal_dends` (~177
     leaves). Cite `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L140-168` for
     `_map_tree`. `Ra = 100 Ω·cm`, `cm = 1 µF/cm²`, `celsius = 36.9°C` (cite
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L19`). Reference
     `bed_b_morphology.png`.
   * `### Membrane equation` — write the canonical HH equation in identical format to Bed A:
     ```
     C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj
     ```
     then expand `Σᵢ Iᵢ` with one current per line: `I_Na`, `I_Kdr`, `I_Km`, `I_leak`, `I_CaL`,
     `I_CaT`. Note that **unlike Bed A**, `I_CaL` and `I_CaT` are at the `HHst_noiseless.mod`
     PARAMETER defaults (3e-4 each, cite `HHst_noiseless.mod:L57-58`) on every section because the
     Python builder never zeros them. Also describe the `cad` (calcium decay) mechanism:
     `depth = 0.1 µm`, `taur = 5 ms`, `cainf = 2e-4 mM` (`cadecay.mod:L44-49`), present on every
     section that has `HHst` inserted.
   * `### Conductance table` — same column structure as Bed A, but three sub-rows per channel (soma,
     primary dendrites, non-terminal mid dendrites, terminal dendrites). Tabulate every channel from
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L34-42` and
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/build_cell.py:L192-248`:
     * `Na` (kinetics identical to Bed A's `HHst.mod` Na — kinetics live in
       `HHst_noiseless.mod:L244-261`; soma gNa = 0.150, primary = 0.200 (higher than soma!),
       non-terminal = 0 (zeroed), terminal = 0.030 S/cm²).
     * `Kdr` (soma 0.035, primary 0.035, non-terminal 0.025, terminal 0.025 S/cm²).
     * `Km` (uniform 0.003 S/cm² across all sections).
     * `Leak` (uniform 1.667e-4 S/cm², eleak = -60 mV).
     * `CaL` (uniform 3e-4 S/cm² — `.mod` default, never overridden; `HHst_noiseless.mod:L57`).
     * `CaT` (uniform 3e-4 S/cm² — `.mod` default, never overridden; `HHst_noiseless.mod:L58`).
   * `### Synaptic excitation (PD vs ND)` — describe the `Exp2Syn` ACh synapse (one per terminal
     dendrite, ~177 instances, placed by
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L189-226`,
     `_setup_synapses`). `tau1 = 0.1 ms` (rise), `tau2 = 4 ms` (decay), `e = 0 mV`, NetCon weight =
     0.001 µS (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L45-48`). Note that
     `Exp2NMDA.mod` is vendored but **not wired** into either `run_tuning_curve.py` or the
     EPSP/IPSP/Vm protocol — only ACh is placed. The NMDA parameters in
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L57-61` are present for potential
     future use. PD/ND encoding for excitation: bar arrival times at each synapse are
     direction-dependent via `_bar_arrival_times(syn_xy, origin_xy, direction_deg)` (
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L92-109`). Bar moves at
     `BAR_VELOCITY_UM_PER_MS = 1.0`; PD = 0° (rightward), ND = 180° (leftward) (cite
     `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/constants.py:L19-20`). AR(2) Poisson noise drives
     `nc.event(t)`; release model is fully Python-side (no presynaptic-voltage vesicle- release
     model like Bed A's `bipolarNMDA.mod`). Reference `bed_b_synaptic_diagram.png`.
   * `### Synaptic inhibition (PD vs ND)` — describe the `Exp2Syn` GABA synapse (one per terminal
     dendrite, ~177 instances). `tau1 = 0.5 ms` (rise), `tau2 = 12 ms` (decay), `e = -60 mV`
     (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L50-52`), NetCon weight = 0.003 µS
     (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L53`). PD/ND encoding via
     `_gaba_prob_for_direction` sigmoid
     (`tasks/t0024_port_de_rosenroll_2026_dsgc/code/run_tuning_curve.py:L80-89`): `pref_prob = 0.05`
     (PD), `null_prob = 0.80` (ND), with `CELL_PREF = 0°`. Per-synapse arrival times also shift with
     direction via `_bar_arrival_times`. Optional AR(2) cross-channel correlation: `rho = 0.6` for
     the correlated condition (used by t0066,
     `tasks/t0024_port_de_rosenroll_2026_dsgc/code/constants.py:L67-68`).
   * `### Differences from the original paper` — bullet list:
     * Vendored `Exp2NMDA.mod` not wired into any driver (NMDA parameters in `constants.py` are
       latent).
     * `HHst_noiseless` deterministic variant matches the upstream de Rosenroll choice.
     * Synaptic-release noise is AR(2) Python-side rather than the upstream `ei_balance.py` Python
       model (which the t0024 port reimplements in simplified form). Satisfies REQ-1, REQ-2, REQ-3,
       REQ-4, REQ-8, REQ-9.

8. **Append the side-by-side comparison table.** A single `## Side-by-side comparison` section
   containing one markdown table with at least 14 rows (one per dimension). Columns:
   `Dimension | Bed A (Poleg-Polsky 2016, t0008) | Bed B (de Rosenroll 2026, t0024)`. Rows (in
   order):

   1. Morphology source — same 350-section template
   2. Section count — 1 soma + 350 dends (both)
   3. ON-typed dendrite count — 282 (Bed A) / ~177 terminal (Bed B)
   4. Synapse placement — HOC-side (Bed A) / Python-side (Bed B)
   5. Point processes per cell — 846 (Bed A) / ~354 (Bed B)
   6. HH variant — `HHst.mod` stochastic (Bed A) / `HHst_noiseless.mod` deterministic (Bed B)
   7. Active channels at default — Na+Kdr+Km only (Bed A, Ca zeroed) / Na+Kdr+Km+CaL+CaT+cad (Bed B,
      Ca at .mod defaults)
   8. Excitation mechanism — `bipNMDA` AMPA+NMDA point process (Bed A) / `Exp2Syn` ACh (Bed B,
      `Exp2NMDA` latent)
   9. NMDA active in driver — Yes (Bed A) / No (Bed B)
   10. Inhibition mechanism — `SACinhib` POINT_PROCESS w/ vesicular release (Bed A) / `Exp2Syn` GABA
       w/ Poisson NetCon events (Bed B)
   11. GABA reversal — −60 mV (both)
   12. Per-vesicle GABA peak — 0.5 nS (Bed A) / 0.003 µS NetCon weight (Bed B)
   13. PD encoding mechanism — `gabaMOD = 0.33` envelope scalar (Bed A) / `direction_deg = 0°` +
       `release_prob = 0.05` (Bed B)
   14. ND encoding mechanism — `gabaMOD = 0.99` envelope scalar (Bed A) / `direction_deg = 180°` +
       `release_prob = 0.80` (Bed B)
   15. Release noise — Linaro-Storace-Giugliano stochastic per vesicle (Bed A, but `NF=0` by
       default) / AR(2) Python-side Poisson (Bed B)
   16. Temperature — 32°C (Bed A) / 36.9°C (Bed B)
   17. Resting V_init — −65 mV (Bed A) / −60 mV (Bed B)
   18. Ra / cm — 100 Ω·cm / 1 µF/cm² (both) Satisfies REQ-5.

9. **Insert the synaptic-diagram references and finalise the section ordering.** Ensure the four
   PNGs are referenced at the appropriate points in `results_detailed.md`:
   * `bed_a_morphology.png` referenced in Bed A's `### Morphology` subsection.
   * `bed_a_synaptic_diagram.png` referenced in Bed A's `### Synaptic excitation (PD vs ND)`
     subsection.
   * `bed_b_morphology.png` referenced in Bed B's `### Morphology` subsection.
   * `bed_b_synaptic_diagram.png` referenced in Bed B's `### Synaptic excitation (PD vs ND)`
     subsection. Each reference uses standard markdown image syntax
     `![alt text](images/<filename>.png)`. Run
     `uv run flowmark --inplace --nobackup tasks/t0070_writeup_two_model_beds/results/ results_detailed.md`
     to normalise wrapping (100-char target). Satisfies REQ-3, REQ-4, REQ-6, REQ-7.

### Milestone 3 — Write the summary (step 10)

10. **Write `results/results_summary.md`.** A 2-3 paragraph abstract (~250-400 words) suitable as a
    presentation abstract. Frontmatter follows `arf/specifications/task_results_specification.md`.
    Content:
    * Paragraph 1 (~100 words): name the two beds, their source libraries, and the project tasks
      that use each. State that the writeup leads each bed with the canonical HH equation, then
      enumerates conductances and synaptic models, with a side-by-side comparison table at the end.
    * Paragraph 2 (~100 words): summarise the headline differences (HH variant, Ca current handling,
      NMDA presence, PD/ND encoding mechanism). Cross-reference the comparison table.
    * Paragraph 3 (~100 words): point to the four schematic figures and state that every parameter
      in the detailed writeup carries a `file:line` citation back to the committed code, making the
      document fully auditable. Run
      `uv run flowmark --inplace --nobackup tasks/t0070_writeup_two_model_beds/results/ results_summary.md`.
      Satisfies REQ-10.

### Milestone 4 — Quality gates (steps 11-12)

11. **Run formatters and type checks.** From the worktree root:
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0070_writeup_two_model_beds -- uv run ruff check --fix . && uv run ruff format . && uv run mypy tasks/t0070_writeup_two_model_beds/code/`.
    Expected: zero ruff errors, zero mypy errors. If mypy complains about untyped matplotlib calls,
    add a targeted `# type: ignore[attr-defined]` with a comment explaining which matplotlib API is
    being used. Idempotent — safe to re-run.

12. **Run the task-results verificator.** From the worktree root:
    `uv run python -m arf.scripts.utils.run_with_logs --task-id t0070_writeup_two_model_beds -- uv run python -u -m arf.scripts.verificators.verify_task_results t0070_writeup_two_model_beds`.
    Expected: zero errors. Address every warning unless documented as deliberate. If any warning
    relates to missing metrics, refer the reader to the explicit note in
    `results/results_detailed.md` Methodology section that no quantitative metrics are measured
    (this is a documentation-only task).

**Note on the boundary**: The Step by Step ends here. The orchestrator-managed bookkeeping JSON
files are created in the orchestrator-managed `results`, `reporting`, and `suggestions` steps that
follow this plan's scope, not by the implementation agent. The verificator's PL-W009 warning about
the writeup-document filenames in this Step by Step is acknowledged and acceptable: this is a
documentation-only task whose entire deliverable, per the parent task description in
`task_description.md` ("implementation — produce the schematic PNGs and write the `results/*`
documents"), IS the writing of those two markdown documents. There is no other compute or asset
production to which the Step by Step could end.

**Registered metrics applicability check**: The four registered project metrics
(`direction_selectivity_index`, `tuning_curve_hwhm_deg`, `tuning_curve_reliability`,
`tuning_curve_rmse`) all require simulated AP rates from a NEURON tuning-curve sweep. **None apply
to this task** because no simulations are run. `results/metrics.json` will therefore be empty (`{}`)
and a Methodology note in `results_detailed.md` will state explicitly that the omission is
deliberate and motivated by the documentation-only nature of the task.

## Remote Machines

None required. The task is documentation-only — no NEURON simulations, no GPU, no remote compute.
All matplotlib plotting and markdown writing happens on the local Windows workstation in seconds.
See `arf/specifications/remote_machines_specification.md`; `results/remote_machines_used.json` will
be `{}`.

## Assets Needed

Input assets (all already exist in the worktree from the dependency tasks):

* `tasks/t0008_port_modeldb_189347/assets/library/modeldb_189347_dsgc/` — Bed A's vendored sources
  (HOC + MOD files) plus `code/build_cell.py`, `code/constants.py` for runtime parameter overrides.
  From dependency [t0008].
* `tasks/t0020_port_modeldb_189347_gabamod/code/constants.py` — canonical `gabaMOD = 0.33` (PD) /
  `0.99` (ND) values and the `run_one_trial_gabamod` driver showing the swap. From dependency
  [t0020].
* `tasks/t0024_port_de_rosenroll_2026_dsgc/assets/library/de_rosenroll_2026_dsgc/` — Bed B's
  vendored sources plus `code/build_cell.py`, `code/constants.py`, `code/run_tuning_curve.py`. From
  dependency [t0024].
* `tasks/t0065_t0020_epsp_ipsp_vm_protocol/code/run_protocol.py` and `code/constants.py` — Bed A's
  EPSP/IPSP/FULL protocol mechanism (HOC-level `h.exptype`, `h.gabaMOD`, `h.s2ggaba`, `h.b2gampa`,
  etc.). From dependency [t0065].
* `tasks/t0066_t0024_epsp_ipsp_vm_protocol/code/run_protocol.py` and `code/constants.py` — Bed B's
  EPSP/IPSP/FULL protocol mechanism (Python-side `seg.HHst.gnabar = 0`, `nc.weight[0] = 0`). From
  dependency [t0066].
* `tasks/t0070_writeup_two_model_beds/research/research_code.md` — the 671-line file:line inventory
  already produced by this task's research-code stage. The implementation step uses this as the
  primary lookup table for parameter values and citations.

No external downloads, no new datasets, no new libraries, no paper assets created or modified.

## Expected Assets

Per `tasks/t0070_writeup_two_model_beds/task.json` `expected_assets` field, this task produces no
formal asset-type assets (no papers, no datasets, no libraries, no models, no predictions, no
answers). The `expected_assets` is `{}` by design — the task's outputs are the standard `results/`
documents and four schematic PNGs:

* `results/results_detailed.md` — full research-paper-format writeup of both beds, ~3000-4500 words,
  with bed-by-bed sections leading with the HH membrane equation, conductance tables, synaptic
  excitation + inhibition subsections, and a side-by-side comparison table.
* `results/results_summary.md` — 250-400 word abstract suitable for a presentation slide.
* `results/images/bed_a_morphology.png` — Bed A axial-schematic morphology diagram.
* `results/images/bed_b_morphology.png` — Bed B axial-schematic morphology diagram with
  primary/mid/terminal tier highlighting.
* `results/images/bed_a_synaptic_diagram.png` — Bed A PD-vs-ND synaptic conductance time courses
  showing the gabaMOD modulation-envelope swap.
* `results/images/bed_b_synaptic_diagram.png` — Bed B PD-vs-ND synaptic conductance time courses
  showing the bar-direction sweep + sigmoidal release-probability swap.
* `code/paths.py`, `code/constants.py`, `code/schematic_helpers.py`, `code/plot_morphology.py`,
  `code/plot_synaptic_diagram.py` — five Python files (matplotlib-only, no NEURON).

The orchestrator-managed bookkeeping outputs (`results/metrics.json` = `{}`, `results/costs.json`,
`results/remote_machines_used.json` = `{}`, `results/suggestions.json`) are not part of this plan's
Step by Step but are produced by the orchestrator during the `results`, `reporting`, and
`suggestions` steps that follow.

## Time Estimation

Per-phase wall-clock estimates on a local Windows workstation:

* Research (already done in step 4 of step_tracker, `research/research_code.md`): completed in ~14
  minutes (`logs/steps/004_research-code/`).
* Implementation milestone 1 (matplotlib scripts + four PNGs, steps 1-5): ~45 minutes for paths /
  constants / helpers / two plotting scripts; matplotlib script execution under 10 seconds total.
* Implementation milestone 2 (write `results_detailed.md` Bed A + Bed B + comparison table, steps
  6-9): ~75 minutes — the bulk of the work; 10+ tables and 60+ citations to look up from the
  research_code.md inventory.
* Implementation milestone 3 (write `results_summary.md`, step 10): ~15 minutes.
* Implementation milestone 4 (formatters + verificator, steps 11-12): ~5 minutes.
* **Total active implementation time**: ~2h20m, matching the task description's "2-3 hours total"
  estimate. No simulation runtime, no remote compute wait time.

## Risks & Fallbacks

| Risk | Likelihood | Impact | Mitigation |
| --- | --- | --- | --- |
| Bed B (t0024) and Bed A (t0008) use different parameter naming conventions, making the conductance tables hard to align in a shared column structure (e.g., Bed A has soma/dend rows; Bed B has soma/primary/mid/terminal rows). | High | Medium — table readability suffers and the side-by-side comparison loses crispness. | Use two separate conductance tables (one per bed) with bed-specific row counts, then a third "shared parameters" reference table for the values that match (Ra, cm, eleak, vshift). The side-by-side comparison table at the end summarises the headline differences in a single uniform table. |
| Effective synaptic parameter values differ from `.mod` PARAMETER defaults because of GLOBAL-vs-RANGE behaviour (e.g., `tau_SACinhib`, `gsingle_SACinhib` are GLOBAL in `SAC2RGCinhib.mod:L7`, so HOC `tau_SACinhib = 30` updates per-instance `tau` for every instance). The writeup could quote the wrong (default) values. | Medium | High — undermines the audit-trail credibility. | Lessons-learned section of `research/research_code.md` already enumerates the known GLOBAL-vs-RANGE traps (`tau`, `e`, `gsingle` in SAC2RGCinhib; `gabaMOD` as envelope scalar). The writeup must report effective runtime values, not `.mod` PARAMETER defaults, and cite the override site (`apply_params` in `tasks/t0008_port_modeldb_189347/code/build_cell.py:L280-316`) alongside the original `.mod` line. |
| The matplotlib schematic PNGs become misleading by oversimplifying — e.g., a fan diagram does not show the 3D dendritic tree and a reader interprets it literally as 1D. | Medium | Low — cosmetic; unlikely to cause downstream errors. | Add an explicit caption beneath each figure in `results_detailed.md` stating "Schematic; not to scale; see RGCmodel.hoc:L212-11722 for the full 3D coordinates." Also note in the figure title that the diagram is illustrative. |
| `verify_task_results` fails on the `results/metrics.json = {}` empty file because the verificator expects at least one metric. | Low | Medium — would block the task. | Read `arf/specifications/task_results_specification.md` first; if `metrics.json` is required to have at least one entry, add a single sentinel entry such as `{"document_completeness": null}` or omit the file and rely on the orchestrator's empty-file generation. The `results_detailed.md` Methodology section explicitly states no quantitative metrics are measured; the verificator should treat empty metrics.json as acceptable for a documentation-only task. If it does not, file an intervention requesting clarification rather than fabricating metric values. |
| The four PNGs end up inconsistent in style (different fonts, different colour conventions for excitation/inhibition) because each is generated by a different script call. | Low | Low — cosmetic. | Centralise plotting style constants in `code/constants.py` (`COLOR_EXC`, `COLOR_INH`, `FIG_DPI`, etc.) and import them in both plotting scripts. Use `matplotlib.rcParams` defaults — no per-script style overrides. |
| `flowmark` reflows the equation blocks and breaks the LaTeX-style math. | Low | Low — purely visual. | Inspect `results_detailed.md` after running flowmark; if equation lines were reflowed unexpectedly, wrap them in fenced `text` blocks (`` ```text `` … `` ``` ``) which flowmark preserves. The task description's snippet already uses fenced blocks for equations. |

## Verification Criteria

* **VC-1: Plan-specification verificator passes.** Run
  `uv run python -u -m arf.scripts.verificators.verify_plan t0070_writeup_two_model_beds`. Expected
  output: zero errors reported. (This is the verificator the planning skill must satisfy before
  handing off.)
* **VC-2: Both result documents exist and pass `verify_task_results`.** After implementation, run
  `uv run python -u -m arf.scripts.verificators.verify_task_results t0070_writeup_two_model_beds`.
  Expected output: zero errors. Confirms `results_summary.md` and `results_detailed.md` exist,
  contain the mandatory frontmatter and sections per
  `arf/specifications/task_results_specification.md`, and that REQ-10 is satisfied.
* **VC-3: All four schematic PNGs exist and are non-trivial.** Run from the worktree root:
  `uv run python -c "from pathlib import Path; ps = ['tasks/t0070_writeup_two_model_beds/results/images/bed_a_morphology.png', 'tasks/t0070_writeup_two_model_beds/results/images/bed_b_morphology.png', 'tasks/t0070_writeup_two_model_beds/results/images/bed_a_synaptic_diagram.png', 'tasks/t0070_writeup_two_model_beds/results/images/bed_b_synaptic_diagram.png']; [print(p, Path(p).exists(), Path(p).stat().st_size) for p in ps]"`.
  Expected output: all four paths print `True` with `st_size >= 20000` (20 KB) for the synaptic
  diagrams and `>= 30000` (30 KB) for the morphology diagrams. Confirms REQ-6 and REQ-7.
* **VC-4: Both bed sections open with the canonical HH equation.** Run
  `uv run python -c "import re; t = open('tasks/t0070_writeup_two_model_beds/results/results_detailed.md', encoding='utf-8').read(); print(len(re.findall(r'C_m\\\\s*[·\\\\*]\\\\s*dV/dt', t)))"`.
  Expected output: integer ≥ 2 (one occurrence per bed section). Confirms REQ-1.
* **VC-5: Every parameter row carries a `file:line` citation.** Run
  `uv run python -c "import re; t = open('tasks/t0070_writeup_two_model_beds/results/results_detailed.md', encoding='utf-8').read(); print(len(set(re.findall(r'(?:[A-Za-z_/0-9]+\\\\.(?:mod|hoc|py)):L?\\\\d+', t))))"`.
  Expected output: integer ≥ 60. Confirms REQ-2 and REQ-8.
* **VC-6: Side-by-side comparison table exists with at least 14 rows.** Run
  `uv run python -c "t = open('tasks/t0070_writeup_two_model_beds/results/results_detailed.md', encoding='utf-8').read(); s = t.split('## Side-by-side comparison')[1] if '## Side-by-side comparison' in t else ''; print(s.count(chr(10) + '|') - 2)"`.
  Expected output: integer ≥ 14 (header + alignment row are subtracted). Confirms REQ-5.
* **VC-7: Every `REQ-*` item is referenced at least once in `results_detailed.md`'s
  implementation-tracking notes or its Methodology / Coverage section.** Run
  `uv run python -c "import re; t = open('tasks/t0070_writeup_two_model_beds/results/results_detailed.md', encoding='utf-8').read(); ids = set(re.findall(r'REQ-\\\\d+', t)); print(sorted(ids), len(ids))"`.
  Expected output: a set containing at least `{REQ-1, REQ-2, ..., REQ-10}` and `len(ids) >= 10`.
  Confirms requirement coverage in the produced document.
* **VC-8: Python style and type checks pass.** Run
  `uv run ruff check tasks/t0070_writeup_two_model_beds/code/ && uv run ruff format --check tasks/t0070_writeup_two_model_beds/code/ && uv run mypy tasks/t0070_writeup_two_model_beds/code/`.
  Expected output: zero errors from each. Confirms the matplotlib scripts conform to project Python
  style guide.
