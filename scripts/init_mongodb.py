#!/usr/bin/env python3
"""
MongoDB Database Initialization Script
Initialize MongoDB databases and collections for resource and reservation services
"""

import pymongo
from pymongo import MongoClient
from datetime import datetime, UTC
import sys
import os

def init_mongodb():
    """Initialize MongoDB databases and collections"""

    # MongoDB connection
    mongo_host = os.getenv('MONGO_HOST', 'mongodb')
    mongo_port = int(os.getenv('MONGO_PORT', '27017'))

    try:
        # Connect to MongoDB
        client = MongoClient(f"mongodb://{mongo_host}:{mongo_port}/")
        print(f"Connected to MongoDB at {mongo_host}:{mongo_port}")

        # Initialize Resource Database
        resource_db = client['resourcedb']
        print("Initializing resourcedb...")

        # Create collections
        resources_collection = resource_db['resources']

        # Create indexes for resources
        resources_collection.create_index([('name', pymongo.TEXT)])
        resources_collection.create_index([('resource_type', pymongo.ASCENDING)])
        resources_collection.create_index([('location', pymongo.ASCENDING)])
        resources_collection.create_index([('status', pymongo.ASCENDING)])
        resources_collection.create_index([('building', pymongo.ASCENDING)])
        resources_collection.create_index([('capacity', pymongo.ASCENDING)])

        # Clear existing resources and add sample data
        resources_collection.drop()

        sample_resources = [
            {
                "name": "Meeting Room A",
                "resource_type": "meeting_room",
                "description": "Large meeting room with projector and whiteboards",
                "location": "Building A, Room 101",
                "building": "Building A",
                "floor": 1,
                "capacity": 12,
                "amenities": ["projector", "whiteboard", "wifi", "coffee_machine"],
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
                "location": "Building A, Room 102",
                "building": "Building A",
                "floor": 1,
                "capacity": 6,
                "amenities": ["whiteboard", "wifi"],
                "available_days": [0, 1, 2, 3, 4],
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
                "name": "Computer Lab 1",
                "resource_type": "computer_lab",
                "description": "Computer lab with 20 workstations",
                "location": "Building B, Room 201",
                "building": "Building B",
                "floor": 2,
                "capacity": 20,
                "amenities": ["computers", "printers", "wifi", "projector"],
                "available_days": [0, 1, 2, 3, 4],
                "available_hours": {
                    "start_time": "08:00",
                    "end_time": "22:00"
                },
                "slot_duration_minutes": 120,
                "max_booking_hours": 8,
                "requires_approval": False,
                "status": "available",
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC)
            },
            {
                "name": "Study Room 1",
                "resource_type": "study_room",
                "description": "Quiet study room for individual work",
                "location": "Library, Room 301",
                "building": "Library",
                "floor": 3,
                "capacity": 4,
                "amenities": ["wifi", "power_outlets", "whiteboard"],
                "available_days": [0, 1, 2, 3, 4, 5, 6],  # All days
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
                "description": "Group study room with discussion area",
                "location": "Library, Room 302",
                "building": "Library",
                "floor": 3,
                "capacity": 8,
                "amenities": ["wifi", "power_outlets", "projector", "whiteboard"],
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
                "description": "Private office for meetings or work",
                "location": "Building C, Room 101",
                "building": "Building C",
                "floor": 1,
                "capacity": 2,
                "amenities": ["desk", "chair", "wifi", "phone"],
                "available_days": [0, 1, 2, 3, 4],
                "available_hours": {
                    "start_time": "08:00",
                    "end_time": "18:00"
                },
                "slot_duration_minutes": 60,
                "max_booking_hours": 8,
                "requires_approval": True,
                "status": "available",
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC)
            },
            {
                "name": "Library Desk 1",
                "resource_type": "library_desk",
                "description": "Individual study desk in the library",
                "location": "Library, Main Area",
                "building": "Library",
                "floor": 1,
                "capacity": 1,
                "amenities": ["power_outlet", "lamp"],
                "available_days": [0, 1, 2, 3, 4, 5, 6],
                "available_hours": {
                    "start_time": "07:00",
                    "end_time": "23:00"
                },
                "slot_duration_minutes": 120,
                "max_booking_hours": 4,
                "requires_approval": False,
                "status": "available",
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC)
            },
            {
                "name": "Library Desk 2",
                "resource_type": "library_desk",
                "description": "Individual study desk in the library",
                "location": "Library, Main Area",
                "building": "Library",
                "floor": 1,
                "capacity": 1,
                "amenities": ["power_outlet", "lamp"],
                "available_days": [0, 1, 2, 3, 4, 5, 6],
                "available_hours": {
                    "start_time": "07:00",
                    "end_time": "23:00"
                },
                "slot_duration_minutes": 120,
                "max_booking_hours": 4,
                "requires_approval": False,
                "status": "available",
                "created_at": datetime.now(UTC),
                "updated_at": datetime.now(UTC)
            }
        ]

        # Insert sample resources
        result = resources_collection.insert_many(sample_resources)
        print(f"Inserted {len(result.inserted_ids)} resources into resourcedb")

        # Initialize Reservation Database
        reservation_db = client['reservationdb']
        print("Initializing reservationdb...")

        # Create collections
        reservations_collection = reservation_db['reservations']

        # Create indexes for reservations
        reservations_collection.create_index([('user_id', pymongo.ASCENDING)])
        reservations_collection.create_index([('resource_id', pymongo.ASCENDING)])
        reservations_collection.create_index([('date', pymongo.ASCENDING)])
        reservations_collection.create_index([('status', pymongo.ASCENDING)])
        reservations_collection.create_index([('created_at', pymongo.DESCENDING)])

        # Clear existing reservations (keep it empty for fresh start)
        reservations_collection.drop()

        print("MongoDB databases initialized successfully!")
        print("resourcedb: 8 sample resources added")
        print("reservationdb: ready for reservations")

        # Close connection
        client.close()

    except Exception as e:
        print(f"Error initializing MongoDB: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_mongodb()