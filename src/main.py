from fastapi import FastAPI
from fastapi_cache.backends.redis import RedisBackend

from auth.base_config import auth_backend
from auth.schema import UserRead, UserCreate
from auth.base_config import fastapi_users
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from operations.router import router as router_operation
from chat.router import router as router_websocket
from tasks.router import router as router_tasks
from fastapi.middleware.cors import CORSMiddleware
from pages.router import router as router_page

app = FastAPI(title='Trading app')

# Роутер Авторизация
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth_users",
    tags=["auth"], )

# Роутер Регистрация
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/register_user",
    tags=["auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)
app.include_router(router_page)
app.include_router(router_websocket)

origins = ["*"
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'OPTIONS', 'DELETE', 'PATCH', 'PUT'],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event('startup')
async def start_redis():
    redis = aioredis.from_url('redis://localhost', encoding='utf8', decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
