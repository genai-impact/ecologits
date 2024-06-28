# Environmental Impacts

!!! warning

    This page is under construction.

Environmental impacts are reported for each request in the [`Impacts`][impacts.modeling.Impacts] pydantic model and features multiple [criteria](#criteria) such as the [energy](#energy) and [global warming potential](#global-warming-potential-gwp) per phase ([usage](#usage) or [embodied](#embodied)) as well as the total impacts.

To learn more on how we estimate the environmental impacts and what are our hypotheses go to the [methodology](../methodology/index.md) section.

```python title="Structure of Impacts model"
from ecologits.impacts.modeling import *

Impacts(
    energy=Energy(), # (1)!
    gwp= GWP(),
    adpe=ADPe(),
    pe=PE(),
    usage=Usage( # (2)!
        energy=Energy(),
        gwp=GWP(),
        adpe=ADPe(),
        pe=PE(),
    ),
    embodied=Embodied( # (3)!
        gwp=GWP(),
        adpe=ADPe(),
        pe=PE(),
    )
)
```

1. Total impacts for all phases.
2. Usage impacts for the electricity consumption impacts. Note that the energy is equal to the "total" energy impact.
3. Embodied impacts for resource extract, manufacturing and transportation of hardware components allocated to the request. 

You can extract an impact with:

```python
response.impacts.usage.gwp.value  # (1)!

>>> 0.34    # Expressed in kgCO2eq.
```

1. Assuming you have made an inference and get the response in an `response` object.

## Criteria

To evaluate the impact of human activities on the planet or on the climate we use criteria that usually focus on a specific issue such as **GHG emissions for global warming**, **water consumption and pollution** or the **depletion of natural resources**. We currently support three environmental impact criteria in addition with the direct energy consumption. 

**Monitoring multiple criteria is useful to avoid pollution shifting**, which is defined as the transfer of pollution from one medium to another. It is a common pitfall to optimize only one criterion like GHG emissions (e.g. buying new hardware that is more energy efficient), that can lead to higher impacts on minerals and metals depletion for example. (see [encyclopedia.com :octicons-link-external-16:](https://www.encyclopedia.com/environment/educational-magazines/pollution-shifting))

### Energy

The [`Energy`][impacts.modeling.Energy] criterion refers to the **direct electricity consumption of GPUs, server and other equipments from the data center**. As defined the energy criteria is not an environmental impact, but it is used to estimate other impacts in the [usage phase](#usage). This criterion is expressed in **kilowatt-hour (kWh)**.

??? note "Energy model attributes"
    ::: impacts.modeling.Energy
        options:
            show_root_toc_entry: false
            show_bases: false
            show_docstring_description: false
            docstring_section_style: list


### Global Warming Potential (GWP)

The Global Warming Potential ([`GWP`][impacts.modeling.GWP]) criterion is an index **measuring how much heat is absorbed by greenhouse gases in the atmosphere compared to carbon dioxide**. This criterion is expressed in **kilogram of carbon dioxide equivalent (kgCO2eq)**.

*[carbon dioxide]: Carbon Dioxide chemical formula is CO2

Learn more: [wikipedia.org :octicons-link-external-16:](https://en.wikipedia.org/wiki/Global_warming_potential)

??? note "GWP model attributes"
    ::: impacts.modeling.GWP
        options:
            show_root_toc_entry: false
            show_bases: false
            show_docstring_description: false
            docstring_section_style: list


### Abiotic Depletion Potential for Elements (ADPe)

The Abiotic Depletion Potential – elements ([`ADPe`][impacts.modeling.ADPe]) criterion represents the **reduction of non-renewable and non-living (abiotic) resources such as metals and minerals**. This criterion is expressed in **kilogram of antimony equivalent (kgSbeq)**.

*[antimony]: Antimony symbol is Sb

Learn more: [sciencedirect.com :octicons-link-external-16:](https://www.sciencedirect.com/topics/engineering/abiotic-depletion-potential)

??? note "ADPe model attributes"
    ::: impacts.modeling.ADPe
        options:
            show_root_toc_entry: false
            show_bases: false
            show_docstring_description: false
            docstring_section_style: list

### Primary Energy (PE)

The Primary Energy ([`PE`][impacts.modeling.PE]) criterion represents the amount of **energy consumed from natural sources such as raw fuels and other forms of energy, including waste**. This criterion is expressed in **megajoule (MJ)**. 

Learn more: [wikipedia.org :octicons-link-external-16:](https://en.wikipedia.org/wiki/Primary_energy)

??? note "PE model attributes"
    ::: impacts.modeling.PE
        options:
            show_root_toc_entry: false
            show_bases: false
            show_docstring_description: false
            docstring_section_style: list

## Phases

Inspired from the Life Cycle Assessment methodology we classify impacts is two phases (usage and embodied). The **usage phase** is about the environmental impacts related to the energy consumption while using an AI model. The **embodied phase** encompasses upstream impacts such as resource extraction, manufacturing, and transportation. We currently do not support the third phase which is end-of-life due to a lack of open research and transparency on that matter.

Learn more: [wikipedia.org :octicons-link-external-16:](https://en.wikipedia.org/wiki/Life-cycle_assessment)

Another **pitfall in environmental impact assessment is to only look at the usage phase and ignore upstream and downstream impacts**. This can lead to higher overall impacts on the entire life cycle. If you replace old hardware by newer that is more energy efficient, you will get a reduction of impacts on the usage phase, but it will increase the upstream impacts as well.  

### Usage

The [`Usage`][impacts.modeling.Usage] phase accounts for the environmental impacts while using AI models. We report all criteria in addition to direct energy consumption for this phase. 

??? note "Usage model attributes"
    ::: impacts.modeling.Usage
        options:
            show_root_toc_entry: false
            show_bases: false
            show_docstring_description: false
            docstring_section_style: list

### Embodied

The [Embodied][impacts.modeling.Embodied] phase accounts for the upstream environmental impacts such as resource extraction, manufacturing and transportation allocated to the request. We report all criteria (excluding energy consumption) for this phase.

??? note "Embodied model attributes"
    ::: impacts.modeling.Embodied
        options:
            show_root_toc_entry: false
            show_bases: false
            show_docstring_description: false
            docstring_section_style: list
