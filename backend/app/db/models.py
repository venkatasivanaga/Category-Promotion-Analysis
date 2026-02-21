# add these imports if not present
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text, ForeignKey
from sqlalchemy.orm import relationship
import json

# inside class Run(Base):
file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)

from app.db.session import Base

class Run(Base):
    __tablename__ = "runs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    status: Mapped[str] = mapped_column(String(20), default="created", nullable=False)
    file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    original_filename: Mapped[str | None] = mapped_column(String(255), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    

# inside Run class
# result = relationship("RunResult", uselist=False, back_populates="run")  # optional

class RunResult(Base):
    __tablename__ = "run_results"

    run_id: Mapped[str] = mapped_column(String(36), ForeignKey("runs.id"), primary_key=True)
    summary_json: Mapped[str] = mapped_column(Text, nullable=False)  # store JSON as text

    created_at: Mapped[str] = mapped_column(DateTime(timezone=True), server_default=func.now())

    run = relationship("Run")