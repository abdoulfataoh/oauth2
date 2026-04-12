# coding: utf-8

from pydantic import BaseModel


class Token(BaseModel):
    token: str
    token_type: str


class AccessTokenRequest(BaseModel):
    client_id: str
    grant_type: str
    authorization_code: str
    redirect_uri: str
    code_verifier: str
