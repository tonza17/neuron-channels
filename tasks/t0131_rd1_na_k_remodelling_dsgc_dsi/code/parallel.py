"""Resumable parallel job runner: results are appended to a JSONL file as jobs complete."""

import json
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import numpy as np
from tqdm import tqdm

from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.cell_factory import get_h
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.constants import MAX_WORKERS
from tasks.t0131_rd1_na_k_remodelling_dsgc_dsi.code.paths import DATA_DIR

TRACES_DIR: Path = DATA_DIR / "traces"
TRACE_KEY: str = "_trace"


def load_done_rows(*, path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    if not path.exists():
        return rows
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if len(line) == 0:
                continue
            try:
                row: dict[str, Any] = json.loads(line)
            except json.JSONDecodeError:
                continue
            rows[str(row["job_key"])] = row
    return rows


def safe_name(*, key: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in key)


def save_trace(*, key: str, trace: dict[str, Any]) -> Path:
    TRACES_DIR.mkdir(parents=True, exist_ok=True)
    path = TRACES_DIR / f"{safe_name(key=key)}.npz"
    arrays: dict[str, Any] = {k: np.asarray(v) for k, v in trace.items()}
    np.savez_compressed(path, **arrays)
    return path


def _init_worker() -> None:
    get_h()


def run_jobs(
    *,
    jobs: list[Any],
    worker_fn: Callable[[Any], dict[str, Any]],
    out_path: Path,
    key_of: Callable[[Any], str],
    max_workers: int = MAX_WORKERS,
    desc: str = "jobs",
) -> dict[str, dict[str, Any]]:
    """Run ``jobs`` skipping keys already in ``out_path``; returns all rows (old + new)."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    done = load_done_rows(path=out_path)
    todo: list[Any] = [j for j in jobs if key_of(j) not in done]
    print(f"[{desc}] {len(jobs)} jobs, {len(done)} already done, {len(todo)} to run", flush=True)
    if len(todo) == 0:
        return done

    def _store(row: dict[str, Any], f: Any) -> None:
        trace = row.pop(TRACE_KEY, None)
        if trace is not None:
            save_trace(key=str(row["job_key"]), trace=trace)
        f.write(json.dumps(row) + "\n")
        f.flush()
        done[str(row["job_key"])] = row

    with out_path.open("a", encoding="utf-8") as f:
        if max_workers <= 1:
            for job in tqdm(todo, desc=desc):
                _store(worker_fn(job), f)
        else:
            with ProcessPoolExecutor(max_workers=max_workers, initializer=_init_worker) as ex:
                futures = [ex.submit(worker_fn, job) for job in todo]
                for fut in tqdm(as_completed(futures), total=len(futures), desc=desc):
                    _store(fut.result(), f)
    return done
