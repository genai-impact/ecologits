import json
import os
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel

from ecologits.status_messages import WarningMessage
from ecologits.utils.range_value import ValueOrRange


class Providers(Enum):
    anthropic = "anthropic"
    mistralai = "mistralai"
    openai = "openai"
    huggingface_hub = "huggingface_hub"
    cohere = "cohere"
    google = "google"


class ArchitectureTypes(Enum):
    DENSE = "dense"
    MOE = "moe"


class ParametersMoE(BaseModel):
    total: ValueOrRange
    active: ValueOrRange


class Architecture(BaseModel):
    type: ArchitectureTypes
    parameters: Union[ValueOrRange, ParametersMoE]


class Alias(BaseModel):
    provider: Providers
    name: str
    alias: str


class Model(BaseModel):
    provider: Providers
    name: str
    architecture: Architecture
    warnings: list[WarningMessage] = []
    sources: list[str] = []

    @property
    def has_warnings(self) -> bool:
        return len(self.warnings) > 0

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "Model":
        warnings = []
        if data["warnings"] is not None:
            warnings = [WarningMessage.from_code(code) for code in data["warnings"]]
        return cls(
            provider=Providers(data["provider"]),
            name=data["name"],
            architecture=Architecture.model_validate(data["architecture"]),
            warnings=warnings,
            sources=data["sources"] or []
        )


class ModelRepository:

    def __init__(self, models: list[Model], aliases: Optional[list[Alias]] = None) -> None:
        self.__models: dict[tuple[str, str], Model] = {}
        if models is not None:
            for m in models:
                key = m.provider.value, m.name
                if key in self.__models:
                    raise ValueError(f"duplicated models with: {key}")
                self.__models[key] = m

        if aliases is not None:
            for a in aliases:
                model_key = a.provider.value, a.alias
                if model_key not in self.__models:
                    raise ValueError(f"model alias not found: {model_key}")
                alias_key = a.provider.value, a.name
                model = self.__models[model_key].model_copy()
                model.name = a.name
                self.__models[alias_key] = model

    def find_model(self, provider: str, model_name: str) -> Optional[Model]:
        return self.__models.get((provider, model_name))

    def list_models(self) -> list[Model]:
        return list(self.__models.values())

    @classmethod
    def from_json(cls, filepath: Optional[str] = None) -> "ModelRepository":
        if filepath is None:
            filepath = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "data", "models.json"
            )
        with open(filepath) as fd:
            data = json.load(fd)

            alias_list = []
            if "aliases" in data and data["aliases"] is not None:
                for alias in data["aliases"]:
                    alias_list.append(Alias.model_validate(alias))

            model_list = []
            if "models" in data and data["models"] is not None:
                for model in data["models"]:
                    model_list.append(Model.from_json(model))

        if len(model_list) == 0:
            raise ValueError("Cannot initialize on an empty model repository.")
        return cls(models=model_list, aliases=alias_list)


models = ModelRepository.from_json()
