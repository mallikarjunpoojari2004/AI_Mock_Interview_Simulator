from services.gemini_service import generate_response

prompt = "Explain what Python is in 3 simple sentences."

result = generate_response(prompt)

print("\nAI Response:")
print(result)