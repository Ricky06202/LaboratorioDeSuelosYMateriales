from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str = "SECRET_KEY_PLACEHOLDER"
    STORAGE_PATH: str = "./dev_mnt/documentos_suelos"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
