from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import init_db
from routers.auth import router as auth_router
from routers.patients import router as patients_router
from config import Settings

settings = Settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins temporarily 
    #allow_origins=["http://localhost:3000"],  # Replace with your frontend domain(s) in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(patients_router, prefix="/patients", tags=["patients"])
