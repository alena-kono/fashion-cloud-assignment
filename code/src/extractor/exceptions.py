from src.exceptions import ApplicationError


class ExtractorError(ApplicationError):
    message = "Extraction error"


class CsvReaderError(ExtractorError):
    message = "CSV reader error"


class InvalidCsvSchemaError(ExtractorError):
    message = "Invalid csv schema"
