from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from .database import Base


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, nullable=False, default=False, server_default="0")
    created_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.datetime("now")
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.datetime("now"),
        onupdate=func.datetime("now"),
    )
