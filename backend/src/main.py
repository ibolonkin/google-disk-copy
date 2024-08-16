from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
from .users.router import router as user_router
from .posts.router import router as post_router
from .base import Base, engine
from .users.models import Users
from .posts.models import Posts

app = FastAPI()
# origins = [
#     "http://localhost",
#     "http://localhost:8000",
#     "http://localhost:3000",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

@app.on_event("startup")
async def init_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def drop_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


app.include_router(user_router, prefix="/v1", tags=['users'])
app.include_router(post_router, prefix="/posts", tags=['posts'])

# TODO: обновить информацию и удалить аккаунт ( сделать не активным ) и сделать рефреш токен на куках
