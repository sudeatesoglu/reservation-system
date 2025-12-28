import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response
from app.config import get_settings
from app.consumer import NotificationConsumer

settings = get_settings()

# Prometheus metrics
NOTIFICATIONS_PROCESSED = Counter(
    'notifications_processed_total',
    'Total notifications processed',
    ['event_type', 'status']
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("Starting Notification Service...")
    
    # Start consumer in background
    consumer_task = asyncio.create_task(start_consumer_with_retry())
    
    yield
    
    # Shutdown
    print("Shutting down Notification Service...")
    consumer_task.cancel()
    try:
        await consumer_task
    except asyncio.CancelledError:
        pass
    await NotificationConsumer.disconnect()


async def start_consumer_with_retry():
    """Start consumer with retry logic"""
    max_retries = 5
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            await NotificationConsumer.connect()
            # Keep running
            while True:
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Consumer error (attempt {attempt + 1}/{max_retries}): {e}")
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay)
            else:
                print("Max retries reached, consumer stopped")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Notification service for sending emails and alerts",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoints
@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes"""
    return {"status": "healthy", "service": "notification-service"}


@app.get("/ready")
async def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    return {"status": "ready", "service": "notification-service"}


@app.get("/metrics")
def metrics():
    """Prometheus metrics endpoint"""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/")
def root():
    """Root endpoint"""
    return {
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }
