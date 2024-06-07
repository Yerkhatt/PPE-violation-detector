from pathlib import Path

import httpx
from loguru import logger

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

env_file = Path(__file__).parent / '.env'
env_file_encoding = 'utf-8'

class HostPort(BaseSettings):
    host: str
    port: str


class Server(HostPort):
    @property
    def url(self):
        return httpx.URL(f'http://{self.host}:{self.port}')

    model_config = SettingsConfigDict(
        env_prefix='SERVER_',
        env_file=env_file,
        env_file_encoding=env_file_encoding,
        extra='ignore',
    )


class Settings(BaseSettings):
    project_folder: Path = Field(..., alias='PROJECT_DIR')
    storage_folder: Path = Field(..., alias='STORAGE_DIR')
    yolo_checkpoint: str = Field(..., alias='YOLO_CKPT')
    server_api_key: str = Field(..., alias='SERVER_API_KEY')

    server: Server

    @field_validator('project_folder', 'storage_folder')
    def resolve_path(cls, v):
        path = Path(v).resolve()
        logger.debug("path: {}", path)
        assert path.exists(), f"Path does not exist: {path}"
        return path

    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding=env_file_encoding,
        extra='ignore',
    )


settings = Settings(
    server=Server(),
)