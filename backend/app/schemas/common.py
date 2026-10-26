from typing import Annotated, Literal

from pydantic import BaseModel, Field, StringConstraints

Title = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=100),
]
LongContent = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=20_000),
]
Tag = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=1, max_length=20),
]
Tags = Annotated[list[Tag], Field(max_length=5)]


class PaginationParams(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: Literal[20] = 20
