"""Run the six-trial EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol on the deposited DSGC.

The deposited GUI-free HOC bundled with t0008 (``dsgc_model.hoc``) strips ``simplerun()``;
the canonical drive is ``apply_params -> init_active -> update -> placeBIP -> finitialize ->
continuerun``. Direction is encoded purely via ``h.gabaMOD`` (PD = 0.33, ND = 0.99) following
t0020's gabaMOD-swap protocol — no spatial rotation. HH activation is encoded via
``h.exptype``: 1 = active (HH on), 2 = TTX (HH off).

Per trial:

1. ``apply_params(h, seed=SEED)`` writes canonical conductances and the random-stream seed.
2. Set ``h.gabaMOD`` to ``GABA_MOD_PD`` (0.33) for PD or ``GABA_MOD_ND`` (0.99) for ND.
3. Apply per-mode overrides:
   * ``FULL``: ``h.exptype = 1`` (HH on).
   * ``EPSP_PASSIVE``: ``h.exptype = 2`` (HH off via TTX) and ``h.gabaMOD = 0`` (silence GABA).
   * ``IPSP_PASSIVE``: ``h.exptype = 2`` (HH off) and ``h.b2gampa = 0`` + ``h.b2gnmda = 0``.
4. ``h("init_active()")`` rebinds ``RGCsomana`` / ``RGCdendna`` per ``exptype``.
5. ``h("update()")`` writes the channel-density globals to all sections.
6. ``h("placeBIP()")`` lays the stimulus with the (now-overridden) conductance and direction
   parameters.
7. Attach fresh recorders, ``h.finitialize(V_INIT_MV)``, ``h.continuerun(TSTOP_MS)``.

Outputs:
* ``data/voltage_traces.csv`` long-format ``(mode, direction, t_ms, v_mv)``.
* ``results/metrics.json`` per-trial scalar summary.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import dataclass
from typing import Any

import numpy as np
from tqdm import tqdm

from tasks.t0008_port_modeldb_189347.code.build_cell import (
    SynapseCoords,
    apply_params,
    build_dsgc,
    get_cell_summary,
    load_neuron,
    read_synapse_coords,
)
from tasks.t0008_port_modeldb_189347.code.constants import (
    AP_THRESHOLD_MV,
    TSTOP_MS,
    V_INIT_MV,
)
from tasks.t0065_t0020_epsp_ipsp_vm_protocol.code.constants import (
    ACH_MOD_OFF,
    B_AMPA_OFF_NS,
    B_NMDA_OFF_NS,
    BASELINE_END_MS,
    BASELINE_V_MV_KEY,
    DIRECTION_COLUMN,
    EXPTYPE_HH_OFF,
    EXPTYPE_HH_ON,
    GABA_MOD_ND,
    GABA_MOD_OFF,
    GABA_MOD_PD,
    MODE_COLUMN,
    N_SAMPLES_KEY,
    PEAK_MINUS_BASELINE_MV_KEY,
    PEAK_V_MV_KEY,
    S_ACH_OFF_NS,
    S_GABA_OFF_NS,
    SEED,
    SPIKE_COUNT_KEY,
    T_MS_COLUMN,
    TRIAL_KEY_KEY,
    V_MV_COLUMN,
    Condition,
    TrialMode,
)
from tasks.t0065_t0020_epsp_ipsp_vm_protocol.code.paths import (
    DATA_DIR,
    METRICS_JSON,
    RESULTS_DIR,
    VOLTAGE_TRACES_CSV,
)


@dataclass(frozen=True, slots=True)
class TrialPlan:
    """One trial in the six-trial protocol."""

    mode: TrialMode
    condition: Condition

    @property
    def trial_key(self) -> str:
        return f"{self.mode.value}_{self.condition.value}"

    @property
    def gabamod_for_direction(self) -> float:
        return GABA_MOD_PD if self.condition == Condition.PD else GABA_MOD_ND

    @property
    def exptype(self) -> int:
        return EXPTYPE_HH_ON if self.mode == TrialMode.FULL else EXPTYPE_HH_OFF


@dataclass(frozen=True, slots=True)
class TrialResult:
    """One trial's recorded trace and per-trial scalar metrics."""

    plan: TrialPlan
    t_ms: np.ndarray
    v_mv: np.ndarray
    peak_v_mv: float
    baseline_v_mv: float
    peak_minus_baseline_mv: float
    spike_count: int
    n_samples: int


def _build_trial_plans() -> list[TrialPlan]:
    plans: list[TrialPlan] = []
    for mode in (TrialMode.FULL, TrialMode.EPSP_PASSIVE, TrialMode.IPSP_PASSIVE):
        for cond in (Condition.PD, Condition.ND):
            plans.append(TrialPlan(mode=mode, condition=cond))
    return plans


def _assert_bip_positions_baseline(
    *,
    h: Any,
    baseline: list[SynapseCoords],
) -> None:
    """Guard against silent re-engagement of the t0008 rotation proxy."""
    for s in baseline:
        assert h.RGC.BIPsyn[s.index].locx == s.bip_locx_um, (
            f"BIPsyn[{s.index}].locx = {h.RGC.BIPsyn[s.index].locx} "
            f"!= baseline {s.bip_locx_um}; rotation logic re-engaged?"
        )
        assert h.RGC.BIPsyn[s.index].locy == s.bip_locy_um, (
            f"BIPsyn[{s.index}].locy = {h.RGC.BIPsyn[s.index].locy} "
            f"!= baseline {s.bip_locy_um}; rotation logic re-engaged?"
        )


def _apply_mode_override(*, h: Any, mode: TrialMode) -> None:
    """Apply per-mode conductance overrides on top of the canonical apply_params write.

    EPSP_PASSIVE silences inhibition by zeroing both the GABA modulation envelope
    (``gabaMOD``) and the per-vesicle SAC GABA conductance (``s2ggaba``). IPSP_PASSIVE
    silences excitation by zeroing both bipolar pathways (``b2gampa``, ``b2gnmda``) and the
    SAC cholinergic pathway (``s2gach``, ``achMOD``). Belt-and-braces silencing prevents the
    deposited model's baseline noise envelope from leaking residual current into the
    silenced pathway.
    """
    if mode == TrialMode.FULL:
        return
    if mode == TrialMode.EPSP_PASSIVE:
        h.gabaMOD = float(GABA_MOD_OFF)
        h.s2ggaba = float(S_GABA_OFF_NS)
        return
    if mode == TrialMode.IPSP_PASSIVE:
        h.b2gampa = float(B_AMPA_OFF_NS)
        h.b2gnmda = float(B_NMDA_OFF_NS)
        h.s2gach = float(S_ACH_OFF_NS)
        h.achMOD = float(ACH_MOD_OFF)
        return
    raise ValueError(f"Unknown TrialMode: {mode}")


def _run_one_trial(
    *,
    h: Any,
    plan: TrialPlan,
    baseline: list[SynapseCoords],
) -> TrialResult:
    # Step 1: canonical params + per-trial seed.
    apply_params(h, seed=SEED)

    # Step 2: encode direction via h.gabaMOD (matches t0020 protocol).
    h.gabaMOD = float(plan.gabamod_for_direction)

    # Step 3: encode HH state via h.exptype, then re-init the active globals.
    h.exptype = int(plan.exptype)

    # Step 4: per-mode synaptic conductance overrides.
    _apply_mode_override(h=h, mode=plan.mode)

    # Step 5: rebind RGCsomana / RGCdendna based on exptype, then push the conductance globals
    # into the channel densities, then lay out the stimulus.
    h("init_active()")
    h("access RGC.soma")
    h("update()")
    h("placeBIP()")

    # Guard: BIP positions still at baseline.
    _assert_bip_positions_baseline(h=h, baseline=baseline)

    # Fresh recorders for the recorded run.
    v_rec: Any = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec: Any = h.Vector()
    t_rec.record(h._ref_t)
    spike_vec: Any = h.Vector()
    netcon: Any | None = None
    if plan.mode == TrialMode.FULL:
        netcon = h.NetCon(h.RGC.soma(0.5)._ref_v, None, sec=h.RGC.soma)
        netcon.threshold = float(AP_THRESHOLD_MV)
        netcon.record(spike_vec)

    h.finitialize(float(V_INIT_MV))
    h.continuerun(float(TSTOP_MS))

    v_arr: np.ndarray = np.array(list(v_rec), dtype=np.float64)
    t_arr: np.ndarray = np.array(list(t_rec), dtype=np.float64)
    if v_arr.size == 0:
        raise RuntimeError(
            f"No samples recorded for {plan.trial_key}; finitialize/continuerun did not run."
        )

    # Baseline = mean(v) for t < BASELINE_END_MS.
    baseline_mask: np.ndarray = t_arr < float(BASELINE_END_MS)
    if not bool(baseline_mask.any()):
        baseline_v_mv: float = float(V_INIT_MV)
    else:
        baseline_v_mv = float(v_arr[baseline_mask].mean())

    peak_v_mv: float = float(v_arr.max())
    peak_minus_baseline_mv: float = float(peak_v_mv - baseline_v_mv)

    spike_count: int = int(len(list(spike_vec))) if plan.mode == TrialMode.FULL else 0
    # Keep netcon reference alive for the run; releasing earlier would let NEURON GC it.
    del netcon

    return TrialResult(
        plan=plan,
        t_ms=t_arr,
        v_mv=v_arr,
        peak_v_mv=peak_v_mv,
        baseline_v_mv=baseline_v_mv,
        peak_minus_baseline_mv=peak_minus_baseline_mv,
        spike_count=spike_count,
        n_samples=int(v_arr.size),
    )


def _write_traces_csv(*, results: list[TrialResult]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with VOLTAGE_TRACES_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow([MODE_COLUMN, DIRECTION_COLUMN, T_MS_COLUMN, V_MV_COLUMN])
        for r in results:
            mode_str: str = r.plan.mode.value
            cond_str: str = r.plan.condition.value
            for t_val, v_val in zip(r.t_ms, r.v_mv, strict=True):
                writer.writerow([mode_str, cond_str, f"{float(t_val):.4f}", f"{float(v_val):.6f}"])


def _write_metrics_json(*, results: list[TrialResult]) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    payload: list[dict[str, Any]] = []
    for r in results:
        payload.append(
            {
                TRIAL_KEY_KEY: r.plan.trial_key,
                MODE_COLUMN: r.plan.mode.value,
                DIRECTION_COLUMN: r.plan.condition.value,
                PEAK_V_MV_KEY: r.peak_v_mv,
                BASELINE_V_MV_KEY: r.baseline_v_mv,
                PEAK_MINUS_BASELINE_MV_KEY: r.peak_minus_baseline_mv,
                SPIKE_COUNT_KEY: r.spike_count if r.plan.mode == TrialMode.FULL else None,
                N_SAMPLES_KEY: r.n_samples,
            }
        )
    METRICS_JSON.write_text(
        json.dumps({"trials": payload}, indent=2) + "\n",
        encoding="utf-8",
    )


def _print_summary(*, results: list[TrialResult]) -> None:
    print("\nPer-trial summary:", flush=True)
    header: str = (
        f"{'mode':<14} {'dir':<3} {'peak_v_mv':>10} {'base_v_mv':>10} "
        f"{'amp_mv':>8} {'spikes':>6} {'n':>6}"
    )
    print(header, flush=True)
    print("-" * len(header), flush=True)
    for r in results:
        spikes_str: str = f"{r.spike_count:>6}" if r.plan.mode == TrialMode.FULL else f"{'-':>6}"
        print(
            f"{r.plan.mode.value:<14} {r.plan.condition.value:<3} "
            f"{r.peak_v_mv:>10.3f} {r.baseline_v_mv:>10.3f} "
            f"{r.peak_minus_baseline_mv:>8.3f} {spikes_str} {r.n_samples:>6}",
            flush=True,
        )


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run the six-trial EPSP_PASSIVE / IPSP_PASSIVE / FULL protocol on the deposited "
            "Poleg-Polsky 2016 DSGC."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="If set, only run the first N trials (for smoke testing). Default: 6.",
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    limit: int | None = args.limit

    print("Bootstrapping NEURON and building deposited DSGC...", flush=True)
    h: Any = load_neuron()
    _ = h  # bootstrap side effect; build_dsgc loads the cell HOC
    h = build_dsgc()
    summary = get_cell_summary(h=h)
    baseline = read_synapse_coords(h=h)
    print(
        f"  countON={summary.num_on_sections} numsyn={summary.num_synapses}",
        flush=True,
    )

    plans: list[TrialPlan] = _build_trial_plans()
    if limit is not None:
        plans = plans[:limit]
    print(f"Running {len(plans)} trials (mode x direction).", flush=True)

    results: list[TrialResult] = []
    bar = tqdm(total=len(plans), desc="trials", unit="trial")
    for plan in plans:
        result = _run_one_trial(h=h, plan=plan, baseline=baseline)
        results.append(result)
        bar.update(1)
    bar.close()

    _write_traces_csv(results=results)
    _write_metrics_json(results=results)
    _print_summary(results=results)
    print(f"\nWrote {VOLTAGE_TRACES_CSV}", flush=True)
    print(f"Wrote {METRICS_JSON}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
