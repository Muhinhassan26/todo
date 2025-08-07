from typing import Annotated,List,Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from fastapi import Depends
from src.modules.todos.models import Todo
from sqlalchemy import select,delete,func
from src.modules.todos.schemas import TodoCreate,TodoUpdate
from src.core.base.repository import BaseRepository

class TodoRepository(BaseRepository[Todo]):
    def __init__(self,session: Annotated[AsyncSession, Depends(get_db)]):
        self.session=session
        super().__init__(Todo, session)
    
    async def get_all_by_user(self, user_id: int) -> List[Todo]:
        query = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all() 

    async def get_all_by_user_paginated(self,
                                        user_id:int,
                                        skip:int,
                                        limit:int=10,
                                        search: str | None = None,
                                        filter:str= 'all') -> List[Todo]:
        
        query = select(Todo).where(Todo.user_id == user_id)
        if search:
                query = query.where(Todo.title.ilike(f"%{search}%"))
        if filter == "completed":
            query = query.where(Todo.completed == True)
        elif filter == "not_completed":
            query = query.where(Todo.completed == False)

        query = query.order_by(Todo.created_at.desc()).offset(skip).limit(limit + 1)

        result = await self.session.execute(query)
        
        return result.scalars().all()
    

    async def count_by_user(self, 
                            user_id: int,
                            search: List[str]  = [],
                            filter:str='all',
                            ) -> int:
        query = select(func.count()).select_from(Todo).where(Todo.user_id == user_id)
       
        if search:
            for term in search:
                query = query.where(Todo.title.ilike(f"%{term}%"))

        if filter == "completed":
            query = query.where(Todo.completed == True)
        elif filter == "not_completed":
            query = query.where(Todo.completed == False)

        result = await self.session.execute(query)
        return result.scalar_one()
                                        
    
    async def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == todo_id, self.model.user_id == user_id)
        )
        return result.scalar_one_or_none()
    
    async def create(self, user_id: int, todo_data: TodoCreate) -> Todo:
        return await super().create({**todo_data.model_dump(), "user_id": user_id})

    
    async def update(self, todo_id: int, user_id: int, update_data: TodoUpdate) -> Optional[Todo]:
        todo = await self.get_by_id(todo_id, user_id)
        if not todo:
            return None

        return await super().update(todo.id, update_data.model_dump(exclude_unset=True))

    
    
    async def delete(self, todo_id: int, user_id: int) -> bool:
        todo = await self.get_by_id(todo_id, user_id)
        if not todo:
            return False
        return await super().delete(todo.id)