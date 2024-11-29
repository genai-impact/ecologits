# About proprietary models

EcoLogits has been designed from the ground up to assess the environmental footprint of generative AI models at the inference phase, including open and proprietary models. You can learn by reading our methodology that all our work is based on open science, open data and open models. This is mandatory to make sure that we can have a transparent and reproducible methodology to evaluate environmental impacts.

Transparency and reproducibility are crucial to ensure that users of EcoLogits can meaningfully use our tool with confidence and be aware of the limitations of these approach. One major limitation is about the impact assessment for proprietary models released and hosted by private AI providers. Below, we explain what is our approach to model the environmental impacts of proprietary models and sources of inaccuracies that comes along.


## Extrapolation from open models

Our methodology uses a bottom-up approach to model environmental impacts. This means we account for the physical infrastructure and resource consumption required to host generative AI services. Part of this modeling focuses on the AI models themselves, including:

- Model architecture (e.g., number of parameters)
- Deployment strategy and optimizations (e.g., backend types, quantization techniques)

For open models, obtaining this information is straightforward as the models are publicly available. However, for proprietary models, we must rely on extrapolations from open model characteristics. For example, to assess the energy consumption of a request, we use GPU energy consumption benchmarks from open models and apply them to proprietary models accordingly.


## Methodology to estimate the model architecture

For LLMs, key architectural aspects include whether the model is **dense** or a **mixture of experts (MoE)**, and the **model size** (number of parameters). To estimate these characteristics for proprietary models, we leverage various information sources such as **leaked data**, **evaluation benchmarks**, and **pricing information**. This process is manual and may be updated as new information becomes available. Below are some examples of how we determine specific model architectures.

### From leaked data

The model architecture of GPT-4 was leaked[^1] and estimated to be a sparse mixture of experts model with a total of 1.8 trillion parameters and 16 experts of 111 billion parameters each. The number of active experts during inference could be around 2. We used this information to add GPT-4 to EcoLogits with a range of active experts between 2 and 8 (~half of the models), so active parameters are between 220B and 880B.

### From evaluation benchmarks

At the time of release Claude 3 Opus from Anthropic had about the same performance on general benchmarks such as MMLU of HelloSwag[^2]. That is why we considered that Claude 3 Opus was about the same size of GPT-4. The model size is estimated to be about 2 trillion parameters[^3], and we also consider that it is a sparse mixture of experts, just like GPT-4, with between 250B and 1000B active parameters.

### From pricing information

When OpenAI released GPT-4-Turbo we considered the model to a distilled version of GPT-4 which justified the price drop[^4]. We thus estimated that GPT-4-Turbo was a scaled down (2x when comparing output tokens price) architecture of GPT-4 and used the price difference to conclude that GPT-4-Turbo was a sparse mixture of experts of 880B total parameters and between 110B and 440B active parameters.


## Transparency and updates

To maintain transparency, we publish an [**additional document** :octicons-link-external-16:](https://docs.google.com/spreadsheets/d/1XkPTkrGxpwWpIVIxpVvgRJuInSZsqbndTQbFGcHhdd0/edit?usp=sharing) detailing our estimations for model architectures. This document is regularly updated to stay in sync with new releases of EcoLogits.

The full list of supported models is also available [on GitHub :octicons-link-external-16:](https://github.com/genai-impact/ecologits/blob/main/ecologits/data/models.json).


[^1]: Tweet from Yam Peleg ([https://archive.ph/2RQ8X](https://archive.ph/2RQ8X))
[^2]: Claude 3 family ([https://www.anthropic.com/news/claude-3-family](https://www.anthropic.com/news/claude-3-family))
[^3]: LifeArchitect memo on Claude 3 Opus ([https://lifearchitect.substack.com/p/the-memo-special-edition-claude-3](https://lifearchitect.substack.com/p/the-memo-special-edition-claude-3))
[^4]: OpenAI GPT-4-Turbo official release ([https://openai.com/index/new-models-and-developer-products-announced-at-devday/](https://openai.com/index/new-models-and-developer-products-announced-at-devday/))

