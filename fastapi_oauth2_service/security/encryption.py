# coding: utf-8

from passlib.hash import bcrypt


class Secret:

    def __init__(self) -> None:
        pass

    def hash(secret: str) -> str:
        hash = bcrypt.hash(secret)
        return hash

    def verify(secret: str, hash: str) -> bool:
        status = bcrypt.verify(secret, hash)
        return status
