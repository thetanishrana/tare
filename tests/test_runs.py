import shutil
import subprocess

import pytest

from tare import runs
from tare.prompts import build_messages, extract_code
from tare.providers import FakeClient
from tare.tasks import BENCHMARK, BUNDLES_DIR, load_all_tasks, load_task


def _docker_ready() -> bool:
    if not shutil.which("docker"):
        return False
    r = subprocess.run(
        ["docker", "image", "inspect", "tare-sandbox:dev"], capture_output=True, check=False
    )
    return r.returncode == 0


needs_sandbox = pytest.mark.skipif(
    not (_docker_ready() and (BUNDLES_DIR / "adsl-saffl-std").exists()),
    reason="needs the tare-sandbox:dev image and built task bundles (data/tasks)",
)


def fenced(code: str) -> str:
    return f"Here you go.\n```python\n{code}\n```\n"


def test_extract_code_variants():
    assert extract_code("x\n```python\nprint(1)\n```\n", "python") == "print(1)\n"
    assert extract_code("```\nprint(2)\n```", "python") == "print(2)\n"
    assert extract_code("```python\na\n```\ntext\n```python\nb\n```", "python") == "b\n"
    assert extract_code("```r\nx <- 1\n```", "python") is None
    assert extract_code("no code here", "python") is None
    assert extract_code("```R\nx <- 1\n```", "r") == "x <- 1\n"


@needs_sandbox
def test_prompt_contains_spec_and_no_answers():
    t = load_task("adsl-saffl-std")
    msgs = build_messages(t, "python")
    text = "\n".join(m["content"] for m in msgs)
    assert "SAFFL" in text and "/work/out/result.parquet" in text
    assert "data/answers" not in text and "oracle" not in text.lower()


@needs_sandbox
def test_golden_all_references_score_correct():
    """A fake model that returns each task's reference solution must score 'correct' on every task."""
    for t in load_all_tasks():
        code = (BENCHMARK / "reference" / f"{t.id}.py").read_text()
        client = FakeClient(lambda _m, c=code: fenced(c))
        rec = runs.run_sample(
            t, client, {"language": "python", "max_repairs": 0}, _tmp_log(t), _tmp_dir(t), 0
        )
        assert rec["class"] == "correct", (t.id, rec)


_TMP = {}


def _tmp_dir(t):
    import tempfile
    from pathlib import Path

    d = Path(_TMP.setdefault("d", tempfile.mkdtemp(prefix="tare-test-")))
    return d


def _tmp_log(t):
    return _tmp_dir(t) / "calls.jsonl"


@needs_sandbox
def test_wrong_code_is_silent_and_broken_code_is_loud_then_repaired():
    t = load_task("adsl-saffl-std")
    cfg = {"language": "python", "max_repairs": 2}
    wrong = "import pandas as pd\ndm = pd.read_parquet('/work/inputs/dm.parquet')\nout = dm[['USUBJID']].copy()\nout['SAFFL'] = 'Y'\nout.to_parquet('/work/out/result.parquet')\n"
    rec = runs.run_sample(t, FakeClient(lambda _m: fenced(wrong)), cfg, _tmp_log(t), _tmp_dir(t), 1)
    assert rec["class"] == "silent_error" and rec["attempts"] == 1 and rec["mismatched_records"] > 0

    good = (BENCHMARK / "reference" / "adsl-saffl-std.py").read_text()
    replies = iter([fenced("raise SystemExit(3)"), "no code at all", fenced(good)])
    client = FakeClient(lambda _m: next(replies))
    rec = runs.run_sample(t, client, cfg, _tmp_log(t), _tmp_dir(t), 2)
    assert rec["class"] == "correct" and rec["attempts"] == 3


def test_call_log_records_stop_reason_and_sent_params(tmp_path):
    import json

    from tare.providers.base import Completion, Usage

    class Stub:
        provider, model = "stub", "stub-1"

        def complete(self, messages, **params):
            return Completion(
                "no code", Usage(1, 1), 0.0, "stub-1", {"max_tokens": 5}, None, "end_turn"
            )

        def identity(self):
            return {"provider": "stub", "model": "stub-1"}

    t = load_task("adsl-saffl-std")
    log = tmp_path / "calls.jsonl"
    runs.run_sample(t, Stub(), {"language": "python", "max_repairs": 0}, log, tmp_path, 0)
    rec = json.loads(log.read_text().splitlines()[0])
    assert rec["stop_reason"] == "end_turn" and rec["params"] == {"max_tokens": 5}


def test_escalation_reply_is_recorded_not_run(tmp_path):

    from tare.prompts import extract_escalation

    assert (
        extract_escalation("ESCALATE: Does the first dose day count?")
        == "Does the first dose day count?"
    )
    assert extract_escalation("```python\nprint(1)\n```\nESCALATE: x") is None  # code present wins
    assert extract_escalation("just prose") is None

    t = load_task("adsl-trtdurd-amb")
    calls = FakeClient(lambda _m: "ESCALATE: Is the duration inclusive of both days?")
    log = tmp_path / "calls.jsonl"
    rec = runs.run_sample(
        t,
        calls,
        {"language": "python", "max_repairs": 2, "prompt_version": "k2-v2"},
        log,
        tmp_path,
        0,
    )
    assert rec["class"] == "escalated" and rec["attempts"] == 1 and rec["ambiguous"] is True
    assert "inclusive" in rec["question"]
    # v1 prompts have no escalation path: the same reply is just a missing code block
    rec1 = runs.run_sample(
        t,
        FakeClient(lambda _m: "ESCALATE: x"),
        {"language": "python", "max_repairs": 0},
        log,
        tmp_path,
        1,
    )
    assert rec1["class"] == "loud_error"


@needs_sandbox
def test_v2_prompt_offers_escalation_and_v1_does_not():
    t = load_task("adsl-trtdurd-amb")
    v1 = "\n".join(m["content"] for m in build_messages(t, "python", "k2-v1"))
    v2 = "\n".join(m["content"] for m in build_messages(t, "python", "k2-v2"))
    assert "ESCALATE" not in v1 and "ESCALATE:" in v2


@needs_sandbox
def test_sample_record_carries_output_digest():
    t = load_task("adsl-saffl-std")
    code = (BENCHMARK / "reference" / "adsl-saffl-std.py").read_text()
    rec = runs.run_sample(
        t,
        FakeClient(lambda _m: fenced(code)),
        {"language": "python", "max_repairs": 0},
        _tmp_log(t),
        _tmp_dir(t),
        3,
    )
    assert (
        rec["class"] == "correct"
        and isinstance(rec["output_digest"], str)
        and len(rec["output_digest"]) == 16
    )


def test_assumptions_extraction_and_v4_escalation():
    from tare.prompts import ESCALATION_VERSIONS, extract_assumptions, extract_escalation

    reply = "ASSUMPTIONS:\n- first dose day counts as after\n- placebo counts\nESCALATE: Does the first dose day count?"
    assert extract_assumptions(reply).startswith("- first dose day counts as after")
    assert "ESCALATE" not in extract_assumptions(reply)
    assert extract_escalation(reply) == "Does the first dose day count?"
    code_reply = "ASSUMPTIONS:\n- none\n```python\nprint(1)\n```"
    assert extract_assumptions(code_reply) == "- none" and extract_escalation(code_reply) is None
    assert extract_assumptions("no section here") is None
    assert {"k2-v2", "k2-v3", "k2-v4"} == set(ESCALATION_VERSIONS)


@needs_sandbox
def test_v3_v4_prompts_differ_and_v4_has_checklist(tmp_path):
    t = load_task("adsl-trtdurd-amb")
    text = {
        v: "\n".join(m["content"] for m in build_messages(t, "python", v))
        for v in ("k2-v1", "k2-v2", "k2-v3", "k2-v4")
    }
    assert "ESCALATE" not in text["k2-v1"]
    assert "silently guessing" in text["k2-v3"] and "checklist" not in text["k2-v3"]
    assert "checklist" in text["k2-v4"] and "ASSUMPTIONS:" in text["k2-v4"]
    assert len(set(text.values())) == 4


def test_v4_escalation_with_assumptions_is_recorded(tmp_path):
    t = load_task("adsl-trtdurd-amb")
    client = FakeClient(
        lambda _m: (
            "ASSUMPTIONS:\n- inclusive counting is unclear\nESCALATE: Is the duration inclusive of both days?"
        )
    )
    rec = runs.run_sample(
        t,
        client,
        {"language": "python", "max_repairs": 2, "prompt_version": "k2-v4"},
        tmp_path / "c.jsonl",
        tmp_path,
        0,
    )
    assert rec["class"] == "escalated" and "inclusive counting" in rec["assumptions"]
