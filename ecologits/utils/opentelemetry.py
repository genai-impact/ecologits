from typing import Union

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from ecologits.utils.range_value import RangeValue


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
            energy_value: Union[float, RangeValue],
            gwp_value: Union[float, RangeValue],
            adpe_value: Union[float, RangeValue],
            pe_value: Union[float, RangeValue],
            model: str,
            endpoint: str
    ) -> None:
        labels = {
            "endpoint": endpoint,
            "model": model
        }

        energy_value = energy_value if isinstance(energy_value, (int, float)) else energy_value.avg
        gwp_value = gwp_value if isinstance(gwp_value, (int, float)) else gwp_value.avg
        adpe_value = adpe_value if isinstance(adpe_value, (int, float)) else adpe_value.avg
        pe_value = pe_value if isinstance(pe_value, (int, float)) else pe_value.avg

        self.request_counter.add(1, labels)
        self.input_tokens.add(input_tokens, labels)
        self.output_tokens.add(output_tokens, labels)
        self.request_latency.add(request_latency, labels)
        self.energy_value.add(energy_value, labels)
        self.gwp_value.add(gwp_value, labels)
        self.adpe_value.add(adpe_value, labels)
        self.pe_value.add(pe_value, labels)
