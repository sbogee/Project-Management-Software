from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import users
from app.routers import auth
from app.db.database import Base, engine
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Project Management API"}
