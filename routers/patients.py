from fastapi import APIRouter, Path, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
import pymongo
from datetime import date, timedelta
from typing import Optional

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
async def sort_patients(sort_by: str = Query(..., description='Sort on the basis of_id,latest_diagnosis_date, latest_condition, height, weight, age  '), order: str = Query('asc', description='sort in asc or desc order'), current_doctor: str = Depends(get_current_doctor)):

    valid_fields = ['height', 'weight', 'age', '_id', 'latest_diagnosis_date', 'latest_condition']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc and desc')
    
    sort_order = pymongo.DESCENDING if order=='desc' else pymongo.ASCENDING

    sorted_data = await Patient.find(Patient.doctor_id == current_doctor).sort((sort_by,sort_order)).to_list()

    return sorted_data

@router.get("/group_by_disease")
async def group_patients_by_disease(current_doctor: str = Depends(get_current_doctor)):
    pipeline = [
        {"$match": {"doctor_id": current_doctor}},  # Filter by current doctor
        {"$unwind": "$diagnoses_history"},  # Deconstruct the diagnoses_history array
        {"$group": {
            "_id": "$diagnoses_history.disease",  # Group by disease name
            "patients": {"$push": {
                "id": "$_id",
                "name": "$name",
                "city": "$city",
                "age": "$age",
                "gender": "$gender",
                "height": "$height",
                "weight": "$weight",
                "latest_condition": "$latest_condition",
                "latest_diagnosis_date": "$latest_diagnosis_date",
                "diagnosis_details": "$diagnoses_history" # Include specific diagnosis details
            }}
        }}
    ]
    
    grouped_data = await Patient.aggregate(pipeline).to_list()
    return grouped_data

@router.get("/group_by_condition")
async def group_patients_by_condition(current_doctor: str = Depends(get_current_doctor)):
    pipeline = [
        {"$match": {"doctor_id": current_doctor}},  # Filter by current doctor
        {"$unwind": "$diagnoses_history"},  # Deconstruct the diagnoses_history array
        {"$group": {
            "_id": "$diagnoses_history.condition",  # Group by condition
            "patients": {"$push": {
                "id": "$_id",
                "name": "$name",
                "city": "$city",
                "age": "$age",
                "gender": "$gender",
                "height": "$height",
                "weight": "$weight",
                "latest_condition": "$latest_condition",
                "latest_diagnosis_date": "$latest_diagnosis_date",
                "diagnosis_details": "$diagnoses_history" # Include specific diagnosis details
            }}
        }}
    ]
    
    grouped_data = await Patient.aggregate(pipeline).to_list()
    return grouped_data

@router.get("/filter")
async def filter_patients(
    disease_name: Optional[str] = Query(None, description="Filter by disease name"),
    condition: Optional[str] = Query(None, description="Filter by disease condition"),
    diagnosed_after_months: Optional[str] = Query(None, description="Filter by diagnoses in the last X months"),
    current_doctor: str = Depends(get_current_doctor)
):
    query = Patient.find(Patient.doctor_id == current_doctor)

    if disease_name:
        query = query.find({"diagnoses_history.disease": {"$regex": disease_name, "$options": "i"}})
    
    if condition:
        query = query.find({"diagnoses_history.condition": condition})

    if diagnosed_after_months:
        try:
            diagnosed_after_months_int = int(diagnosed_after_months)
            from_date = date.today() - timedelta(days=diagnosed_after_months_int * 30) # Approximate months
            query = query.find({"diagnoses_history.diagnosis_on": {"$gte": from_date}})
        except ValueError:
            raise HTTPException(status_code=400, detail="diagnosed_after_months must be an integer")

    filtered_data = await query.to_list()
    return filtered_data

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
