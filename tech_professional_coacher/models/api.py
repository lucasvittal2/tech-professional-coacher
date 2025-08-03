from pydantic import BaseModel, Field

class TestRequest(BaseModel):
    content: str = Field(..., description="text content of the request")
    agent_name: str = Field(..., description="the name of the agent making the request")
    token: str = Field(..., description="JWT token for authentication")

class TestResponse(BaseModel):
    message: str = Field(..., description="response message from the server")
    status: str = Field(..., description="status of the request processing")
