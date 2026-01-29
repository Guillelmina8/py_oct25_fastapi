from datetime import datetime

from sqlalchemy import ForeignKey, String, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db import Base


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(
        nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    owner: Mapped["User"] = relationship(back_populates="projects")

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="project",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("name", "owner_id", name="uq_project_name_per_owner"),
    )
