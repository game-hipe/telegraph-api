import asyncio

from datetime import datetime

from telegraph_api.client._client import AsyncTelegraph


async def main():
    async with AsyncTelegraph() as client:
        account = await client.create_account(short_name="test", author_name="test")
        page = await client.create_page(
            access_token=account.access_token,
            title="Test-Bot",
            html="<p>Hello, world!</p>",
        )
        print(page.url)

        await client.edit_account(
            access_token=account.access_token,
            short_name="test",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe",
        )

        page = await client.edit_page(
            access_token=account.access_token,
            path=page.path,
            title="Test-Edit!",
            html="<p>Hello, world! Again!</p>",
        )

        print(page)

        author = await client.get_account_info(
            access_token=account.access_token, fields=["author_name"]
        )
        print(author)

        print(await client.get_page(path=page.path, return_content=True))

        print(await client.get_page_list(access_token=account.access_token))

        print(
            await client.get_views(
                path=page.path,
                year=datetime.now().year,
                month=datetime.now().month,
                day=datetime.now().day,
            )
        )

        print(await client.revoke_access_token(access_token=account.access_token))


asyncio.run(main())
