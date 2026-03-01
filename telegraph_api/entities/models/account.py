from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator


class Account(BaseModel):
    """
    Объект, представляющий аккаунт Telegraph.
    """

    short_name: Optional[str] = Field(
        None,
        description="Имя аккаунта, отображается пользователю над кнопкой «Редактировать/Опубликовать».",
    )
    author_name: Optional[str] = Field(
        None,
        description="Имя автора по умолчанию, используемое при создании новых статей.",
    )
    author_url: Optional[HttpUrl] = Field(
        None,
        description="Ссылка профиля автора, открывается при клике на имя автора под заголовком.",
    )
    access_token: Optional[str] = Field(
        None,
        description="Токен доступа аккаунта. Возвращается только методами createAccount и revokeAccessToken.",
    )
    auth_url: Optional[HttpUrl] = Field(
        None,
        description="URL для авторизации браузера на telegra.ph и привязки к аккаунту. Действителен 5 минут, одноразовый.",
    )
    page_count: Optional[int] = Field(
        None, description="Количество страниц, принадлежащих аккаунту."
    )

    @field_validator("short_name")
    def validate_short_name(cls, v: str) -> Optional[str]:
        if v is None:
            return v
        if not (1 <= len(v) <= 32):
            raise ValueError("Длина short_name должна быть от 1 до 32 символов.")
        return v

    @field_validator("author_name")
    def validate_author_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not (0 <= len(v) <= 128):
            raise ValueError("Длина author_name должна быть от 0 до 128 символов.")
        return v

    @field_validator("author_url", mode="before")
    def validate_author_url(cls, v: Optional[HttpUrl]) -> Optional[HttpUrl]:
        if len(str(v)) == 0:
            return None
        if v is not None and not (0 <= len(str(v)) <= 512):
            raise ValueError("Длина author_url должна быть от 0 до 512 символов.")
        return v
