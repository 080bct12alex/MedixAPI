# 🧠 Patient Management System  (FastAPI production-ready backend  Project)

A **FastAPI**-powered RESTful backend simulates a real-world use case of managing patient health records, including BMI calculations and automatic health verdicts with doctor-based data isolation, and a secure JWT-based login system — ideal for **Flask transitioning to FastAPI** or learning  scalable modern Python APIs development.

    📌 Began as a FastAPI learning journey Project , evolved into a production-ready backend project.


## 🌐 Live Docs

You can explore and test the API using the live Swagger documentation hosted here:

**[https://medixapi.onrender.com/docs](https://medixapi.onrender.com/docs)**

This is the deployed version of the Patient Management System API, fully functional and ready to use.

## 🌍 **Frontend Website:**  
  [https://medix-neon.vercel.app](https://medix-neon.vercel.app) 

##  💻 **Frontend GitHub Repository:**  
  [https://github.com/080bct12alex/MedixUI](https://github.com/080bct12alex/MedixUI)



## ✅ Key Features

-   🔐 JWT-authenticated API access
    
-   👨‍⚕️ Doctor-Based Access Control
      -   📋 View all patients
    
      -   🔍 Retrieve a patient by ID
    
      -   ➕ Add new patient records
    
      -   🛠 Update patient information
    
      -   🗑 Delete a patient
    
      -   📊 Sort by   `_id`, `latest_diagnosis_date`, `latest_condition`, `age`,`height`, `weight`.

      -   �� Automatically calculate BMI and assign a health category (`Underweight`, `Normal`, `Obese`)
     - 🩺 Diagnosis Tracking
       - Track each patient’s medical diagnosis history .
     - 📚 Diagnosis-Based Grouping
       - Group patients by `disease` , `condition` .

     - Filter patients based on  `Disease name` , `Condition` , `Diagnosis` `date`. 
       

----------

## 🛠 Tech Stack

-   **Language:** Python
    
-   **Framework:** FastAPI
    
-   **Database:** MongoDB (via Beanie ODM + Motor async driver)
    
-   **Tools:**
    
    -   Uvicorn (ASGI server)
        
    -   Pydantic (data validation)
        
    -   Passlib (password hashing)
        
    -   PyJWT (JWT token handling)
        
    -   Docker (containerization)
        
    -   Ruff (linter/formatter)
        
    -   Pytest (unit testing framework)
    
    -  GitHub Actions ( CI/CD Integration )
    
        
-   **Frontend:** Next.js (integrated)

