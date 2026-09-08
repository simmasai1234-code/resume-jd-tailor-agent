from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

from backend.app.services.document_parser import extract_text
from backend.app.orchestrator.agent_orchestrator import AgentOrchestrator


router = APIRouter(
    prefix="/workflow",
    tags=["End-to-End Workflow"]
)

orchestrator = AgentOrchestrator()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_file(filename: str):
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    return extension


async def save_upload(file: UploadFile, suffix: str) -> Path:

    extension = validate_file(file.filename)

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB."
        )

    filename = f"{uuid.uuid4()}_{suffix}{extension}"

    file_path = UPLOAD_DIR / filename

    with open(file_path, "wb") as buffer:
        buffer.write(content)

    return file_path


@router.post("/")
async def run_end_to_end_workflow(
    resume: UploadFile = File(...),
    job_description: UploadFile = File(...),
    max_revisions: int = 2
):
    """
    Run the complete Resume JD Tailor agentic workflow
    using uploaded Resume and Job Description files.
    """

    resume_path = await save_upload(
        resume,
        "resume"
    )

    jd_path = await save_upload(
        job_description,
        "job_description"
    )

    try:
        resume_text = extract_text(
            str(resume_path)
        )

        jd_text = extract_text(
            str(jd_path)
        )

        if not resume_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume."
            )

        if not jd_text:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the job description."
            )

        result = orchestrator.run(
            resume_text=resume_text,
            jd_text=jd_text,
            max_revisions=max_revisions
        )

        return {
            "message": "End-to-end agentic workflow completed",
            "resume_file": resume.filename,
            "job_description_file": job_description.filename,
            "result": result
        }

    finally:
        if resume_path.exists():
            resume_path.unlink()

        if jd_path.exists():
            jd_path.unlink()