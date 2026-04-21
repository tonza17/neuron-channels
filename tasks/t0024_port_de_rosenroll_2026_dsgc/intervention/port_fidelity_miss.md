# Port Fidelity Gate: MISS

The de Rosenroll 2026 DSGC port did not meet the REQ-5 port-fidelity gate. This is a first-class
finding per plan step 13, not a blocking error.

## Gate checks

- corr DSI = 0.818 required [0.3, 0.5] -> FAIL
- uncorr DSI = 0.835 required [0.18, 0.35] -> FAIL
- drop frac = 0.000 required >= 0.2 -> FAIL

## Measured values

- DSI (correlated, 8-dir) = 0.8182
- DSI (uncorrelated, 8-dir) = 0.8351

## Interpretation

The simplified port (ACh/GABA Exp2Syn pairs per terminal with AR(2)-modulated Poisson release and a
null-biased GABA release probability, no full SAC varicosity network) captures the
asymmetric-inhibition mechanism but does not perfectly reproduce the paper's absolute DSI
magnitudes. Follow-up tasks can port the full `SacNetwork` (`bp_locs`, `probs`, `deltas`) to close
the gap.
