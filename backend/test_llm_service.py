from app.services.llm_service import LLMService


print("Starting Gemini test...")

llm = LLMService()

response = llm.generate(
    "What is the purpose of a resume in 2 sentences?"
)

print("\nGemini Response:")
print(response)

print("\nTest completed successfully!")