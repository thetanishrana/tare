import datetime as dt

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from tare.compare import compare_frames, contract_violations
from tare.score import CORRECT, LOUD, SILENT, score_output
from tare.tasks import Task

KINDS = {"K": "string", "S": "string", "D": "date", "N": "number"}


def cmp(left, right, targets):
    return compare_frames(pd.DataFrame(left), pd.DataFrame(right), ["K"], targets, KINDS)


def test_identical_agree():
    a = {"K": ["a", "b"], "S": ["Y", None]}
    assert cmp(a, a, ["S"]).agree


def test_null_equals_null_but_not_value():
    a = {"K": ["a", "b"], "S": ["Y", None]}
    b = {"K": ["a", "b"], "S": ["Y", "N"]}
    r = cmp(a, b, ["S"])
    assert not r.agree and r.mismatches == {"S": 1}


def test_empty_string_is_null():
    a = {"K": ["a"], "S": [None]}
    b = {"K": ["a"], "S": [""]}
    assert cmp(a, b, ["S"]).agree


def test_number_tolerance():
    a = {"K": ["a", "b"], "N": [1.0, 1e6]}
    ok = {"K": ["a", "b"], "N": [1.0 + 1e-10, 1e6 + 1e-4]}
    bad = {"K": ["a", "b"], "N": [1.0001, 1e6]}
    assert cmp(a, ok, ["N"]).agree
    assert cmp(a, bad, ["N"]).mismatches == {"N": 1}


def test_nan_vs_value_number():
    a = {"K": ["a"], "N": [float("nan")]}
    assert cmp(a, {"K": ["a"], "N": [0.0]}, ["N"]).mismatches == {"N": 1}
    assert cmp(a, {"K": ["a"], "N": [float("nan")]}, ["N"]).agree


def test_date_vs_timestamp_same_day():
    a = {"K": ["a"], "D": [dt.date(2014, 1, 2)]}
    b = {"K": ["a"], "D": [pd.Timestamp("2014-01-02 00:00:00")]}
    assert cmp(a, b, ["D"]).agree
    c = {"K": ["a"], "D": [dt.date(2014, 1, 3)]}
    assert not cmp(a, c, ["D"]).agree


def test_missing_and_extra_keys():
    a = {"K": ["a", "b"], "S": ["Y", "Y"]}
    b = {"K": ["a", "c"], "S": ["Y", "Y"]}
    r = cmp(a, b, ["S"])
    assert (r.missing_keys, r.extra_keys) == (1, 1) and not r.agree


def _task(tmp_cols=None):
    return Task(
        {
            "id": "t",
            "dataset": "ADSL",
            "keys": ["K"],
            "target_vars": ["S"],
            "oracle_id": "std",
            "split": "dev",
            "output_contract": {
                "columns": {"K": "string", "S": "string"},
                "allowed_values": {"S": ["Y", "N"]},
                "nullable": [],
            },
        }
    )


def _write(path, df):
    pq.write_table(pa.Table.from_pandas(pd.DataFrame(df)), path)


def test_scoring_classes(tmp_path):
    task = _task()
    answer = pd.DataFrame({"K": ["a", "b"], "S": ["Y", "N"]})
    p = tmp_path / "r.parquet"
    _write(p, {"K": ["a", "b"], "S": ["Y", "N"]})
    assert score_output(task, p, answer).klass == CORRECT
    _write(p, {"K": ["a", "b"], "S": ["Y", "Y"]})
    s = score_output(task, p, answer)
    assert s.klass == SILENT and s.compare.mismatched_records == 1
    _write(p, {"K": ["a"], "S": ["Y"]})  # missing key
    assert score_output(task, p, answer).klass == LOUD
    _write(p, {"K": ["a", "b"], "S": ["Y", "maybe"]})  # outside allowed values
    assert score_output(task, p, answer).klass == LOUD
    _write(p, {"K": ["a", "b"], "S": ["Y", None]})  # null where not nullable
    assert score_output(task, p, answer).klass == LOUD
    _write(p, {"K": ["a", "b"], "T": ["Y", "N"]})  # missing column
    assert score_output(task, p, answer).klass == LOUD
    assert score_output(task, tmp_path / "nope.parquet", answer).klass == LOUD


def test_contract_wrong_type(tmp_path):
    p = tmp_path / "r.parquet"
    _write(p, {"K": ["a"], "S": [1]})
    df = pd.read_parquet(p)
    probs = contract_violations(p, _task().contract(), df)
    assert any("type" in x for x in probs)


def test_output_digest_ignores_row_order_and_empty_string():
    from tare.compare import output_digest

    a = pd.DataFrame({"K": ["a", "b"], "S": ["Y", None]})
    b = pd.DataFrame({"K": ["b", "a"], "S": ["", "Y"]})
    c = pd.DataFrame({"K": ["a", "b"], "S": ["Y", "N"]})
    assert output_digest(a, ["K"], ["S"], KINDS) == output_digest(b, ["K"], ["S"], KINDS)
    assert output_digest(a, ["K"], ["S"], KINDS) != output_digest(c, ["K"], ["S"], KINDS)


def test_tz_aware_timestamp_equals_plain_date():
    a = {"K": ["a", "b"], "D": [pd.Timestamp("2014-01-03", tz="UTC"), None]}
    b = {"K": ["a", "b"], "D": [dt.date(2014, 1, 3), None]}
    assert cmp(a, b, ["D"]).agree
    c = {"K": ["a", "b"], "D": [dt.date(2014, 1, 4), None]}
    assert cmp(a, c, ["D"]).mismatches == {"D": 1}
