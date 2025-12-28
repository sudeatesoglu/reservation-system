from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "Reservation Service"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # MongoDB
    MONGODB_URL: str = "mongodb://mongodb:27017"
    MONGODB_DB: str = "reservationdb"
    
    # RabbitMQ
    RABBITMQ_URL: str = "amqp://guest:guest@rabbitmq:5672/"
    NOTIFICATION_QUEUE: str = "notifications"
    
    # JWT Settings (for token validation)
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    
    # Service URLs
    USER_SERVICE_URL: str = "http://user-service:8000"
    RESOURCE_SERVICE_URL: str = "http://resource-service:8001"
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
