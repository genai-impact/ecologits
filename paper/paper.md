---
title: "EcoLogits: Evaluate the Environmental Impacts of Generative AI"
tags:
  - Python
  - Generative AI
  - Environmental Impact
  - Life Cycle Assessment
authors:
  - name: Samuel Rincé
    mail: samuel@genai-impact.org
    orcid: 0009-0000-0739-6114
    affiliation: "1,2"
  - name: Adrien Banse
    orcid: 0000-0002-4456-6618
    affiliation: "1,3"
affiliations:
  - name: GenAI Impact
    index: 1
  - name: Alygne
    index: 2
  - name: ICTEAM, UCLouvain, Belgium
    index: 3
date: TODO
bibliography: paper.bib
---

# Summary

Recent advancements in generative AI (GenAI), particularly Large Language Models (LLMs), have led to significant increases in computational power and energy demands. These models are not only becoming larger and more complex but are also being widely deployed across various platforms, reaching millions of users and developers. This widespread use has escalated the overall energy consumption and environmental impact associated with these technologies.

To address these concerns, we introduce EcoLogits, an open-source Python package designed to evaluate the environmental footprint of using GenAI models. EcoLogits enables users to estimate energy consumption and assess various environmental impacts — including carbon emissions, abiotic resource depletion, and primary energy consumption — associated with each API request to an GenAI service provider. Specifically, the tool implements a bottom-up Life Cycle Assessment (LCA) methodology, outlined in this paper and extensively described in the package documentation, covering both the usage impacts from direct energy consumption and the embodied impacts from hardware production and lifecycle. EcoLogits adheres to high standards of open-source practices, including versioning, automated testing, and comprehensive code documentation.

# Statement of need

While the recent developments in GenAI and LLMs offer tools of unprecedented quality, there is a general trend of increased energy consumption associated with these technologies. It is a known fact that the training process of large neural networks yields non-negligible carbon emissions [@lacoste_quantifying_2019; @patterson_carbon_2021]. Some industry actors communicate about the emissions of training their own models, such as Meta that reported the carbon emissions of training Llama models [@touvron_llama_2023; @touvron_llama_2023-1; @llama3modelcard_2024].

The major difference in recent years is that GenAI models are not only large models but are also used daily by millions of people on user-friendly websites such as OpenAI’s ChatGPT or via easy-to-use API clients written in popular languages such as Python or Javascript. The literature agrees on the fact that the share of carbon emissions from the inference is increasing [@patterson_carbon_2021; @desislavov_trends_2023] although these proportions vary among providers, with AWS reporting 80-90%, Google 60% and Meta 33% [@luccioni_power_2024].

Moreover although energy consumption is important, it is alone not sufficient for a comprehensive evaluation of the environmental impacts of training and inference. It is also crucial to include embodied impacts that come from raw material extraction, hardware manufacturing and transportation to end-use location. For LLMs such as BLOOM 176B, accounting for the embodied impacts increased the total carbon emissions by 22% for the training phase of the model [@luccioni_estimating_2022]. Environmental impacts evaluations of AI models should be more transparent and follow Life Cycle Assessment methodologies to be complete [@ligozat_unraveling_2022].

In parallel to the large deployment of energy-consuming models in the industry, there is a growing need for tools that automatically approximate their environmental impacts. While tools like CodeCarbon or Zeus [@codecarbon_2024; @zeus_2023] can track energy consumption and carbon emissions for locally-deployed models, estimating impacts becomes necessary when using external APIs from GenAI service providers. EcoLogits is the first Python library to approximate the environmental impacts of GenAI models inference via Python client calls. By adding `EcoLogits.init()` to their codebase, users can access the estimated energy consumption and the multi-phase impacts of their requests, including usage and embodied impacts for carbon emissions, abiotic resource depletion, and primary energy consumption.

# Methodology

## Methodological background

The **Attributional Life Cycle Assessment (A-LCA)** methodology defined by the ISO 14044 standard [@klopffer_life_1997; @boustead_lca_1996; @hunt_lca_1996] is used to properly estimate potential environmental impacts of products, processes, projects or services. In EcoLogits, we apply this methodology to estimate the impacts of a request to an GenAI inference service. The methodology encompasses multi-phases and multi-criteria environmental impacts.
Life cycle phases are usually defined as follows: raw material extraction, manufacturing, transportation, usage and end-of-life. The three first phases will be denoted as embodied impacts in this paper. Note that the end-of-life phase is not covered in this work mainly because we lack data and transparency on e-waste collection and recycling [@bordage_digital_2021; @forti_global_2020]. Transportation to the end-user location is not included; only transport from extraction sites to factories and between factories is accounted for.
We support three environmental impact criteria:

- Global Warming Potential (GWP), which evaluates the effects on global warming. Expressed in the amount of emitted greenhouse gas, in units of kilograms of carbon dioxide (CO2) equivalent [@ipcc_2013].
- Abiotic Resource Depletion for Elements (ADPe), which quantifies the use of raw minerals and metals. Expressed in kilograms of antimony (Sb) equivalent [@van_oers_abiotic_2020].
- Primary Energy (PE), which accounts for the quantity of energy consumed from natural sources such as raw fuels and other forms of energy. Expressed in megajoules [@frischknecht_cumulative_2015].

To estimate the impacts of a GenAI service we use a **bottom-up modeling approach**, i.e. we assess the environmental impacts of all components that compose the service individually and then aggregate and allocate these impacts to a request. This differs from a top-down approach and enables us to derive the proportion of contribution of each resource to the global impact.

The scope of our bottom-up methodology encompasses cloud compute primitives and data center extra equipment such as cooling (see \autoref{fig:boundaries}). More importantly we focus our study on high-performance GPU-accelerated cloud instances since they are commonly used for GenAI inference tasks. We currently do not include environmental impacts related to training the model nor the networking and end-user devices, but we evaluate the workloads related to hosting the model and running inference. 

<figure markdown="span">
  ![Scope and boundaries of our methodology focused on compute primitives \label{fig:boundaries}](figures/figure_boundaries.png)
</figure>

The methodology relies on open data to ensure that the results are transparent, reproducible and auditable. We use **market and technical data** such as components characteristics and **impact factors** that converts physical quantities to environmental impacts.

## Environmental impacts of GenAI service

The objective of the methodology is to assess the environmental impacts of a request made to an GenAI inference service, noted $I_{\text{request}}^{\alpha}$, where $\alpha$ is one the three different measures that we account for, that are GWP, ADPe and PE. We split each impact $I_{\text{request}}^{\alpha}$ into usage impacts, noted $I_{\text{request}}^{\text{u},\alpha}$, and embodied impacts, noted $I_{\text{request}}^{\text{e},\alpha}$: 
$$
I_{\text{request}}^{\alpha}=I_{\text{request}}^{\text{u},\alpha}+I_{\text{request}}^{\text{e},\alpha}.
$$

EcoLogits catches API requests made to GenAI inference service and input parameters such as the number of parameters of the model, noted $N_{\text{parameters}}$, or the number of generated tokens for an LLM, noted $N_{\text{output}}$. It returns both impacts $I_{\text{request}}^{\text{u},\alpha}$ and $I_{\text{request}}^{\text{e},\alpha}$, using the internal model outlined hereinafter and detailed in the package documentation[^1].

[^1]: See full and up-to-date methodology details at [https://ecologits.ai/latest/methodology/](https://ecologits.ai/latest/methodology/)


### Usage impacts

To compute the usage impacts $I_{\text{request}}^{\text{u},\alpha}$, we focus on the direct energy consumption $E_{\text{request}}$ of the IT equipment and data center operations that are involved when a request is made and convert it into an environmental impact with
$$
I_{\text{request}}^{\text{u},\alpha} = E_{\text{request}} \times F_{\text{em}}^{\alpha}, 
$$
where $F_{\text{em}}^{\alpha}$ is the impact factor of the electricity mix given at certain time and location [@ademe_base_empreinte]. We estimate $E_{\text{request}}$ as 
$$
E_{\text{request}} = \text{PUE} \times \left( E_{\text{server} \backslash \text{GPU}} + N_{\text{GPU}, \text{required}} \times E_{\text{GPU}} \right), 
$$
where $E_{\text{server} \backslash \text{GPU}}$ is the server overall energy consumption excluding the GPUs, $E_{\text{GPU}}$ is the GPU energy consumption, $N_{\text{GPU}, \text{required}}$ is the number of required GPUs used during inference, and PUE denotes the Power Usage Effectiveness, that accounts for the energy consumption overhead from the data center, typically set at 1.2 for hyperscalers [@uptimeinstitute_2024]. Finally we approximate $E_{\text{server} \backslash \text{GPU}}$ by the formula
$$
E_{\text{server} \backslash \text{GPU}} = \Delta T \times P_{\text{server} \backslash \text{GPU}} \times \frac{N_{\text{GPU}, \text{required}}}{N_{\text{GPU}, \text{available}}}, 
$$
where $P_{\text{server} \backslash \text{GPU}}$ is the average electric power of the server without GPUs (estimated from industry standard), $\Delta T$ is the generation latency and $N_{\text{GPU}, \text{available}}$ is the number of available GPUs in the server. For instance, in the case of LLMs, we make use of experimental data and benchmarks provided by the Hugging Face LLM-Perf Leaderboard [@llm-perf-leaderboard; @optimum-benchmark] to estimate $E_{\text{GPU}}$ and $\Delta T$. As illustrated in \autoref{fig:energy_latency}, it is a simple but good approximation to assume that $E_{\text{GPU}}$ and $\Delta T$ vary linearly with $N_{\text{output}}$ and $N_{\text{parameters}}$, that is
$$
\begin{split}
E_{\text{GPU}} &= N_{\text{output}} \times (a_1 \times N_{\text{parameters}} + b_1) \\
\Delta T &= N_{\text{output}} \times (a_2 \times  N_{\text{parameters}} + b_2), 
\end{split}
$$
where $a_1$, $b_1$, $a_2$, and $b_2$ are fitting parameters[^2]. 

[^2]: Note that the data points and linear regression models apply solely to the specific benchmark and hardware considered. Future releases of EcoLogits may utilize alternative data points and modeling techniques.

<figure markdown="span">
  ![Linear regressions based on LLM inference benchmarks to determine the energy (in Wh) and latency (in s) per token and number of parameters of the model. The $p$-value of both regressions are below 0.001. \label{fig:energy_latency}](figures/figure_energy_latency.png)
</figure>

### Embodied impacts

In order to estimate the embodied impacts $I_{\text{request}}^{\text{e},\alpha}$, we assume that when a request is made, the fraction of the server used for inference is given by $\frac{\Delta T}{\Delta L}$, where $\Delta L$ is the server lifespan, estimated to 5 years [@uptimeinstitute_2022]. Therefore, the request embodied impacts are given by
$$
I_{\text{request}}^{\text{e},\alpha} = \frac{\Delta T}{\Delta L} \times I^{\text{e},\alpha}_{\text{server}}, 
$$
where $I^{\text{e},\alpha}_{\text{server}}$ are the total embodied impacts inherent to the server. The latter are allocated either to the GPUs or to the rest of the server, and are given by
$$
I^{\text{e},\alpha}_{\text{server}} = \frac{N_{\text{GPU}, \text{required}}}{N_{\text{GPU}, \text{available}}} \times I^{\text{e},\alpha}_{\text{server} \backslash \text{GPU}} + N_{\text{GPU}, \text{required}} \times I^{\text{e},\alpha}_{\text{GPU}}.
$$

Finally the embodied impacts $I^{\text{e},\alpha}_{\text{server} \backslash \text{GPU}}$ and $I^{\text{e},\alpha}_{\text{GPU}}$ are estimated with the Boavizta methodology [@boaviztapi], that provides a bottom-up framework for impact assessment of cloud resources.

# Discussions 

Our approach for estimating the environmental impacts of GenAI inference services is built on a set of assumptions that align with industry standards. We focus on real-world deployments that use compressed models and high-performance data center hardware. However we know that this field is constantly evolving so we are committed to refining our methodology to keep up with new model architectures, optimization techniques, and hardware innovations. This is particularly relevant as trends shift from developing larger models to employing smaller models that are trained for extended periods or fine-tuned for specific tasks. Our tool allows GenAI practitioners to evaluate and compare these models based on their environmental footprints. In the future, we plan to expand our scope to include more stages of the model lifecycle and new modalities.

One challenge we face is dealing with proprietary models from companies that do not share details about their models and infrastructure. In these cases, we have to make educated guesses, such as estimating the number of parameters in models and which hardware is being used in production. We document these assumptions carefully and update them regularly as new models are released.

Finally, we want to mention deeper concerns about impact assessment of GenAI. Our current approach and tools are robust, but they do not capture the full range of environmental impacts associated with GenAI technologies. To get a complete picture, indirect impacts and potential rebound effects must be considered. Pursuing 'Green AI' means more than just making models smaller and more efficient - it requires a holistic view of the environmental changes driven by this technology, as well as its broader societal and service-level implications.

# Acknowledgements

We extend our gratitude to Geneviève Fleury, Yoann Couble, and Caroline Jean-Pierre for their thorough review of this paper and the methodology. Additionally, we appreciate the contributions of Fabrice Gentot, Flavien Henrion, Luc Berton, Ryane Hamami, Sakina Ouisrani, Vinh Nguyen, and Andrea Leylavergne to this project. Their collaborative efforts have greatly supported our research.

# References
