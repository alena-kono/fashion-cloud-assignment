class ApplicationError(Exception):
    """Base class for all exceptions in the application."""

    message = "An unknown error occurred."

    def __init__(self, message: str | None = None) -> None:
        if message is None:
            message = self.message
        super().__init__(message)
        self.message = message

    def __str__(self) -> str:
        return self.message
