#!/usr/bin/env python3
"""
Add sample resources to the database
"""
from pymongo import MongoClient
from datetime import datetime, UTC

# MongoDB connection (no authentication)
client = MongoClient("mongodb://localhost:27017/")
db = client["resourcedb"]  # Use the correct database name
resources_collection = db["resources"]

# Sample resources
sample_resources = [
    {
        "name": "Meeting Room A",
        "resource_type": "meeting_room",
        "description": "Large meeting room with projector and whiteboard",
        "location": "Main Building Floor 2, Room 201",
        "building": "Main Building",
        "floor": 2,
        "capacity": 20,
        "amenities": ["Projector", "Whiteboard", "Video Conference", "WiFi"],
        "available_days": [0, 1, 2, 3, 4],  # Monday to Friday
        "available_hours": {
            "start_time": "08:00",
            "end_time": "18:00"
        },
        "slot_duration_minutes": 60,
        "max_booking_hours": 4,
        "requires_approval": False,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Meeting Room B",
        "resource_type": "meeting_room",
        "description": "Small meeting room for team discussions",
        "location": "Main Building Floor 2, Room 202",
        "building": "Main Building",
        "floor": 2,
        "capacity": 8,
        "amenities": ["TV Screen", "Whiteboard", "WiFi"],
        "available_days": [0, 1, 2, 3, 4],
        "available_hours": {
            "start_time": "08:00",
            "end_time": "18:00"
        },
        "slot_duration_minutes": 60,
        "max_booking_hours": 3,
        "requires_approval": False,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Computer Lab 1",
        "resource_type": "computer_lab",
        "description": "Computer lab with 30 workstations",
        "location": "Engineering Building Floor 1, Room E101",
        "building": "Engineering Building",
        "floor": 1,
        "capacity": 30,
        "amenities": ["30 Computers", "Projector", "Air Conditioning", "WiFi"],
        "available_days": [0, 1, 2, 3, 4],
        "available_hours": {
            "start_time": "08:00",
            "end_time": "22:00"
        },
        "slot_duration_minutes": 120,
        "max_booking_hours": 4,
        "requires_approval": True,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Study Room 1",
        "resource_type": "study_room",
        "description": "Quiet study room for individual or small group study",
        "location": "Library Floor 2, Room L201",
        "building": "Library",
        "floor": 2,
        "capacity": 6,
        "amenities": ["Whiteboard", "Quiet Zone", "Power Outlets", "WiFi"],
        "available_days": [0, 1, 2, 3, 4, 5, 6],  # All week
        "available_hours": {
            "start_time": "07:00",
            "end_time": "23:00"
        },
        "slot_duration_minutes": 60,
        "max_booking_hours": 4,
        "requires_approval": False,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Study Room 2",
        "resource_type": "study_room",
        "description": "Group study room with large table",
        "location": "Library Floor 2, Room L202",
        "building": "Library",
        "floor": 2,
        "capacity": 10,
        "amenities": ["Large Table", "Whiteboard", "Power Outlets", "WiFi"],
        "available_days": [0, 1, 2, 3, 4, 5, 6],
        "available_hours": {
            "start_time": "07:00",
            "end_time": "23:00"
        },
        "slot_duration_minutes": 60,
        "max_booking_hours": 4,
        "requires_approval": False,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Office 101",
        "resource_type": "office",
        "description": "Private office space for consultations",
        "location": "Admin Building Floor 1, Room A101",
        "building": "Admin Building",
        "floor": 1,
        "capacity": 4,
        "amenities": ["Desk", "Computer", "Phone", "WiFi"],
        "available_days": [0, 1, 2, 3, 4],
        "available_hours": {
            "start_time": "09:00",
            "end_time": "17:00"
        },
        "slot_duration_minutes": 30,
        "max_booking_hours": 2,
        "requires_approval": True,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Library Desk 1",
        "resource_type": "library_desk",
        "description": "Individual study desk in quiet zone",
        "location": "Library Floor 1, Desk L-D1",
        "building": "Library",
        "floor": 1,
        "capacity": 1,
        "amenities": ["Desk Lamp", "Power Outlet", "WiFi"],
        "available_days": [0, 1, 2, 3, 4, 5, 6],
        "available_hours": {
            "start_time": "07:00",
            "end_time": "23:00"
        },
        "slot_duration_minutes": 120,
        "max_booking_hours": 8,
        "requires_approval": False,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    },
    {
        "name": "Library Desk 2",
        "resource_type": "library_desk",
        "description": "Individual study desk near windows",
        "location": "Library Floor 1, Desk L-D2",
        "building": "Library",
        "floor": 1,
        "capacity": 1,
        "amenities": ["Desk Lamp", "Power Outlet", "Natural Light", "WiFi"],
        "available_days": [0, 1, 2, 3, 4, 5, 6],
        "available_hours": {
            "start_time": "07:00",
            "end_time": "23:00"
        },
        "slot_duration_minutes": 120,
        "max_booking_hours": 8,
        "requires_approval": False,
        "status": "available",
        "created_at": datetime.now(UTC),
        "updated_at": datetime.now(UTC)
    }
]

# Clear existing resources
print("Clearing existing resources...")
resources_collection.delete_many({})

# Insert sample resources
print("Adding sample resources...")
result = resources_collection.insert_many(sample_resources)
print(f"Added {len(result.inserted_ids)} resources")

# Verify
count = resources_collection.count_documents({})
print(f"Total resources in database: {count}")

for resource in resources_collection.find():
    print(f"  - {resource['name']} ({resource['resource_type']}) - {resource['status']}")

print("\nDone!")
