import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

from fastapi import FastAPI, Path, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from typing import Annotated, Literal, Optional
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import pymongo

from database import init_db
from auth import create_access_token, authenticate_user, get_current_user, get_current_doctor, verify_password, get_password_hash
from models.patient import Patient, PatientUpdate, PatientCreate
from models.doctor import Doctor, DoctorCreate


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins temporarily
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
async def register_doctor(doctor: DoctorCreate):
    existing_doctor = await Doctor.find_one(Doctor.username == doctor.username)
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(doctor.password)
    new_doctor = Doctor(username=doctor.username, password=hashed_password)
    await new_doctor.create()
    return {"message": "Doctor registered successfully"}

@app.post("/login")
async def login_for_access_token(form_data: DoctorCreate):
    doctor = await Doctor.find_one(Doctor.username == form_data.username)
    if not doctor or not verify_password(form_data.password, doctor.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": doctor.username})
    return {"access_token": access_token, "token_type": "bearer"}
        

@app.get("/")
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message': 'A fully functional API to manage your patient records'}

@app.get('/view')
async def view(current_doctor: str = Depends(get_current_doctor)):
    data = await Patient.find(Patient.doctor_id == current_doctor).to_list()
    return data

@app.get('/patient/{patient_id}')
async def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', examples=['P001']), current_doctor: str = Depends(get_current_doctor)):
    patient = await Patient.get(patient_id)
    if not patient or patient.doctor_id != current_doctor:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient

@app.get('/sort')
async def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight, age or _id'), order: str = Query('asc', description='sort in asc or desc order'), current_doctor: str = Depends(get_current_doctor)):

    valid_fields = ['height', 'weight', 'age', '_id']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    sort_order = pymongo.DESCENDING if order=='desc' else pymongo.ASCENDING

    sorted_data = await Patient.find(Patient.doctor_id == current_doctor).sort((sort_by,sort_order)).to_list()

    return sorted_data

@app.post('/create')
async def create_patient(patient_data: PatientCreate, current_doctor: str = Depends(get_current_doctor)):

    # check if the patient already exists
    existing_patient = await Patient.get(patient_data.id)
    if existing_patient:
        raise HTTPException(status_code=400, detail='Patient already exists')

    patient = Patient(**patient_data.model_dump(), doctor_id=current_doctor)
    # new patient add to the database
    await patient.create()

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


@app.put('/edit/{patient_id}')
async def update_patient(patient_id: str, patient_update: PatientUpdate, current_doctor: str = Depends(get_current_doctor)):

    patient = await Patient.get(patient_id)

    if not patient or patient.doctor_id != current_doctor:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    patient_update_dict = patient_update.model_dump(exclude_unset=True)

    for key, value in patient_update_dict.items():
        setattr(patient, key, value)

    await patient.save()


    return JSONResponse(status_code=200, content={'message':'patient updated'})

@app.delete('/delete/{patient_id}')
async def delete_patient(patient_id: str, current_doctor: str = Depends(get_current_doctor)):

    patient = await Patient.get(patient_id)

    if not patient or patient.doctor_id != current_doctor:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    await patient.delete()


    return JSONResponse(status_code=200, content={'message':'patient deleted'})
