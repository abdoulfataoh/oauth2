# coding: utf-8

import pytest
from app.schemas.user import UserCreate


def test_user_create_with_email():
    user = UserCreate(
        firstname='John',
        lastname='Doe',
        email='john@test.com',
        password='password123'
    )

    assert user.email == 'john@test.com'


def test_user_create_with_phone():
    user = UserCreate(
        firstname='John',
        lastname='Doe',
        phone='12345678',
        password='password123'
    )

    assert user.phone == '12345678'


def test_user_create_without_contact():
    with pytest.raises(ValueError):
        UserCreate(
            firstname='John',
            lastname='Doe',
            password='password123'
        )


def test_password_secret():
    user = UserCreate(
        firstname='John',
        lastname='Doe',
        email='john@test.com',
        password='password123'
    )

    assert user.password.get_secret_value() == 'password123'