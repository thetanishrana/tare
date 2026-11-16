"""Run model-written code in the Docker sandbox (never on the host).

Workdir layout (built by the caller, validated by the isolation guard):
    <workdir>/inputs/*.parquet   mounted read-only
    <workdir>/code.R | code.py   mounted read-only
    <workdir>/out/               the only writable mount; the program writes out/result.parquet
"""

from __future__ import annotations

import subprocess
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

from tare.isolation import check_workdir, validate_mount

IMAGE = "tare-sandbox:dev"
MAX_LOG_CHARS = 4000
COMMANDS = {
    "r": ("code.R", ["Rscript", "/work/code.R"]),
    "python": ("code.py", ["python", "/work/code.py"]),
}


@dataclass
class SandboxResult:
    exit_code: int | None
    stdout: str
    stderr: str
    timed_out: bool
    seconds: float

    @property
    def ok(self) -> bool:
        return self.exit_code == 0 and not self.timed_out


def _tail(text: str) -> str:
    return text if len(text) <= MAX_LOG_CHARS else "...[truncated]...\n" + text[-MAX_LOG_CHARS:]


def run_in_sandbox(
    workdir: Path,
    language: str,
    timeout: int = 120,
    memory: str = "2g",
    cpus: str = "2",
    pids: int = 256,
    image: str = IMAGE,
) -> SandboxResult:
    code_file, cmd = COMMANDS[language]
    workdir = Path(workdir).resolve()
    check_workdir(workdir, code_file)
    inputs = validate_mount(workdir / "inputs", workdir)
    out = validate_mount(workdir / "out", workdir)
    code = validate_mount(workdir / code_file, workdir)
    out.chmod(0o777)  # the sandbox user (uid 10001) must be able to write here

    name = f"tare-{uuid.uuid4().hex[:12]}"
    docker = [
        "docker",
        "run",
        "--rm",
        "--name",
        name,
        "--network",
        "none",
        "--read-only",
        "--tmpfs",
        "/tmp",
        "--memory",
        memory,
        "--cpus",
        cpus,
        "--pids-limit",
        str(pids),
        "-v",
        f"{inputs}:/work/inputs:ro",
        "-v",
        f"{out}:/work/out",
        "-v",
        f"{code}:/work/{code_file}:ro",
        image,
        *cmd,
    ]
    start = time.monotonic()
    try:
        p = subprocess.run(docker, capture_output=True, text=True, timeout=timeout, check=False)
        return SandboxResult(
            p.returncode, _tail(p.stdout), _tail(p.stderr), False, time.monotonic() - start
        )
    except subprocess.TimeoutExpired as e:
        subprocess.run(["docker", "kill", name], capture_output=True, check=False)
        so = (e.stdout or b"").decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
        se = (e.stderr or b"").decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
        return SandboxResult(None, _tail(so), _tail(se), True, time.monotonic() - start)
