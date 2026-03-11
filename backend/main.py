from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, SessionLocal
from . import models

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables automatically
models.Base.metadata.create_all(bind=engine)

# Request Model
class RequirementInput(BaseModel):
    requirement: str

# Health Check

@app.get("/")
def home():
    return {"message": "AI SDLC Assistant running "}


# Generate SDLC Artifacts
@app.post("/generate")
def generate_artifacts(data: RequirementInput):

    requirement_text = data.requirement

    prompt = f"""
You are a software engineering assistant.

Convert the following requirement into structured JSON.

Return ONLY valid JSON in this format:

{{
  "user_stories": [
    "As a ..., I want ..., so that ..."
  ],
  "acceptance_criteria": [
    "Given ..., when ..., then ..."
  ],
  "test_cases": [
    "TC01 - ...",
    "TC02 - ..."
  ]
}}

Do not add explanations.
Do not add extra text.
Return JSON only.

Requirement:
{requirement_text}
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False
            },
            timeout=600
        )

        result = response.json()

        if "response" not in result:
            raise Exception("Invalid response from Ollama")

        ai_text = result["response"].strip()

        # Clean model output
        
        ai_text = ai_text.replace("```json", "").replace("```", "").strip()

        start = ai_text.find("{")
        end = ai_text.rfind("}") + 1

        if start == -1 or end == -1:
            return {
                "error": "AI response did not contain JSON",
                "raw_output": ai_text
            }

        cleaned_json = ai_text[start:end]

        try:
            structured_output = json.loads(cleaned_json)

            # Save to Database
            
            db = SessionLocal()

            project = models.Project(
                requirement=requirement_text,
                user_stories=json.dumps(structured_output.get("user_stories", [])),
                acceptance_criteria=json.dumps(structured_output.get("acceptance_criteria", [])),
                test_cases=json.dumps(structured_output.get("test_cases", []))
            )

            db.add(project)
            db.commit()
            db.refresh(project)

            response_data = {
                "project_id": project.id,
                "data": structured_output
            }

            db.close()

            return response_data

        except json.JSONDecodeError:
            return {
                "error": "AI did not return perfectly formatted JSON",
                "raw_output": ai_text
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Get All Projects

@app.get("/projects")
def get_projects():

    db = SessionLocal()

    projects = db.query(models.Project).all()

    result = []

    for project in projects:
        result.append({
            "id": project.id,
            "requirement": project.requirement
        })

    db.close()

    return result

# Get Single Project
@app.get("/projects/{project_id}")
def get_project(project_id: int):

    db = SessionLocal()

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    result = {
        "id": project.id,
        "requirement": project.requirement,
        "user_stories": json.loads(project.user_stories),
        "acceptance_criteria": json.loads(project.acceptance_criteria),
        "test_cases": json.loads(project.test_cases)
    }

    db.close()

    return result