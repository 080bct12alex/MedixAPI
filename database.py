
from beanie import init_beanie
import motor.motor_asyncio
from models.patient import Patient
from models.doctor import Doctor

async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb+srv://alexstha103:alex03@cluster0.j2559tn.mongodb.net/Medix_DB?retryWrites=true&w=majority&appName=Cluster0")
    await init_beanie(database=client.db_name, document_models=[Patient, Doctor])
