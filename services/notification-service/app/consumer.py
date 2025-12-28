import aio_pika
import json
import asyncio
from app.config import get_settings
from app.schemas import NotificationEvent
from app.services import NotificationService

settings = get_settings()


class NotificationConsumer:
    """Consumer for notification events from RabbitMQ"""
    
    connection = None
    channel = None
    queue = None
    
    @classmethod
    async def connect(cls):
        """Connect to RabbitMQ and start consuming"""
        try:
            cls.connection = await aio_pika.connect_robust(settings.RABBITMQ_URL)
            cls.channel = await cls.connection.channel()
            
            # Set QoS
            await cls.channel.set_qos(prefetch_count=10)
            
            # Declare queue
            cls.queue = await cls.channel.declare_queue(
                settings.NOTIFICATION_QUEUE,
                durable=True
            )
            
            print(f"Connected to RabbitMQ, listening on queue: {settings.NOTIFICATION_QUEUE}")
            
            # Start consuming
            await cls.queue.consume(cls.process_message)
            
        except Exception as e:
            print(f"Failed to connect to RabbitMQ: {e}")
            raise
    
    @classmethod
    async def disconnect(cls):
        """Disconnect from RabbitMQ"""
        if cls.connection:
            await cls.connection.close()
            print("Disconnected from RabbitMQ")
    
    @classmethod
    async def process_message(cls, message: aio_pika.IncomingMessage):
        """Process incoming message"""
        async with message.process():
            try:
                # Parse message body
                body = json.loads(message.body.decode())
                event = NotificationEvent(**body)
                
                print(f"Received notification event: {event.event_type}")
                
                # Process the notification
                success = await NotificationService.process_notification(event)
                
                if success:
                    print(f"Successfully processed: {event.event_type}")
                else:
                    print(f"Failed to process: {event.event_type}")
                    
            except json.JSONDecodeError as e:
                print(f"Invalid JSON in message: {e}")
            except Exception as e:
                print(f"Error processing message: {e}")


async def start_consumer():
    """Start the notification consumer"""
    await NotificationConsumer.connect()
    
    # Keep running
    try:
        while True:
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        await NotificationConsumer.disconnect()
