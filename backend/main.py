from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi import UploadFile, File
from .database import engine, SessionLocal
from pydantic import BaseModel
from . import models


app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
models.Base.metadata.create_all(bind=engine)


# Request Model
class RequirementInput(BaseModel):
    requirement: str
    user_id: int


# Health Check
@app.get("/")
def home():
    return {"message": "SDLC Assistant backend running"}


@app.post("/generate")
def generate_artifacts(data: RequirementInput):

    requirement_text = data.requirement

    structured_output = {
        "user_stories": [
            "As a user, I want to create and manage tasks so that I stay organized"
        ],
        "acceptance_criteria": [
            "Given user is logged in, when they create a task, then it should be saved successfully"
        ],
        "test_cases": [
            "TC01 - User creates a task successfully",
            "TC02 - Task appears in the project list"
        ]
    }

    db = SessionLocal()

    project = models.Project(
        requirement=requirement_text,
        user_stories=json.dumps(structured_output["user_stories"]),
        acceptance_criteria=json.dumps(structured_output["acceptance_criteria"]),
        test_cases=json.dumps(structured_output["test_cases"]),
        user_id=data.user_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    db.close()

    return {
        "project_id": project.id,
        "data": structured_output
    }
# Get All Projects
@app.get("/projects/user/{user_id}")
def get_projects(user_id: int):

    db = SessionLocal()

    projects = db.query(models.Project).filter(models.Project.user_id == user_id).all()

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
@app.put("/projects/{project_id}")
def update_project(project_id: int, data: dict):

    db = SessionLocal()

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    project.user_stories = json.dumps(data.get("user_stories", []))
    project.acceptance_criteria = json.dumps(data.get("acceptance_criteria", []))
    project.test_cases = json.dumps(data.get("test_cases", []))

    db.commit()

    db.close()

    return {"message": "Project updated successfully"}
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    try:
        content = await file.read()
        text = content.decode("utf-8")

        return {"requirement": text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@app.delete("/projects/{project_id}")
def delete_project(project_id: int):

    db = SessionLocal()

    project = db.query(models.Project).filter(models.Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    db.close()

    return {"message": "Project deleted"}
class UserInput(BaseModel):
    username: str
    password: str


@app.post("/signup")
def signup(user: UserInput):

    db = SessionLocal()

    existing_user = db.query(models.User).filter(models.User.username == user.username).first()

    if existing_user:
        db.close()
        raise HTTPException(status_code=400, detail="User already exists")

    new_user = models.User(
        username=user.username,
        password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {"message": "User created successfully"}
@app.post("/login")
def login(user: UserInput):

    db = SessionLocal()

    existing_user = db.query(models.User).filter(
        models.User.username == user.username,
        models.User.password == user.password
    ).first()

    if not existing_user:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid credentials")

    db.close()

    return {
    "message": "Login successful",
    "user_id": existing_user.id,
    "is_pro": existing_user.is_pro   # NEW
}
@app.post("/upgrade/{user_id}")
def upgrade_user(user_id: int):

    db = SessionLocal()

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    user.is_pro = 1

    db.commit()
    db.close()

    return {"message": "Upgraded to Pro"}