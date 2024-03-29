from datetime import date

import pytest
from pytest import mark, fixture
from unittest.mock import patch, AsyncMock

from src.services.auth import auth_service

user_data = {"username": "agent007", "email": "agent7@gmail.com", "password": "12345678"}


@pytest.mark.usefixtures('mock_rate_limit')
def test_get_contacts(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_get_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token

        response1 = client.post(
            "api/contacts",
            json={
                "name": "test_name",
                "surname": "test_surname",
                "email": "test_mail@gmail.com",
                "phone_number": "+380501111111",
                "birth_date": str(date(1981, 1, 11)),  
                },
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response1.status_code == 201, response1.text

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(
            "api/contacts/{contact_id}".format(contact_id=response1.json()['id']),
            headers=headers,
        )
        assert response.status_code == 200
        expected_keys = ["id", "name", "surname", "email", "phone_number", "birth_date"]
        assert all(key in response.json() for key in expected_keys)


def test_get_contact_invalid(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(
            "api/contacts/{contact_id}".format(contact_id=0),
            headers=headers,
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
    response = client.post(
            "api/contacts",
            json={
                "name": "test_name",
                "surname": "test_surname",
                "email": "test_mail@gmail.com",
                "phone_number": "+380501111111",
                "birth_date": str(date(1981, 1, 11)),  
                },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 201
    assert response.json().get('id') is not None


@pytest.mark.asyncio
async def test_create_contact_invalid(client, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = "get_token_invalid"
    response = client.post(
            "api/contacts",
            json={
                "name": "test_name",
                "surname": "test_surname",
                "email": "test_mail@gmail.com",
                "phone_number": "+380501111111",
                "birth_date": str(date(1981, 1, 11)),  
                },
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 401


def test_get_contact_invalid_404(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token

        headers = {"Authorization": f"Bearer {token}"}
        response = client.get(
            "api/contacts/{contact_id}".format(contact_id=17),
            headers=headers,
        )
        assert response.status_code == 404, response.text
        assert response.json()['detail'] == "NOT FOUND"


def test_delete_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
    response = client.delete(
            "api/contacts/{contact_id}".format(contact_id=17),
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 204, response.text


def test_update_contact(client, monkeypatch, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.redis", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.identifier", AsyncMock())
        monkeypatch.setattr("fastapi_limiter.FastAPILimiter.http_callback", AsyncMock())
        token = get_token
    contact = {
            "name": "test_name_update",
            "surname": 'test_surname_update',
            "email": 'test_mail_update@gmail.com',
            "phone_number": '+380509999999',
            "birth_date": str(date(1999, 9, 19)),
            }

    response = client.put(
            "api/contacts/{contact_id}".format(contact_id=1),
            json=contact,
            headers={"Authorization": f"Bearer {token}"},
        )
    assert response.status_code == 200
