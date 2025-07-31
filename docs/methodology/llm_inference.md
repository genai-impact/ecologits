# Environmental Impacts of LLM Inference

<span class="badge" markdown>
    <span class="badge__icon">:material-tag-outline:</span>
    <span class="badge__text">v1.0</span>
</span>


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

By leveraging the open dataset from the [LLM Perf Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard), produced by Hugging Face, we can estimate the energy consumption of the GPU using a parametric model.

We fit a linear regression model to the dataset, which models the energy consumption per output token as a function of the number of active parameters in the LLM, denoted as $P_{\text{active}}$.

??? note "What are active parameters?"

    We distinguish between active parameters and total parameter count for Sparse Mixture-of-Experts (SMoE) models. The total parameter count is used to determine the number of required GPUs to load the model into memory. In contrast, the active parameter count is used to estimate the energy consumption of a single GPU. In practice, SMoE models exhibit lower energy consumption per GPU compared to dense models of equivalent size (in terms of total parameters).

    * For a dense model: $P_{\text{active}} = P_{\text{total}}$
    * For a SMoE model: $P_{\text{active}} =  P_{\text{total}} / \text{number of active experts}$

??? info "On the LLM Perf Leaderboard dataset filtering"
    
    We have filtered the dataset to keep relevant data points for the analysis. In particular we have applied the following conditions:
    
    * Model number of parameters >= 7B
    * Keep dtype set to float16
    * GPU model is "NVIDIA A100-SXM4-80GB"
    * No optimization
    * 8bit and 4bit quantization excluding bitsandbytes (bnb)


<figure markdown="span">
  ![Figure: Energy consumption per output token vs. number of active parameters ](../assets/methodology/llm/figure_energy.png)
  <figcaption>Figure: Energy consumption (in Wh) per output token vs. number of active parameters (in billions)</figcaption>
</figure>

??? info "What is a 95% confidence interval?"

    The standard deviation $\delta$ of a linear regression measures "how close are the datapoints to the fitted line". A priori, the larger it is, the worse is the approximation. Consider a linear regression $Y(x) \approx \alpha x + \beta$. Given some assumptions, we can say that $Y(x) \in [\alpha x + \beta - 1.96\delta, \alpha x + \beta + 1.96\delta]$ with probability 95% (see [[1]](https://en.wikipedia.org/wiki/Linear_regression) and [[2]](https://en.wikipedia.org/wiki/97.5th_percentile_point) for more details).

In our methodology, **in order to take into account approximation errors as much as possible**, we provide the **95% confidence interval** of our linear approximation. The computed linear regression gives a confidence interval of

$$
\frac{E_{\text{GPU}}}{\#T_{\text{out}}} = \alpha \times P_{\text{active}} + \beta \pm 1.96 \sigma, 
$$

with $\alpha = 8.91e-5$, $\beta = 1.43e-3$ and $\sigma = 5.19e-4$. 

Using these values, we can estimate the energy consumption of a simple GPU for the entire request, given the number of output tokens $\#T_{\text{out}}$ and the number of active parameters $P_{\text{active}}$:

$$
E_{\text{GPU}}(\#T_{\text{out}}, P_{\text{active}}) = \#T_{\text{out}} \times (\alpha \times P_{\text{active}} + \beta \pm 1.96 \sigma).
$$

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

The generation latency, $\Delta T$, is the duration of the inference measured on the server and is independent of networking latency. We estimate the generation latency using the [LLM Perf Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard) dataset with the previously mentioned filters applied.

We fit a linear regression model on the dataset modeling the generation latency per output token given the number of active parameters of the LLM $P_{\text{active}}$:

<figure markdown="span">
  ![Figure: Latency per output token vs. number of active parameters ](../assets/methodology/llm/figure_latency.png)
  <figcaption>Figure: Latency (in s) per output token vs. number of active parameters (in billions)</figcaption>
</figure>

Again, we propagate 95% confidence intervals through our computations. The fit gives an interval of

$$
\frac{\Delta T}{\#T_{\text{out}}} = \alpha \times P_{\text{active}} + \beta \pm 1.96\delta, 
$$

with $\alpha = 8.02e-4$, $\beta = 2.23e-2$ and $\delta = 7.00e-6$. Using these values, we can estimate the generation latency for the entire request given the number of output tokens, $\#T_{\text{out}}$, and the number of active parameters, $P_{\text{active}}$. When possible, we also measure the request latency, $\Delta T_{\text{request}}$, and use it as the maximum bound for the generation latency:

$$
\Delta T(\#T_{\text{out}}, P_{\text{active}}) = \#T_{\text{out}} \times (\alpha \times P_{\text{active}} + \beta \pm 1.96\delta).
$$

With the request latency, the generation latency is defined as follows:

$$
\Delta T(\#T_{\text{out}}, P_{\text{active}}, \Delta T_{\text{request}}) = \min \left\{ \#T_{\text{out}} \times (\alpha \times P_{\text{active}} + \beta \pm 1.96 \delta), \Delta T_{\text{request}} \right\}.
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

To stay consistent with previous assumptions based on LLM Perf Leaderboard data, we use $M_{\text{GPU}} = 80$ GB for an NVIDIA A100 80GB GPU.

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

- Water Use (WCF): Water consumption from this request. The formula for quantifying this is:

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

| AI Provider      | Datacenter Provider |
|------------------|---------------------|
| Anthropic        | Google              |
| MistralAI        | OVHCloud            |
| Cohere           | AWS                 |
| Databricks       | Microsoft           |
| Meta             | Meta                |
| Azure OpenAI     | Microsoft           |
| Hugging Face Hub | AWS                 |
| Google           | Google              |
| Microsoft        | Microsoft           |
| OpenAI           | Microsoft           |

  
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
  
The $WUE_{on-site}$ of each datacenter provider:
  
| Datacenter Provider | WUE   | Source |
|---------------------|-------|--------|
| Google              | 0.916 | [source](https://www.gstatic.com/gumdrop/sustainability/google-2025-environmental-report.pdf) |
| Meta                | 0.18  | [source](https://sustainability.atmeta.com/wp-content/uploads/2024/08/Meta-2024-Sustainability-Report.pdf) |
| Microsoft           | 0.49  | [source](https://azure.microsoft.com/en-us/blog/how-microsoft-measures-datacenter-water-and-energy-use-to-improve-azure-cloud-sustainability/) |
| OVHCloud            | 0.37  | [source](https://corporate.ovhcloud.com/en/sustainability/environment/) |
| Scaleway            | 0.216 | [source](https://www-uploads.scaleway.com/Impact_Report2024_A4_EN_e63efcae20.pdf) |
| AWS                 | 0.18  | [source](https://sustainability.aboutamazon.com/2023-report) |
| Equinix             | 1.07  | [source](https://www.equinix.com/resources/infopapers/2023-corporate-sustainability-report) |
  
Finally, for $WUE_{off-site}$, we take the data from a [report](https://www.wri.org/research/guidance-calculating-water-use-embedded-purchased-electricity) by the [World Resource Institue](https://www.wri.org). For brevity, we will not list the list of countries here. For the countries whose data is missing, the user will get a userwarning along with the result telling them that the global average is used.   

## Embodied impacts

To determine the embodied impacts of an LLM inference, we need to estimate the **hardware configuration** used to host the model and its lifetime. Embodied impacts account for resource extraction (e.g., minerals and metals), manufacturing, and transportation of the hardware.

### Modeling server embodied impacts

To estimate the embodied impacts of IT hardware, we use the [BoaviztAPI](https://github.com/Boavizta/boaviztapi) tool from the non-profit organization [Boavizta](https://boavizta.org/en/). This API embeds a bottom-up multicriteria environment impact estimation engine for embodied and usage phases of IT resources and services. We focus on estimating the embodied impacts of a server and a GPU. BoaviztAPI is an open-source project that relies on open databases and open research on environmental impacts of IT equipment.

#### Server embodied impacts without GPU

To assess the embodied environmental impacts of a high-end AI server, we use an AWS cloud instance as a reference. We selected the `p4de.24xlarge` instance, as it corresponds to a server that can be used for LLM inference with eight NVIDIA A100 80GB GPU cards. The embodied impacts of this instance will be used to estimate the embodied impacts of the server without GPUs, denoted as $I^{\text{e}}_{\text{server} \backslash \text{GPU}}$.

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

Boavizta is currently developing a methodology to provide multicriteria embodied impacts for GPU cards. For this analysis, we use the embodied impact data they computed for a NVIDIA A100 80GB GPU. These values will be used to estimate the embodied impacts of a single GPU, denoted as $I^{\text{e}}_{\text{GPU}}$.

|                | NIDIA A100 80GB       |
|----------------|-----------------------|
| GWP (kgCO2eq)  | $143$                 |
| ADPe (kgSbeq)  | $5.09 \times 10^{-3}$ |
| PE (MJ)        | $1,828$               |

!!! warning "The GPU embodied impacts will be soon available in the BoaviztAPI tool."


#### Complete server embodied impacts

The final embodied impacts for the server, including the GPUs, are calculated as follows. Note that the embodied impacts of the server without GPUs are scaled by the number of GPUs required to host the model. This allocation is made to account for the fact that the remaining GPUs on the server can be used to host other models or multiple instances of the same model. As we are estimating the impacts of a single LLM inference, we need to exclude the embodied impacts that would be attributed to other services hosted on the same server:

$$
I^{\text{e}}_{\text{server}}=\frac{\text{GPU}}{\#\text{GPU}_{\text{installed}}} \times I^{\text{e}}_{\text{server} \backslash \text{GPU}} + \text{GPU} \times I^{\text{e}}_{\text{GPU}}.
$$


### Modeling request embodied environmental impacts

To allocate the server embodied impacts to the request, we use an allocation based on the hardware utilization factor, $\frac{\Delta T}{\Delta L}$. In this case, $\Delta L$ represents the lifetime of the server and GPU, which we fix at 5 years:

$$
I^{\text{e}}_{\text{request}}=\frac{\Delta T}{\Delta L} \times I^{\text{e}}_{\text{server}}.
$$

## Modeling water embodied impacts

We draw from the [ESG report](https://esg.tsmc.com/en-US/file/public/e-all_2023.pdf) of [Taiwan Semiconductor Manufacturing Company](https://www.tsmc.com/english) that states that each 12-inch wafer layer consumes about 176.4 liters to produce. According to this [article](https://waferpro.com/how-many-chips-can-be-cut-from-a-silicon-wafer/?srsltid=AfmBOoriSA25IQoHzZsc2-7QC8kMqAn8GRsnDFlA0OcSnvNFPFH0zUH8), assuming a 15mm x 15mm chip size:  
300mm wafer: ~70,685 mm² area (π * (150mm)²)  
15mm x 15mm chip: 225 mm²  
Which brings us to
70,685 mm2 / 225 mm2 ​≈ 314 chips per wafer.  
Using the 176.4 liters per wafer divided by 314 chips per wafer, this brings us to 0.562 L/chip. According to this [article](https://massedcompute.com/faq-answers/?question=How%20many%20NVIDIA%20L40S%20GPUs%20can%20be%20installed%20in%20a%20single%20server?#:~:text=1U%20Servers%3A%20Typically%20support%201,for%20AI%20training%20and%20inference.), there are around 8 GPUs in a specialized inference server. We are still working on integrating batching size; right now the placeholder value is one. 

## Assumptions and limitations

To be able to estimate environmental impacts of LLMs at inference we took the approach of modeling the key components that compose the service. In this section we will list major assumptions we make when modeling environmental impacts as well as known limitations. When possible we will try to quantify the potential inaccuracies.

### On models

Two major information we are looking for is the required infrastructure to host the AI model, such as the number of GPUs as well as the energy consumption that results from doing an inference on the model.

Assuming the **required infrastructure** for open models can be relatively straightforward because the model size is known. But for proprietary models this can very be challenging given that some AI provider do not disclose any technical information on that matter. That's why we rely on estimations of parameters count for closed models, to learn more [read the dedicated section](proprietary_models.md).

Assuming the **energy consumption** for AI models is done through benchmarking open models. We tend to rely on external sources for benchmarking, but we conduct our own experiments as well. Because of our limited capacity and the technical complexity to host very big AI models we extrapolate the consumption of smaller models to bigger models.

**Assumptions:**

* Models are deployed with pytorch backend.
* Models are quantized to 4 bits.

**Limitations:**

* We do not account for other inference optimizations such as flash attention, batching or parallelism.
* We do not benchmark models bigger than 70 billion parameters.
* We do not have benchmarks for multi-GPU deployments.
* We do not account for the multiple modalities of a model (only text-to-text generation).

### On benchmarking data

We use **linear regression models** to approximate energy consumption per token and latency per token as a function of the number of active parameters in the LLM. We represent the linear model as $Y = a \times X + b + \epsilon$, where $Y$ is the predicted value, $X$ is the input variable, $a$ and $b$ are the regression coefficients, and $\epsilon$ is the error term. We assume that the errors ($\epsilon$) follow a **normal distribution** with a mean of zero and a constant variance, represented as $\epsilon \sim \mathcal{N}(0, \sigma^2)$. This enables us to use the 95% confidence interval, calculated using the standard deviation of the errors ($\sigma$) and the 97.5th percentile point of the standard normal distribution (approximately 1.96).

### On hardware

We estimate the **required infrastructure** to run the service in terms of hardware. We consider that the service is hosted in the cloud on servers equipped with high-end GPUs. 

**Assumptions:**

* Models are deployed on NVIDIA A100 GPUs with 80GB of memory.
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

- [LLM-Perf Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard) to estimate GPU energy consumption and latency based on the model architecture and number of output tokens.
- [BoaviztAPI](https://github.com/Boavizta/boaviztapi) to estimate server embodied impacts and base energy consumption.
- [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/) for electricity mix impacts per country.

## :material-bookshelf: Citation

Please cite **GenAI Impact** non-profit organization and **link to this documentation page**. 

```bibtex
"""
@software{ecologits,
  author = {Samuel Rincé, Adrien Banse, Vinh Nguyen, Luc Berton, and Chieh Hsu},
  publisher = {GenAI Impact},
  title = {EcoLogits: track the energy consumption and environmental footprint of using generative AI models through APIs.},
}"""
```

## :material-scale-balance: License

**This work is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/)**
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1" alt="">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1" alt="">
