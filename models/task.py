from datetime import datetime

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Table,
    func, UniqueConstraint,
)
from sqlalchemy.orm import relationship, Mapped, mapped_column


from db import Base
from models.enums import TaskStatusEnum

task_assignees = Table(
    "task_assignees",
    Base.metadata,
    Column("task_id", ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        nullable=False
    )
    status: Mapped[TaskStatusEnum]
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )

    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE")
    )
    project: Mapped["Project"] = relationship(back_populates="tasks")

    assignees: Mapped[list["User"]] = relationship(
        secondary=task_assignees,
        back_populates="tasks"
    )

    __table_args__ = (
        UniqueConstraint("title", "project_id", name="uq_title_per_project"),
    )

