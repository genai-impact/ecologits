from pydantic import BaseModel

class Impact(BaseModel):
    type: str
    name: str
    value: float
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


class Energy(Impact):
    type: str = "energy"
    name: str = "Energy"
    unit: str = "kWh"


class GWP(Impact):
    type: str = "GWP"
    name: str = "Global Warming Potential"
    unit: str = "kgCO2eq"


class ADPe(Impact):
    type: str = "ADPe"
    name: str = "Abiotic Depletion Potential (elements)"
    unit: str = "kgSbeq"


class PE(Impact):
    type: str = "PE"
    name: str = "Primary Energy"
    unit: str = "MJ"


class Phase(BaseModel):
    type: str
    name: str


class Usage(Phase):
    type: str = "usage"
    name: str = "Usage"
    energy: Energy
    gwp: GWP
    adpe: ADPe
    pe: PE


class Embodied(Phase):
    type: str = "embodied"
    name: str = "Embodied"
    gwp: GWP
    adpe: ADPe
    pe: PE


class Impacts(BaseModel):
    energy: Energy
    gwp: GWP
    adpe: ADPe
    pe: PE
    usage: Usage
    embodied: Embodied
