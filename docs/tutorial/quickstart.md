# Quickstart

!!! warning

    This page is under construction.

The :seedling: **EcoLogits** library tracks the energy consumption and environmental impacts of generative AI models accessed through APIs and their official client libraries. 

It achieves this by **patching the Python client libraries**, ensuring that each API request is wrapped with an impact calculation function. This function computes the **environmental impact based on several request features**, such as the **chosen model**, the **number of tokens generated**, and the **request's latency**. The resulting data is then encapsulated in an `Impacts` object, which is added to the response, containing the environmental impacts for a specific request.

In the following sections we will didactically demonstrate **how the library works and how you can integrate it in your own projects**. As of today we only support text generation models, but we plan to expand to other modalities (image generation, embeddings for RAG, etc.) in the near future.


## Chat Completions with OpenAI

An example on how to integrate :seedling: EcoLogits when using OpenAI GPT-3.5-Turbo model. To learn about all integrations with OpenAI, see the following page: [OpenAI provider](providers/openai.md).

```python
from ecologits import EcoLogits
from openai import OpenAI

# Initialize EcoLogits
EcoLogits.init()

client = OpenAI(api_key="<OPENAI_API_KEY>")

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell me a funny joke!"}
    ]
)

# Get estimated environmental impacts of the inference
print(f"Energy consumption: {response.impacts.energy.value} kWh")
print(f"GHG emissions: {response.impacts.gwp.value} kgCO2eq")
```
