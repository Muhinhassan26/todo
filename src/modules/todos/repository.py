from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base.repository import BaseRepository
from src.core.db import get_db
from src.modules.todos.models import Todo


class TodoRepository(BaseRepository[Todo]):
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db)]):
        self.session = session
        super().__init__(Todo, session)
