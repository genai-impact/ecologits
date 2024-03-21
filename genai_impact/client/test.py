from genai_impact import InferenceClient

client = InferenceClient(
    # api_key="<OPENAI_API_KEY>",
)

res = client.text_generation("Today is", max_new_tokens=12, details=True)

# Get estimated environmental impacts for that inference.
print(res)
