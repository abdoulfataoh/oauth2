# coding: utf-8

from fastapi import HTTPException


# 400
class ParsingFileFailedException(HTTPException):
    def __init__(self, detail: str = "Parsing file failed."):
        super().__init__(status_code=400, detail=detail)


class InvalidUserSchemeException(HTTPException):
    def __init__(self, detail: str = "Invalid user scheme."):
        super().__init__(status_code=400, detail=detail)


# 403
class InvalidAuthenticationSchemeException(HTTPException):
    def __init__(self, detail: str = "Invalid authentication scheme."):
        super().__init__(status_code=403, detail=detail)


class InvalidAPIKeyException(HTTPException):
    def __init__(self, detail: str = "Invalid API key."):
        super().__init__(status_code=403, detail=detail)


# 404
class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(status_code=400, detail=detail)


class ClientNotFoundException(HTTPException):
    def __init__(self, detail: str = "Client not found."):
        super().__init__(status_code=400, detail=detail)


# 409
class ConflictedUserException(HTTPException):
    def __init__(self, detail: str = "Conflict: user already exists."):
        super().__init__(status_code=409, detail=detail)


class ConflictedClientException(HTTPException):
    def __init__(self, detail: str = "Conflict: Client already exists."):
        super().__init__(status_code=409, detail=detail)


# 413
class ContextLengthExceededException(HTTPException):
    def __init__(self, detail: str = "Context length exceeded."):
        super().__init__(status_code=413, detail=detail)


class FileSizeLimitExceededException(HTTPException):
    def __init__(self, detail: str = "File size limit exceeded."):
        super().__init__(status_code=413, detail=detail)


# 422
class InvalidJSONFormatException(HTTPException):
    def __init__(self, detail: str = "Invalid JSON file format."):
        super().__init__(status_code=422, detail=detail)


class InvalidFieldsException(HTTPException):
    def __init__(self, detail: str = "Some fields are invalid format."):
        super().__init__(status_code=422, detail=detail)


class UnsupportedFileTypeException(HTTPException):
    def __init__(self, detail: str = "Unsupported file type."):
        super().__init__(status_code=422, detail=detail)