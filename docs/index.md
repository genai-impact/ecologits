#

<figure markdown="span">
  ![EcoLogits](assets/logo_light.png#only-light)
  ![EcoLogits](assets/logo_dark.png#only-dark)
</figure>

**EcoLogits** tracks the energy consumption and environmental impacts of using generative AI models through APIs.


## Installation

```shell
pip install ecologits
```


## Usage

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
