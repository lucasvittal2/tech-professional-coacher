"""Configure health check routes"""
import time

from fastapi import APIRouter
from starlette import status

from tech_professional_coacher.utils.config.settings import settings
from tech_professional_coacher.utils.logs.log import LoggerHandler

logger = LoggerHandler(name=__name__, level="info").getLogger()

router = APIRouter()


@router.get(
    path="/health"
)
async def get_health():
    """
    Endpoint to check the health of the application.

    Returns:
        dict: A dictionary containing the health status, application name,
        application version, elapsed time, and environment.
    """
    start_time = time.time()

    logger.info("Getting health status")

    end_time = time.time()

    return {
        "message": "Applications is healthy!",
        "status": status.HTTP_200_OK,
        "application_name": settings.service_name,
        "application_version": settings.service_version,
        "elapsed_time": f"{end_time - start_time} seconds",
        "environment": settings.stage
    }


@router.get(
    path="/liveness"
)
async def get_liveness():
    """
    Endpoint to check if the application is alive.

    Returns:
        dict: A dictionary containing the liveness status, application name,
        application version, elapsed time, and environment.
    """
    start_time = time.time()

    logger.info("Getting liveness status")

    end_time = time.time()

    return {
        "message": "Applications is alive!",
        "status": status.HTTP_200_OK,
        "application_name": settings.service_name,
        "application_version": settings.service_version,
        "elapsed_time": f"{end_time - start_time} seconds",
        "environment": settings.stage
    }
