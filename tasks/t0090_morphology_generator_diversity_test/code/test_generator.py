"""Edge-case + sanity tests for the procedural DSGC morphology generator."""

from __future__ import annotations

import math

import numpy as np

from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    _compute_nseg,
    _get_neuron_h,
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)

_RNG = np.random.default_rng(7)


def _params_with(*, num_primary: int, max_depth: int) -> MorphologyParams:
    base = MorphologyParams.from_bedb_base_point().to_dict()
    base["num_primary_branches"] = int(num_primary)
    base["max_strahler_depth"] = int(max_depth)
    return MorphologyParams.from_dict(data=base)


def test_min_branches_three_primaries_depth_two() -> None:
    p = _params_with(num_primary=3, max_depth=2)
    cell = generate_morphology(params=p, morph_seed=42)
    assert len(cell.primary_dends) == 3
    assert len(cell.all_dends) >= 3


def test_max_branches_seven_primaries_depth_six() -> None:
    p = _params_with(num_primary=7, max_depth=6)
    cell = generate_morphology(params=p, morph_seed=43)
    assert len(cell.primary_dends) == 7


def test_no_nan_lengths_or_diameters_for_random_draws() -> None:
    base = MorphologyParams.from_bedb_base_point().to_dict()
    for trial in range(10):
        # Mutate a few params to random plausible values.
        d = dict(base)
        d["mean_segment_length_um"] = float(_RNG.uniform(15.0, 50.0))
        d["mean_branching_angle_deg"] = float(_RNG.uniform(35.0, 80.0))
        d["rall_exponent"] = float(_RNG.uniform(0.7, 1.8))
        d["branch_length_cv"] = float(_RNG.uniform(0.0, 0.4))
        d["primary_branch_pd_concentration"] = float(_RNG.uniform(0.0, 4.0))
        d["morph_seed"] = int(_RNG.integers(1, 2**31 - 1))
        p = MorphologyParams.from_dict(data=d)
        cell = generate_morphology(params=p, morph_seed=int(d["morph_seed"]))
        for sec in cell.all_dends:
            assert sec.L > 0.0, f"section L <= 0 at trial {trial}"
            assert sec.diam > 0.0, f"section diam <= 0 at trial {trial}"
            assert not math.isnan(sec.L), f"section L NaN at trial {trial}"
            assert not math.isnan(sec.diam), f"section diam NaN at trial {trial}"


def test_nseg_dlambda_returns_odd_positive() -> None:
    """For L in [10, 600] um, _compute_nseg returns an odd integer >= 1."""
    h = _get_neuron_h()
    sec = h.Section(name="t90_nseg_probe")
    sec.diam = 1.0
    sec.Ra = 100.0
    sec.cm = 1.0
    for length in (10.0, 50.0, 100.0, 250.0, 600.0):
        sec.L = length
        nseg = _compute_nseg(h=h, section=sec)
        assert nseg >= 1, f"nseg < 1 at L={length}"
        assert nseg % 2 == 1, f"nseg not odd at L={length}: nseg={nseg}"


def test_connectivity_no_orphans() -> None:
    p = MorphologyParams.from_bedb_base_point()
    cell = generate_morphology(params=p, morph_seed=11)
    section_names = {s.name() for s in cell.all_dends}
    section_names.add("soma_t90")
    for child_name, parent_name in cell.connectivity.items():
        # In NEURON the "name()" is e.g. "dend_p0_d1_n0_t90", we strip off the suffix.
        parent_short = parent_name + "_t90" if parent_name == "soma" else parent_name + "_t90"
        if parent_name == "soma":
            assert parent_short == "soma_t90"
        else:
            assert parent_short in section_names, f"parent {parent_short} missing"
        child_short = child_name + "_t90"
        assert child_short in section_names, f"child {child_short} missing"


def test_round_trip_via_to_from_dict() -> None:
    p = MorphologyParams.from_bedb_base_point()
    p2 = MorphologyParams.from_dict(data=p.to_dict())
    assert p == p2
