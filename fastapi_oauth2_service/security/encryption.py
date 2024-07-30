# coding: utf-8

from passlib.hash import bcrypt
import secrets


class Secret:

    def __init__(self) -> None:
        pass

    def hash(self, secret: str) -> str:
        hash = bcrypt.hash(secret)
        return hash

    def verify(self, secret: str, hash: str) -> bool:
        status = bcrypt.verify(secret, hash)
        return status

    def generate(self, length: int = 32) -> str:
        secret = secrets.token_urlsafe(length)
        return secret
