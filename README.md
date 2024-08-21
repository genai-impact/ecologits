<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/genai-impact/ecologits/main/docs/assets/logo_dark.png">
    <img alt="EcoLogits" src="https://raw.githubusercontent.com/genai-impact/ecologits/main/docs/assets/logo_light.png">
  </picture>
</p>

🌱 **EcoLogits** tracks the energy consumption and environmental impacts of using generative AI models through APIs.

[![PyPI version](https://img.shields.io/pypi/v/ecologits?color=00bf63)](https://pypi.org/project/ecologits/)
[![Python version](https://img.shields.io/pypi/pyversions/ecologits)](https://pypi.org/project/ecologits/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1VxrpJ5xuWZKQLsSN12kdqUqkppHRct3G?usp=sharing)

**Documentation: [ecologits.ai](https://ecologits.ai/)**


## ⚙️ Installation

```shell
pip install ecologits
```

For integration with a specific provider, use `pip install ecologits[openai]`. We are currently supporting the following providers: `anthropic`, `cohere`, `google-generativeai`, `huggingface-hub`, `mistralai` and `openai`. See the full [list of providers](https://ecologits.ai/latest/tutorial/providers/).

## 🚀 Usage

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

See package documentation on [EcoLogits](https://ecologits.ai/)

## 💪 Contributing

To get started with setting up a development environment and making a contribution to EcoLogits, see [Contributing to EcoLogits](https://ecologits.ai/latest/contributing/).

## ⚖️ License

This project is licensed under the terms of the [Mozilla Public License Version 2.0 (MPL-2.0)](https://www.mozilla.org/en-US/MPL/2.0/).
