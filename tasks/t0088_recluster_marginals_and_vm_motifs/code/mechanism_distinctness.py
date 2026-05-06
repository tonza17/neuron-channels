"""Phase C: synthesise mechanism-distinctness verdict across clusters.

Loads per-representative attribution JSONs, compares fractional NMDA / Nav1.6
/ NaP across clusters, produces verdict in {distinct, shared_mechanism,
mixed}, and writes ``mechanism_distinctness.json``.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from tasks.t0088_recluster_marginals_and_vm_motifs.code.paths import (
    MECHANISM_DISTINCTNESS_JSON,
    REPRESENTATIVE_CELLS_JSON,
    RESULTS_DATA_DIR,
)


@dataclass(frozen=True, slots=True)
class ClusterAttribution:
    cluster_id: int
    representative_cell_id: int
    frac_nmda: float
    frac_nav16: float
    frac_nap: float
    dominant_mechanism: str


def _load_attributions() -> list[ClusterAttribution]:
    reps_payload = json.loads(REPRESENTATIVE_CELLS_JSON.read_text(encoding="utf-8"))
    out: list[ClusterAttribution] = []
    for rep in reps_payload["representatives"]:
        cell_id = int(rep["representative_cell_id"])
        cluster_id = int(rep["cluster_id"])
        attribution_path = RESULTS_DATA_DIR / f"cell{cell_id}_attribution.json"
        assert attribution_path.exists(), f"Missing attribution: {attribution_path}"
        attribution = json.loads(attribution_path.read_text(encoding="utf-8"))
        out.append(
            ClusterAttribution(
                cluster_id=cluster_id,
                representative_cell_id=cell_id,
                frac_nmda=float(attribution["frac_nmda"]),
                frac_nav16=float(attribution["frac_nav16"]),
                frac_nap=float(attribution["frac_nap"]),
                dominant_mechanism=str(attribution["dominant_mechanism"]),
            )
        )
    return out


def _compute_verdict(*, attributions: list[ClusterAttribution]) -> dict[str, object]:
    """Decide the cross-cluster mechanism-distinctness verdict.

    Rules:
    * If all clusters share the same dominant mechanism: verdict =
      `shared_mechanism_different_scale`.
    * If clusters split into 2+ different dominant mechanisms: verdict =
      `distinct`.
    * `mixed` is reserved for future extension; not used here.
    """
    dominants: list[str] = [a.dominant_mechanism for a in attributions]
    unique_dominants: set[str] = set(dominants)
    if len(unique_dominants) == 1 and "none" not in unique_dominants:
        verdict = "shared_mechanism_different_scale"
    elif len(unique_dominants) >= 2:
        verdict = "distinct"
    else:
        verdict = "no_data"

    # Per-cluster narrative
    narratives: list[dict[str, object]] = []
    for a in attributions:
        narrative_str = (
            f"Cluster {a.cluster_id} (representative cell {a.representative_cell_id}): "
            f"frac NMDA = {a.frac_nmda:.3f}, frac Nav1.6 = {a.frac_nav16:.3f}, "
            f"frac NaP = {a.frac_nap:.3f}; dominant = {a.dominant_mechanism}."
        )
        narratives.append(
            {
                "cluster_id": a.cluster_id,
                "representative_cell_id": a.representative_cell_id,
                "frac_nmda": a.frac_nmda,
                "frac_nav16": a.frac_nav16,
                "frac_nap": a.frac_nap,
                "dominant_mechanism": a.dominant_mechanism,
                "narrative": narrative_str,
            }
        )

    # Fractional spread across clusters (range of frac for each channel).
    spread = {
        "nmda": max(a.frac_nmda for a in attributions) - min(a.frac_nmda for a in attributions),
        "nav16": max(a.frac_nav16 for a in attributions) - min(a.frac_nav16 for a in attributions),
        "nap": max(a.frac_nap for a in attributions) - min(a.frac_nap for a in attributions),
    }

    # t0084 baseline comparison: cell 767 NaP-dominant 93%, Nav1.6 7%, NMDA 0%.
    t0084_baseline = {
        "cell_id": 767,
        "frac_nmda": 0.0,
        "frac_nav16": 0.07,
        "frac_nap": 0.93,
        "dominant_mechanism": "nap",
        "directions": 8,
        "note": (
            "t0084 attribution computed at 8-direction angular resolution on cell 767 only. "
            "t0088 extends this to 16 directions and applies to per-cluster representatives."
        ),
    }

    return {
        "verdict": verdict,
        "n_clusters": len(attributions),
        "unique_dominants": sorted(unique_dominants),
        "fractional_spread_across_clusters": spread,
        "per_cluster_narrative": narratives,
        "t0084_baseline_cell_767": t0084_baseline,
        "verdict_rationale": (
            "Clusters use different dominant mechanisms across the per-representative "
            "PD-minus-ND attribution; mechanism-distinctness verdict = distinct."
            if verdict == "distinct"
            else (
                "All clusters share the same dominant mechanism in PD-minus-ND attribution; "
                "they differ in parameter scale (parameter-vector position in 54-d space) but "
                "not in which channel drives the PD response. verdict = "
                "shared_mechanism_different_scale."
                if verdict == "shared_mechanism_different_scale"
                else ("Insufficient or absent dominant-mechanism signal; verdict = no_data.")
            )
        ),
    }


def main() -> None:
    attributions = _load_attributions()
    print(
        f"[mechanism_distinctness] loaded {len(attributions)} per-cluster attributions",
        flush=True,
    )
    out = _compute_verdict(attributions=attributions)
    out["attributions"] = [asdict(a) for a in attributions]
    MECHANISM_DISTINCTNESS_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(
        f"[mechanism_distinctness] verdict = {out['verdict']}; "
        f"unique dominants = {out['unique_dominants']}",
        flush=True,
    )
    print(f"[mechanism_distinctness] wrote {MECHANISM_DISTINCTNESS_JSON}", flush=True)


if __name__ == "__main__":
    main()
