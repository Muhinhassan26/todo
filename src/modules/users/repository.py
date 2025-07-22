from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from src.core.db import get_db
from src.modules.users.models import User
from sqlalchemy import select



class UserRepository:
    def __init__(self, session: Annotated[AsyncSession, Depends(get_db)]):
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        
        result=await self.session.execute(
            select(User).where(user_id==User.id)
        )

        return result.scalar_one_or_none()
    

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()   
    
    
    async def create(self, user_data: User) -> User:
        
        self.session.add(user_data)
        await self.session.commit()
        await self.session.refresh(user_data)
        return user_data
    
    async def list_all(self) -> list[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()
    
    async def delete(self, user_id: int) -> None:
        user = await self.get_by_id(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()