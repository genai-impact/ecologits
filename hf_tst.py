import asyncio
from huggingface_hub import InferenceClient
from huggingface_hub import AsyncInferenceClient
from genai_impact import Tracer

Tracer.init()


async def main():
    messages = [{"role": "user", "content": "What is the capital of France?"}]
    client = AsyncInferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
    res = await client.chat_completion(messages, max_tokens=15)
    print(res)


messages = [{"role": "user", "content": "What is the capital of France?"}]
client = InferenceClient(model="HuggingFaceH4/zephyr-7b-beta")
res = client.chat_completion(messages, max_tokens=15)
print(res)


if __name__ == '__main__':
    asyncio.run(main())
