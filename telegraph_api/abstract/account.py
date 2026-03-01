from abc import ABC, abstractmethod
from typing import overload, Optional, List, TypeVar, Literal, Generic

from pydantic import BaseModel
from httpx import Client, AsyncClient
from httpx._client import BaseClient

from ..core._http import RequestManager, AsyncRequestManager, BaseRequestManager
from ..entities.create.account import (
    CreateAccount,
    EditAccount,
    GetAccountInfo,
    RevokeAccessToken,
)
from ..entities.models import Account

_T = TypeVar("_T", bound=BaseModel)
T = TypeVar("T", bound=BaseRequestManager)
_G = TypeVar("_G", bound=BaseClient)


class BaseAccountMethods(ABC, Generic[T, _G]):
    REQUEST_MANAGER: type[T] = RequestManager

    def __init__(self, client: _G = None):
        self._http = self.REQUEST_MANAGER(client)

    @overload
    def create_account(self, account: CreateAccount) -> Account:
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
    ) -> Account:
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

    @abstractmethod
    def create_account(self, *args, **kwargs) -> Account:
        """Создание нового аккаунта Telegraph."""

    @abstractmethod
    def edit_account(self, *args, **kwargs) -> Account:
        """Обновление информации об аккаунте Telegraph."""

    @abstractmethod
    def get_account_info(self, *args, **kwargs) -> Account:
        """Получение информации об аккаунте Telegraph."""

    @abstractmethod
    def revoke_access_token(self, *args, **kwargs) -> Account:
        """Аннулирование токена доступа и получение нового."""

    def _make_create_account(self, *args, **kwargs) -> CreateAccount:
        return self._make_method(CreateAccount, *args, **kwargs)

    def _make_edit_account(self, *args, **kwargs) -> EditAccount:
        return self._make_method(EditAccount, *args, **kwargs)

    def _make_get_account_info(self, *args, **kwargs) -> GetAccountInfo:
        return self._make_method(GetAccountInfo, *args, **kwargs)

    def _make_revoke_access_token(self, *args, **kwargs) -> RevokeAccessToken:
        return self._make_method(RevokeAccessToken, *args, **kwargs)

    @staticmethod
    def _make_method(model: type[_T], *args, **kwargs) -> _T:
        if args and isinstance(args[0], model):
            return args[0]
        return model(**kwargs)


class BaseAsyncAccountMethods(BaseAccountMethods[AsyncRequestManager, AsyncClient]):
    @overload
    async def create_account(self, account: CreateAccount) -> Account:
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
    ) -> Account:
        """
        Создание нового аккаунта Telegraph.

        Args:
            short_name (str): Имя аккаунта. Длина: от 1 до 32 символов.
            author_name (Optional[str], optional): Имя автора по умолчанию.
            author_url (Optional[str], optional): Ссылка на профиль автора.

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

    @abstractmethod
    async def create_account(self, *args, **kwargs) -> Account:
        """Создание нового аккаунта Telegraph."""

    @abstractmethod
    async def edit_account(self, *args, **kwargs) -> Account:
        """Обновление информации об аккаунте Telegraph."""

    @abstractmethod
    async def get_account_info(self, *args, **kwargs) -> Account:
        """Получение информации об аккаунте Telegraph."""

    @abstractmethod
    async def revoke_access_token(self, *args, **kwargs) -> Account:
        """Аннулирование токена доступа и получение нового."""


class AccountMethods(BaseAccountMethods[RequestManager, Client]): ...
