"Log module to track application steps"

import logging
from typing import Tuple

from opentelemetry._logs import get_logger_provider, set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from tech_professional_coacher.utils.tools.resources import get_telemetry_resource
from tech_professional_coacher.utils.config.settings import settings

handler: logging.Handler = None
stream_handler: logging.Handler = None



class LoggerHandler(object):
    """
    Logger class
    """

    level_relations = {
        "not_set": logging.NOTSET,
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }

    logger = None
    def __init__(self, level=settings.log_level, name=__name__, mode="local") -> None:
        """
        Class constructor that's initializing all necessary variables and instatiating the root
        logger.
        """
        self._logger = logging.getLogger()
        self._logger.setLevel(self.level_relations.get(level))

        global handler, stream_handler
        handler, stream_handler = self.__initialize_logger()
        if mode == "local":
            # Log locally to console only
            if settings.add_logs_to_console:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
                self._logger.addHandler(console_handler)
                self._logger = logging.getLogger(name)
        elif mode == "online":
            if settings.add_logs_to_console and stream_handler:
                self._logger.addHandler(stream_handler)
            if handler:
                self._logger.addHandler(handler)
            self._logger = logging.getLogger(name)

    def __initialize_logger(self) -> Tuple[logging.Handler, logging.Handler]:
        """
        Initialize the logger

        Returns:
            Tuple[logging.Handler, logging.Handler]: The logger handlers
        """
        global handler, stream_handler
        if handler is not None and stream_handler is not None:
            return handler, stream_handler


        resource = get_telemetry_resource()
        if resource is None:
            resource = Resource(attributes={
                "service.name": settings.service_name,
                "service.version": settings.service_version
            })
        logger_provider = LoggerProvider(
            resource=resource,
        )

        set_logger_provider(logger_provider)

        exporter = OTLPLogExporter(insecure=True, endpoint=settings.otel_exporter_otlp_logs_endpoint)
        logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))

        handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
        stream_handler = logging.StreamHandler()

        return handler, stream_handler

    def getLogger(self) -> logging.Logger:
        return self._logger
