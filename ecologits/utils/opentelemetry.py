from contextlib import contextmanager
from typing import Generator

from opentelemetry import context, metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from ecologits.log import logger
from ecologits.tracers.utils import ImpactsOutput
from ecologits.utils.range_value import RangeValue

# Create a context key for your labels
_LABELS_KEY = context.create_key("ecologits_labels")


@contextmanager
def opentelemetry_labels(**user_labels: str) -> Generator[None, None, None]:
    """Context manager using OpenTelemetry's Context API."""
    # Get current labels and merge with new ones
    current_labels = context.get_value(_LABELS_KEY) or {}
    merged_labels = {**current_labels, **user_labels}

    # Create new context with merged labels
    new_ctx = context.set_value(_LABELS_KEY, merged_labels)

    # Attach the new context
    token = context.attach(new_ctx)

    try:
        yield
    finally:
        context.detach(token)


def get_current_labels() -> dict[str, str]:
    """Get labels from current context."""
    return context.get_value(_LABELS_KEY) or {}


class OpenTelemetry:
    def __init__(self, endpoint: str) -> None:
        exporter = OTLPMetricExporter(endpoint=endpoint)
        reader = PeriodicExportingMetricReader(exporter, export_interval_millis=5000)
        provider = MeterProvider(metric_readers=[reader])
        metrics.set_meter_provider(provider)

        meter = metrics.get_meter("ecologits")

        self.request_counter = meter.create_counter(
            name="ecologits_requests_total",
            description="Total number of AI requests",
            unit="1"
        )
        self.input_tokens = meter.create_counter(
            name="ecologits_input_tokens",
            description="Total input tokens",
            unit="1"
        )
        self.output_tokens = meter.create_counter(
            name="ecologits_output_tokens",
            description="Total output tokens",
            unit="1"
        )
        self.request_latency = meter.create_counter(
            name="ecologits_request_latency_seconds",
            description="Request latency in seconds",
            unit="s"
        )
        self.energy_value = meter.create_counter(
            name="ecologits_energy_total",
            description="Total energy consumption",
            unit="kWh"
        )
        self.gwp_value = meter.create_counter(
            name="ecologits_gwp_total",
            description="Total Global Warming Potential",
            unit="kg"
        )
        self.adpe_value = meter.create_counter(
            name="ecologits_adpe_total",
            description="Total Abiotic Depletion Potential for Elements",
            unit="kg"
        )
        self.pe_value = meter.create_counter(
            name="ecologits_pe_total",
            description="Total Primary Energy",
            unit="MJ"
        )

    def record_request(
            self,
            input_tokens: int,
            output_tokens: int,
            request_latency: float,
            impacts: ImpactsOutput,
            model: str,
            endpoint: str
    ) -> None:
        if impacts.energy is None \
                or impacts.gwp is None \
                or impacts.adpe is None \
                or impacts.pe is None:
            logger.error("Skipped sending request metrics because at least one of the impact values is none.")
            return

        # Build default labels
        labels = {
            "endpoint": endpoint,
            "model": model
        }

        # Merge with user-defined labels from context
        user_labels = get_current_labels()
        labels.update(user_labels)

        energy_value = impacts.energy.value.mean if isinstance(impacts.energy.value,
                                                               RangeValue) else impacts.energy.value
        gwp_value = impacts.gwp.value.mean if isinstance(impacts.gwp.value, RangeValue) else impacts.gwp.value
        adpe_value = impacts.adpe.value.mean if isinstance(impacts.adpe.value, RangeValue) else impacts.adpe.value
        pe_value = impacts.pe.value.mean if isinstance(impacts.pe.value, RangeValue) else impacts.pe.value

        self.request_counter.add(1, labels)
        self.input_tokens.add(input_tokens, labels)
        self.output_tokens.add(output_tokens, labels)
        self.request_latency.add(request_latency, labels)
        self.energy_value.add(energy_value, labels)
        self.gwp_value.add(gwp_value, labels)
        self.adpe_value.add(adpe_value, labels)
        self.pe_value.add(pe_value, labels)
