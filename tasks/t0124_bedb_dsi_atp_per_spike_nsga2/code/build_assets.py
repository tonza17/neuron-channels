"""Build the t0123 answer asset (REQ-25).

Creates ``tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/answer/
dsgc-bits-per-atp-vs-niven-2007/`` with:

* ``details.json`` per ``meta/asset_types/answer/specification.md``.
* ``short_answer.md`` -- 2-5 sentences starting with "Yes" / "No" /
  "Partially" / "Insufficient evidence".
* ``full_answer.md`` -- canonical full answer describing the Niven 2007
  comparison, the top-10 cells' Strong-Bialek bits/s, the Sengupta 2010
  ATP recipe, and the Carter-Bean 2009 calibration.
"""

from __future__ import annotations

import argparse
import json
import math
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.constants import T0124_SEEDS
from tasks.t0124_bedb_dsi_atp_per_spike_nsga2.code.paths import (
    RESULTS_DATA_DIR,
    TASK_ROOT,
)

ANSWER_ID: str = "dsgc-bits-per-atp-vs-niven-2007"
ASSET_DIR: Path = TASK_ROOT / "assets" / "answer" / ANSWER_ID
DETAILS_PATH: Path = ASSET_DIR / "details.json"
SHORT_ANSWER_PATH: Path = ASSET_DIR / "short_answer.md"
FULL_ANSWER_PATH: Path = ASSET_DIR / "full_answer.md"

QUESTION: str = (
    "Where does the DSGC bits-per-ATP front sit relative to Niven 2007's "
    "fly-photoreceptor curve, and does it match the Niven super-linear "
    "cost-vs-information scaling?"
)
SHORT_TITLE: str = "DSGC bits-per-ATP vs Niven 2007 fly-photoreceptor cost-vs-information scaling"


def _load_strong_bialek_top10() -> dict[str, Any]:
    path = RESULTS_DATA_DIR / "post_hoc_strong_bialek_mi_top10.json"
    if not path.exists():
        return {"cells": [], "n_top_cells": 0}
    return json.loads(path.read_text(encoding="utf-8"))


def _fit_log_log_exponent(
    *, atp_values: list[float], bits_values: list[float]
) -> tuple[float, float] | None:
    """Fit log(bits) = p * log(atp) + b via least squares; return (p, r^2)."""
    finite = [(a, b) for a, b in zip(atp_values, bits_values, strict=True) if a > 0 and b > 0]
    if len(finite) < 2:
        return None
    log_a = [math.log(a) for a, _ in finite]
    log_b = [math.log(b) for _, b in finite]
    n = len(log_a)
    mean_x = sum(log_a) / n
    mean_y = sum(log_b) / n
    num = sum((log_a[i] - mean_x) * (log_b[i] - mean_y) for i in range(n))
    den = sum((log_a[i] - mean_x) ** 2 for i in range(n))
    if den == 0.0:
        return None
    slope = num / den
    intercept = mean_y - slope * mean_x
    pred = [slope * x + intercept for x in log_a]
    ss_res = sum((log_b[i] - pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y - mean_y) ** 2 for y in log_b)
    r_squared = 1.0 if ss_tot == 0.0 else 1.0 - ss_res / ss_tot
    return (float(slope), float(r_squared))


def _summarise_strong_bialek(*, sb_data: dict[str, Any]) -> dict[str, Any]:
    cells = sb_data.get("cells", [])
    atp_values: list[float] = []
    bits_values: list[float] = []
    r_squared_per_cell: list[float] = []
    for c in cells:
        atp = c.get("atp_per_spike_molecules")
        bits = c.get("bits_per_sec")
        if (
            isinstance(atp, int | float)
            and isinstance(bits, int | float)
            and math.isfinite(float(atp))
            and math.isfinite(float(bits))
        ):
            atp_values.append(float(atp))
            bits_values.append(float(bits))
        r2_raw = c.get("r_squared")
        if isinstance(r2_raw, int | float) and math.isfinite(float(r2_raw)):
            r_squared_per_cell.append(float(r2_raw))
    fit = _fit_log_log_exponent(atp_values=atp_values, bits_values=bits_values)
    mean_r2: float | None = (
        float(sum(r_squared_per_cell) / len(r_squared_per_cell))
        if len(r_squared_per_cell) > 0
        else None
    )
    return {
        "n_cells": int(len(cells)),
        "atp_values": atp_values,
        "bits_values": bits_values,
        "p_exponent": fit[0] if fit is not None else None,
        "fit_r_squared": fit[1] if fit is not None else None,
        "mean_r_squared_per_cell": mean_r2,
    }


def _verdict_text(*, summary: dict[str, Any]) -> tuple[str, str]:
    n = int(summary["n_cells"])
    p_exp = summary.get("p_exponent")
    fit_r2 = summary.get("fit_r_squared")
    if n < 10 or p_exp is None or fit_r2 is None:
        return ("Insufficient evidence", "Insufficient evidence")
    if fit_r2 < 0.5:
        return ("Insufficient evidence", "Insufficient evidence")
    if p_exp > 1.0:
        return ("Yes", "Yes")
    if p_exp <= 0.0:
        return ("No", "No")
    return ("Partially", "Partially")


def _build_short_answer(
    *,
    seed: int,
    summary: dict[str, Any],
    date_answered: str,
) -> str:
    n = int(summary["n_cells"])
    p_exp = summary.get("p_exponent")
    fit_r2 = summary.get("fit_r_squared")
    verdict_word, _ = _verdict_text(summary=summary)
    p_str = f"{p_exp:.3f}" if isinstance(p_exp, int | float) else "n/a"
    r2_str = f"{fit_r2:.3f}" if isinstance(fit_r2, int | float) else "n/a"
    if verdict_word == "Insufficient evidence":
        body = (
            f"Insufficient evidence. The t0123 single-seed NSGA-II run "
            f"produced {n} top-Pareto cells under the post-hoc Strong-Bialek "
            f"1998 direct method; the log-log fit exponent p = {p_str} at "
            f"r^2 = {r2_str} is too noisy (n < 10 or r^2 < 0.5) to make a "
            f"definitive statement about super-linear scaling."
        )
    elif verdict_word == "Yes":
        body = (
            f"Yes. The t0123 top-{n} DSGC cells trace a super-linear "
            f"bits-per-ATP curve consistent with Niven 2007's fly-photoreceptor "
            f"scaling: log-log fit exponent p = {p_str} (> 1.0) at r^2 = {r2_str}."
        )
    elif verdict_word == "No":
        body = (
            f"No. The t0123 top-{n} DSGC cells do NOT trace the Niven 2007 "
            f"super-linear scaling: log-log fit exponent p = {p_str} (<= 0) "
            f"at r^2 = {r2_str}; the cells exhibit a flat or inverse "
            f"bits-per-ATP relationship rather than the fly-photoreceptor "
            f"super-linear curve."
        )
    else:  # Partially
        body = (
            f"Partially. The t0123 top-{n} DSGC cells exhibit a sub-linear "
            f"bits-per-ATP trend (log-log p = {p_str} at r^2 = {r2_str}); the "
            f"front rises with ATP per spike but the slope is shallower than "
            f"Niven 2007's super-linear (p > 1.0) fly-photoreceptor curve."
        )
    return (
        f"---\n"
        f'spec_version: "2"\n'
        f'answer_id: "{ANSWER_ID}"\n'
        f'answered_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"\n'
        f'date_answered: "{date_answered}"\n'
        f"---\n\n"
        f"## Question\n\n"
        f"{QUESTION}\n\n"
        f"## Answer\n\n"
        f"{body}\n\n"
        f"## Sources\n\n"
        f"* Paper: `10.1103_PhysRevLett.80.197` (Strong et al. 1998)\n"
        f"* External: Niven et al. 2007 (https://doi.org/10.1242/jeb.005249)\n"
        f"* Task: `t0124_bedb_dsi_atp_per_spike_nsga2`\n"
        f"* Predictions asset: "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/predictions/"
        f"nsga2-mi-atp-per-spike-bedb-morph`\n"
        f"* Chart: "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/"
        f"niven_2007_comparison.png`\n"
        f"* Chart: "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/"
        f"carter_bean_atp_per_ap_check.png`\n"
    )


def _build_full_answer(
    *,
    seed: int,
    summary: dict[str, Any],
    sb_data: dict[str, Any],
    date_answered: str,
    confidence: str,
) -> str:
    n = int(summary["n_cells"])
    p_exp = summary.get("p_exponent")
    fit_r2 = summary.get("fit_r_squared")
    verdict_word, _ = _verdict_text(summary=summary)
    p_str = f"{p_exp:.3f}" if isinstance(p_exp, int | float) else "n/a"
    r2_str = f"{fit_r2:.3f}" if isinstance(fit_r2, int | float) else "n/a"
    cells = sb_data.get("cells", [])
    per_cell_lines: list[str] = []
    for c in cells:
        rank = c.get("rank", c.get("cell_index", "?"))
        atp = c.get("atp_per_spike_molecules")
        bits = c.get("bits_per_sec")
        r2 = c.get("r_squared")
        atp_s = f"{atp:.3e}" if isinstance(atp, int | float) else "n/a"
        bits_s = f"{bits:.1f}" if isinstance(bits, int | float) else "n/a"
        r2_s = f"{r2:.3f}" if isinstance(r2, int | float) else "n/a"
        per_cell_lines.append(f"| {rank} | {atp_s} | {bits_s} | {r2_s} |")
    per_cell_table = (
        "\n".join(per_cell_lines) if len(per_cell_lines) > 0 else ("| -- | -- | -- | -- |")
    )
    return (
        f"---\n"
        f'spec_version: "2"\n'
        f'answer_id: "{ANSWER_ID}"\n'
        f'answered_by_task: "t0124_bedb_dsi_atp_per_spike_nsga2"\n'
        f'date_answered: "{date_answered}"\n'
        f'confidence: "{confidence}"\n'
        f"---\n\n"
        f"## Question\n\n"
        f"{QUESTION}\n\n"
        f"## Short Answer\n\n"
        f"{verdict_word}. The t0123 single-seed NSGA-II run produced {n} "
        f"top-Pareto cells re-evaluated under the post-hoc Strong-Bialek "
        f"1998 direct method (8 directions x 20 trials). The log-log fit "
        f"`log(bits_per_sec) = p * log(atp_per_spike) + b` returned exponent "
        f"`p = {p_str}` at `r^2 = {r2_str}`. Niven 2007's fly-photoreceptor "
        f"scaling fits `p ~ 1.5` at the 4-species level (D. melanogaster "
        f"200 bits/s to S. carnaria 1000 bits/s across an order of "
        f"magnitude in ATP per spike).\n\n"
        f"## Research Process\n\n"
        f"The answer was produced from a single in-silico experiment "
        f"executed by this task. The procedure: (1) fork the t0122 "
        f"NSGA-II substrate end-to-end, swap both F-axes to (MI_count_bits, "
        f"ATP_per_spike_molecules), raise N_DIRECTIONS to 4 (antipodal "
        f"pairs at 0/90/180/270 deg), and wire per-segment `seg.ina` "
        f"recording for the Sengupta 2010 ATP recipe; (2) provision a "
        f"Vast.ai EPYC instance and run the Carter-Bean 2009 ATP/AP/cm "
        f"calibration on the canonical Bed B anchor cell (within +/-30% "
        f"of 2.41e21 ATP/cm); (3) run NSGA-II for up to 60 generations at "
        f"pop=96, N_EVAL_SEEDS=3 under the $6 cost cap and $5 per-instance "
        f"watchdog; (4) at termination, take the top-10 Pareto cells by "
        f"`mi_count_bits` and re-run each at 8 directions x 20 trials per "
        f"direction under the Strong-Bialek 1998 direct method with 1/T "
        f"extrapolation at T in {{25, 50, 75, 100}} ms; (5) fit the log-log "
        f"`bits_per_sec vs atp_per_spike` exponent across the top cells "
        f"and compare to Niven 2007's reported super-linear `p > 1.0` "
        f"scaling.\n\n"
        f"## Evidence from Papers\n\n"
        f"**Niven et al. 2007** (`10.1242_jeb.005249`, J Exp Biol 210, "
        f"1797) is the primary reference. The paper reports information "
        f"rates of 4 fly-photoreceptor species: D. melanogaster ~200 "
        f"bits/s, D. virilis ~400 bits/s, M. domestica ~700 bits/s, S. "
        f"carnaria ~1000 bits/s, alongside a fixed ~20% baseline ATP cost "
        f"and a super-linear scaling exponent between information rate "
        f"and ATP per spike across the 4 species.\n\n"
        f"**Strong et al. 1998** (`10.1103_PhysRevLett.80.197`, Phys Rev "
        f"Lett 80, 197) describes the direct-method MI estimator used for "
        f"the bits/s rate: discretise each trial into binary words of "
        f"length T, compute H_total - <H_noise> at each T, fit MI/T "
        f"against 1/T, intercept = bits/s.\n\n"
        f"**Carter & Bean 2009** is used as the calibration anchor for "
        f"the Sengupta 2010 ATP recipe: AIS ATP/AP/cm ~4 mM-mol/cm = "
        f"2.41e21 ATP/cm. The smoke gate aborts the NSGA-II launch if the "
        f"recipe's output deviates by more than 30% on the canonical Bed "
        f"B anchor cell.\n\n"
        f"**Sengupta 2010** is the methodological anchor for ATP per "
        f"spike: integrate inward Na current (`seg.ina`) over per-AP +/-2 "
        f"ms windows, multiply by per-segment area in cm^2, divide by "
        f"elementary charge `e = 1.602e-19 C` and by the Na+/K+ ATPase "
        f"stoichiometry factor of 3.\n\n"
        f"## Evidence from Internet Sources\n\n"
        f"No external internet sources were used beyond the published "
        f"papers cited above. The Niven 2007 reference values (4 fly "
        f"photoreceptor species at ~200, ~400, ~700, and ~1000 bits/s) "
        f"are taken directly from the paper at "
        f"`https://doi.org/10.1242/jeb.005249` and reproduced verbatim in "
        f"`code/build_pareto_plots.py:NIVEN_2007_SPECIES`. The Strong & "
        f"Bialek 1998 direct-method MI estimator is reproduced from the "
        f"paper at `https://doi.org/10.1103/PhysRevLett.80.197` and "
        f"implemented in `code/mi_estimator.py:"
        f"compute_mi_strong_bialek_bits_per_sec`. No supplementary "
        f"datasets or web tools were consulted.\n\n"
        f"## Evidence from Code or Experiments\n\n"
        f"The t0123 NSGA-II run plus post-hoc Strong-Bialek re-evaluation "
        f"of the top-10 Pareto cells is the primary code-experiment "
        f"evidence. Per-cell results:\n\n"
        f"| Rank | ATP/spike (molecules) | bits/s | 1/T fit r^2 |\n"
        f"|------|----------------------|--------|-------------|\n"
        f"{per_cell_table}\n\n"
        f"The log-log fit across these {n} cells returned `p = {p_str}` "
        f"at `r^2 = {r2_str}`. The supporting code is in "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/code/` "
        f"(`atp_per_spike.py`, `mi_estimator.py`, `evaluator.py`, "
        f"`nsga2_driver.py`, `post_hoc_strong_bialek.py`, "
        f"`build_pareto_plots.py`). Per-cell bits/s values are in "
        f"`results/data/post_hoc_strong_bialek_mi_top10.json`; the "
        f"comparison chart with the Niven curve overlay is at "
        f"`results/images/niven_2007_comparison.png`.\n\n"
        f"## Synthesis\n\n"
        f"Niven 2007's prediction is that the cost-vs-information curve "
        f"for spike-based codes scales super-linearly (`p > 1`) across "
        f"the 4 fly-photoreceptor species: a 5x increase in ATP per spike "
        f"buys a >5x increase in bits/s. The t0123 NSGA-II run tests "
        f"whether the same scaling holds for an in-silico DSGC substrate "
        f"under explicit (max MI, min ATP/spike) selection pressure.\n\n"
        f"The verdict (`{verdict_word}`) is read off the log-log fit "
        f"exponent (`p = {p_str}`) against the Niven super-linear "
        f"threshold (`p > 1.0`). The 1/T extrapolation r^2 per cell is "
        f"the secondary diagnostic for whether the Strong-Bialek estimate "
        f"is reliable; lower r^2 indicates that the spike-time word "
        f"distribution is too noisy at the {{25, 50, 75, 100}} ms range "
        f"to give a reliable bits/s rate.\n\n"
        f"## Limitations\n\n"
        f"* **Single GA seed**. Cross-seed replication is deferred to a "
        f"follow-up task; the bits/s distribution may be wider when more "
        f"seeds are sampled.\n"
        f"* **Top-10 cells only**. The Strong-Bialek rerun was limited to "
        f"the top-10 cells to fit the $6 cost cap; a larger sample would "
        f"tighten the log-log fit.\n"
        f"* **Niven 2007 4-species anchor**. The Niven 2007 reference "
        f"curve is anchored at only 4 species; the super-linear `p ~ 1.5` "
        f"exponent has wide uncertainty.\n"
        f"* **DSGC vs photoreceptors**. The Niven 2007 comparison is "
        f"across phyla and cell types; matching DSGC bits-per-ATP to fly "
        f"photoreceptors is suggestive rather than definitive.\n"
        f"* **Spike-count vs spike-time codes**. The inner-loop MI is a "
        f"spike-count code (4 directions x 3 seeds = 12 trials, 2-bit "
        f"ceiling); the post-hoc Strong-Bialek is the spike-time code. "
        f"Their disagreement on any single cell is informative for the "
        f"trade-off but complicates the comparison to Niven's "
        f"single-quantity bits/s.\n\n"
        f"## Sources\n\n"
        f"* Paper: `10.1103_PhysRevLett.80.197` (Strong et al. 1998, "
        f'"Entropy and information in neural spike trains")\n'
        f"* External: Niven et al. 2007, "
        f'"Energy limitation as a selective pressure on the evolution of '
        f'sensory systems" (https://doi.org/10.1242/jeb.005249); not in '
        f"local paper corpus, referenced as external URL.\n"
        f"* Task: `t0124_bedb_dsi_atp_per_spike_nsga2`\n"
        f"* Task: `t0097_multi_obj_optim` (Strong-Bialek + Sengupta "
        f"recipes catalogued)\n"
        f"* Task: `t0122_dsi_cytoplasm_volume_nsga2` (fork point)\n"
        f"* Predictions asset: "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/assets/predictions/"
        f"nsga2-mi-atp-per-spike-bedb-morph`\n"
        f"* Chart: "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/"
        f"niven_2007_comparison.png`\n"
        f"* Chart: "
        f"`tasks/t0124_bedb_dsi_atp_per_spike_nsga2/results/images/"
        f"carter_bean_atp_per_ap_check.png`\n"
    )


def _build_details(
    *,
    seed: int,
    summary: dict[str, Any],
    date_created: str,
) -> dict[str, Any]:
    verdict_word, _ = _verdict_text(summary=summary)
    return {
        "spec_version": "2",
        "answer_id": ANSWER_ID,
        "question": QUESTION,
        "short_title": SHORT_TITLE,
        "short_answer_path": "short_answer.md",
        "full_answer_path": "full_answer.md",
        "categories": [
            "compartmental-modeling",
            "dendritic-computation",
            "retinal-ganglion-cell",
        ],
        "answer_methods": [
            "code-experiment",
            "papers",
            "internet",
        ],
        "source_paper_ids": [
            "10.1103_PhysRevLett.80.197",
        ],
        "source_urls": [
            "https://doi.org/10.1242/jeb.005249",
            "https://doi.org/10.1103/PhysRevLett.80.197",
        ],
        "source_task_ids": [
            "t0097_multi_obj_optim",
            "t0122_dsi_cytoplasm_volume_nsga2",
            "t0124_bedb_dsi_atp_per_spike_nsga2",
        ],
        "confidence": "medium",
        "created_by_task": "t0124_bedb_dsi_atp_per_spike_nsga2",
        "date_created": date_created,
        "metrics_at_creation": {
            "task_seed": int(seed),
            "n_top_cells": int(summary["n_cells"]),
            "log_log_p_exponent": summary.get("p_exponent"),
            "log_log_fit_r_squared": summary.get("fit_r_squared"),
            "mean_per_cell_r_squared": summary.get("mean_r_squared_per_cell"),
            "niven_2007_verdict": verdict_word,
        },
    }


def build_answer_asset(*, seed: int) -> Path:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    sb_data = _load_strong_bialek_top10()
    summary = _summarise_strong_bialek(sb_data=sb_data)
    date_answered = datetime.now(UTC).date().isoformat()

    short = _build_short_answer(seed=seed, summary=summary, date_answered=date_answered)
    SHORT_ANSWER_PATH.write_text(short, encoding="utf-8")
    print(f"[answer] wrote {SHORT_ANSWER_PATH}")

    details = _build_details(seed=seed, summary=summary, date_created=date_answered)
    full = _build_full_answer(
        seed=seed,
        summary=summary,
        sb_data=sb_data,
        date_answered=date_answered,
        confidence=str(details["confidence"]),
    )
    FULL_ANSWER_PATH.write_text(full, encoding="utf-8")
    print(f"[answer] wrote {FULL_ANSWER_PATH}")
    DETAILS_PATH.write_text(json.dumps(details, indent=2), encoding="utf-8")
    print(f"[answer] wrote {DETAILS_PATH}")

    return ASSET_DIR


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=int(T0124_SEEDS[0]))
    parser.add_argument(
        "--answer",
        type=str,
        default=ANSWER_ID,
        help="Currently only one answer supported.",
    )
    args = parser.parse_args()
    if args.answer != ANSWER_ID:
        raise ValueError(f"unknown answer id: {args.answer}; only {ANSWER_ID} is supported")
    build_answer_asset(seed=int(args.seed))


if __name__ == "__main__":
    main()
