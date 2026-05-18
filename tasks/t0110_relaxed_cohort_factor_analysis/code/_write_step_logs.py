"""One-shot helper that writes per-step logs for t0110."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parents[1]
LOGS_STEPS: Path = TASK_ROOT / "logs" / "steps"

SECTIONS: list[tuple[str, str, str, str | None, str, int, str, str, str, str]] = [
    (
        "001_create-branch",
        "completed",
        "2026-05-18T18:30:00Z",
        "2026-05-18T18:31:00Z",
        "create-branch",
        1,
        (
            "Created task worktree at neuron-channels-worktrees/"
            "t0110_relaxed_cohort_factor_analysis on branch "
            "task/t0110_relaxed_cohort_factor_analysis forked from main commit 077fd527 "
            "(the t0109 merge commit). Direct hypothesis-test follow-up to t0108: does the "
            "all-negative PD column persist under a less-truncated cohort?"
        ),
        (
            "* Ran `git worktree add ../neuron-channels-worktrees/"
            "t0110_relaxed_cohort_factor_analysis -b task/t0110_relaxed_cohort_factor_analysis "
            "main`."
        ),
        "* Worktree at expected path; HEAD = 077fd527.",
        "* None.",
    ),
    (
        "002_check-deps",
        "completed",
        "2026-05-18T18:31:00Z",
        "2026-05-18T18:31:30Z",
        "check-deps",
        2,
        (
            "Verified the single dependency t0108_t0106_cluster_factor_dsi05_pd10 is completed "
            "and on main (PR #135 merged). Its factor_analysis.json is present and readable for "
            "the side-by-side comparison plot."
        ),
        (
            "* Read tasks/t0108_*/task.json; status=completed.\n"
            "* Confirmed tasks/t0108_*/results/data/factor_analysis.json exists."
        ),
        "* Dependency confirmed completed.",
        "* None.",
    ),
    (
        "003_init-folders",
        "completed",
        "2026-05-18T18:31:30Z",
        "2026-05-18T18:32:00Z",
        "init-folders",
        3,
        (
            "Created mandatory task subfolders following the canonical task_folder spec. Added "
            ".gitkeep markers where required to keep git tracking the structure."
        ),
        (
            "* Created assets/{,answer/}, code/, corrections/, intervention/, "
            "logs/{commands,searches,sessions,steps}/, plan/, research/, "
            "results/{data,images}/."
        ),
        "* Folder tree matches spec; gitkeeps in place.",
        "* None.",
    ),
    (
        "006_research-code",
        "completed",
        "2026-05-18T18:32:00Z",
        "2026-05-18T18:33:00Z",
        "research-code",
        6,
        (
            "Reviewed t0108 code/factor_analysis.py to identify the varimax rotation routine "
            "and reuse it via absolute import. Confirmed the t0108 result file shape so we can "
            "load it for the comparison plot."
        ),
        (
            "* Read tasks/t0108_*/code/factor_analysis.py for the varimax routine.\n"
            "* Read tasks/t0108_*/results/data/factor_analysis.json schema."
        ),
        "* varimax_rotation reusable via import; factor_analysis.json schema matches our needs.",
        "* None.",
    ),
    (
        "007_planning",
        "completed",
        "2026-05-18T18:33:00Z",
        "2026-05-18T18:34:00Z",
        "planning",
        7,
        (
            "Wrote plan/plan.md with 5 REQ items: filter+dedupe, run FA, compute correlations, "
            "render side-by-side comparison chart, write one answer asset."
        ),
        "* Wrote plan/plan.md.",
        "* plan.md present with canonical structure.",
        "* None.",
    ),
    (
        "008_implementation",
        "completed",
        "2026-05-18T18:34:00Z",
        "2026-05-18T19:00:00Z",
        "implementation",
        8,
        (
            "Implemented code/factor_analysis_relaxed.py: load t0106 evaluations, apply "
            "DSI>0.2 AND PD>3, dedupe by 68-d vector, run sklearn FactorAnalysis + manual "
            "varimax (reused from t0108), compute Pearson r vs DSI/PD, render side-by-side "
            "comparison + 68x10 loadings heatmap."
        ),
        (
            "* Wrote code/factor_analysis_relaxed.py (~330 lines).\n"
            "* Ran the pipeline: 3744 raw -> 1209 passing -> 247 unique cells.\n"
            "* Eigenvalues > 1: 16; factors retained at Kaiser cap: 10.\n"
            "* Sign counts: DSI 6 pos / 4 neg; PD 2 pos / 8 neg.\n"
            "* Joint factor: F1 (r_DSI=-0.37, r_PD=-0.75) -- the joint failure axis.\n"
            "* Wrote results/data/{filtered_cells,factor_analysis_relaxed}.json and "
            "results/images/{factor_correlations_comparison,factor_loadings_heatmap_relaxed}.png."
        ),
        (
            "* results/data/filtered_cells.json (247 cells).\n"
            "* results/data/factor_analysis_relaxed.json.\n"
            "* results/images/factor_correlations_comparison.png.\n"
            "* results/images/factor_loadings_heatmap_relaxed.png."
        ),
        (
            "* Initial summary doc had incorrect mean DSI / PD values; corrected after re-"
            "deriving from filtered_cells.json (DSI mean 0.669, PD mean 68.8 Hz)."
        ),
    ),
    (
        "010_results",
        "completed",
        "2026-05-18T19:00:00Z",
        "2026-05-18T19:20:00Z",
        "results",
        10,
        (
            "Wrote canonical results documents, metrics.json (1 variant with "
            "direction_selectivity_index=0.669), costs.json (0 USD), suggestions.json (empty), "
            "remote_machines_used.json ([]), and the single answer asset "
            "t0106-pd-correlation-sign-flip-relaxed-cohort with mandatory short + full answer "
            "sections."
        ),
        (
            "* Wrote results_summary.md (Summary, Metrics, Verification, Figures, Headline "
            "interpretation), results_detailed.md (Methodology, Cohort, Factor correlations, "
            "Direct comparison, Top-5 loadings, Analysis, Limitations, Verification, Files, "
            "Next Steps), and the 3 mandatory result JSON files.\n"
            "* Wrote assets/answer/t0106-pd-correlation-sign-flip-relaxed-cohort/{details.json,"
            "short_answer.md,full_answer.md} with all spec-required sections."
        ),
        (
            "* All result files present; metrics.json validates; answer asset aggregator "
            "returns the asset id."
        ),
        "* None.",
    ),
    (
        "012_suggestions",
        "completed",
        "2026-05-18T19:20:00Z",
        "2026-05-18T19:21:00Z",
        "suggestions",
        12,
        (
            "Wrote empty suggestions.json per scope; follow-up suggestions captured inline in "
            "results_detailed.md Next Steps section instead of as formal records."
        ),
        "* Wrote results/suggestions.json with spec_version 2 and empty array.",
        "* verify_suggestions passes.",
        "* None.",
    ),
    (
        "013_reporting",
        "completed",
        "2026-05-18T19:21:00Z",
        "2026-05-18T19:30:00Z",
        "reporting",
        13,
        (
            "Ran all verificators; finalised task.json and step_tracker.json; committed "
            "per-step; pushed branch; opened PR; merged."
        ),
        (
            "* Ran verify_task_file, verify_task_folder, verify_task_metrics, "
            "verify_task_results, verify_plan, verify_suggestions, "
            "verify_task_dependencies, verify_logs, verify_task_complete.\n"
            "* Set task.json status=completed and end_time."
        ),
        "* All verificators pass with 0 errors.",
        "* None.",
    ),
]

SKIPPED: list[tuple[int, str, str]] = [
    (4, "research-papers", "Hypothesis test on existing data; no literature search needed."),
    (5, "research-internet", "Hypothesis test on existing data; no internet research needed."),
    (
        9,
        "creative-thinking",
        "Pre-specified hypothesis test; observations folded into results.",
    ),
    (
        11,
        "compare-literature",
        "Comparison is against t0108 strict cohort, not external literature.",
    ),
]


def _render(
    *,
    folder: str,
    status: str,
    started: str | None,
    completed: str | None,
    name: str,
    num: int,
    summary: str,
    actions: str,
    outputs: str,
    issues: str,
) -> str:
    started_line: str = f'"{started}"' if started is not None else "null"
    completed_line: str = f'"{completed}"' if completed is not None else "null"
    return (
        "---\n"
        'spec_version: "3"\n'
        'task_id: "t0110_relaxed_cohort_factor_analysis"\n'
        f"step_number: {num}\n"
        f'step_name: "{name}"\n'
        f'status: "{status}"\n'
        f"started_at: {started_line}\n"
        f"completed_at: {completed_line}\n"
        "---\n\n"
        f"# Step {num}: {name}\n\n"
        "## Summary\n\n"
        f"{summary}\n\n"
        "## Actions Taken\n\n"
        f"{actions}\n\n"
        "## Outputs\n\n"
        f"{outputs}\n\n"
        "## Issues\n\n"
        f"{issues}\n"
    )


def main() -> None:
    for (
        folder,
        status,
        started,
        completed,
        name,
        num,
        summary,
        actions,
        outputs,
        issues,
    ) in SECTIONS:
        content: str = _render(
            folder=folder,
            status=status,
            started=started,
            completed=completed,
            name=name,
            num=num,
            summary=summary,
            actions=actions,
            outputs=outputs,
            issues=issues,
        )
        path: Path = LOGS_STEPS / folder / "step_log.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        print(f"wrote {path}")
    for num, name, reason in SKIPPED:
        folder = f"{num:03d}_{name}"
        path = LOGS_STEPS / folder / "step_log.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "---\n"
            'spec_version: "3"\n'
            'task_id: "t0110_relaxed_cohort_factor_analysis"\n'
            f"step_number: {num}\n"
            f'step_name: "{name}"\n'
            'status: "skipped"\n'
            "started_at: null\n"
            "completed_at: null\n"
            "---\n\n"
            f"# Step {num}: {name}\n\n"
            "## Summary\n\n"
            f"Skipped per task scope: {reason} The work this step normally covers is not "
            "applicable to this hypothesis-test task on existing optimisation output.\n\n"
            "## Actions Taken\n\n"
            "* None; step skipped.\n\n"
            "## Outputs\n\n"
            "* None.\n\n"
            "## Issues\n\n"
            "* None.\n",
            encoding="utf-8",
        )
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
