# Tutorial

The :seedling: **EcoLogits** library tracks the energy consumption and environmental impacts of generative AI models accessed through APIs and their official client libraries. 

It achieves this by **patching the Python client libraries**, ensuring that each API request is wrapped with an impact calculation function. This function computes the **environmental impact based on several request features**, such as the **chosen model**, the **number of tokens generated**, and the **request's latency**. The resulting data is then encapsulated in an `Impacts` object, which is added to the response, containing the environmental impacts for a specific request.


<div class="grid cards" markdown>

-   :material-clock-fast:{ .lg .middle } __Set up in 5 minutes__

    ---

    Install [`ecologits`](#) with [`pip`](#) and get up
    and running in minutes.

    [:octicons-arrow-right-24: Getting started](../index.md)

-   :material-earth:{ .lg .middle } __Environmental impacts__

    ---

    Understand what environmental impacts and phases are reported.  

    [:octicons-arrow-right-24: Tutorial](impacts.md)

-   :fontawesome-regular-handshake:{ .lg .middle } __Supported providers__

    ---

    List of providers and tutorials on how to make requests.

    [:octicons-arrow-right-24: Providers](providers.md)

-   :material-test-tube:{ .lg .middle } __Methodology__

    ---
    
    Understand how we estimate environmental impacts.
    
    [:octicons-arrow-right-24: Methodology](../methodology/index.md)

</div>


## Initialization of EcoLogits

To use EcoLogits in your projects, you will need to initialize the client tracers that are used internally to intercept and enrich responses. 

!!! info "Default behavior is to search and initialize all available providers."

```python
from ecologits import EcoLogits

# Initialize for all available providers
EcoLogits.init()

# Initialize for `openai` provider only
EcoLogits.init(providers="openai")

# Initialize for `openai` and `anthropic` providers only
EcoLogits.init(providers=["openai", "anthropic"])
```

!!! warning "It is currently not possible to un-initialize a provider at runtime. Each time that `EcoLogits` is re-initialized with another providers, the latter will be added to the list of already initialized providers. If you think that un-initializing a provider could be necessary for your use case, please [open an issue :octicons-link-external-16:](https://github.com/genai-impact/ecologits/issues/new/choose)."

It is also possible to initialize `EcoLogits` with a different electricity mix. The latter has to be chosen among the mixes in the [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/) database.

!!! info "The default electricity mix is the world mix given by [ADEME Base Empreinte®](https://base-empreinte.ademe.fr/)."

```python title="Choose a different electricity mix"
from ecologits import EcoLogits

EcoLogits.init() 
# Impacts are computed with the world electricity mix

EcoLogits.init(electricity_mix_zone="FRA")
# Impacts are computed with the electricity mix of France
```
