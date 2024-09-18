import logging
from contextlib import asynccontextmanager
from json import loads, JSONDecodeError
from typing import Any
from fastapi import FastAPI, Depends
from gmqtt import Client as MQTTClient
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.httpsredirect import HTTPSRedirectMiddleware
from starlette.requests import Request
from starlette.templating import Jinja2Templates
from database import Base, engine
from dependencies import get_session
from mqtt import mqtt
from services import check_device_exists, save_device_reading, get_readings
from settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Create database models if they do not exist.
    Base.metadata.create_all(bind=engine)

    # Connect to MQTT broker.
    await mqtt.mqtt_startup()
    yield
    await mqtt.mqtt_shutdown()


app = FastAPI(title=settings.APPLICATION_TITLE,
              description=settings.APPLICATION_DESCRIPTION,
              version=settings.APPLICATION_VERSION,
              debug=settings.APPLICATION_DEBUG,
              docs_url="/docs" if settings.SWAGGER_ENABLED else None,
              redoc_url="/redoc" if settings.REDOC_ENABLED else None,
              swagger_ui_parameters={"defaultModelsExpandDepth": -1},
              lifespan=lifespan)
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger(__name__)

# Set application middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@mqtt.subscribe("devices/+/readings", qos=1)
async def subscribe(client: MQTTClient,
                    topic: str,
                    payload: bytes,
                    qos: int,
                    properties: Any):
    # Log received payload from topic.
    logger.info(f"MQTT Topic {topic} | {payload.decode()}")

    # Attempt to parse payload.
    try:
        id = topic.split("/")[1]
        data = loads(payload.decode())
        if "temperature" not in data or "humidity" not in data:
            return

        # Create new database instance and get device by identifier.
        # Need to use next() to initialize generator. Needed to fix max connection pool issues.
        db: Session = next(get_session())
        device = check_device_exists(id, db)

        # Ensure device exists before saving reading.
        if device is None:
            logging.error(f"Device {id} does not exist.")
            return

        # Check the device is not disabled before saving reading.
        if device.disabled:
            logging.error(f"Device {id} disabled.")
            return

        # Save device reading to database.
        save_device_reading(id, data["temperature"], data["humidity"], db)
    except (ValueError, KeyError, UnicodeDecodeError, JSONDecodeError):
        logger.error("Unable to parse payload.")
        return


@app.get("/",
         summary="Returns frontend to the client.")
async def get(request: Request):
    return templates.TemplateResponse(
        request=request, name="readings.html", context={}
    )


@app.get("/readings",
         summary="Returns readings for all devices within a given timeframe.")
async def get(minutes: int = 5,
              db: Session = Depends(get_session)):
    return get_readings((settings.MAX_READINGS_MINUTES if minutes > settings.MAX_READINGS_MINUTES else minutes), db)
