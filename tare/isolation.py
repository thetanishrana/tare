"""Isolation guard: a programmer's sandbox must never see oracle outputs, answer keys, reference
solutions, results, or another programmer's files.

Mounts are validated against an allowlist (everything must live inside the run's own workdir) and
against a forbidden list (nothing may be, contain, or sit above a forbidden path).
"""

from __future__ import annotations

from pathlib import Path

from tare.tasks import ANSWERS_DIR, BENCHMARK, ORACLE_DIR, ROOT

FORBIDDEN: list[Path] = [
    ORACLE_DIR,
    ANSWERS_DIR,
    ROOT / "results",
    BENCHMARK / "reference",
    BENCHMARK / "tasks",
]


class IsolationError(RuntimeError):
    pass


def _is_inside(path: Path, parent: Path) -> bool:
    return path == parent or parent in path.parents


def validate_mount(
    host_path: str | Path, allowed_root: str | Path, extra_forbidden: list[Path] | None = None
) -> Path:
    """Return the resolved path if it is safe to mount, else raise IsolationError."""
    p = Path(host_path).resolve()
    root = Path(allowed_root).resolve()
    if not _is_inside(p, root):
        raise IsolationError(f"mount {p} is outside the run workdir {root}")
    for f in [*FORBIDDEN, *(extra_forbidden or [])]:
        f = f.resolve()
        # inside a forbidden tree, or a parent that would expose one
        if _is_inside(p, f) or _is_inside(f, p):
            raise IsolationError(f"mount {p} overlaps forbidden path {f}")
    return p


def check_workdir(workdir: str | Path, expected_code_file: str) -> None:
    """The workdir may contain only inputs/, out/ and the code file."""
    wd = Path(workdir)
    allowed = {"inputs", "out", expected_code_file}
    found = {p.name for p in wd.iterdir()}
    extra = found - allowed
    if extra:
        raise IsolationError(f"unexpected files in sandbox workdir: {sorted(extra)}")
    if not (wd / "inputs").is_dir():
        raise IsolationError("workdir has no inputs/")
