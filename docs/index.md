#

<figure markdown="span">
  ![EcoLogits](assets/logo_light.png#only-light)
  ![EcoLogits](assets/logo_dark.png#only-dark)
</figure>

**EcoLogits** tracks the energy consumption and environmental impacts of using generative AI models through APIs. It supports major LLM providers such as OpenAI, Anthropic, Mistral AI and more (see [supported providers](tutorial/providers.md)).

EcoLogits was created and is actively maintained by the **[GenAI Impact :octicons-link-external-16:](https://genai-impact.org/) non-profit**.


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

Below is a simple example demonstrating how to use the GPT-4o-mini model from OpenAI with **EcoLogits** to track environmental impacts.

```python
from ecologits import EcoLogits
from openai import OpenAI

# Initialize EcoLogits
EcoLogits.init()

client = OpenAI(api_key="<OPENAI_API_KEY>")

response = client.chat.completions.create( # (1)!
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Tell me a funny joke!"}
    ]
)

# Get estimated environmental impacts of the inference
print(f"Energy consumption: {response.impacts.energy.value} kWh") # (2)!
print(f"GHG emissions: {response.impacts.gwp.value} kgCO2eq") # (3)!

# Get potential warnings
if response.impacts.has_warnings:
    for w in response.impacts.warnings:
        print(w) # (4)!

# Get potential errors
if response.impacts.has_errors:
    for w in response.impacts.errors:
        print(w) # (5)!
```

1. You don't need to change your code when making a request! :tada:
2. Total estimated energy consumption for the request in kilowatt-hour (kWh).
3. Total estimated greenhouse gas emissions for the request in kilogram of CO2 equivalent (kgCO2eq).
4. For `gpt-4o-mini`, you can expect two warnings: [`model-arch-not-released`](tutorial/warnings_and_errors.md#model-arch-not-released) and [`model-arch-multimodal`](tutorial/warnings_and_errors.md#model-arch-multimodal).
5. On this example you shouldn't get any errors.


### Impacts output in a nutshell 

**[`ImpactsOutput`][tracers.utils.ImpactsOutput]** object is returned for each request made to supported clients. It gathers, **[environmental impacts](tutorial/impacts.md)** and potential **[warnings and errors](tutorial/warnings_and_errors.md)**.

EcoLogits aims to give a comprehensive view of the environmental footprint of generative AI models at **inference**. Impacts are reported in total, but also **per life cycle phases**:

* **Usage**: related to the impacts of the energy consumption during model execution.
* **Embodied**: related to resource extraction, manufacturing and transportation of the hardware.

And, **multiple criteria**:

* **Energy**: related to the final electricity consumption in kWh. 
* **Global Warming Potential** (GWP): related to climate change, commonly known as GHG emissions in kgCO2eq.
* **Abiotic Depletion Potential for Elements** (ADPe): related to the depletion of minerals and metals in kgSbeq.
* **Primary Energy** (PE): related to the energy consumed from primary sources like oil, gas or coal in MJ. 

For detailed instructions on how to use the library, see our **[tutorial section](tutorial/index.md)**. If you want more details on the underlying impacts calculations, see our **[methodology section](methodology/index.md)**.


## License

This project is licensed under the terms of the [Mozilla Public License Version 2.0 (MPL-2.0) :octicons-link-external-16:](https://www.mozilla.org/en-US/MPL/2.0/).


## Acknowledgements

We extend our gratitude to [Data For Good :octicons-link-external-16:](https://dataforgood.fr/) and [Boavizta :octicons-link-external-16:](https://boavizta.org/en) for supporting the development of this project. Their contributions of tools, best practices, and expertise in environmental impact assessment have been invaluable.
