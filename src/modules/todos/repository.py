from typing import Annotated,List,Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import get_db
from fastapi import Depends
from src.modules.todos.models import Todo
from sqlalchemy import select
from src.modules.todos.schemas import TodoCreate,TodoUpdate
from src.core.base.repository import BaseRepository


 
    

class TodoRepository(BaseRepository[Todo]):
    def __init__(self,session: Annotated[AsyncSession, Depends(get_db)]):
        self.session=session
        super().__init__(Todo, session)
    
    # async def get_all_by_user(self, user_id: int) -> list[Todo]:
    #     return await self.filters(
    #         filters={"user_id": user_id},
    #     )



    # # async def get_all_by_user_paginated(self,
    # #                                     user_id:int,
    # #                                     skip:int,
    # #                                     limit:int=10,
    # #                                     search: str | None = None,
    # #                                     filter:str= 'all',
    # #                                     ) -> tuple[List[Todo],int]:
                                    
    # #     extra_conditions=[]

    # #     if filter == "completed":
    # #          extra_conditions.append(Todo.completed == True)
    # #     elif filter == "not_completed":
    # #         extra_conditions.append(Todo.completed == False)

    # #     page = (skip // limit) + 1

    # #     return await super().paginate_filters(
    # #         filters={"user_id": user_id},
    # #         search=search,
    # #         search_fields=["title"], 
    # #         page=page,
    # #         page_size=limit,
    # #         extra_conditions=extra_conditions,
    # #         order_by=Todo.created_at.desc()
    # #     )
                                        
    
    # async def get_by_id(self, todo_id: int, user_id: int) -> Optional[Todo]:
    #     result = await self.session.execute(
    #         select(self.model).where(self.model.id == todo_id, self.model.user_id == user_id)
    #     )
    #     return result.scalar_one_or_none()
    

    # async def create(self, user_id: int, todo_data: TodoCreate) -> Todo:
    #     todo = Todo(**todo_data.model_dump(), user_id=user_id)
    #     return await super().create(todo)
    
    # async def update(self, todo_id: int, user_id: int, update_data: TodoUpdate) -> Optional[Todo]:
    #     return await super().update(
    #         filters={"id": todo_id, "user_id": user_id},
    #         update_data=update_data.model_dump(exclude_unset=True)
    #     )

        
    
    # async def delete(self, todo_id: int, user_id: int) -> bool:
    #     todo = await self.get_by_id(todo_id, user_id)
    #     if not todo:
    #         return False
    #     return await super().delete(todo.id)