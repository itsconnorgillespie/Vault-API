import logging
from asyncio import create_task
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from aiosmtplib import SMTP, SMTPAuthenticationError
from sqlalchemy.orm import Session
from models import Device, Reading, Notification
from settings import settings

logger = logging.getLogger(__name__)


def check_device_exists(id: str,
                        db: Session) -> Device or None:
    device: Device = db.query(Device).filter(Device.id == id).first()
    return device if device is not None else None


async def send_device_notification(id: str,
                                   reading: Reading,
                                   db: Session):
    # Get email address of the recipient.
    notifications: list[Notification] = db.query(Notification).filter(Notification.device == id).all()
    if notifications is None:
        logger.warning(f"No notification email address for device {id}.")
        return

    # Iterate through subscribed email addresses.
    for notification in notifications:
        # Check that a notification has not already been sent.
        if notification.last is not None and (datetime.utcnow() - notification.last) < timedelta(seconds=settings.NOTIFICATION_INTERVAL_SECONDS):
            logger.info(f"Notification for {notification.email} blocked since interval has not surpassed.")
            return

        # Prepare MIME email body.
        message = MIMEText(f"Temperature hit {reading.temperature}C!")
        message["From"] = settings.SMTP_USERNAME
        message["To"] = notification.email
        message["Subject"] = "Coco Vault Notification"

        try:
            # Send notification email with SMTP.
            async with SMTP(hostname=settings.SMTP_HOST, port=settings.SMTP_PORT) as smtp:
                await smtp.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
                await smtp.send_message(message)

                # Update last notification timestamp.
                notification.last = datetime.utcnow()
                db.commit()
                db.refresh(notification)
                logger.info(f"Sent {notification.email} a notification email.")
        except SMTPAuthenticationError as error:
            logger.error(f"Invalid SMTP credentials.")


def save_device_reading(id: str,
                        temperature: float,
                        humidity: float,
                        db: Session) -> Reading:
    # Add new temperature reading to database.
    reading: Reading = Reading(device=id, temperature=temperature, humidity=humidity)
    db.add(reading)
    db.commit()
    db.refresh(reading)

    # Create new task to send notification.
    create_task(send_device_notification(id, reading, db))

    # Log reading saved and return object.
    logger.info(f"Reading {reading.id} created for device {id}.")
    return reading


def get_readings(minutes: int,
                 db: Session) -> list[Reading]:
    # Get all readings that are within the specified timeframe.
    elapsed = datetime.utcnow() - timedelta(minutes=minutes)
    readings: list[Reading] = db.query(Reading).filter(Reading.timestamp >= elapsed).all()

    # Log and return readings.
    logger.info(f"Returned {len(readings)} readings from the last {minutes} minutes.")
    return readings
