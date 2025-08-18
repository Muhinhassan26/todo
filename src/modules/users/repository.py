from typing import Annotated

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from src.core.repository import BaseRepository
from src.modules.users.models import User


class UserRepository(BaseRepository[User]):
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db)]):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
