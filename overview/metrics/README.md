# Metrics (4)

## 📊 ratio (2)

<details>
<summary>📊 <strong>Direction Selectivity Index</strong>
(<code>direction_selectivity_index</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `direction_selectivity_index` |
| **Unit** | ratio |
| **Value type** | float |
| **Datasets** | — |

Classic DSI = (R_pref - R_null) / (R_pref + R_null), where R_pref and R_null are AP rates in
the preferred and null directions. Scalar summary of directional tuning strength, reported per
simulation condition.

</details>

<details>
<summary>📊 <strong>Tuning Curve Reliability</strong>
(<code>tuning_curve_reliability</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `tuning_curve_reliability` |
| **Unit** | ratio |
| **Value type** | float |
| **Datasets** | — |

Pearson correlation coefficient of the angle-to-AP-rate tuning curve across repeated noisy
trials. Measures robustness of directional tuning to stochastic synaptic or membrane noise;
1.0 means perfectly reproducible across trials, 0 means noise-dominated.

</details>

## ➖ none (2)

<details>
<summary>➖ <strong>Tuning Curve Half-Width at Half-Max (degrees)</strong>
(<code>tuning_curve_hwhm_deg</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `tuning_curve_hwhm_deg` |
| **Unit** | none |
| **Value type** | float |
| **Datasets** | — |

Angular half-width in degrees at which the AP rate drops to half of the peak rate. Measures
the sharpness of the directional tuning curve; lower values indicate steeper, more selective
tuning.

</details>

<details>
<summary>➖ <strong>Tuning Curve RMSE (Hz)</strong> (<code>tuning_curve_rmse</code>)</summary>

| Field | Value |
|---|---|
| **Key** | `tuning_curve_rmse` |
| **Unit** | none |
| **Value type** | float |
| **Datasets** | — |

Root-mean-square error in Hz between the simulated angle-to-AP-rate tuning curve and the
target tuning curve. Primary optimisation objective; captures absolute rates, preferred angle,
and curve shape in one scalar.

</details>
