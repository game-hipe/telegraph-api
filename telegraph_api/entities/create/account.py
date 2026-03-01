from typing import Literal, Optional, TypeAlias

from pydantic import BaseModel, Field, HttpUrl, field_validator

SUPPORTED_FIELDS: TypeAlias = Literal[
    "short_name", "author_name", "author_url", "auth_url", "page_count"
]


class CreateAccount(BaseModel):
    """
    Модель для метода createAccount – создание нового аккаунта Telegraph.
    """

    short_name: str = Field(
        ...,
        description="Имя аккаунта, отображается пользователю над кнопкой «Редактировать/Опубликовать». Длина: от 1 до 32 символов.",
    )
    author_name: Optional[str] = Field(
        None,
        description="Имя автора по умолчанию, используемое при создании новых статей. Длина: от 0 до 128 символов.",
    )
    author_url: Optional[HttpUrl] = Field(
        None,
        description="Ссылка на профиль автора по умолчанию. Может быть любой ссылкой. Длина: от 0 до 512 символов.",
    )

    @field_validator("short_name")
    def validate_short_name(cls, v: str) -> str:
        if not (1 <= len(v) <= 32):
            raise ValueError("Длина short_name должна быть от 1 до 32 символов.")
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


class EditAccount(BaseModel):
    """
    Модель для метода editAccountInfo – обновление информации об аккаунте Telegraph.
    """

    access_token: str = Field(..., description="Токен доступа к аккаунту Telegraph.")
    short_name: str = Field(
        ..., description="Новое имя аккаунта. Длина: от 1 до 32 символов."
    )
    author_name: Optional[str] = Field(
        None, description="Новое имя автора по умолчанию. Длина: от 0 до 128 символов."
    )
    author_url: Optional[HttpUrl] = Field(
        None,
        description="Новая ссылка на профиль автора по умолчанию. Длина: от 0 до 512 символов.",
    )

    @field_validator("access_token")
    def validate_access_token(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("access_token не может быть пустым.")
        return v

    @field_validator("short_name")
    def validate_short_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not (1 <= len(v) <= 32):
            raise ValueError("Длина short_name должна быть от 1 до 32 символов.")
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


class GetAccountInfo(BaseModel):
    """
    Модель для метода getAccountInfo – получение информации об аккаунте Telegraph.
    """

    access_token: str = Field(..., description="Токен доступа к аккаунту Telegraph.")
    fields: Optional[list[SUPPORTED_FIELDS]] = Field(
        None,
        description="Список полей аккаунта для возврата. Допустимые поля: short_name, author_name, author_url, auth_url, page_count. Если не указан, API вернёт поля по умолчанию.",
    )

    @field_validator("access_token")
    def validate_access_token(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("access_token не может быть пустым.")
        return v

    @field_validator("fields")
    def validate_fields(
        cls, v: Optional[list[SUPPORTED_FIELDS]]
    ) -> Optional[list[SUPPORTED_FIELDS]]:
        if v is not None:
            # Проверка, что список не пустой (опционально)
            if len(v) == 0:
                raise ValueError("Список fields не может быть пустым, если передан.")
            # Дубликаты не имеют смысла, но API их проигнорирует? Можно пропустить.
        return v


class RevokeAccessToken(BaseModel):
    """
    Модель для метода revokeAccessToken – аннулирование текущего токена доступа и создание нового.
    """

    access_token: str = Field(
        ...,
        description="Токен доступа к аккаунту Telegraph, который требуется заменить.",
    )

    @field_validator("access_token")
    def validate_access_token(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("access_token не может быть пустым.")
        return v
