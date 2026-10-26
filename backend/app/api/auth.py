from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.config import get_settings
from app.core.errors import ApplicationError
from app.core.security import (
    create_session_token,
    hash_password,
    hash_session_token,
    verify_password,
)
from app.db.session import get_db
from app.models import AuthSession, User
from app.models.mixins import utc_now
from app.schemas.auth import (
    AuthResponse,
    LoginRequest,
    MessageResponse,
    RegisterRequest,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])
DatabaseSession = Annotated[Session, Depends(get_db)]
CurrentUser = Annotated[User, Depends(get_current_user)]


def set_session_cookie(response: Response, token: str) -> None:
    settings = get_settings()
    response.set_cookie(
        key=settings.session_cookie_name,
        value=token,
        max_age=settings.session_max_age_seconds,
        httponly=True,
        secure=settings.session_cookie_secure,
        samesite="lax",
        path="/",
    )


def create_auth_session(db: Session, user_id: int) -> str:
    settings = get_settings()
    token = create_session_token()
    db.add(
        AuthSession(
            user_id=user_id,
            token_hash=hash_session_token(token),
            expires_at=utc_now() + timedelta(seconds=settings.session_max_age_seconds),
        )
    )
    return token


@router.post(
    "/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED
)
def register(
    payload: RegisterRequest,
    response: Response,
    db: DatabaseSession,
) -> AuthResponse:
    email = str(payload.email).strip().lower()
    if db.scalar(select(User).where(User.email == email)) is not None:
        raise ApplicationError("이미 가입된 이메일입니다.", status.HTTP_409_CONFLICT)

    user = User(email=email, password_hash=hash_password(payload.password))
    db.add(user)
    try:
        db.flush()
        token = create_auth_session(db, user.id)
        db.commit()
    except IntegrityError as error:
        db.rollback()
        raise ApplicationError(
            "이미 가입된 이메일입니다.", status.HTTP_409_CONFLICT
        ) from error

    db.refresh(user)
    set_session_cookie(response, token)
    return AuthResponse(
        message="회원 가입이 완료되었습니다.", user=UserResponse.model_validate(user)
    )


@router.post("/login", response_model=AuthResponse)
def login(
    payload: LoginRequest,
    response: Response,
    db: DatabaseSession,
) -> AuthResponse:
    email = str(payload.email).strip().lower()
    user = db.scalar(select(User).where(User.email == email))
    if user is None or not verify_password(payload.password, user.password_hash):
        raise ApplicationError(
            "이메일 또는 비밀번호를 확인해주세요.",
            status.HTTP_401_UNAUTHORIZED,
        )

    token = create_auth_session(db, user.id)
    db.commit()
    set_session_cookie(response, token)
    return AuthResponse(
        message="로그인했습니다.", user=UserResponse.model_validate(user)
    )


@router.post("/logout", response_model=MessageResponse)
def logout(
    request: Request,
    response: Response,
    db: DatabaseSession,
) -> MessageResponse:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if token:
        auth_session = db.scalar(
            select(AuthSession).where(
                AuthSession.token_hash == hash_session_token(token)
            )
        )
        if auth_session is not None:
            db.delete(auth_session)
            db.commit()

    response.delete_cookie(key=settings.session_cookie_name, path="/")
    return MessageResponse(message="로그아웃했습니다.")


@router.get("/me", response_model=UserResponse)
def get_me(current_user: CurrentUser) -> UserResponse:
    return UserResponse.model_validate(current_user)
