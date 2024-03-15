from anthropic import Anthropic
from genai_impact.client.anthropic_tracer import AnthropicInstrumentor

AnthropicInstrumentor().instrument()

api_key = '<YOUR_API_KEY>'

client = Anthropic(
    # defaults to os.environ.get("ANTHROPIC_API_KEY")
    api_key=api_key,
)
message = client.messages.create(
    model="claude-3-opus-20240229",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude"}
    ]
)
print(message)
print(message.impacts)
