"""Run the PD/ND gabaMOD-swap sweep.

Emits a two-point tuning-curve CSV at ``data/tuning_curves.csv`` with
columns ``(condition, trial_seed, firing_rate_hz)``. For each trial seed in
``range(n_trials)``, runs one PD trial (``h.gabaMOD = 0.33``) followed by
one ND trial (``h.gabaMOD = 0.99``).

Unlike t0008's rotation-proxy ``run_one_trial``, this driver keeps BIP
synapse coordinates fixed at their baseline values; direction selectivity
comes entirely from the inhibitory scalar swap. A per-trial assertion
guarantees the rotation logic does not silently re-engage.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from pathlib import Path
from typing import Any

from tqdm import tqdm

_NEURONHOME_DEFAULT: str = r"C:\Users\md1avn\nrn-8.2.7"
_NEURONHOME_SENTINEL_ENV: str = "_T0020_NEURONHOME_BOOTSTRAPPED"


def _ensure_neuron_importable() -> None:
    """Set NEURONHOME, put NEURON's Python bindings on sys.path, register DLL dir.

    The project's venv does not pip-install NEURON; the bindings ship
    with the system NEURON install at ``<NEURONHOME>/lib/python/neuron``.
    This function:

    1. Ensures ``NEURONHOME`` is set in the C runtime environment. NEURON's
       native layer reads ``NEURONHOME`` at the C level when the interpreter
       starts. Setting it via ``os.environ[...]`` inside Python does not
       propagate: by the time NEURON loads its default resources (via
       ``load_file('stdrun.hoc')``), it has already resolved its resource
       directory from the C env as it was at interpreter startup. If
       ``NEURONHOME`` is missing at interpreter startup, we re-exec this
       process with the variable set.
    2. Inserts ``<NEURONHOME>/lib/python`` into ``sys.path`` so the
       ``neuron`` package is importable.
    3. Calls ``os.add_dll_directory`` on ``<NEURONHOME>/bin`` so the
       ``hoc.pyd`` extension module can find its dependent DLLs
       (``libnrniv.dll`` and friends). Python 3.8+ on Windows no longer
       respects PATH for extension-module DLL loading.

    The function is idempotent across re-execs (guarded by a sentinel env
    var to prevent infinite re-exec loops).
    """
    # Step 1: if NEURONHOME is missing, re-exec ourselves with it set.
    if "NEURONHOME" not in os.environ:
        if os.environ.get(_NEURONHOME_SENTINEL_ENV) == "1":
            # We already tried to re-exec; if NEURONHOME still isn't
            # set, bail loudly rather than loop forever.
            raise RuntimeError(
                "NEURONHOME not set in environment after bootstrap re-exec; refusing to loop.",
            )
        os.environ["NEURONHOME"] = _NEURONHOME_DEFAULT
        os.environ[_NEURONHOME_SENTINEL_ENV] = "1"
        # os.execv replaces the current process image with a fresh one
        # whose C environ includes NEURONHOME. The child sees
        # _NEURONHOME_SENTINEL_ENV set so we do not re-exec again.
        os.execv(sys.executable, [sys.executable, *sys.argv])

    neuron_home = os.environ["NEURONHOME"]

    python_lib_dir = Path(neuron_home) / "lib" / "python"
    if python_lib_dir.is_dir() and str(python_lib_dir) not in sys.path:
        sys.path.insert(0, str(python_lib_dir))

    if sys.platform == "win32":
        bin_dir = Path(neuron_home) / "bin"
        if bin_dir.is_dir() and hasattr(os, "add_dll_directory"):
            os.add_dll_directory(str(bin_dir))


_ensure_neuron_importable()


from tasks.t0008_port_modeldb_189347.code.build_cell import (  # noqa: E402
    SynapseCoords,
    apply_params,
    build_dsgc,
    get_cell_summary,
    read_synapse_coords,
)
from tasks.t0020_port_modeldb_189347_gabamod.code.constants import (  # noqa: E402
    AP_THRESHOLD_MV,
    CONDITION_COLUMN,
    FIRING_RATE_COLUMN,
    GABA_MOD_ND,
    GABA_MOD_PD,
    N_TRIALS_PER_CONDITION,
    TRIAL_SEED_COLUMN,
    TSTOP_MS,
    V_INIT_MV,
    Condition,
)
from tasks.t0020_port_modeldb_189347_gabamod.code.paths import (  # noqa: E402
    DATA_DIR,
    TUNING_CURVES_CSV,
)


def _assert_bip_positions_baseline(
    *,
    h: Any,
    baseline_coords: list[SynapseCoords],
) -> None:
    """Assert every BIPsyn (locx, locy) matches the baseline snapshot.

    This guards against silent re-engagement of the t0008 rotation-proxy.
    If this assertion fires, the gabaMOD-swap protocol has been corrupted.
    """
    for s in baseline_coords:
        assert h.RGC.BIPsyn[s.index].locx == s.bip_locx_um, (
            f"BIPsyn[{s.index}].locx = {h.RGC.BIPsyn[s.index].locx} "
            f"!= baseline {s.bip_locx_um}; rotation logic re-engaged?"
        )
        assert h.RGC.BIPsyn[s.index].locy == s.bip_locy_um, (
            f"BIPsyn[{s.index}].locy = {h.RGC.BIPsyn[s.index].locy} "
            f"!= baseline {s.bip_locy_um}; rotation logic re-engaged?"
        )


def run_one_trial_gabamod(
    *,
    h: Any,
    gabamod_value: float,
    seed: int,
    baseline_coords: list[SynapseCoords],
) -> float:
    """Run a single trial; return the somatic spike count / (tstop_s).

    Applies canonical paper parameters, overrides ``h.gabaMOD`` to the
    condition-specific scalar, asserts BIP positions stay at baseline,
    records soma voltage, runs ``finitialize`` + ``continuerun``, and
    counts upward threshold crossings of ``V_{soma}`` above
    ``AP_THRESHOLD_MV``.
    """
    # apply_params writes h.gabaMOD = GABA_MOD (=0.33). We override it
    # immediately after, and the HOC placeBIP() proc reads the global
    # when the inhibitory point processes are next evaluated.
    apply_params(h, seed=seed)
    h.gabaMOD = gabamod_value

    # Re-run update() and placeBIP() so the inhibitory point processes
    # pick up the new gabaMOD scalar (matches t0008's per-trial flow,
    # minus the rotation call).
    h("update()")
    h("placeBIP()")

    # Critical guard: after placeBIP re-seats the synapses, verify BIP
    # positions are still at their baseline values. If rotation logic
    # leaked back in, this assertion fires.
    _assert_bip_positions_baseline(h=h, baseline_coords=baseline_coords)

    v_rec = h.Vector()
    v_rec.record(h.RGC.soma(0.5)._ref_v)
    t_rec = h.Vector()
    t_rec.record(h._ref_t)

    h.finitialize(V_INIT_MV)
    h.continuerun(TSTOP_MS)

    # Count upward threshold crossings (rising-edge count, matching
    # t0008's run_one_trial).
    samples: list[float] = list(v_rec)
    spike_count = 0
    above = samples[0] >= AP_THRESHOLD_MV
    for val in samples[1:]:
        now_above = val >= AP_THRESHOLD_MV
        if now_above and not above:
            spike_count += 1
        above = now_above

    tstop_s = TSTOP_MS / 1000.0
    return float(spike_count) / tstop_s


def _build_trial_plan(
    *,
    n_trials_per_condition: int,
) -> list[tuple[Condition, int]]:
    """Produce interleaved (condition, seed) pairs: PD, ND for each seed."""
    plan: list[tuple[Condition, int]] = []
    for trial_idx in range(n_trials_per_condition):
        seed = trial_idx + 1
        plan.append((Condition.PD, seed))
        plan.append((Condition.ND, seed))
    return plan


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=("Run the PD/ND gabaMOD-swap sweep and emit data/tuning_curves.csv."),
    )
    parser.add_argument(
        "--n-trials",
        type=int,
        default=N_TRIALS_PER_CONDITION,
        help=(
            "Number of trials per condition (default: "
            f"{N_TRIALS_PER_CONDITION}). Total trials = 2 * n_trials."
        ),
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help=(
            "If set, process only this many total trials (for smoke "
            "testing). Default: process all trials."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = _parse_args()
    n_trials: int = args.n_trials
    limit: int | None = args.limit
    assert n_trials > 0, "n_trials must be positive"

    print("Building DSGC for gabaMOD-swap sweep...", flush=True)
    h = build_dsgc()
    summary = get_cell_summary(h=h)
    baseline = read_synapse_coords(h=h)
    print(
        f"  countON={summary.num_on_sections} numsyn={summary.num_synapses}",
        flush=True,
    )

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    plan = _build_trial_plan(n_trials_per_condition=n_trials)
    if limit is not None:
        plan = plan[:limit]

    total_trials = len(plan)
    bar = tqdm(total=total_trials, desc="trials", unit="trial")
    rows: list[tuple[str, int, float]] = []
    for condition, seed in plan:
        gabamod_value = GABA_MOD_PD if condition == Condition.PD else GABA_MOD_ND
        rate = run_one_trial_gabamod(
            h=h,
            gabamod_value=gabamod_value,
            seed=seed,
            baseline_coords=baseline,
        )
        rows.append((condition.value, seed, rate))
        bar.update(1)
    bar.close()

    with TUNING_CURVES_CSV.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(
            [CONDITION_COLUMN, TRIAL_SEED_COLUMN, FIRING_RATE_COLUMN],
        )
        for cond_val, seed_val, rate_val in rows:
            writer.writerow([cond_val, seed_val, f"{rate_val:.6f}"])

    # Quick summary for sanity checking.
    pd_rates = [r[2] for r in rows if r[0] == Condition.PD.value]
    nd_rates = [r[2] for r in rows if r[0] == Condition.ND.value]
    if len(pd_rates) > 0:
        mean_pd = sum(pd_rates) / len(pd_rates)
        print(
            f"  PD (n={len(pd_rates)}): mean = {mean_pd:6.2f} Hz",
            flush=True,
        )
    else:
        mean_pd = 0.0
        print("  PD: (no trials)", flush=True)
    if len(nd_rates) > 0:
        mean_nd = sum(nd_rates) / len(nd_rates)
        print(
            f"  ND (n={len(nd_rates)}): mean = {mean_nd:6.2f} Hz",
            flush=True,
        )
    else:
        mean_nd = 0.0
        print("  ND: (no trials)", flush=True)

    denom = mean_pd + mean_nd
    if denom > 0.0:
        dsi_estimate = (mean_pd - mean_nd) / denom
        print(f"  DSI estimate: {dsi_estimate:.4f}", flush=True)
    else:
        print("  DSI estimate: (undefined; both means zero)", flush=True)

    print(f"\nWrote {TUNING_CURVES_CSV}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
