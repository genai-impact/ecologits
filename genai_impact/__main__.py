from genai_impact.client_wrapper import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-3.5-turbo", messages=[{"role": "user", "content": "Hello World!"}]
)

print(response.impacts)
