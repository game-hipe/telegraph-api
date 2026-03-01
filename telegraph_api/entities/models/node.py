from __future__ import annotations

from typing import Dict, List, Optional, Union

from pydantic import BaseModel, Field, field_validator


class NodeElement(BaseModel):
    """
    Объект, представляющий элемент DOM-узла.
    """

    tag: str = Field(..., description="Имя DOM-элемента.")
    attrs: Optional[Dict[str, str]] = Field(
        None,
        description="Атрибуты DOM-элемента. Ключ — имя атрибута, значение — значение атрибута.",
    )
    children: Optional[List["Node"]] = Field(
        None, description="Список дочерних узлов DOM-элемента."
    )

    @field_validator("tag")
    def validate_tag(cls, v: str) -> str:
        allowed_tags = {
            "a",
            "aside",
            "b",
            "blockquote",
            "br",
            "code",
            "em",
            "figcaption",
            "figure",
            "h3",
            "h4",
            "hr",
            "i",
            "iframe",
            "img",
            "li",
            "ol",
            "p",
            "pre",
            "s",
            "strong",
            "u",
            "ul",
            "video",
        }
        if v not in allowed_tags:
            raise ValueError(
                f"Тег должен быть одним из: {', '.join(sorted(allowed_tags))}"
            )
        return v

    @field_validator("attrs")
    def validate_attrs(cls, v: Optional[Dict[str, str]]) -> Optional[Dict[str, str]]:
        if v is not None:
            allowed_attrs = {"href", "src"}
            for key in v.keys():
                if key not in allowed_attrs:
                    raise ValueError(
                        f"Атрибут должен быть одним из: {', '.join(sorted(allowed_attrs))}"
                    )
        return v


# Node может быть либо строкой (текстовый узел), либо объектом NodeElement.
Node = Union[str, NodeElement]


# Для корректной работы с рекурсивными ссылками обновляем model_config у NodeElement
NodeElement.model_config = {
    "arbitrary_types_allowed": True,  # разрешаем Union типы
}
