from typing import Callable, Optional

from pydantic import BaseModel
from wrapt import wrap_function_wrapper

from ecologits.impacts.modeling import GWP, PE, ADPe, Embodied, Energy, Usage
from ecologits.status_messages import ErrorMessage, WarningMessage


class WrappedMethod(BaseModel):
    module: str
    name: str
    wrapper: Callable


class Instrumentor(BaseModel):
    wrapped_methods: list[WrappedMethod]


class Provider(BaseModel):
    name: str
    instrumentor: Instrumentor
    modules: list[str]

    def __init__(self, name: str) -> None:
        self.name = name

    def instrument(self) -> None:
        for wrapper in self.instrumentor.wrapped_methods:
            wrap_function_wrapper(wrapper.module, wrapper.name, wrapper.wrapper)


class EcoLogitsConfiguration(BaseModel):
    providers: list[Provider]
    electricity_mix_zone: str
    providers_electricity_mixes_zones: dict[str, str]


class ImpactsOutput(BaseModel):
    """
    Impacts output data model.

    Attributes:
        energy: Total energy consumption
        gwp: Total Global Warming Potential (GWP) impact
        adpe: Total Abiotic Depletion Potential for Elements (ADPe) impact
        pe: Total Primary Energy (PE) impact
        usage: Impacts for the usage phase
        embodied: Impacts for the embodied phase
        warnings: List of warnings
        errors: List of errors
    """

    energy: Optional[Energy] = None
    gwp: Optional[GWP] = None
    adpe: Optional[ADPe] = None
    pe: Optional[PE] = None
    usage: Optional[Usage] = None
    embodied: Optional[Embodied] = None
    warnings: Optional[list[WarningMessage]] = None
    errors: Optional[list[ErrorMessage]] = None

    @property
    def has_warnings(self) -> bool:
        return isinstance(self.warnings, list) and len(self.warnings) > 0

    @property
    def has_errors(self) -> bool:
        return isinstance(self.errors, list) and len(self.errors) > 0

    def add_warning(self, warning: WarningMessage) -> None:
        if self.warnings is None:
            self.warnings = []
        self.warnings.append(warning)

    def add_errors(self, error: ErrorMessage) -> None:
        if self.errors is None:
            self.errors = []
        self.errors.append(error)
