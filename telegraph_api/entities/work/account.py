from __future__ import annotations

from typing import overload, Optional, List, Literal, Any

from pydantic import model_validator

from ...abstract.interface import TelegraphInterface, AsyncTelegraphInterface
from ...entities.models.account import Account as BaseAccount
from ...entities.create.page import CreatePage, EditPage
from ...entities.models import Page, PageList, PageViews
from ...entities.create.account import EditAccount, GetAccountInfo
from ...entities.create.page import GetPage, GetPageList, GetViews


class SyncAccount(BaseAccount):
    """
    Расширенная модель аккаунта Telegraph с привязанным клиентом.
    Автоматически подставляет access_token во все методы, где это требуется.
    """

    telegraph: TelegraphInterface

    @model_validator(mode="after")
    def validate_access_token(self) -> SyncAccount:
        if not self.access_token:
            raise ValueError(
                "access_token обязателен для использования методов аккаунта."
            )
        return self

    @overload
    def edit_account(self, edit_account: EditAccount) -> BaseAccount: ...

    @overload
    def edit_account(
        self,
        *,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> BaseAccount: ...

    def edit_account(self, *args, **kwargs) -> BaseAccount:
        if len(args) == 1 and isinstance(args[0], EditAccount):
            account = args[0]
            return self.telegraph.edit_account(
                access_token=self.access_token,
                short_name=account.short_name,
                author_name=account.author_name,
                author_url=str(account.author_url) if account.author_url else None,
            )
        return self.telegraph.edit_account(
            access_token=self.access_token,
            short_name=kwargs["short_name"],
            author_name=kwargs.get("author_name"),
            author_url=str(kwargs.get("author_url")),
        )

    @overload
    def get_account_info(self, info: GetAccountInfo) -> BaseAccount: ...

    @overload
    def get_account_info(
        self,
        *,
        fields: Optional[
            List[
                Literal[
                    "short_name", "author_name", "author_url", "auth_url", "page_count"
                ]
            ]
        ] = None,
    ) -> BaseAccount: ...

    def get_account_info(self, *args, **kwargs) -> BaseAccount:
        if len(args) == 1 and isinstance(args[0], GetAccountInfo):
            info = args[0]
            return self.telegraph.get_account_info(
                access_token=self.access_token,
                fields=info.fields,
            )
        return self.telegraph.get_account_info(
            access_token=self.access_token,
            fields=kwargs.get("fields"),
        )

    def revoke_access_token(self) -> BaseAccount:
        return self.telegraph.revoke_access_token(access_token=self.access_token)

    # --- Page Methods ---

    @overload
    def create_page(self, page: CreatePage) -> Page: ...

    @overload
    def create_page(
        self,
        *,
        title: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    def create_page(self, *args, **kwargs) -> Page:
        if len(args) == 1 and isinstance(args[0], CreatePage):
            page = args[0]
            return self.telegraph.create_page(
                access_token=self.access_token,
                title=page.title,
                author_name=page.author_name or self.author_name,
                author_url=str(page.author_url)
                if page.author_url
                else None or self.author_url,
                content=page.content,
                html=page.html,
                return_content=page.return_content,
            )
        return self.telegraph.create_page(
            access_token=self.access_token,
            title=kwargs["title"],
            author_name=kwargs.get("author_name", self.author_name),
            author_url=kwargs.get("author_url", self.author_url),
            content=kwargs.get("content"),
            html=kwargs.get("html"),
            return_content=kwargs.get("return_content", False),
        )

    @overload
    def edit_page(self, edit_page: EditPage) -> Page: ...

    @overload
    def edit_page(
        self,
        *,
        title: str,
        path: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    def edit_page(self, *args, **kwargs) -> Page:
        if len(args) == 1 and isinstance(args[0], EditPage):
            page = args[0]
            return self.telegraph.edit_page(
                access_token=self.access_token,
                title=page.title,
                path=page.path,
                author_name=page.author_name or self.author_name,
                author_url=str(page.author_url)
                if page.author_url
                else None or self.author_url,
                content=page.content,
                html=page.html,
                return_content=page.return_content,
            )
        return self.telegraph.edit_page(
            access_token=self.access_token,
            title=kwargs["title"],
            path=kwargs["path"],
            author_name=kwargs.get("author_name", self.author_name),
            author_url=kwargs.get("author_url", self.author_url),
            content=kwargs.get("content"),
            html=kwargs.get("html"),
            return_content=kwargs.get("return_content", False),
        )

    @overload
    def get_page(self, get_page: GetPage) -> Page: ...

    @overload
    def get_page(self, *, path: str, return_content: bool = False) -> Page: ...

    def get_page(self, *args, **kwargs) -> Page:
        if len(args) == 1 and isinstance(args[0], GetPage):
            page = args[0]
            return self.telegraph.get_page(
                path=page.path, return_content=page.return_content
            )
        return self.telegraph.get_page(
            path=kwargs["path"],
            return_content=kwargs.get("return_content", False),
        )

    @overload
    def get_page_list(self, get_page_list: GetPageList) -> PageList: ...

    @overload
    def get_page_list(self, *, offset: int = 0, limit: int = 50) -> PageList: ...

    def get_page_list(self, *args, **kwargs) -> PageList:
        if len(args) == 1 and isinstance(args[0], GetPageList):
            page_list = args[0]
            return self.telegraph.get_page_list(
                access_token=self.access_token,
                offset=page_list.offset,
                limit=page_list.limit,
            )
        return self.telegraph.get_page_list(
            access_token=self.access_token,
            offset=kwargs.get("offset", 0),
            limit=kwargs.get("limit", 50),
        )

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

    def get_views(self, *args, **kwargs) -> PageViews:
        if len(args) == 1 and isinstance(args[0], GetViews):
            views = args[0]
            return self.telegraph.get_views(
                path=views.path,
                year=views.year,
                month=views.month,
                day=views.day,
                hour=views.hour,
            )
        return self.telegraph.get_views(
            path=kwargs["path"],
            year=kwargs.get("year"),
            month=kwargs.get("month"),
            day=kwargs.get("day"),
            hour=kwargs.get("hour"),
        )

    model_config = {"arbitrary_types_allowed": True}


class AsyncAccount(BaseAccount):
    """
    Асинхронная обёртка аккаунта Telegraph. Автоматически подставляет access_token.
    Работает с асинхронным клиентом через AsyncTelegraphInterface.
    """

    telegraph: AsyncTelegraphInterface

    @model_validator(mode="after")
    def validate_access_token(self) -> AsyncAccount:
        if not self.access_token:
            raise ValueError(
                "access_token обязателен для использования методов аккаунта."
            )
        return self

    # --- Account Methods ---

    @overload
    async def edit_account(self, edit_account: EditAccount) -> BaseAccount: ...

    @overload
    async def edit_account(
        self,
        *,
        short_name: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
    ) -> BaseAccount: ...

    async def edit_account(self, *args, **kwargs) -> BaseAccount:
        if len(args) == 1 and isinstance(args[0], EditAccount):
            account = args[0]
            return await self.telegraph.edit_account(
                access_token=self.access_token,
                short_name=account.short_name,
                author_name=account.author_name,
                author_url=str(account.author_url) if account.author_url else None,
            )
        return await self.telegraph.edit_account(
            access_token=self.access_token,
            short_name=kwargs["short_name"],
            author_name=kwargs.get("author_name"),
            author_url=kwargs.get("author_url"),
        )

    @overload
    async def get_account_info(self, info: GetAccountInfo) -> BaseAccount: ...

    @overload
    async def get_account_info(
        self,
        *,
        fields: Optional[
            List[
                Literal[
                    "short_name", "author_name", "author_url", "auth_url", "page_count"
                ]
            ]
        ] = None,
    ) -> BaseAccount: ...

    async def get_account_info(self, *args, **kwargs) -> BaseAccount:
        if len(args) == 1 and isinstance(args[0], GetAccountInfo):
            info = args[0]
            return await self.telegraph.get_account_info(
                access_token=self.access_token,
                fields=info.fields,
            )
        return await self.telegraph.get_account_info(
            access_token=self.access_token,
            fields=kwargs.get("fields"),
        )

    async def revoke_access_token(self) -> BaseAccount:
        return await self.telegraph.revoke_access_token(access_token=self.access_token)

    # --- Page Methods ---

    @overload
    async def create_page(self, page: CreatePage) -> Page: ...

    @overload
    async def create_page(
        self,
        *,
        title: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    async def create_page(self, *args, **kwargs) -> Page:
        if len(args) == 1 and isinstance(args[0], CreatePage):
            page = args[0]
            return await self.telegraph.create_page(
                access_token=self.access_token,
                title=page.title,
                author_name=page.author_name or self.author_name,
                author_url=str(page.author_url)
                if page.author_url
                else None or self.author_url,
                content=page.content,
                html=page.html,
                return_content=page.return_content,
            )
        return await self.telegraph.create_page(
            access_token=self.access_token,
            title=kwargs["title"],
            author_name=kwargs.get("author_name", self.author_name),
            author_url=str(kwargs.get("author_url", self.author_url)),
            content=kwargs.get("content"),
            html=kwargs.get("html"),
            return_content=kwargs.get("return_content", False),
        )

    @overload
    async def edit_page(self, edit_page: EditPage) -> Page: ...

    @overload
    async def edit_page(
        self,
        *,
        title: str,
        path: str,
        author_name: Optional[str] = None,
        author_url: Optional[str] = None,
        content: Optional[List[Any]] = None,
        html: Optional[str] = None,
        return_content: bool = False,
    ) -> Page: ...

    async def edit_page(self, *args, **kwargs) -> Page:
        if len(args) == 1 and isinstance(args[0], EditPage):
            page = args[0]
            return await self.telegraph.edit_page(
                access_token=self.access_token,
                title=page.title,
                path=page.path,
                author_name=page.author_name or self.author_name,
                author_url=str(page.author_url)
                if page.author_url
                else None or self.author_url,
                content=page.content,
                html=page.html,
                return_content=page.return_content,
            )
        return await self.telegraph.edit_page(
            access_token=self.access_token,
            title=kwargs["title"],
            path=kwargs["path"],
            author_name=kwargs.get("author_name", self.author_name),
            author_url=kwargs.get("author_url", self.author_url),
            content=kwargs.get("content"),
            html=kwargs.get("html"),
            return_content=kwargs.get("return_content", False),
        )

    @overload
    async def get_page(self, get_page: GetPage) -> Page: ...

    @overload
    async def get_page(self, *, path: str, return_content: bool = False) -> Page: ...

    async def get_page(self, *args, **kwargs) -> Page:
        if len(args) == 1 and isinstance(args[0], GetPage):
            page = args[0]
            return await self.telegraph.get_page(
                path=page.path, return_content=page.return_content
            )
        return await self.telegraph.get_page(
            path=kwargs["path"],
            return_content=kwargs.get("return_content", False),
        )

    @overload
    async def get_page_list(self, get_page_list: GetPageList) -> PageList: ...

    @overload
    async def get_page_list(self, *, offset: int = 0, limit: int = 50) -> PageList: ...

    async def get_page_list(self, *args, **kwargs) -> PageList:
        if len(args) == 1 and isinstance(args[0], GetPageList):
            page_list = args[0]
            return await self.telegraph.get_page_list(
                access_token=self.access_token,
                offset=page_list.offset,
                limit=page_list.limit,
            )
        return await self.telegraph.get_page_list(
            access_token=self.access_token,
            offset=kwargs.get("offset", 0),
            limit=kwargs.get("limit", 50),
        )

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

    async def get_views(self, *args, **kwargs) -> PageViews:
        if len(args) == 1 and isinstance(args[0], GetViews):
            views = args[0]
            return await self.telegraph.get_views(
                path=views.path,
                year=views.year,
                month=views.month,
                day=views.day,
                hour=views.hour,
            )
        return await self.telegraph.get_views(
            path=kwargs["path"],
            year=kwargs.get("year"),
            month=kwargs.get("month"),
            day=kwargs.get("day"),
            hour=kwargs.get("hour"),
        )

    model_config = {"arbitrary_types_allowed": True}
