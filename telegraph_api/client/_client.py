from typing import overload, Optional, List, Literal, Any, Dict, TypeVar

from httpx import Client, AsyncClient
from pydantic import BaseModel
from bs4 import BeautifulSoup

from ..abstract.interface import TelegraphInterface, AsyncTelegraphInterface
from ..abstract.page import PageMethods, AsyncPageMethods
from ..abstract.account import AccountMethods, AsyncAccountMethods
from ..entities.create.account import (
    CreateAccount,
    EditAccount,
    GetAccountInfo,
    RevokeAccessToken,
)
from ..entities.models import Account, Response, NodeElement, Page
from ..entities.work.account import SyncAccount, AsyncAccount

from ..entities.create.page import CreatePage, EditPage, GetPage, GetPageList, GetViews
from ..entities.models import PageList, PageViews, Node
from ..exc import TelegraphError


_T = TypeVar("_T", bound=BaseModel)


class BaseTelegraph:
    BASE_FEATURES: str = "html.parser"

    def __init__(self, features: Optional[str] = None):
        self.features = features or self.BASE_FEATURES

    def _to_model(self, model: type[_T], data: Dict[str, Any]) -> _T:
        response = Response[model](**data)
        if not response.ok:
            raise TelegraphError(
                f"Запрос к серверу не увенчался успехом, сообщение от Telegraph: {response.error}"
            )

        return response.result

    def _create_nodes(
        self, content: str, features: str | None = None
    ) -> list[NodeElement]:
        soup = BeautifulSoup(content, features=features or self.BASE_FEATURES)
        nodes: list[NodeElement] = []

        for child in soup:
            if child.name is None:
                nodes.append(str(child.string))
                continue
            tag = NodeElement(
                tag=child.name,
                attrs=child.attrs,
                children=self._create_nodes("".join(map(str, child.contents))),
            )
            nodes.append(tag)
        return nodes


class Telegraph(AccountMethods, PageMethods, BaseTelegraph, TelegraphInterface):
    BASE_FEATURES: str = "html.parser"

    def __init__(self, client: Optional[Client] = None):
        super().__init__(client)

    @overload
    def create_account(self, account: CreateAccount) -> SyncAccount:
        """
        Создание нового аккаунта Telegraph.

        Args:
            account (CreateAccount): Модель для метода createAccount.

        Returns:
            Account: Объект, представляющий аккаунт Telegraph.
        """

    @overload
    def create_account(
        self,
        *,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> SyncAccount:
        """
        Создание нового аккаунта Telegraph.

        Args:
            short_name (str): Имя аккаунта. Длина: от 1 до 32 символов.
            author_name (Optional[str], optional): Имя автора по умолчанию. Длина: от 0 до 128 символов.
            author_url (Optional[str], optional): Ссылка на профиль автора. Длина: от 0 до 512 символов.

        Returns:
            Account: Объект, представляющий аккаунт Telegraph.
        """

    @overload
    def edit_account(self, edit_account: EditAccount) -> Account:
        """
        Обновление информации об аккаунте Telegraph.

        Args:
            edit_account (EditAccount): Модель для метода editAccountInfo.

        Returns:
            Account: Обновлённый объект аккаунта.
        """

    @overload
    def edit_account(
        self,
        *,
        access_token: str,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> Account:
        """
        Обновление информации об аккаунте Telegraph.

        Args:
            access_token (str): Токен доступа к аккаунту.
            short_name (Optional[str], optional): Новое имя аккаунта.
            author_name (Optional[str], optional): Новое имя автора.
            author_url (Optional[str], optional): Новая ссылка на профиль автора.

        Returns:
            Account: Обновлённый объект аккаунта.
        """

    @overload
    def get_account_info(self, info: GetAccountInfo) -> Account:
        """
        Получение информации об аккаунте Telegraph.

        Args:
            info (GetAccountInfo): Модель для метода getAccountInfo.

        Returns:
            Account: Информация об аккаунте.
        """

    @overload
    def get_account_info(
        self,
        *,
        access_token: str,
        fields: Optional[
            List[
                Literal[
                    "short_name", "author_name", "author_url", "auth_url", "page_count"
                ]
            ]
        ] = None,
    ) -> Account:
        """
        Получение информации об аккаунте Telegraph.

        Args:
            access_token (str): Токен доступа к аккаунту.
            fields (Optional[List], optional): Поля, которые нужно вернуть.

        Returns:
            Account: Информация об аккаунте.
        """

    @overload
    def revoke_access_token(self, revoke: RevokeAccessToken) -> Account:
        """
        Аннулирование текущего токена и получение нового.

        Args:
            revoke (RevokeAccessToken): Модель для метода revokeAccessToken.

        Returns:
            Account: Новый объект аккаунта с новым токеном.
        """

    @overload
    def revoke_access_token(self, *, access_token: str) -> Account:
        """
        Аннулирование текущего токена и получение нового.

        Args:
            access_token (str): Токен, который нужно заменить.

        Returns:
            Account: Новый объект аккаунта с новым токеном.
        """

    @overload
    def create_page(self, page: CreatePage) -> Page:
        """создание новой страницы Telegraph.

        Args:
            page (CreatePage): Модель для метода createPage

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    def create_page(
        self,
        *,
        access_token: str,
        title: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Node]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page:
        """
        создание новой страницы Telegraph.

        *Важно, один из атрибутов (content | html) должен будет быть заполнен, приоритет одаётся content если html заполнен*

        Args:
            access_token (str): Токен доступа к аккаунту Telegraph.
            title (str): Заголовок страницы. Допустимая длина: от 1 до 256 символов.
            author_name (Optional[str], optional): Имя автора, отображаемое под заголовком. Длина: от 0 до 128 символов. Обычное значение None.
            author_url (Optional[str], optional): Ссылка на профиль автора. Может быть любой ссылкой. Длина: от 0 до 512 символов. Обычное значение None.
            content (Optional[List[Node]], optional): Содержимое страницы в виде массива узлов DOM. Общий размер JSON не должен превышать 64 КБ.. Обычное значение None.
            html (Optional[str], optional): Содержимое страницы в виде HTML, который в дальнейшем будет обработан. Обычное значение None.
            return_content (bool, optional): Если true, в ответе будет возвращено поле content объекта Page. Обычное значение False.

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    def edit_page(self, edit_page: EditPage) -> Page:
        """Редактирование существующей страницы Telegraph.

        Args:
            edit_page (EditPage): Модель для метода editPage

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    def edit_page(
        self,
        *,
        access_token: str,
        title: str,
        path: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Node]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ):
        """
        Редактирование существующей страницы Telegraph.

        *Важно, один из атрибутов (content | html) должен будет быть заполнен, приоритет одаётся content если html заполнен*

        Args:
            access_token (str): Токен доступа к аккаунту Telegraph.
            title (str): Заголовок страницы. Допустимая длина: от 1 до 256 символов.
            path (str): Путь к странице (часть URL после telegra.ph/)
            author_name (Optional[str], optional): Имя автора, отображаемое под заголовком. Длина: от 0 до 128 символов. Обычное значение None.
            author_url (Optional[str], optional): Ссылка на профиль автора. Может быть любой ссылкой. Длина: от 0 до 512 символов. Обычное значение None.
            content (Optional[List[Node]], optional): Содержимое страницы в виде массива узлов DOM. Общий размер JSON не должен превышать 64 КБ.. Обычное значение None.
            html (Optional[str], optional): Содержимое страницы в виде HTML, который в дальнейшем будет обработан. Обычное значение None.
            return_content (bool, optional): Если true, в ответе будет возвращено поле content объекта Page. Обычное значение False.

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    def get_page(self, get_page: GetPage) -> Page:
        """получение информации о странице Telegraph.

        Args:
            get_page (GetPage): Модель для метода getPage

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    def get_page(self, *, path: str, return_content: bool = False) -> Page:
        """получение информации о странице Telegraph.

        Args:
            path (str): Путь к странице (часть URL после telegra.ph/)
            return_content (bool, optional): Если true, в ответе будет возвращено поле content объекта Page. Обычное значение False.

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    def get_page_list(self, get_page_list: GetPageList) -> PageList:
        """Получение списка страниц аккаунта.

        Args:
            get_page_list (GetPageList): Модель для метода getPageList

        Returns:
            PageList: Объект, представляющий список статей Telegraph, принадлежащих аккаунту.
        """

    @overload
    def get_page_list(
        self, *, access_token: str, offset: int = 0, limit: int = 50
    ) -> PageList:
        """Получение списка страниц аккаунта.

        Args:
            access_token (str): Токен доступа к аккаунту Telegraph.
            offset (int, optional): Смещение относительно начала списка. Обычное значение 0.
            limit (int, optional): Количество статей, которое необходимо получить. Обычное значение 50.

        Returns:
            PageList: Объект, представляющий список статей Telegraph, принадлежащих аккаунту.
        """

    @overload
    def get_views(self, get_views: GetViews) -> PageViews:
        """Получение статистики просмотров страницы.

        Args:
            get_views (GetViews): Модель для метода getViews

        Returns:
            PageViews: Объект, представляющий количество просмотров страницы Telegraph.
        """

    @overload
    def get_views(
        self,
        *,
        path: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
    ) -> GetViews:
        """Получение статистики просмотров страницы.

        Args:
            path (str): Путь к странице (например, Sample-Page-12-15).
            year (Optional[int], optional): Год (2000–2100). Обязателен, если передан month. Обычное значение None.
            month (Optional[int], optional): Месяц (1–12). Обязателен, если передан day. Обычное значение None.
            day (Optional[int], optional): День (1–31). Обязателен, если передан hour. Обычное значение None.
            hour (Optional[int], optional): Час (0–24). Если передан, также должны быть указаны year, month и day. Обычное значение None.

        Returns:
            GetViews: Объект, представляющий количество просмотров страницы Telegraph.
        """

    def create_account(self, *args, **kwargs):
        account = self._make_create_account(*args, **kwargs)
        response = self._http.request(
            url=self._http.create_account,
            method="POST",
            json=account.model_dump(mode="json"),
        )

        response.raise_for_status()
        json = response.json()
        if json.get("result"):
            json["result"] |= {"telegraph": self}

        return self._to_model(SyncAccount, json)

    def create_page(self, *args, **kwargs):
        page = self._make_create_page(*args, **kwargs)
        if not page.content and page.html:
            page.content = self._create_nodes(page.html)

        response = self._http.request(
            url=self._http.create_page,
            method="POST",
            json=page.model_dump(exclude=["html"], mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Page, response.json())

    def edit_account(self, *args, **kwargs):
        account = self._make_edit_account(*args, **kwargs)

        response = self._http.request(
            url=self._http.edit_account,
            method="POST",
            json=account.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Account, response.json())

    def edit_page(self, *args, **kwargs):
        page = self._make_edit_page(*args, **kwargs)
        if not page.content and page.html:
            page.content = self._create_nodes(page.html)

        response = self._http.request(
            url=self._http.edit_page,
            method="POST",
            json=page.model_dump(exclude=["html"]),
        )
        response.raise_for_status()

        return self._to_model(Page, response.json())

    def get_account_info(self, *args, **kwargs):
        account = self._make_get_account_info(*args, **kwargs)

        response = self._http.request(
            url=self._http.get_account,
            method="POST",
            json=account.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Account, response.json())

    def get_page(self, *args, **kwargs):
        page = self._make_get_page(*args, **kwargs)

        response = self._http.request(
            url=self._http.get_page,
            method="POST",
            json=page.model_dump(exclude=["html"]),
        )
        response.raise_for_status()

        return self._to_model(Page, response.json())

    def get_page_list(self, *args, **kwargs):
        page = self._make_get_page_list(*args, **kwargs)

        response = self._http.request(
            url=self._http.get_page_list,
            method="POST",
            json=page.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(PageList, response.json())

    def get_views(self, *args, **kwargs):
        views = self._make_get_views(*args, **kwargs)

        response = self._http.request(
            url=self._http.get_views, method="POST", json=views.model_dump(mode="json")
        )
        response.raise_for_status()

        return self._to_model(PageViews, response.json())

    def revoke_access_token(self, *args, **kwargs):
        token = self._make_revoke_access_token(*args, **kwargs)

        response = self._http.request(
            url=self._http.revoke_accesstoken,
            method="POST",
            json=token.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Account, response.json())

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self._http.client.close()


class AsyncTelegraph(
    AsyncAccountMethods, AsyncPageMethods, BaseTelegraph, AsyncTelegraphInterface
):
    BASE_FEATURES: str = "html.parser"

    def __init__(self, client: Optional[AsyncClient] = None):
        super().__init__(client or AsyncClient())

    @overload
    async def create_account(self, account: CreateAccount) -> AsyncAccount:
        """
        Создание нового аккаунта Telegraph.

        Args:
            account (CreateAccount): Модель для метода createAccount.

        Returns:
            Account: Объект, представляющий аккаунт Telegraph.
        """

    @overload
    async def create_account(
        self,
        *,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> AsyncAccount:
        """
        Создание нового аккаунта Telegraph.

        Args:
            short_name (str): Имя аккаунта. Длина: от 1 до 32 символов.
            author_name (Optional[str], optional): Имя автора по умолчанию. Длина: от 0 до 128 символов.
            author_url (Optional[str], optional): Ссылка на профиль автора. Длина: от 0 до 512 символов.

        Returns:
            Account: Объект, представляющий аккаунт Telegraph.
        """

    @overload
    async def edit_account(self, edit_account: EditAccount) -> Account:
        """
        Обновление информации об аккаунте Telegraph.

        Args:
            edit_account (EditAccount): Модель для метода editAccountInfo.

        Returns:
            Account: Обновлённый объект аккаунта.
        """

    @overload
    async def edit_account(
        self,
        *,
        access_token: str,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> Account:
        """
        Обновление информации об аккаунте Telegraph.

        Args:
            access_token (str): Токен доступа к аккаунту.
            short_name (Optional[str], optional): Новое имя аккаунта.
            author_name (Optional[str], optional): Новое имя автора.
            author_url (Optional[str], optional): Новая ссылка на профиль автора.

        Returns:
            Account: Обновлённый объект аккаунта.
        """

    @overload
    async def get_account_info(self, info: GetAccountInfo) -> Account:
        """
        Получение информации об аккаунте Telegraph.

        Args:
            info (GetAccountInfo): Модель для метода getAccountInfo.

        Returns:
            Account: Информация об аккаунте.
        """

    @overload
    async def get_account_info(
        self,
        *,
        access_token: str,
        fields: Optional[
            List[
                Literal[
                    "short_name", "author_name", "author_url", "auth_url", "page_count"
                ]
            ]
        ] = None,
    ) -> Account:
        """
        Получение информации об аккаунте Telegraph.

        Args:
            access_token (str): Токен доступа к аккаунту.
            fields (Optional[List], optional): Поля, которые нужно вернуть.

        Returns:
            Account: Информация об аккаунте.
        """

    @overload
    async def revoke_access_token(self, revoke: RevokeAccessToken) -> Account:
        """
        Аннулирование текущего токена и получение нового.

        Args:
            revoke (RevokeAccessToken): Модель для метода revokeAccessToken.

        Returns:
            Account: Новый объект аккаунта с новым токеном.
        """

    @overload
    async def revoke_access_token(self, *, access_token: str) -> Account:
        """
        Аннулирование текущего токена и получение нового.

        Args:
            access_token (str): Токен, который нужно заменить.

        Returns:
            Account: Новый объект аккаунта с новым токеном.
        """

    @overload
    async def create_page(self, page: CreatePage) -> Page:
        """создание новой страницы Telegraph.

        Args:
            page (CreatePage): Модель для метода createPage

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    async def create_page(
        self,
        *,
        access_token: str,
        title: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Node]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page:
        """
        создание новой страницы Telegraph.

        *Важно, один из атрибутов (content | html) должен будет быть заполнен, приоритет одаётся content если html заполнен*

        Args:
            access_token (str): Токен доступа к аккаунту Telegraph.
            title (str): Заголовок страницы. Допустимая длина: от 1 до 256 символов.
            author_name (Optional[str], optional): Имя автора, отображаемое под заголовком. Длина: от 0 до 128 символов. Обычное значение None.
            author_url (Optional[str], optional): Ссылка на профиль автора. Может быть любой ссылкой. Длина: от 0 до 512 символов. Обычное значение None.
            content (Optional[List[Node]], optional): Содержимое страницы в виде массива узлов DOM. Общий размер JSON не должен превышать 64 КБ.. Обычное значение None.
            html (Optional[str], optional): Содержимое страницы в виде HTML, который в дальнейшем будет обработан. Обычное значение None.
            return_content (bool, optional): Если true, в ответе будет возвращено поле content объекта Page. Обычное значение False.

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    async def edit_page(self, edit_page: EditPage) -> Page:
        """Редактирование существующей страницы Telegraph.

        Args:
            edit_page (EditPage): Модель для метода editPage

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    async def edit_page(
        self,
        *,
        access_token: str,
        title: str,
        path: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Node]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page:
        """
        Редактирование существующей страницы Telegraph.

        *Важно, один из атрибутов (content | html) должен будет быть заполнен, приоритет одаётся content если html заполнен*

        Args:
            access_token (str): Токен доступа к аккаунту Telegraph.
            title (str): Заголовок страницы. Допустимая длина: от 1 до 256 символов.
            path (str): Путь к странице (часть URL после telegra.ph/)
            author_name (Optional[str], optional): Имя автора, отображаемое под заголовком. Длина: от 0 до 128 символов. Обычное значение None.
            author_url (Optional[str], optional): Ссылка на профиль автора. Может быть любой ссылкой. Длина: от 0 до 512 символов. Обычное значение None.
            content (Optional[List[Node]], optional): Содержимое страницы в виде массива узлов DOM. Общий размер JSON не должен превышать 64 КБ.. Обычное значение None.
            html (Optional[str], optional): Содержимое страницы в виде HTML, который в дальнейшем будет обработан. Обычное значение None.
            return_content (bool, optional): Если true, в ответе будет возвращено поле content объекта Page. Обычное значение False.

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    async def get_page(self, get_page: GetPage) -> Page:
        """получение информации о странице Telegraph.

        Args:
            get_page (GetPage): Модель для метода getPage

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    async def get_page(self, *, path: str, return_content: bool = False) -> Page:
        """получение информации о странице Telegraph.

        Args:
            path (str): Путь к странице (часть URL после telegra.ph/)
            return_content (bool, optional): Если true, в ответе будет возвращено поле content объекта Page. Обычное значение False.

        Returns:
            Page: Объект, представляющий страницу на Telegraph.
        """

    @overload
    async def get_page_list(self, get_page_list: GetPageList) -> PageList:
        """Получение списка страниц аккаунта.

        Args:
            get_page_list (GetPageList): Модель для метода getPageList

        Returns:
            PageList: Объект, представляющий список статей Telegraph, принадлежащих аккаунту.
        """

    @overload
    async def get_page_list(
        self, *, access_token: str, offset: int = 0, limit: int = 50
    ) -> PageList:
        """Получение списка страниц аккаунта.

        Args:
            access_token (str): Токен доступа к аккаунту Telegraph.
            offset (int, optional): Смещение относительно начала списка. Обычное значение 0.
            limit (int, optional): Количество статей, которое необходимо получить. Обычное значение 50.

        Returns:
            PageList: Объект, представляющий список статей Telegraph, принадлежащих аккаунту.
        """

    @overload
    async def get_views(self, get_views: GetViews) -> PageViews:
        """Получение статистики просмотров страницы.

        Args:
            get_views (GetViews): Модель для метода getViews

        Returns:
            PageViews: Объект, представляющий количество просмотров страницы Telegraph.
        """

    @overload
    async def get_views(
        self,
        *,
        path: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
    ) -> GetViews:
        """Получение статистики просмотров страницы.

        Args:
            path (str): Путь к странице (например, Sample-Page-12-15).
            year (Optional[int], optional): Год (2000–2100). Обязателен, если передан month. Обычное значение None.
            month (Optional[int], optional): Месяц (1–12). Обязателен, если передан day. Обычное значение None.
            day (Optional[int], optional): День (1–31). Обязателен, если передан hour. Обычное значение None.
            hour (Optional[int], optional): Час (0–24). Если передан, также должны быть указаны year, month и day. Обычное значение None.

        Returns:
            GetViews: Объект, представляющий количество просмотров страницы Telegraph.
        """

    async def create_account(self, *args, **kwargs):
        account = self._make_create_account(*args, **kwargs)
        response = await self._http.request(
            url=self._http.create_account,
            method="POST",
            json=account.model_dump(mode="json"),
        )

        response.raise_for_status()
        json = response.json()
        if json.get("result"):
            json["result"] |= {"telegraph": self}

        return self._to_model(AsyncAccount, json)

    async def create_page(self, *args, **kwargs):
        page = self._make_create_page(*args, **kwargs)
        if not page.content and page.html:
            page.content = self._create_nodes(page.html)

        response = await self._http.request(
            url=self._http.create_page,
            method="POST",
            json=page.model_dump(exclude=["html"], mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Page, response.json())

    async def edit_account(self, *args, **kwargs):
        account = self._make_edit_account(*args, **kwargs)

        response = await self._http.request(
            url=self._http.edit_account,
            method="POST",
            json=account.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Account, response.json())

    async def edit_page(self, *args, **kwargs):
        page = self._make_edit_page(*args, **kwargs)
        if not page.content and page.html:
            page.content = self._create_nodes(page.html)

        response = await self._http.request(
            url=self._http.edit_page,
            method="POST",
            json=page.model_dump(exclude=["html"]),
        )
        response.raise_for_status()

        return self._to_model(Page, response.json())

    async def get_account_info(self, *args, **kwargs):
        account = self._make_get_account_info(*args, **kwargs)

        response = await self._http.request(
            url=self._http.get_account,
            method="POST",
            json=account.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Account, response.json())

    async def get_page(self, *args, **kwargs):
        page = self._make_get_page(*args, **kwargs)

        response = await self._http.request(
            url=self._http.get_page,
            method="POST",
            json=page.model_dump(exclude=["html"]),
        )
        response.raise_for_status()

        return self._to_model(Page, response.json())

    async def get_page_list(self, *args, **kwargs):
        page = self._make_get_page_list(*args, **kwargs)

        response = await self._http.request(
            url=self._http.get_page_list,
            method="POST",
            json=page.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(PageList, response.json())

    async def get_views(self, *args, **kwargs):
        views = self._make_get_views(*args, **kwargs)

        response = await self._http.request(
            url=self._http.get_views, method="POST", json=views.model_dump(mode="json")
        )
        response.raise_for_status()

        return self._to_model(PageViews, response.json())

    async def revoke_access_token(self, *args, **kwargs):
        token = self._make_revoke_access_token(*args, **kwargs)

        response = await self._http.request(
            url=self._http.revoke_accesstoken,
            method="POST",
            json=token.model_dump(mode="json"),
        )
        response.raise_for_status()

        return self._to_model(Account, response.json())

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self._http.client.aclose()
