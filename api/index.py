from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load student data from JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'q-vercel-python.json')

with open(json_path, 'r') as f:
    students_data = json.load(f)

@app.get("/")
async def root():
    return {
        "message": "Student Class API is running. Use /api?studentId=1&studentId=2 to get class data."
    }

@app.get("/api")
async def get_classes(studentId: List[int] = Query(None)):
    """
    Get class names for one or more student IDs.
    Example: /api?studentId=1&studentId=2
    """
    if not studentId:
        return {"error": "Please provide at least one studentId"}
    
    student_list = students_data["students"]
    classes = []
    for sid in studentId:
        student_class = next((s["class"] for s in student_list if s["studentId"] == sid), None)
        classes.append(student_class)
    
    return {"classes": classes}
