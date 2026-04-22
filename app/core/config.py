from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    # Proyecto
    PROJECT_NAME: str = "Green Live API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Base de datos
    DATABASE_URL: str 

    # Seguridad
    SECRET_KEY: str 
    ALGORITHM: str 
    ACCESS_TOKEN_EXPIRE_MINUTES: int 

    # CORS 
    BACKEND_CORS_ORIGINS: List[str] 

    # Configuración de Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra="ignore" 
    )

settings = Settings()