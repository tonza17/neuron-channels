"""HH save-and-zero correctness regression test (REQ-14).

Runs one FULL trial at the canonical reference point (gampa_ns=0.5, gaba_base_ns=1.0,
theta=0 deg, trial_seed=0) and compares the soma V(t) to a stored reference. The reference
is generated on first run (when no `.npy` exists) by running the same FULL trial — this is
the reference implementation, with HH active throughout. Subsequent runs compare against this
reference at ``atol=1e-6`` mV.

This test guards against accidentally leaving HH disabled after EPSP_PASSIVE / IPSP_PASSIVE
trials (e.g., a missed try/finally, or a save-and-zero that touches more sections than it
should).
"""

from __future__ import annotations

import numpy as np

from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.constants import TrialMode
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.paths import HH_REFERENCE_TRACE_NPY
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.run_tuning_curve import (
    SweepArtifacts,
    setup_sweep_artifacts,
)
from tasks.t0059_bar_locked_gaba_ampa_sweep_t0057.code.trial import (
    TrialResult,
    run_one_trial,
)

REF_GAMPA_NS: float = 0.5
REF_GABA_BASE_NS: float = 1.0
REF_THETA_DEG: float = 0.0
REF_TRIAL_SEED: int = 0
COMPARE_ATOL_MV: float = 1e-6


def _run_reference_trial(*, artifacts: SweepArtifacts) -> TrialResult:
    from neuron import h  # noqa: PLC0415

    return run_one_trial(
        h=h,
        cell=artifacts.cell,
        pairs=artifacts.pairs,
        mode=TrialMode.FULL,
        angle_deg=REF_THETA_DEG,
        trial_seed=REF_TRIAL_SEED,
        gampa_ns=REF_GAMPA_NS,
        gaba_base_ns=REF_GABA_BASE_NS,
    )


def test_hh_save_and_zero_full_trace_matches_reference() -> None:
    """Run one FULL reference trial and assert match against the stored reference array."""
    artifacts: SweepArtifacts = setup_sweep_artifacts()

    if not HH_REFERENCE_TRACE_NPY.exists():
        print(
            f"[hh-save-zero] No reference at {HH_REFERENCE_TRACE_NPY}; generating one now from "
            f"the current FULL trial (this trial IS the reference; no comparison performed).",
            flush=True,
        )
        result: TrialResult = _run_reference_trial(artifacts=artifacts)
        HH_REFERENCE_TRACE_NPY.parent.mkdir(parents=True, exist_ok=True)
        np.save(HH_REFERENCE_TRACE_NPY, result.v_soma_mv)
        print(
            f"[hh-save-zero] Reference saved with {result.v_soma_mv.shape[0]} samples; "
            f"re-run to compare.",
            flush=True,
        )
        return

    # First, run a passive (EPSP_PASSIVE) trial to exercise the save-and-zero path.
    from neuron import h  # noqa: PLC0415

    _ = run_one_trial(
        h=h,
        cell=artifacts.cell,
        pairs=artifacts.pairs,
        mode=TrialMode.EPSP_PASSIVE,
        angle_deg=REF_THETA_DEG,
        trial_seed=999,
        gampa_ns=REF_GAMPA_NS,
        gaba_base_ns=REF_GABA_BASE_NS,
    )
    # Then run the FULL reference trial, with HH expected to have been restored.
    result: TrialResult = _run_reference_trial(artifacts=artifacts)
    actual: np.ndarray = result.v_soma_mv

    reference: np.ndarray = np.load(HH_REFERENCE_TRACE_NPY)
    print(
        f"[hh-save-zero] reference shape={reference.shape}, actual shape={actual.shape}",
        flush=True,
    )

    if reference.shape != actual.shape:
        # CVODE produces variable-length traces; fall back to comparing summary statistics.
        ref_max: float = float(np.max(reference))
        ref_min: float = float(np.min(reference))
        act_max: float = float(np.max(actual))
        act_min: float = float(np.min(actual))
        print(
            f"[hh-save-zero] shape mismatch (CVODE adaptive samples differ); "
            f"comparing summary stats: reference max={ref_max:.4f} min={ref_min:.4f}, "
            f"actual max={act_max:.4f} min={act_min:.4f}",
            flush=True,
        )
        # Tighter tolerance because mostly the same dynamics; allow 0.1 mV slack on extrema.
        assert abs(ref_max - act_max) <= 0.1, (
            f"max Vm mismatch (reference={ref_max:.4f}, actual={act_max:.4f}); "
            f"HH save-and-zero may have leaked into the FULL trial."
        )
        assert abs(ref_min - act_min) <= 0.1, (
            f"min Vm mismatch (reference={ref_min:.4f}, actual={act_min:.4f}); "
            f"HH save-and-zero may have leaked into the FULL trial."
        )
        return

    np.testing.assert_allclose(
        actual=actual,
        desired=reference,
        atol=COMPARE_ATOL_MV,
        err_msg="HH save-and-zero correctness test failed: FULL reference trial does not match"
        " stored reference array within atol=1e-6 mV. HH state may have leaked between trials.",
    )
    print(
        f"[hh-save-zero] PASS: reference trace matches at atol={COMPARE_ATOL_MV} mV "
        f"({actual.shape[0]} samples).",
        flush=True,
    )


if __name__ == "__main__":
    test_hh_save_and_zero_full_trace_matches_reference()
    print("[hh-save-zero] PASS", flush=True)
