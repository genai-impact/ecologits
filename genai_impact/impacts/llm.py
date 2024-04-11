from math import ceil
from typing import Optional

from genai_impact.impacts.dag import DAG
from genai_impact.impacts.models import Impacts, Embodied, Usage, GWP, ADPe, PE, Energy


MODEL_QUANTIZATION_BITS = 4

GPU_ENERGY_ALPHA = 8.91e-8
GPU_ENERGY_BETA = 1.43e-6
GPU_LATENCY_ALPHA = 8.02e-4
GPU_LATENCY_BETA = 2.23e-2
GPU_MEMORY = 80     # GB
GPU_EMBODIED_IMPACT_GWP = 143
GPU_EMBODIED_IMPACT_ADPE = 5.1e-3
GPU_EMBODIED_IMPACT_PE = 1828


SERVER_GPUS = 8
SERVER_POWER = 1     # kW
SERVER_EMBODIED_IMPACT_GWP = 3000
SERVER_EMBODIED_IMPACT_ADPE = 0.24
SERVER_EMBODIED_IMPACT_PE = 38000

HARDWARE_LIFESPAN = 5 * 365 * 24 * 60 * 60

DATACENTER_PUE = 1.2

IF_ELECTRICITY_MIX_GWP = 5.90478e-1     # kgCO2eq / kWh (World)
IF_ELECTRICITY_MIX_ADPE = 7.37708e-8    # kgSbeq / kWh (World)
IF_ELECTRICITY_MIX_PE = 9.988           # MJ / kWh (World)


dag = DAG()


@dag.asset
def gpu_energy(
    model_parameter_count: float,
    output_token_count: float,
    gpu_energy_alpha: float,
    gpu_energy_beta: float
) -> float:
    return output_token_count * (gpu_energy_alpha * model_parameter_count + gpu_energy_beta)


@dag.asset
def generation_latency(
    model_parameter_count: float,
    output_token_count: float,
    gpu_latency_alpha: float,
    gpu_latency_beta: float,
    request_latency: float,
) -> float:
    gpu_latency = output_token_count * (gpu_latency_alpha * model_parameter_count + gpu_latency_beta)
    return min(gpu_latency, request_latency)


@dag.asset
def model_required_memory(
    model_parameter_count: float,
    model_quantization_bits: int,
) -> float:
    return 1.2 * model_parameter_count * model_quantization_bits / 8


@dag.asset
def gpu_required_count(
    model_required_memory: float,
    gpu_memory: float
) -> int:
    return ceil(model_required_memory / gpu_memory)


@dag.asset
def server_energy(
    generation_latency: float,
    server_power: float,
    server_gpu_count: int,
    gpu_required_count: int
) -> float:
    return generation_latency * server_power * (gpu_required_count / server_gpu_count)


@dag.asset
def request_energy(
    datacenter_pue: float,
    server_energy: float,
    gpu_required_count: int,
    gpu_energy: float
) -> float:
    return datacenter_pue * (server_energy + gpu_required_count * gpu_energy)


@dag.asset
def request_usage_gwp(
    request_energy: float,
    if_electricity_mix_gwp: float
) -> float:
    return request_energy * if_electricity_mix_gwp


@dag.asset
def request_usage_adpe(
    request_energy: float,
    if_electricity_mix_adpe: float
) -> float:
    return request_energy * if_electricity_mix_adpe


@dag.asset
def request_usage_pe(
    request_energy: float,
    if_electricity_mix_pe: float
) -> float:
    return request_energy * if_electricity_mix_pe


@dag.asset
def server_gpu_embodied_gwp(
    server_embodied_gwp: float,
    server_gpu_count: float,
    gpu_embodied_gwp: float,
    gpu_required_count: int
) -> float:
    return (gpu_required_count / server_gpu_count) * server_embodied_gwp + gpu_required_count * gpu_embodied_gwp


@dag.asset
def server_gpu_embodied_adpe(
    server_embodied_adpe: float,
    server_gpu_count: float,
    gpu_embodied_adpe: float,
    gpu_required_count: int
) -> float:
    return (gpu_required_count / server_gpu_count) * server_embodied_adpe + gpu_required_count * gpu_embodied_adpe


@dag.asset
def server_gpu_embodied_pe(
    server_embodied_pe: float,
    server_gpu_count: float,
    gpu_embodied_pe: float,
    gpu_required_count: int
) -> float:
    return (gpu_required_count / server_gpu_count) * server_embodied_pe + gpu_required_count * gpu_embodied_pe


@dag.asset
def request_embodied_gwp(
    server_gpu_embodied_gwp: float,
    server_lifetime: float,
    generation_latency: float
) -> float:
    return (generation_latency / server_lifetime) * server_gpu_embodied_gwp


@dag.asset
def request_embodied_adpe(
    server_gpu_embodied_adpe: float,
    server_lifetime: float,
    generation_latency: float
) -> float:
    return (generation_latency / server_lifetime) * server_gpu_embodied_adpe


@dag.asset
def request_embodied_pe(
    server_gpu_embodied_pe: float,
    server_lifetime: float,
    generation_latency: float
) -> float:
    return (generation_latency / server_lifetime) * server_gpu_embodied_pe


def compute_llm_impacts(
    model_parameter_count: float,
    output_token_count: float,
    request_latency: float,
    model_quantization_bits: Optional[int] = MODEL_QUANTIZATION_BITS,
    gpu_energy_alpha: Optional[float] = GPU_ENERGY_ALPHA,
    gpu_energy_beta: Optional[float] = GPU_ENERGY_BETA,
    gpu_latency_alpha: Optional[float] = GPU_LATENCY_ALPHA,
    gpu_latency_beta: Optional[float] = GPU_LATENCY_BETA,
    gpu_memory: Optional[float] = GPU_MEMORY,
    gpu_embodied_gwp: Optional[float] = GPU_EMBODIED_IMPACT_GWP,
    gpu_embodied_adpe: Optional[float] = GPU_EMBODIED_IMPACT_ADPE,
    gpu_embodied_pe: Optional[float] = GPU_EMBODIED_IMPACT_PE,
    server_gpu_count: Optional[int] = SERVER_GPUS,
    server_power: Optional[float] = SERVER_POWER,
    server_embodied_gwp: Optional[float] = SERVER_EMBODIED_IMPACT_GWP,
    server_embodied_adpe: Optional[float] = SERVER_EMBODIED_IMPACT_ADPE,
    server_embodied_pe: Optional[float] = SERVER_EMBODIED_IMPACT_PE,
    server_lifetime: Optional[float] = HARDWARE_LIFESPAN,
    datacenter_pue: Optional[float] = DATACENTER_PUE,
    if_electricity_mix_gwp: Optional[float] = IF_ELECTRICITY_MIX_GWP,
    if_electricity_mix_adpe: Optional[float] = IF_ELECTRICITY_MIX_ADPE,
    if_electricity_mix_pe: Optional[float] = IF_ELECTRICITY_MIX_PE,
) -> Impacts:
    results = dag.execute(
        model_parameter_count=model_parameter_count,
        model_quantization_bits=model_quantization_bits,
        output_token_count=output_token_count,
        request_latency=request_latency,
        gpu_energy_alpha=gpu_energy_alpha,
        gpu_energy_beta=gpu_energy_beta,
        gpu_latency_alpha=gpu_latency_alpha,
        gpu_latency_beta=gpu_latency_beta,
        gpu_memory=gpu_memory,
        gpu_embodied_gwp=gpu_embodied_gwp,
        gpu_embodied_adpe=gpu_embodied_adpe,
        gpu_embodied_pe=gpu_embodied_pe,
        server_gpu_count=server_gpu_count,
        server_power=server_power,
        server_embodied_gwp=server_embodied_gwp,
        server_embodied_adpe=server_embodied_adpe,
        server_embodied_pe=server_embodied_pe,
        server_lifetime=server_lifetime,
        datacenter_pue=datacenter_pue,
        if_electricity_mix_gwp=if_electricity_mix_gwp,
        if_electricity_mix_adpe=if_electricity_mix_adpe,
        if_electricity_mix_pe=if_electricity_mix_pe
    )
    energy = Energy(value=results['request_energy'])
    gwp_usage = GWP(value=results['request_usage_gwp'])
    adpe_usage = ADPe(value=results['request_usage_adpe'])
    pe_usage = PE(value=results['request_usage_pe'])
    gwp_embodied = GWP(value=results['request_embodied_gwp'])
    adpe_embodied = ADPe(value=results['request_embodied_adpe'])
    pe_embodied = PE(value=results['request_embodied_pe'])
    return Impacts(
        energy=energy,
        gwp=gwp_usage + gwp_embodied,
        adpe=adpe_usage + adpe_embodied,
        pe=pe_usage + pe_embodied,
        usage=Usage(
            energy=energy,
            gwp=gwp_usage,
            adpe=adpe_usage,
            pe=pe_usage
        ),
        embodied=Embodied(
            gwp=gwp_embodied,
            adpe=adpe_embodied,
            pe=pe_embodied
        )
    )


if __name__ == '__main__':
    print(compute_llm_impacts(70, 200, 10))
