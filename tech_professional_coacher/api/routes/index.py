"""Default route and docs route"""
from fastapi import APIRouter, status
from fastapi.openapi.docs import get_swagger_ui_html
from tech_professional_coacher.utils.logs.log import LoggerHandler

logger = LoggerHandler(name=__name__, level="info").getLogger()

router = APIRouter()

@router.get(
    path="/"
)
async def root():
    """
    Default route that returns a welcome message.

    Returns:
        dict: A dictionary containing a message indicating the application is running and a status
            code.
    """
    logger.info("Accessing root function of index route")

    return {
        "message": "Application is running",
        "status": status.HTTP_200_OK
    }

@router.get("/openapi", include_in_schema=False)
async def openapi_docs():
    """
    Route that lead to API docs.

    Returns:
        HTMLResponse: Formatted Docs with UI.
    """

    logger.info("Accessing API docs")

    return get_swagger_ui_html(
        openapi_url="./openapi.json",
        title="Archetype Python IA"
    )
