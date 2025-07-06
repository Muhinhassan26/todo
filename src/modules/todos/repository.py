from typing import Annotated,List,Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from fastapi import Depends
from src.modules.todos.models import Todo
from sqlalchemy import select,delete,func
from src.modules.todos.schemas import TodoCreate,TodoUpdate

class TodoRepository:
    def __init__(self,session: Annotated[AsyncSession, Depends(get_db)]):
        self.session=session

    
    async def get_all_by_user(self, user_id: int) -> List[Todo]:
        query = select(Todo).where(Todo.user_id == user_id).order_by(Todo.created_at.desc())
        result = await self.session.execute(query)
        return result.scalars().all() 

    async def get_all_by_user_paginated(self,
                                        user_id:int,
                                        skip:int,
                                        limit:int=10,
                                        search: str | None = None,) -> List[Todo]:
        
        print(search, '----------------')
        query = select(Todo).where(Todo.user_id == user_id)
        if search:
            query = query.where(Todo.title.ilike(f"%{search}%"))

        query = query.order_by(Todo.created_at.desc()).offset(skip).limit(limit + 1)

        result = await self.session.execute(query)
        
        return result.scalars().all()

    async def count_by_user(self, user_id: int, search: str | None = None) -> int:
        query = select(func.count()).select_from(Todo).where(Todo.user_id == user_id)
        if search:
            query = query.where(Todo.title.ilike(f"%{search}%"))
        result = await self.session.execute(query)
        return result.scalar_one()
                                        
    
    async def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
        query= select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()
    
    async def create(self, user_id: int, todo_data: TodoCreate) -> Todo:
        new_todo = Todo(**todo_data.model_dump(), user_id=user_id)
        self.session.add(new_todo)
        await self.session.flush()  
        await self.session.commit()
        await self.session.refresh(new_todo)
        return new_todo
    
    async def update(self, todo_id: int, user_id: int, update_data: TodoUpdate) -> Optional[Todo]:
        query = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        result = await self.session.execute(query)
        todo = result.scalars().first()

        if not todo:
            return None

        for field, value in update_data.model_dump(exclude_unset=True).items():
            setattr(todo, field, value)

        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(todo)
        return todo
    
    
    async def delete(self, todo_id: int, user_id: int) -> bool:
        query= delete(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
        result = await self.session.execute(query)
        await self.session.commit()
        return result.rowcount > 0