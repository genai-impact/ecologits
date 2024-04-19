<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="./docs/assets/logo_dark.png">
    <img alt="EcoLogits" src="./docs/assets/logo_light.png">
  </picture>
</p>

🌱 **EcoLogits** tracks the energy and environmental footprint of using generative AI models through APIs.


## ⚙️ Installation

```shell
pip install ecologits
```

## 🚀 Usage

```python
from ecologits import EcoLogits
from openai import OpenAI

EcoLogits.init()

client = OpenAI(
    api_key="<OPENAI_API_KEY>",
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Tell me a funny joke!"}
    ]
)

# Get estimated environmental impacts for that inference.
print(response.impacts)  # Impacts(energy=0.025, energy_unit='Wh', ...)
```



See package documentation on [EcoLogits](<link-to-mkdocs-material>)

## 💪 Contributing

### Requirements

Have [poetry](https://python-poetry.org/docs/#installation) installed on your system.


<details>
<summary>
Easy install using a virtualenv:
</summary>

Create a venv:

```shell
python3 -m venv .venv
source .venv/bin/activate
```

Install poetry:

```shell
pip install poetry
```

</details>


### Install project

```shell
poetry install --all-extras --with dev,docs
```


### Run tests

```shell
poetry run pytest
```


### Run pre-commit hooks locally

[Install pre-commit](https://pre-commit.com/)

```shell
pre-commit run --all-files
```
