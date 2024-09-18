from fastapi_mqtt import FastMQTT, MQTTConfig
from settings import settings

# Prepare MQTT credentials.
mqtt = FastMQTT(
    config=MQTTConfig(
        host=settings.MQTT_HOST,
        port=settings.MQTT_PORT,
        username=settings.MQTT_USERNAME,
        password=settings.MQTT_PASSWORD,
    ))
