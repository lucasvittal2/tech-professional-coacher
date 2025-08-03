from fastapi import APIRouter
from fastapi.responses import Response
from fastapi import status
from tech_professional_coacher.utils.logs.log import LoggerHandler
from tech_professional_coacher.models.api import *
from tech_professional_coacher.services.authetication import JWTAuthenticationService
from tech_professional_coacher.models.errors import TokenExpiredError, InvalidTokenAuthError
from tech_professional_coacher.utils.tools.agents import call_openai

logger = LoggerHandler(name=__name__).getLogger()
router = APIRouter()

@router.post(path="/test")
async def travel_agent_client(request: TestRequest) -> Response:
    try:
        # Process the request here
        logger.info(f"Received request from {request.agent_name} client")
        auth_service = JWTAuthenticationService()
        auth_service.validate_token(request.token)
        message = call_openai(request.content)

        return TestResponse(
            message=message,
            status="success"
        )
    except TokenExpiredError as e:
        logger.warning(f"Token expired: {e}")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Token expired")

    except InvalidTokenAuthError as e:

        logger.warning(f"Invalid token: {e}")
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="Invalid token"
                        )
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="Internal Server Error")
