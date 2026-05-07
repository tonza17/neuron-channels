"""Tests: same (params, seed) -> identical sections, lengths, diameters, connectivity."""

from __future__ import annotations

from typing import Any

from tasks.t0090_morphology_generator_diversity_test.code.generator import (
    generate_morphology,
)
from tasks.t0090_morphology_generator_diversity_test.code.morphology_params import (
    MorphologyParams,
)


def _section_lengths(*, sections: list[Any]) -> list[float]:
    return [float(s.L) for s in sections]


def _section_diams(*, sections: list[Any]) -> list[float]:
    return [float(s.diam) for s in sections]


def test_determinism_default_bedb_base_point() -> None:
    """Two builds at the BedB base point with the same seed produce identical sections."""
    p = MorphologyParams.from_bedb_base_point()
    a = generate_morphology(params=p, morph_seed=12345)
    b = generate_morphology(params=p, morph_seed=12345)

    assert len(a.all_dends) == len(b.all_dends)
    assert _section_lengths(sections=a.all_dends) == _section_lengths(sections=b.all_dends)
    assert _section_diams(sections=a.all_dends) == _section_diams(sections=b.all_dends)
    assert a.connectivity == b.connectivity
    assert a.morphometric_summary.to_dict() == b.morphometric_summary.to_dict()


def test_determinism_different_seeds_differ() -> None:
    """Two seeds should generally produce different morphologies (not byte-identical)."""
    p = MorphologyParams.from_bedb_base_point()
    a = generate_morphology(params=p, morph_seed=12345)
    b = generate_morphology(params=p, morph_seed=99999)
    # Either section count or at least some lengths differ.
    same_n = len(a.all_dends) == len(b.all_dends)
    same_lengths = _section_lengths(sections=a.all_dends) == _section_lengths(sections=b.all_dends)
    assert not (same_n and same_lengths), "different seeds collided to the same morphology"


def test_round_trip_morphology_params() -> None:
    p = MorphologyParams.from_bedb_base_point()
    rebuilt = MorphologyParams.from_dict(data=p.to_dict())
    assert p == rebuilt
