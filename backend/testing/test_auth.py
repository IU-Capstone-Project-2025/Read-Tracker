import pytest
import requests
import os

PORT = 8000 # os.getenv("BACKEND_PORT")

# Doesn't consider case when email already exist
def test_register():
    url = f"http://localhost:{PORT}/auth/register"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "name": "Ivan",
        "email": "justemail123@yandex.ru",
        "password": "qwerty"
    }

    response = requests.post(url, headers=header, json=data)
    if response.status_code == 400 and response.json()["detail"]["message"] == "Email already exists":
        assert True
    else:
        assert response.status_code == 201


def test_bad_register():
    url = f"http://localhost:{PORT}/auth/register"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "name": "Ivan",
        "email": "Not mail at all",
        "password": "qwerty"
    }

    response = requests.post(url, headers=header, json=data)
    assert response.status_code == 400


def test_login():
    url = f"http://localhost:{PORT}/auth/login"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "email": "justemail123@yandex.ru",
        "password": "qwerty"
    }

    response = requests.post(url, headers=header, json=data)
    assert response.status_code == 200


def test_bad_login():
    url = f"http://localhost:{PORT}/auth/login"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "email": "justemail123@yandex.ru",
        "password": "WrongPassword"
    }
    response = requests.post(url, headers=header, json=data)
    print(response.json())
    assert response.status_code == 401


def test_get_profile():
    url = f"http://localhost:{PORT}/auth/profile"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }

    response = requests.get(url, headers=header, json=data)
    assert response.status_code == 200


def test_invalid_profile_id():
    url = f"http://localhost:{PORT}/auth/profile"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-1000-000000000001"
    }

    response = requests.get(url, headers=header, json=data)
    assert response.status_code == 400


def test_update_avatar():
    url = f"http://localhost:{PORT}/auth/profile/avatar"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "avatar": "some avatar"
    }

    response = requests.put(url, headers=header, json=data)
    assert response.status_code == 200


def test_invalid_avatar_id():
    url = f"http://localhost:{PORT}/auth/profile/avatar"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000001110001",
        "avatar": "some avatar"
    }

    response = requests.put(url, headers=header, json=data)
    assert response.status_code == 400


def test_valid_password_restore():
    url = f"http://localhost:{PORT}/auth/profile/password"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "password": "qwerty"
    }

    response = requests.put(url, headers=header, json=data)
    assert response.status_code == 200


def test_invalid_password_restore():
    url = f"http://localhost:{PORT}/auth/profile/password"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "55555555-0000-0000-0000-000000000001",
        "password": "new_password"
    }

    response = requests.put(url, headers=header, json=data)
    assert response.status_code == 400
