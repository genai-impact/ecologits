# Environmental Impacts of LLM Inference

## Introduction

The environmental impacts of a request, $I_{\text{request}}$ to a Large Language Model (LLM) can be divided into two components: the usage impacts, $I_{\text{request}}^{\text{u}}$, which account for energy consumption, and the embodied impacts, $I_{\text{request}}^{\text{e}}$, which account for resource extraction, hardware manufacturing, and transportation:

$$
\begin{equation*}
\begin{split}
I_{\text{request}}&=I_{\text{request}}^{\text{u}}  + I_{\text{request}}^{\text{e}} \\ 
&= E_{\text{request}} \times F_{\text{em}}+\frac{\Delta T}{\Delta L} \times I_{\text{server}}^{\text{e}}, 
\end{split}
\end{equation*}
$$

where $E_{\text{request}}$ represents the energy consumption of the IT resources associated with the request. $F_{\text{em}}$ denotes the impact factor of electricity consumption, which varies depending on the location and time. Furthermore, $I_{\text{server}}^{\text{e}}$ captures the embodied impacts of the IT resources, and $\frac{\Delta T}{\Delta L}$ signifies the hardware utilization factor, calculated as the computation time divided by the lifetime of the hardware.


## Usage impacts

To assess the usage impacts of an LLM inference, we first need to estimate the energy consumption of the server, which is equipped with one or more GPUs. We will also take into account the energy consumption of cooling equipment integrated with the data center, using the Power Usage Effectiveness (PUE) metric.

Subsequently, we can calculate the environmental impacts by using the $F_{\text{em}}$ impact factor of the electricity mix. Ideally, $F_{\text{em}}$ should vary with location and time to accurately reflect the local energy mix.

### Modeling GPU energy consumption

By leveraging the open dataset from the [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/?__theme=light), we can estimate the energy consumption of the GPU using a parametric model. This leaderboard aims at being as close as possible to production conditions (vLLM on NVIDIA H100 GPUs, see [the paper](https://arxiv.org/pdf/2505.06371) for more information). 

??? info "On the ML.ENERGY dataset filtering"
    
    We have filtered the dataset to keep only the benchmark on NVIDIA H100 80GB HBM3 GPUs. 

We approximate energy consumption per output token as a function of the number of activate parameters, denoted as $P_{\text{active}}$, and the batching size, denoted as $B$. 

??? note "What are active parameters?"

    We distinguish between active parameters and total parameter count for Sparse Mixture-of-Experts (SMoE) models. The total parameter count is used to determine the number of required GPUs to load the model into memory. In contrast, the active parameter count is used to estimate the energy consumption of a single GPU. In practice, SMoE models exhibit lower energy consumption per GPU compared to dense models of equivalent size (in terms of total parameters).

    * For a dense model: $P_{\text{active}} = P_{\text{total}}$
    * For a SMoE model: $P_{\text{active}} =  P_{\text{total}} / \text{number of active experts}$

??? note "What is the batching size "

    The batching size $B$ is the number of requests that the server can handle concurrently. A large batching size decreases the energy used for a unique request, but increases the latency. The providers aim at finding a good tradeoff between energy efficiency and latency. 

In order to being consistent with physics (and fit the data) while staying relatively simple, we opted for a function of the form 

$$ 
f_E(P_{\text{active}}, B) = \alpha P_{\text{active}} + \beta B + \gamma P_{\text{active}} B + \delta B^2 + \eta, 
$$

that is a function that is **linear** with $P_{\text{active}}$ and **quadratic** with $B$. We fitted such a model with the data, and got 

- $\alpha = 4.36 \times 10^{-6}$, 
- $\beta = -2.93 \times 10^{-7}$, 
- $\gamma = -2.43 \times 10^{-9}$, 
- $\delta = 2.43 \times 10^{-10}$, 
- $\eta = 6.02 \times 10^{-5}$.

The result is illustrated below. 

<figure markdown="span">
  ![Figure: Energy consumption per output token vs. number of active parameters ](../assets/methodology/llm/figure_energy.png)
  <figcaption>Figure: Energy consumption (in Wh) per output token vs. number of active parameters (in billions). The points are the datapoints from the ML.ENERGY leaderboard, and the lines are the result of our regression for fixed batching sizes (64, 128, 256, 512, 1024).</figcaption>
</figure>

!!! warning "From now on, we consider that the batching size fixed to $B = 64$."


Using these values, we can estimate the energy consumption of a simple GPU for the entire request, given the number of output tokens $\#T_{\text{out}}$ and the number of active parameters $P_{\text{active}}$: 

$$ 
E_{\text{GPU}}(\#T_{\text{out}}, P_{\text{active}}) = \#T_{\text{out}} \times f_E(P_{\text{active}}, 64), 
$$

where $f_E$ is the linear-quadratic model cited above. 

If the model requires multiple GPUs to be loaded into VRAM, the energy consumption $E_{\text{GPU}}$ should be multiplied by the number of required GPUs, $\text{GPU}$ (see [below](#complete-server-energy-consumption)).


### Modeling server energy consumption

To estimate the energy consumption of the entire server, we will use the previously estimated GPU energy model and separately estimate the energy consumption of the server itself (without GPUs), denoted as $E_{\text{server} \backslash \text{GPU}}$.

#### Server energy consumption without GPUs

To model the energy consumption of the server without GPUs, we consider a fixed power consumption, $W_{\text{server} \backslash \text{GPU}}$, during inference (or generation latency), denoted as $\Delta T$. We assume that the server hosts multiple GPUs, but not all of them are actively used for the target inference. Therefore, we account for a portion of the energy consumption based on the number of required GPUs, $\text{GPU}$:

$$
E_{\text{server} \backslash \text{GPU}}(\Delta T) = \Delta T \times W_{\text{server} \backslash \text{GPU}} \times \frac{\text{GPU}}{\#\text{GPU}_{\text{installed}}}.
$$

For a typical high-end GPU-accelerated cloud instance, we use $W_{\text{server} \backslash \text{GPU}} = 1$ kW and $\#\text{GPU}_{\text{installed}} = 8$.

#### Estimating the generation latency

The generation latency, $\Delta T$, is the duration of the inference measured on the server and is independent of networking latency. We estimate the generation latency using the [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/?__theme=light) dataset with the previously mentioned filters applied.

We fit a function $f_L(P_{\text{active}}, B)$ (of the same form as $f_E$ above) on the dataset, and find 

- $\alpha = 3.50 \times 10^{-4}$, 
- $\beta = 3.53 \times 10^{-4}$, 
- $\gamma = 5.91 \times 10^{-8}$, 
- $\delta = -1.10 \times 10^{-7}$, 
- $\eta = 0.027$.

The result is illustrated below. 

<figure markdown="span">
  ![Figure: Latency per output token vs. number of active parameters ](../assets/methodology/llm/figure_latency.png)
  <figcaption>Figure: Latency (in s) per output token vs. number of active parameters (in billions). The points are the datapoints from the ML.ENERGY leaderboard, and the lines are the result of our regression for fixed batching sizes (64, 128, 256, 512, 1024)</figcaption>
</figure>

Using these values, we can estimate the generation latency for the entire request given the number of output tokens, $\#T_{\text{out}}$, and the number of active parameters, $P_{\text{active}}$. When possible, we also measure the request latency, $\Delta T_{\text{request}}$, and use it as the maximum bound for the generation latency:

$$
\Delta T(\#T_{\text{out}}, P_{\text{active}}, \Delta T_{\text{request}}) = \min \left\{ \#T_{\text{out}} \times f_L(P_{\text{active}}, 64), \Delta T_{\text{request}} \right\}.
$$

#### Estimating the number of active GPUs

To estimate the number of required GPUs, $\text{GPU}$, to load the model in virtual memory, we divide the required memory to host the LLM for inference, noted $M_{\text{model}}$, by the memory available on one GPU, noted $M_{\text{GPU}}$.

The required memory to host the LLM for inference is estimated based on the total number of parameters and the number of bits used for model weights related to quantization. We also apply a memory overhead of $1.2$ (see [Transformers Math 101 :octicons-link-external-16:](https://blog.eleuther.ai/transformer-math/#total-inference-memory)):

$$
M_{\text{model}}(P_{\text{total}},Q)=1.2 \times \frac{P_{\text{total}} \times Q}{8}.
$$

We then estimate the number of required GPUs, rounded up:

$$
\text{GPU}(P_{\text{total}},Q,M_{\text{GPU}}) = \left\lceil \frac{M_{\text{model}}(P_{\text{total}},Q)}{M_{\text{GPU}}} \right\rceil.
$$

To stay consistent with previous assumptions based on [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/?__theme=light) data, we use $M_{\text{GPU}} = 80$ GB for an NVIDIA H100 80GB GPU.

#### Complete server energy consumption

The total server energy consumption for the request, $E_{\text{server}}$, is computed as follows:

$$
E_{\text{server}} = E_{\text{server} \backslash \text{GPU}} + \text{GPU} \times E_{\text{GPU}}.
$$

### Modeling request energy consumption

To estimate the energy consumption of the request, we multiply the previously computed server energy by the Power Usage Effectiveness (PUE) to account for cooling equipment in the data center:

$$
E_{\text{request}} = \text{PUE} \times E_{\text{server}}.
$$

We typically use a $\text{PUE} = 1.2$ for hyperscaler data centers or supercomputers.

### Modeling request usage environmental impacts

To assess the environmental impacts of the request for the usage phase, we multiply the estimated electricity consumption by the impact factor of the electricity mix, $F_{\text{em}}$, specific to the target country and time. **Unless otherwise stated, we currently use a worldwide average multicriteria impact factor from the [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/)**:

$$
I^\text{u}_{\text{request}} = E_{\text{request}} \times F_{\text{em}}.
$$

Note that the user can still chose another electricity mix from the [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/).

??? note "Some values of $F_{\text{em}}$ per geographical area"
        
    | Area or country                                                           | GWP (gCO2eq / kWh) | ADPe (kgSbeq / kWh) | PE (MJ / kWh) |
    |---------------------------------------------------------------------------|--------------------|---------------------|---------------|
    | 🌐 Worldwide                                                              | $590.4$            | $7.378 \times 10^{-8}$   | $9.99$  |
    | 🇪🇺 Europe ([EEA](https://en.wikipedia.org/wiki/European_Economic_Area)) | $509.4$            | $6.423 \times 10^{-8}$   | $12.9$  |
    | 🇺🇸 USA                                                                  | $679.8$            | $9.855 \times 10^{-8}$   | $11.4$  |
    | 🇨🇳 China                                                                | $1,057$            | $8.515 \times 10^{-8}$   | $14.1$  |
    | 🇫🇷 France                                                               | $81.3$            | $4.858 \times 10^{-8}$   | $11.3$     |

### Modeling request usage water impact

- Water Consumption Footprint (WCF): Water consumption from this request. The formula for quantifying this is:

$$
\begin{equation}
\begin{aligned}
\text{WCF}_{\text{request}} &= \frac{E_\text{server}}{N_\text{requests}} \times \left[\text{WUE}_{\text{on-site}} + \text{PUE} \times \text{WUE}_\text{off-site} \right] \\
&\quad + \frac{\Delta T}{\Delta L} \times \frac{\text{WCF}_\text{embodied}}{N_\text{requests}}
\end{aligned}
\end{equation}
$$

Where

* $WCF_{request}$ : Water consumption footprint for the request
* $E_{\text{server}}$ : Energy cost at the server for the request 
* ${N_{requests}}$ : Number of simultanous reqeusts handled by the server
* $WUE_{on-site}$ : Water usage efficiency at the data center 
* $PUE$: Power usage efficiency at the data center 
* $WUE_{off-site}$ : Water usage efficiency of the local electricity mix 
* ${\Delta T}$ : Generation latency, or the time it takes for the server to process the request, in seconds
* ${\Delta L}$ : Server lifespan in seconds
* ${WCF_{embodied}}$ : Embodied water consumption footprint for manufacturing the server

A table of the AI providers and the datacenter providers whose PUE and WUE we use to calculate their WCF is given by:  

| AI Provider      | Datacenter Provider | Source |
|------------------|---------------------|--------|
| Anthropic        | Google              |[source](https://www.aboutamazon.com/news/company-news/amazon-aws-anthropic-ai)|
| MistralAI        | Unsure > EU average |        |
| Cohere           | Unsure > EU average |        |
| Databricks       | AWS and Google      |[source](https://www.databricks.com/legal/cloud-provider-directory#:~:text=Azure%20Databricks%20)|
| Meta             | Meta                |[source](https://www.theguardian.com/technology/2025/jul/16/zuckerberg-meta-data-center-ai-manhattan)|
| Azure OpenAI     | Microsoft           |[source](https://datacenters.microsoft.com/)|
| Hugging Face Hub | AWS                 |[source](https://huggingface.co/docs/sagemaker/index)|
| Google           | Google              |[source](https://deepmind.google/discover/blog/deepmind-ai-reduces-google-data-centre-cooling-bill-by-40/?utm_source=chatgpt.com)|
| Microsoft        | Microsoft           |[source](https://azure.microsoft.com/en-us/products/phi?utm_source=chatgpt.com)|
| OpenAI           | Unsure > EU average |        |

In the case that the datacenter provider is unsure, we use the EU average.  
For each datacenter provider, we use their globally averaged PUE number.  
  
| Datacenter Provider | PUE  | Source |
|---------------------|------|--------|
| Google              | 1.09 | [source](https://www.gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf) |
| Meta                | 1.09 | [source](https://sustainability.atmeta.com/data-centers/) |
| Microsoft           | 1.18 | [source](https://azure.microsoft.com/en-us/blog/how-microsoft-measures-datacenter-water-and-energy-use-to-improve-azure-cloud-sustainability/) |
| OVHCloud            | 1.26 | [source](https://corporate.ovhcloud.com/en/sustainability/environment/) |
| Scaleway            | 1.37 | [source](https://www-uploads.scaleway.com/Impact_Report2024_A4_EN_e63efcae20.pdf) |
| AWS                 | 1.15 | [source](https://sustainability.aboutamazon.com/products-services/aws-cloud) |
| Equinix             | 1.42 | [source](https://www.equinix.com/content/dam/eqxcorp/en_us/documents/resources/infopapers/ip_2023_sustainability_en.pdf) |
| EU Average          | 1.56 | [source](https://www.europeanlawblog.eu/pub/1jb3tzus/release/2#:~:text=According%20to%20the%20current%20state,source%20of%20its%20GHG%20emissions.) |
  
The $WUE_{on-site}$ of each datacenter provider:
  
| Datacenter Provider   | WUE   | Source |
|-----------------------|-------|--------|
| Google                | 0.916 | [source](https://www.gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf) |
| Meta                  | 0.18  | [source](https://sustainability.atmeta.com/wp-content/uploads/2024/08/Meta-2024-Sustainability-Report.pdf) |
| Microsoft             | 0.49  | [source](https://azure.microsoft.com/en-us/blog/how-microsoft-measures-datacenter-water-and-energy-use-to-improve-azure-cloud-sustainability/) |
| OVHCloud              | 0.37  | [source](https://corporate.ovhcloud.com/en/sustainability/environment/) |
| Scaleway              | 0.216 | [source](https://www-uploads.scaleway.com/Impact_Report2024_A4_EN_e63efcae20.pdf) |
| AWS                   | 0.18  | [source](https://sustainability.aboutamazon.com/2023-report) |
| Equinix               | 1.07  | [source](https://www.equinix.com/resources/infopapers/2023-corporate-sustainability-report) |
| EU Colocation Average | 0.31  | [source](https://www.eudca.org/documents/content/E8VdyUuATTC_BmbNp4nhAwo89?download=0) |

We could not find the number for the EU averaged hyperscaler WUE, so we use the number for EU colocation average.

Finally, for $WUE_{off-site}$, we take the data from a [report](https://www.wri.org/research/guidance-calculating-water-use-embedded-purchased-electricity) by the [World Resource Institue](https://www.wri.org). For brevity, we will not list the list of countries here. For the countries whose data is missing, the user will get a userwarning along with the result telling them that the global average is used.   

## Embodied impacts

To determine the embodied impacts of an LLM inference, we need to estimate the **hardware configuration** used to host the model and its lifetime. Embodied impacts account for resource extraction (e.g., minerals and metals), manufacturing, and transportation of the hardware.

### Modeling server embodied impacts

To estimate the embodied impacts of IT hardware, we use the [BoaviztAPI](https://github.com/Boavizta/boaviztapi) tool from the non-profit organization [Boavizta](https://boavizta.org/en/). This API embeds a bottom-up multicriteria environment impact estimation engine for embodied and usage phases of IT resources and services. We focus on estimating the embodied impacts of a server and a GPU. BoaviztAPI is an open-source project that relies on open databases and open research on environmental impacts of IT equipment.

#### Server embodied impacts without GPU

To assess the embodied environmental impacts of a high-end AI server, we use an AWS cloud instance as a reference. We selected the `p4de.24xlarge` instance, as it corresponds to a server that can be used for LLM inference with eight NVIDIA H100 80GB GPU cards. The embodied impacts of this instance will be used to estimate the embodied impacts of the server without GPUs, denoted as $I^{\text{e}}_{\text{server} \backslash \text{GPU}}$.

The embodied environmental impacts of the cloud instance are:

|                 | Server (without GPU) |
|-----------------|----------------------|
| GWP (kgCO2eq)   | $3000$               |
| ADPe (kgSbeq)   | $0.25$               |
| PE (MJ)         | $39,000$             |

!!! warning "These impacts do not take into account the eight GPUs. ([see below](#gpu-embodied-impacts))"

??? info "Example request to reproduce this calculation"

    On the cloud instance route (/v1/cloud/instance) you can POST the following JSON.
    
    ```json
    {
        "provider": "aws",
        "instance_type": "p4de.24xlarge"
    }
    ```

    Or you can use the demo available demo API with this command using `curl` and parsing the JSON output with `jq`.

    ```shell
    curl -X 'POST' \
        'https://api.boavizta.org/v1/cloud/instance?verbose=true&criteria=gwp&criteria=adp&criteria=pe' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -d '{
        "provider": "aws",
        "instance_type": "p4de.24xlarge"
    }' | jq
    ```

#### GPU embodied impacts

According to this [NVIDIA datasheet](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-H100-PCF-Summary.pdf), a NVIDIA H100 80GB GPU has a GWP of 164 kgCO2eq. To approximate the ADPe and PE, we rely on the Boavizta methodology for previous A100 GPUs. These values will be used to estimate the embodied impacts of a single GPU, denoted as $I^{\text{e}}_{\text{GPU}}$.

|                | NVIDIA H100 80GB      |
|----------------|-----------------------|
| GWP (kgCO2eq)  | $164$                 |

|                | NVIDIA A100 80GB      |
|----------------|-----------------------|
| ADPe (kgSbeq)  | $5.09 \times 10^{-3}$ |
| PE (MJ)        | $1,828$               |

!!! warning "The GPU embodied impacts will be soon available in the BoaviztAPI tool."


#### Complete server embodied impacts

The final embodied impacts for the server, including the GPUs, are calculated as follows. Note that the embodied impacts of the server without GPUs are scaled by the number of GPUs required to host the model. This allocation is made to account for the fact that the remaining GPUs on the server can be used to host other models or multiple instances of the same model. As we are estimating the impacts of a single LLM inference, we need to exclude the embodied impacts that would be attributed to other services hosted on the same server:

$$
I^{\text{e}}_{\text{server}}=\frac{\text{GPU}}{\#\text{GPU}_{\text{installed}}} \times I^{\text{e}}_{\text{server} \backslash \text{GPU}} + \text{GPU} \times I^{\text{e}}_{\text{GPU}}.
$$


### Modeling request embodied environmental impacts

To allocate the server embodied impacts to the request, we use an allocation based on the hardware utilization factor, $\frac{\Delta T}{B \times \Delta L}$. In this case, $\Delta L$ represents the lifetime of the server and GPU, which we fix at 3 years (according to [this NVIDIA report](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-H100-PCF-Summary.pdf)), and $B$ is the batching size such as above: 

$$
I^{\text{e}}_{\text{request}}=\frac{\Delta T}{B \times  \Delta L} \times I^{\text{e}}_{\text{server}}.
$$

## Modeling water embodied impacts

We draw from the [ESG report](https://esg.tsmc.com/en-US/file/public/e-all_2023.pdf) of [Taiwan Semiconductor Manufacturing Company](https://www.tsmc.com/english) that states that each 12-inch wafer layer consumes about 176.4 liters to produce. 
300mm wafer: ~70,685 mm² area (π * (150mm)²)  
surface area of a NVIDIA H100 SXM5 80 GB chip: 814 mm² [source](https://www.techpowerup.com/gpu-specs/h100-sxm5-80-gb.c3900) 
Which brings us to
70,685 mm2 / 814 mm2 ​≈ 86.837 chips per wafer.  
Using the 176.4 liters per wafer divided by 86.837 chips per wafer, this brings us to 2.03 L/chip. According to this [article](https://massedcompute.com/faq-answers/?question=How%20many%20NVIDIA%20L40S%20GPUs%20can%20be%20installed%20in%20a%20single%20server?#:~:text=1U%20Servers%3A%20Typically%20support%201,for%20AI%20training%20and%20inference.), there are around 8 GPUs in a specialized inference server. We are still working on integrating batching size; right now the placeholder value is one. 

## Assumptions and limitations

To be able to estimate environmental impacts of LLMs at inference we took the approach of modeling the key components that compose the service. In this section we will list major assumptions we make when modeling environmental impacts as well as known limitations. When possible we will try to quantify the potential inaccuracies.

### On models

Two major information we are looking for is the required infrastructure to host the AI model, such as the number of GPUs as well as the energy consumption that results from doing an inference on the model.

Assuming the **required infrastructure** for open models can be relatively straightforward because the model size is known. But for proprietary models this can very be challenging given that some AI provider do not disclose any technical information on that matter. That's why we rely on estimations of parameters count for closed models, to learn more [read the dedicated section](proprietary_models.md).

Assuming the **energy consumption** for AI models is done through benchmarking open models. We tend to rely on external sources for benchmarking, but we conduct our own experiments as well. Because of our limited capacity and the technical complexity to host very big AI models we extrapolate the consumption of smaller models to bigger models.

**Assumptions:**

* Models are deployed with vLLM backend.
* Models are quantized to 4 bits.

**Limitations:**

* We do not account for some inference optimizations such as flash attention. 
* We do not have benchmarks for multi-GPU deployments.
* We do not account for the multiple modalities of a model (only text-to-text generation).

### On hardware

We estimate the **required infrastructure** to run the service in terms of hardware. We consider that the service is hosted in the cloud on servers equipped with high-end GPUs. 

**Assumptions:**

* Models are deployed on NVIDIA H100 GPUs with 80GB of memory.
* Base servers are similar to p4de.24xlarge AWS cloud instances.

**Limitations:**

* We do not account for TPUs or other type of accelerators.
* We do not account for networking or storage primitives.
* We do not account for infrastructure overheads or utilization factors.

### On data centers

The type of services we model rely on high-end hardware that we consider is hosted by cloud service providers. Thus, we model data centers impacts as well and especially the overhead for cooling equipments.

We consider the **Power Usage Effectiveness** (PUE) metric from data centers. These values can be quite complicated to get from the providers themselves. A good amount of data is available for providers that build their own data centers (such as hyperscalers). But part of the AI workloads are also located in non-hyperscale data centers or in co-located data centers. For each datacenter provider, we use the PUE number published by them on a global average.


**Limitations:**

* We do not know precisely where are located the data centers that run AI models.
* We do not account for the specific infrastructure or way to cooldown servers in data centers.
* We do not account for the local electricity generation (private power plants) specific to the data center.
* We do not account for the overhead of the cloud provider for internal services like backing up or monitoring.

The water consumption for the production of electricity varies widely by regions, and you could consider checking out our [environmental impact simulator](https://huggingface.co/spaces/genai-impact/ecologits-calculator) to find out about regional differences.  


### On impact factors

To transform physical values such as energy consumption into environmental impacts we use **impact factors**. These can be hard to estimate and precise and up-to-date data is rarely open to use.

**Assumptions:**

* Electricity mix are taken from the ADEME Base Empreinte database and averaged per country.

**Limitations:**

* We do not account for local electricity generation for data center or regional electricity mixes the smallest supported zone is a country.

### On embodied impacts

We aim at covering the largest scope possible when assessing the environmental impacts. That is why we rely extensively on the work done by [Boavizta](https://boavizta.org/) non-profit. Unfortunately, assessing the environmental impacts of resources extraction, hardware manufacturing and transportation is very challenging mainly due to a lack of transparency from all the organizations that are involved. Estimations of the inaccuracies are currently not supported within Boavizta's methodology and tool ([BoaviztAPI](https://doc.api.boavizta.org/)).


## References

- [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/?__theme=light) to estimate GPU energy consumption and latency based on the model architecture and number of output tokens.
- [BoaviztAPI](https://github.com/Boavizta/boaviztapi) to estimate server embodied impacts and base energy consumption.
- [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/) for electricity mix impacts per country.

## :material-bookshelf: Citation

Please cite **GenAI Impact** non-profit organization and **link to this documentation page**. 

```bibtex
@article{ecologits, 
    doi = {10.21105/joss.07471}, 
    url = {https://doi.org/10.21105/joss.07471}, 
    year = {2025}, 
    publisher = {The Open Journal}, 
    volume = {10}, number = {111}, pages = {7471}, 
    author = {Rincé, Samuel and Banse, Adrien}, 
    title = {EcoLogits: Evaluating the Environmental Impacts of Generative AI}, 
    journal = {Journal of Open Source Software}
}
```

## :material-scale-balance: License

**This work is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">
