from fastapi import FastAPI
from contextlib import asynccontextmanager

from database.config import connect_db, disconnect_db
from routers.resume import router as resume_router
from routers.user import router as user_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await disconnect_db()

app = FastAPI(lifespan=lifespan)

app.include_router(resume_router, prefix="/api/v1/resume")
app.include_router(user_router, prefix="/api/v1/user")