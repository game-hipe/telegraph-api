import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import pytest
import pytest_asyncio
from httpx import AsyncClient
from pydantic import ValidationError

from telegraph_api.client._client import AsyncTelegraph, Telegraph
from telegraph_api.entities.models import NodeElement, Page
from telegraph_api.entities.work.account import AsyncAccount, SyncAccount
from telegraph_api.exc import TelegraphError


class BaseTest:
    def test_create_account(self, created_account):
        """Тест проверяет созданный аккаунт"""
        assert created_account.access_token is not None
        assert created_account.auth_url is not None
        assert created_account.short_name == "GH"
        assert created_account.author_name == "GameHipe"


class TestSync(BaseTest):
    @pytest.fixture
    def telegraph(self) -> Telegraph:
        return Telegraph()

    @pytest.fixture(scope="class")
    def created_account(self, telegraph_class):
        """Фикстура создает аккаунт и возвращает его для всех тестов класса"""
        account = telegraph_class.create_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe/telegraph-api",
        )
        return account

    @pytest.fixture(scope="class")
    def created_page(self, created_account):
        """Фикстура создает страницу и возвращает ее для всех тестов класса"""
        page = created_account.create_page(
            access_token=created_account.access_token,
            title="Test Page",
            author_name="GameHipe",
            content=[NodeElement(tag="p", children=["Hello, World!"])],
        )
        return page

    @pytest.fixture(scope="class")
    def telegraph_class(self) -> Telegraph:
        """Фикстура с областью class для использования в других class-фикстурах"""
        return Telegraph()

    def test_create_page(self, telegraph, created_page):
        """Тест использует аккаунт из фикстуры"""

        assert created_page.title == "Test Page"
        assert created_page.author_name == "GameHipe"

    def test_edit_account(self, telegraph, created_account):
        """Тест редактирует аккаунт"""
        edited_account = telegraph.edit_account(
            access_token=created_account.access_token,
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe",
        )
        assert edited_account.short_name == "GH"
        assert edited_account.author_name == "GameHipe"
        assert str(edited_account.author_url) == "https://github.com/game-hipe"

    def test_edit_page(
        self, telegraph: Telegraph, created_page: Page, created_account: SyncAccount
    ):
        page = telegraph.edit_page(
            access_token=created_account.access_token,
            path=created_page.path,
            title="Test Page 2",
            author_name="GameHipe",
            content=[NodeElement(tag="p", children=["Hello, World! Test 2"])],
            return_content=True,
        )

        assert page.title == "Test Page 2"
        assert page.author_name == "GameHipe"

        assert page.content[0].children[0] == "Hello, World! Test 2"

    def test_edit_without_access_token(self, telegraph: Telegraph, created_page: Page):
        with pytest.raises(ValidationError):
            telegraph.edit_page(
                path=created_page.path,
                title="Test Page 2",
                author_name="GameHipe",
                content=[NodeElement(tag="p", children=["Hello, World! Test 2"])],
                return_content=True,
            )

    def test_get_page(
        self, telegraph: Telegraph, created_page: Page, created_account: SyncAccount
    ):
        page = telegraph.get_page(
            access_token=created_account.access_token,
            path=created_page.path,
            return_content=True,
        )

        assert page.title == "Test Page 2"
        assert page.author_name == "GameHipe"

        assert page.content[0].children[0] == "Hello, World! Test 2"

    def test_get_views(
        self, telegraph: Telegraph, created_page: Page, created_account: SyncAccount
    ):
        views = telegraph.get_views(
            access_token=created_account.access_token,
            path=created_page.path,
            day=1,
            month=2,
            year=2026,
        )

    def test_get_views_error(
        self, telegraph: Telegraph, created_page: Page, created_account: SyncAccount
    ):
        with pytest.raises(TelegraphError):
            telegraph.get_views(
                access_token=created_account.access_token, path=created_page.path
            )

    def test_get_account_info(self, telegraph: Telegraph, created_account: SyncAccount):
        account = telegraph.get_account_info(access_token=created_account.access_token)

        assert account.short_name == "GH"
        assert account.author_name == "GameHipe"
        assert str(account.author_url) == "https://github.com/game-hipe"

    def test_get_account_info_error(self, telegraph: Telegraph):
        with pytest.raises(TelegraphError):
            telegraph.get_account_info(access_token="123")

    def test_get_page_list(self, telegraph: Telegraph, created_account: SyncAccount):
        # Создадим несколько страниц
        for i in range(3):
            created_account.create_page(
                title=f"Page {i}", content=[NodeElement(tag="p", children=["test"])]
            )
        page_list = telegraph.get_page_list(
            access_token=created_account.access_token, limit=2
        )
        assert page_list.total_count >= 3
        assert len(page_list.pages) == 2

    def test_create_page_with_html(
        self, telegraph: Telegraph, created_account: SyncAccount
    ):
        html_content = "<p>Hello from <b>HTML</b></p>"
        page = telegraph.create_page(
            access_token=created_account.access_token,
            title="HTML Page",
            html=html_content,
        )
        # Получим страницу с контентом и проверим структуру
        page_with_content = telegraph.get_page(path=page.path, return_content=True)
        assert page_with_content.content[0].tag == "p"
        assert page_with_content.content[0].children[0] == "Hello from "
        assert page_with_content.content[0].children[1].tag == "strong"
        assert page_with_content.content[0].children[1].children[0] == "HTML"

    def test_create_page_without_content_or_html(
        self, telegraph: Telegraph, created_account: SyncAccount
    ):
        with pytest.raises(ValidationError):
            telegraph.create_page(
                access_token=created_account.access_token, title="No content"
            )

    def test_get_views_with_date(
        self, telegraph: Telegraph, created_page: Page, created_account: SyncAccount
    ):
        # Запросим просмотры за текущую дату (может быть 0)
        views = telegraph.get_views(
            access_token=created_account.access_token,
            path=created_page.path,
            year=2026,
            month=3,
            day=3,
        )
        assert isinstance(views.views, int)

    def test_context_manager(self):
        with Telegraph() as t:
            account = t.create_account(short_name="Test")
            assert account.access_token is not None
        # Проверим, что клиент закрыт (можно через mock, но в реальности httpx.Client закроется)

    def test_revoke_access_token(
        self, telegraph: Telegraph, created_account: SyncAccount
    ):
        old_token = created_account.access_token
        new_account = telegraph.revoke_access_token(access_token=old_token)
        assert new_account.access_token != old_token
        # Проверим, что старый токен больше не работает
        with pytest.raises(TelegraphError):
            telegraph.get_account_info(access_token=old_token)


class TestAccountORM(BaseTest):
    @pytest.fixture
    def telegraph(self) -> Telegraph:
        return Telegraph()

    @pytest.fixture(scope="class")
    def created_account(self, telegraph_class):
        """Фикстура создает аккаунт и возвращает его для всех тестов класса"""
        account = telegraph_class.create_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe/telegraph-api",
        )
        return account

    @pytest.fixture(scope="class")
    def telegraph_class(self) -> Telegraph:
        """Фикстура с областью class для использования в других class-фикстурах"""
        return Telegraph()

    def test_create_page(self, created_account: SyncAccount):
        page = created_account.create_page(
            title="Test Page",
            author_name="GameHipe",
            content=[NodeElement(tag="p", children=["Hello, World!"])],
            return_content=True,
        )

        assert page.title == "Test Page"
        assert page.author_name == "GameHipe"

        assert page.content[0].children[0] == "Hello, World!"

    def test_edit_account(self, created_account: SyncAccount):
        edited_account = created_account.edit_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe",
        )

        assert edited_account.short_name == "GH"
        assert edited_account.author_name == "GameHipe"
        assert str(edited_account.author_url) == "https://github.com/game-hipe"

    def test_get_account(self, created_account: SyncAccount):
        account = created_account.get_account_info(
            fields=["short_name", "author_name", "author_url"]
        )

        assert account.short_name == "GH"
        assert account.author_name == "GameHipe"
        assert str(account.author_url) == "https://github.com/game-hipe"

    def test_get_page_list(self, created_account: SyncAccount):
        # Создадим несколько страниц
        for i in range(3):
            created_account.create_page(
                title=f"Page {i}", content=[NodeElement(tag="p", children=["test"])]
            )
        page_list = created_account.get_page_list(limit=2)
        assert page_list.total_count >= 3
        assert len(page_list.pages) == 2

    def test_revoke_access_token(self, created_account: SyncAccount):
        old_token = created_account.access_token
        new_account = created_account.revoke_access_token()
        assert new_account.access_token != old_token
        # Проверим, что старый токен больше не работает
        with pytest.raises(TelegraphError):
            created_account.get_account_info()

        account = new_account.get_account_info(
            fields=["short_name", "author_name", "author_url"]
        )

        assert account.access_token != new_account.access_token
        assert account.short_name == "GH"
        assert account.author_name == "GameHipe"
        assert str(account.author_url) == "https://github.com/game-hipe"

@pytest.mark.asyncio(loop_scope="class")
class TestAsyncClient:
    @pytest_asyncio.fixture
    def telegraph(self) -> AsyncTelegraph:
        return AsyncTelegraph()

    @pytest_asyncio.fixture(scope="class")
    async def created_account(self, telegraph_class):
        """Фикстура создает аккаунт и возвращает его для всех тестов класса"""
        account = await telegraph_class.create_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe/telegraph-api",
        )
        return account

    @pytest_asyncio.fixture(scope="class")
    async def created_page(self, created_account):
        """Фикстура создает страницу и возвращает ее для всех тестов класса"""
        page = await created_account.create_page(
            access_token=created_account.access_token,
            title="Test Page",
            author_name="GameHipe",
            content=[NodeElement(tag="p", children=["Hello, World!"])],
        )
        return page

    @pytest.fixture(scope="class")
    def telegraph_class(self) -> AsyncTelegraph:
        """Фикстура с областью class для использования в других class-фикстурах"""
        return AsyncTelegraph()

    def test_create_page(self, telegraph, created_page):
        """Тест использует аккаунт из фикстуры"""

        assert created_page.title == "Test Page"
        assert created_page.author_name == "GameHipe"

    @pytest.mark.asyncio
    async def test_edit_account(self, telegraph, created_account):
        """Тест редактирует аккаунт"""
        edited_account = await telegraph.edit_account(
            access_token=created_account.access_token,
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe",
        )
        assert edited_account.short_name == "GH"
        assert edited_account.author_name == "GameHipe"
        assert str(edited_account.author_url) == "https://github.com/game-hipe"

    @pytest.mark.asyncio
    async def test_edit_page(
        self,
        telegraph: AsyncTelegraph,
        created_page: Page,
        created_account: AsyncAccount,
    ):
        page = await telegraph.edit_page(
            access_token=created_account.access_token,
            path=created_page.path,
            title="Test Page 2",
            author_name="GameHipe",
            content=[NodeElement(tag="p", children=["Hello, World! Test 2"])],
            return_content=True,
        )

        assert page.title == "Test Page 2"
        assert page.author_name == "GameHipe"

        assert page.content[0].children[0] == "Hello, World! Test 2"

    @pytest.mark.asyncio
    async def test_edit_without_access_token(
        self, telegraph: AsyncTelegraph, created_page: Page
    ):
        with pytest.raises(ValidationError):
            await telegraph.edit_page(
                path=created_page.path,
                title="Test Page 2",
                author_name="GameHipe",
                content=[NodeElement(tag="p", children=["Hello, World! Test 2"])],
                return_content=True,
            )

    @pytest.mark.asyncio
    async def test_get_page(
        self,
        telegraph: AsyncTelegraph,
        created_page: Page,
        created_account: AsyncAccount,
    ):
        page = await telegraph.get_page(
            access_token=created_account.access_token,
            path=created_page.path,
            return_content=True,
        )

        assert page.title == "Test Page 2"
        assert page.author_name == "GameHipe"

        assert page.content[0].children[0] == "Hello, World! Test 2"

    @pytest.mark.asyncio
    async def test_get_views(
        self,
        telegraph: AsyncTelegraph,
        created_page: Page,
        created_account: AsyncAccount,
    ):
        views = await telegraph.get_views(
            access_token=created_account.access_token,
            path=created_page.path,
            day=1,
            month=2,
            year=2026,
        )

    @pytest.mark.asyncio
    async def test_get_views_error(
        self,
        telegraph: AsyncTelegraph,
        created_page: Page,
        created_account: AsyncAccount,
    ):
        with pytest.raises(TelegraphError):
            await telegraph.get_views(
                access_token=created_account.access_token, path=created_page.path
            )

    @pytest.mark.asyncio
    async def test_get_account_info(
        self, telegraph: AsyncTelegraph, created_account: AsyncAccount
    ):
        account = await telegraph.get_account_info(
            access_token=created_account.access_token
        )

        assert account.short_name == "GH"
        assert account.author_name == "GameHipe"
        assert str(account.author_url) == "https://github.com/game-hipe"

    @pytest.mark.asyncio
    async def test_get_account_info_error(self, telegraph: AsyncTelegraph):
        with pytest.raises(TelegraphError):
            await telegraph.get_account_info(access_token="123")

    @pytest.mark.asyncio
    async def test_get_page_list(
        self, telegraph: AsyncTelegraph, created_account: AsyncAccount
    ):
        # Создадим несколько страниц
        for i in range(3):
            await created_account.create_page(
                title=f"Page {i}", content=[NodeElement(tag="p", children=["test"])]
            )
        page_list = await telegraph.get_page_list(
            access_token=created_account.access_token, limit=2
        )
        assert page_list.total_count >= 3
        assert len(page_list.pages) == 2

    @pytest.mark.asyncio
    async def test_create_page_with_html(
        self, telegraph: AsyncTelegraph, created_account: AsyncAccount
    ):
        html_content = "<p>Hello from <b>HTML</b></p>"
        page = await telegraph.create_page(
            access_token=created_account.access_token,
            title="HTML Page",
            html=html_content,
        )
        # Получим страницу с контентом и проверим структуру
        page_with_content = await telegraph.get_page(
            path=page.path, return_content=True
        )
        assert page_with_content.content[0].tag == "p"
        assert page_with_content.content[0].children[0] == "Hello from "
        assert page_with_content.content[0].children[1].tag == "strong"
        assert page_with_content.content[0].children[1].children[0] == "HTML"

    @pytest.mark.asyncio
    async def test_create_page_without_content_or_html(
        self, telegraph: AsyncTelegraph, created_account: SyncAccount
    ):
        with pytest.raises(ValidationError):
            await telegraph.create_page(
                access_token=created_account.access_token, title="No content"
            )

    @pytest.mark.asyncio
    async def test_get_views_with_date(
        self,
        telegraph: AsyncTelegraph,
        created_page: Page,
        created_account: SyncAccount,
    ):
        # Запросим просмотры за текущую дату (может быть 0)
        views = await telegraph.get_views(
            access_token=created_account.access_token,
            path=created_page.path,
            year=2026,
            month=3,
            day=3,
        )
        assert isinstance(views.views, int)

    @pytest.mark.asyncio
    async def test_context_manager(self):
        async with AsyncTelegraph() as t:
            account = await t.create_account(short_name="Test")
            assert account.access_token is not None
        # Проверим, что клиент закрыт (можно через mock, но в реальности httpx.Client закроется)

    @pytest.mark.asyncio
    async def test_revoke_access_token(
        self, telegraph: AsyncTelegraph, created_account: SyncAccount
    ):
        old_token = created_account.access_token
        new_account = await telegraph.revoke_access_token(access_token=old_token)
        assert new_account.access_token != old_token
        # Проверим, что старый токен больше не работает
        with pytest.raises(TelegraphError):
            await telegraph.get_account_info(access_token=old_token)


@pytest.mark.asyncio(loop_scope="class")
class TestAsyncORM:
    @pytest_asyncio.fixture
    async def telegraph_class(self):
        async with AsyncTelegraph(AsyncClient(timeout=30)) as tg:
            yield tg

    @pytest_asyncio.fixture
    async def created_account(self, telegraph_class):
        """Фикстура создает аккаунт и возвращает его для всех тестов класса"""
        account = await telegraph_class.create_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe/telegraph-api",
        )
        return account

    @pytest.mark.asyncio
    async def test_create_page(self, created_account: AsyncAccount):
        page = await created_account.create_page(
            title="Test Page",
            author_name="GameHipe",
            content=[NodeElement(tag="p", children=["Hello, World!"])],
            return_content=True,
        )

        assert page.title == "Test Page"
        assert page.author_name == "GameHipe"

        assert page.content[0].children[0] == "Hello, World!"

    @pytest.mark.asyncio
    async def test_edit_account(self, created_account: AsyncAccount):
        edited_account = await created_account.edit_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe",
        )

        assert edited_account.short_name == "GH"
        assert edited_account.author_name == "GameHipe"
        assert str(edited_account.author_url) == "https://github.com/game-hipe"

    @pytest.mark.asyncio
    async def test_get_account(self, created_account: AsyncAccount):
        account = await created_account.get_account_info(
            fields=["short_name", "author_name", "author_url"]
        )

        assert account.short_name == "GH"
        assert account.author_name == "GameHipe"
        assert str(account.author_url) == "https://github.com/game-hipe/telegraph-api"

    @pytest.mark.asyncio
    async def test_get_page_list(self, created_account: AsyncAccount):
        # Создадим несколько страниц
        for i in range(3):
            await created_account.create_page(
                title=f"Page {i}", content=[NodeElement(tag="p", children=["test"])]
            )
        page_list = await created_account.get_page_list(limit=2)
        assert page_list.total_count >= 3
        assert len(page_list.pages) == 2

    @pytest.mark.asyncio
    async def test_revoke_access_token(self, created_account: AsyncAccount):
        old_token = created_account.access_token
        new_account = await created_account.revoke_access_token()
        assert new_account.access_token != old_token
        # Проверим, что старый токен больше не работает
        with pytest.raises(TelegraphError):
            await created_account.get_account_info()

        account = await new_account.get_account_info(
            fields=["short_name", "author_name", "author_url"]
        )

        assert account.access_token != new_account.access_token
        assert account.short_name == "GH"
        assert account.author_name == "GameHipe"
        assert str(account.author_url) == "https://github.com/game-hipe/telegraph-api"


# --- ТЕСТЫ ВАЛИДАЦИИ (Общие) ---


@pytest.mark.parametrize(
    "invalid_data",
    [
        {"short_name": ""},  # Слишком короткое
        {"short_name": "a" * 33},  # Слишком длинное
    ],
)
def test_create_account_validation_errors(invalid_data):
    client = Telegraph()
    with pytest.raises((TelegraphError, ValidationError)):
        client.create_account(**invalid_data)


def test_page_validation():
    client = Telegraph()
    # Ошибка: нет ни content, ни html
    with pytest.raises(ValidationError):
        client.create_page(access_token="token", title="Title")
