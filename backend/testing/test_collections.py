import pytest
import requests
import os

PORT = 8000  # os.getenv("BACKEND_PORT")


def test_create_collection():
    url = f"http://localhost:{PORT}/me/collections"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "title": "Collection test",
        "description": "Test description",
        "is_private": True
    }

    response = requests.post(url, headers=header, json=data)
    assert response.status_code == 200


def test_get_collections():
    url = f"http://localhost:{PORT}/me/collections/all"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }

    response = requests.post(url, headers=header, json=data)
    assert response.status_code == 200


def test_get_collection():
    url = f"http://localhost:{PORT}/me/collections/all"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }

    response = requests.post(url, headers=header, json=data).json()["data"][0]["id"]

    url = f"http://localhost:{PORT}/me/collections/{response}"

    response = requests.get(url, headers=header)

    assert response.status_code == 200


def test_update_collection():
    url_all = f"http://localhost:{PORT}/me/collections/all"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }

    response = requests.post(url_all, headers=header, json=data).json()["data"][0]["id"]

    url = f"http://localhost:{PORT}/me/collections/{response}"
    data2 = {
        "title": "Collection 2 test",
        "description": "Test 2 description",
        "is_private": False
    }

    response1 = requests.put(url, headers=header, json=data2)

    url = f"http://localhost:{PORT}/me/collections/{response}"

    response2 = requests.get(url, headers=header)

    print(response1.json())
    print(response2.json())
    assert response1.status_code == 200
    assert response2.json()['data'][0]["title"] == "Collection 2 test"

"""
def test_add_book_to_collection():
    collection_url = f"http://localhost:{PORT}/me/collections/"
    header = {
        "Content-Type": "application/json"
    }
    data_collection = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }

    collection_id = requests.get(collection_url, headers=header, json=data_collection).json()["data"][0]["id"]

    books_url = f"http://localhost:{PORT}/books"
    book_id = requests.get(books_url, headers=header).json()["data"][0]["id"]

    url = f"http://localhost:{PORT}/me/collections/{collection_id}/books"
    data_for_adding_book = {
        "book_id": book_id
    }
    response_adding = requests.post(url, headers=header, json=data_for_adding_book)

    collection_response = requests.get(collection_url, headers=header, json=data_collection)
    assert response_adding.status_code == 200
    assert collection_response.json()['data'][0]['items'] != []


def test_delete_collection():
    url = f"http://localhost:{PORT}/me/collections/"
    header = {
        "Content-Type": "application/json"
    }
    data = {
        "user_id": "00000000-0000-0000-0000-000000000001"
    }

    response = requests.get(url, headers=header, json=data)

    url = f"http://localhost:{PORT}/me/collections/{response.json()['data'][0]['id']}"

    response1 = requests.delete(url, headers=header, json=data)

    url = f"http://localhost:{PORT}/me/collections/{response.json()['data'][0]['id']}"
    response2 = requests.get(url, headers=header)
    assert response1.status_code == 200
    assert response2.status_code == 404
"""