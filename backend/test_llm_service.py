from unittest.mock import MagicMock, patch

import pytest

from backend.app.services.llm_service import LLMService


def test_llm_service_success():
    llm = LLMService.__new__(LLMService)

    mock_response = MagicMock()
    mock_response.text = "Hello from Gemini."

    llm.client = MagicMock()
    llm.model = "gemini-3.6-flash"

    llm.client.models.generate_content.return_value = mock_response

    result = llm.generate("Say hello.")

    assert result == "Hello from Gemini."

    llm.client.models.generate_content.assert_called_once_with(
        model="gemini-3.6-flash",
        contents="Say hello."
    )


def test_llm_service_empty_response():
    llm = LLMService.__new__(LLMService)

    mock_response = MagicMock()
    mock_response.text = ""

    llm.client = MagicMock()
    llm.model = "gemini-3.6-flash"

    llm.client.models.generate_content.return_value = mock_response

    with pytest.raises(RuntimeError):
        llm.generate("Say hello.")


def test_llm_service_quota_error():
    llm = LLMService.__new__(LLMService)

    llm.client = MagicMock()
    llm.model = "gemini-3.6-flash"

    llm.client.models.generate_content.side_effect = Exception(
        "429 RESOURCE_EXHAUSTED"
    )

    with pytest.raises(
        RuntimeError,
        match="Gemini API quota exceeded"
    ):
        llm.generate("Say hello.")