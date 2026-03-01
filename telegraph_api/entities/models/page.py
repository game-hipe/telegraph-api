from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator

from .node import Node


class PageList(BaseModel):
    """
    Объект, представляющий список статей Telegraph, принадлежащих аккаунту.
    """

    total_count: int = Field(
        ..., description="Общее количество страниц, принадлежащих целевому аккаунту."
    )
    pages: List["Page"] = Field(
        ..., description="Запрошенные страницы целевого аккаунта."
    )


class Page(BaseModel):
    """
    Объект, представляющий страницу на Telegraph.
    """

    path: str = Field(..., description="Путь к странице.")
    url: HttpUrl = Field(..., description="URL страницы.")
    title: str = Field(..., description="Заголовок страницы.")
    description: str = Field(..., description="Описание страницы.")
    author_name: Optional[str] = Field(
        None, description="Имя автора, отображаемое под заголовком."
    )
    author_url: Optional[HttpUrl] = Field(
        None,
        description="Ссылка профиля автора, открывается при клике на имя автора под заголовком.",
    )
    image_url: Optional[HttpUrl] = Field(None, description="URL изображения страницы.")
    content: Optional[List[Node]] = Field(
        None, description="Содержимое страницы в виде списка узлов DOM."
    )
    views: int = Field(..., description="Количество просмотров страницы.")
    can_edit: Optional[bool] = Field(
        None,
        description="True, если целевой аккаунт может редактировать страницу. Возвращается только при передаче access_token.",
    )

    @field_validator("path")
    def validate_path(cls, v: str) -> str:
        if not (1 <= len(v) <= 255):
            raise ValueError("Длина path должна быть от 1 до 255 символов.")
        return v

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if not (1 <= len(v) <= 256):
            raise ValueError("Длина title должна быть от 1 до 256 символов.")
        return v

    @field_validator("description")
    def validate_description(cls, v: str) -> str:
        if not (0 <= len(v) <= 256):
            raise ValueError("Длина description должна быть от 0 до 256 символов.")
        return v

    @field_validator("author_name")
    def validate_author_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not (0 <= len(v) <= 128):
            raise ValueError("Длина author_name должна быть от 0 до 128 символов.")
        return v

    @field_validator("author_url")
    def validate_author_url(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        if v is not None and not (0 <= len(str(v)) <= 512):
            raise ValueError("Длина author_url должна быть от 0 до 512 символов.")
        return v

    @field_validator("image_url")
    def validate_image_url(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        if v is not None and not (0 <= len(str(v)) <= 512):
            raise ValueError("Длина image_url должна быть от 0 до 512 символов.")
        return v


class PageViews(BaseModel):
    """
    Объект, представляющий количество просмотров страницы Telegraph.
    """

    views: int = Field(..., description="Количество просмотров целевой страницы.")
