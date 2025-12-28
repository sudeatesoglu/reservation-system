from typing import List, Optional
from datetime import datetime
from bson import ObjectId
import httpx
from app.database import get_database
from app.schemas import (
    ReservationCreate, ReservationUpdate, ReservationStatus, NotificationEvent
)
from app.config import get_settings
from app.queue import MessageQueue

settings = get_settings()


class ReservationService:
    """Service class for reservation operations"""
    
    COLLECTION = "reservations"
    
    @staticmethod
    def _serialize_reservation(reservation: dict) -> dict:
        """Convert MongoDB document to response format"""
        if reservation:
            reservation["id"] = str(reservation.pop("_id"))
        return reservation
    
    @staticmethod
    async def get_resource_info(resource_id: str, token: str) -> Optional[dict]:
        """Fetch resource info from resource service"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.RESOURCE_SERVICE_URL}/api/v1/resources/{resource_id}",
                    headers={"Authorization": f"Bearer {token}"},
                    timeout=5.0
                )
                if response.status_code == 200:
                    return response.json()
        except Exception as e:
            print(f"Failed to fetch resource info: {e}")
        return None
    
    @staticmethod
    async def check_availability(
        resource_id: str, 
        date: str, 
        start_time: str, 
        end_time: str,
        exclude_reservation_id: Optional[str] = None
    ) -> bool:
        """Check if time slot is available for the resource"""
        db = get_database()
        
        query = {
            "resource_id": resource_id,
            "date": date,
            "status": {"$in": ["pending", "confirmed"]},
            "$or": [
                # New slot starts during existing slot
                {"$and": [
                    {"start_time": {"$lte": start_time}},
                    {"end_time": {"$gt": start_time}}
                ]},
                # New slot ends during existing slot
                {"$and": [
                    {"start_time": {"$lt": end_time}},
                    {"end_time": {"$gte": end_time}}
                ]},
                # New slot contains existing slot
                {"$and": [
                    {"start_time": {"$gte": start_time}},
                    {"end_time": {"$lte": end_time}}
                ]}
            ]
        }
        
        if exclude_reservation_id and ObjectId.is_valid(exclude_reservation_id):
            query["_id"] = {"$ne": ObjectId(exclude_reservation_id)}
        
        conflict = await db[ReservationService.COLLECTION].find_one(query)
        return conflict is None
    
    @staticmethod
    async def create_reservation(
        reservation_data: ReservationCreate,
        user_id: int,
        username: str,
        token: str
    ) -> dict:
        """Create a new reservation"""
        db = get_database()
        
        # Verify resource exists
        resource = await ReservationService.get_resource_info(
            reservation_data.resource_id, token
        )
        resource_name = resource.get("name") if resource else "Unknown Resource"
        
        # Create reservation document
        reservation_dict = {
            "user_id": user_id,
            "username": username,
            "resource_id": reservation_data.resource_id,
            "resource_name": resource_name,
            "date": reservation_data.date,
            "start_time": reservation_data.start_time,
            "end_time": reservation_data.end_time,
            "purpose": reservation_data.purpose,
            "notes": reservation_data.notes,
            "status": ReservationStatus.CONFIRMED.value,
            "created_at": datetime.utcnow(),
            "updated_at": None,
            "cancelled_at": None,
            "cancellation_reason": None
        }
        
        result = await db[ReservationService.COLLECTION].insert_one(reservation_dict)
        reservation_dict["_id"] = result.inserted_id
        
        # Send notification
        await MessageQueue.publish_notification(NotificationEvent(
            event_type="reservation_created",
            user_id=user_id,
            username=username,
            reservation_id=str(result.inserted_id),
            resource_name=resource_name,
            date=reservation_data.date,
            start_time=reservation_data.start_time,
            end_time=reservation_data.end_time
        ))
        
        return ReservationService._serialize_reservation(reservation_dict)
    
    @staticmethod
    async def get_reservation_by_id(reservation_id: str) -> Optional[dict]:
        """Get reservation by ID"""
        db = get_database()
        if not ObjectId.is_valid(reservation_id):
            return None
        reservation = await db[ReservationService.COLLECTION].find_one(
            {"_id": ObjectId(reservation_id)}
        )
        return ReservationService._serialize_reservation(reservation) if reservation else None
    
    @staticmethod
    async def get_user_reservations(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        upcoming_only: bool = False
    ) -> List[dict]:
        """Get reservations for a specific user"""
        db = get_database()
        query = {"user_id": user_id}
        
        if status:
            query["status"] = status
        
        if upcoming_only:
            today = datetime.utcnow().strftime("%Y-%m-%d")
            query["date"] = {"$gte": today}
        
        cursor = db[ReservationService.COLLECTION].find(query).sort(
            [("date", 1), ("start_time", 1)]
        ).skip(skip).limit(limit)
        
        reservations = await cursor.to_list(length=limit)
        return [ReservationService._serialize_reservation(r) for r in reservations]
    
    @staticmethod
    async def get_user_reservations_count(
        user_id: int,
        status: Optional[str] = None
    ) -> int:
        """Get count of user's reservations"""
        db = get_database()
        query = {"user_id": user_id}
        if status:
            query["status"] = status
        return await db[ReservationService.COLLECTION].count_documents(query)
    
    @staticmethod
    async def get_resource_reservations(
        resource_id: str,
        date: Optional[str] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Get reservations for a specific resource"""
        db = get_database()
        query = {"resource_id": resource_id}
        
        if date:
            query["date"] = date
        
        cursor = db[ReservationService.COLLECTION].find(query).sort(
            [("date", 1), ("start_time", 1)]
        ).skip(skip).limit(limit)
        
        reservations = await cursor.to_list(length=limit)
        return [ReservationService._serialize_reservation(r) for r in reservations]
    
    @staticmethod
    async def get_all_reservations(
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        date: Optional[str] = None
    ) -> List[dict]:
        """Get all reservations (admin)"""
        db = get_database()
        query = {}
        
        if status:
            query["status"] = status
        if date:
            query["date"] = date
        
        cursor = db[ReservationService.COLLECTION].find(query).sort(
            [("date", -1), ("start_time", 1)]
        ).skip(skip).limit(limit)
        
        reservations = await cursor.to_list(length=limit)
        return [ReservationService._serialize_reservation(r) for r in reservations]
    
    @staticmethod
    async def get_all_reservations_count(
        status: Optional[str] = None,
        date: Optional[str] = None
    ) -> int:
        """Get count of all reservations"""
        db = get_database()
        query = {}
        if status:
            query["status"] = status
        if date:
            query["date"] = date
        return await db[ReservationService.COLLECTION].count_documents(query)
    
    @staticmethod
    async def update_reservation(
        reservation_id: str,
        update_data: ReservationUpdate
    ) -> Optional[dict]:
        """Update a reservation"""
        db = get_database()
        if not ObjectId.is_valid(reservation_id):
            return None
        
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        if not update_dict:
            return await ReservationService.get_reservation_by_id(reservation_id)
        
        update_dict["updated_at"] = datetime.utcnow()
        
        result = await db[ReservationService.COLLECTION].find_one_and_update(
            {"_id": ObjectId(reservation_id)},
            {"$set": update_dict},
            return_document=True
        )
        return ReservationService._serialize_reservation(result) if result else None
    
    @staticmethod
    async def cancel_reservation(
        reservation_id: str,
        reason: Optional[str] = None
    ) -> Optional[dict]:
        """Cancel a reservation"""
        db = get_database()
        if not ObjectId.is_valid(reservation_id):
            return None
        
        update_data = {
            "status": ReservationStatus.CANCELLED.value,
            "cancelled_at": datetime.utcnow(),
            "cancellation_reason": reason,
            "updated_at": datetime.utcnow()
        }
        
        result = await db[ReservationService.COLLECTION].find_one_and_update(
            {"_id": ObjectId(reservation_id)},
            {"$set": update_data},
            return_document=True
        )
        
        if result:
            # Send cancellation notification
            await MessageQueue.publish_notification(NotificationEvent(
                event_type="reservation_cancelled",
                user_id=result["user_id"],
                username=result["username"],
                reservation_id=reservation_id,
                resource_name=result.get("resource_name", "Unknown"),
                date=result["date"],
                start_time=result["start_time"],
                end_time=result["end_time"],
                additional_data={"reason": reason}
            ))
        
        return ReservationService._serialize_reservation(result) if result else None
    
    @staticmethod
    async def complete_reservation(reservation_id: str) -> Optional[dict]:
        """Mark reservation as completed"""
        db = get_database()
        if not ObjectId.is_valid(reservation_id):
            return None
        
        result = await db[ReservationService.COLLECTION].find_one_and_update(
            {"_id": ObjectId(reservation_id)},
            {"$set": {
                "status": ReservationStatus.COMPLETED.value,
                "updated_at": datetime.utcnow()
            }},
            return_document=True
        )
        return ReservationService._serialize_reservation(result) if result else None
    
    @staticmethod
    async def mark_no_show(reservation_id: str) -> Optional[dict]:
        """Mark reservation as no-show"""
        db = get_database()
        if not ObjectId.is_valid(reservation_id):
            return None
        
        result = await db[ReservationService.COLLECTION].find_one_and_update(
            {"_id": ObjectId(reservation_id)},
            {"$set": {
                "status": ReservationStatus.NO_SHOW.value,
                "updated_at": datetime.utcnow()
            }},
            return_document=True
        )
        return ReservationService._serialize_reservation(result) if result else None
