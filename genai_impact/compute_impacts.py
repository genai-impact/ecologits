from typing import Union

from pydantic import BaseModel

GPU_ENERGY_ALPHA = 8.91e-5
GPU_ENERGY_BETA = 1.43e-3


class Impacts(BaseModel):
    energy: float
    energy_range: tuple[float, float]
    energy_unit: str = "Wh"


def compute_llm_impact(
    model_parameter_count: Union[float, tuple[float, float]],
    output_token_count: int,
) -> Impacts:
    if isinstance(model_parameter_count, (tuple, list)):
        # TODO: check tuple or list validity (min, max)
        energy_min = output_token_count * (GPU_ENERGY_ALPHA * model_parameter_count[0] + GPU_ENERGY_BETA)
        energy_max = output_token_count * (GPU_ENERGY_ALPHA * model_parameter_count[1] + GPU_ENERGY_BETA)
        energy_avg = (energy_min + energy_max) / 2
    else:
        energy_avg = output_token_count * (GPU_ENERGY_ALPHA * model_parameter_count + GPU_ENERGY_BETA)
        energy_min = energy_avg
        energy_max = energy_avg
    return Impacts(
        energy=energy_avg,
        energy_range=(energy_min, energy_max)
    )
