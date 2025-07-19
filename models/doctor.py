from beanie import Document
from pydantic import BaseModel, Field

class Doctor(Document):
    username: str = Field(..., unique=True)
    password: str

    class Settings:
        name = "doctors"

class DoctorCreate(BaseModel):
    username: str
    password: str