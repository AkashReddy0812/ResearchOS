from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, String, Float, Integer, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Job(Base):
    __tablename__ = "jobs"

    job_id: Mapped[str] = mapped_column(String(36), primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    query: Mapped[str] = mapped_column(String(1000))
    status: Mapped[str] = mapped_column(String(20), default="queued")
    current_node: Mapped[str | None] = mapped_column(String(50), nullable=True)
    iteration_count: Mapped[int] = mapped_column(Integer, default=0)
    sufficiency_score: Mapped[float] = mapped_column(Float, default=0.0)
    coverage_metrics: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    result_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str | None] = mapped_column(String(1000), nullable=True)
