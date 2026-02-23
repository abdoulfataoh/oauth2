# coding: utf-8

from pydantic import BaseModel


class Consent(BaseModel):
    request_id: str
    approved: bool
