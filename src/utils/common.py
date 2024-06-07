from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette import status

from settings import settings

base_folder = settings.project_folder
app_folder = settings.project_folder / 'src'

api_key_header = APIKeyHeader(name="X-API-Key")
server_api_key = settings.server_api_key


def get_api_key(api_key: str = Security(api_key_header)) -> str:
    if api_key == server_api_key:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )


def collect_paths(pattern: str):
    for model_file in list(app_folder.rglob(pattern)):
        model_file = model_file.relative_to(base_folder)
        module_path = str(model_file.with_suffix('')).replace('/', '.').replace('\\', '.')
        yield module_path
