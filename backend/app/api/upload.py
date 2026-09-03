from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import shutil
import uuid

router = APIRouter(prefix="/upload", tags=["Upload"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_extension(filename: str):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are allowed."
        )

    return extension


async def validate_file_size(file: UploadFile):
    content = await file.read()
    await file.seek(0)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB."
        )


@router.post("/")
async def upload_documents(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):
    resume_extension = validate_extension(resume.filename)
    jd_extension = validate_extension(job_description.filename)

    await validate_file_size(resume)
    await validate_file_size(job_description)

    resume_name = f"{uuid.uuid4()}_resume{resume_extension}"
    jd_name = f"{uuid.uuid4()}_job_description{jd_extension}"

    resume_path = UPLOAD_DIR / resume_name
    jd_path = UPLOAD_DIR / jd_name

    with open(resume_path, "wb") as buffer:
        shutil.copyfileobj(resume.file, buffer)

    with open(jd_path, "wb") as buffer:
        shutil.copyfileobj(job_description.file, buffer)

    return {
        "message": "Files uploaded successfully",
        "resume": {
            "original_name": resume.filename,
            "saved_name": resume_name
        },
        "job_description": {
            "original_name": job_description.filename,
            "saved_name": jd_name
        }
    }