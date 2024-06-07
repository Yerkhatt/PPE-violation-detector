import importlib

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.utils.common import collect_paths


app = FastAPI(
    title='PPE violation detection Service',
    # root_path="/main",
)

routers = {
    module_path.split('.')[1]: importlib.import_module(module_path, package=None)
    for module_path in collect_paths('router.py')
}

for module_name in ['violation_detector']:
    router_module = routers[module_name]
    app.include_router(router_module.router)

origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/ping')
async def ping():
    return 'pong'