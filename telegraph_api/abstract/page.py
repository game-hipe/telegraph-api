from abc import ABC, abstractmethod
from typing import overload, Optional, List, TypeVar, Generic

from pydantic import BaseModel
from httpx import Client, AsyncClient
from httpx._client import BaseClient

from ..core._http import BaseRequestManager, AsyncRequestManager
from ..entities.create.page import CreatePage, EditPage, GetPage, GetPageList, GetViews
from ..entities.models import Page, PageList, PageViews, Node

_T = TypeVar("_T", bound=BaseModel)
T = TypeVar("T", bound=BaseRequestManager)
_G = TypeVar("_G", bound=BaseClient)


class BasePageMethods(ABC, Generic[T, _G]):
    HTTP_CLIENT: type[T] = BaseRequestManager

    def __init__(self, client: _G = None):
        self._http = self.HTTP_CLIENT(client)

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

    @abstractmethod
    def get_views(self, *args, **kwargs):
        """Получение статистики просмотров страницы."""

    @abstractmethod
    def get_page_list(self, *args, **kwargs):
        """Получение списка страниц аккаунта."""

    @abstractmethod
    def get_page(self, *args, **kwargs):
        """получение информации о странице Telegraph."""

    @abstractmethod
    def edit_page(self, *args, **kwargs):
        """Редактирование существующей страницы Telegraph."""

    @abstractmethod
    def create_page(self, *args, **kwargs):
        """создание новой страницы Telegraph."""

    def _make_create_page(self, *args, **kwargs) -> CreatePage:
        return self._make_methods(CreatePage, *args, **kwargs)

    def _make_edit_page(self, *args, **kwargs) -> EditPage:
        return self._make_methods(EditPage, *args, **kwargs)

    def _make_get_page(self, *args, **kwargs) -> GetPage:
        return self._make_methods(GetPage, *args, **kwargs)

    def _make_get_page_list(self, *args, **kwargs) -> GetPageList:
        return self._make_methods(GetPageList, *args, **kwargs)

    def _make_get_views(self, *args, **kwargs) -> GetViews:
        return self._make_methods(GetViews, *args, **kwargs)

    @staticmethod
    def _make_methods(model: type[_T], *args, **kwargs) -> _T:
        if args and issubclass(args[0], model):
            return args[0]

        return model(**kwargs)


class AsyncPageMethods(BasePageMethods[AsyncRequestManager, AsyncClient]):
    HTTP_CLIENT = AsyncRequestManager

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

    @abstractmethod
    async def get_views(self, *args, **kwargs):
        """Получение статистики просмотров страницы."""

    @abstractmethod
    async def get_page_list(self, *args, **kwargs):
        """Получение списка страниц аккаунта."""

    @abstractmethod
    async def get_page(self, *args, **kwargs):
        """получение информации о странице Telegraph."""

    @abstractmethod
    async def edit_page(self, *args, **kwargs):
        """Редактирование существующей страницы Telegraph."""

    @abstractmethod
    async def create_page(self, *args, **kwargs):
        """создание новой страницы Telegraph."""


class PageMethods(BasePageMethods[BaseRequestManager, Client]):
    HTTP_CLIENT = BaseRequestManager
