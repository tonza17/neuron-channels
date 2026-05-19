# Smoke Gate Failure

Anchor 1 PD-rate None not within 1.0 Hz of expected 43.6.

Per-anchor results: [
  {
    "anchor_index": 0,
    "anchor_name": "bedb_like",
    "dsi_vector_sum": null,
    "pd_rate_hz": null,
    "robustness": null,
    "is_unstable": true,
    "n_errors": 1,
    "elapsed_s": 0.0,
    "error": "Compiled t0080 MOD library not found. Run nrnivmodl on the mods/ folder. Tried: C:\\Users\\md1avn\\Documents\\GitHub\\neuron-channels-worktrees\\t0112_t0106_seed77_replicate\\tasks\\t0080_bedb_mobo_v3_dendritic_spike_nsga2\\code\\build\\nrnmech.dll.",
    "pd_within_tolerance": false,
    "dsi_within_tolerance": false,
    "expected_pd_rate_hz": 43.6
  },
  {
    "anchor_index": 1,
    "anchor_name": "symmetric",
    "dsi_vector_sum": -1.0,
    "pd_rate_hz": 0.0,
    "robustness": 0.0,
    "is_unstable": true,
    "n_errors": 1,
    "elapsed_s": 0.013209342956542969,
    "error": null
  },
  {
    "anchor_index": 2,
    "anchor_name": "pd_asymmetric",
    "dsi_vector_sum": -1.0,
    "pd_rate_hz": 0.0,
    "robustness": 0.0,
    "is_unstable": true,
    "n_errors": 1,
    "elapsed_s": 0.015184402465820312,
    "error": null
  },
  {
    "anchor_index": 3,
    "anchor_name": "nd_asymmetric",
    "dsi_vector_sum": -1.0,
    "pd_rate_hz": 0.0,
    "robustness": 0.0,
    "is_unstable": true,
    "n_errors": 1,
    "elapsed_s": 0.013873100280761719,
    "error": null
  },
  {
    "anchor_index": 4,
    "anchor_name": "alt_topology",
    "dsi_vector_sum": -1.0,
    "pd_rate_hz": 0.0,
    "robustness": 0.0,
    "is_unstable": true,
    "n_errors": 1,
    "elapsed_s": 0.005948543548583984,
    "error": null
  }
]
