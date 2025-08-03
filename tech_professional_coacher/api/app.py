"""Starts the API"""

import asyncio
import time
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.propagate import extract
from starlette import status
from starlette.requests import Request

from tech_professional_coacher.api.routes import health, index, client
from tech_professional_coacher.utils.config.settings import settings
from tech_professional_coacher.utils.logs.log import LoggerHandler
from tech_professional_coacher.utils.metrics.metric import initialize_metrics
from tech_professional_coacher.utils.traces.tracer import initialize_tracer

logger = LoggerHandler(name=__name__).getLogger()
tracer = initialize_tracer()
initialize_metrics()


logger.info("Starting Application...")
load_dotenv(".env")
testApp = FastAPI(title=settings.service_name, version=settings.service_version, docs_url=None, redoc_url="/openapi-redoc")

logger.info("Application Started")

logger.info("Starting Instrumentation...")
FastAPIInstrumentor().instrument_app(app=testApp)
AsyncioInstrumentor().instrument()
RequestsInstrumentor().instrument()
logger.info("Instrumentation started")


@testApp.middleware("http")
async def timeout_middleware(request: Request, call_next):
    """
    Middleware that sets the timeout of application.

    Returns:
        If errors don't occur, it'll proceed with the request without any probles.
        Else it'll return a JSONResponse with the explanation of the error.
    """
    start_time = time.time()

    try:
        return await asyncio.wait_for(call_next(request), timeout=int(settings.http_timeout))

    except asyncio.TimeoutError:
        process_time = time.time() - start_time
        return JSONResponse(
            {"detail": "Request processing time excedeed limit", "processing_time": process_time},
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
        )


@testApp.middleware("http")
async def tracing_middleware(request: Request, call_next):
    """
    Middleware that traces the request.
    """
    context = extract(request.headers)

    with tracer.start_as_current_span(
        f"request_{request.method}_{request.url}", context=context, kind=trace.SpanKind.SERVER
    ):
        logger.info("Injecting trace context from headers: %s", request.headers)
        span = trace.get_current_span()
        trace_id = span.get_span_context().trace_id
        span_id = span.get_span_context().span_id
        response = await call_next(request)
        response.headers["X-Trace-Id"] = f"{trace_id:032x}"
        response.headers["X-Span-Id"] = f"{span_id:016x}"
        return response


testApp.include_router(router=index.router, prefix="")
testApp.include_router(router=client.router, prefix="")
testApp.include_router(router=health.router, prefix="/health_check")
