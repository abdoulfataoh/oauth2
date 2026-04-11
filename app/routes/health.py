# coding: utf-8

from fastapi import APIRouter

router = APIRouter()


@router.get('/health')
async def health() -> dict:
    return {'status': 'ok'}
