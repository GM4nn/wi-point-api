# other lib
from datetime import datetime
import pandas as pd
import dateparser

# scraper and loader
from app.seed.scraper import ScraperWiFiPoints
from app.seed.loader import WifiPointLoader

# providers
from app.src.providers.wifi_point_version import WifiPointVersionProvider

# db
from app.core.database import SessionLocal


class Seed():

    def __init__(self) -> None:
        self._wpv_provider: WifiPointVersionProvider = WifiPointVersionProvider(SessionLocal())

    def clean_date(self, raw_date: str) -> datetime | None:
        return dateparser.parse(raw_date)

    def run_seed(self) -> None:
        
        print("-> INITIALIZING SEED DATA FROM XLSX")

        scraper: ScraperWiFiPoints = ScraperWiFiPoints()

        # Get last update of file
        last_update: str | None = scraper.extract_last_update_date()
        clean_date: datetime | None = self.clean_date(last_update)
        print(f"--> LAST UPDATE OF DATA SET -> {clean_date}")

        # Get download url file
        url: str | None = scraper.extract_download_url()
        file_name: str = url.split("/")[-1]
        print(f"--> DATA SET URL -> {url}")

        # Get file
        file: bytes | None = scraper.get_file_from_url(url)

        if clean_date:

            wpv = self._wpv_provider.get()
            is_first_time: bool = wpv is None

            if is_first_time:
                wpv = self._wpv_provider.create(clean_date, file_name)

            elif clean_date > wpv.last_update:
                self._wpv_provider.update(file_name=file_name, last_update=clean_date)

            else:
                print("--> DATA IS UP TO DATE, SKIPPING...")
                return

            loader: WifiPointLoader = WifiPointLoader()
            dt: pd.DataFrame = loader.read_file(file)
            loader.load(dt)

if __name__ == "__main__":
    seed = Seed()
    seed.run_seed()
