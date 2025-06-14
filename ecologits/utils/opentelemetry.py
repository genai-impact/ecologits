from typing import Optional

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from ecologits.impacts.modeling import GWP, PE, ADPe, Energy
from ecologits.log import logger
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
            energy: Optional[Energy],
            gwp: Optional[GWP],
            adpe: Optional[ADPe],
            pe: Optional[PE],
            model: str,
            endpoint: str
    ) -> None:
        if energy is None \
                or gwp is None \
                or adpe is None \
                or pe is None:
            logger.error("Skipped sending request metrics because one of the impact values is None.")
            return

        labels = {
            "endpoint": endpoint,
            "model": model
        }

        energy_value = energy.value.mean if isinstance(energy.value, RangeValue) else energy.value
        gwp_value = gwp.value.mean if isinstance(gwp.value, RangeValue) else gwp.value
        adpe_value = adpe.value.mean if isinstance(adpe.value, RangeValue) else adpe.value
        pe_value = pe.value.mean if isinstance(pe.value, RangeValue) else pe.value

        self.request_counter.add(1, labels)
        self.input_tokens.add(input_tokens, labels)
        self.output_tokens.add(output_tokens, labels)
        self.request_latency.add(request_latency, labels)
        self.energy_value.add(energy_value, labels)
        self.gwp_value.add(gwp_value, labels)
        self.adpe_value.add(adpe_value, labels)
        self.pe_value.add(pe_value, labels)
