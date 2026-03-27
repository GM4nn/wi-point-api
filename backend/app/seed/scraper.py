from bs4.element import NavigableString
import requests
from bs4 import BeautifulSoup


class ScraperWiFiPoints:

    url: str = "https://datos.cdmx.gob.mx/dataset/puntos-de-acceso-wifi-en-la-cdmx"
    text_to_search: str = "Última actualización"

    def __init__(self) -> None:
        self.html: str = self.get_html()

    def get_file_from_url(self, url: str) -> bytes | None:

        try:
            response: requests.Response = requests.get(
                url,
                timeout=30
            )
            response.raise_for_status()
        except requests.RequestException:
            return None

        return response.content

    def get_html(self) -> str | None:

        try:
            response: requests.Response = requests.get(
                self.url,
                timeout=30
            )
            response.raise_for_status()
        except requests.RequestException:
            return None

        return response.text

    def extract_last_update_date(self) -> str | None:

        soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

        tag: NavigableString = soup.find(
            string=lambda text: text 
            and self.text_to_search 
            in text
        )

        if not tag:
            return None

        raw: str = tag.parent.parent.get_text(" ", strip=True)
        date_str: str = raw.replace(self.text_to_search, "").strip()
        
        return date_str

    def extract_download_url(self) -> str | None:

        soup: BeautifulSoup = BeautifulSoup(self.html, "html.parser")

        tag: NavigableString = soup.find(
            "a",
            string=lambda text: text and "descargar" in text.lower()
        )

        return tag["href"] if tag else None