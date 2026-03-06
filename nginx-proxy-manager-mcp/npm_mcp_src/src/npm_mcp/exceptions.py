"""Custom exceptions for NPM API client."""


class NpmClientError(Exception):
    pass

class NpmAuthenticationError(NpmClientError):
    pass

class NpmConnectionError(NpmClientError):
    pass

class NpmNotFoundError(NpmClientError):
    pass

class NpmApiError(NpmClientError):
    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code
