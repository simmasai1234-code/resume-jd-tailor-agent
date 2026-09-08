from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

from pathlib import Path
import uuid

from backend.app.services.document_parser import (
    extract_text
)

from backend.app.orchestrator.agent_orchestrator import (
    AgentOrchestrator
)


router = APIRouter(
    prefix="/workflow",
    tags=["End-to-End Workflow"]
)


orchestrator = AgentOrchestrator()


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

MAX_REVISIONS = 5


def validate_file(filename: str):

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
    suffix: str
):

    extension = validate_file(
        file.filename
    )

    content = await file.read()

    if len(content) > MAX_FILE_SIZE:

        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB."
        )

    filename = (
        f"{uuid.uuid4().hex}_"
        f"{suffix}{extension}"
    )

    file_path = UPLOAD_DIR / filename

    with file_path.open("wb") as buffer:
        buffer.write(content)

    return file_path


@router.post("/")
async def run_end_to_end_workflow(

    resume: UploadFile = File(...),

    job_description: UploadFile = File(...),

    max_revisions: int = 2

):

    if max_revisions < 0:

        raise HTTPException(
            status_code=400,
            detail="max_revisions cannot be negative."
        )

    if max_revisions > MAX_REVISIONS:

        raise HTTPException(
            status_code=400,
            detail=(
                f"max_revisions cannot exceed "
                f"{MAX_REVISIONS}."
            )
        )


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


        resume_text = extract_text(
            str(resume_path)
        )

        jd_text = extract_text(
            str(jd_path)
        )


        if not resume_text:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text "
                    "from the resume."
                )
            )


        if not jd_text:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Could not extract text "
                    "from the job description."
                )
            )


        result = orchestrator.run(

            resume_text=resume_text,

            jd_text=jd_text,

            max_revisions=max_revisions

        )


        return {

            "message":
                "End-to-end agentic workflow completed",

            "resume_file":
                resume.filename,

            "job_description_file":
                job_description.filename,

            "result":
                result

        }


    except HTTPException:
        raise


    except RuntimeError as e:

        raise HTTPException(
            status_code=503,
            detail=str(e)
        ) from e


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Workflow execution failed."
        ) from e


    finally:

        if (
            resume_path
            and resume_path.exists()
        ):

            resume_path.unlink()


        if (
            jd_path
            and jd_path.exists()
        ):

            jd_path.unlink()