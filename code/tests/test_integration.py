import json
import pathlib

import pytest

from src.extractor import reader
from src.main import run_pipeline


@pytest.mark.integration()
def test_run_pipeline(
    capsys: pytest.CaptureFixture[str],
    input_source_pricat_csv_path: pathlib.Path,
    input_mappings_csv_path: pathlib.Path,
    expected_output_json: str,
) -> None:
    delimiter = ";"
    source_csv = reader.CsvFileReaderMeta(
        path=input_source_pricat_csv_path, delimiter=delimiter
    )
    mappings_csv = reader.CsvFileReaderMeta(
        path=input_mappings_csv_path, delimiter=delimiter
    )

    run_pipeline(source_csv, mappings_csv)

    captured = capsys.readouterr()

    assert json.loads(captured.out) == json.loads(expected_output_json)


@pytest.mark.integration()
def test_run_pipeline_mini(
    capsys: pytest.CaptureFixture[str],
    input_source_pricat_mini_csv_path: pathlib.Path,
    input_mappings_csv_path: pathlib.Path,
    expected_output_mini_json: str,
) -> None:
    delimiter = ";"
    source_csv = reader.CsvFileReaderMeta(
        path=input_source_pricat_mini_csv_path, delimiter=delimiter
    )
    mappings_csv = reader.CsvFileReaderMeta(
        path=input_mappings_csv_path, delimiter=delimiter
    )

    run_pipeline(source_csv, mappings_csv)

    captured = capsys.readouterr()

    assert json.loads(captured.out) == json.loads(expected_output_mini_json)


@pytest.mark.integration()
def test_run_pipeline_bonus(
    capsys: pytest.CaptureFixture[str],
    input_source_pricat_csv_path: pathlib.Path,
    input_mappings_bonus_csv_path: pathlib.Path,
    expected_output_json_bonus: str,
) -> None:
    delimiter = ";"
    source_csv = reader.CsvFileReaderMeta(
        path=input_source_pricat_csv_path, delimiter=delimiter
    )
    mappings_csv = reader.CsvFileReaderMeta(
        path=input_mappings_bonus_csv_path, delimiter=delimiter
    )

    run_pipeline(source_csv, mappings_csv)

    captured = capsys.readouterr()

    assert json.loads(captured.out) == json.loads(expected_output_json_bonus)
