Ecologits
============

**Ecologits** tracks and estimates the energy consumption and environmental impacts of using generative AI models through APIs.


## ⚙️ Installation

Coming soon...

## 🚀 Usage

```python
from ecologits import Ecologits
from openai import OpenAI

Ecologits.init()

client = OpenAI(
    api_key="<OPENAI_API_KEY>",
)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "user", "content": "Hello, can you explain what is the GenAI Impact project?"}
    ]
)

# Get estimated environmental impacts for that inference.
print(response.impacts)        # Impacts(energy=0.025, energy_unit='Wh', ...)
```



See package documentation on [Ecologits](<link-to-mkdocs-material>)

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
