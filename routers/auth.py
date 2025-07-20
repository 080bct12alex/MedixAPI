from fastapi import APIRouter, HTTPException
from auth import create_access_token, verify_password, get_password_hash
from models.doctor import Doctor, DoctorCreate

router = APIRouter()

@router.post("/register")
async def register_doctor(doctor: DoctorCreate):
    existing_doctor = await Doctor.find_one(Doctor.username == doctor.username)
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = get_password_hash(doctor.password)
    new_doctor = Doctor(username=doctor.username, password=hashed_password)
    await new_doctor.create()
    return {"message": "Doctor registered successfully"}

@router.post("/login")
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
