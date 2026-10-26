from fastapi import status

from app.core.errors import ApplicationError


def ensure_owner(resource_user_id: int, current_user_id: int) -> None:
    if resource_user_id != current_user_id:
        raise ApplicationError(
            "이 기록에 접근할 수 없습니다.", status.HTTP_403_FORBIDDEN
        )
