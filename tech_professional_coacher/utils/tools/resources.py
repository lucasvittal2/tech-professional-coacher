"""Define and create functions to get any resources necessary to the applications"""
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource

from tech_professional_coacher.utils.config.settings import settings


def get_telemetry_resource() -> Resource:
    """
    Function to get resources for telemetry instruments (tracer, metrics and logs).

    Returns:
        Resource: A Resource object containg necessary information to the provide instrumentation.
    """

    return Resource(
        attributes={
            SERVICE_NAME: settings.service_name,
            SERVICE_VERSION: settings.service_version

        }
    )
