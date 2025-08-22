import asyncio
from typing import Any

from src.core.db.connection import Base, engine
from src.modules.todos.models import Todo  # noqa: F401
from src.modules.users.models import User  # noqa: F401


async def create_all_tables() -> Any:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully.")
    return


if __name__ == "__main__":
    asyncio.run(create_all_tables())
