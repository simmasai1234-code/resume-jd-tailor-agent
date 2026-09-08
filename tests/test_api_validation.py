from fastapi.testclient import (
    TestClient
)

from backend.app.main import app


client = TestClient(app)


def test_workflow_rejects_invalid_revision():

    response = client.post(
        "/workflow/?max_revisions=-1"
    )

    assert response.status_code in [
        400,
        422
    ]