# Methodology

## Evaluation methodologies

The following methodologies are **currently available and implemented in EcoLogits**:

- [x] [LLM Inference](llm_inference.md)

Upcoming methodologies ([join us](https://genai-impact.org/contact) to help speed up our progress):

- [ ] Embeddings
- [ ] Image Generation
- [ ] Multi-Modal

## Methodological background

EcoLogits employs the **Life Cycle Assessment (LCA) methodology**, as defined by ISO 14044, to estimate the environmental impacts of requests made to generative AI inference services. This approach focuses on **multiple phases** of the lifecycle, specifically raw material extraction, manufacturing, transportation (denoted as embodied impacts), usage and end-of-life. Notably, we do not cover the end-of-life phase due to data limitations on e-waste recycling.

Our assessment considers **three key environmental criteria**:

- Global Warming Potential (GWP): Evaluates the impact on global warming in terms of CO2 equivalents.
- Abiotic Resource Depletion for Elements (ADPe): Assesses the consumption of raw minerals and metals, expressed in antimony equivalents.
- Primary Energy (PE): Calculates energy consumed from natural sources, expressed in megajoules.

Using a **bottom-up modeling approach**, we assess and aggregate the environmental impacts of all individual service components. This method differs from top-down approaches by allowing precise allocation of each resource's impact to the overall environmental footprint.

Our current focus is on high-performance GPU-accelerated cloud instances, crucial for GenAI inference tasks. While we exclude impacts from training, networking, and end-user devices, we thoroughly evaluate the impacts associated with hosting and running the model inferences.

The methodology is grounded in **transparency** and **reproducibility**, utilizing open market and technical data to ensure our results are reliable and verifiable.

## Licenses and citations

All the methodologies are **licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">

Please ensure that you adhere to the license terms and properly cite the authors and the GenAI Impact non-profit organization when utilizing this work. Each methodology has an associated paper with specific citation requirements.
