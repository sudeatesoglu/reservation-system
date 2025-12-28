from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional, List
from app.schemas import (
    ResourceCreate, ResourceUpdate, ResourceResponse, 
    ResourceListResponse, MessageResponse, ResourceType, ResourceStatus
)
from app.services import ResourceService
from app.auth import get_current_user, get_current_admin_user, TokenData

router = APIRouter()


# ==================== Protected Routes (Require Authentication) ====================

@router.get("/resources", response_model=ResourceListResponse)
async def get_resources(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    resource_type: Optional[ResourceType] = None,
    status: Optional[ResourceStatus] = None,
    building: Optional[str] = None
):
    """Get list of resources with optional filtering - Public endpoint for browsing"""
    type_value = resource_type.value if resource_type else None
    status_value = status.value if status else None
    
    resources = await ResourceService.get_resources(
        skip=skip, limit=limit, 
        resource_type=type_value, 
        status=status_value,
        building=building
    )
    total = await ResourceService.get_resources_count(
        resource_type=type_value,
        status=status_value,
        building=building
    )
    return ResourceListResponse(resources=resources, total=total)


@router.get("/resources/available", response_model=List[ResourceResponse])
async def get_available_resources(
    resource_type: Optional[ResourceType] = None
):
    """Get all available resources - Public endpoint for browsing"""
    type_value = resource_type.value if resource_type else None
    return await ResourceService.get_available_resources(resource_type=type_value)


@router.get("/resources/search", response_model=ResourceListResponse)
async def search_resources(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100)
):
    """Search resources by name, description, or location - Public endpoint"""
    resources = await ResourceService.search_resources(q, skip=skip, limit=limit)
    return ResourceListResponse(resources=resources, total=len(resources))


@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str
):
    """Get resource by ID - Public endpoint"""
    resource = await ResourceService.get_resource_by_id(resource_id)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return resource


# ==================== Admin Routes ====================

@router.post("/resources", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    resource_data: ResourceCreate,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Create a new resource (admin only)"""
    resource = await ResourceService.create_resource(resource_data)
    return resource


@router.put("/resources/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: str,
    resource_data: ResourceUpdate,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Update a resource (admin only)"""
    resource = await ResourceService.update_resource(resource_id, resource_data)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return resource


@router.delete("/resources/{resource_id}", response_model=MessageResponse)
async def delete_resource(
    resource_id: str,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Delete a resource (admin only)"""
    deleted = await ResourceService.delete_resource(resource_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return MessageResponse(message="Resource deleted successfully")


@router.patch("/resources/{resource_id}/status", response_model=ResourceResponse)
async def update_resource_status(
    resource_id: str,
    new_status: ResourceStatus,
    current_user: TokenData = Depends(get_current_admin_user)
):
    """Update resource status (admin only)"""
    update_data = ResourceUpdate(status=new_status)
    resource = await ResourceService.update_resource(resource_id, update_data)
    if not resource:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Resource not found"
        )
    return resource


# ==================== Resource Types Endpoint ====================

@router.get("/resource-types", response_model=List[dict])
async def get_resource_types():
    """Get all available resource types"""
    return [
        {"value": t.value, "label": t.value.replace("_", " ").title()}
        for t in ResourceType
    ]
