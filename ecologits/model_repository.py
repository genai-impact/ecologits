import os
from csv import DictReader
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class Providers(Enum):
    anthropic = "anthropic"
    mistralai = "mistralai"
    openai = "openai"
    huggingface_hub = "huggingface_hub"
    cohere = "cohere"
    google = "google"


class Warnings(Enum):
    model_architecture_not_released = "model_architecture_not_released"


@dataclass
class Model:
    provider: str
    name: str
    total_parameters: Optional[float] = None
    active_parameters: Optional[float] = None
    total_parameters_range: Optional[tuple[float, float]] = None
    active_parameters_range: Optional[tuple[float, float]] = None
    warnings: Optional[list[str]] = None
    sources: Optional[list[str]] = None


class ModelRepository:
    def __init__(self, models: list[Model]) -> None:
        self.__models = models

    def find_model(self, provider: str, model_name: str) -> Optional[Model]:
        provider_models = [model for model in self.__models if model.provider == provider]
        return next(
            (
                model
                for model in provider_models
                if (model.name == model_name or model.name.replace(".", "") == model_name)
            ),
            next((model for model in provider_models if model.name in model_name), None),
        )

    def find_provider(self, model_name: str) -> Optional[str]:
        for model in self.__models:
            if model.name in model_name:
                return model.provider
        return None

    @classmethod
    def from_csv(cls, filepath: Optional[str] = None) -> "ModelRepository":
        if filepath is None:
            filepath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data", "models.csv")
        models = []
        with open(filepath) as fd:
            csv = DictReader(fd)
            for row in csv:
                total_parameters = None
                total_parameters_range = None
                if ";" in row["total_parameters"]:
                    total_parameters_range = [float(p) for p in row["total_parameters"].split(";")]
                elif row["total_parameters"] != "":
                    total_parameters = float(row["total_parameters"])

                active_parameters = None
                active_parameters_range = None
                if ";" in row["active_parameters"]:
                    active_parameters_range = [float(p) for p in row["active_parameters"].split(";")]
                elif row["active_parameters"] != "":
                    active_parameters = float(row["active_parameters"])

                warnings = None
                if row["warnings"] != "":
                    warnings = [Warnings(w).name for w in row["warnings"].split(";")]

                sources = None
                if row["sources"] != "":
                    sources = row["sources"].split(";")

                models.append(
                    Model(
                        provider=Providers(row["provider"]).name,
                        name=row["name"],
                        total_parameters=total_parameters,
                        active_parameters=active_parameters,
                        total_parameters_range=total_parameters_range,
                        active_parameters_range=active_parameters_range,
                        warnings=warnings,
                        sources=sources,
                    )
                )
        return cls(models)


models = ModelRepository.from_csv()
