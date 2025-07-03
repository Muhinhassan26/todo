
from src.modules.todos.repository import TodoRepository
from fastapi import Depends,HTTPException,status
from typing import Annotated,List
from src.modules.todos.models import Todo
from src.core.logger import logger
from src.modules.todos.schemas import TodoCreate,TodoUpdate



class TodoService:
    def __init__(self,todo_repo:Annotated[TodoRepository,Depends(TodoRepository)]):
        self.todo_repo=todo_repo

    

    async def get_user_todos(self, user_id: int) -> List[Todo]:
        todos = await self.todo_repo.get_all_by_user(user_id=user_id)
        return todos 

    
    async def get_user_todos_paginated(self,user_id:int,
                                       skip: int , 
                                       limit: int ) -> List[Todo]:
        todos= await self.todo_repo.get_all_by_user_paginated(user_id=user_id,
                                                              skip=skip, 
                                                              limit=limit+1)
        has_next=len(todos) > limit
        return todos[:limit],has_next

    async def count_user_todos(self, user_id: int) -> int:
        return await self.todo_repo.count_by_user(user_id)


    async def get_todo(self, todo_id: int, user_id: int) -> Todo:
        todo = await self.todo_repo.get_by_id(todo_id=todo_id, user_id=user_id)
        if not todo:
            logger.warning(f"Todo not found: todo_id={todo_id}, user_id={user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo

    
    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:
        todo = await self.todo_repo.create(user_id=user_id, todo_data=data)
        logger.info(f"Todo created: id={todo.id}, user_id={user_id}")
        return todo
    

    async def update_todo(self, todo_id: int, user_id: int, data: TodoUpdate) -> Todo:
        todo = await self.todo_repo.update(todo_id=todo_id, user_id=user_id, update_data=data)
        if not todo:
            logger.warning(f"Update failed: todo_id={todo_id}, user_id={user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        logger.info(f"Todo updated: id={todo_id}, user_id={user_id}")
        return todo

    
    async def delete_todo(self, todo_id: int, user_id: int) -> None:
        success = await self.todo_repo.delete(todo_id=todo_id, user_id=user_id)
        if not success:
            logger.warning(f"Delete failed: todo_id={todo_id}, user_id={user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        logger.info(f"Todo deleted: id={todo_id}, user_id={user_id}")
        