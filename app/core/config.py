from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Settings(BaseSettings):
    app_name: str = 'API'
    debug: bool = False
    db_user: str = "postgres"
    db_password: str = "development"
    db_name: str = "test.db"
    sgbd_driver: str = "sqlite"
    secret_key: str = "your_secret_key"

    @property
    def db_url(self) -> str:
        if self.sgbd_driver == "sqlite":
            return f"sqlite:///{self.db_name}"
        else:
            return f"{self.sgbd_driver}://{self.db_user}:{self.db_password}@localhost/{self.db_name}"
        
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()