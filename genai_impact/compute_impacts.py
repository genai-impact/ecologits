from dataclasses import dataclass

ENERGY_PROFILE = 1.17e-4

MODEL_SIZES = {
    "gpt-4-0125-preview": None,
    "gpt-4-turbo-preview": None,
    "gpt-4-1106-preview": None,
    "gpt-4-vision-preview": None,
    "gpt-4": 200,
    "gpt-4-0314": 200,
    "gpt-4-0613": 200,
    "gpt-4-32k": 200,
    "gpt-4-32k-0314": 200,
    "gpt-4-32k-0613": 200,
    "gpt-3.5-turbo": 20,
    "gpt-3.5-turbo-16k": 20,
    "gpt-3.5-turbo-0301": 20,
    "gpt-3.5-turbo-0613": 20,
    "gpt-3.5-turbo-1106": 20,
    "gpt-3.5-turbo-0125": 20,
    "gpt-3.5-turbo-16k-0613": 20,
}


@dataclass
class Impacts:
    energy: float
    energy_unit: str = "Wh"


def compute_llm_impact(
    model_parameter_count: float,
    output_token_count: int,
) -> Impacts:
    return Impacts(energy=ENERGY_PROFILE * model_parameter_count * output_token_count)
