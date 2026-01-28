# coding: utf-8

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base exception for the application"""
    pass


# 400 BAD REQUEST
class ParsingFileFailedException(AppException):
    def __init__(self, detail: str = "Parsing file failed."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class InvalidUserSchemeException(AppException):
    def __init__(self, detail: str = "Invalid user scheme."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class UnsupportedResponseTypeException(AppException):
    def __init__(self, detail: str = "Unsupported response type."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class UnsupportedGrantTypeException(AppException):
    def __init__(self, detail: str = "Unsupported grant type."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class RedirectUriMismatchException(AppException):
    def __init__(self, detail: str = "Redirect URI does not match the registered URI."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class AuthorizationRequestInvalidException(AppException):
    def __init__(self, detail: str = "Invalid authorization request."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class AuthorizationRequestExpiredException(AppException):
    def __init__(self, detail: str = "Authorization request expired."):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail)


class InvalidScope(AppException):
    def __init__(self, detail: str = "The requested scope is invalid, unknown, or not allowed for this client."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


# 401 UNAUTHORIZED
class LoginFailedException(AppException):
    def __init__(self, detail: str = "Invalid username or password."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ClientAuthFailedException(AppException):
    def __init__(self, detail: str = "Invalid client secret or id."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class InvalidClientRedirectURIException(AppException):
    def __init__(self, detail: str = "Invalid client redirect uri."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class InvalidTokenException(AppException):
    def __init__(self, detail: str = "Invalid token."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class ExpiredTokenException(AppException):
    def __init__(self, detail: str = "Token has expired."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


class TokenDecodeException(AppException):
    def __init__(self, detail: str = "Token decoding failed."):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail)


# 403 FORBIDDEN
class InvalidAuthenticationSchemeException(AppException):
    def __init__(self, detail: str = "Invalid authentication scheme."):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


class InvalidAPIKeyException(AppException):
    def __init__(self, detail: str = "Invalid API key."):
        super().__init__(status.HTTP_403_FORBIDDEN, detail)


# 404 NOT FOUND
class UserNotFoundException(AppException):
    def __init__(self, detail: str = "User not found."):
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


class ClientNotFoundException(AppException):
    def __init__(self, detail: str = "Client not found."):
        super().__init__(status.HTTP_404_NOT_FOUND, detail)


# 409 CONFLICT
class ConflictedUserException(AppException):
    def __init__(self, detail: str = "User already exists."):
        super().__init__(status.HTTP_409_CONFLICT, detail)


class ConflictedClientException(AppException):
    def __init__(self, detail: str = "Client already exists."):
        super().__init__(status.HTTP_409_CONFLICT, detail)


# 413 PAYLOAD TOO LARGE
class ContextLengthExceededException(AppException):
    def __init__(self, detail: str = "Context length exceeded."):
        super().__init__(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail)


class FileSizeLimitExceededException(AppException):
    def __init__(self, detail: str = "File size limit exceeded."):
        super().__init__(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail)


# 422 UNPROCESSABLE ENTITY
class InvalidJSONFormatException(AppException):
    def __init__(self, detail: str = "Invalid JSON format."):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail)


class InvalidFieldsException(AppException):
    def __init__(self, detail: str = "One or more fields have invalid format."):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail)


class UnsupportedFileTypeException(AppException):
    def __init__(self, detail: str = "Unsupported file type."):
        super().__init__(status.HTTP_422_UNPROCESSABLE_ENTITY, detail)
