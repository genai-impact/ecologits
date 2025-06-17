import pytest
from unittest.mock import Mock, patch
from ecologits.impacts.modeling import GWP, ADPe, PE, Energy
from ecologits.utils.range_value import RangeValue
from ecologits.utils.opentelemetry import OpenTelemetry
from ecologits.tracers.utils import ImpactsOutput


@pytest.fixture
def mock_opentelemetry_setup():
    with patch('ecologits.utils.opentelemetry.OTLPMetricExporter') as mock_exporter_class, \
            patch('ecologits.utils.opentelemetry.PeriodicExportingMetricReader') as mock_reader_class, \
            patch('ecologits.utils.opentelemetry.MeterProvider') as mock_provider_class, \
            patch('ecologits.utils.opentelemetry.metrics') as mock_metrics:
        # Create mock instances
        mock_exporter = Mock()
        mock_reader = Mock()
        mock_provider = Mock()
        mock_meter = Mock()

        # Configure the mocks
        mock_exporter_class.return_value = mock_exporter
        mock_reader_class.return_value = mock_reader
        mock_provider_class.return_value = mock_provider
        mock_metrics.get_meter.return_value = mock_meter

        # Mock counter creation
        mock_counter = Mock()
        mock_meter.create_counter.return_value = mock_counter

        yield {
            'exporter_class': mock_exporter_class,
            'reader_class': mock_reader_class,
            'provider_class': mock_provider_class,
            'metrics': mock_metrics,
            'meter': mock_meter,
            'counter': mock_counter
        }


def test_init(mock_opentelemetry_setup):
    endpoint = "http://localhost:4318/v1/metrics"
    _ = OpenTelemetry(endpoint)

    # Verify OTLPMetricExporter was initialized with the correct endpoint
    mock_opentelemetry_setup['exporter_class'].assert_called_once_with(endpoint=endpoint)

    # Verify PeriodicExportingMetricReader was initialized correctly
    mock_opentelemetry_setup['reader_class'].assert_called_once()

    # Verify MeterProvider was initialized with the reader
    mock_opentelemetry_setup['provider_class'].assert_called_once()

    # Verify metrics provider was set
    mock_opentelemetry_setup['metrics'].set_meter_provider.assert_called_once()

    # Verify meter was created
    mock_opentelemetry_setup['metrics'].get_meter.assert_called_once_with("ecologits")

    # Verify all counters were created (8 counters in total)
    assert mock_opentelemetry_setup['meter'].create_counter.call_count == 8


def test_record_request_with_valid_data(mock_opentelemetry_setup):
    telemetry = OpenTelemetry("http://localhost:4318/v1/metrics")

    # Reset the mock to clear the initialization calls
    mock_counter = mock_opentelemetry_setup['counter']
    mock_counter.add.reset_mock()

    # Create test data
    input_tokens = 100
    output_tokens = 50
    request_latency = 1.5
    model = "gpt-4o-mini"
    endpoint = "openai"

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
        model=model,
        endpoint=endpoint
    )

    # Verify counters were updated with correct values
    expected_labels = {"endpoint": endpoint, "model": model}

    # We expect 8 add calls (one for each counter)
    assert mock_counter.add.call_count == 8

    # Check specific calls
    mock_counter.add.assert_any_call(1, expected_labels)  # request_counter
    mock_counter.add.assert_any_call(input_tokens, expected_labels)  # input_tokens
    mock_counter.add.assert_any_call(output_tokens, expected_labels)  # output_tokens
    mock_counter.add.assert_any_call(request_latency, expected_labels)  # request_latency
    mock_counter.add.assert_any_call(0.1, expected_labels)  # energy_value
    mock_counter.add.assert_any_call(0.2, expected_labels)  # gwp_value
    mock_counter.add.assert_any_call(0.3, expected_labels)  # adpe_value
    mock_counter.add.assert_any_call(0.4, expected_labels)  # pe_value


def test_record_request_with_range_values(mock_opentelemetry_setup):
    telemetry = OpenTelemetry("http://locahost:4318/v1/metrics")

    # Reset the mock to clear the initialization calls
    mock_counter = mock_opentelemetry_setup['counter']
    mock_counter.add.reset_mock()

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
        model="gpt-4o-mini",
        endpoint="openai"
    )
    # Verify mean values were used
    expected_labels = {"endpoint": "openai", "model": "gpt-4o-mini"}
    mock_counter.add.assert_any_call(pytest.approx(0.1), expected_labels)  # energy_value.mean
    mock_counter.add.assert_any_call(pytest.approx(0.2), expected_labels)  # gwp_value.mean
    mock_counter.add.assert_any_call(pytest.approx(0.3), expected_labels)  # adpe_value.mean
    mock_counter.add.assert_any_call(pytest.approx(0.4), expected_labels)  # pe_value.mean


def test_record_request_with_missing_data(mock_opentelemetry_setup):
    telemetry = OpenTelemetry("http://localhost:4318/v1/metrics")

    # Reset the mock to clear the initialization calls
    mock_counter = mock_opentelemetry_setup['counter']
    mock_counter.add.reset_mock()

    # Call with None values
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
        model="gpt-4o-mini",
        endpoint="openai"
    )

    # Verify no counters were updated
    assert mock_counter.add.call_count == 0

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
        model="gpt-4o-mini",
        endpoint="openai"
    )

    # Verify no counters were updated
    assert mock_counter.add.call_count == 0
