from unittest.mock import Mock, patch

import pytest

from src.services.auth import auth_service


def test_get_contacts(client, get_token):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("api/contacts", headers=headers)
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 0


def test_create_contact(client, get_token, monkeypatch):
    with patch.object(auth_service, 'cache') as redis_mock:
        redis_mock.get.return_value = None
        token = get_token
        headers = {"Authorization": f"Bearer {token}"}
        response = client.post("api/contacts", headers=headers, json={
            "first_name": "test",
            "last_name": "test",
            "email": "test@example.com",
            "phone": "0991234567",
            "birthday": "test",
        })
        assert response.status_code == 201, response.text
        data = response.json()
        assert "id" in data
        assert data["first_name"] == "test"
        assert data["last_name"] == "test"
        assert data["email"] == "test@example.com"
        assert data["phone"] == "0991234567"
        assert data["birthday"] == "test"
