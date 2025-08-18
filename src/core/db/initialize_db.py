import asyncio

from src.core.db.connection import Base, engine


async def create_all_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully.")


if __name__ == "__main__":
    asyncio.run(create_all_tables())
