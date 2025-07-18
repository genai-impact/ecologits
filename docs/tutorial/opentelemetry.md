# OpenTelemetry support

With the support of [OpenTelemetry :octicons-link-external-16:](https://opentelemetry.io/) in EcoLogits you can monitor request metrics such as the number of input/output tokens or the environmental impacts in time.

## Configuration

To configure OpenTelemetry with EcoLogits, you will need to provide the URL endpoint at the initialization.

```python
from ecologits import EcoLogits
from openai import OpenAI

# Configure OpenTelemetry endpoint in EcoLogits
EcoLogits.init(
    providers=["openai"],
    opentelemetry_endpoint='https://localhost:4318/v1/metrics'
)

client = OpenAI()

# All requests will log ecologits metrics
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Tell me a funny joke!"}]
)
```


## Metrics

EcoLogits will automatically report the following metrics when OpenTelemetry is enabled. 

!!! warning "Different units for impact metrics"
    
    Notice that the units used for impacts differ from the original [`ImpactsOutput`][tracers.utils.ImpactsOutput] object, in order to respect [OpenTelemetry guidelines](https://opentelemetry.io/docs/specs/semconv/general/metrics/#units).


| Metric name                               | Description                                         |
|-------------------------------------------|-----------------------------------------------------|
| `ecologits_requests_total`                | Number of requests                                  |
| `ecologits_input_tokens_total`            | Number of input tokens                              |
| `ecologits_output_tokens_total`           | Number of output tokens                             |
| `ecologits_request_latency_seconds_total` | Request latency in seconds                          |
| `ecologits_energy_joules_total`           | Average energy consumption of the request in joules |
| `ecologits_gwp_gCO2eq_total`              | Average GWP impacts of the request in gCO2eq        |
| `ecologits_adpe_gSbeq_total`              | Average ADPe impacts of the request in gSbeq        |
| `ecologits_pe_joules_total`               | Average PE impacts of the request in joules         |


## Labels

By default, EcoLogits will report two labels:

- `provider`: Name of the provider
- `model`: Name of the model used
- `endpoint`: API endpoint of the request

### Configure custom labels

It is possible to add custom labels to any request using the [`EcoLogits.label`][_ecologits.EcoLogits.label] method.

#### With a context manager

```python hl_lines="10"
from ecologits import EcoLogits
from openai import OpenAI

EcoLogits.init(
    providers=["openai"], 
    opentelemetry_endpoint="http://localhost:4318/v1/metrics"
)
client = OpenAI()

with EcoLogits.label(my_custom_label="test"): # (1)! 
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": "Tell me a funny joke"}]
    )
```

1. Also work with asynchronous code with `async with` syntax.

#### With a function decorator

```python hl_lines="10"
from ecologits import EcoLogits
from openai import OpenAI

EcoLogits.init(
    providers=["openai"], 
    opentelemetry_endpoint="http://localhost:4318/v1/metrics"
)
client = OpenAI()

@EcoLogits.label(task="summarization")  # (1)! 
def summarize(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Summarize this:\n\n{text}"}]
    )
    return response.choices[0].message.content
```

1. Also work with asynchronous functions with `async def` syntax.



    