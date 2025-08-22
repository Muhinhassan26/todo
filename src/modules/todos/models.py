from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.models import BaseModel

if TYPE_CHECKING:
    from src.modules.users.models import User


class Todo(BaseModel):
    __tablename__ = "todos"

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    completed: Mapped[bool] = mapped_column(default=False, nullable=False)
    priority: Mapped[int] = mapped_column(Integer, nullable=False)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    user: Mapped["User"] = relationship(back_populates="todos")  # noqa: F821
