---
title: "EcoLogits: Evaluating the Environmental Impacts of Generative AI"
tags:
  - Python
  - Generative AI
  - Environmental Impact
  - Life Cycle Assessment
authors:
  - name: Samuel Rincé
    mail: samuel@genai-impact.org
    orcid: 0009-0000-0739-6114
    affiliation: "1"
  - name: Adrien Banse
    orcid: 0000-0002-4456-6618
    affiliation: "1,2"
affiliations:
  - name: GenAI Impact
    index: 1
  - name: ICTEAM, UCLouvain, Belgium
    index: 2
date: TODO
bibliography: paper.bib
---

# Summary

Recent advancements in *Generative AI (GenAI)*, particularly Large Language Models (LLMs), have led to significant increases in computational power and energy demands. These models are not only becoming larger and more complex but are also being widely deployed across various platforms, reaching millions of users and developers. This widespread use has escalated the overall energy consumption and environmental impact associated with these technologies.

To address these concerns, we introduce EcoLogits, an open-source Python package designed to evaluate the environmental footprint of using GenAI models. EcoLogits estimates energy consumption and multi-criteria environmental impacts of GenAI API requests using a bottom-up Life Cycle Assessment methodology, considering both direct energy use and hardware production impacts.

# Statement of need

While the recent developments in GenAI offer tools of unprecedented quality, there is a general trend of increased energy consumption associated with these technologies [@de_vries_growing_2023]. It is a well-known fact that training large neural networks yield non-negligible carbon emissions [@lacoste_quantifying_2019; @patterson_carbon_2021]; Some industry actors communicate about the emissions of training their own models, such as Meta that estimated carbon emissions of Llama models [@touvron_llama_2023; @touvron_llama_2023-1; @llama3modelcard_2024].

The major difference in recent years is that GenAI models are not only large models but are also widely used by millions of people through web application such as OpenAI's ChatGPT or via APIs. The literature agrees on the fact that the share of carbon emissions from the serving of GenAI models (inference) is increasing [@patterson_carbon_2021; @desislavov_trends_2023], although these proportions vary among providers, with AWS reporting 80-90%, Google 60% and Meta 33% [@luccioni_power_2024].

Moreover, while energy consumption is important, it alone is insufficient for a comprehensive evaluation of the environmental impacts of training and inference. It is crucial to include embodied impacts that come from hardware production. For LLMs such as BLOOM 176B, accounting for the embodied impacts increased the total carbon emissions by 22% during the training phase of the model [@luccioni_estimating_2022]. Environmental impacts evaluations of AI models should be more transparent and follow *Life Cycle Assessment (LCA)* methodologies to be complete [@ligozat_unraveling_2022].

In parallel to the large deployment of energy-consuming models in the industry, there is a growing need for tools that automatically approximate their environmental impacts. While tools like CodeCarbon or Zeus[^1] [@codecarbon_2024; @zeus_2023] can track energy consumption and carbon emissions for locally-deployed models, estimating impacts becomes necessary when using external APIs from GenAI service providers. EcoLogits is the first Python library to approximate the environmental impacts of GenAI models inference via Python client calls. By adding `EcoLogits.init()` to their codebase, users can access an estimation of the energy consumption and the environmental impacts of their requests.

[^1]: See https://github.com/mlco2/codecarbon and https://github.com/ml-energy/zeus. 

# Methodology

The **Attributional Life Cycle Assessment (A-LCA)** methodology defined by the ISO 14044 standard [@klopffer_life_1997; @boustead_lca_1996; @hunt_lca_1996] is used to properly estimate potential environmental impacts of products, processes, projects, or services. In EcoLogits, we apply this methodology to estimate the impacts of a request to a GenAI inference service. The methodology encompasses multi-phase and multi-criteria environmental impacts.

In our approach we consider the usage phase accounting for the direct energy consumption [@llm-perf-leaderboard; @optimum-benchmark] and the embodied phase accounting for the hardware production, including raw material extraction, manufacturing, and transportation [@boaviztapi]. We do not include the end-of-life phase for lack of data and transparency on e-waste collection and recycling [@bordage_digital_2021; @forti_global_2020]. EcoLogits reports an estimation of the direct energy consumption in addition to other environmental impact criteria such as *Global Warming Potential* [@ipcc_2013], *Abiotic Depletion Potential* [@van_oers_abiotic_2020] and *Primary Energy Consumption* [@frischknecht_cumulative_2015]. Assessing multiple impact criteria helps prevent pollution shifting that can result from optimizing for a single criterion.

To estimate the impacts of a GenAI service we use a **bottom-up modeling approach**, i.e. we individually assess the environmental impacts of components that frame the service, and then aggregate and allocate these impacts to a request. The scope of our methodology encompasses cloud compute primitives and data center extra equipment such as cooling (see \autoref{fig:boundaries}). We focus our study on high-performance GPU-accelerated cloud instances since they are commonly used for GenAI inference tasks. We do not account for other impacts related to model training, networking transfers, or end-user devices.

<figure markdown="span">
  ![Scope and boundaries of our methodology focused on compute primitives \label{fig:boundaries}](figures/figure_boundaries.png)
</figure>

# Discussions 

Our approach for estimating the environmental impacts of GenAI inference aligns with industry standards and focuses on real-world deployments. As the field is constantly evolving, we are committed to refining our methodology to keep up with new model architectures, optimization techniques, and hardware innovations. Our tool enables GenAI practitioners to evaluate and compare these models based on their environmental footprints. In the future, we plan to expand our scope to include more stages of the model life cycle and new modalities.

One challenge we face is dealing with proprietary models from companies that do not share details about their models and infrastructure. In these cases, we have to make educated guesses, such as estimating the number of parameters in models and which hardware is being used in production. We document these assumptions carefully and update them regularly as new models are released.

We wish to highlight deeper concerns about the impact assessment of GenAI. Our approach, while robust, does not capture the full range of environmental impacts associated with GenAI technologies. To get a complete picture, indirect impacts and potential rebound effects must also be considered. Pursuing "Green AI" means more than just making models smaller and more efficient; it requires a holistic view of the environmental changes driven by this technology, as well as its broader societal and service-level implications.

# Acknowledgements

We extend our gratitude to Geneviève Fleury, Yoann Couble, and Caroline Jean-Pierre for their thorough review of this paper and the methodology. Additionally, we appreciate the contributions of Fabrice Gentot, Flavien Henrion, Luc Berton, Ryane Hamami, Sakina Ouisrani, Vinh Nguyen, and Andrea Leylavergne to this project. Their collaborative efforts have greatly supported our research.

# References
