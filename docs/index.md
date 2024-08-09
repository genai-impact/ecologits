#

<figure markdown="span">
  ![EcoLogits](assets/logo_light.png#only-light)
  ![EcoLogits](assets/logo_dark.png#only-dark)
</figure>

**EcoLogits** tracks the energy consumption and environmental impacts of using generative AI models through APIs. It supports major LLM providers such as OpenAI, Anthropic, Mistral AI and more (see [supported providers](tutorial/providers.md)).


## Requirements

Python 3.9+

EcoLogits relies on key libraries to provide essential functionalities:

* [Pydantic :octicons-link-external-16:](https://docs.pydantic.dev/) for data modeling.
* [Wrapt :octicons-link-external-16:](https://wrapt.readthedocs.io/) for function patching.


## Installation

<p><strong>Select providers</strong></p>
<span class="provider-item">
    <input type="checkbox" id="anthropic" value="anthropic" class="provider-option">
    <label for="anthropic">Anthropic</label>
</span>
<span class="provider-item">
    <input type="checkbox" id="cohere" value="cohere" class="provider-option">
    <label for="cohere">Cohere</label>
</span>
<span class="provider-item">
    <input type="checkbox" id="google-generativeai" value="google-generativeai" class="provider-option">
    <label for="google-generativeai">Google Gemini</label>
</span>
<span class="provider-item">
    <input type="checkbox" id="huggingface-hub" value="huggingface-hub" class="provider-option">
    <label for="huggingface-hub">Hugging Face Inference Endpoints</label>
</span>
<span class="provider-item">
    <input type="checkbox" id="litellm" value="litellm" class="provider-option">
    <label for="litellm">LiteLLM</label>
</span>
<span class="provider-item">
    <input type="checkbox" id="mistralai" value="mistralai" class="provider-option">
    <label for="mistralai">Mistral AI</label>
</span>
<span class="provider-item">
    <input type="checkbox" id="openai" value="openai" checked="checked" class="provider-option">
    <label for="openai">OpenAI</label>
</span>

<p><strong>Run this command</strong></p>
<pre><code id="install-command"></code></pre>
<script src="js/installer.js"></script>

For detailed instructions on each provider, refer to the complete list of [supported providers and features](tutorial/providers.md). It is also possible to install EcoLogits without any provider.


## Usage Example

Below is a simple example demonstrating how to use the GPT-3.5-Turbo model from OpenAI with EcoLogits to track environmental impacts.

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

Environmental impacts are quantified based on four criteria and across two phases:

Criteria:

- **Energy** (energy): Final energy consumption in kWh,
- **Global Warming Potential** (gwp): Potential impact on global warming in kgCO2eq (commonly known as GHG/carbon emissions),
- **Abiotic Depletion Potential for Elements** (adpe): Impact on the depletion of non-living resources such as minerals or metals in kgSbeq,
- **Primary Energy** (pe): Total energy consumed from primary sources in MJ.

Phases:

- **Usage** (usage): Represents the phase of energy consumption during model execution,
- **Embodied** (embodied): Encompasses resource extraction, manufacturing, and transportation phases associated with the model's lifecycle.

!!! info "Learn more about environmental impacts assessment in the [methodology](methodology/index.md) section."


## License

This project is licensed under the terms of the [Mozilla Public License Version 2.0 (MPL-2.0) :octicons-link-external-16:](https://www.mozilla.org/en-US/MPL/2.0/).


## Acknowledgements

**EcoLogits** is actively developed and maintained by [GenAI Impact :octicons-link-external-16:](https://genai-impact.org/) non-profit. We extend our gratitude to [Data For Good :octicons-link-external-16:](https://dataforgood.fr/) and [Boavizta :octicons-link-external-16:](https://boavizta.org/en) for supporting the development of this project. Their contributions of tools, best practices, and expertise in environmental impact assessment have been invaluable.
