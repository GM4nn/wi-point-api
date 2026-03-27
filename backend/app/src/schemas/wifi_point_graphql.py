from __future__ import annotations

import strawberry

from app.src.models import WifiPoint


@strawberry.type
class WifiPointGraphQL:
    id: int
    original_id: str | None
    programa: str | None
    alcaldia: str
    latitud: float
    longitud: float

    @classmethod
    def from_instance(cls, instance: WifiPoint) -> WifiPointGraphQL:
        return cls(
            id=instance.id,
            original_id=instance.original_id,
            programa=instance.program,
            alcaldia=instance.town_hall,
            latitud=instance.lat,
            longitud=instance.ltg,
        )
