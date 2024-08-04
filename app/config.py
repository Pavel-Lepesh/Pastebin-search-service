from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ES_HOST: str
    ES_PORT: int
    ES_SCHEME: str

    KAFKA_HOST: str
    KAFKA_PORT: int

    model_config = SettingsConfigDict(env_file="../.env")


settings = Settings()
