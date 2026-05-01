# Plot synaptic conductances and currents for PD and ND on both model beds

## Motivation

The t0070 / t0071 writeups document every synaptic-current equation analytically (canonical
`I_syn(t,V) = g_syn(t,V) · (V − E_syn)` form per channel, with parameters and direction-encoding
mechanism). What they do NOT show is the actual time-domain shape of these conductances and currents
during a real trial — i.e., what does `g_AMPA(t)` actually look like across the bar sweep, and how
does the PD vs ND swap reshape `g_GABA(t)`? Visual traces make the direction-encoding mechanism
viscerally obvious in a way the equations alone cannot.

This task records every synaptic state variable (`gAMPA`, `gNMDA`, `g` for SACinhib/SACexc, `g` for
Exp2Syn) during one PD and one ND trial on each model bed, then plots the population mean ± SD per
synapse type. Result: a presentation-ready figure pair (one per bed) showing exactly how each
synaptic conductance (and the resulting current) evolves over time, and how PD vs ND differ.

## Scope

* **Two model beds**:
  * **Bed A** — t0008 deposited Poleg-Polsky, with the t0020 gabaMOD-swap protocol applied (PD:
    `gabaMOD = 0.33`; ND: `gabaMOD = 0.99`). 282 ON dendrites, each carrying one BIPsyn (AMPA +
    NMDA), one SACinhibsyn (GABA), and one SACexcsyn (ACh). 4 synapse types to plot.
  * **Bed B** — t0024 de Rosenroll port. Uses moving-bar angle for direction encoding, with
    per-event Bernoulli release sigmoid (PD: bar at preferred angle; ND: bar at null angle, i.e.
    rotated 180°). Active synapses on this bed are Exp2Syn ACh and Exp2Syn GABA. 2 synapse types to
    plot.
* **Two directions per bed**: PD and ND, single trial each, fixed seed for reproducibility.
* **Trial duration**: full bar-sweep duration as defined by each bed's existing driver (~1000 ms for
  Bed A; whatever t0066's protocol uses for Bed B).
* **Quantities recorded per synapse**:
  * Conductance state: `g(t)` in nS (or µS for Bed B; converted to nS for plotting consistency).
  * Local membrane voltage at the synapse insertion point: `v_local(t)` in mV.
  * Current: `I(t) = g(t) · (v_local(t) − E_rev)` computed post-hoc, in pA.
* **Aggregation**: across all synapse instances of a given type, compute mean and SD at each
  recorded time point. Plot mean as a solid line, ±1 SD as a shaded band.

## Approach

1. For each bed, write a driver script that:
   * Builds the cell using the existing dependency-task code (no modification of t0008 / t0020 /
     t0024 source files).
   * Sets the direction (PD or ND) via the canonical mechanism for that bed.
   * Iterates over every synapse instance of every type, attaches NEURON Vector recorders to the
     relevant `_ref_g` (or `_ref_gAMPA` / `_ref_gNMDA` for Bed A's BIPsyn) plus the local membrane
     voltage `_ref_v` at the synapse's section.
   * Runs `h.continuerun(tstop)`.
   * Saves raw traces to `data/` as compressed numpy arrays (one .npz per
     `bed × direction × synapse_type`).
2. Compute population mean ± SD across synapses for each synapse type, in each direction.
3. Compute currents from g(t) and v_local(t) post-hoc, then average across synapses.
4. Generate two figures (one per bed):
   * Bed A figure: 4 rows (AMPA, NMDA, GABA, ACh), 2 columns (g(t), I(t)), PD and ND overlaid in
     each panel as solid lines with shaded ±SD bands.
   * Bed B figure: 2 rows (ACh, GABA), 2 columns (g(t), I(t)), same overlay format.
5. Optionally add a third "comparison" figure showing the dendritic spatial pattern of per-synapse
   mean conductance (e.g., heatmap over the dendritic tree) — only if it doesn't significantly
   increase task time.
6. Author a `results/results_detailed.md` writeup describing methodology and the visible PD vs ND
   structure (e.g., "Bed A: AMPA/NMDA/ACh traces are identical between PD and ND because excitation
   is direction-symmetric on this bed; only g_GABA differs, scaled by gabaMOD"). Render to
   `results/results_detailed.pdf` via Typst (consistent with t0071).

## Outputs

* `tasks/t0072_synaptic_traces_pd_nd/code/{paths,constants,record_synapses,plot_traces, render_pdf}.py`
  — driver, plot generator, PDF compiler.
* `tasks/t0072_synaptic_traces_pd_nd/data/bed_a_{pd,nd}_{ampa,nmda,gaba,ach}.npz` and
  `bed_b_{pd,nd}_{ach,gaba}.npz` — raw per-synapse traces (compressed numpy).
* `tasks/t0072_synaptic_traces_pd_nd/results/images/bed_a_synaptic_traces.png` — Bed A figure (4
  rows × 2 cols).
* `tasks/t0072_synaptic_traces_pd_nd/results/images/bed_b_synaptic_traces.png` — Bed B figure (2
  rows × 2 cols).
* `tasks/t0072_synaptic_traces_pd_nd/results/results_summary.md` — abstract.
* `tasks/t0072_synaptic_traces_pd_nd/results/results_detailed.md` + `.typ` + `.pdf` — full writeup.
* `tasks/t0072_synaptic_traces_pd_nd/results/{metrics,costs,remote_machines_used}.json` +
  `suggestions.json` — standard bookkeeping.

## Compute and budget

* Local Windows workstation. Each bed simulation is ~1-3 seconds for one trial; with recorders on
  every synapse (282 × 3 types for Bed A, plus voltage on each section), expect 10-30 seconds per
  trial. Total: < 5 minutes wall-clock.
* External costs: $0.
* Disk: raw .npz traces ~10-50 MB total; PDF ~1 MB.
* Time estimate: 2-3 hours (most of it is the driver code + plotting).

## Dependencies

Six tasks: t0008 (Bed A cell builder), t0020 (Bed A gabaMOD protocol), t0024 (Bed B cell builder),
t0065 / t0066 (EPSP/IPSP/FULL protocol drivers — for tstop and direction conventions), t0070 (the
writeup these traces complement), t0071 (the Typst PDF pipeline reused here).

## Risks and fallbacks

| # | Risk | Detection | Fallback |
| --- | --- | --- | --- |
| 1 | Recording vectors on 282 synapses × 3 types × 4 sections each may consume >2 GB RAM. | OOM error or slow execution. | Reduce recording dt from default `h.dt` (~25 µs) to 1 ms; subsample to 1 sample per ms. |
| 2 | Bed B's Exp2Syn `g` accessor returns the post-factor conductance directly (not the raw A/B states). | g(t) shape doesn't match the canonical bi-exponential. | Document: Bed B's `g` is the post-factor conductance, ready for the I = g·(v-e) computation. No bug. |
| 3 | Bed A's BIPsyn release model is stochastic; per-synapse traces are noisy. | Individual traces look like sparse spikes. | Population mean ± SD across 282 synapses smooths this out (this is the whole point of plotting the population, not one synapse). |
| 4 | Bed B's PD/ND encoding requires correctly-set bar angle in the t0024 driver; misconfiguring it yields wrong asymmetry. | Bed B GABA traces look identical between PD and ND. | Mirror t0066's PD/ND configuration exactly; cite source line. |
| 5 | Typst PDF compilation fails on the new figures. | Compile error. | Fallback to embedding PNGs as raster only (no MathML) or use t0071's working render_pdf.py verbatim. |

## Verification criteria

* All 6 (Bed A: 4 + Bed B: 2) synapse types have raw .npz traces in `data/`.
* Both PNG figures exist and are non-trivial (>50 KB each, > 5 panels each).
* PD and ND lines are visibly different on at least the GABA channel (Bed A) and the GABA channel
  (Bed B).
* `results_detailed.md`, `.typ`, and `.pdf` all exist.
* All standard verificators pass.

## Task Requirement Checklist

* **REQ-1**: Bed A — record `gAMPA(t)`, `gNMDA(t)` from every BIPsyn instance, in PD and ND.
* **REQ-2**: Bed A — record `g(t)` from every SACinhibsyn (GABA) and SACexcsyn (ACh), PD and ND.
* **REQ-3**: Bed B — record `g(t)` from every Exp2Syn ACh and Exp2Syn GABA instance, PD and ND.
* **REQ-4**: Compute `I(t) = g(t) · (v_local(t) − E_rev)` post-hoc for every synapse.
* **REQ-5**: Aggregate to population mean ± SD per synapse type per direction.
* **REQ-6**: Bed A figure: 4 rows × 2 cols (g and I per synapse type), PD and ND overlaid.
* **REQ-7**: Bed B figure: 2 rows × 2 cols, PD and ND overlaid.
* **REQ-8**: Both figures embedded in `results_detailed.md` with descriptive captions.
* **REQ-9**: Typst-typeset PDF produced (consistent with t0071 pipeline).
* **REQ-10**: Discussion in `results_detailed.md` highlighting which traces differ between PD and ND
  for each bed, and what that reveals about the direction-encoding mechanism.
