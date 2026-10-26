from datetime import timedelta

from sqlalchemy import select

from app.models import AuthSession, User
from app.models.mixins import utc_now

REGISTER_PAYLOAD = {
    "email": "student@example.com",
    "password": "safe-password",
}


def test_register_creates_user_and_logs_in(client, db_session) -> None:
    response = client.post("/api/auth/register", json=REGISTER_PAYLOAD)

    assert response.status_code == 201
    assert response.json()["user"]["email"] == REGISTER_PAYLOAD["email"]
    assert "buildlog_session" in response.cookies
    assert "Max-Age=604800" in response.headers["set-cookie"]
    assert "HttpOnly" in response.headers["set-cookie"]
    assert client.get("/api/auth/me").status_code == 200

    user = db_session.scalar(
        select(User).where(User.email == REGISTER_PAYLOAD["email"])
    )
    assert user is not None
    assert user.password_hash != REGISTER_PAYLOAD["password"]
    assert REGISTER_PAYLOAD["password"] not in user.password_hash


def test_register_rejects_duplicate_email(client) -> None:
    first_response = client.post("/api/auth/register", json=REGISTER_PAYLOAD)
    duplicate_response = client.post("/api/auth/register", json=REGISTER_PAYLOAD)

    assert first_response.status_code == 201
    assert duplicate_response.status_code == 409
    assert duplicate_response.json()["detail"] == "이미 가입된 이메일입니다."


def test_register_validates_email_and_password(client) -> None:
    invalid_email = client.post(
        "/api/auth/register",
        json={"email": "not-an-email", "password": "safe-password"},
    )
    short_password = client.post(
        "/api/auth/register",
        json={"email": "student@example.com", "password": "short"},
    )

    assert invalid_email.status_code == 422
    assert short_password.status_code == 422


def test_login_and_logout(client) -> None:
    client.post("/api/auth/register", json=REGISTER_PAYLOAD)
    client.post("/api/auth/logout")

    login_response = client.post("/api/auth/login", json=REGISTER_PAYLOAD)
    assert login_response.status_code == 200
    assert client.get("/api/auth/me").status_code == 200

    logout_response = client.post("/api/auth/logout")
    assert logout_response.status_code == 200
    assert client.get("/api/auth/me").status_code == 401


def test_login_rejects_wrong_password(client) -> None:
    client.post("/api/auth/register", json=REGISTER_PAYLOAD)
    client.post("/api/auth/logout")

    response = client.post(
        "/api/auth/login",
        json={"email": REGISTER_PAYLOAD["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "이메일 또는 비밀번호를 확인해주세요."


def test_me_requires_login(client) -> None:
    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "로그인이 필요합니다."


def test_expired_session_is_rejected(client, db_session) -> None:
    client.post("/api/auth/register", json=REGISTER_PAYLOAD)
    auth_session = db_session.scalar(select(AuthSession))
    auth_session.expires_at = utc_now() - timedelta(seconds=1)
    db_session.commit()

    response = client.get("/api/auth/me")

    assert response.status_code == 401
    assert response.json()["detail"] == "로그인 시간이 만료되었습니다."
