from huggingface_hub import InferenceClient
from genai_impact import Tracer

Tracer.init()


client = InferenceClient()

res = client.text_generation("Today is", max_new_tokens=12, model="HuggingFaceH4/zephyr-7b-beta")

# Outputs content
print(res)

# Outputs environmental impacts
# print(res.impacts)
