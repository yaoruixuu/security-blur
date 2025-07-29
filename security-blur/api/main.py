from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
import uuid

from docai_utils import process_document_from_gcs

from summarizer import summarize

import os
from dotenv import load_dotenv

load_dotenv()

env_path = os.getenv("ENV_FILE", ".env.local")
load_dotenv(dotenv_path=env_path)

PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["LOCATION"]
PROCESSOR_ID = os.environ["PROCESSOR_ID"]
MIME_TYPE = "application/pdf"

app = FastAPI()

class GCSProcessRequest(BaseModel):
    gcs_uri: str

class Prompt(BaseModel):
    prompt: str

@app.get("/")
def root():
    return {"message": "Document AI API is running"}

@app.post("/process_gcs")
def process_from_gcs(request: GCSProcessRequest):

    result = process_document_from_gcs(
    project_id = PROJECT_ID,
    location = LOCATION,
    processor_id = PROCESSOR_ID,
    gcs_input_uri = request.gcs_uri,
    mime_type = MIME_TYPE)

  
    return result

@app.post("/summarize")
def summarize_text(request: Prompt):

    result = summarize(request.prompt, PROJECT_ID)

    return result

