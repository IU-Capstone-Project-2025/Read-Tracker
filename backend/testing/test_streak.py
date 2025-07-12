import pytest
import requests
import os

PORT = 8000  # os.getenv("BACKEND_PORT")


def test_check_in():
    header = {
        "Content-Type": "application/json"
    }

    check_in_url = f"http://localhost:{PORT}/me/check_in"
    get_streaks_url = f"http://localhost:{PORT}/me/streaks"

    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }
    get_streaks_response_before = requests.post(get_streaks_url, headers=header, json=data)
    print(get_streaks_response_before.json())
    check_in_response = requests.post(check_in_url, headers=header, json=data)
    print(check_in_response.json())
    get_streaks_response_after = requests.post(get_streaks_url, headers=header, json=data)
    print(get_streaks_response_after.json())
    assert check_in_response.status_code == 200
    assert get_streaks_response_after.json()["data"][0] is not None