from typing import Generic, Type, Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,delete
from src.core.db import ModelType





class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, id_: int) -> Optional[ModelType]:
        result = await self.session.execute(
            select(self.model).where(self.model.id == id_)
        )
        return result.scalar_one_or_none()

    async def list_all(self) -> List[ModelType]:
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def create(self, data: dict) -> ModelType:
        """Accepts a dictionary and creates an instance of the model."""
        instance = self.model(**data)
        self.session.add(instance)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, id_: int, update_data: dict) -> Optional[ModelType]:
        """Fetch object by ID and update with given fields."""
        obj = await self.get_by_id(id_)
        if not obj:
            return None

        for key, value in update_data.items():
            setattr(obj, key, value)

        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def delete(self, id_: int) -> bool:
        """Delete by ID and return success status."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id_)
        )
        await self.session.commit()
        return result.rowcount > 0