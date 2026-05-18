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

    # Cloudflare R2
    CLOUDFLARE_R2_ENDPOINT_URL: str = ""
    CLOUDFLARE_R2_ACCESS_KEY_ID: str = ""
    CLOUDFLARE_R2_SECRET_ACCESS_KEY: str = ""
    CLOUDFLARE_R2_BUCKET_NAME: str = ""
    CLOUDFLARE_R2_PUBLIC_URL: str = ""
    CLOUDFLARE_R2_REGION: str = "auto"

    @property
    def db_url(self) -> str:
        if self.sgbd_driver == "sqlite":
            return f"sqlite:///{self.db_name}"
        else:
            return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    def time_now(self) -> datetime:
        return (
            datetime.now(ZoneInfo("UTC"))
            .astimezone(ZoneInfo("America/Sao_Paulo"))
            .replace(tzinfo=None)
        )

    @property
    def time_now_prop(self) -> datetime:
        return self.time_now()


settings = Settings()
