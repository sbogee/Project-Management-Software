from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, projects
from app.db.database import Base, engine
from sqlalchemy import text

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(projects.router)

@app.get("/")
def root():
    return {"message": "Project Management API"}
