# coding: utf-8


class DomainException(Exception):
    error_code = "DOMAIN_ERROR"
    message = "A domain error occurred"

    def __init__(self, message=None):
        self.message = message or self.message
        super().__init__(self.message)

    def get_status_code(self):
        code = self.error_code

        if code.endswith("_NOT_FOUND"):
            return 404
        if code.endswith("_ALREADY_EXISTS"):
            return 409
        if code.endswith("_FAILED"):
            return 401
        if code.endswith("_EXPIRED"):
            return 401
        if code.startswith("INVALID"):
            return 400
        if code.startswith("PERMISSION"):
            return 403

        return 400


# VALIDATION / INPUT
class InvalidFieldsError(DomainException):
    error_code = "INVALID_FIELDS"
    message = "One or more fields are invalid."


class InvalidJSONFormatError(DomainException):
    error_code = "INVALID_JSON_FORMAT"
    message = "Invalid JSON format."


class UnsupportedFileTypeError(DomainException):
    error_code = "UNSUPPORTED_FILE_TYPE"
    message = "Unsupported file type."


# USER
class UserNotFoundError(DomainException):
    error_code = "USER_NOT_FOUND"
    message = "User not found."


class UserAlreadyExistsError(DomainException):
    error_code = "USER_ALREADY_EXISTS"
    message = "User already exists."


class UserDisabledError(DomainException):
    error_code = "USER_DISABLED"
    message = "User account is disabled."


class UserPhoneNotSetError(DomainException):
    error_code = "USER_PHONE_NOT_SET"
    message = "User phone is not set."


class UserEmailNotSetError(DomainException):
    error_code = "USER_EMAIL_NOT_SET"
    message = "User email is not set."


# AUTHENTICATION
class AuthenticationFailedError(DomainException):
    error_code = "AUTHENTICATION_FAILED"
    message = "Invalid username or password."


class AuthenticationRequiredError(DomainException):
    error_code = "AUTHENTICATION_FAILED"
    message = "Valid authentification required."


class InvalidAuthenticationSchemeError(DomainException):
    error_code = "INVALID_AUTH_SCHEME"
    message = "Invalid authentication scheme."


class InvalidAPIKeyError(DomainException):
    error_code = "INVALID_API_KEY"
    message = "Invalid API key."


class PermissionDeniedError(DomainException):
    error_code = "PERMISSION_DENIED"
    message = "Permission denied."


# CLIENT (OAuth)
class ClientNotFoundError(DomainException):
    error_code = "CLIENT_NOT_FOUND"
    message = "Client not found."


class ClientAlreadyExistsError(DomainException):
    error_code = "CLIENT_ALREADY_EXISTS"
    message = "Client already exists."


class ClientAuthenticationFailedError(DomainException):
    error_code = "CLIENT_AUTH_FAILED"
    message = "Invalid client credentials."


class InvalidClientRedirectURIError(DomainException):
    error_code = "INVALID_REDIRECT_URI"
    message = "Invalid client redirect URI."


# AUTHORIZATION (OAuth)
class AuthorizationRequestInvalidError(DomainException):
    error_code = "INVALID_AUTH_REQUEST"
    message = "Invalid authorization request."


class AuthorizationRequestExpiredError(DomainException):
    error_code = "AUTH_REQUEST_EXPIRED"
    message = "Authorization request expired."


class AuthorizationRequestAlreadyBoundError(DomainException):
    error_code = "AUTH_REQUEST_ALREADY_USED"
    message = "Authorization request already used."


class UnsupportedResponseTypeError(DomainException):
    error_code = "UNSUPPORTED_RESPONSE_TYPE"
    message = "Unsupported response type."


class UnsupportedGrantTypeError(DomainException):
    error_code = "UNSUPPORTED_GRANT_TYPE"
    message = "Unsupported grant type."


class InvalidScopeError(DomainException):
    error_code = "INVALID_SCOPE"
    message = "Invalid or unauthorized scope."


# PKCE
class InvalidCodeChallengeError(DomainException):
    error_code = "INVALID_CODE_CHALLENGE"
    message = "Invalid code challenge."


class InvalidCodeChallengeMethodError(DomainException):
    error_code = "INVALID_CODE_CHALLENGE_METHOD"
    message = "Invalid code challenge method."


# OTP
class InvalidOtpError(DomainException):
    error_code = "INVALID_OTP"
    message = "Invalid OTP."


class OtpExpiredError(DomainException):
    error_code = "OTP_EXPIRED"
    message = "OTP expired."


class TooManyVerificationAttemptsError(DomainException):
    error_code = "TOO_MANY_ATTEMPTS"
    message = "Too many verification attempts."


# TOKEN
class InvalidTokenError(DomainException):
    error_code = "INVALID_TOKEN"
    message = "Invalid token."


class TokenExpiredError(DomainException):
    error_code = "TOKEN_EXPIRED"
    message = "Token has expired."


class TokenDecodeError(DomainException):
    error_code = "TOKEN_DECODE_FAILED"
    message = "Token decoding failed."


# FILE / PROCESSING
class ParsingFileFailedError(DomainException):
    error_code = "PARSING_FILE_FAILED"
    message = "Parsing file failed."


class FileSizeLimitExceededError(DomainException):
    error_code = "FILE_SIZE_LIMIT_EXCEEDED"
    message = "File size limit exceeded."


class ContextLengthExceededError(DomainException):
    error_code = "CONTEXT_LENGTH_EXCEEDED"
    message = "Context length exceeded."


# GENERIC
class InternalServerError(DomainException):
    error_code = "INTERNAL_ERROR"
    message = "Internal server error."
