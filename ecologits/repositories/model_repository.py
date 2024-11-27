import json
import os
from enum import Enum
from typing import Optional, Union

from pydantic import BaseModel

from ecologits.utils.range_value import ValueOrRange


class Providers(Enum):
    anthropic = "anthropic"
    mistralai = "mistralai"
    openai = "openai"
    huggingface_hub = "huggingface_hub"
    cohere = "cohere"
    google = "google"


class Warnings(Enum):
    model_architecture_not_released = "model_architecture_not_released"
    model_architecture_multimodal = "model_architecture_multimodal"



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
    warnings: Optional[list[Warnings]] = None
    sources: Optional[list[str]] = None


class Models(BaseModel):
    aliases: Optional[list[Alias]] = None
    models: Optional[list[Model]] = None


class ModelRepository:

    def __init__(self, models: list[Model], aliases: Optional[list[Alias]] = None) -> None:
        self.__models: dict[tuple[str, str], Model] = {}
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
            mf = Models.model_validate(data)
        return cls(models=mf.models, aliases=mf.aliases)


models = ModelRepository.from_json()
