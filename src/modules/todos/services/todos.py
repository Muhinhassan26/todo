from src.modules.todos.repository import TodoRepository
from fastapi import Depends,HTTPException,status
from typing import Annotated,Sequence
from src.modules.todos.models import Todo
from src.core.logger import logger
from src.modules.todos.schemas import TodoCreate,TodoUpdate
from src.core.schemas.common import FilterOptions,QueryParams
from src.core.error.exceptions import NotFoundException



class TodoService:
    def __init__(self,todo_repo:Annotated[TodoRepository,Depends(TodoRepository)]):
        self.todo_repo=todo_repo

    

    async def get_user_todos(self, user_id: int) -> list[Todo]:
        todos = await self.todo_repo.filter(
        filter_options=FilterOptions(
            filters={"user_id": user_id},
            prefetch=("user",),
            )
            )
        return todos
        
    async def get_user_todos_paginated(self,
                                       search_fields:list[str]|None,
                                       user_id:int,
                                       page: int=1 , 
                                       page_size: int=10 ,
                                       search: str|None=None,
                                       filter_by:str="all",
                                       ) -> tuple[Sequence[Todo], int]:
        filters={"user_id":user_id}


        if filter_by == "completed":
            filters["completed"] = True
        elif filter_by == "not_completed":
            filters["completed"] = False
        
        pagination=QueryParams(page=page,
                               page_size=page_size,
                               search=search,
                            )
        
        filter_options = FilterOptions(
            filters=filters,     
            pagination=pagination,
            prefetch=("user",),
            search_fields=search_fields,              
        )
        
        todos, total = await self.todo_repo.paginate_filters(
            filter_options=filter_options    
            )
        return todos,total
        
        # todos,total_count= await self.todo_repo.get_all_by_user_paginated(
        #                                                       user_id=user_id,
        #                                                       skip=skip, 
        #                                                       limit=limit,
        #                                                       search=search,
        #                                                       filter=filter,
        #                                                       )
        # has_next=skip + limit < total_count
        # return todos,has_next,total_count

    # async def count_user_todos(self, user_id: int,search: str|None=None,filter:str='all') -> int:
    #     return await self.todo_repo.count_by_user(user_id,search=search,filter=filter)


    async def get_todo(self, todo_id: int, user_id: int) -> Todo:

        todo = await self.todo_repo.get_by_filed(obj_id=todo_id,
                                              filter_options=FilterOptions(
                                                  filters={'id':todo_id,
                                                      "user_id":user_id},
                                                  prefetch=('user'))
           )
        if not todo:
            logger.warning(f"Todo not found: todo_id={todo_id}, user_id={user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo

    
    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:

      
        todo=await self.todo_repo.create(obj=Todo(
            user_id=user_id,
            **data.model_dump()
        ))
        logger.info(f"Todo created: id={todo.id}, user_id={user_id}")
        return todo
    
    

    async def update_todo(self, todo_id: int, user_id: int, data: TodoUpdate) -> None:

        filters = FilterOptions(filters={
            "id": todo_id,
            "user_id": user_id
        })

        update_data = TodoUpdate(
        **data.model_dump()
    )
        updated_count = await self.todo_repo.update(
            filter_options=filters,
            values=update_data
        )

        if updated_count == 0:
            logger.warning(f"Todo with id {todo_id} is not available for user with user id {user_id}")
            raise NotFoundException()
        
        logger.info(f"Todo updated: id={todo_id}, user_id={user_id}")

        # todo = await self.todo_repo.update(todo_id=todo_id, user_id=user_id, update_data=data)
        # if not todo:
        #     logger.warning(f"Update failed: todo_id={todo_id}, user_id={user_id}")
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        # logger.info(f"Todo updated: id={todo_id}, user_id={user_id}")
        # return todo

    
    # async def delete_todo(self, todo_id: int, user_id: int) -> None:
    #     success = await self.todo_repo.delete(todo_id=todo_id, user_id=user_id)
    #     if not success:
    #         logger.warning(f"Delete failed: todo_id={todo_id}, user_id={user_id}")
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    #     logger.info(f"Todo deleted: id={todo_id}, user_id={user_id}")


    async def delete_todo(self, user_id: int, todo_id: int) -> None:
        """
        Delete a todo for a specific user.
        Raises NotFoundException if no matching todo exists.
        """
        filters = FilterOptions(filters={
            "id": todo_id,
            "user_id": user_id
        })

        deleted_count = await self.todo_repo.delete(filter_options=filters)

        if deleted_count == 0:
            logger.warning(f"Delete failed: todo_id={todo_id}, user_id={user_id}")
            raise NotFoundException(f"Todo with id {todo_id} not found for user {user_id}")
        
        logger.info(f"Todo deleted: id={todo_id}, user_id={user_id}")