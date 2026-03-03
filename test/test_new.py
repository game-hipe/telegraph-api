import os
import sys
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import httpx
import pytest
from pydantic import ValidationError

# Моки для HTTP-запросов
try:
    import pytest_httpx
except ImportError:
    pytest_httpx = None

from telegraph_api.client._client import BaseTelegraph
from telegraph_api.entities.create.account import (
    CreateAccount,
)
from telegraph_api.entities.create.page import (
    CreatePage,
    EditPage,
    GetViews,
)
from telegraph_api.entities.models import (
    NodeElement,
)

# ----------------------------------------------------------------------
# NEW TESTS: Фикстуры для мокирования httpx
# ----------------------------------------------------------------------


@pytest.fixture
def mock_httpx_client(monkeypatch):
    """Создаёт мок для синхронного httpx.Client."""
    mock_client = MagicMock(spec=httpx.Client)
    mock_response = MagicMock(spec=httpx.Response)
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"ok": True, "result": {}}
    mock_client.request.return_value = mock_response
    monkeypatch.setattr(httpx, "Client", lambda *args, **kwargs: mock_client)
    return mock_client


@pytest.fixture
def mock_async_httpx_client(monkeypatch):
    """Создаёт мок для асинхронного httpx.AsyncClient."""
    mock_client = AsyncMock(spec=httpx.AsyncClient)
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"ok": True, "result": {}}
    mock_client.request.return_value = mock_response
    monkeypatch.setattr(httpx, "AsyncClient", lambda *args, **kwargs: mock_client)
    return mock_client


@pytest.fixture
def mock_response_factory():
    """Фабрика для создания мок-ответов с заданными данными."""

    def _create_response(
        ok: bool = True, result: Dict[str, Any] = None, error: str = None
    ):
        mock = MagicMock(spec=httpx.Response)
        mock.raise_for_status = MagicMock()
        data = {"ok": ok}
        if result is not None:
            data["result"] = result
        if error is not None:
            data["error"] = error
        mock.json.return_value = data
        return mock

    return _create_response


# ----------------------------------------------------------------------
# NEW TESTS: Тесты валидации Pydantic моделей
# ----------------------------------------------------------------------


class TestModelValidation:
    """Тесты для проверки валидации входных моделей (Pydantic)."""

    @pytest.mark.parametrize(
        "short_name,expected",
        [
            ("a", "a"),  # минимальная длина
            ("x" * 32, "x" * 32),  # максимальная длина
        ],
    )
    def test_create_account_valid_short_name(self, short_name, expected):
        account = CreateAccount(short_name=short_name)
        assert account.short_name == expected

    @pytest.mark.parametrize(
        "short_name",
        [
            "",  # пустая строка
            "x" * 33,  # слишком длинная
        ],
    )
    def test_create_account_invalid_short_name(self, short_name):
        with pytest.raises(ValidationError):
            CreateAccount(short_name=short_name)

    @pytest.mark.parametrize(
        "author_name",
        [
            None,
            "",
            "a" * 128,
        ],
    )
    def test_create_account_valid_author_name(self, author_name):
        account = CreateAccount(short_name="name", author_name=author_name)
        assert account.author_name == author_name

    def test_create_account_invalid_author_name_length(self):
        with pytest.raises(ValidationError):
            CreateAccount(short_name="name", author_name="a" * 129)

    @pytest.mark.parametrize(
        "author_url",
        [
            None,
            "https://example.com/",
            "http://localhost/",
        ],
    )
    def test_create_account_valid_author_url(self, author_url):
        account = CreateAccount(short_name="name", author_url=author_url)
        assert str(account.author_url) == author_url if author_url else True

    def test_create_account_invalid_author_url(self):
        with pytest.raises(ValidationError):
            CreateAccount(short_name="name", author_url="not a url")

    def test_create_page_missing_content_and_html(self):
        with pytest.raises(ValidationError, match="content | html"):
            CreatePage(access_token="token", title="Title")

    def test_create_page_with_html_only(self):
        page = CreatePage(access_token="token", title="Title", html="<p>Hi</p>")
        assert page.html == "<p>Hi</p>"
        assert page.content is None

    def test_create_page_with_content_only(self):
        content = [NodeElement(tag="p", children=["Hi"])]
        page = CreatePage(access_token="token", title="Title", content=content)
        assert page.content == content
        assert page.html is None

    def test_create_page_content_too_large(self):
        # Генерируем контент, который в JSON превысит 64KB
        long_text = "a" * 70000
        content = [NodeElement(tag="p", children=[long_text])]
        with pytest.raises(ValidationError, match="64 КБ"):
            CreatePage(access_token="token", title="Title", content=content)

    def test_edit_page_missing_content_and_html(self):
        with pytest.raises(ValidationError, match="content | html"):
            EditPage(access_token="token", path="path", title="Title")

    def test_get_views_dependencies(self):
        # Передан month без year
        with pytest.raises(ValidationError):
            GetViews(path="path", month=1)
        # Передан day без month
        with pytest.raises(ValidationError):
            GetViews(path="path", day=1, year=2023)
        # Передан hour без day
        with pytest.raises(ValidationError):
            GetViews(path="path", hour=1, year=2023, month=1)
        # Передан hour без year и month
        with pytest.raises(ValidationError):
            GetViews(path="path", hour=1, day=1)

    def test_get_views_valid_with_all(self):
        views = GetViews(path="path", year=2023, month=12, day=31, hour=23)
        assert views.year == 2023

    @pytest.mark.parametrize(
        "field,value",
        [
            ("year", 1999),
            ("year", 2101),
            ("month", 0),
            ("month", 13),
            ("day", 0),
            ("day", 32),
            ("hour", -1),
            ("hour", 25),
        ],
    )
    def test_get_views_out_of_range(self, field, value):
        kwargs = {"path": "path", field: value}
        if field == "month" and "year" not in kwargs:
            kwargs["year"] = 2023  # чтобы не было ошибки зависимости
        with pytest.raises(ValidationError):
            GetViews(**kwargs)


# ----------------------------------------------------------------------
# NEW TESTS: Тесты преобразования HTML в узлы
# ----------------------------------------------------------------------


class TestHtmlToNodes:
    """Тестирование метода _create_nodes, преобразующего HTML в список NodeElement."""

    @pytest.fixture
    def base_telegraph(self):
        return BaseTelegraph()

    def test_empty_html(self, base_telegraph):
        nodes = base_telegraph._create_nodes("")
        assert nodes == []

    def test_simple_text(self, base_telegraph):
        nodes = base_telegraph._create_nodes("Hello")
        # BeautifulSoup оборачивает строку в [<string>], но _create_nodes возвращает строку напрямую?
        # Проверим по коду: если child.name is None, добавляем str(child.string). Значит, для простого текста должен вернуться список с одной строкой.
        assert nodes == ["Hello"]

    def test_single_tag_with_text(self, base_telegraph):
        html = "<p>Hello</p>"
        nodes = base_telegraph._create_nodes(html)
        assert len(nodes) == 1
        node = nodes[0]
        assert isinstance(node, NodeElement)
        assert node.tag == "p"
        assert node.children == ["Hello"]
        assert node.attrs == {}

    def test_tag_with_attributes(self, base_telegraph):
        html = '<a href="https://example.com">Link</a>'
        nodes = base_telegraph._create_nodes(html)
        assert len(nodes) == 1
        node = nodes[0]
        assert node.tag == "a"
        assert node.attrs == {"href": "https://example.com"}
        assert node.children == ["Link"]

    def test_nested_tags(self, base_telegraph):
        html = "<p>Text</p>"
        nodes = base_telegraph._create_nodes(html)
        p = nodes[0]
        assert isinstance(p, NodeElement)
        assert p.tag == "p"
        assert p.children == ["Text"]

    def test_mixed_content(self, base_telegraph):
        html = "<p>Hello <b>world</b>!</p>"
        nodes = base_telegraph._create_nodes(html)
        p = nodes[0]
        assert p.tag == "p"
        assert len(p.children) == 3
        assert p.children[0] == "Hello "
        assert p.children[1].tag == "b"
        assert p.children[1].children == ["world"]
        assert p.children[2] == "!"

    def test_unsupported_tag(self, base_telegraph):
        # Тег, не разрешённый в NodeElement (проверка валидации в NodeElement, но _create_nodes не валидирует, только создаёт)
        with pytest.raises(ValidationError):
            html = "<script>alert(1)</script>"
            nodes = base_telegraph._create_nodes(html)
            assert len(nodes) == 1
            node = nodes[0]
            assert node.tag == "script"
        # При создании Page этот узел будет передан в API, но валидация NodeElement может не сработать,
        # если мы не вызываем её явно. В реальном коде при создании Page через клиент будет вызвана валидация модели.
        # Добавим проверку, что при попытке создать NodeElement с недопустимым тегом возникнет ошибка.
        with pytest.raises(ValidationError):
            NodeElement(tag="script", children=[])
