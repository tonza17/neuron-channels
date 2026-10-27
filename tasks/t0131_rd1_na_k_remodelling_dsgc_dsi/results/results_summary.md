# Results Summary: rd1-like Na/K Remodelling of the DSGC Model and Its Effect on DSI

## Summary

Local NEURON experiments on 8 LEGIT reference cells tested whether scaling soma and AIS Na and K
conductances reproduces the researcher's rd1 phenotype (panels A to D). The headline is mostly
negative: only the panel C sustained-current ratio is reproduced (**1.63 to 1.70** on all 8 cells,
every fit at the grid edge s_Na = 0.25), while evoked firing, spontaneous hyperactivity, signed DSI
and the panel D predictions could not be reproduced because rd1-like cells never spike at the
pre-declared -10 mV threshold.

## Metrics

* **Sustained-current ratio** (rd1-like / WT-like): mean **1.674**, range **1.631 to 1.698**, 8 of 8
  cells within 0.15 of 1.7, all fits at s_Na = **0.25** and s_K = **2.36 to 3.0**
* **Na transient ratio**: mean **0.455** (range 0.399 to 0.573) against a 0.25 target, so the
  transient reduction is only partly reproduced
* **WT-like spontaneous rate**: median **73.5 Hz** (mean 78.5 Hz) without any input, versus **0 Hz**
  for rd1-like (panel A shows the opposite); +60 pA changes nothing (40.75 vs 40.88 mean spikes)
* **Signed DSI, WT-like**: median **0.874** (PD **86.7 Hz**, ND **3.1 Hz**), 8 of 8 cells defined
* **Signed DSI, rd1-like**: undefined (`None`) on **8 of 8** cells with and without bias, and on 5
  of 5 cells in the dendritic arm
* **Panel D**: toy model matches **11 of 11** by-eye anchors within 20% (fitted to them); NEURON
  disproves **4 of 4** predictions
* **Cost**: **$0**, local CPU only

## Verification

* `verify_task_results.py` — see the final run recorded in `results_detailed.md` (0 errors
  required)
* Unit tests `code/test_scaling_and_clamp.py` and `code/test_toy_model.py` — final run **8
  passed** (two earlier runs had one failure each, fixed before the final run; see
  `logs/commands/041_20261027T162721Z_uv-run-pytest.json`)
