from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid


router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = BASE_DIR / "uploads"

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_filename(filename: str):

    if not filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    return extension


async def save_upload(
    file: UploadFile,
    prefix: str
):

    extension = validate_filename(
        file.filename
    )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB."
        )

    filename = (
        f"{uuid.uuid4().hex}_{prefix}"
        f"{extension}"
    )

    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        buffer.write(content)

    return file_path


@router.post("/")
async def upload_files(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...)
):

    resume_path = None
    jd_path = None

    try:

        resume_path = await save_upload(
            resume,
            "resume"
        )

        jd_path = await save_upload(
            job_description,
            "job_description"
        )

        return {
            "message": "Files uploaded successfully",
            "resume_file": resume.filename,
            "job_description_file":
                job_description.filename,
            "resume_saved_as":
                resume_path.name,
            "job_description_saved_as":
                jd_path.name
        }

    except HTTPException:
        raise

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="File upload failed."
        ) from e

    finally:

        if resume_path and resume_path.exists():
            resume_path.unlink()

        if jd_path and jd_path.exists():
            jd_path.unlink()