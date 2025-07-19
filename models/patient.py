
from beanie import Document
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional

class Patient(Document):
    id: str = Field(..., description='ID of the patient', examples=['P001'])
    name: str = Field(..., description='Name of the patient')
    city: str = Field(..., description='City where the patient is living')
    age: int = Field(..., gt=0, lt=120, description='Age of the patient')
    gender: Literal['male', 'female', 'others'] = Field(..., description='Gender of the patient')
    height: float = Field(..., gt=0, description='Height of the patient in mtrs')
    weight: float = Field(..., gt=0, description='Weight of the patient in kgs')
    doctor_id: str = Field(..., description='ID of the doctor')

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:

        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Normal'
        else:
            return 'Obese'

    class Settings:
        name = "patients"


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female']] = Field(default=None)
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
