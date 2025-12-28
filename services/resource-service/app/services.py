from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from app.database import get_database
from app.schemas import ResourceCreate, ResourceUpdate, ResourceResponse


class ResourceService:
    """Service class for resource operations"""
    
    COLLECTION = "resources"
    
    @staticmethod
    def _serialize_resource(resource: dict) -> dict:
        """Convert MongoDB document to response format"""
        if resource:
            resource["id"] = str(resource.pop("_id"))
        return resource
    
    @staticmethod
    async def create_resource(resource_data: ResourceCreate) -> dict:
        """Create a new resource"""
        db = get_database()
        resource_dict = resource_data.model_dump()
        resource_dict["created_at"] = datetime.utcnow()
        resource_dict["updated_at"] = None
        
        result = await db[ResourceService.COLLECTION].insert_one(resource_dict)
        resource_dict["_id"] = result.inserted_id
        return ResourceService._serialize_resource(resource_dict)
    
    @staticmethod
    async def get_resource_by_id(resource_id: str) -> Optional[dict]:
        """Get resource by ID"""
        db = get_database()
        if not ObjectId.is_valid(resource_id):
            return None
        resource = await db[ResourceService.COLLECTION].find_one(
            {"_id": ObjectId(resource_id)}
        )
        return ResourceService._serialize_resource(resource) if resource else None
    
    @staticmethod
    async def get_resources(
        skip: int = 0,
        limit: int = 100,
        resource_type: Optional[str] = None,
        status: Optional[str] = None,
        building: Optional[str] = None
    ) -> List[dict]:
        """Get list of resources with filtering"""
        db = get_database()
        query = {}
        
        if resource_type:
            query["resource_type"] = resource_type
        if status:
            query["status"] = status
        if building:
            query["building"] = building
        
        cursor = db[ResourceService.COLLECTION].find(query).skip(skip).limit(limit)
        resources = await cursor.to_list(length=limit)
        return [ResourceService._serialize_resource(r) for r in resources]
    
    @staticmethod
    async def get_resources_count(
        resource_type: Optional[str] = None,
        status: Optional[str] = None,
        building: Optional[str] = None
    ) -> int:
        """Get total count of resources"""
        db = get_database()
        query = {}
        
        if resource_type:
            query["resource_type"] = resource_type
        if status:
            query["status"] = status
        if building:
            query["building"] = building
        
        return await db[ResourceService.COLLECTION].count_documents(query)
    
    @staticmethod
    async def update_resource(resource_id: str, update_data: ResourceUpdate) -> Optional[dict]:
        """Update a resource"""
        db = get_database()
        if not ObjectId.is_valid(resource_id):
            return None
        
        update_dict = {k: v for k, v in update_data.model_dump().items() if v is not None}
        if not update_dict:
            # Nothing to update, return existing
            return await ResourceService.get_resource_by_id(resource_id)
        
        update_dict["updated_at"] = datetime.utcnow()
        
        result = await db[ResourceService.COLLECTION].find_one_and_update(
            {"_id": ObjectId(resource_id)},
            {"$set": update_dict},
            return_document=True
        )
        return ResourceService._serialize_resource(result) if result else None
    
    @staticmethod
    async def delete_resource(resource_id: str) -> bool:
        """Delete a resource"""
        db = get_database()
        if not ObjectId.is_valid(resource_id):
            return False
        
        result = await db[ResourceService.COLLECTION].delete_one(
            {"_id": ObjectId(resource_id)}
        )
        return result.deleted_count > 0
    
    @staticmethod
    async def search_resources(
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """Search resources by name or description"""
        db = get_database()
        search_query = {
            "$or": [
                {"name": {"$regex": query, "$options": "i"}},
                {"description": {"$regex": query, "$options": "i"}},
                {"location": {"$regex": query, "$options": "i"}}
            ]
        }
        cursor = db[ResourceService.COLLECTION].find(search_query).skip(skip).limit(limit)
        resources = await cursor.to_list(length=limit)
        return [ResourceService._serialize_resource(r) for r in resources]
    
    @staticmethod
    async def get_available_resources(
        resource_type: Optional[str] = None
    ) -> List[dict]:
        """Get all available resources"""
        db = get_database()
        query = {"status": "available"}
        if resource_type:
            query["resource_type"] = resource_type
        
        cursor = db[ResourceService.COLLECTION].find(query)
        resources = await cursor.to_list(length=1000)
        return [ResourceService._serialize_resource(r) for r in resources]
