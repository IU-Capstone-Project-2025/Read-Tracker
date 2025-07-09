import pytest
import requests
import os

PORT = 8000  # os.getenv("BACKEND_PORT")


def test_check_in():
    header = {
        "Content-Type": "application/json"
    }

    url = f"http://localhost:{PORT}/me/check_in"

    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }
    check_in_response = requests.post(url, headers=header, json=data)

    assert check_in_response.status_code == 200
