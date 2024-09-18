from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    class Config:
        env_file = [".env"]  # Ensure to only load the default env file.
        env_file_encoding = "utf-8"  # Ensure UTF-8 to allow for parsing of lists in env file.

    APPLICATION_TITLE: str
    APPLICATION_DESCRIPTION: str
    APPLICATION_VERSION: str
    APPLICATION_DEBUG: bool
    SWAGGER_ENABLED: bool
    REDOC_ENABLED: bool
    MQTT_HOST: str
    MQTT_PORT: int
    MQTT_USERNAME: str
    MQTT_PASSWORD: str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USERNAME: str
    SMTP_PASSWORD: str
    SQL_CONNECTION_URI: str
    SQL_DEBUG_ENABLED: bool
    MAX_READINGS_MINUTES: int
    NOTIFICATION_TEMPERATURE_CELSIUS: float
    NOTIFICATION_INTERVAL_SECONDS: int


settings = Settings()
