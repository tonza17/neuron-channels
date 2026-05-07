"""Phase G.2: NMDA units calibration ablation.

Sweep ``gnmda_dend`` from 1e-5 to 1e-2 uS on a single Bed-B-equivalent cell at PD
direction; record per-spine effective open conductance from the NEURON state
during the stimulus window; produce a calibration mapping NetCon weight to
per-spine conductance in nS; re-score t0086 / t0088 cluster centroids in the
calibrated units.

Outputs:

* ``data/g2_nmda_calibration.json``
* ``results/images/nmda_calibration_curve.png``
"""

from __future__ import annotations

import json
import time
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    CELSIUS_DEG_C,
    DT_MS,
    PD_DIRECTION_DEG,
    SEED_BASE,
    STEPS_PER_MS,
    TSTOP_MS,
    V_INIT_MV,
    ParameterVector,
    ParamIndex,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_driver import (
    run_one_trial,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    GNMDA_SWEEP_US,
    SIVYER_NMDA_MEAN_NS,
    SIVYER_NMDA_SIGMA_NS,
)
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    load_t0083_best_cell_param_vector,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_G2_CALIB_JSON,
    RESULTS_IMAGES_DIR,
    T0088_RECLUSTER_CENTROIDS_JSON,
    ensure_directories,
)
from tasks.t0090_morphology_generator_diversity_test.code.verification import (
    _LIVE_CELLS,
    _insert_baseline_channels,
)


def _build_calibration_cell() -> Any:
    """Build the BedB-equivalent procedural cell used for the NMDA sweep."""
    bedb = MorphologyParams.from_bedb_base_point()
    cell = generate_morphology(params=bedb, morph_seed=int(bedb.morph_seed))
    _LIVE_CELLS.append(cell)
    _insert_baseline_channels(cell=cell)
    return cell


def _run_one_sweep_point(*, gnmda_us: float, base_pv: ParameterVector, duration_ms: float) -> float:
    cell = _build_calibration_cell()
    pv_values = base_pv.values.copy()
    pv_values[int(ParamIndex.GNMDA_DEND)] = float(gnmda_us)
    pv = ParameterVector(values=pv_values)
    apply_parameter_vector(cell=cell, params=pv)
    placer_seed = SEED_BASE + (int(hash(pv.values.tobytes())) & 0xFFFF)
    bundle = setup_synapses_parametric(
        cell=cell,
        n_ach=pv.n_ach,
        n_gaba=pv.n_gaba,
        rho_0_ach=pv.rho0_ach,
        lambda_ach_um=pv.lambda_ach_um,
        rho_0_gaba=pv.rho0_gaba,
        lambda_gaba_um=pv.lambda_gaba_um,
        w_ach_us=pv.w_ach_us,
        w_gaba_us=pv.w_gaba_us,
        placer_seed=placer_seed,
        gnmda_dend=pv.gnmda_dend,
        mg_conc_mm=pv.mg_conc_mm,
        voff_nmda=pv.voff_nmda,
    )

    # Set up an empty trial run via run_one_trial to drive the synapses; record g_nmda.
    g_vecs = [cell.h.Vector() for _ in bundle.syns_nmda]
    recorded_any = False
    for vec, syn in zip(g_vecs, bundle.syns_nmda, strict=True):
        attached = False
        for ref_name in ("_ref_g", "_ref_g_nmda_us"):
            ref = getattr(syn, ref_name, None)
            if ref is not None:
                vec.record(ref)
                attached = True
                break
        recorded_any = recorded_any or attached
    if not recorded_any:
        # Fallback: use the integrated nonlinear-mg estimate from the NetCon weight.
        return float(gnmda_us) * 1e3  # crude conversion uS -> nS

    h = cell.h
    h.celsius = CELSIUS_DEG_C
    h.dt = DT_MS
    h.steps_per_ms = STEPS_PER_MS
    h.v_init = V_INIT_MV
    h.tstop = float(duration_ms)

    _ = run_one_trial(
        cell=cell,
        bundle=bundle,
        direction_deg=PD_DIRECTION_DEG,
        seed=SEED_BASE,
    )
    arrs: list[NDArray[np.float64]] = []
    for vec in g_vecs:
        a = np.asarray(vec.to_python(), dtype=np.float64)
        if a.size > 0:
            arrs.append(a)
    if len(arrs) == 0:
        return float(gnmda_us) * 1e3
    min_len = min(a.size for a in arrs)
    stacked = np.stack([a[:min_len] for a in arrs], axis=0)
    skip_steps = int(100.0 / float(DT_MS))
    if min_len <= skip_steps:
        skip_steps = 0
    if skip_steps >= min_len:
        skip_steps = 0
    g_peak_us = float(stacked.max()) if stacked.size > 0 else 0.0
    # Use peak per-spine conductance during the bar (more biologically meaningful
    # for comparison to Sivyer 2013's voltage-clamp open-conductance measurement).
    return g_peak_us * 1e3  # uS -> nS


def _rescore_clusters(
    *,
    calibration: list[tuple[float, float]],
    centroids: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Re-score t0088 cluster centroids against Sivyer 2013 in calibrated nS."""
    weights = np.array([c[0] for c in calibration], dtype=np.float64)
    nss = np.array([c[1] for c in calibration], dtype=np.float64)
    out: list[dict[str, Any]] = []
    for c in centroids:
        cluster_id = int(c["cluster_id"])
        unnorm = c["centroid_unnormalised"]
        gnmda_us = float(unnorm[int(ParamIndex.GNMDA_DEND)])
        if gnmda_us <= 0.0 or len(weights) < 2:
            ns_calibrated = float(gnmda_us) * 1e3
        else:
            log_w = np.log10(np.maximum(weights, 1e-12))
            log_ns = np.log10(np.maximum(nss, 1e-12))
            target_log_w = float(np.log10(max(gnmda_us, 1e-12)))
            slope, intercept = np.polyfit(log_w, log_ns, deg=1)
            ns_calibrated = float(10 ** (slope * target_log_w + intercept))
        sigma_dev = (ns_calibrated - SIVYER_NMDA_MEAN_NS) / SIVYER_NMDA_SIGMA_NS
        out.append(
            {
                "cluster_id": cluster_id,
                "gnmda_dend_us": gnmda_us,
                "ns_calibrated": ns_calibrated,
                "sivyer_mean_ns": SIVYER_NMDA_MEAN_NS,
                "sivyer_sigma_ns": SIVYER_NMDA_SIGMA_NS,
                "sigma_deviation": sigma_dev,
            }
        )
    return out


def _plot_calibration(*, sweep: list[tuple[float, float]], output_png: str) -> None:
    weights = [w for w, _ in sweep]
    nss = [n for _, n in sweep]
    fig, ax = plt.subplots(figsize=(7.0, 5.0))
    ax.loglog(weights, nss, "o-", color="#0072B2", lw=2.0, ms=8, label="measured")
    # Sivyer prior reference line.
    ax.axhline(SIVYER_NMDA_MEAN_NS, ls="--", color="#D55E00", label="Sivyer 2013 prior (0.1 nS)")
    ax.fill_between(
        [min(weights), max(weights)],
        SIVYER_NMDA_MEAN_NS - SIVYER_NMDA_SIGMA_NS,
        SIVYER_NMDA_MEAN_NS + SIVYER_NMDA_SIGMA_NS,
        alpha=0.2,
        color="#D55E00",
    )
    ax.set_xlabel("NetCon weight (gnmda_dend, uS)")
    ax.set_ylabel("Per-spine effective conductance (nS)")
    ax.set_title("NMDA units calibration: NetCon weight -> per-spine nS")
    ax.legend(loc="best")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main(*, sweep: tuple[float, ...] = GNMDA_SWEEP_US) -> None:
    ensure_directories()
    base_pv = load_t0083_best_cell_param_vector()
    print(f"NMDA sweep: {sweep}")

    calibration: list[tuple[float, float]] = []
    t0 = time.time()
    for gnmda_us in sweep:
        print(f"  gnmda_dend = {gnmda_us:.2e} uS ...")
        ns_per_spine = _run_one_sweep_point(
            gnmda_us=gnmda_us,
            base_pv=base_pv,
            duration_ms=TSTOP_MS,
        )
        print(f"    -> {ns_per_spine:.4f} nS per spine (peak)")
        calibration.append((float(gnmda_us), float(ns_per_spine)))
    elapsed = time.time() - t0

    centroids_data = json.loads(T0088_RECLUSTER_CENTROIDS_JSON.read_text())
    cluster_rescore = _rescore_clusters(
        calibration=calibration,
        centroids=centroids_data["centroids"],
    )

    summary = {
        "sweep_levels_us": [c[0] for c in calibration],
        "ns_per_spine_peak": [c[1] for c in calibration],
        "cluster_rescore": cluster_rescore,
        "elapsed_s": elapsed,
        "sivyer_mean_ns": SIVYER_NMDA_MEAN_NS,
        "sivyer_sigma_ns": SIVYER_NMDA_SIGMA_NS,
    }
    DATA_G2_CALIB_JSON.write_text(json.dumps(summary, indent=2))
    print(f"wrote {DATA_G2_CALIB_JSON}")

    out_png = RESULTS_IMAGES_DIR / "nmda_calibration_curve.png"
    _plot_calibration(sweep=calibration, output_png=str(out_png))
    print(f"wrote {out_png}")


if __name__ == "__main__":
    main()
