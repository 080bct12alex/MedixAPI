from beanie import Document
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional, List
from datetime import date

class DiagnosisEntry(BaseModel):
    disease: str = Field(..., description='Name of the diagnosed disease', examples=['Diabetes', 'Hypertension'])
    condition: str = Field(..., description='Current condition or status of the disease', examples=['Chronic', 'Stable', 'Severe'])
    diagnosis_on: date = Field(default_factory=date.today, description='Date of diagnosis')
    notes: Optional[str] = Field(default=None, description="Optional additional information or observations")

class Patient(Document):
    id: str = Field(..., description='ID of the patient', examples=['P001'])
    name: str = Field(..., description='Name of the patient')
    city: str = Field(..., description='City where the patient is living')
    age: int = Field(..., gt=0, lt=120, description='Age of the patient')
    gender: Literal['male', 'female', 'others'] = Field(..., description='Gender of the patient')
    height: Optional[float] = Field(default=None, gt=0, description='Height of the patient in mtrs')
    weight: Optional[float] = Field(default=None, gt=0, description='Weight of the patient in kgs')
    doctor_id: str = Field(..., description='ID of the doctor')
    diagnoses_history: List[DiagnosisEntry] = Field(default_factory=list, description='List of diagnoses for the patient')

    @computed_field
    def bmi(self) -> Optional[float]:
        if self.weight is None or self.height is None or self.height == 0:
            return None
        bmi = round(self.weight / (self.height ** 2), 2)
        return bmi

    @computed_field
    def verdict(self) -> Optional[str]:
        if self.bmi is None:
            return None
        if self.bmi < 18.5:
            return 'Underweight'
        elif self.bmi < 25:
            return 'Normal'
        elif self.bmi < 30:
            return 'Overweight'
        else:
            return 'Obese'

    @computed_field
    def latest_condition(self) -> Optional[str]:
        if not self.diagnoses_history:
            return None
        # Sort by diagnosis_on date to get the latest
        latest_diagnosis = max(self.diagnoses_history, key=lambda d: d.diagnosis_on)
        return latest_diagnosis.condition

    @computed_field
    def latest_diagnosis_date(self) -> Optional[date]:
        if not self.diagnoses_history:
            return None
        return max(self.diagnoses_history, key=lambda d: d.diagnosis_on).diagnosis_on

    class Settings:
        name = "patients"


class PatientCreate(BaseModel):
    id: str = Field(..., description='ID of the patient', examples=['P001'])
    name: str = Field(..., description='Name of the patient')
    city: str = Field(..., description='City where the patient is living')
    age: int = Field(..., gt=0, lt=120, description='Age of the patient')
    gender: Literal['male', 'female', 'others'] = Field(..., description='Gender of the patient')
    height: Optional[float] = Field(default=None, gt=0, description='Height of the patient in mtrs')
    weight: Optional[float] = Field(default=None, gt=0, description='Weight of the patient in kgs')
    diagnoses_history: Optional[List[DiagnosisEntry]] = Field(default_factory=list, description='List of diagnoses for the patient')


class PatientUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    age: Optional[int] = Field(default=None, gt=0)
    gender: Optional[Literal['male', 'female', 'others']] = Field(default=None)
    height: Optional[float] = Field(default=None, gt=0)
    weight: Optional[float] = Field(default=None, gt=0)
    diagnoses_history: Optional[List[DiagnosisEntry]] = Field(default=None, description='List of diagnoses for the patient')
