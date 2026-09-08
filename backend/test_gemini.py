import pytest

from backend.app.services.llm_service import LLMService


def test_gemini_success():
    llm = LLMService.__new__(LLMService)

    mock_response = type(
        "MockResponse",
        (),
        {
            "text": "Hello from Gemini"
        }
    )()

    class MockModels:
        def generate_content(self, model, contents):
            return mock_response

    class MockClient:
        models = MockModels()

    llm.client = MockClient()
    llm.model = "gemini-3.6-flash"

    result = llm.generate("Say hello.")

    assert result == "Hello from Gemini"


def test_gemini_empty_response():
    llm = LLMService.__new__(LLMService)

    mock_response = type(
        "MockResponse",
        (),
        {
            "text": ""
        }
    )()

    class MockModels:
        def generate_content(self, model, contents):
            return mock_response

    class MockClient:
        models = MockModels()

    llm.client = MockClient()
    llm.model = "gemini-3.6-flash"

    with pytest.raises(RuntimeError):
        llm.generate("Say hello.")


def test_gemini_quota_error():
    llm = LLMService.__new__(LLMService)

    class MockModels:
        def generate_content(self, model, contents):
            raise Exception("429 RESOURCE_EXHAUSTED")

    class MockClient:
        models = MockModels()

    llm.client = MockClient()
    llm.model = "gemini-3.6-flash"

    with pytest.raises(
        RuntimeError,
        match="Gemini API quota exceeded"
    ):
        llm.generate("Say hello.")