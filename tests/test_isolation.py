import pytest

from tare.isolation import IsolationError, check_workdir, validate_mount
from tare.tasks import ANSWERS_DIR, BENCHMARK, ORACLE_DIR, ROOT


def test_mount_inside_workdir_ok(tmp_path):
    (tmp_path / "inputs").mkdir()
    assert validate_mount(tmp_path / "inputs", tmp_path) == (tmp_path / "inputs").resolve()


@pytest.mark.parametrize(
    "bad",
    [ORACLE_DIR, ORACLE_DIR / "std", ANSWERS_DIR, ROOT / "results" / "k1", BENCHMARK / "reference"],
)
def test_forbidden_paths_refused(bad):
    # even if the caller (wrongly) made the forbidden path its own allowed root
    with pytest.raises(IsolationError):
        validate_mount(bad, bad)


def test_parent_of_forbidden_refused():
    with pytest.raises(IsolationError):
        validate_mount(ROOT / "data", ROOT / "data")  # contains data/oracle and data/answers


def test_mount_outside_workdir_refused(tmp_path):
    other = tmp_path / "other"
    other.mkdir()
    work = tmp_path / "work"
    work.mkdir()
    with pytest.raises(IsolationError):
        validate_mount(other, work)


def test_symlink_escape_refused(tmp_path):
    work = tmp_path / "work"
    work.mkdir()
    (work / "inputs").symlink_to(ORACLE_DIR)  # symlink pointing at the oracle
    with pytest.raises(IsolationError):
        validate_mount(work / "inputs", work)


def test_workdir_with_stray_files_refused(tmp_path):
    (tmp_path / "inputs").mkdir()
    (tmp_path / "out").mkdir()
    (tmp_path / "code.py").write_text("")
    check_workdir(tmp_path, "code.py")
    (tmp_path / "answer.parquet").write_text("x")
    with pytest.raises(IsolationError):
        check_workdir(tmp_path, "code.py")
