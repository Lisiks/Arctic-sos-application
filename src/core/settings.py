from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    port: int

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_prefix="APP_",
        extra="ignore",
        env_file=".env"
    )


class Config:
    app: AppSettings = AppSettings()


config = Config()
