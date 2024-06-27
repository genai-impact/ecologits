from functools import total_ordering
from typing import Union
from typing_extensions import Self

from pydantic import BaseModel, model_validator


@total_ordering
class RangeValue(BaseModel):
    min: float
    max: float

    @model_validator(mode='after')
    def check_order(self) -> Self:
        if self.min > self.max:
            raise ValueError('min value must be lower than max value')
        return self

    def __add__(self, other):
        if isinstance(other, RangeValue):
            return RangeValue(
                min=self.min + other.min,
                max=self.max + other.max,
            )
        else:
            return RangeValue(
                min=self.min + other,
                max=self.max + other
            )

    def __lt__(self, other):
        if isinstance(other, RangeValue):
            return self.max < other.min
        else:
            return self.max < other and self.min < other

    def __eq__(self, other):
        if isinstance(other, RangeValue):
            return self.min == other.min and self.max == other.max
        else:
            return self.min == other and self.max == other


ValueOrRange = Union[float, RangeValue]


@total_ordering
class Impact(BaseModel):
    """
    Base impact data model.

    Attributes:
        type: Impact type.
        name: Impact name.
        value: Impact value.
        unit: Impact unit.
    """
    type: str
    name: str
    value: ValueOrRange
    unit: str

    def __add__(self, other: "Impact") -> "Impact":
        if not isinstance(other, Impact):
            RuntimeError(f"Error occurred, cannot add an Impact with {type(other)}.")
        if self.type != other.type:
            TypeError(f"Error occurred, cannot add a {self.type} Impact with {other.type} Impact.")
        return self.__class__(
            type=self.type,
            name=self.name,
            value=self.value + other.value,
            unit=self.unit
        )

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class Energy(Impact):
    """
    Energy consumption.

    Info:
        Final energy consumption "measured from the plug".

    Attributes:
        type: energy.
        name: Energy.
        value: Energy value.
        unit: Kilowatt-hour (kWh).
    """
    type: str = "energy"
    name: str = "Energy"
    unit: str = "kWh"


class GWP(Impact):
    """
    Global Warming Potential (GWP) impact.

    Info:
        Also, commonly known as GHG/carbon emissions.

    Attributes:
        type: GWP.
        name: Global Warming Potential.
        value: Impact value.
        unit: Kilogram Carbon Dioxide Equivalent (kgCO2eq).
    """
    type: str = "GWP"
    name: str = "Global Warming Potential"
    unit: str = "kgCO2eq"


class ADPe(Impact):
    """
    Abiotic Depletion Potential for Elements (ADPe) impact.

    Info:
        Impact on the depletion of non-living resources such as minerals or metals.

    Attributes:
        type: ADPe.
        name: Abiotic Depletion Potential (elements).
        value: Impact value.
        unit: Kilogram Antimony Equivalent (kgSbeq).
    """
    type: str = "ADPe"
    name: str = "Abiotic Depletion Potential (elements)"
    unit: str = "kgSbeq"


class PE(Impact):
    """
    Primary Energy (PE) impact.

    Info:
        Total energy consumed from primary sources.

    Attributes:
        type: PE.
        name: Primary Energy.
        value: Impact value.
        unit: Megajoule (MJ).
    """
    type: str = "PE"
    name: str = "Primary Energy"
    unit: str = "MJ"


class Phase(BaseModel):
    """
    Base impact phase data model.

    Attributes:
        type: Phase type.
        name: Phase name.
    """
    type: str
    name: str


class Usage(Phase):
    """
    Usage impacts data model.

    Info:
        Represents the phase of energy consumption during model execution.

    Attributes:
        type: usage.
        name: Usage.
        energy: Energy consumption.
        gwp: Global Warming Potential (GWP) usage impact.
        adpe: Abiotic Depletion Potential for Elements (ADPe) usage impact.
        pe: Primary Energy (PE) usage impact.
    """
    type: str = "usage"
    name: str = "Usage"
    energy: Energy
    gwp: GWP
    adpe: ADPe
    pe: PE


class Embodied(Phase):
    """
    Embodied impacts data model.

    Info:
        Encompasses resource extraction, manufacturing, and transportation phases associated with the model's lifecycle.

    Attributes:
        type: embodied.
        name: Embodied.
        gwp: Global Warming Potential (GWP) embodied impact.
        adpe: Abiotic Depletion Potential for Elements (ADPe) embodied impact.
        pe: Primary Energy (PE) embodied impact.
    """
    type: str = "embodied"
    name: str = "Embodied"
    gwp: GWP
    adpe: ADPe
    pe: PE


class Impacts(BaseModel):
    """
    Impacts data model.

    Attributes:
        energy: Total energy consumption.
        gwp: Total Global Warming Potential (GWP) impact.
        adpe: Total Abiotic Depletion Potential for Elements (ADPe) impact.
        pe: Total Primary Energy (PE) impact.
        usage: Impacts for the usage phase.
        embodied: Impacts for the embodied phase.
    """
    energy: Energy
    gwp: GWP
    adpe: ADPe
    pe: PE
    usage: Usage
    embodied: Embodied
