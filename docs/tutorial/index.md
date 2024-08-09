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
