from huggingface_hub import InferenceClient
from genai_impact import Tracer

Tracer.init()


messages = [{"role": "user", "content": "What is the capital of France?"}]
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
res = client.chat_completion(messages, max_tokens=10)
print(res)
# ChatCompletionOutput(choices=[ChatCompletionOutputChoice(finish_reason='eos_token', index=0, message=ChatCompletionOutputChoiceMessage(content='The capital of France is Paris (French: Paris). The French government, including the President, the National Assembly, and the Senate, are located in Paris. Other major cities in France include Marseille, Lyon, and Toulouse, but Paris is the administrative, cultural, and economic center of the country.', role='assistant'))], created=1711590573)
# print(res.choices[0].message.content)

# print(res.impacts)
