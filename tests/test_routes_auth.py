def test_login_get(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Login" in response.data


def test_login_post_invalid(client):
    response = client.post(
        "/login",
        data={"username": "invalid", "password": "wrong"},
        follow_redirects=True,
    )

    assert b"Login failed" in response.data or b"Error" in response.data


def test_logout(client):
    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data
