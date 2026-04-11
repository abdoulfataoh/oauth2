# coding: utf-8


from app.services.oauth_service import (
    request_authorize,
    attach_user_to_request,
    get_authorization_request_by_id,
    approve_consent,
)

from app.services.client_service import (
    create_client,
    get_clients,
    get_client_by_client_id,
    get_client_by_id,
    delete_client_by_id,
)

from app.services.user_verification_service import (
    send_otp,
    validate_signup,
    validate_contact_change,
    validate_password_change,
    resolve_otp_recipient,
    validate_otp_without_consume,
)

from app.services.user_service import (
    signup,
    create_user,
    update_user_by_id,
    get_users,
    get_user_by_id,
    delete_user_by_id,
    silent_get_user_by_contact,
    update_user_password,
    authenticate_user,
)

from app.services.session_service import (
    create_session,
    get_my_sessions,
    logout_session,
)

__all__ = [
    # oauth_service
    "request_authorize",
    "attach_user_to_request",
    "get_authorization_request_by_id",
    "approve_consent",

    # client_service
    "create_client",
    "get_clients",
    "get_client_by_client_id",
    "get_client_by_id",
    "delete_client_by_id",

    # user_verification_service
    "send_otp",
    "validate_signup",
    "validate_contact_change",
    "validate_password_change",
    "resolve_otp_recipient",
    "validate_otp_without_consume",

    # user_service
    "signup",
    "create_user",
    "update_user_by_id",
    "get_users",
    "get_user_by_id",
    "delete_user_by_id",
    "silent_get_user_by_contact",
    "update_user_password",
    "authenticate_user",

    # session_service
    "create_session",
    "get_my_sessions",
    "logout_session",
]
