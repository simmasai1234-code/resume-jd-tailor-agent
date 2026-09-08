from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import uuid

from backend.app.services.document_parser import extract_text


router = APIRouter(
    prefix="/parse",
    tags=["Document Parsing"]
)


BASE_DIR = Path(__file__).resolve().parents[3]

UPLOAD_DIR = (BASE_DIR / "uploads").resolve()

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


MAX_FILE_SIZE = 5 * 1024 * 1024


def validate_file(filename: str) -> str:
    """
    Validate the uploaded filename and return its extension.
    """

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


def safe_upload_path(
    filename: str
) -> Path:
    """
    Create a safe file path inside the uploads directory.

    UUID-based filenames prevent:
    - path traversal
    - filename collisions
    - malicious original filenames
    """

    extension = validate_file(filename)

    safe_filename = (
        f"{uuid.uuid4().hex}"
        f"{extension}"
    )

    file_path = (
        UPLOAD_DIR / safe_filename
    ).resolve()

    # Extra protection against path traversal.
    if UPLOAD_DIR not in file_path.parents:
        raise HTTPException(
            status_code=400,
            detail="Invalid file path."
        )

    return file_path


async def save_upload(
    file: UploadFile
) -> Path:
    """
    Safely save an uploaded document.
    """

    file_path = safe_upload_path(
        file.filename
    )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail="File size must be less than 5 MB."
        )

    try:

        with file_path.open("wb") as buffer:
            buffer.write(content)

    except OSError as e:

        raise HTTPException(
            status_code=500,
            detail="Could not save uploaded file."
        ) from e

    return file_path


@router.post("/")
async def parse_document(
    file: UploadFile = File(...)
):
    """
    Upload and parse a PDF or DOCX document.

    The temporary file is deleted after parsing.
    """

    file_path = None

    try:

        file_path = await save_upload(
            file
        )

        try:

            text = extract_text(
                str(file_path)
            )

        except ValueError as e:

            raise HTTPException(
                status_code=400,
                detail=str(e)
            ) from e

        except FileNotFoundError as e:

            raise HTTPException(
                status_code=404,
                detail="Uploaded file could not be found."
            ) from e

        except Exception as e:

            raise HTTPException(
                status_code=400,
                detail="Could not parse the uploaded document."
            ) from e


        if not text:

            raise HTTPException(
                status_code=400,
                detail="No readable text found in the document."
            )


        return {
            "message": "Document parsed successfully",
            "filename": file.filename,
            "extension": file_path.suffix.lower(),
            "text": text
        }


    except HTTPException:
        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Document processing failed."
        ) from e


    finally:

        if (
            file_path is not None
            and file_path.exists()
        ):

            try:
                file_path.unlink()

            except OSError:
                pass