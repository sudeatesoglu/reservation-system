from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Optional
from app.schemas import (
    ReservationCreate, ReservationUpdate, ReservationResponse,
    ReservationListResponse, ReservationStatus, CancelReservation,
    MessageResponse, ResourceAvailabilityResponse, TimeSlotAvailability
)
from app.services import ReservationService
from app.auth import get_current_user, get_current_admin_user, TokenData

router = APIRouter()
security = HTTPBearer()


# ==================== User Reservation Routes ====================

@router.post("/reservations", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation_data: ReservationCreate,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    current_user: TokenData = Depends(get_current_user)
):
    """Create a new reservation"""
    # Check availability
    is_available = await ReservationService.check_availability(
        reservation_data.resource_id,
        reservation_data.date,
        reservation_data.start_time,
        reservation_data.end_time
    )
    
    if not is_available:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Time slot is not available"
        )
    
    reservation = await ReservationService.create_reservation(
        reservation_data,
        user_id=current_user.user_id,
        username=current_user.username,
        token=credentials.credentials
    )
    return reservation


@router.get("/reservations/my", response_model=ReservationListResponse)
async def get_my_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[ReservationStatus] = None,
    upcoming_only: bool = False,
    current_user: TokenData = Depends(get_current_user)
):
    """Get current user's reservations"""
    status_value = status.value if status else None
    reservations = await ReservationService.get_user_reservations(
        user_id=current_user.user_id,
        skip=skip,
        limit=limit,
        status=status_value,
        upcoming_only=upcoming_only
    )
    total = await ReservationService.get_user_reservations_count(
        user_id=current_user.user_id,
        status=status_value
    )
    return ReservationListResponse(reservations=reservations, total=total)


@router.get("/reservations/{reservation_id}", response_model=ReservationResponse)
async def get_reservation(
    reservation_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get reservation by ID"""
    reservation = await ReservationService.get_reservation_by_id(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    # Users can only view their own reservations unless admin
    if reservation["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this reservation"
        )
    
    return reservation


@router.put("/reservations/{reservation_id}", response_model=ReservationResponse)
async def update_reservation(
    reservation_id: str,
    update_data: ReservationUpdate,
    current_user: TokenData = Depends(get_current_user)
):
    """Update a reservation"""
    reservation = await ReservationService.get_reservation_by_id(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    # Users can only update their own reservations
    if reservation["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this reservation"
        )
    
    # Cannot update cancelled or completed reservations
    if reservation["status"] in ["cancelled", "completed"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot update {reservation['status']} reservation"
        )
    
    # If changing time, check availability
    if update_data.date or update_data.start_time or update_data.end_time:
        date = update_data.date or reservation["date"]
        start = update_data.start_time or reservation["start_time"]
        end = update_data.end_time or reservation["end_time"]
        
        is_available = await ReservationService.check_availability(
            reservation["resource_id"], date, start, end,
            exclude_reservation_id=reservation_id
        )
        
        if not is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="New time slot is not available"
            )
    
    updated = await ReservationService.update_reservation(reservation_id, update_data)
    return updated


@router.post("/reservations/{reservation_id}/cancel", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: str,
    cancel_data: CancelReservation = None,
    current_user: TokenData = Depends(get_current_user)
):
    """Cancel a reservation"""
    reservation = await ReservationService.get_reservation_by_id(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    
    # Users can only cancel their own reservations
    if reservation["user_id"] != current_user.user_id and current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to cancel this reservation"
        )
    
    if reservation["status"] == "cancelled":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reservation is already cancelled"
        )
    
    reason = cancel_data.reason if cancel_data else None
    cancelled = await ReservationService.cancel_reservation(reservation_id, reason)
    return cancelled


# ==================== Availability Routes ====================

@router.get("/availability/{resource_id}", response_model=ResourceAvailabilityResponse)
async def get_resource_availability(
    resource_id: str,
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    current_user: TokenData = Depends(get_current_user)
):
    """Get availability slots for a resource on a specific date"""
    # Get existing reservations for this resource on this date
    reservations = await ReservationService.get_resource_reservations(
        resource_id=resource_id,
        date=date
    )
    
    # Generate time slots (example: 08:00 to 22:00, 1-hour slots)
    slots = []
    for hour in range(8, 22):
        start = f"{hour:02d}:00"
        end = f"{hour+1:02d}:00"
        
        # Check if slot is booked
        is_booked = any(
            r["status"] in ["pending", "confirmed"] and
            r["start_time"] <= start and r["end_time"] > start
            for r in reservations
        )
        
        slots.append(TimeSlotAvailability(
            start_time=start,
            end_time=end,
            is_available=not is_booked
        ))
    
    return ResourceAvailabilityResponse(
        resource_id=resource_id,
        date=date,
        slots=slots
    )


# ==================== Admin Routes ====================

@router.get("/reservations", response_model=ReservationListResponse)
async def get_all_reservations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    status: Optional[ReservationStatus] = None,
    date: Optional[str] = None,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Get all reservations (admin only)"""
    status_value = status.value if status else None
    reservations = await ReservationService.get_all_reservations(
        skip=skip, limit=limit, status=status_value, date=date
    )
    total = await ReservationService.get_all_reservations_count(
        status=status_value, date=date
    )
    return ReservationListResponse(reservations=reservations, total=total)


@router.get("/reservations/resource/{resource_id}", response_model=ReservationListResponse)
async def get_resource_reservations(
    resource_id: str,
    date: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: TokenData = Depends(get_current_user)
):
    """Get reservations for a specific resource"""
    reservations = await ReservationService.get_resource_reservations(
        resource_id=resource_id,
        date=date,
        skip=skip,
        limit=limit
    )
    return ReservationListResponse(reservations=reservations, total=len(reservations))


@router.post("/reservations/{reservation_id}/complete", response_model=ReservationResponse)
async def complete_reservation(
    reservation_id: str,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Mark reservation as completed (admin only)"""
    reservation = await ReservationService.complete_reservation(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    return reservation


@router.post("/reservations/{reservation_id}/no-show", response_model=ReservationResponse)
async def mark_no_show(
    reservation_id: str,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Mark reservation as no-show (admin only)"""
    reservation = await ReservationService.mark_no_show(reservation_id)
    if not reservation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reservation not found"
        )
    return reservation
