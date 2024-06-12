import json
import subprocess

import pytest

RETURN_CODE_OK = 0
RETURN_CODE_ERROR = 2


@pytest.mark.e2e()
def test_e2e_ok(expected_output_json: str) -> None:
    result = subprocess.run(
        [
            "python",
            "-m",
            "src.main",
            "-s",
            "tests/data/input/pricat.csv",
            "-m",
            "tests/data/input/mappings.csv",
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == RETURN_CODE_OK

    assert result.stderr == ""
    assert json.loads(result.stdout) == json.loads(expected_output_json)


@pytest.mark.e2e()
def test_e2e_error() -> None:
    result = subprocess.run(
        [
            "python",
            "-m",
            "src.main",
            "-s",
            "tests/data/input/pricat.csv",
            # Mappings missing
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == RETURN_CODE_ERROR

    assert result.stderr != ""
    assert result.stdout == ""
