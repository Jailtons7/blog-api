from typing import List, Dict, cast

import pytest

from src.blog.models import Post, Comment
from src.authentication.models import User
from tests.conftest import override_get_db


@pytest.fixture(scope="module")
def test_users() -> List[Dict[str, str]]:
    """
    creates two test users
    :return: list of dict with test users credentials
    """
    password1 = "password1"
    password2 = "password2"
    user1 = User(name="test1", username="test1", email="test1@example.com")
    user2 = User(name="test2", username="test2", email="test2@example.com")
    user1.set_password(password=password1)
    user2.set_password(password=password2)
    for db in override_get_db():
        db.add(user1)
        db.add(user2)
        db.commit()
        db.refresh(user1)
        db.refresh(user2)
    return [{"username": user1.email, "password": password1}, {"username": user2.email, "password": password2}]


@pytest.fixture(scope="module")
def access_token(client, test_users):
    response = client.post("/auth/access-token", data=test_users[0])
    assert response.status_code == 201
    token = response.json()["access_token"]
    assert token is not None
    return token


def test_not_authenticated(client):
    """
    given an unauthenticated client
    when it tries to access some protected endpoint
    then the api should respond with a 401, not authenticated
    """
    protected_endpoints = [
        ("post", "/posts/"),
        ("delete", "/posts/1"),
        ("put", "/posts/1"),
        ("post", "/comments/1"),
        ("get", "/comments/1"),
        ("delete", "/comments/1"),
    ]
    for method, endpoint in protected_endpoints:
        response = getattr(client, method)(endpoint)
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_add_posts(client, access_token):
    """
    given an authenticated user
    when it makes post requests to /posts
    then it should create a post in database
    """
    post_data = {
        "title": "test title",
        "body": "test body"
    }
    response = client.post(url="/posts", json=post_data, headers={"Authorization": f"Bearer {access_token}"})
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "test title"
    assert data["body"] == "test body"
    for db in override_get_db():
        assert db.query(Post).count() == 1


def test_get_post(client):
    """
    given a user
    when it makes a get requests in some specific post
    then the api should respond with a 200 response and posts info
    """
    user_data = {
        "name": "test",
        "username": "test",
        "email": "test@example.com"
    }
    post_data = {
        "title": "test title",
        "body": "test body"
    }
    for db in override_get_db():
        user = User(**user_data)
        user.set_password("pass")
        db.add(user)
        db.commit()
        db.refresh(user)
        post_data["creator"] = user
        post = Post(**post_data)
        db.add(post)
        db.commit()
        db.refresh(post)
        post_id = post.id
        response = client.get(url=f"/posts/{post_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == post_data["title"]
        assert data["body"] == post_data["body"]


def test_delete_posts(client, access_token):
    """
    given an authenticated user
    when it creates a post
    then it must be able to delete it
    """
    post = {"title": "test title", "body": "test body"}
    response = client.post("/posts", json=post, headers={"Authorization": f"Bearer {access_token}"})
    post_id = response.json()["id"]
    response = client.delete(url="/posts/{}".format(post_id), headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204
    for db in override_get_db():
        assert db.query(Post).filter(cast("ColumnElement[bool]", Post.id == post_id)).count() == 0


def test_post_not_found(client, access_token):
    """
    given an authenticated user
    when it tries to get a nonexistent post
    then the system must return a not found message
    """
    response = client.delete(url="/posts/{}".format(10000), headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Post not found"


def test_update_post(client, access_token):
    """
    given an authenticated user
    when it creates a post
    then it must be able to update it
    """
    post = {"title": "test title", "body": "test body"}
    response = client.post("/posts", json=post, headers={"Authorization": f"Bearer {access_token}"})
    post_id = response.json()["id"]
    update_ = {"title": "updated title", "body": "updated body"}
    response = client.put(f"/posts/{post_id}", json=update_, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["title"] == update_["title"]
    assert response.json()["body"] == update_["body"]


def test_add_comment(client, access_token):
    """
    Given an authenticated user
    When it makes a post requests to /comments/{post_id}
    Then it must be able to add a comment to that post
    """
    post = {"title": "test title", "body": "test body"}
    response = client.post("/posts", json=post, headers={"Authorization": f"Bearer {access_token}"})
    post_id = response.json()["id"]
    comment = {"body": "Test comment!"}
    response = client.post(f"/comments/{post_id}", json=comment, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 201
    assert response.json()["body"] == "Test comment!"


def test_list_comments(client, access_token):
    """
    Given an authenticated user
    When it makes a post requests to /comments/{post_id}
    Then it must be able to add a comment to that post
    """
    post_data = {"title": "test title", "body": "test body", "user_id": 1}
    db = next(override_get_db())
    post1 = Post(**post_data)
    post2 = Post(**post_data)
    db.add(post1)
    db.add(post2)
    db.commit()
    db.refresh(post1)
    db.refresh(post2)
    comments_data = [
        {"body": "Test comment 1!", "user_id": 1, "post_id": post1.id},
        {"body": "Test comment 2!", "user_id": 1, "post_id": post1.id},
        {"body": "Test comment 3!", "user_id": 1, "post_id": post2.id},  # this comment was created on post 2
        {"body": "Test comment 4!", "user_id": 1, "post_id": post2.id}  # this comment was created on post 2
    ]
    for comment in comments_data:
        comm = Comment(**comment)
        db.add(comm)
        db.commit()
        db.refresh(comm)

    # getting comments of the post 1
    response = client.get(f"/comments/{post1.id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for index, comment in enumerate(iterable=data, start=1):
        assert comment["body"] == f"Test comment {index}!"


def test_delete_comment(client, access_token):
    """
    Given an authenticated user
    When it makes a delete request /comments/{post_id}
    Then it must be able to delete it
    """
    post_data = {"title": "test title", "body": "test body", "user_id": 1}
    db = next(override_get_db())
    post = Post(**post_data)
    db.add(post)
    db.commit()
    db.refresh(post)
    comment_data = {"body": "Test comment!", "user_id": 1, "post_id": post.id}
    comment = Comment(**comment_data)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    response = client.delete(f"/comments/{comment.id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 204
    assert db.query(Comment).filter(cast("ColumnElement[bool]", Comment.id == comment.id)).all() == []
