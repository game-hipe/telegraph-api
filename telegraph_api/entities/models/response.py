from typing import Generic, TypeVar

from pydantic import BaseModel, Field

_T = TypeVar("_T", bound=BaseModel)


class Response(BaseModel, Generic[_T]):
    ok: bool
    error: str | None = Field(default=None, description="Сообщение об ошибке")
    result: _T | None = Field(default=None, description="Результат запроса")
