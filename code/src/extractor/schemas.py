import dataclasses
import pathlib


@dataclasses.dataclass(frozen=True)
class CsvSourceSchemaRequired:
    article_number: str


@dataclasses.dataclass(frozen=True)
class CsvMappingSchemaRequired:
    source: str
    destination: str
    source_type: str
    destination_type: str


@dataclasses.dataclass(frozen=True)
class CsvFileReaderMeta:
    path: pathlib.Path
    delimiter: str
    encoding: str = "utf-8"
