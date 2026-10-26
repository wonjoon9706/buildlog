import pytest
from pydantic import BaseModel, ValidationError

from app.api.permissions import ensure_owner
from app.core.errors import ApplicationError
from app.schemas.common import LongContent, PaginationParams, Tags, Title


class ExampleRecord(BaseModel):
    title: Title
    content: LongContent
    tags: Tags


def test_common_record_rules_accept_valid_values() -> None:
    record = ExampleRecord(title="  제목  ", content="  내용  ", tags=["python"])

    assert record.title == "제목"
    assert record.content == "내용"


@pytest.mark.parametrize(
    "field,value",
    [
        ("title", "t" * 101),
        ("content", "c" * 20_001),
        ("tags", ["tag"] * 6),
        ("tags", ["t" * 21]),
    ],
)
def test_common_record_rules_reject_limits(field, value) -> None:
    payload = {"title": "제목", "content": "내용", "tags": []}
    payload[field] = value

    with pytest.raises(ValidationError):
        ExampleRecord.model_validate(payload)


def test_pagination_size_is_fixed_to_twenty() -> None:
    assert PaginationParams().page_size == 20

    with pytest.raises(ValidationError):
        PaginationParams(page_size=10)


def test_owner_permission_rejects_another_user() -> None:
    ensure_owner(resource_user_id=1, current_user_id=1)

    with pytest.raises(ApplicationError) as error:
        ensure_owner(resource_user_id=1, current_user_id=2)

    assert error.value.status_code == 403
