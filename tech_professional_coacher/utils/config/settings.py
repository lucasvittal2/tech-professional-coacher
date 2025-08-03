"""Configure environment variables"""

from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    service_name: Optional[str] = Field(None, alias="SERVICE_NAME")
    service_version: Optional[str] = Field(None, alias="SERVICE_VERSION")
    stage: Optional[str] = Field(None, alias="STAGE")
    log_level: Optional[str] = Field(None, alias="LOG_LEVEL")
    http_timeout: Optional[str] = Field(None, alias="HTTP_TIMEOUT")
    http_retry: Optional[str] = Field(None, alias="HTTP_RETRY")
    delay_ms: Optional[str] = Field(None, alias="DELAY_MS")
    otel_exporter_otlp_traces_endpoint: Optional[str] = Field(None, alias="OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    otel_exporter_otlp_metrics_endpoint: Optional[str] = Field(None, alias="OTEL_EXPORTER_OTLP_METRICS_ENDPOINT")
    otel_exporter_otlp_logs_endpoint: Optional[str] = Field(None, alias="OTEL_EXPORTER_OTLP_LOGS_ENDPOINT")
    add_logs_to_console: bool = Field(True, alias="ADD_LOGS_TO_CONSOLE")
    KEYCLOAK_JWKS_URL: Optional[str] = Field(None, alias="KEYCLOAK_JWKS_URL")



settings = Settings()
