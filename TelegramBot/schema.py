from sqlalchemy import String, Text, ForeignKey, Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import Mapped

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    created_at = Column(DateTime, name="created_at", default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name_id!r}, context_id={self.context_id!r})"

class Context(Base):
    __tablename__ = "context"
    id: Mapped[int] = mapped_column(primary_key=True)
    context_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    context: Mapped[str] = mapped_column(Text)
    created_at = Column(DateTime, name="created_at", default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.current_timestamp())

    def __repr__(self) -> str:
        return f"Context(id={self.id!r}, context_id={self.context_id!r}, context={self.context!r})"

