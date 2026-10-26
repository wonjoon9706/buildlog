from datetime import date

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.models import ErrorLog, StudyLog, Todo, User


def test_record_models_are_connected_to_user(db_session) -> None:
    user = User(email="owner@example.com", password_hash="hashed-password")
    db_session.add(user)
    db_session.flush()

    db_session.add_all(
        [
            StudyLog(
                user_id=user.id,
                title="FastAPI 공부",
                content="라우터 구조를 정리했다.",
                studied_on=date(2026, 10, 26),
                tags=["fastapi"],
            ),
            Todo(user_id=user.id, content="로그인 화면 만들기"),
            ErrorLog(
                user_id=user.id,
                title="연결 오류",
                error_message="connection failed",
                context="로컬 테스트",
                tags=[],
            ),
        ]
    )
    db_session.commit()

    assert db_session.scalars(select(StudyLog)).one().user_id == user.id
    assert db_session.scalars(select(Todo)).one().due_date is None
    assert db_session.scalars(select(ErrorLog)).one().solution is None


def test_user_email_is_unique(db_session) -> None:
    db_session.add(User(email="same@example.com", password_hash="first-hash"))
    db_session.commit()
    db_session.add(User(email="same@example.com", password_hash="second-hash"))

    with pytest.raises(IntegrityError):
        db_session.commit()


def test_record_requires_existing_owner(db_session) -> None:
    db_session.add(Todo(user_id=999, content="존재하지 않는 사용자의 할 일"))

    with pytest.raises(IntegrityError):
        db_session.commit()
