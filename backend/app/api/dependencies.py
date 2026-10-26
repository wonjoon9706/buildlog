from typing import Annotated

from fastapi import Depends, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.errors import ApplicationError
from app.core.security import hash_session_token
from app.db.session import get_db
from app.models import AuthSession, User
from app.models.mixins import utc_now


def get_current_user(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
) -> User:
    settings = get_settings()
    token = request.cookies.get(settings.session_cookie_name)
    if not token:
        raise ApplicationError("로그인이 필요합니다.", status.HTTP_401_UNAUTHORIZED)

    auth_session = db.scalar(
        select(AuthSession).where(AuthSession.token_hash == hash_session_token(token))
    )
    if auth_session is None:
        raise ApplicationError("로그인이 필요합니다.", status.HTTP_401_UNAUTHORIZED)

    if auth_session.expires_at <= utc_now():
        db.delete(auth_session)
        db.commit()
        raise ApplicationError(
            "로그인 시간이 만료되었습니다.", status.HTTP_401_UNAUTHORIZED
        )

    user = db.get(User, auth_session.user_id)
    if user is None:
        db.delete(auth_session)
        db.commit()
        raise ApplicationError("로그인이 필요합니다.", status.HTTP_401_UNAUTHORIZED)

    return user
