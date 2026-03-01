# TelegrapAPI - Асинхронная и синхронная версия
В чём суть проекта? Да в мире существуют 100-1000 API под Telegraph, но я просто захотел, почему бы и нет?

## Features (Особенности)
1. Синхронный и Асинхронный режим.
2. Поддержка Pydantic.
3. Более приятный DX, работа как с ORM

## How to Download (Как скачать?)
```bash
pip install "git+https://github.com/game-hipe/telegraph-api.git" # Вуаля!
```

## Example (Примеры)
```python
from telegraph_api import Telegraph

with Telegraph() as client:
    account = client.create_account(
        short_name="GH",
        author_name="GameHipe",
        author_url="https://github.com/game-hipe",
    )

    page = account.create_page(
        title = "Hello World! Start Game!",
        html = "<p>Hello, world!</p>"
    )

    print(page)
```

## AsyncExample (Примеры)
```python
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
```

Ебашьте!
