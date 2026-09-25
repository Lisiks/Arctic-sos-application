from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import computed_field

class AppSettings(BaseSettings):
    port: int

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="APP_",
        extra="ignore",
    )

class DBSettings(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    name: str

    @computed_field
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="DB_",
        extra="ignore",
    )


class Config:
    app: AppSettings = AppSettings()


config = Config()
