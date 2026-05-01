---
spec_version: "1"
task_id: "t0070_writeup_two_model_beds"
---
# Results Summary: Writeup of Two Standard DSGC Model Beds

## Summary

This task delivers a single, self-contained, presentation-ready research-paper document
(`results/results_detailed.md`) describing the two canonical direction-selective ganglion cell
(DSGC) model substrates that every other modelling task in the project uses as a backbone. **Bed A**
is the deposited Poleg-Polsky 2016 ON-OFF DRD4 DSGC ported in [t0008] (ModelDB 189347, library
`modeldb_189347_dsgc`), used by [t0020], [t0065], [t0067], [t0068], and [t0069]; **Bed B** is the de
Rosenroll 2026 DSGC ported in [t0024], used by [t0066]. Each bed section opens with the canonical
Hodgkin-Huxley membrane equation `C_m · dV/dt = -Σᵢ Iᵢ - I_syn - I_inj` rendered identically in
fenced math blocks, then enumerates every active conductance with `gbar`, `V_half`, kinetics, and
reversal potential in a markdown table, then defines the synaptic excitation and inhibition models
for the preferred direction (PD) and null direction (ND). A side-by-side comparison table at the end
summarises the headline differences across **18 dimensions**. Every numerical parameter carries a
`code/<file>:line` citation back to the committed source so the document is fully auditable.

The headline cross-bed differences are: **HH variant** (`HHst.mod` stochastic with `NF = 0` for Bed
A vs `HHst_noiseless.mod` deterministic for Bed B); **calcium currents** (Bed A zeros `CaL` and
`CaT` via `init_active`; Bed B leaves them at the `HHst_noiseless.mod` PARAMETER defaults of 3e-4
S/cm² each, plus a `cad` calcium-decay shell); **excitation mechanism** (Bed A's `bipNMDA`
POINT_PROCESS combines AMPA + voltage-dependent NMDA with a vesicular release model; Bed B uses
NEURON's built-in `Exp2Syn` for ACh and vendors `Exp2NMDA` but does not wire it into any driver);
**inhibition mechanism** (Bed A's `SACinhib` POINT_PROCESS with `gabaMOD = 0.33` (PD) / `0.99` (ND)
modulation-envelope scalar vs Bed B's `Exp2Syn` GABA with sigmoidal release-probability
`p_rel ≈ 0.05` (PD) / `0.80` (ND) and per-synapse arrival-time shift); and **PD/ND encoding
strategy** (Bed A keeps the bar geometry fixed and swaps a presynaptic envelope scalar; Bed B keeps
the conductances fixed and rotates the bar direction). These are fundamentally different encoding
strategies, not different parameterisations of the same mechanism.

The document is accompanied by four schematic PNGs in `results/images/`: two morphology diagrams
showing the 350-section dendritic tree topology with bed-specific synapse markers, and two PD-vs-ND
synaptic-conductance diagrams showing the analytically computed Exp2Syn / single- exponential traces
under each bed's direction-encoding mechanism. Every parameter in the detailed writeup carries a
`file:line` citation back to the committed code (the conductance and synaptic tables collectively
contain ~60 unique citations across `HHst.mod`, `HHst_noiseless.mod`, `bipolarNMDA.mod`,
`SAC2RGCinhib.mod`, `SAC2RGCexc.mod`, `Exp2NMDA.mod`, `cadecay.mod`, `RGCmodel.hoc`,
`RGCmodelGD.hoc`, `main.hoc`, `dsgc_model.hoc`, and the dependency tasks' `code/build_cell.py`,
`code/constants.py`, `code/run_*.py` files), making the entire document auditable against the
committed source tree.

## Metrics

* **Beds documented**: 2 (Bed A — t0008 deposited Poleg-Polsky 2016; Bed B — t0024 de Rosenroll 2026
  port).
* **Active conductances tabulated per bed**: **4** in Bed A (Na, Kdr, Km, Leak — Ca-L and Ca-T
  zeroed); **7** in Bed B (Na, Kdr, Km, Leak, CaL, CaT, plus `cad` calcium-decay shell).
* **Synapse types tabulated per bed**: **3** in Bed A (BIPsyn AMPA+NMDA, SACinhibsyn GABA, SACexcsyn
  ACh); **2 active + 1 latent** in Bed B (Exp2Syn ACh and Exp2Syn GABA active; Exp2NMDA vendored but
  not wired).
* **Side-by-side comparison rows**: **18** dimensions.
* **Schematic PNGs produced**: **4** (`bed_a_morphology.png` 345 KB, `bed_b_morphology.png` 146 KB,
  `bed_a_synaptic_diagram.png` 150 KB, `bed_b_synaptic_diagram.png` 159 KB).
* **Quantitative project metrics measured**: **0** (this is a documentation-only task; no NEURON
  simulations were run, so `results/metrics.json` is `{}` by design).

## Verification

* `verify_task_results t0070_writeup_two_model_beds` — see the orchestrator's post-implementation
  step report; the implementation document includes the mandatory frontmatter and all six mandatory
  sections per `arf/specifications/task_results_specification.md`.
* `ruff check --fix tasks/t0070_writeup_two_model_beds/code/` — PASSED (zero errors).
* `ruff format tasks/t0070_writeup_two_model_beds/code/` — PASSED (one file reformatted on first
  pass, idempotent on re-run).
* `mypy -p tasks.t0070_writeup_two_model_beds.code` — PASSED (zero errors with project mypy config;
  also zero errors when run with `--strict --explicit-package-bases` outside the project config).
* All four schematic PNGs were generated and exceed the size thresholds in the plan (morphology PNGs
  ≥ 30 KB, synaptic-diagram PNGs ≥ 20 KB).
