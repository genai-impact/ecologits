
!!! warning

    This page is under construction.


# Environmental impacts of an LLM inference

Limitations:

- Assuming fixed and worldwide impact factor for electricity consumption.
- Not accounting SMoE (only dense models)


Hypotheses:

- Production-like deployment (quantization + high-end servers) A100


The environmental impacts of a request $I_{request}$ will be split into the usage impacts $I_{request}^u$ to account for energy consumption and the embodied impacts $I_{request}^e$ to account for ressource extraction, hardware manufacturing and transportation.

$$
\begin{equation*}
\begin{split}
I_{request}&=I_{request}^u  + I_{request}^e \\ 
&= E_{request}*F_{em}+\frac{\Delta T}{\Delta L}*I_{server}^e
\end{split}
\end{equation*}
$$

Where $E_{request}$ denotes the energy consumption of the IT ressources in Wh for the request, $F_{em}$ is the impact factor of the electricity consumption that depends on the location and time, $I_{server}^e$ the emboddied impacts of the IT ressources and finally $\frac{\Delta T}{\Delta L}$  is the ratio of usage of hardware a.k.a the computation time over the life time of the hardware.


## Usage impacts

To determine the usage impacts of an LLM inference we first need to estimate the energy consumption of the server equipped with one or more GPUs. We will also include the energy consumption of cooling equipments integrated with the datacenter using the Power Usage Effectiveness (PUE).

Then we can compute environmental impacts with known $F_{em}$ impact factor for the energy consumption. $F_{em}$ ideally varies with location and time.

### Modeling GPU energy consumption

Using open dataset from the [LLM Perf Leaderboard](https://huggingface.co/spaces/optimum/llm-perf-leaderboard) produced by Hugging Face, we can estimate the energy consunption of the GPU based on a parametric model.

We fit a linear regression model on the dataset modeling the energy consumption per output token given the number of active parameters of the LLM $P_{active}$.

IMAGE

$$
E_{token}(P) = \alpha * P + \beta
$$

??? info "On the LLM Perf Leaderboard dataset filtering"
    
    We have filtered the dataset to keep relevant data points for the analysis. In particular we have applied the following conditions:
    
    * Model number of parameters >= 7B
    * Keep dtype set to float16
    * GPU model is "NVIDIA A100-SXM4-80GB"
    * No optimization
    * 8bit and 4bit quantization excluding bitsandbytes (bnb)


We found $\alpha=8.91e-5$ and $\beta=1.43e-3$. Then we can estimate the energy consumption of the GPU for the whole request given the number of output tokens $\#T_{out}$ and the number of active parameters $P_{active}$.

$$
E_{GPU}(\#T_{out}, P_{active}) = \#T_{out} * E_{token}(P_{active})
$$

If the model requires multiple GPUs to be loaded in VRAM the energy consumption $E_{GPU}$ will be multiplied by the number of GPUs $\#GPU$ (see bellow).


### Modeling server energy consumption

To estimate the energy consumption of the whole server we will use the previously estimated GPU energy modeling and estimate seperately the energy consumption of the server itself (without GPUs) $E_{server\\GPU}$.

#### Server energy consumption without GPUs

The modeling of the energy consumption of the server without GPUs we will consider a fixed power consumption $W_{server\GPU}$ during inference (or generation latency) denoted $\Delta T$. We also assume that the server hosts multiple GPUs, but not all GPUs are actively used for the target inference, so we will account for a portion of the energy consumption based on the number of active GPUs $\#GPU_{active}$.

$$
E_{server\\GPU}(\Delta T) = \Delta T * W_{server\\GPU} * \frac{\#GPU_{active}}{\#GPU_{total}}
$$

We use $W_{server\backslash GPU}=1\ kW$ and $\#GPU_{total}=8$ for a typical high-end GPU accelerated cloud instance.

#### Estimating the number of active GPUs

To estimate the number of active GPUs used to load the model in virtual memory we simply use divide the required memory to host the LLM for inference $M_{model}$ by the memory available on one GPU $M_{GPU}$.

The required memory to host the LLM for inference is estimated based on the total number of parameters and the number of bits used for model weights related to quantization. We also apply a memory overhead of $1.2$. [REF]

$$
M_{model}(P,Q)=\frac{P*Q}{8}*1.2
$$

Then estimating the number of required GPUs, rounded up.

$$
\#GPU(P,Q,M_{GPU}) = \lceil \frac{M_{model}(P,Q)}{M_{GPU}}\rceil
$$

To stay inline with previous assumptions based on LLM Perf Leaderboard data, we use $M_{GPU}=80\ GB$ for an NVIDIA A100 80GB GPU.

#### Complete server energy consumption

The server energy consumption for the request including the data centre cooling equipments is thus estimated as follow.

$$
E_{server} = PUE * [E_{server\\ GPU}(\Delta T) + \#GPU * E_{GPU}(\#T_{out}, P)]
$$

We typically use a $PUE=1.2$ for a hyperscaler data centre or super-computer.

### Modeling request environmental impacts

For now we consider that the energy consumption of the request is equal to the previously computed server energy with PUE. 

$E_{request} = E_{server}$
