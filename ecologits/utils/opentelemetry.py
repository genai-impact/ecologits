import asyncio
from functools import wraps
from typing import Any, Callable, Optional

from opentelemetry import context, metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from ecologits.log import logger
from ecologits.tracers.utils import ImpactsOutput
from ecologits.utils.range_value import RangeValue

# Create a context key for your labels
_LABELS_KEY = context.create_key("ecologits_labels")


class OpenTelemetryLabels:
    """Context manager supporting both sync and async for OpenTelemetry labels."""

    def __init__(self, **user_labels: str) -> None:
        self.user_labels = user_labels
        self.token = None

    def __enter__(self) -> "OpenTelemetryLabels":
        self._setup_context()
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        self._cleanup_context()

    async def __aenter__(self) -> "OpenTelemetryLabels":
        self._setup_context()
        return self

    async def __aexit__(self, exc_type: Optional[type], exc_val: Optional[Exception], exc_tb: Optional[Any]) -> None:
        self._cleanup_context()

    def __call__(self, func: Callable) -> Callable:
        if asyncio.iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                with self:
                    return await func(*args, **kwargs)
            return async_wrapper
        else:
            @wraps(func)
            def wrapper(*args: Any, **kwargs: Any) -> Any:
                with self:
                    return func(*args, **kwargs)
            return wrapper

    def _setup_context(self) -> None:
        """Common setup logic for both sync and async."""
        current_labels = context.get_value(_LABELS_KEY) or {}
        merged_labels = {**current_labels, **self.user_labels}
        new_ctx = context.set_value(_LABELS_KEY, merged_labels)
        self.token = context.attach(new_ctx)

    def _cleanup_context(self) -> None:
        """Common cleanup logic for both sync and async."""
        if self.token is not None:
            context.detach(self.token)


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
            name="ecologits_requests",
            description="Total number of AI requests",
            unit="1"
        )
        self.input_tokens = meter.create_gauge(
            name="ecologits_input_tokens",
            description="Input tokens",
            unit="1"
        )
        self.output_tokens = meter.create_gauge(
            name="ecologits_output_tokens",
            description="Output tokens",
            unit="1"
        )
        self.request_latency = meter.create_gauge(
            name="ecologits_request_latency",
            description="Request latency in seconds",
            unit="s"
        )
        self.energy_value = meter.create_gauge(
            name="ecologits_energy",
            description="Energy consumption in joules",
            unit="joules"
        )
        self.gwp_value = meter.create_gauge(
            name="ecologits_gwp",
            description="Global Warming Potential in grams of CO2 equivalent",
            unit="gCO2eq"
        )
        self.adpe_value = meter.create_gauge(
            name="ecologits_adpe",
            description="Abiotic Depletion Potential for Elements in grams of Sb equivalent",
            unit="gSbeq"
        )
        self.pe_value = meter.create_gauge(
            name="ecologits_pe",
            description="Primary Energy in joules",
            unit="joules"
        )

    def record_request(
            self,
            input_tokens: int,
            output_tokens: int,
            request_latency: float,
            impacts: ImpactsOutput,
            provider: str,
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
            "provider": provider,
            "endpoint": endpoint,
            "model": model
        }

        # Merge with user-defined labels from context
        user_labels = get_current_labels()
        labels.update(user_labels)

        energy_value = (
            impacts.energy.value.mean if isinstance(impacts.energy.value, RangeValue) else impacts.energy.value
        )
        energy_value *= 3_600_000  # convert kWh to J

        gwp_value = impacts.gwp.value.mean if isinstance(impacts.gwp.value, RangeValue) else impacts.gwp.value
        gwp_value *= 1000  # convert kg to g

        adpe_value = impacts.adpe.value.mean if isinstance(impacts.adpe.value, RangeValue) else impacts.adpe.value
        adpe_value *= 1000  # convert kg to g

        pe_value = impacts.pe.value.mean if isinstance(impacts.pe.value, RangeValue) else impacts.pe.value
        pe_value *= 1_000_000  # convert MJ to J

        self.request_counter.add(1, labels)
        self.input_tokens.set(input_tokens, labels)
        self.output_tokens.set(output_tokens, labels)
        self.request_latency.set(request_latency, labels)
        self.energy_value.set(energy_value, labels)
        self.gwp_value.set(gwp_value, labels)
        self.adpe_value.set(adpe_value, labels)
        self.pe_value.set(pe_value, labels)
