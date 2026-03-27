# other lib
from datetime import datetime

# sqlalchemy
from sqlalchemy.orm import Session

# models
from app.src.models.wifi_point_version import WifiPointVersion


class WifiPointVersionProvider:

    def __init__(self, db_session: Session) -> None:
        self._db_session: Session = db_session

    def get(self) -> WifiPointVersion | None:
        return self._db_session.query(WifiPointVersion).first()

    def create(
        self,
        last_update: datetime,
        file_name: str,
        version: int = 1,
    ) -> WifiPointVersion | None:

        wpv = WifiPointVersion(
            version=version,
            last_update=last_update,
            file_name=file_name,
        )

        self._db_session.add(wpv)
        self._db_session.commit()
        self._db_session.refresh(wpv)

        return wpv
