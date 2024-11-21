from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    POSTGRES_NAME: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_NAME}"

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()