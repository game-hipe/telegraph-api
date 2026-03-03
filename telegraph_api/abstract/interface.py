"""Интерфейсы Telegraph"""

from typing import Any, List, Literal, Optional, overload

from ..entities.create.account import (
    CreateAccount,
    EditAccount,
    GetAccountInfo,
    RevokeAccessToken,
)
from ..entities.create.page import CreatePage, EditPage, GetPage, GetPageList, GetViews
from ..entities.models import Account, Page, PageList, PageViews


class TelegraphInterface:
    """
    Интерфейс для синхронного клиентского API Telegraph.
    Определяет все публичные методы с полной типизацией и перегрузками.
    """

    @overload
    def create_account(self, account: CreateAccount) -> Account: ...

    @overload
    def create_account(
        self,
        *,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> Account: ...

    @overload
    def edit_account(self, edit_account: EditAccount) -> Account: ...

    @overload
    def edit_account(
        self,
        *,
        access_token: str,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> Account: ...

    @overload
    def get_account_info(self, info: GetAccountInfo) -> Account: ...

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
    ) -> Account: ...

    @overload
    def revoke_access_token(self, revoke: RevokeAccessToken) -> Account: ...

    @overload
    def revoke_access_token(self, *, access_token: str) -> Account: ...

    @overload
    def create_page(self, page: CreatePage) -> Page: ...

    @overload
    def create_page(
        self,
        *,
        access_token: str,
        title: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    @overload
    def edit_page(self, edit_page: EditPage) -> Page: ...

    @overload
    def edit_page(
        self,
        *,
        access_token: str,
        title: str,
        path: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    @overload
    def get_page(self, get_page: GetPage) -> Page: ...

    @overload
    def get_page(self, *, path: str, return_content: bool = False) -> Page: ...

    @overload
    def get_page_list(self, get_page_list: GetPageList) -> PageList: ...

    @overload
    def get_page_list(
        self, *, access_token: str, offset: int = 0, limit: int = 50
    ) -> PageList: ...

    @overload
    def get_views(self, get_views: GetViews) -> PageViews: ...

    @overload
    def get_views(
        self,
        *,
        path: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
    ) -> PageViews: ...


class AsyncTelegraphInterface:
    """
    Интерфейс для асинхронного клиентского API Telegraph.
    Аналогичен TelegraphInterface, но все методы асинхронные.
    """

    @overload
    async def create_account(self, account: CreateAccount) -> Account: ...

    @overload
    async def create_account(
        self,
        *,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> Account: ...

    @overload
    async def edit_account(self, edit_account: EditAccount) -> Account: ...

    @overload
    async def edit_account(
        self,
        *,
        access_token: str,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> Account: ...

    @overload
    async def get_account_info(self, info: GetAccountInfo) -> Account: ...

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
    ) -> Account: ...

    @overload
    async def revoke_access_token(self, revoke: RevokeAccessToken) -> Account: ...

    @overload
    async def revoke_access_token(self, *, access_token: str) -> Account: ...

    @overload
    async def create_page(self, page: CreatePage) -> Page: ...

    @overload
    async def create_page(
        self,
        *,
        access_token: str,
        title: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    @overload
    async def edit_page(self, edit_page: EditPage) -> Page: ...

    @overload
    async def edit_page(
        self,
        *,
        access_token: str,
        title: str,
        path: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    @overload
    async def get_page(self, get_page: GetPage) -> Page: ...

    @overload
    async def get_page(self, *, path: str, return_content: bool = False) -> Page: ...

    @overload
    async def get_page_list(self, get_page_list: GetPageList) -> PageList: ...

    @overload
    async def get_page_list(
        self, *, access_token: str, offset: int = 0, limit: int = 50
    ) -> PageList: ...

    @overload
    async def get_views(self, get_views: GetViews) -> PageViews: ...

    @overload
    async def get_views(
        self,
        *,
        path: str,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = None,
    ) -> PageViews: ...
