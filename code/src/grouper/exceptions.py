from src.exceptions import ApplicationError


class GrouperError(ApplicationError):
    message = "Grouper error"


class RequiredFieldMissingError(GrouperError):
    message = "Required field missing"
