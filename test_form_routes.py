from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app



client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to api"}


def test_create_forums():

    # Create a user first

    user = {
        "username": "test",
        "password": "test",
        "email": "wangtester@gmail.com"
    }

    response = client.post(
        "/users/",
        json=user
    )

    user = response.json()
    print(user)


    response = client.post(
        "/forum/",
        json={
            "title": "Test forum",
            "body": "Test body",
            "user_id": user.id,
            "tags": ["test", "forum"]
        }
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test forum"
    assert response.json()["body"] == "Test body"
    assert response.json()["user_id"] == 1
    assert response.json()["tags"] == ["test", "forum"]