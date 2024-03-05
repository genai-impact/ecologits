from pydantic import BaseModel

ENERGY_PROFILE = 1.17e-4


class Impacts(BaseModel):
    energy: float
    energy_unit: str = "Wh"


def compute_llm_impact(
    model_parameter_count: float,
    output_token_count: int,
) -> Impacts:
    return Impacts(energy=ENERGY_PROFILE * model_parameter_count * output_token_count)
