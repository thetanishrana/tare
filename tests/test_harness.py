import json
import re
from pathlib import Path

from tare import adjudicate, harness
from tare.adjudicate import parse_verdict
from tare.providers import FakeClient
from tare.tasks import BENCHMARK, load_task
from tests.test_runs import fenced, needs_sandbox

REPO = Path(__file__).resolve().parent.parent
TASK = "adsl-saffl-std"


def _code(name: str) -> str:
    return (BENCHMARK / "reference" / f"{name}.py").read_text()


def _programmer(code: str, assumptions: str = "- none") -> FakeClient:
    return FakeClient(lambda _m: f"ASSUMPTIONS:\n{assumptions}\n" + fenced(code))


def _json(**kw) -> FakeClient:
    return FakeClient(lambda _m: json.dumps(kw))


WRONG = _code("alt/adsl-saffl-amb__placebo-excluded")


def test_parse_verdict_variants():
    assert parse_verdict('{"verdict": "A", "reason": "r", "question": null}').verdict == "A"
    v = parse_verdict('Sure:\n{"verdict": "escalate", "reason": "r", "question": "Q?"}')
    assert (v.verdict, v.question) == ("escalate", "Q?")


def test_malformed_or_questionless_verdicts_fail_safe_to_escalation():
    assert parse_verdict("I think A is right.").verdict == "escalate"
    assert parse_verdict('{"verdict": "C"}').verdict == "escalate"
    v = parse_verdict('{"verdict": "escalate", "reason": "x", "question": ""}')
    assert v.verdict == "escalate" and v.question is None


def test_programmer_and_adjudicator_never_touch_answers():
    """Isolation by construction: no import of the scorer, answer keys or oracle."""
    for rel in ("tare/programmer/agent.py", "tare/adjudicate.py"):
        src = (REPO / rel).read_text()
        imports = "\n".join(re.findall(r"^(?:from|import) .*$", src, re.MULTILINE))
        for banned in ("tare.score", "ANSWERS_DIR", "ORACLE_DIR", "answers"):
            assert banned not in imports, (rel, banned)


@needs_sandbox
def test_agreeing_programmers_are_accepted_and_correct():
    t = load_task(TASK)
    r = harness.run_pair(t, _programmer(_code(TASK)), _programmer(_code(TASK)), max_repairs=0)
    assert (r.decision, r.source) == ("accepted", "agree")
    assert harness.score_harness(t, r).klass == "correct"


@needs_sandbox
def test_disagreement_goes_to_the_adjudicator_verdict():
    t = load_task(TASK)
    a, b = _programmer(_code(TASK)), _programmer(WRONG)
    good = harness.run_pair(t, a, b, _json(verdict="A", reason="r", question=None), max_repairs=0)
    assert (good.decision, good.source) == ("accepted", "A")
    assert harness.score_harness(t, good).klass == "correct"
    bad = harness.run_pair(t, a, b, _json(verdict="B", reason="r", question=None), max_repairs=0)
    assert harness.score_harness(t, bad).klass == "silent_error"
    esc = harness.run_pair(
        t,
        a,
        b,
        _json(verdict="escalate", reason="r", question="Do placebo rows count?"),
        max_repairs=0,
    )
    assert esc.decision == "escalated" and esc.question == "Do placebo rows count?"
    assert harness.score_harness(t, esc).klass == "escalated"
    rule = harness.run_pair(t, a, b, adjudicator=None, max_repairs=0)
    assert rule.decision == "escalated" and rule.question is None


@needs_sandbox
def test_programmer_escalation_and_assumption_check():
    t = load_task(TASK)
    asks = FakeClient(lambda _m: "ESCALATE: Does dose 0 count?")
    assert (
        harness.run_pair(t, asks, _programmer(_code(TASK)), max_repairs=0).decision == "escalated"
    )
    agree = (_programmer(_code(TASK)), _programmer(_code(TASK)))
    flagged = FakeClient(lambda _m: "ESCALATE: Both assumed placebo counts; is that right?")
    r = harness.run_pair(t, *agree, reviewer=flagged, max_repairs=0)
    assert (r.decision, r.reason) == ("escalated", "assumption check")
    clear = FakeClient(lambda _m: "PROCEED")
    assert harness.run_pair(t, *agree, reviewer=clear, max_repairs=0).decision == "accepted"


def test_describe_diff_lists_counts_and_sample():
    from tare.compare import CompareResult

    c = CompareResult(False, 10, 9, 1, 0, {"V": 2}, 2, [{"K": "a", "V__a": "Y", "V__b": None}])
    text = adjudicate.describe_diff(c)
    assert "keys only in A: 1" in text and '"V__a": "Y"' in text


@needs_sandbox
def test_pair_experiment_writes_logs_and_scores(tmp_path, monkeypatch):
    import yaml

    from tare import pair_runs

    monkeypatch.setattr(pair_runs, "RESULTS", tmp_path)
    t = load_task(TASK)
    ref = fenced(_code(TASK))
    monkeypatch.setattr(
        pair_runs, "make_client", lambda spec: FakeClient(lambda _m: ref, spec["model"])
    )
    cfg = {
        "name": "pair_test",
        "programmer_a": {"provider": "fake", "model": "fa"},
        "programmer_b": {"provider": "fake", "model": "fb"},
        "adjudicator": "rule",
        "prompt_version": "k2-v2",
        "max_repairs": 0,
        "tasks": [TASK],
    }
    run_dir = pair_runs.run_pair_experiment(cfg, tasks=[t])
    rec = json.loads((run_dir / "scores.jsonl").read_text().splitlines()[0])
    assert (rec["class"], rec["decision"], rec["source"]) == ("correct", "accepted", "agree")
    calls = [json.loads(x) for x in (run_dir / "calls.jsonl").read_text().splitlines()]
    assert {c["role"] for c in calls} == {"programmer_a", "programmer_b"}
    assert all(c["task_id"] == TASK for c in calls)
    assert yaml.safe_load((run_dir / "config.yaml").read_text())["name"] == "pair_test"


@needs_sandbox
def test_replay_reuses_logged_programmers_with_a_new_reviewer(tmp_path, monkeypatch):
    from tare import pair_runs

    monkeypatch.setattr(pair_runs, "RESULTS", tmp_path)
    t = load_task(TASK)
    ref = f"ASSUMPTIONS:\n- none\n{fenced(_code(TASK))}"

    def entry(role):
        return {
            "task_id": TASK,
            "sample": 0,
            "role": role,
            "model": "m",
            "response": ref,
            "usage": {"input_tokens": 1, "output_tokens": 1},
        }

    src = tmp_path / "orig"
    src.mkdir()
    (src / "calls.jsonl").write_text(
        "\n".join(json.dumps(entry(r)) for r in ("programmer_a", "programmer_b")) + "\n"
    )
    answers = {"q": "ESCALATE: Is placebo included?"}
    monkeypatch.setattr(
        pair_runs, "make_client", lambda spec: FakeClient(lambda _m: answers["q"], "rev")
    )
    base = {
        "name": "replay_test",
        "programmer_a": {"provider": "fake", "model": "a"},
        "programmer_b": {"provider": "fake", "model": "b"},
        "replay_from": str(src),
        "tasks": [TASK],
    }
    off = pair_runs.run_pair_experiment({**base, "reviewer": None}, tasks=[t])
    on = pair_runs.run_pair_experiment(
        {**base, "reviewer": {"provider": "fake", "model": "rev"}}, tasks=[t]
    )
    rec_off = json.loads((off / "scores.jsonl").read_text().splitlines()[0])
    rec_on = json.loads((on / "scores.jsonl").read_text().splitlines()[0])
    assert (rec_off["class"], rec_off["decision"]) == ("correct", "accepted")
    assert (rec_on["class"], rec_on["reason"]) == ("escalated", "assumption check")
    calls = [json.loads(x) for x in (on / "calls.jsonl").read_text().splitlines()]
    assert [c["role"] for c in calls] == ["reviewer"]  # the programmers were not called again


def test_review_v2_rule_escalates_on_unsettled_choice_that_changes_output():
    from tare.review import parse_review_v2

    def reply(settles, changes):
        return json.dumps(
            {
                "choices": [
                    {
                        "choice": "c",
                        "readings": ["a", "b"],
                        "spec_settles": settles,
                        "quote": "",
                        "changes_output": changes,
                        "question": "Which one?",
                    }
                ]
            }
        )

    assert parse_review_v2(reply(False, "yes")).question == "Which one?"
    assert parse_review_v2(reply(False, "unknown")).escalate
    assert not parse_review_v2(reply(True, "yes")).escalate  # settled by the spec
    assert not parse_review_v2(reply(False, "no")).escalate  # does not change the output
    assert parse_review_v2("not json").escalate  # fail safe
    assert not parse_review_v2('{"choices": []}').escalate


@needs_sandbox
def test_reviewer_v2_is_used_when_selected():
    t = load_task(TASK)
    agree = (_programmer(_code(TASK)), _programmer(_code(TASK)))
    unsettled = json.dumps(
        {
            "choices": [
                {
                    "choice": "placebo",
                    "readings": ["counts", "does not"],
                    "spec_settles": False,
                    "quote": "",
                    "changes_output": "yes",
                    "question": "Do placebo rows count?",
                }
            ]
        }
    )
    r = harness.run_pair(
        t, *agree, reviewer=FakeClient(lambda _m: unsettled), reviewer_version="v2", max_repairs=0
    )
    assert (r.decision, r.question) == ("escalated", "Do placebo rows count?")
    settled = json.dumps({"choices": []})
    ok = harness.run_pair(
        t, *agree, reviewer=FakeClient(lambda _m: settled), reviewer_version="v2", max_repairs=0
    )
    assert ok.decision == "accepted"
