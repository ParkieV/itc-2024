from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.routers.api import api_router
from src.shared.config import server_config


@asynccontextmanager
async def lifespan(self):
    # SetUp
    yield
    # TakeDown

app = FastAPI(root_path='/api',lifespan=lifespan)
app.add_middleware(
	CORSMiddleware,
	allow_origins=server_config.origins,
	allow_credentials=server_config.credentials,
	allow_methods=server_config.methods,
	allow_headers=server_config.headers,
)

app.include_router(api_router)

@app.get('/')
def root():
    return 'Hello world!'

if __name__ == '__main__':
    uvicorn.run("__main__:app", host=server_config.host, port=server_config.port)