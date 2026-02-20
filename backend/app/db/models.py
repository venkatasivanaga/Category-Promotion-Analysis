# add these imports if not present
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

# inside class Run(Base):
file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)

from app.db.session import Base

class Run(Base):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="created", nullable=False)

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[str] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )