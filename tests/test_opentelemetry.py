from unittest.mock import patch

import pytest
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import InMemoryMetricReader

from ecologits.impacts.modeling import GWP, PE, ADPe, Energy
from ecologits.tracers.utils import ImpactsOutput
from ecologits.utils.opentelemetry import OpenTelemetry, OpenTelemetryLabels, get_current_labels
from ecologits.utils.range_value import RangeValue


@pytest.fixture
def in_memory_telemetry():
    """Create OpenTelemetry instance with in-memory metric reader for testing."""

    # Create in-memory reader to capture metrics
    reader = InMemoryMetricReader()
    provider = MeterProvider(metric_readers=[reader])

    # Patch the OpenTelemetry class to use our in-memory setup
    with patch("ecologits.utils.opentelemetry.OTLPMetricExporter"), \
            patch("ecologits.utils.opentelemetry.PeriodicExportingMetricReader") as mock_reader, \
            patch("ecologits.utils.opentelemetry.MeterProvider") as mock_provider, \
            patch("ecologits.utils.opentelemetry.metrics") as mock_metrics:

        # Configure mocks to use our in-memory setup
        mock_reader.return_value = reader
        mock_provider.return_value = provider
        mock_metrics.set_meter_provider.side_effect = lambda p: metrics.set_meter_provider(provider)
        mock_metrics.get_meter.side_effect = lambda name: provider.get_meter(name)

        # Create telemetry instance
        telemetry = OpenTelemetry("http://fake-endpoint:4318/v1/metrics")

        yield telemetry, reader


def get_metric_data(reader, metric_name):
    """Helper to extract metric data from the in-memory reader."""
    metrics_data = reader.get_metrics_data()
    if not metrics_data:
        return None

    for resource_metrics in metrics_data.resource_metrics:
        for scope_metrics in resource_metrics.scope_metrics:
            for metric in scope_metrics.metrics:
                if metric.name == metric_name:
                    return metric
    return None


def get_metric_value_with_attributes(metric, expected_attributes):
    """Helper to get metric value for specific attributes."""
    if not metric or not metric.data or not metric.data.data_points:
        return None

    for data_point in metric.data.data_points:
        # Convert attributes to dict for comparison
        point_attributes = dict(data_point.attributes) if data_point.attributes else {}
        if point_attributes == expected_attributes:
            return data_point.value
    return None


def test_init(in_memory_telemetry):
    telemetry, reader = in_memory_telemetry

    # Just verify that the telemetry instance was created successfully
    assert telemetry is not None
    assert reader is not None

    # The counters should be accessible as attributes
    assert hasattr(telemetry, "request_counter")
    assert hasattr(telemetry, "input_tokens")
    assert hasattr(telemetry, "output_tokens")
    assert hasattr(telemetry, "request_latency")
    assert hasattr(telemetry, "energy_value")
    assert hasattr(telemetry, "gwp_value")
    assert hasattr(telemetry, "adpe_value")
    assert hasattr(telemetry, "pe_value")


def test_record_request_with_valid_data(in_memory_telemetry):
    telemetry, reader = in_memory_telemetry

    # Create test data
    input_tokens = 100
    output_tokens = 50
    request_latency = 1.5
    model = "gpt-4o-mini"
    provider = "openai"
    endpoint = "/chat/completions"

    # Call the method
    telemetry.record_request(
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        request_latency=request_latency,
        impacts=ImpactsOutput(
            energy=Energy(value=0.1),
            gwp=GWP(value=0.2),
            adpe=ADPe(value=0.3),
            pe=PE(value=0.4)
        ),
        provider=provider,
        model=model,
        endpoint=endpoint
    )

    # Force collection of metrics
    reader.collect()

    # Verify counters were updated with correct values
    expected_labels = {"endpoint": endpoint, "model": model, "provider": provider}

    # Check that metrics were created with correct values
    request_metric = get_metric_data(reader, "ecologits_requests")
    assert request_metric is not None
    assert get_metric_value_with_attributes(request_metric, expected_labels) == 1

    # input_tokens_metric = get_metric_data(reader, "ecologits_input_tokens")
    # assert input_tokens_metric is not None
    # assert get_metric_value_with_attributes(input_tokens_metric, expected_labels) == input_tokens
    #
    # output_tokens_metric = get_metric_data(reader, "ecologits_output_tokens")
    # assert output_tokens_metric is not None
    # assert get_metric_value_with_attributes(output_tokens_metric, expected_labels) == output_tokens
    #
    # request_latency_metric = get_metric_data(reader, "ecologits_request_latency")
    # assert request_latency_metric is not None
    # assert get_metric_value_with_attributes(request_latency_metric, expected_labels) == request_latency
    #
    # energy_metric = get_metric_data(reader, "ecologits_energy")
    # assert energy_metric is not None
    # assert get_metric_value_with_attributes(energy_metric, expected_labels) == 0.1 * 3_600_000
    #
    # gwp_metric = get_metric_data(reader, "ecologits_gwp")
    # assert gwp_metric is not None
    # assert get_metric_value_with_attributes(gwp_metric, expected_labels) == 0.2 * 1000
    #
    # adpe_metric = get_metric_data(reader, "ecologits_adpe")
    # assert adpe_metric is not None
    # assert get_metric_value_with_attributes(adpe_metric, expected_labels) == 0.3 * 1000
    #
    # pe_metric = get_metric_data(reader, "ecologits_pe")
    # assert pe_metric is not None
    # assert get_metric_value_with_attributes(pe_metric, expected_labels) == 0.4 * 1_000_000


@pytest.mark.skip()
def test_record_request_with_range_values(in_memory_telemetry):
    telemetry, reader = in_memory_telemetry

    telemetry.record_request(
        input_tokens=100,
        output_tokens=50,
        request_latency=1.5,
        impacts=ImpactsOutput(
            energy=Energy(value=RangeValue(min=0.05, max=0.15)),    # mean = 0.1
            gwp=GWP(value=RangeValue(min=0.1, max=0.3)),            # mean = 0.2
            adpe=ADPe(value=RangeValue(min=0.2, max=0.4)),          # mean = 0.3
            pe=PE(value=RangeValue(min=0.3, max=0.5)),              # mean = 0.4
        ),
        provider="openai",
        model="gpt-4o-mini",
        endpoint="/chat/completions"
    )

    # Force collection
    reader.collect()

    # Verify mean values were used
    expected_labels = {"provider": "openai", "model": "gpt-4o-mini", "endpoint": "/chat/completions"}

    energy_metric = get_metric_data(reader, "ecologits_energy")
    assert get_metric_value_with_attributes(energy_metric, expected_labels) == pytest.approx(0.1 * 3_600_000)

    gwp_metric = get_metric_data(reader, "ecologits_gwp")
    assert get_metric_value_with_attributes(gwp_metric, expected_labels) == pytest.approx(0.2 * 1000)

    adpe_metric = get_metric_data(reader, "ecologits_adpe")
    assert get_metric_value_with_attributes(adpe_metric, expected_labels) == pytest.approx(0.3 * 1000)

    pe_metric = get_metric_data(reader, "ecologits_pe")
    assert get_metric_value_with_attributes(pe_metric, expected_labels) == pytest.approx(0.4 * 1_000_000)


def test_record_request_with_missing_data(in_memory_telemetry):
    telemetry, reader = in_memory_telemetry

    # Call with None values - should not record any metrics
    telemetry.record_request(
        input_tokens=100,
        output_tokens=50,
        request_latency=1.5,
        impacts=ImpactsOutput(
            energy=None,
            gwp=GWP(value=0.2),
            adpe=ADPe(value=0.3),
            pe=PE(value=0.4)
        ),
        provider="openai",
        model="gpt-4o-mini",
        endpoint="/chat/completions"
    )

    reader.collect()

    # Verify no counters were updated
    request_metric = get_metric_data(reader, "ecologits_requests")
    assert request_metric is None or len(request_metric.data.data_points) == 0

    # Test with another None value
    telemetry.record_request(
        input_tokens=100,
        output_tokens=50,
        request_latency=1.5,
        impacts=ImpactsOutput(
            energy=Energy(value=0.1),
            gwp=GWP(value=0.2),
            adpe=None,
            pe=PE(value=0.4)
        ),
        provider="openai",
        model="gpt-4o-mini",
        endpoint="/chat/completions"
    )

    reader.collect()

    # Verify still no counters were updated
    request_metric = get_metric_data(reader, "ecologits_requests")
    assert request_metric is None or len(request_metric.data.data_points) == 0


def test_otel_labels_context_basic_functionality():
    """Test that otel_labels context manager correctly stores and retrieves labels."""
    # Test outside context - should be empty
    assert get_current_labels() == {}

    # Test inside context
    with OpenTelemetryLabels(user_id="user123", experiment="test"):
        labels = get_current_labels()
        assert labels == {"user_id": "user123", "experiment": "test"}

    # Test after context - should be empty again
    assert get_current_labels() == {}


def test_otel_labels_nested_contexts():
    """Test nested otel_labels contexts merge correctly."""
    with OpenTelemetryLabels(experiment="main", version="1.0"):
        # First level
        assert get_current_labels() == {"experiment": "main", "version": "1.0"}

        with OpenTelemetryLabels(user_id="user123", experiment="override"):
            # Second level - experiment should be overridden
            expected = {"experiment": "override", "version": "1.0", "user_id": "user123"}
            assert get_current_labels() == expected

            with OpenTelemetryLabels(temp_flag=True):
                # Third level - add more labels
                expected = {
                    "experiment": "override",
                    "version": "1.0",
                    "user_id": "user123",
                    "temp_flag": True
                }
                assert get_current_labels() == expected

            # Back to second level
            expected = {"experiment": "override", "version": "1.0", "user_id": "user123"}
            assert get_current_labels() == expected

        # Back to first level
        assert get_current_labels() == {"experiment": "main", "version": "1.0"}


def test_record_request_with_user_labels(in_memory_telemetry):
    """Test that user labels from context are included in metrics."""
    telemetry, reader = in_memory_telemetry

    # Record request with user labels
    with OpenTelemetryLabels(user_id="user123", experiment="test_run"):
        telemetry.record_request(
            input_tokens=200,
            output_tokens=100,
            request_latency=2.0,
            impacts=ImpactsOutput(
                energy=Energy(value=0.2),
                gwp=GWP(value=0.4),
                adpe=ADPe(value=0.6),
                pe=PE(value=0.8)
            ),
            provider="openai",
            model="gpt-4",
            endpoint="/chat/completions"
        )

    # Force collection
    reader.collect()

    # Check that metrics include both system and user labels
    expected_attributes = {
        "provider": "openai",
        "model": "gpt-4",
        "endpoint": "/chat/completions",
        "user_id": "user123",
        "experiment": "test_run"
    }

    request_metric = get_metric_data(reader, "ecologits_requests")
    assert request_metric is not None
    assert get_metric_value_with_attributes(request_metric, expected_attributes) == 1

    # energy_metric = get_metric_data(reader, "ecologits_energy")
    # assert energy_metric is not None
    # assert get_metric_value_with_attributes(energy_metric, expected_attributes) == 0.2 * 3_600_000


def test_multiple_requests_with_different_labels(in_memory_telemetry):
    """Test multiple requests with different label combinations."""
    telemetry, reader = in_memory_telemetry

    # First request with user labels
    with OpenTelemetryLabels(user_id="user1", environment="prod"):
        telemetry.record_request(
            input_tokens=100,
            output_tokens=50,
            request_latency=1.0,
            impacts=ImpactsOutput(
                energy=Energy(value=0.1),
                gwp=GWP(value=0.1),
                adpe=ADPe(value=0.1),
                pe=PE(value=0.1)
            ),
            provider="openai",
            model="gpt-4",
            endpoint="/chat/completions"
        )

    # Second request with different user labels
    with OpenTelemetryLabels(user_id="user2", environment="dev"):
        telemetry.record_request(
            input_tokens=150,
            output_tokens=75,
            request_latency=1.5,
            impacts=ImpactsOutput(
                energy=Energy(value=0.15),
                gwp=GWP(value=0.15),
                adpe=ADPe(value=0.15),
                pe=PE(value=0.15)
            ),
            provider="openai",
            model="gpt-4",
            endpoint="/chat/completions"
        )

    # Third request without user labels
    telemetry.record_request(
        input_tokens=200,
        output_tokens=100,
        request_latency=2.0,
        impacts=ImpactsOutput(
            energy=Energy(value=0.2),
            gwp=GWP(value=0.2),
            adpe=ADPe(value=0.2),
            pe=PE(value=0.2)
        ),
        provider="openai",
        model="gpt-4",
        endpoint="/chat/completions"
    )

    # Force collection
    reader.collect()

    # Check that we have three separate metric series
    request_metric = get_metric_data(reader, "ecologits_requests")
    assert request_metric is not None
    assert len(request_metric.data.data_points) == 3

    # Check specific values for each label combination
    attrs1 = {"provider": "openai", "model": "gpt-4", "endpoint": "/chat/completions", "user_id": "user1",
              "environment": "prod"}
    attrs2 = {"provider": "openai", "model": "gpt-4", "endpoint": "/chat/completions", "user_id": "user2",
              "environment": "dev"}
    attrs3 = {"provider": "openai", "model": "gpt-4", "endpoint": "/chat/completions"}

    assert get_metric_value_with_attributes(request_metric, attrs1) == 1
    assert get_metric_value_with_attributes(request_metric, attrs2) == 1
    assert get_metric_value_with_attributes(request_metric, attrs3) == 1

    # Check input tokens for each series
    # input_tokens_metric = get_metric_data(reader, "ecologits_input_tokens")
    # assert get_metric_value_with_attributes(input_tokens_metric, attrs1) == 100
    # assert get_metric_value_with_attributes(input_tokens_metric, attrs2) == 150
    # assert get_metric_value_with_attributes(input_tokens_metric, attrs3) == 200


def test_context_isolation_across_threads():
    """Test that contextvars properly isolate labels across different contexts."""
    import queue
    import threading
    import time

    results = queue.Queue()

    def worker(worker_id, result_queue):
        with OpenTelemetryLabels(worker_id=worker_id, thread="worker"):
            # Sleep to allow other threads to run
            time.sleep(0.1)
            labels = get_current_labels()
            result_queue.put((worker_id, labels))

    # Start multiple threads
    threads = []
    for i in range(3):
        t = threading.Thread(target=worker, args=(f"worker_{i}", results))
        threads.append(t)
        t.start()

    # Wait for all threads
    for t in threads:
        t.join()

    # Check results - each thread should have its own labels
    collected_results = []
    while not results.empty():
        collected_results.append(results.get())

    assert len(collected_results) == 3

    # Each worker should have its own worker_id
    worker_ids = {result[1]["worker_id"] for result in collected_results}
    assert worker_ids == {"worker_0", "worker_1", "worker_2"}

    # All should have the same thread label
    thread_labels = {result[1]["thread"] for result in collected_results}
    assert thread_labels == {"worker"}
