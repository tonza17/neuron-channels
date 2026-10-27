# Brainstorm Results Session 24

## Trigger

The researcher asked for a simple modelling test of an experimental finding: FVB/N rd1 retinal
ganglion cells (RGCs) show higher spontaneous activity, weaker evoked spiking, smaller voltage-gated
Na currents and larger sustained K currents than mature wild-type (WT) cells. The question is
whether the DSGC model reproduces this phenotype and what the remodelling does to direction
selectivity.

## Inputs Read

* Aggregator outputs: `aggregate_tasks`, `aggregate_suggestions --uncovered`, `aggregate_costs`.
* Results summaries for t0120-t0129 (geometry audit, 5-seed substrate rate, cytoplasm-volume, MI/ATP
  and DSI/ATP NSGA-II runs, signed-DSI rerun).
* `SomeResults.pdf` in the repository root (panels A-D): spontaneous activity, +60 pA current step,
  +100 mV voltage step, and a preliminary toy input-output concept.

## Decisions

1. **New task** - one standalone task `t0131_rd1_na_k_remodelling_dsgc_dsi` with four parts:
   voltage-clamp calibration of soma/AIS gNa and gK scaling against panel C; current-clamp
   prediction of panels A and B using those scalings; direction-selectivity protocol on WT-like and
   rd1-like cells; reproduction (or refutation) of the panel D toy input-output model. Dendritic
   channel scaling is a fallback arm if the soma/AIS-only remodelling does not reproduce the
   phenotype.
2. **Suggestion cleanup deferred** - the proposed rejections, downgrades and promotions (S-0113-01,
   S-0114-02, S-0116-06, S-0124-02, S-0129-03/05/06, S-0122-02) are postponed to the next brainstorm
   session at the researcher's request. No corrections are written in this session.
3. **t0128** is left untouched (in progress).
