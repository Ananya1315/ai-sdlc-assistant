from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import json

app = FastAPI()

class RequirementInput(BaseModel):
    requirement: str


@app.get("/")
def home():
    return {"message": "AI SDLC Assistant running (Local LLM - Structured Mode)"}


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

        
        start = ai_text.find("{")
        end = ai_text.rfind("}") + 1
        cleaned_json = ai_text[start:end]

        try:
            structured_output = json.loads(cleaned_json)
            return structured_output
        except json.JSONDecodeError:
            return {
                "error": "AI did not return perfectly formatted JSON",
                "raw_output": ai_text
            }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))