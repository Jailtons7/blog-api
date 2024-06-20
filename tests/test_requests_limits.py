from src.constants import REQUESTS_LIMIT_GET_POSTS


def test_requests_limits_get_posts(client):
    for _ in range(5):
        resp = client.get("/posts")
        assert resp.status_code == 200
    resp = client.get("/posts")
    assert resp.status_code == 429
    seconds = REQUESTS_LIMIT_GET_POSTS.get('SECONDS')
    assert resp.headers["Retry-After"] == f"{seconds} seconds"


def test_requests_limits_get_post(client):
    for _ in range(5):
        resp = client.get("/posts/1")
        assert resp.status_code == 200
    resp = client.get("/posts/1")
    assert resp.status_code == 429
    seconds = REQUESTS_LIMIT_GET_POSTS.get('SECONDS')
    assert resp.headers["Retry-After"] == f"{seconds} seconds"
