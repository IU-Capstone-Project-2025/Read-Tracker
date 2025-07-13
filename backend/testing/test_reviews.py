import pytest
import requests
import os

PORT = 8000  # os.getenv("BACKEND_PORT")


def test_get_all_reviews():
    header = {
        "Content-Type": "application/json"
    }

    create_user_1_json = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "rate": 8,
        "text": "SOme text by user 1"
    }
    create_user_2_json = {
        "user_id": '00000000-0000-0000-0000-000000000005',
        "rate": 3,
        "text": "Other hdhdhhdhd text by user 2"
    }
    delete_user_1_json = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }
    delete_user_2_json = {
        "user_id": "00000000-0000-0000-0000-000000000005"
    }
    book_id = "00000000-0000-0000-0000-000000000003"

    get_reviews_url = f"http://localhost:{PORT}/me/reviews/{book_id}/all_reviews"
    create_review_url = f"http://localhost:{PORT}/me/reviews/{book_id}/new"
    delete_review_url = f"http://localhost:{PORT}/me/reviews/{book_id}"

    user_1_creation = requests.post(create_review_url, headers=header, json=create_user_1_json)
    user_2_creation = requests.post(create_review_url, headers=header, json=create_user_2_json)
    get_reviews_response_before = requests.get(get_reviews_url, headers=header)
    print(user_1_creation.json())
    print(user_2_creation.json())
    print(get_reviews_response_before.json())
    assert user_1_creation.status_code == 200
    assert user_2_creation.status_code == 200
    assert get_reviews_response_before.status_code == 200
    assert len(get_reviews_response_before.json()["data"]) == 2
    user_1_rev_deletion = requests.delete(delete_review_url, headers=header, json=delete_user_1_json)
    user_2_rev_deletion = requests.delete(delete_review_url, headers=header, json=delete_user_2_json)
    get_reviews_response_after = requests.get(get_reviews_url, headers=header)
    print(get_reviews_response_after.json())
    assert user_1_rev_deletion.status_code == 200
    assert user_2_rev_deletion.status_code == 200
    assert get_reviews_response_after.status_code == 200
    assert len(get_reviews_response_after.json()["data"]) == 0