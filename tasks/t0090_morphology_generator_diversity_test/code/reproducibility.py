"""Phase F: Bed-B reproducibility check on 5 t0083 Pareto cells.

For each of 5 random t0083 Pareto cells (deterministic seed):

1. Build the procedural cell at the BedB-equivalent base point.
2. Apply the cell's 54-d parameter vector via ``apply_parameter_vector``.
3. Run the 8-direction protocol; compute DSI + PD-rate.
4. Compare to the cell's original t0083 Pareto values.

Pass criterion (relaxed from the task description's 5 percent to 10 percent per
plan rationale): |delta| <= 10 percent on both DSI and PD-rate.
"""

from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any, cast

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np

from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.apply_params import (
    apply_parameter_vector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.build_cell_ais import (
    DSGCCellWithAIS,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ANGLES_8DIR_DEG as ANGLES_8DIR_DEG_T80,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.constants import (
    ND_DIRECTION_DEG,
    PD_DIRECTION_DEG,
    SEED_BASE,
    TSTOP_MS,
    ParameterVector,
)
from tasks.t0080_bedb_mobo_v3_dendritic_spike_nsga2.code.trial_helpers import (
    setup_synapses_parametric,
)
from tasks.t0090_morphology_generator_diversity_test.code.constants import (
    BEDB_PARETO_CHOICE_SEED,
)
from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.load_default_params import (
    cell_record_to_param_vector,
    load_t0083_pareto_cells,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)
from tasks.t0090_morphology_generator_diversity_test.code.paths import (
    DATA_BEDB_REPRO_JSON,
    RESULTS_IMAGES_DIR,
    ensure_directories,
)
from tasks.t0090_morphology_generator_diversity_test.code.verification import (
    _LIVE_CELLS,
    _insert_baseline_channels,
    _run_8direction_protocol,
)

N_CELLS: int = 5


@dataclass(frozen=True, slots=True)
class ReproEntry:
    cell_index: int
    original_dsi: float
    original_pd_rate_hz: float
    procedural_dsi: float
    procedural_pd_rate_hz: float
    procedural_nd_rate_hz: float
    dsi_delta_pct: float
    pd_rate_delta_pct: float
    pass_10pct: bool
    elapsed_s: float
    spikes_per_direction: dict[float, int]
    error: str | None


def _to_dict(*, e: ReproEntry) -> dict[str, Any]:
    return {
        "cell_index": e.cell_index,
        "original_dsi": e.original_dsi,
        "original_pd_rate_hz": e.original_pd_rate_hz,
        "procedural_dsi": e.procedural_dsi,
        "procedural_pd_rate_hz": e.procedural_pd_rate_hz,
        "procedural_nd_rate_hz": e.procedural_nd_rate_hz,
        "dsi_delta_pct": e.dsi_delta_pct,
        "pd_rate_delta_pct": e.pd_rate_delta_pct,
        "pass_10pct": bool(e.pass_10pct),
        "elapsed_s": e.elapsed_s,
        "spikes_per_direction": {
            f"{k:.1f}": int(v) for k, v in sorted(e.spikes_per_direction.items())
        },
        "error": e.error,
    }


def _delta_pct(*, procedural: float, reference: float) -> float:
    if abs(reference) < 1e-9:
        return 0.0 if abs(procedural) < 1e-9 else 100.0
    return float(100.0 * (procedural - reference) / reference)


def select_5_pareto_cells(*, seed: int = BEDB_PARETO_CHOICE_SEED) -> list[dict[str, Any]]:
    """Deterministically pick 5 cells from the t0083 Pareto front."""
    cells = load_t0083_pareto_cells()
    rng = np.random.default_rng(seed)
    n_pareto = len(cells)
    indices = rng.choice(n_pareto, size=N_CELLS, replace=False)
    return [cells[int(i)] for i in indices]


def evaluate_one_cell(
    *,
    cell_record: dict[str, Any],
    bedb_params: MorphologyParams,
) -> ReproEntry:
    """Build procedural cell, apply vector, run 8-direction protocol, compute deltas."""
    t0 = time.time()
    cell_index = int(cell_record["cell_index"])
    original_dsi = float(cell_record["dsi"])
    original_pd = float(cell_record["pd_rate_hz"])

    pv: ParameterVector = cell_record_to_param_vector(cell=cell_record)

    try:
        cell = generate_morphology(params=bedb_params, morph_seed=int(bedb_params.morph_seed))
        _LIVE_CELLS.append(cell)
        _insert_baseline_channels(cell=cell)
        apply_parameter_vector(cell=cast(DSGCCellWithAIS, cell), params=pv)
        placer_seed = SEED_BASE + (int(hash(pv.values.tobytes())) & 0xFFFF)
        bundle = setup_synapses_parametric(
            cell=cast(DSGCCellWithAIS, cell),
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
        spikes_by_angle = _run_8direction_protocol(
            cell=cell,
            bundle=bundle,
            angles_deg=ANGLES_8DIR_DEG_T80,
            seed_base=SEED_BASE + cell_index,
        )
    except (RuntimeError, ValueError, ArithmeticError, AssertionError) as exc:
        return ReproEntry(
            cell_index=cell_index,
            original_dsi=original_dsi,
            original_pd_rate_hz=original_pd,
            procedural_dsi=0.0,
            procedural_pd_rate_hz=0.0,
            procedural_nd_rate_hz=0.0,
            dsi_delta_pct=100.0,
            pd_rate_delta_pct=100.0,
            pass_10pct=False,
            elapsed_s=time.time() - t0,
            spikes_per_direction={},
            error=f"{type(exc).__name__}: {exc}",
        )

    pd_count = spikes_by_angle.get(PD_DIRECTION_DEG, 0)
    nd_count = spikes_by_angle.get(ND_DIRECTION_DEG, 0)
    pd_rate = pd_count / (TSTOP_MS / 1000.0)
    nd_rate = nd_count / (TSTOP_MS / 1000.0)
    denom = pd_count + nd_count
    proc_dsi = float((pd_count - nd_count) / denom) if denom > 0 else 0.0

    dsi_delta = _delta_pct(procedural=proc_dsi, reference=original_dsi)
    pd_delta = _delta_pct(procedural=pd_rate, reference=original_pd)
    pass_ok = abs(dsi_delta) <= 10.0 and abs(pd_delta) <= 10.0

    return ReproEntry(
        cell_index=cell_index,
        original_dsi=original_dsi,
        original_pd_rate_hz=original_pd,
        procedural_dsi=proc_dsi,
        procedural_pd_rate_hz=pd_rate,
        procedural_nd_rate_hz=nd_rate,
        dsi_delta_pct=dsi_delta,
        pd_rate_delta_pct=pd_delta,
        pass_10pct=pass_ok,
        elapsed_s=time.time() - t0,
        spikes_per_direction=spikes_by_angle,
        error=None,
    )


def _plot_polar_panel(*, entries: list[ReproEntry], output_png: str | None = None) -> None:
    """5-panel polar plot showing procedural (solid) vs reference (dashed)."""
    fig, axes = plt.subplots(1, 5, figsize=(20.0, 4.5), subplot_kw={"projection": "polar"})
    for ax, entry in zip(axes, entries, strict=True):
        angles = sorted(entry.spikes_per_direction.keys())
        rates = [entry.spikes_per_direction[a] / (TSTOP_MS / 1000.0) for a in angles]
        if len(angles) > 0:
            theta = np.deg2rad(angles + [angles[0]])
            rho = rates + [rates[0]]
            ax.plot(theta, rho, marker="o", label="procedural", color="#0072B2")
        ax.set_title(
            f"cell {entry.cell_index}\n"
            f"DSI: {entry.procedural_dsi:.2f} vs {entry.original_dsi:.2f} "
            f"(delta {entry.dsi_delta_pct:+.1f}%)",
            fontsize=8,
        )
    fig.suptitle("Bed-B reproducibility: procedural vs t0083 Pareto", fontsize=12)
    fig.tight_layout()
    if output_png is not None:
        fig.savefig(output_png, dpi=150, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    ensure_directories()
    bedb_params = MorphologyParams.from_bedb_base_point()
    cells = select_5_pareto_cells()
    print(f"loaded {len(cells)} t0083 Pareto cells: {[int(c['cell_index']) for c in cells]}")

    entries: list[ReproEntry] = []
    for cell in cells:
        e = evaluate_one_cell(cell_record=cell, bedb_params=bedb_params)
        print(
            f"cell {e.cell_index}: dsi {e.procedural_dsi:+.3f} vs {e.original_dsi:+.3f} "
            f"(delta {e.dsi_delta_pct:+.1f}%), "
            f"pd {e.procedural_pd_rate_hz:.2f} vs {e.original_pd_rate_hz:.2f} "
            f"(delta {e.pd_rate_delta_pct:+.1f}%), pass={e.pass_10pct}"
        )
        entries.append(e)

    out = [_to_dict(e=e) for e in entries]
    DATA_BEDB_REPRO_JSON.write_text(json.dumps(out, indent=2))
    print(f"wrote {DATA_BEDB_REPRO_JSON}")

    polar_png = RESULTS_IMAGES_DIR / "bedb_polar_comparison.png"
    _plot_polar_panel(entries=entries, output_png=str(polar_png))
    print(f"wrote {polar_png}")

    n_pass = sum(1 for e in entries if e.pass_10pct)
    print(f"summary: {n_pass}/{len(entries)} cells pass within 10 pct on both DSI and PD-rate")


if __name__ == "__main__":
    main()
