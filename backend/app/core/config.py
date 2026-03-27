# pydantic settings
from pathlib import Path
from pydantic import computed_field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    POSTGRES_DB: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_SERVER: str
    POSTGRES_USER: str

    @computed_field
    @property
    def DATABASE_URI(self) -> str:
        return (
            f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}'
            f'@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'
        )

    _root: Path = Path(__file__).resolve().parents[3]
    model_config = {"env_file": [_root / ".env", _root / ".env.local"]}

settings: Settings = Settings()