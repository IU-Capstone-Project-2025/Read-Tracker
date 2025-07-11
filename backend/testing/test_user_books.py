import pytest
import requests
import os

PORT = 8000  # os.getenv("BACKEND_PORT")


def test_get_user_books():
    header = {
        "Content-Type": "application/json"
    }
    get_user_books_url = f"http://localhost:{PORT}/me/books"
    get_user_books_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",

    }
    response = requests.post(url=get_user_books_url, headers=header, json=get_user_books_data)
    assert response.status_code == 200


def test_add_user_book():
    header = {
        "Content-Type": "application/json"
    }
    get_books_url = f"http://localhost:{PORT}/books"
    book_id = requests.get(url=get_books_url, headers=header).json()["data"][0]["id"]

    add_user_book_url = f"http://localhost:{PORT}/me/books/{book_id}/new"
    add_user_book_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "status": "want to read"
    }
    add_user_book_response = requests.post(url=add_user_book_url, headers=header, json=add_user_book_data)
    assert add_user_book_response.status_code == 200


def test_get_user_book():
    header = {
        "Content-Type": "application/json"
    }
    get_user_books_url = f"http://localhost:{PORT}/me/books"
    get_user_books_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",

    }
    book_id = requests.post(url=get_user_books_url, headers=header, json=get_user_books_data).json()["data"][0]["id"]

    get_user_book_url = f"http://localhost:{PORT}/me/books/{book_id}"
    response = requests.post(url=get_user_book_url, headers=header, json=get_user_books_data)

    assert response.status_code == 200


def test_update_user_book():
    header = {
        "Content-Type": "application/json"
    }
    get_user_books_url = f"http://localhost:{PORT}/me/books"
    get_user_books_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",

    }
    book_id = requests.post(url=get_user_books_url, headers=header, json=get_user_books_data).json()["data"][0]["id"]

    put_user_book_url = f"http://localhost:{PORT}/me/books/{book_id}"
    put_user_book_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "status": "reading now"
    }
    response = requests.put(url=put_user_book_url, headers=header, json=put_user_book_data)
    updated_book_response = requests.post(url=get_user_books_url, headers=header, json=get_user_books_data)
    assert response.status_code == 200
    assert updated_book_response.status_code == 200
    assert updated_book_response.json()["data"][0]["status"] == "reading now"


def test_delete_user_book():
    header = {
        "Content-Type": "application/json"
    }
    get_user_books_url = f"http://localhost:{PORT}/me/books"
    get_user_books_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",

    }
    book_id = requests.post(url=get_user_books_url, headers=header, json=get_user_books_data).json()["data"][0]["id"]

    put_user_book_url = f"http://localhost:{PORT}/me/books/{book_id}"
    put_user_book_data = {
        "user_id": "00000000-0000-0000-0000-000000000001",
        "status": "reading now"
    }
    delete_response = requests.delete(url=put_user_book_url, headers=header, json=put_user_book_data)
    get_user_book_url = f"http://localhost:{PORT}/me/books/{book_id}"
    deleted_book_response = requests.post(url=get_user_book_url, headers=header, json=get_user_books_data)
    assert delete_response.status_code == 200
    assert deleted_book_response.status_code == 404
