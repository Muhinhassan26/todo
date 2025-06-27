from datetime import datetime
from src.core.db import Base
from sqlalchemy.sql import func
from sqlalchemy import DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column

class BaseModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(
        primary_key=True, 
        autoincrement=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )