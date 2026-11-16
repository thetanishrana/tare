"""A silent error that equals a stored defensible reading is recorded as such (class unchanged)."""

import pandas as pd

import tare.score as score_mod
import tare.tasks as tasks_mod
from tare.score import SILENT, score_output
from tare.tasks import Task

TASK = Task(
    {
        "id": "t-amb",
        "keys": ["K"],
        "target_vars": ["V"],
        "output_contract": {"columns": {"K": "string", "V": "string"}, "nullable": ["V"]},
        "readings": [
            {"id": "alt", "description": "other reading"},
            {"id": "gone", "description": "x"},
        ],
    }
)


def _frame(vals):
    return pd.DataFrame({"K": ["a", "b", "c"], "V": vals})


def _setup(tmp_path, monkeypatch):
    monkeypatch.setattr(tasks_mod, "ANSWERS_DIR", tmp_path)
    monkeypatch.setattr(score_mod, "ANSWERS_DIR", tmp_path)
    _frame(["Y", "Y", None]).to_parquet(tmp_path / "t-amb.parquet", index=False)
    _frame(["Y", None, None]).to_parquet(tmp_path / "t-amb__alt.parquet", index=False)


def _score(tmp_path, vals):
    out = tmp_path / "out.parquet"
    _frame(vals).to_parquet(out, index=False)
    return score_output(TASK, out)


def test_matching_alternative_is_recorded_but_still_silent(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    s = _score(tmp_path, ["Y", None, None])
    assert s.klass == SILENT and s.matches_reading == "alt"
    assert s.to_dict()["matches_reading"] == "alt"


def test_oracle_match_and_unmatched_error_have_no_reading(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    assert _score(tmp_path, ["Y", "Y", None]).matches_reading is None
    s = _score(tmp_path, [None, None, "Y"])
    assert s.klass == SILENT and s.matches_reading is None


def test_rowset_is_target_makes_missing_rows_a_silent_error(tmp_path, monkeypatch):
    _setup(tmp_path, monkeypatch)
    raw = dict(TASK.raw, rowset_is_target=True)
    task = Task(raw)
    out = tmp_path / "out.parquet"
    pd.DataFrame({"K": ["a", "b"], "V": ["Y", "Y"]}).to_parquet(out, index=False)  # key "c" missing
    assert score_output(task, out).klass == SILENT
    assert (
        score_output(TASK, out).klass == "loud_error"
    )  # without the flag a missing key is a contract break
