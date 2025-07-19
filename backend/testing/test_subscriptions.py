import pytest
import requests

PORT = 8000
BASE_URL = f"http://localhost:{PORT}/subscriptions"
HEADERS = {
    "Content-Type": "application/json"
}

VALID_USER_ID = "00000000-0000-0000-0000-000000000001"
INVALID_USER_ID = "99999999-0000-0000-0000-000000000002"


def test_subscribe():
    data = {
        "subscriber_id": VALID_USER_ID,
        "publisher_id": VALID_USER_ID
    }

    response = requests.post(BASE_URL, headers=HEADERS, json=data)
    print(response.json())
    assert response.status_code in [200, 400]  # 400 if already subscribed


def test_unsubscribe():
    data = {
        "subscriber_id": VALID_USER_ID,
        "publisher_id": VALID_USER_ID
    }

    response = requests.delete(BASE_URL, headers=HEADERS, json=data)
    print(response.json())
    assert response.status_code in [200, 400]  # 400 if not subscribed


def test_get_publisher_reviews():
    data = {
        "publisher_id": VALID_USER_ID,
        "subscriber_id": VALID_USER_ID
    }

    response = requests.post(f"{BASE_URL}/publisher_reviews", headers=HEADERS, json=data)
    try:
        print(response.json())
    except Exception:
        print(response.status_code, response.text)
    assert response.status_code == 200


def test_get_all_reviews():
    data = {
        "subscriber_id": VALID_USER_ID,
    }

    response = requests.post(f"{BASE_URL}/all_reviews", headers=HEADERS, json=data)
    try:
        print(response.json())
    except Exception:
        print(response.status_code, response.text)

    assert response.status_code == 200


def test_invalid_subscribe():
    data = {
        "subscriber_id": VALID_USER_ID,
        "publisher_id": INVALID_USER_ID
    }

    response = requests.post(BASE_URL, headers=HEADERS, json=data)
    print(response.json())
    assert response.status_code == 400


def test_invalid_unsubscribe():
    data = {
        "subscriber_id": VALID_USER_ID,
        "publisher_id": INVALID_USER_ID
    }

    response = requests.delete(BASE_URL, headers=HEADERS, json=data)
    print(response.json())
    assert response.status_code == 400


def test_invalid_publisher_reviews():
    data = {
        "subscriber_id": INVALID_USER_ID,
        "publisher_id": INVALID_USER_ID
    }

    response = requests.post(f"{BASE_URL}/publisher_reviews", headers=HEADERS, json=data)
    print(response.json())
    assert response.status_code == 400


def test_invalid_all_reviews():
    data = {
        "subscriber_id": INVALID_USER_ID,
    }

    response = requests.post(f"{BASE_URL}/all_reviews", headers=HEADERS, json=data)
    try:
        print(response.json())
    except Exception:
        print(response.status_code, response.text)
    assert response.status_code == 404


def test_get_subscriptions_request():
    data = {
        "user_id": VALID_USER_ID,
    }
    response = requests.post(f"{BASE_URL}/all_subscriptions", headers=HEADERS, json=data)
    try:
        print(response.json())
    except Exception:
        print(response.status_code, response.text)
    assert response.status_code == 200


def test_get_subscriptions_invalid_request():
    data = {
        "user_id": INVALID_USER_ID,
    }
    response = requests.post(f"{BASE_URL}/all_subscriptions", headers=HEADERS, json=data)
    try:
        print(response.json())
    except Exception:
        print(response.status_code, response.text)
    assert response.status_code == 404
