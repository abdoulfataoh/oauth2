# coding: utf-8

from app.crud.users import (
    create_user,
    update_user_by_id,
    get_user_by_id,
    get_user_by_username,
    get_users,
    delete_user_by_id,
)

from app.crud.clients import (
    create_client,
    get_clients,
    get_client_by_client_id,
    delete_client_by_client_id,
)

from app.crud.oauth_authorization_request import (
    create_authorization_request,
    get_authorization_request_by_id,
    approve_authorization_request,
    delete_expired_authorization_requests,
    attach_user_to_authorization_request,
)

from app.crud.oauth_authorization_code import (
    create_authorization_code,
    get_authorization_code,
    mark_authorization_code_as_used,
    delete_expired_authorization_codes,
)

__all__ = [
    'create_user',
    'update_user_by_id',
    'get_user_by_id',
    'get_user_by_username',
    'get_users',
    'delete_user_by_id',
]

__all__ += [
    'create_client',
    'get_clients',
    'get_client_by_client_id',
    'delete_client_by_client_id',
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
