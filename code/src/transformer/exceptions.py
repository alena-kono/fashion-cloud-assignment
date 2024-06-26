from src.exceptions import ApplicationError


class TransformerError(ApplicationError):
    message = "Transformer Error"


class MappingError(ApplicationError):
    message = "Mapping error"


class MappingBuildError(MappingError):
    message = "Mapping build error"


class RowDoesNotContainFieldError(TransformerError):
    message = "Row does not contain field"
