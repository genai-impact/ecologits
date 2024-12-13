from functools import total_ordering
from typing import TypeVar

from pydantic import BaseModel

from ecologits.exceptions import ModelingError
from ecologits.utils.range_value import ValueOrRange

Impact = TypeVar("Impact", bound="BaseImpact")


@total_ordering
class BaseImpact(BaseModel):
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

    def __add__(self: Impact, other: object) -> Impact:
        if not isinstance(other, BaseImpact):
            raise ModelingError(f"Error occurred, cannot add an Impact with {type(other)}.")
        if self.type != other.type:
            raise ModelingError(f"Error occurred, cannot add a {self.type} Impact with {other.type} Impact.")
        return self.__class__(
            type=self.type,
            name=self.name,
            value=self.value + other.value,
            unit=self.unit
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BaseImpact):
            raise ModelingError(f"Error occurred, cannot compare an Impact with {type(other)}.")
        if self.type != other.type:
            raise ModelingError(f"Error occurred, cannot compare a {self.type} Impact with {other.type} Impact.")
        return self.value == other.value

    def __le__(self, other: object) -> bool:
        if not isinstance(other, BaseImpact):
            raise ModelingError(f"Error occurred, cannot compare an Impact with {type(other)}.")
        if self.type != other.type:
            raise ModelingError(f"Error occurred, cannot compare a {self.type} Impact with {other.type} Impact.")
        return self.value <= other.value

    def __ge__(self, other: object) -> bool:
        if not isinstance(other, BaseImpact):
            raise ModelingError(f"Error occurred, cannot compare an Impact with {type(other)}.")
        if self.type != other.type:
            raise ModelingError(f"Error occurred, cannot compare a {self.type} Impact with {other.type} Impact.")
        return self.value >= other.value


class Energy(BaseImpact):
    """
    Energy consumption.

    Info:
        Final energy consumption "measured from the plug".

    Attributes:
        type: energy
        name: Energy
        value: Energy value
        unit: Kilowatt-hour (kWh)
    """
    type: str = "energy"
    name: str = "Energy"
    unit: str = "kWh"


class GWP(BaseImpact):
    """
    Global Warming Potential (GWP) impact.

    Info:
        Also, commonly known as GHG/carbon emissions.

    Attributes:
        type: GWP
        name: Global Warming Potential
        value: GWP value
        unit: Kilogram Carbon Dioxide Equivalent (kgCO2eq)
    """
    type: str = "GWP"
    name: str = "Global Warming Potential"
    unit: str = "kgCO2eq"


class ADPe(BaseImpact):
    """
    Abiotic Depletion Potential for Elements (ADPe) impact.

    Info:
        Impact on the depletion of non-living resources such as minerals or metals.

    Attributes:
        type: ADPe
        name: Abiotic Depletion Potential (elements)
        value: ADPe value
        unit: Kilogram Antimony Equivalent (kgSbeq)
    """
    type: str = "ADPe"
    name: str = "Abiotic Depletion Potential (elements)"
    unit: str = "kgSbeq"


class PE(BaseImpact):
    """
    Primary Energy (PE) impact.

    Info:
        Total energy consumed from primary sources.

    Attributes:
        type: PE
        name: Primary Energy
        value: PE value
        unit: Megajoule (MJ)
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
        type: usage
        name: Usage
        energy: Energy consumption
        gwp: Global Warming Potential (GWP) usage impact
        adpe: Abiotic Depletion Potential for Elements (ADPe) usage impact
        pe: Primary Energy (PE) usage impact
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
        type: embodied
        name: Embodied
        gwp: Global Warming Potential (GWP) embodied impact
        adpe: Abiotic Depletion Potential for Elements (ADPe) embodied impact
        pe: Primary Energy (PE) embodied impact
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
        energy: Total energy consumption
        gwp: Total Global Warming Potential (GWP) impact
        adpe: Total Abiotic Depletion Potential for Elements (ADPe) impact
        pe: Total Primary Energy (PE) impact
        usage: Impacts for the usage phase
        embodied: Impacts for the embodied phase
    """
    energy: Energy
    gwp: GWP
    adpe: ADPe
    pe: PE
    usage: Usage
    embodied: Embodied
