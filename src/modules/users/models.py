from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.models import BaseModel

if TYPE_CHECKING:
    from src.modules.todos.models import Todo


class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

    todos: Mapped[list["Todo"]] = relationship(back_populates="user")  # noqa: F821
