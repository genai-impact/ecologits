from openai import OpenAI
from genai_impact import Tracer

Tracer.init()

client = OpenAI()

response = client.chat.completions.create(
  messages=[
    {"role": "user", "content": "Hello tell a funny story!"}
  ],
  model="gpt-3.5-turbo"
)

# Outputs content
print(response)

# Outputs environmental impacts
# print(response.impacts)
