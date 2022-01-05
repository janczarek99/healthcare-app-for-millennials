from typing import Any, Dict, Optional

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    # Authentication
    AUTHORIZATION_OFF: bool = False

    SECRET_KEY: str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "healthcare_api_db"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_HOST"),
            query="port=" + values.get("POSTGRES_PORT"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    # External services
    # Azure storage connection
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    AZURE_STORAGE_CONTAINER_NAME: str = ""
    AZURE_STORAGE_PATH: str = "users/{user_id}/{entity}/{entity_id}"

    # Azure OCR
    AZURE_OCR_ENDPOINT: str = ""
    AZURE_OCR_KEY: str = ""

    # Azure custom vision models
    AZURE_CV_ENDPOINT: str = ""
    AZURE_CV_KEY: str = ""
    AZURE_CV_MODEL_PNEUMONIA_ITERATION: int = 1
    AZURE_CV_MODEL_PNEUMONIA_PROJECT_ID: str = ""
    AZURE_CV_MODEL_LUNG_CANCER_ITERATION: int = 1
    AZURE_CV_MODEL_LUNG_CANCER_PROJECT_ID: str = ""
    AZURE_CV_MODEL_BRAIN_TUMOUR_ITERATION: int = 2
    AZURE_CV_MODEL_BRAIN_TUMOUR_PROJECT_ID: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
