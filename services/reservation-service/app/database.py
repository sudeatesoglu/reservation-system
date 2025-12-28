from motor.motor_asyncio import AsyncIOMotorClient
from app.config import get_settings

settings = get_settings()


class Database:
    client: AsyncIOMotorClient = None
    db = None


db = Database()


async def connect_to_mongo():
    """Connect to MongoDB"""
    db.client = AsyncIOMotorClient(settings.MONGODB_URL)
    db.db = db.client[settings.MONGODB_DB]
    
    # Create indexes
    await db.db.reservations.create_index("user_id")
    await db.db.reservations.create_index("resource_id")
    await db.db.reservations.create_index("status")
    await db.db.reservations.create_index([("date", 1), ("start_time", 1)])
    
    print(f"Connected to MongoDB: {settings.MONGODB_DB}")


async def close_mongo_connection():
    """Close MongoDB connection"""
    if db.client:
        db.client.close()
        print("Closed MongoDB connection")


def get_database():
    """Get database instance"""
    return db.db
