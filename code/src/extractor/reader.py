import csv
import dataclasses
import typing as tp

from src.extractor.exceptions import (
    CsvReaderError,
    InvalidCsvSchemaError,
)
from src.extractor.schemas import (
    CsvFileReaderMeta,
    CsvMappingSchemaRequired,
    CsvSourceSchemaRequired,
)

CsvFieldnames = tp.Sequence[str]
Row = dict[str, str]


class CsvReader:
    def __init__(
        self,
        file_meta: CsvFileReaderMeta,
        validation_schema: type[CsvSourceSchemaRequired]
        | type[CsvMappingSchemaRequired],
    ) -> None:
        self.file_meta = file_meta

        self._validation_schema = validation_schema
        self._validate_file()

    def read_by_row(self) -> tp.Generator[Row, None, None]:
        with open(self.file_meta.path, encoding=self.file_meta.encoding) as csv_file:
            reader = csv.DictReader(csv_file, delimiter=self.file_meta.delimiter)

            if not reader.fieldnames:
                raise InvalidCsvSchemaError("Header fieldnames are missing")
            self._validate_schema(header=reader.fieldnames)

            yield from reader

    def _validate_file(self) -> None:
        if not self.file_meta.path.exists():
            raise FileNotFoundError(f"{self.file_meta.path}")

        if not self.file_meta.path.is_file() or self.file_meta.path.suffix != ".csv":
            raise CsvReaderError(f"File is not a CSV file: {self.file_meta.path}")

    def _validate_schema(self, header: CsvFieldnames) -> None:
        """Validate a CSV header to contain required fields."""

        required_fields = dataclasses.fields(self._validation_schema)
        if not any(field.name in header for field in required_fields):
            raise InvalidCsvSchemaError(
                f"Missing required fields in CSV file: {self.file_meta.path}"
            )
