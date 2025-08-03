"""Define metric telemetry object"""

from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

from tech_professional_coacher.utils.tools.resources import get_telemetry_resource
from tech_professional_coacher.utils.config.settings import settings

meter = None


def initialize_metrics() -> metrics.Meter:
    global meter
    if meter is not None:
        return meter

    reader = PeriodicExportingMetricReader(
        exporter=OTLPMetricExporter(endpoint=settings.otel_exporter_otlp_metrics_endpoint)
    )

    meter_provider = MeterProvider(resource=get_telemetry_resource(), metric_readers=[reader])

    metrics.set_meter_provider(meter_provider=meter_provider)

    meter = metrics.get_meter(settings.service_name, settings.service_version)

    return meter


initialize_metrics()
