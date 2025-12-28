from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, time
from enum import Enum
from bson import ObjectId


class ResourceType(str, Enum):
    LIBRARY_DESK = "library_desk"
    STUDY_ROOM = "study_room"
    MEETING_ROOM = "meeting_room"
    OFFICE = "office"
    COMPUTER_LAB = "computer_lab"


class ResourceStatus(str, Enum):
    AVAILABLE = "available"
    MAINTENANCE = "maintenance"
    UNAVAILABLE = "unavailable"


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema, handler):
        return {"type": "string"}


# Time Slot Schema
class TimeSlot(BaseModel):
    start_time: str  # Format: "HH:MM"
    end_time: str    # Format: "HH:MM"


# Request Schemas
class ResourceCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    resource_type: ResourceType
    description: Optional[str] = None
    location: str = Field(..., min_length=1)
    building: Optional[str] = None
    floor: Optional[int] = None
    capacity: int = Field(default=1, ge=1)
    amenities: List[str] = []
    available_days: List[int] = [0, 1, 2, 3, 4]  # 0=Monday, 6=Sunday
    available_hours: TimeSlot = TimeSlot(start_time="08:00", end_time="22:00")
    slot_duration_minutes: int = Field(default=60, ge=15, le=480)
    max_booking_hours: int = Field(default=4, ge=1, le=24)
    requires_approval: bool = False
    status: ResourceStatus = ResourceStatus.AVAILABLE


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    building: Optional[str] = None
    floor: Optional[int] = None
    capacity: Optional[int] = None
    amenities: Optional[List[str]] = None
    available_days: Optional[List[int]] = None
    available_hours: Optional[TimeSlot] = None
    slot_duration_minutes: Optional[int] = None
    max_booking_hours: Optional[int] = None
    requires_approval: Optional[bool] = None
    status: Optional[ResourceStatus] = None


# Response Schemas
class ResourceResponse(BaseModel):
    id: str
    name: str
    resource_type: ResourceType
    description: Optional[str]
    location: str
    building: Optional[str]
    floor: Optional[int]
    capacity: int
    amenities: List[str]
    available_days: List[int]
    available_hours: TimeSlot
    slot_duration_minutes: int
    max_booking_hours: int
    requires_approval: bool
    status: ResourceStatus
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class ResourceListResponse(BaseModel):
    resources: List[ResourceResponse]
    total: int


class AvailableSlot(BaseModel):
    start_time: str
    end_time: str
    is_available: bool


class ResourceAvailability(BaseModel):
    resource_id: str
    resource_name: str
    date: str
    slots: List[AvailableSlot]


class MessageResponse(BaseModel):
    message: str
