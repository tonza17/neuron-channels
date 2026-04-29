# NMDAR-Escape Test with AMPA Priming on t0059 Substrate at PD with GABA = 0

## Source

User-commissioned diagnostic, parallel to t0061 but with AMPA priming. Goal: characterise how
co-located AMPA + NMDA (no GABA) responds to PD bar input across the same gNMDA range as t0061.

## Mechanism Choice

* **AMPA**: standard `Exp2Syn` (rise 0.5 ms, decay 2.5 ms, e = 0 mV), fixed at **gAMPA = 0.5 nS**.
* **NMDA**: t0055's `NMDA_MgBlock` (Jahr-Stevens voltage-dependent), swept gNMDA in
  {0.1, 0.5, 1, 2, 5, 10, 15, 20} nS.
* Both AMPA and NMDA at the same dendritic locations, driven by a shared NetStim. AMPA primes
  the cell with a fast (~10 ms) depolarization, partially unblocking Mg from the NMDA channel.

## Sweep

| Axis | Values |
| --- | --- |
| `GABA_BASE_NS` | **0** |
| `gAMPA_PRIMING_NS` | **0.5** (fixed) |
| Direction | theta = 0 deg only |
| Trials per condition | 1 |
| `gNMDA` (nS) | {0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0} |
| Mode | `FULL` and `EPSP_PASSIVE` |

Total: 8 gNMDA × 2 modes × 1 trial × 1 direction = **16 trials**.

## Outputs

Same shape as t0061: `voltage_traces_pd_only.csv`, `summary_pd_only.csv`, `wallclock.json`,
`placement_seed0.json`, `voltage_response_grid.png` (8 panels), `voltage_response_overlay.png`
(all 16 traces).

## Architecture

Reuses t0059's library for cell + placement and t0055's NMDA_MgBlock.mod (copied verbatim).
Each E location gets both an AMPA `Exp2Syn` and an `NMDA_MgBlock` POINT_PROCESS, both wired to
the same NetStim that fires once at bar-arrival time.

## Verification Criteria

* CSVs and 2 PNGs exist; verifiers pass.
