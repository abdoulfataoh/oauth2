# coding: utf-8

from app.crud.users import (
    create_user,
    update_user_by_id,
    get_user_by_id,
    get_user_by_email,
    get_user_by_phone,
    get_user_by_username,
    get_users,
    delete_user_by_id,
    update_user_password,
)

from app.crud.otp import (
    create_otp,
    get_otp,
    increment_otp_attempts,
    delete_otp,
    delete_expired_otp,
)

from app.crud.clients import (
    create_client,
    get_clients,
    get_client_by_client_id,
    get_client_by_id,
    delete_client_by_id,
)

from app.crud.oauth_authorization_requests import (
    create_authorization_request,
    get_authorization_request_by_id,
    approve_authorization_request,
    delete_expired_authorization_requests,
    attach_user_to_authorization_request,
)

from app.crud.oauth_authorization_codes import (
    create_authorization_code,
    get_authorization_code,
    mark_authorization_code_as_used,
    delete_expired_authorization_codes,
)

from app.crud.sessions import (
    create_session,
    get_sessions_by_user_id,
    get_session_by_session_id,
    update_session_activity,
    deactivate_session,
    delete_session_by_id,
    delete_sessions_by_user_id,
)

__all__ = [
    'create_user',
    'update_user_by_id',
    'get_user_by_id',
    'get_user_by_email',
    'get_user_by_phone',
    'get_user_by_username',
    'get_users',
    'delete_user_by_id',
    'update_user_password',
]

__all__ += [
    'create_otp',
    'get_otp',
    'increment_otp_attempts',
    'delete_otp',
    'delete_expired_otp',
]

__all__ += [
    'create_client',
    'get_clients',
    'get_client_by_client_id',
    'get_client_by_id',
    'delete_client_by_id',
]

__all__ += [
    'create_authorization_request',
    'get_authorization_request_by_id',
    'approve_authorization_request',
    'delete_expired_authorization_requests',
    'attach_user_to_authorization_request',
]

__all__ += [
    'create_authorization_code',
    'get_authorization_code',
    'mark_authorization_code_as_used',
    'delete_expired_authorization_codes',
]

__all__ += [
    'create_session',
    'get_sessions_by_user_id',
    'get_session_by_session_id',
    'update_session_activity',
    'deactivate_session',
    'delete_session_by_id',
    'delete_sessions_by_user_id',
]
