
from beanie import init_beanie
import motor.motor_asyncio
from models.patient import Patient
from models.doctor import Doctor
import os

async def init_db():
    db_url = os.getenv("DATABASE_URL")
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    await init_beanie(database=client.db_name, document_models=[Patient, Doctor])
