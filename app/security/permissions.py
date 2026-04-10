# coding: utf-8

from typing import Annotated, TypeAlias

from fastapi import Depends

from app import models as M
from app.exceptions.http import PermissionDeniedException
from app.security.dependencies import CurrentUser

__all__ = [
    'AdminUser'
]


def require_roles(*roles: str):
    """
    Check at least one role in roles satisfied
    """

    def check_roles(user: CurrentUser):

        user_roles = user.roles or []

        if not any(role in roles for role in user_roles):
            raise PermissionDeniedException()

        return user

    return check_roles


def Role(*roles: str):
    return Annotated[M.User, Depends(require_roles(*roles))]


AdminUser: TypeAlias = Annotated[
    M.User,
    Depends(require_roles('admin'))
]
