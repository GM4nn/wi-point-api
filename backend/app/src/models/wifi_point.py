# sqlalchemy
from sqlalchemy import Index, String, Float
from sqlalchemy.orm import Mapped, mapped_column

# geoalchemy
from geoalchemy2 import Geography

# app
from app.core.base import Base


class WifiPoint(Base):

    __tablename__ = "wifi_points"

    original_id: Mapped[str | None] = mapped_column(String(50), nullable=True)
    program: Mapped[str | None] = mapped_column(String(255), nullable=True)
    town_hall: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    lat: Mapped[float] = mapped_column(Float, nullable=False)
    ltg: Mapped[float] = mapped_column(Float, nullable=False)

    # PostGIS column for geospatial queries (SRID 4326 = WGS84)
    # SRID = Spatial Reference ID,
    # 4326 = the WGS84 system code
    location: Mapped[str | None] = mapped_column(
        Geography(geometry_type="POINT", srid=4326),
        nullable=True,
    )

    __table_args__ = (
        Index("ix_wifi_points_location", "location", postgresql_using="gist"),
    )
