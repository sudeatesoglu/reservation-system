import aio_pika
import json
from app.config import get_settings
from app.schemas import NotificationEvent

settings = get_settings()


class MessageQueue:
    connection = None
    channel = None
    
    @classmethod
    async def connect(cls):
        """Connect to RabbitMQ"""
        try:
            cls.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            cls.channel = await cls.connection.channel()
            
            # Declare the notifications queue
            await cls.channel.declare_queue(
                settings.NOTIFICATION_QUEUE,
                durable=True
            )
            print("Connected to RabbitMQ")
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
    
    @classmethod
    async def disconnect(cls):
        """Disconnect from RabbitMQ"""
        if cls.connection:
            await cls.connection.close()
            print("Disconnected from RabbitMQ")
    
    @classmethod
    async def publish_notification(cls, event: NotificationEvent):
        """Publish notification event to queue"""
        if not cls.channel:
            print("Warning: RabbitMQ not connected, notification not sent")
            return False
        
        try:
            message = aio_pika.Message(
                body=event.model_dump_json().encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                content_type="application/json"
            )
            
            await cls.channel.default_exchange.publish(
                message,
                routing_key=settings.NOTIFICATION_QUEUE
            )
            print(f"Published notification: {event.event_type}")
            return True
        except Exception as e:
            print(f"Failed to publish notification: {e}")
            return False
