
from beanie import init_beanie
import motor.motor_asyncio
from models.patient import Patient
from models.doctor import Doctor
from config import Settings

settings = Settings()

async def init_db():
    db_url = settings.DATABASE_URL
    client = motor.motor_asyncio.AsyncIOMotorClient(db_url)
    await init_beanie(database=client.db_name, document_models=[Patient, Doctor])
