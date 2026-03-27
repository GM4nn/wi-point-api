from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import text

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
import pandas as pd
from io import BytesIO

from app.src.models import WifiPoint

class WifiPointLoader:

    COLUMN_MAP: dict[str, str] = {
        "id": "original_id",
        "programa": "program",
        "alcaldia": "town_hall",
        "latitud": "lat",
        "longitud": "ltg",
    }

    def read_file(self, file_in_bytes: bytes) -> pd.DataFrame:
        df: pd.DataFrame = pd.read_excel(BytesIO(file_in_bytes))
        df = self._clean_data(df)
        return df

    def _clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        for col in ["latitud", "longitud"]:
            df[col] = df[col].apply(
                lambda v: float(
                    "".join(
                        c for c in str(v) 
                        if c.isdigit() 
                        or c in ".-"
                    ) or "0"
                )
            )
        return df


    def insert_batch(self, batch: pd.DataFrame, batch_num: int, total_batches: int) -> int:

        print(f"-- INSERTING BATCH {batch_num}/{total_batches}... --")

        db_session: Session = SessionLocal()

        try:
            valid_columns: list[str] = list(self.COLUMN_MAP.values())
            batch = batch.rename(columns=self.COLUMN_MAP)[valid_columns]
            data: list[dict] = batch.to_dict("records")

            stmt = insert(WifiPoint).values(data)
            stmt = stmt.on_conflict_do_update(
                index_elements=[WifiPoint.original_id],
                set_={
                    "program": stmt.excluded.program,
                    "town_hall": stmt.excluded.town_hall,
                    "lat": stmt.excluded.lat,
                    "ltg": stmt.excluded.ltg,
                }
            )

            db_session.execute(stmt)
            db_session.commit()
        except Exception as e:
            print(f"Error when insert batch {batch_num}: {type(e).__name__}: {e.args[0][:200] if e.args else 'unknown'}")
            db_session.rollback()

        finally:
            db_session.close()

    def _update_locations(self) -> None:

        print("-- UPDATING LOCATIONS... --")

        db_session: Session = SessionLocal()

        try:
            db_session.execute(
                text(
                    "UPDATE wifi_points "
                    "SET location = ST_SetSRID(ST_MakePoint(ltg, lat), 4326)::geography "
                    "WHERE location IS NULL AND lat != 0 AND ltg != 0"
                )
            )
            db_session.commit()
        finally:
            db_session.close()

    def load(self, data_in_dataframe: pd.DataFrame) -> None:

        max_batches: int = 5
        batch_size: int = 1000

        # Create list of batches
        # example -> [ 1batch(with 1000 elemtens), 2batch, 3batch, .. ]
        batches: list[pd.DataFrame] = [
            data_in_dataframe.iloc[i: i + batch_size]
            for i in range(0, len(data_in_dataframe), batch_size)
        ]
    
        with ThreadPoolExecutor(max_workers=max_batches) as executor:
            futures: list[Future] = [
                executor.submit(self.insert_batch, batch, batch_num, len(batches)) 
                for batch_num, batch in enumerate(batches)
            ]

            # to await all futures
            for future in as_completed(futures):
                future.result()

        self._update_locations()

