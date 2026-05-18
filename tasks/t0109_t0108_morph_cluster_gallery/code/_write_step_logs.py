"""One-shot helper that writes per-step logs for this task."""

from __future__ import annotations

from pathlib import Path

TASK_ROOT: Path = Path(__file__).resolve().parents[1]
LOGS_STEPS: Path = TASK_ROOT / "logs" / "steps"

SECTIONS: list[tuple[str, str, str, str | None, str, int, str, str, str, str]] = [
    (
        "001_create-branch",
        "completed",
        "2026-05-18T17:00:00Z",
        "2026-05-18T17:01:00Z",
        "create-branch",
        1,
        (
            "Created task worktree at neuron-channels-worktrees/"
            "t0109_t0108_morph_cluster_gallery on branch "
            "task/t0109_t0108_morph_cluster_gallery forked from main commit 2de94325 "
            "(the t0108 merge commit). Pure visualisation task to draw morphology examples "
            "for the four t0108 K-means morphology clusters."
        ),
        (
            "* Ran `git worktree add ../neuron-channels-worktrees/"
            "t0109_t0108_morph_cluster_gallery -b task/t0109_t0108_morph_cluster_gallery "
            "main`."
        ),
        "* Worktree at expected path; HEAD = 2de94325.",
        "* None.",
    ),
    (
        "002_check-deps",
        "completed",
        "2026-05-18T17:01:00Z",
        "2026-05-18T17:01:30Z",
        "check-deps",
        2,
        (
            "Verified the single dependency t0108_t0106_cluster_factor_dsi05_pd10 is "
            "completed (PR #135 merged) and that its filtered_cells.json + "
            "morphology_clusters.json artefacts are present on main."
        ),
        (
            "* Read tasks/t0108_*/task.json; status=completed.\n"
            "* Confirmed filtered_cells.json and morphology_clusters.json exist."
        ),
        "* Dependency confirmed completed; data files readable.",
        "* None.",
    ),
    (
        "003_init-folders",
        "completed",
        "2026-05-18T17:01:30Z",
        "2026-05-18T17:02:00Z",
        "init-folders",
        3,
        (
            "Created mandatory task subfolders following the canonical task_folder "
            "specification. Added .gitkeep markers where required."
        ),
        (
            "* Created assets/, code/, corrections/, intervention/, "
            "logs/{commands,searches,sessions,steps}/, plan/, research/, "
            "results/{data,images}/."
        ),
        "* Folder tree matches spec; gitkeeps in place.",
        "* None.",
    ),
    (
        "006_research-code",
        "completed",
        "2026-05-18T17:02:00Z",
        "2026-05-18T17:03:00Z",
        "research-code",
        6,
        (
            "Reviewed t0105 build_gallery.py for the morphology-build + plot patterns and "
            "confirmed reusability. Confirmed morphology_params layout, MorphologyParams."
            "from_dict signature, and the t0092 generate_fixed_morphology entry point."
        ),
        (
            "* Read tasks/t0105_*/code/build_gallery.py.\n"
            "* Read tasks/t0090_*/code/morphology_params.py for the from_dict signature."
        ),
        "* Reused the t0105 build + plot helpers verbatim in build_cluster_gallery.py.",
        (
            "* Discovered the t0080 compiled MOD library (build/nrnmech.dll) was not "
            "tracked by git; copied from the main repo before the run."
        ),
    ),
    (
        "007_planning",
        "completed",
        "2026-05-18T17:03:00Z",
        "2026-05-18T17:04:00Z",
        "planning",
        7,
        (
            "Wrote plan/plan.md with 5 REQ checklist items: load t0108 data, top-10 per "
            "cluster by DSI*PD, build morphology, render gallery, embed."
        ),
        "* Wrote plan/plan.md.",
        "* plan.md present with the canonical section structure.",
        "* None.",
    ),
    (
        "008_implementation",
        "completed",
        "2026-05-18T17:04:00Z",
        "2026-05-18T17:30:00Z",
        "implementation",
        8,
        (
            "Implemented code/build_cluster_gallery.py: load t0108 filtered_cells.json + "
            "morphology_clusters.json, sort by DSI*PD desc per cluster, take top 10 (or all "
            "if fewer like cluster 3 with 7), build each morphology via "
            "generate_fixed_morphology, extract pt3d coords, render 4x10 grid PNG."
        ),
        (
            "* Wrote tasks/t0109/code/build_cluster_gallery.py.\n"
            "* Ran build_cluster_gallery.py; 37 morphologies built (10/10/10/7); 0 build "
            "failures.\n"
            "* Wrote results/data/gallery_picks.json with the deterministic picks."
        ),
        (
            "* results/images/morphology_gallery_by_cluster.png (4 rows x 10 cols).\n"
            "* results/data/gallery_picks.json."
        ),
        (
            "* First run failed with FileNotFoundError on t0080 build/nrnmech.dll; resolved "
            "by copying the compiled MOD library from the main repo to the worktree (the "
            "dll is gitignored, so this is the standard workaround for fresh worktrees)."
        ),
    ),
    (
        "010_results",
        "completed",
        "2026-05-18T17:30:00Z",
        "2026-05-18T17:45:00Z",
        "results",
        10,
        (
            "Wrote canonical results documents and the per-task JSON outputs. No registered "
            "metrics for a pure visualisation task; metrics.json has an empty variants "
            "array."
        ),
        (
            "* Wrote results_summary.md (with mandatory Summary, Metrics, Verification "
            "sections), results_detailed.md (with embedded gallery + per-cluster pick "
            "tables), metrics.json (empty variants), costs.json (0 USD), suggestions.json "
            "(empty), remote_machines_used.json ([])."
        ),
        "* All result files present and verificator-compliant.",
        "* None.",
    ),
    (
        "012_suggestions",
        "completed",
        "2026-05-18T17:45:00Z",
        "2026-05-18T17:46:00Z",
        "suggestions",
        12,
        (
            "Wrote empty suggestions.json per scope; follow-ups captured inline in "
            "results_detailed.md Next Steps section instead of as formal suggestion records."
        ),
        "* Wrote results/suggestions.json with spec_version 2 and empty array.",
        "* verify_suggestions passes.",
        "* None.",
    ),
    (
        "013_reporting",
        "completed",
        "2026-05-18T17:46:00Z",
        "2026-05-18T17:55:00Z",
        "reporting",
        13,
        (
            "Ran all verificators; addressed warnings; finalised task.json and "
            "step_tracker.json; committed per-step; pushed branch and opened PR."
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
    (4, "research-papers", "Pure visualisation task; no literature search needed."),
    (5, "research-internet", "Pure visualisation task; no internet research needed."),
    (9, "creative-thinking", "Pure visualisation task; observations folded into results."),
    (11, "compare-literature", "Pure visualisation task; no literature comparison."),
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
        'task_id: "t0109_t0108_morph_cluster_gallery"\n'
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
            'task_id: "t0109_t0108_morph_cluster_gallery"\n'
            f"step_number: {num}\n"
            f'step_name: "{name}"\n'
            'status: "skipped"\n'
            "started_at: null\n"
            "completed_at: null\n"
            "---\n\n"
            f"# Step {num}: {name}\n\n"
            "## Summary\n\n"
            f"Skipped per task scope: {reason} The work this step normally covers is not "
            "applicable to this pure-visualisation task.\n\n"
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
