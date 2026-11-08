from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import auth, projects, documents
from app.db.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(documents.router)

@app.get("/")
def root():
    return {"message": "Project Management API"}
