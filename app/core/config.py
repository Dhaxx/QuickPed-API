from pydantic_settings import BaseSettings, SettingsConfigDict
from zoneinfo import ZoneInfo
from datetime import datetime

class Settings(BaseSettings):
    app_name: str = "API"
    debug: bool = False
    db_host: str = "localhost"
    db_user: str = "postgres"
    db_password: str = "development"
    db_name: str = "test.db"
    sgbd_driver: str = "sqlite"
    secret_key: str = ""
    time_now: datetime = datetime.now(ZoneInfo("America/Sao_Paulo"))

    @property
    def db_url(self) -> str:
        if self.sgbd_driver == "sqlite":
            return f"sqlite:///{self.db_name}"
        else:
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
