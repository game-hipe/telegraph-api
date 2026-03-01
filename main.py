import asyncio

from telegraph_api import AsyncTelegraph

async def main():
    async with AsyncTelegraph() as client:
        account = await client.create_account(
            short_name="GH",
            author_name="GameHipe",
            author_url="https://github.com/game-hipe",
        )

        await account.create_page(
            title = "Hello World! Start Game!",
            html = "<p>Hello, world!</p>"
        )
        
asyncio.run(main())
