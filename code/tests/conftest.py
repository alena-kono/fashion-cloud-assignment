import pathlib

import pytest


@pytest.fixture()
def input_source_pricat_csv_path() -> pathlib.Path:
    return pathlib.Path("tests/data/input/pricat.csv")


@pytest.fixture()
def input_mappings_csv_path() -> pathlib.Path:
    return pathlib.Path("tests/data/input/mappings.csv")


@pytest.fixture()
def input_mappings_bonus_csv_path() -> pathlib.Path:
    return pathlib.Path("tests/data/input/mappings_bonus.csv")


@pytest.fixture()
def expected_output_json() -> str:
    with open("tests/data/output/acceptance.json") as f:
        return f.read()


@pytest.fixture()
def expected_output_json_bonus() -> str:
    with open("tests/data/output/acceptance_bonus.json") as f:
        return f.read()
