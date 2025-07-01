from src.core.db.connection import engine, Base
import asyncio
from src.modules.users.models import User
from src.modules.todos.models import Todo

async def create_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ All tables created successfully.")

if __name__ == "__main__":
    asyncio.run(create_all_tables())