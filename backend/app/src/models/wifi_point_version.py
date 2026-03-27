# sqlalchemy
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, DateTime

# app
from app.core.base import Base


class WifiPointVersion(Base):

    __tablename__ = "wifi_points_version"

    version: Mapped[int] = mapped_column(Integer, nullable=False)
    last_update: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    file_name: Mapped[str] = mapped_column(String(255), nullable=True)
