from fastapi import HTTPException, status
from typing import Any


class AlreadyExists(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


class NotFound(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class PermissionDenied(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class NotAuthenticated(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class UnprocessableEntity(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=detail)


class DomainError(HTTPException):
    def __init__(self, detail: Any = None):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)