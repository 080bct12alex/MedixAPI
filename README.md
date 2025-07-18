# 🧠 Patient Management System  (FastAPI Learning Project)

This is  project designed to learn how to build RESTful APIs using **FastAPI**. It simulates a real-world use case of managing patient health records, including BMI calculations and automatic health verdicts. Data is stored in MongoDB


📌 This project is ideal for those transitioning from **Flask to FastAPI**, or learning modern Python API development.

---


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
- Frontend (Next.js)

## Improvement 
- Migrating from patients.json to a real database ( FastAPI → Beanie (ODM) → Motor (async driver) → MongoDB.)
- Use of a Dockerfile ensures the application runs in a consistent and isolated environment, helping to avoid conflicts and making deployment easier and more reliable.
- Integration of frontend with backend supporting doctor login
- Data separation per doctor so each doctor only accesses their own patients login 
- Protected API routes that restrict access to patient list, add, edit, view, and delete pages until the doctor is logged in Custom  using JWTBearer class (subclassing HTTPBearer)
- JWT-based login using real password authentication, where the doctor ID in the token is used to authorize patient data operations
use passlib for password hashing ,PyJWT for creating and verifying JWTs

- ADD pytest for allowing  simple, scalable test writing and execution ,improves code reliability and makes it easier to catch bugs early.



## Notes for Improvement


1. Improve Code Quality with Linting & Formatting
       * installed ruff, b used it to
         check and format the code.



   2. Organize Endpoints with API Routers
       * What: Your app.py file will get crowded as you add more endpoints. We can
         split the patient-related and doctor-related endpoints into separate files
         (e.g., routers/patients.py, routers/auth.py) to keep the code clean and
         modular.

   3. Enhance Configuration Management
       * What: Currently, you load environment variables directly in app.py. We can
         create a dedicated, type-safe config.py file using Pydantic's BaseSettings.
         This validates your settings on startup (like ensuring DATABASE_URL is set)
         and provides better autocompletion.

   4. Set Up a CI/CD Pipeline
        * What: This is a professional best practice. We can create a GitHub Actions
         workflow that automatically runs your tests and linter every time you push
         new code. This acts as a gatekeeper to ensure that no broken or poorly
         formatted code gets merged into your main branch.




