from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the JSON safely
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'q-vercel-python.json')
    with open(json_path, 'r') as f:
        students_data = json.load(f)
except Exception as e:
    students_data = {"students": []}  # fallback if file fails
    print(f"Error loading JSON: {e}")

@app.get("/")
async def root():
    return {"message": "Student Class API is running. Use /api?studentId=1&studentId=2 to get class data."}

@app.get("/api")
async def get_classes(studentId: List[int] = Query(None)):
    if not studentId:
        return {"error": "Please provide at least one studentId"}
    
    try:
        student_list = students_data.get("students", [])
        classes = [
            next((s["class"] for s in student_list if s["studentId"] == sid), None)
            for sid in studentId
        ]
        return {"classes": classes}
    except Exception as e:
        return {"error": f"Internal error: {str(e)}"}
