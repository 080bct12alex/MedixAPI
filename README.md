# 🧠 Patient Management System  (FastAPI production-ready backend  Project)

A **FastAPI**-powered RESTful backend simulates a real-world use case of managing patient health records, including BMI calculations and automatic health verdicts with doctor-based data isolation, and a secure JWT-based login system — ideal for **Flask transitioning to FastAPI** or learning  scalable modern Python APIs development.

    📌 Began as a FastAPI learning journey Project , evolved into a production-ready backend project.



## ✅ Key Features

-   🔐 JWT-authenticated API access
    
-   👨‍⚕️ Doctor-Based Access Control
      -   📋 View all patients
    
      -   🔍 Retrieve a patient by ID
    
      -   ➕ Add new patient records
    
      -   🛠 Update patient information
    
      -   🗑 Delete a patient
    
      -   📊 Sort by `height`, `weight`, or `BMI`
    
      -   �� Automatically calculate BMI and assign a health category (`Underweight`, `Normal`, `Obese`)
    

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
        
    -   Pytest (test framework)
    
    -  GitHub Actions ( CI/CD Integration )
    
        
-   **Frontend:** Next.js (integrated)
