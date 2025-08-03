"""Define tracer telemetry object"""

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from tech_professional_coacher.utils.config.settings import settings
from tech_professional_coacher.utils.tools.resources import get_telemetry_resource

tracer = None


def initialize_tracer() -> trace.Tracer:
    """
    Initialize the tracer

    Returns:
        trace.Tracer: The tracer object
    """

    global tracer, tracer_provider
    if tracer is not None:
        return tracer

    tracer_provider = TracerProvider(resource=get_telemetry_resource())

    processor = BatchSpanProcessor(span_exporter=OTLPSpanExporter(endpoint=settings.otel_exporter_otlp_traces_endpoint))

    tracer_provider.add_span_processor(span_processor=processor)

    trace.set_tracer_provider(tracer_provider=tracer_provider)

    tracer = trace.get_tracer(__name__)

    return tracer


initialize_tracer()
