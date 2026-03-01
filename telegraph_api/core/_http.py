from typing import TypeAlias
from enum import Enum
from urllib.parse import urljoin

from httpx import Client, AsyncClient, Response


ClientAlias: TypeAlias = Client | AsyncClient | None


class AccountEndpoints(Enum):
    """
    Перечисление эндпоинтов для работы с аккаунтом в Telegraph API.

    Содержит константы URL-путей для выполнения операций с аккаунтом:

    Примеры:
        AccountEndpoints.CREATE_ACCOUNT.value -> "/createAccount"
    """

    CREATE_ACCOUNT = "/createAccount"
    """Создание нового аккаунта. 
    Используется для регистрации нового аккаунта в системе Telegraph.
    """

    EDIT_ACCOUNT = "/editAccountInfo"
    """Редактирование информации аккаунта.
    Позволяет изменить имя, аватар или другие данные аккаунта.
    """

    GET_ACCOUNT = "/getAccountInfo"
    """Получение информации об аккаунте.
    Возвращает текущие данные аккаунта, включая имя, токен, количество страниц и т.д.
    """

    REVOKE_ACCESSTOKEN = "/revokeAccessToken"
    """Отзыв текущего токена доступа.
    Генерирует новый токен и делает старый недействительным.
    """


class PageEndpoints(Enum):
    """
    Перечисление эндпоинтов для работы со страницами в Telegraph API.

    Содержит константы URL-путей для создания, редактирования и получения страниц.

    Примеры:
        PageEndpoints.CREATE_PAGE.value -> "/createPage"
    """

    CREATE_PAGE = "/createPage"
    """Создание новой страницы.
    Позволяет опубликовать новую статью или запись на аккаунте.
    """

    EDITPAGE = "/editPage"
    """Редактирование существующей страницы.
    Позволяет обновить содержимое, заголовок или другие атрибуты страницы.
    """

    GET_PAGE = "/getPage"
    """Получение данных страницы по пути.
    Возвращает содержимое указанной страницы в формате JSON.
    """

    GET_PAGE_LIST = "/getPageList"
    """Получение списка страниц аккаунта.
    Возвращает список всех страниц, привязанных к аккаунту, с пагинацией.
    """

    GET_VIEWS = "/getViews"
    """Получение количества просмотров страницы.
    Возвращает число просмотров указанной страницы за выбранный период.
    """


class BaseRequestManager:
    """
    Базовый менеджер запросов для взаимодействия с API Telegraph.

    Класс предоставляет удобные методы для формирования URL-адресов
    и управляет клиентом для выполнения HTTP-запросов.
    Используется как основа для более специфичных менеджеров.

    Атрибуты:
        BASE_URL (str): Базовый URL API Telegraph.
    """

    BASE_URL = "https://api.telegra.ph"
    """Базовый URL API Telegraph. Используется для построения полных адресов эндпоинтов."""

    def __init__(self, client: ClientAlias) -> None:
        """
        Инициализирует менеджер запросов с указанным HTTP-клиентом.

        Аргументы:
            client (ClientAlias): Экземпляр HTTP-клиента, используемый для выполнения запросов.
                                 Может быть синхронным или асинхронным в зависимости от реализации.
        """
        self._client = client or Client()

    def urljoin(self, url: str) -> str:
        """
        Объединяет базовый URL с переданным путём.

        Метод безопасно соединяет BASE_URL и относительный путь,
        корректно обрабатывая слеши.

        Аргументы:
            url (str): Относительный путь к эндпоинту (например, '/createAccount').

        Возвращает:
            str: Полный URL, составленный из BASE_URL и переданного пути.

        Пример:
            >>> manager.urljoin("/getAccountInfo")
            'https://api.telegra.ph/getAccountInfo'
        """
        return urljoin(self.BASE_URL, url)

    @property
    def client(self) -> ClientAlias:
        """
        Возвращает HTTP-клиент, используемый для выполнения запросов.

        Используется как защищённый способ доступа к клиенту.

        Возвращает:
            ClientAlias: Экземпляр HTTP-клиента.
        """
        return self._client

    @property
    def create_account(self) -> str:
        """
        Возвращает полный URL для создания нового аккаунта.

        Возвращает:
            str: Полный URL эндпоинта '/createAccount'.

        Пример:
            >>> manager.create_account
            'https://api.telegra.ph/createAccount'
        """
        return self.urljoin(AccountEndpoints.CREATE_ACCOUNT.value)

    @property
    def edit_account(self) -> str:
        """
        Возвращает полный URL для редактирования информации аккаунта.

        Возвращает:
            str: Полный URL эндпоинта '/editAccountInfo'.
        """
        return self.urljoin(AccountEndpoints.EDIT_ACCOUNT.value)

    @property
    def get_account(self) -> str:
        """
        Возвращает полный URL для получения информации об аккаунте.

        Возвращает:
            str: Полный URL эндпоинта '/getAccountInfo'.
        """
        return self.urljoin(AccountEndpoints.GET_ACCOUNT.value)

    @property
    def revoke_accesstoken(self) -> str:
        """
        Возвращает полный URL для отзыва токена доступа.

        Возвращает:
            str: Полный URL эндпоинта '/revokeAccessToken'.
        """
        return self.urljoin(AccountEndpoints.REVOKE_ACCESSTOKEN.value)

    @property
    def create_page(self) -> str:
        """
        Возвращает полный URL для создания новой страницы.

        Возвращает:
            str: Полный URL эндпоинта '/createPage'.
        """
        return self.urljoin(PageEndpoints.CREATE_PAGE.value)

    @property
    def edit_page(self) -> str:
        """
        Возвращает полный URL для редактирования существующей страницы.

        Возвращает:
            str: Полный URL эндпоинта '/editPage'.
        """
        return self.urljoin(PageEndpoints.EDITPAGE.value)

    @property
    def get_page(self) -> str:
        """
        Возвращает полный URL для получения данных страницы по её пути.

        Возвращает:
            str: Полный URL эндпоинта '/getPage'.
        """
        return self.urljoin(PageEndpoints.GET_PAGE.value)

    @property
    def get_page_list(self) -> str:
        """
        Возвращает полный URL для получения списка страниц аккаунта.

        Возвращает:
            str: Полный URL эндпоинта '/getPageList'.
        """
        return self.urljoin(PageEndpoints.GET_PAGE_LIST.value)

    @property
    def get_views(self) -> str:
        """
        Возвращает полный URL для получения количества просмотров страницы.

        Возвращает:
            str: Полный URL эндпоинта '/getViews'.
        """
        return self.urljoin(PageEndpoints.GET_VIEWS.value)

    def request(self, url: str, method: str, *args, **kwargs) -> Response:
        if isinstance(self.client, Client):
            return self.client.request(method=method, url=url, *args, **kwargs)

        else:
            raise TypeError("Данный клиент не поддерживает синхронную обработку.")


class AsyncRequestManager(BaseRequestManager):
    def __init__(self, client: AsyncClient):
        """Асинхронная реализация

        Args:
            client (AsyncClient): Асинхронный клиент httpx
        """
        super().__init__(client or AsyncClient())

    async def request(self, url, method, *args, **kwargs):
        if isinstance(self.client, AsyncClient):
            return self.client.request(method=method, url=url, *args, **kwargs)

        else:
            raise TypeError("Данный клиент не поддерживает синхронную обработку.")


class RequestManager(BaseRequestManager): ...
