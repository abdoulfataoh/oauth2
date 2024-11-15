# coding: utf-8

from fastapi import APIRouter


__all__ = [
    'router',
]


router = APIRouter()


@router.get('/health')
async def health() -> dict:
    return {'health': 'ok'}
