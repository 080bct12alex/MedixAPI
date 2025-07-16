# 🧠 Patient Management System  (FastAPI Learning Project)

This is a beginner-friendly project designed to learn how to build RESTful APIs using **FastAPI**. It simulates a real-world use case of managing patient health records, including BMI calculations and automatic health verdicts. Data is stored in a local JSON file (`patients.json`). 


📌 This project is ideal for those transitioning from **Flask to FastAPI**, or learning modern Python API development.

---

## 🌐 Live Docs

You can explore and test the API using the live Swagger documentation hosted here:

**[https://medixapi.onrender.com/docs](https://medixapi.onrender.com/docs)**

This is the deployed version of the Patient Management System API, fully functional and ready to use.

## 🌍 **Frontend Website:**  
  [https://medix-neon.vercel.app](https://medix-neon.vercel.app) 

##  💻 **Frontend GitHub Repository:**  
  [https://github.com/080bct12alex/MedixUI](https://github.com/080bct12alex/MedixUI)

## ✅ Features

- 📋 View all patients
- 🔍 Retrieve a patient by ID
- ➕ Add new patient records
- 🛠 Update patient info
- 🗑 Delete a patient
- 📊 Sort by `height`, `weight`, or `BMI`
- 🧮 Auto-calculation of BMI and health category (`Underweight`, `Normal`, `Obese`)

---

## 🛠 Tech Stack

- **Language:** Python 
- **Framework:** FastAPI 
- **Data Storage:** `patients.json` file
- **Tools:** Uvicorn (ASGI server), Pydantic (for validation)
- Frontend (React/Next.js)

## Notes for Improvement
- Migrating from patients.json to a real database (like MongoDB or PostgreSQL)
- Use of a Dockerfile ensures the application runs in a consistent and isolated environment, helping to avoid conflicts and making deployment easier and more reliable.
- Integration of frontend with backend supporting doctor login
- Data separation per doctor so each doctor only accesses their own patients
- Protected API routes that restrict access to patient list, add, edit, view, and delete pages until the doctor is logged in
- JWT-based login using real password authentication, where the doctor ID in the token is used to authorize patient data operations
---

