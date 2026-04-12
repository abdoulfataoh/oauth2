# coding: utf-8

from typing import Annotated, TypeAlias

from fastapi import Depends, Security

from app import models as M
from app.exceptions.domain import PermissionDeniedError
from app.security.dependencies import (
    get_current_user_from_token,
    CurrentUser
)

__all__ = [
    'AdminUser',
    'Role',
    'ReadUserToken',
]


# ROLE BASED
def require_roles(*roles: str):
    """
    Check at least one role is present
    """

    def checker(user: CurrentUser):

        user_roles = user.roles or []

        if not any(role in user_roles for role in roles):
            raise PermissionDeniedError("Insufficient role")

        return user

    return checker


def Role(*roles: str):
    return Annotated[M.User, Depends(require_roles(*roles))]


AdminUser: TypeAlias = Annotated[
    M.User,
    Depends(require_roles('admin'))
]


# SCOPE BASED (OAuth2)
def require_scopes(*scopes: str):
    return Security(
        get_current_user_from_token,
        scopes=list(scopes)
    )


ReadUserToken = Annotated[
    M.User,
    Security(get_current_user_from_token, scopes=['profile:read'])
]
