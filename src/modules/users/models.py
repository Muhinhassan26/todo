from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from src.core.models import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, unique=True, nullable=False)

