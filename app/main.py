"""FastAPI application setup and root endpoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.routers import auth, projects, documents
from app.db.database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database tables when the application starts."""
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)


@app.get("/")
def root():
    """Return the API welcome message."""
    return {"message": "Project Management API"}
