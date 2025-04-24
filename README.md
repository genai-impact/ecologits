<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/genai-impact/ecologits/main/docs/assets/logo_dark.png">
    <img alt="EcoLogits" src="https://raw.githubusercontent.com/genai-impact/ecologits/main/docs/assets/logo_light.png">
  </picture>
</p>

🌱 **EcoLogits** tracks the energy consumption and environmental impacts of using generative AI models through APIs.

[![PyPI version](https://img.shields.io/pypi/v/ecologits?color=00bf63)](https://pypi.org/project/ecologits/)
[![PyPI downloads](https://static.pepy.tech/badge/ecologits/month)](https://pepy.tech/projects/ecologits)
[![Python version](https://img.shields.io/pypi/pyversions/ecologits)](https://pypi.org/project/ecologits/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1VxrpJ5xuWZKQLsSN12kdqUqkppHRct3G?usp=sharing)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.15132099.svg)](https://doi.org/10.5281/zenodo.15132099)


EcoLogits was created and is actively maintained by the **[GenAI Impact](https://genai-impact.org/) non-profit**. 

Read the full **documentation on [ecologits.ai](https://ecologits.ai/)**.


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
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Tell me a funny joke!"}
    ]
)

# Get estimated environmental impacts of the inference
print(f"Energy consumption: {response.impacts.energy.value} kWh")
print(f"GHG emissions: {response.impacts.gwp.value} kgCO2eq")
```

See package documentation on [EcoLogits](https://ecologits.ai/)

## Open Telemetry
Pour initialiser Open Telemetry il suffit d'ajouter ces paramètres à l'initialisation. Le reste de l'exemple au dessus est conforme.
```python
EcoLogits.init(enable_telemetry=True, telemetry_endpoint="http://localhost:4318/v1/metrics")
```


## 💚 Sponsors


<a href="https://resilio-solutions.com/" target="_blank">
<img src="https://raw.githubusercontent.com/genai-impact/ecologits/main/docs/assets/sponsors/resilio.png" alt="Resilio" height="100" width="250">
</a>


## 💪 Contributing

To get started with setting up a development environment and making a contribution to EcoLogits, see [Contributing to EcoLogits](https://ecologits.ai/latest/contributing/).

## ⚖️ License

This project is licensed under the terms of the [Mozilla Public License Version 2.0 (MPL-2.0)](https://www.mozilla.org/en-US/MPL/2.0/).
