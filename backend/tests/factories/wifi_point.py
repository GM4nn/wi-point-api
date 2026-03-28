from unittest.mock import MagicMock
import factory


class WifiPointFactory(factory.Factory):

    class Meta:
        model = MagicMock

    id = factory.Sequence(lambda n: n + 1)
    original_id = factory.LazyAttribute(lambda o: f"WIFI-{o.id:04d}")
    program = "WiFi CDMX"
    town_hall = "Cuauhtémoc"
    lat = 19.4326
    ltg = -99.1332
    location = None
