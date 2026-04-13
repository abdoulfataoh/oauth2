# coding: utf-8

import pytest


@pytest.mark.asyncio
async def test_signup_email(client):
    payload = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john@test.com',
        'password': 'password123'
    }

    res = await client.post('/oauth2/signup', json=payload)

    assert res.status_code == 201
    data = res.json()

    assert data['email'] == 'john@test.com'


@pytest.mark.asyncio
async def test_signup_sets_cookie(client):
    payload = {
        'firstname': 'Jane',
        'lastname': 'Doe',
        'email': 'jane@test.com',
        'password': 'password123'
    }

    res = await client.post('/oauth2/signup', json=payload)

    assert 'ui_access_token' in res.cookies


@pytest.mark.asyncio
async def test_signup_without_contact(client):
    payload = {
        'firstname': 'John',
        'lastname': 'Doe',
        'password': 'password123'
    }

    res = await client.post('/oauth2/signup', json=payload)

    assert res.status_code == 422
