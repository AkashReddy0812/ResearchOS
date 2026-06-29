class ResearchOSError(Exception):
    """
    Base exception for the application.
    """

    def __init__(
        self,
        message: str,
        error_code: str = "APPLICATION_ERROR",
    ) -> None:
        self.message = message
        self.error_code = error_code
        super().__init__(message)