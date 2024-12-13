# coding: utf-8

from fastapi import APIRouter

from app.settings import API_PREFIX


__all__ = [
    'router',
]


router = APIRouter()


@router.get(API_PREFIX + '/health')
async def health() -> dict:
    return {'health': 'ok'}
