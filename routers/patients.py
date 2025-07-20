from fastapi import APIRouter, Path, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import pymongo

from services.auth import get_current_doctor
from models.patient import Patient, PatientUpdate, PatientCreate

router = APIRouter()

@router.get("/view")
async def view(current_doctor: str = Depends(get_current_doctor)):
    data = await Patient.find(Patient.doctor_id == current_doctor).to_list()
    return data

@router.get("/patient/{patient_id}")
async def view_patient(patient_id: str = Path(..., description='ID of the patient in the DB', examples=['P001']), current_doctor: str = Depends(get_current_doctor)):
    patient = await Patient.get(patient_id)
    if not patient or patient.doctor_id != current_doctor:
        raise HTTPException(status_code=404, detail='Patient not found')
    return patient

@router.get("/sort")
async def sort_patients(sort_by: str = Query(..., description='Sort on the basis of height, weight, age or _id'), order: str = Query('asc', description='sort in asc or desc order'), current_doctor: str = Depends(get_current_doctor)):

    valid_fields = ['height', 'weight', 'age', '_id']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    sort_order = pymongo.DESCENDING if order=='desc' else pymongo.ASCENDING

    sorted_data = await Patient.find(Patient.doctor_id == current_doctor).sort((sort_by,sort_order)).to_list()

    return sorted_data

@router.post("/create")
async def create_patient(patient_data: PatientCreate, current_doctor: str = Depends(get_current_doctor)):

    # check if the patient already exists
    existing_patient = await Patient.get(patient_data.id)
    if existing_patient:
        raise HTTPException(status_code=400, detail='Patient already exists')

    patient = Patient(**patient_data.model_dump(), doctor_id=current_doctor)
    # new patient add to the database
    await patient.create()

    return JSONResponse(status_code=201, content={'message':'patient created successfully'})


@router.put("/edit/{patient_id}")
async def update_patient(patient_id: str, patient_update: PatientUpdate, current_doctor: str = Depends(get_current_doctor)):

    patient = await Patient.get(patient_id)

    if not patient or patient.doctor_id != current_doctor:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    patient_update_dict = patient_update.model_dump(exclude_unset=True)

    for key, value in patient_update_dict.items():
        setattr(patient, key, value)

    await patient.save()


    return JSONResponse(status_code=200, content={'message':'patient updated'})

@router.delete("/delete/{patient_id}")
async def delete_patient(patient_id: str, current_doctor: str = Depends(get_current_doctor)):

    patient = await Patient.get(patient_id)

    if not patient or patient.doctor_id != current_doctor:
        raise HTTPException(status_code=404, detail='Patient not found')
    
    await patient.delete()


    return JSONResponse(status_code=200, content={'message':'patient deleted'})
