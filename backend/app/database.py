"""
MongoDB Database Connection and Collections
R-PRIV-01: All candidate data stored securely
R-LOG-01: All operations logged for auditability
"""

from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING
from typing import Optional
import os

# MongoDB connection settings
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "vgp_platform"


class MongoDB:
    """MongoDB connection manager"""
    client: Optional[AsyncIOMotorClient] = None
    
    @classmethod
    async def connect_db(cls):
        """Initialize MongoDB connection"""
        cls.client = AsyncIOMotorClient(MONGODB_URL)
        db = cls.client[DATABASE_NAME]
        
        # Create indexes for efficient queries (R-PERF-01)
        # Use sparse index for email to allow multiple null values
        await db.candidates.create_index([("email", ASCENDING)], unique=True, sparse=True)
        await db.candidates.create_index([("id", ASCENDING)], unique=True)
        
        await db.employers.create_index([("id", ASCENDING)], unique=True)
        await db.employers.create_index([("name", ASCENDING)])
        
        await db.score_reports.create_index([("candidateId", ASCENDING)])
        await db.score_reports.create_index([("trackId", ASCENDING)])
        await db.score_reports.create_index([("overallScore", DESCENDING)])
        await db.score_reports.create_index([("percentile", DESCENDING)])
        
        await db.test_sessions.create_index([("sessionId", ASCENDING)], unique=True)
        await db.test_sessions.create_index([("candidateId", ASCENDING)])
        
        await db.jobs.create_index([("jobId", ASCENDING)], unique=True)
        await db.jobs.create_index([("employerId", ASCENDING)])
        
        await db.item_bank.create_index([("questionId", ASCENDING)], unique=True)
        await db.item_bank.create_index([("trackId", ASCENDING)])
        await db.item_bank.create_index([("difficulty", ASCENDING)])
        
        print(f"✅ Connected to MongoDB at {MONGODB_URL}")
    
    @classmethod
    async def close_db(cls):
        """Close MongoDB connection"""
        if cls.client:
            cls.client.close()
            print("✅ MongoDB connection closed")
    
    @classmethod
    def get_database(cls):
        """Get database instance"""
        if not cls.client:
            raise RuntimeError("Database not connected. Call connect_db() first.")
        return cls.client[DATABASE_NAME]


# Collection accessors
def get_candidates_collection():
    return MongoDB.get_database().candidates


def get_employers_collection():
    return MongoDB.get_database().employers


def get_score_reports_collection():
    return MongoDB.get_database().score_reports


def get_test_sessions_collection():
    return MongoDB.get_database().test_sessions


def get_jobs_collection():
    return MongoDB.get_database().jobs


def get_item_bank_collection():
    return MongoDB.get_database().item_bank


def get_trace_events_collection():
    return MongoDB.get_database().trace_events
