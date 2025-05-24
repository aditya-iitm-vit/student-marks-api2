from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import json
import os

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load the student marks from JSON file
try:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, 'q-vercel-python.json')
    with open(json_path, 'r') as f:
        students_data = json.load(f)  # ← this is a list
except Exception as e:
    students_data = []
    print(f"Failed to load student data: {e}")

@app.get("/")
async def root():
    return {"message": "Student Marks API is running. Use /api?name=X&name=Y to get marks."}

@app.get("/api")
async def get_marks(name: List[str] = Query(None)):
    if not name:
        return {"error": "Please provide at least one name"}
    
    marks = [
        next((s["marks"] for s in students_data if s["name"] == n), None)
        for n in name
    ]
    return {"marks": marks}
