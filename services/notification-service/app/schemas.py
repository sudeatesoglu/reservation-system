from pydantic import BaseModel
from typing import Optional, Dict, Any


class NotificationEvent(BaseModel):
    """Notification event received from message queue"""
    event_type: str
    user_id: int
    username: str
    email: Optional[str] = None
    reservation_id: str
    resource_name: str
    date: str
    start_time: str
    end_time: str
    additional_data: Optional[Dict[str, Any]] = None


class EmailMessage(BaseModel):
    """Email message structure"""
    to_email: str
    subject: str
    body_html: str
    body_text: str


class NotificationLog(BaseModel):
    """Notification log entry"""
    event_type: str
    user_id: int
    status: str  # sent, failed, skipped
    message: Optional[str] = None
