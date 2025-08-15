from typing import Generic, Type,Any,Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db import ModelType
from sqlalchemy import func,Select
from sqlalchemy.orm import joinedload,selectinload,RelationshipProperty
from src.core.db import operators_map
from src.core.schemas.common import FilterOptions 
from pydantic import BaseModel
from sqlalchemy import (
    JSON,
    Select,
    and_,
    cast,
    func,
    or_,
    select,
    update,
    delete,
)
from collections.abc import Callable

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: Callable[[], AsyncSession]):
        self.model = model
        self.session = session


    def _get_query(
        self,
        prefetch: tuple[str, ...] | None = None,
        options: list[Any] | None = None,
    ) -> Select[tuple[ModelType]]:
        

        query = select(self.model)

        if prefetch:
            if options is None:
                options = []
            for relation in prefetch:
                attr = getattr(self.model, relation)
                
                if hasattr(attr, "property") and isinstance(attr.property, RelationshipProperty):
                    if attr.property.uselist:
                        options.append(selectinload(attr))  
                    else:
                        options.append(joinedload(attr))  
            query = query.options(*options).execution_options(populate_existing=True)

        return query
    

    def _build_sorting(self, sorting: dict[str, str]) -> list[Any]:
        """Build list of ORDER_BY clauses."""
        result = []
        for field_name, direction in sorting.items():
            field = getattr(self.model, field_name)
            result.append(getattr(field, direction)())
        return result
    

    def _build_filters(self, filters: dict[str, Any]) -> list[Any]:
        """Build list of WHERE conditions."""
        result = []
        for expression, value in filters.items():
            parts = expression.split("__")
            op_name = parts[1] if len(parts) > 1 else "exact"
            if op_name not in operators_map:
                msg = f"Expression {expression} has incorrect operator {op_name}"
                raise KeyError(msg)
            operator = operators_map[op_name]
            column = getattr(self.model, parts[0])
            result.append(operator(column, value))
        return result
    

    async def get_by_id(self,
                        obj_id: int,
                        filter_options:FilterOptions,
                        ) -> ModelType | None:
        query = self._get_query(prefetch=filter_options.prefetch).where(self.model.id == obj_id)

        async with self.session as session:
            result=await session.execute(query)
            return result.scalars().first()
        

    async def list_all(self,
                      filter_options:FilterOptions,
                      ) -> list[ModelType]:
        
        query= self._get_query(filter_options.prefetch)

        if filter_options.sorting is not None:
            query=query.order_by(*self._build_sorting(sorting=filter_options.sorting))

        async with self.session as session:
            result=await session.execute(query)
            return result.scalars().all()
        

    async def get_by_filed(self,
                           filter_options:FilterOptions,
                           )  -> ModelType | None:

        query = self._get_query(prefetch=filter_options.prefetch)

        if filter_options.distinct_on:
            query = query.distinct(getattr(self.model, filter_options.distinct_on))

        if filter_options.sorting is not None:
            query = query.order_by(*self._build_sorting(filter_options.sorting))

        or_conditions = []
        and_conditions = []

        filters=self._build_filters(filter_options.filters)

        for filter_expr in filters:
            if hasattr(filter_expr, "left") and hasattr(filter_expr.left, "key"):
                if (
                    filter_options.or_filters is not None
                    and filter_expr.left.key in filter_options.or_filters
                ):
                    or_conditions.append(filter_expr)
                else:
                    and_conditions.append(filter_expr)

        final_condition = None
        if and_conditions or or_conditions:
            combined_conditions = []
            if and_conditions:
                combined_conditions.append(and_(*and_conditions))
            if or_conditions:
                combined_conditions.append(or_(*or_conditions))
            final_condition = and_(*combined_conditions) if combined_conditions else None
        async with self.session as session:
            db_execute = await session.execute(query.where(final_condition))  # type: ignore
            return db_execute.scalars().first()


    # async def filters(self,
    #                   filters: dict[str, Any],
    #                   prefetch:tuple[str,...]|None=None,) -> list[ModelType]:
 
    #     query = self._get_query(prefetch=prefetch)
    #     for field, value in filters.items():
    #         query = query.where(getattr(self.model, field) == value)

    #     result = await self.session.execute(query)
    #     return result.scalars().all()
    

    async def filter(
        self,
        filter_options: FilterOptions,  # same object you pass to get_field
    ) -> list[ModelType]:
        async with self.session as session:
            query = self._get_query(prefetch=filter_options.prefetch)

            if filter_options.distinct_on:
                query = query.distinct(getattr(self.model, filter_options.distinct_on))
            if filter_options.sorting is not None:
                query = query.order_by(*self._build_sorting(filter_options.sorting))

            
            filters = self._build_filters(filter_options.filters)

            or_conditions = []
            and_conditions = []

            for filter_expr in filters:
                if hasattr(filter_expr, "left") and hasattr(filter_expr.left, "key"):
                    if (
                        filter_options.or_filters is not None
                        and filter_expr.left.key in filter_options.or_filters
                    ):
                        or_conditions.append(filter_expr)
                    else:
                        and_conditions.append(filter_expr)
            final_condition = None
            if and_conditions or or_conditions:
                combined_conditions = []
                if and_conditions:
                    combined_conditions.append(and_(*and_conditions))
                if or_conditions:
                    combined_conditions.append(or_(*or_conditions))
                final_condition = and_(*combined_conditions) if combined_conditions else None

            if final_condition is not None:
                query = query.where(final_condition)

            result = await session.execute(query)
            return result.scalars().all()



    async def paginate_filters(self,
                               filter_options:FilterOptions,
                               ) -> tuple[Sequence[ModelType] , int]:

        query = self._get_query(prefetch=filter_options.prefetch)

        if filter_options.sorting is not None:
            query = query.order_by(*self._build_sorting(filter_options.sorting))
        
        filters = self._build_filters(filter_options.filters)


        or_conditions = []
        and_conditions = []
        search_conditions = []

        search_fields = filter_options.search_fields

        if filter_options.pagination and filter_options.pagination.search and search_fields:
            search_value = filter_options.pagination.search.strip()
            for field in search_fields:
                search_conditions.append(getattr(self.model, field).ilike(f"%{search_value}%"))

        for filter_expr in filters:
            if hasattr(filter_expr, "left") and hasattr(filter_expr.left, "key"):
                if (
                    filter_options.or_filters is not None
                    and filter_expr.left.key in filter_options.or_filters
                ):
                    or_conditions.append(filter_expr)
                else:
                    and_conditions.append(filter_expr)

        final_condition = None
        if and_conditions or or_conditions or search_conditions:
            combined_conditions = []
            if and_conditions:
                combined_conditions.append(and_(*and_conditions))
            if or_conditions:
                combined_conditions.append(or_(*or_conditions))
            if search_conditions:
                combined_conditions.append(or_(*search_conditions))

            final_condition = and_(*combined_conditions) if combined_conditions else None

        async with self.session as session:

            total_query = select(func.count()).select_from(self.model)
            if final_condition is not None:
                total_query = total_query.where(final_condition)
            total = await session.scalar(total_query) or 0

            if filter_options.pagination:
                query = query.offset(filter_options.pagination.skip).limit(
                    filter_options.pagination.page_size
                )

            if final_condition is not None:
                query = query.where(final_condition)
            db_execute = await session.execute(query)
            result = db_execute.scalars().all()
        
        return  result, total
        

        # for field, value in filters.items():
        #     query = query.where(getattr(self.model, field) == value)
        
        # if search and search_fields:
        #     search_conditions = [
        #         getattr(self.model, field).ilike(f"%{search}%")
        #         for field in search_fields
        #     ]
        #     query = query.where(or_(*search_conditions))

        # if extra_conditions:
        #     for cond in extra_conditions:
        #         query = query.where(cond)

        # count_query = select(func.count()).select_from(query.subquery())
        # total_count = (await self.session.execute(count_query)).scalar_one()
        
        # if order_by is not None:
        #     query = query.order_by(order_by)

        # query = query.offset((page - 1) * page_size).limit(page_size)
        # result = await self.session.execute(query)
        # items = result.scalars().all()

        # return items, total_count


    async def create(self, obj: ModelType) -> ModelType:
        async with self.session as session:
            session.add(obj)
            await session.commit()
            await session.refresh(obj)
        return obj


    async def update(self,
                     filter_options:FilterOptions,
                     values:ModelType,
                     
                     ) -> ModelType | None:
        async with self.session as session:

            filters = self._build_filters(filter_options.filters)
            update_values = values.model_dump(exclude_unset=True)

            for key, value in list(update_values.items()):
                if isinstance(value, dict) and isinstance(getattr(self.model, key).type, JSON):
                    update_values[key] = cast(getattr(self.model, key), JSON).concat(
                        cast(value, JSON)
                    )

            query = (
            update(self.model)
            .where(and_(*filters))
            .values(**update_values)
            )

            result = await session.execute(query)
            await session.commit()
            return result.rowcount
        

    async def create_and_update(self,
                                filter_options:FilterOptions,
                                values:BaseModel,
                                )-> ModelType:
        
        async with self.session as session:

            filters = self._build_filters(filter_options.filters)
            update_values = values.model_dump(exclude_unset=True)

            for key, value in list(update_values.items()):
                if isinstance(value, dict) and isinstance(getattr(self.model, key).type, JSON):
                    update_values[key] = cast(getattr(self.model, key), JSON).concat(
                        cast(value, JSON)
                    )
            
            query = select(self.model).where(and_(*filters))
            existing_obj = await session.execute(query)
            existing_obj = existing_obj.scalars().first()

            if existing_obj:
                for key, value in update_values.items():
                    setattr(existing_obj, key, value)
                session.add(existing_obj)
                await session.commit()
                await session.refresh(existing_obj)
                return existing_obj
            
            new_obj = self.model(**update_values)
            session.add(new_obj)
            await session.commit()
            await session.refresh(new_obj)
            return new_obj

        # """Fetch object by ID and update with given fields."""
        # query = self._get_query(prefetch=prefetch)
        # for field, value in filters.items():
        #     query = query.where(getattr(self.model, field) == value)
        # result = await self.session.execute(query)
        # obj = result.scalar_one_or_none()
        
        # if not obj:
        #     return None

        # for key, value in update_data.items():
        #     setattr(obj, key, value)

        # await self.session.flush()
        # await self.session.commit()
        # await self.session.refresh(obj)
        # return obj

    # async def delete(self, id_: int) -> bool:
    #     """Delete by ID and return success status."""
    #     result = await self.session.execute(
    #         delete(self.model).where(self.model.id == id_)
    #     )
    #     await self.session.commit()
    #     return result.rowcount > 0
    


    async def delete(
        self, filter_options: FilterOptions
    ) -> int:
        """
        Delete rows matching the given filter options.
        Returns the number of deleted rows.
        """
        async with self.session as session:
            filters = self._build_filters(filter_options.filters)

            query = delete(self.model).where(and_(*filters))
            result = await session.execute(query)
            await session.commit()

            return result.rowcount  # Number of rows deleted