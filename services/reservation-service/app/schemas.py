from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime, date
from enum import Enum


class ReservationStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"


# Request Schemas
class ReservationCreate(BaseModel):
    resource_id: str
    date: str  # Format: YYYY-MM-DD
    start_time: str  # Format: HH:MM
    end_time: str  # Format: HH:MM
    purpose: Optional[str] = None
    notes: Optional[str] = None


class ReservationUpdate(BaseModel):
    date: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    purpose: Optional[str] = None
    notes: Optional[str] = None


# Response Schemas
class ReservationResponse(BaseModel):
    id: str
    user_id: int
    username: str
    resource_id: str
    resource_name: Optional[str] = None
    date: str
    start_time: str
    end_time: str
    purpose: Optional[str]
    notes: Optional[str]
    status: ReservationStatus
    created_at: datetime
    updated_at: Optional[datetime]
    cancelled_at: Optional[datetime]
    cancellation_reason: Optional[str]
    
    class Config:
        from_attributes = True


class ReservationListResponse(BaseModel):
    reservations: List[ReservationResponse]
    total: int


class TimeSlotAvailability(BaseModel):
    start_time: str
    end_time: str
    is_available: bool


class ResourceAvailabilityResponse(BaseModel):
    resource_id: str
    date: str
    slots: List[TimeSlotAvailability]


class CancelReservation(BaseModel):
    reason: Optional[str] = None


class MessageResponse(BaseModel):
    message: str


# Notification Event Schema
class NotificationEvent(BaseModel):
    event_type: str  # reservation_created, reservation_cancelled, etc.
    user_id: int
    username: str
    email: Optional[str] = None
    reservation_id: str
    resource_name: str
    date: str
    start_time: str
    end_time: str
    additional_data: Optional[dict] = None
