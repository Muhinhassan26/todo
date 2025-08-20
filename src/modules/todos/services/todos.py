from collections.abc import Sequence
from typing import Annotated

from fastapi import Depends, HTTPException, status
from src.core.error.exceptions import NotFoundException
from src.core.logger import logger
from src.core.schemas.common import FilterOptions, PaginatedResponse, QueryParams
from src.core.service import BaseService
from src.modules.todos.models import Todo
from src.modules.todos.repository import TodoRepository
from src.modules.todos.schemas import TodoCreate, TodoResponse, TodoUpdate


class TodoService(BaseService):
    def __init__(self, todo_repo: Annotated[TodoRepository, Depends(TodoRepository)]):
        self.todo_repo = todo_repo

    async def get_user_todos(self, user_id: int) -> Sequence[Todo]:
        return await self.todo_repo.filter(
            filter_options=FilterOptions(
                filters={"user_id": user_id},
                prefetch=("user",),
            )
        )

    async def get_user_todos_paginated(
        self, user_id: int, query_params: QueryParams
    ) -> PaginatedResponse[TodoResponse]:
        filters = {"user_id": user_id}

        if query_params.filter_params:
            filters.update(query_params.filter_params)

        filter_options = FilterOptions(
            filters=filters,
            pagination=query_params,
            prefetch=("user",),
            search_fields=[
                "title",
                "description",
            ],
        )

        data, total = await self.todo_repo.paginate_filters(filter_options=filter_options)

        return PaginatedResponse(
            data=data,
            meta=await self.setup_pagination_meta(
                total=total,
                page_size=query_params.page_size,
                page=query_params.page,
            ),
        )

    async def get_todo(self, todo_id: int, user_id: int) -> Todo:
        todo = await self.todo_repo.get_by_filed(
            filter_options=FilterOptions(
                filters={"id": todo_id, "user_id": user_id}, prefetch=("user")
            ),
        )
        if not todo:
            logger.warning(f"Todo not found: todo_id={todo_id}, user_id={user_id}")
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
        return todo

    async def create_todo(self, user_id: int, data: TodoCreate) -> Todo:
        todo = await self.todo_repo.create(obj=Todo(user_id=user_id, **data.model_dump()))
        logger.info(f"Todo created: id={todo.id}, user_id={user_id}")
        return todo

    async def update_todo(self, todo_id: int, user_id: int, data: TodoUpdate) -> None:
        filters = {"id": todo_id, "user_id": user_id}

        updated_count = await self.todo_repo.update_obj(
            where=filters, values=data.model_dump(exclude=None)
        )

        if updated_count == 0:
            logger.warning(
                f"Todo with id {todo_id} is not available for user with user id {user_id}"
            )
            raise NotFoundException()

        logger.info(f"Todo updated: id={todo_id}, user_id={user_id}")

    async def delete_todo(self, user_id: int, todo_id: int) -> None:
        filters = FilterOptions(filters={"id": todo_id, "user_id": user_id})

        deleted_count = await self.todo_repo.delete(filter_options=filters)

        if deleted_count == 0:
            logger.warning(f"Delete failed: todo_id={todo_id}, user_id={user_id}")
            raise NotFoundException(f"Todo with id {todo_id} not found for user {user_id}")

        logger.info(f"Todo deleted: id={todo_id}, user_id={user_id}")
