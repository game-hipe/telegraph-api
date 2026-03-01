from __future__ import annotations

import json

from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field, field_validator, model_validator

from ..models.node import Node


class CreatePage(BaseModel):
    """
    Модель для метода createPage – создание новой страницы Telegraph.

    Важно, один из атрибутов (content | html) должен будет быть заполнен, приоритет одаётся content если html заполнен
    """

    access_token: str = Field(..., description="Токен доступа к аккаунту Telegraph.")
    title: str = Field(
        ..., description="Заголовок страницы. Допустимая длина: от 1 до 256 символов."
    )
    author_name: Optional[str] = Field(
        None,
        description="Имя автора, отображаемое под заголовком. Длина: от 0 до 128 символов.",
    )
    author_url: Optional[HttpUrl] = Field(
        None,
        description="Ссылка на профиль автора. Может быть любой ссылкой. Длина: от 0 до 512 символов.",
    )
    content: Optional[List[Node]] = Field(
        None,
        description="Содержимое страницы в виде массива узлов DOM. Общий размер JSON не должен превышать 64 КБ.",
    )
    html: Optional[str] = Field(
        None,
        description="Содержимое страницы в виде HTML, который в дальнейшем будет обработан",
    )
    return_content: bool = Field(
        False,
        description="Если true, в ответе будет возвращено поле content объекта Page.",
    )

    @field_validator("title")
    def validate_title(cls, v: str) -> str:
        if not (1 <= len(v) <= 256):
            raise ValueError("Длина title должна быть от 1 до 256 символов.")
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

    @model_validator(mode="after")
    def validate_content_size(self) -> "CreatePage":
        """
        Проверяет, что размер контента не превышает 64 КБ.
        """
        if not self.content:
            return self
        content_json = json.dumps(
            [
                node.model_dump() if hasattr(node, "model_dump") else node
                for node in self.content
            ]
        )
        if len(content_json.encode("utf-8")) > 64 * 1024:
            raise ValueError("Общий размер content не должен превышать 64 КБ.")
        return self

    @model_validator(mode="after")
    def validate_content_html(self) -> "CreatePage":
        """
        Проверяет, что контент не пустой.
        """
        if self.content:
            return self

        elif self.html:
            return self

        else:
            raise ValueError("Ни один из атрибутов (content | html) не был определён")


class EditPage(BaseModel):
    """
    Модель для метода editPage – редактирование существующей страницы Telegraph.
    """

    access_token: str = Field(..., description="Токен доступа к аккаунту Telegraph.")
    path: str = Field(..., description="Путь к странице (часть URL после telegra.ph/).")
    title: str = Field(
        ..., description="Заголовок страницы. Допустимая длина: от 1 до 256 символов."
    )
    content: List[Node] = Field(
        None,
        description="Содержимое страницы в виде массива узлов DOM. Общий размер JSON не должен превышать 64 КБ.",
    )
    html: Optional[str] = Field(
        None,
        description="Содержимое страницы в виде HTML, который в дальнейшем будет обработан",
    )
    author_name: Optional[str] = Field(
        None,
        description="Имя автора, отображаемое под заголовком. Длина: от 0 до 128 символов.",
    )
    author_url: Optional[HttpUrl] = Field(
        None,
        description="Ссылка на профиль автора. Может быть любой ссылкой. Длина: от 0 до 512 символов.",
    )
    return_content: bool = Field(
        False,
        description="Если true, в ответе будет возвращено поле content объекта Page.",
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

    @model_validator(mode="after")
    def validate_content_size(self) -> "EditPage":
        if self.content is None:
            return self
        content_json = json.dumps(
            [
                node.model_dump() if hasattr(node, "model_dump") else node
                for node in self.content
            ]
        )
        if len(content_json.encode("utf-8")) > 64 * 1024:
            raise ValueError("Общий размер content не должен превышать 64 КБ.")
        return self

    @model_validator(mode="after")
    def validate_content_html(self) -> "EditPage":
        """
        Проверяет, что контент не пустой.
        """
        if self.content:
            return self

        elif self.html:
            return self

        else:
            raise ValueError("Ни один из атрибутов (content | html) не был определён")


class GetPage(BaseModel):
    """
    Модель для метода getPage – получение информации о странице Telegraph.
    """

    path: str = Field(..., description="Путь к странице (например, Sample-Page-12-15).")
    return_content: bool = Field(
        False, description="Если true, в ответе будет возвращено поле content."
    )

    @field_validator("path")
    def validate_path(cls, v: str) -> str:
        if not (1 <= len(v) <= 255):
            raise ValueError("Длина path должна быть от 1 до 255 символов.")
        return v


class GetPageList(BaseModel):
    """
    Модель для метода getPageList – получение списка страниц аккаунта.
    """

    access_token: str = Field(..., description="Токен доступа к аккаунту Telegraph.")
    offset: int = Field(
        0, description="Порядковый номер первой возвращаемой страницы (начиная с 0)."
    )
    limit: int = Field(
        50,
        description="Максимальное количество страниц для получения. Допустимые значения: от 0 до 200.",
    )

    @field_validator("offset")
    def validate_offset(cls, v: int) -> int:
        if v < 0:
            raise ValueError("offset должен быть неотрицательным.")
        return v

    @field_validator("limit")
    def validate_limit(cls, v: int) -> int:
        if not (0 <= v <= 200):
            raise ValueError("limit должен быть в диапазоне от 0 до 200.")
        return v


class GetViews(BaseModel):
    """
    Модель для метода getViews – получение статистики просмотров страницы.
    """

    path: str = Field(..., description="Путь к странице (например, Sample-Page-12-15).")
    year: Optional[int] = Field(
        None, description="Год (2000–2100). Обязателен, если передан month."
    )
    month: Optional[int] = Field(
        None, description="Месяц (1–12). Обязателен, если передан day."
    )
    day: Optional[int] = Field(
        None, description="День (1–31). Обязателен, если передан hour."
    )
    hour: Optional[int] = Field(
        None,
        description="Час (0–24). Если передан, также должны быть указаны year, month и day.",
    )

    @field_validator("path")
    def validate_path(cls, v: str) -> str:
        if not (1 <= len(v) <= 255):
            raise ValueError("Длина path должна быть от 1 до 255 символов.")
        return v

    @field_validator("year")
    def validate_year(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (2000 <= v <= 2100):
            raise ValueError("year должен быть в диапазоне 2000–2100.")
        return v

    @field_validator("month")
    def validate_month(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 12):
            raise ValueError("month должен быть в диапазоне 1–12.")
        return v

    @field_validator("day")
    def validate_day(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (1 <= v <= 31):
            raise ValueError("day должен быть в диапазоне 1–31.")
        return v

    @field_validator("hour")
    def validate_hour(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and not (0 <= v <= 24):
            raise ValueError("hour должен быть в диапазоне 0–24.")
        return v

    @model_validator(mode="after")
    def check_dependencies(self) -> "GetViews":
        """
        Проверяет взаимозависимости полей year, month, day, hour.
        """
        if self.month is not None and self.year is None:
            raise ValueError("Если передан month, необходимо указать year.")
        if self.day is not None and self.month is None:
            raise ValueError("Если передан day, необходимо указать month.")
        if self.hour is not None and self.day is None:
            raise ValueError("Если передан hour, необходимо указать day.")
        # Дополнительно: если передан hour, должны быть и year, и month (хотя они могут быть неявно заданы через day? лучше явно)
        if self.hour is not None and (self.year is None or self.month is None):
            raise ValueError("Если передан hour, необходимо указать year и month.")
        return self
