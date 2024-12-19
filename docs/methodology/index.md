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

Using a **bottom-up modeling approach**, we assess and aggregate the environmental impacts of all individual service components within scope. This method differs from top-down approaches by allowing precise allocation of each resource's impact to the overall environmental footprint. The key advantage of bottom-up modeling is that our methodology can be customized for each provider that share information.

Our method computes **high-confidence approximation intervals**, providing a range of values within which we are confident enough that the true consumption lies.

Our current focus is on high-performance GPU-accelerated cloud instances, crucial for GenAI inference tasks. While we exclude impacts from training, networking, and end-user devices, we thoroughly evaluate the impacts associated with hosting and running the model inferences.

The methodology is grounded in **transparency** and **reproducibility**, utilizing open market and technical data to ensure our results are reliable and verifiable.

## Scope of the methodology

Our methodology focuses on **assessing the environmental impacts of GenAI inference tasks**. That is why we exclude impacts from training, networking and end-used devices, we thoroughly evaluate the impacts associated with hosting and running the model inferences.

<figure markdown="span">
  ![Figure: Energy consumption per output token vs. number of active parameters ](../assets/methodology/llm/figure_boundaries.png)
  <figcaption>Boundaries of our impact assessment methodology.</figcaption>
</figure>

Because evaluating the environmental footprint of GenAI services is hard we make some **assumptions** to simplify the assessment. In the following section we will describe general hypotheses that we use, if you want to learn more about the specifics look at the according methodology page.  


## Hypotheses and limitations

To be able to estimate environmental impacts of generative AI services at inference we took the approach of modeling the key components that compose the service. In this section we will list major assumptions we make when modeling environmental impacts as well as known limitations. When possible we will try to quantify the potential inaccuracies.

!!! note "The hypotheses and limitations listed in this section are intentionally high-level. To get the full details you will need to dive into the methodology."

### On models

Two major information we are looking for is the required infrastructure to host the AI model, such as the number of GPUs as well as the energy consumption that results from doing an inference on the model.

Assuming the **required infrastructure** for open models can be relatively straightforward because the model size is known. But for proprietary models this can very be challenging given that some AI provider do not disclose any technical information on that matter. That's why we rely on estimations of parameters count for closed models, to learn more [read the dedicated section](proprietary_models.md).

Assuming the **energy consumption** for AI models is done through benchmarking open models. We tend to rely on external sources for benchmarking, but we conduct our own experiments as well. Because of our limited capacity and the technical complexity to host very big AI models we extrapolate the consumption of smaller models to bigger models.

**Limitations:**

* We do not account for other inference optimizations such as flash attention or batching.
* We do not benchmark models bigger than 70 billion parameters.
* We do not have benchmarks for multi-GPU deployments.
* We do not account for the multiple modalities of a model.

### On hardware

We estimate the **required infrastructure** to run the service in terms of hardware. We consider that the service is hosted in the cloud on servers equipped with high-end GPUs. 

**Limitations:**

* We do not account for TPUs or other type of accelerators.
* We do not account for networking or storage primitives.
* We do not account for infrastructure overheads or utilization factors.

### On data centers

The type of services we model rely on high-end hardware that we consider is hosted by cloud service providers. Thus, we model data centers impacts as well and especially the overhead for cooling equipments.

We consider the **Power Usage Effectiveness** (PUE) metric from data centers. These values can be quite complicated to get from the providers themselves. A good amount of data is available for providers that build their own data centers (such as hyperscalers). But part of the AI workloads are also located in non-hyperscale data centers or in co-located data centers. That's why we prefer to rely on a global average for PUE that can be overridden for providers that disclose more precise data.

**Limitations:**

* We do not account for the specific infrastructure or way to cooldown servers in data centers.
* We do not account for the overhead of the cloud provider for internal services like backing up or monitoring.

### On electricity mix

Because getting precise information on where the consumption happens and in which data center we also rely on global averages for the environmental impacts of electricity consumption by cloud providers. By default, we use a worldwide value, and have country specific values that can be customized by the end-user or when the provider disclose more precise data on AI workload location.

**Limitations:**

* We do not account for local electricity generation for data centers, whether it be renewable energy (e.g. solar panels) or fossil fuels (e.g. diesel generators) 
* We do not account for regional electricity mixes the smallest supported zone is a country.

### On embodied impacts

We aim at covering the largest scope possible when assessing the environmental impacts. That is why we rely extensively on the work done by [Boavizta](https://boavizta.org/) non-profit. Unfortunately, assessing the environmental impacts of resources extraction, hardware manufacturing and transportation is very challenging mainly due to a lack of transparency from all the organizations that are involved. Estimations of the inaccuracies are currently not supported within Boavizta's methodology and tool ([BoaviztAPI](https://doc.api.boavizta.org/)).


## Licenses and citations

All the methodologies are **licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">

Please ensure that you adhere to the license terms and properly cite the authors and the GenAI Impact non-profit organization when utilizing this work. Each methodology has an associated paper with specific citation requirements.
