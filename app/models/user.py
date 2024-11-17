# coding: utf-8


from typing import TYPE_CHECKING

from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    String,
    Boolean,
)

from app.models.base import BaseModelMixin

if TYPE_CHECKING:
    from app.models.authorization import Authorization  # noqa: F401


__all__ = [
    'User',
]


class User(BaseModelMixin):
    __tablename__ = 'auth_users'
    username = Column(String(64), unique=True, nullable=False)
    email = Column(String, unique=True, nullable=True)
    firstname = Column(String(128), nullable=False)
    lastname = Column(String(128), nullable=False)
    phone_number = Column(String(32), unique=True, nullable=False)
    roles = Column(String, default='user')
    disabled = Column(Boolean, default=True, nullable=False)
    password_hash = Column(String, nullable=False)
    authorizations = relationship('Authorization', back_populates='user')

    def get_roles(self) -> list[str]:
        return self.roles.split(',')

    def add_role(self, role) -> None:
        roles = self.get_roles()
        if role not in roles:
            roles.append(roles)
        self.roles = ','.join(roles)
