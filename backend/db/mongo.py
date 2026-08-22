import logging
import os
from typing import Optional, Dict, Any, List
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from backend.core.config import settings

logger = logging.getLogger(__name__)

async_client: Optional[AsyncIOMotorClient] = None
async_db: Optional[AsyncIOMotorDatabase] = None
sync_client: Optional[pymongo.MongoClient] = None
sync_db: Optional[pymongo.database.Database] = None
_mongo_available: bool = False

async def init_mongo() -> bool:
    """
    Initializes the async Motor and sync PyMongo MongoDB clients.
    Tests the connection with a ping; if MongoDB is unavailable, logs a warning
    and allows the application to proceed gracefully in fallback mode.
    """
    global async_client, async_db, sync_client, sync_db, _mongo_available
    if "PYTEST_CURRENT_TEST" in os.environ or os.getenv("TESTING") == "True":
        logger.info("Skipping MongoDB connection check during tests.")
        _mongo_available = False
        return False

    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGO_URI}...")
        async_client = AsyncIOMotorClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=2000
        )
        # Verify connection
        await async_client.admin.command('ping')
        async_db = async_client[settings.MONGO_DB_NAME]

        # Init sync client for synchronous service calls
        sync_client = pymongo.MongoClient(
            settings.MONGO_URI,
            serverSelectionTimeoutMS=2000
        )
        sync_db = sync_client[settings.MONGO_DB_NAME]

        _mongo_available = True
        logger.info(f"MongoDB connected successfully to database: '{settings.MONGO_DB_NAME}'")

        # Create indexes
        await async_db.document_contents.create_index("document_id", unique=True)
        await async_db.analysis_reports.create_index("analysis_id", unique=True)
        await async_db.chat_sessions.create_index("session_id", unique=True)
        return True
    except Exception as err:
        logger.warning(
            f"MongoDB connection failed ({err}). "
            "Proceeding in relational fallback mode. System will store data in PostgreSQL/SQLite."
        )
        _mongo_available = False
        return False

async def close_mongo():
    """Closes the MongoDB client connections."""
    global async_client, sync_client, _mongo_available
    if async_client is not None:
        async_client.close()
    if sync_client is not None:
        sync_client.close()
    _mongo_available = False
    logger.info("MongoDB connection closed.")

def is_mongo_available() -> bool:
    return _mongo_available

def get_mongo_db() -> Optional[AsyncIOMotorDatabase]:
    if _mongo_available:
        return async_db
    return None

def get_sync_mongo_db() -> Optional[pymongo.database.Database]:
    if _mongo_available:
        return sync_db
    return None

# Synchronous CRUD helpers (for synchronous service calls)
def save_document_content_sync(document_id: str, project_id: str, raw_text: str, metadata: Dict[str, Any] = None) -> bool:
    s_db = get_sync_mongo_db()
    if s_db is not None:
        try:
            doc_data = {
                "document_id": str(document_id),
                "project_id": str(project_id),
                "raw_text": raw_text,
                "metadata": metadata or {},
            }
            s_db.document_contents.update_one(
                {"document_id": str(document_id)},
                {"$set": doc_data},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save document content in MongoDB: {e}")
    return False

def get_document_content_sync(document_id: str) -> Optional[Dict[str, Any]]:
    s_db = get_sync_mongo_db()
    if s_db is not None:
        try:
            return s_db.document_contents.find_one({"document_id": str(document_id)}, {"_id": 0})
        except Exception as e:
            logger.error(f"Failed to fetch document content from MongoDB: {e}")
    return None

def save_analysis_report_sync(analysis_id: str, document_id: str, framework: str, findings: List[Dict[str, Any]], scores: Dict[str, Any] = None) -> bool:
    s_db = get_sync_mongo_db()
    if s_db is not None:
        try:
            report_data = {
                "analysis_id": str(analysis_id),
                "document_id": str(document_id),
                "framework": framework,
                "findings": findings,
                "scores": scores or {},
            }
            s_db.analysis_reports.update_one(
                {"analysis_id": str(analysis_id)},
                {"$set": report_data},
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save analysis report in MongoDB: {e}")
    return False

def get_analysis_report_sync(analysis_id: str) -> Optional[Dict[str, Any]]:
    s_db = get_sync_mongo_db()
    if s_db is not None:
        try:
            return s_db.analysis_reports.find_one({"analysis_id": str(analysis_id)}, {"_id": 0})
        except Exception as e:
            logger.error(f"Failed to fetch analysis report from MongoDB: {e}")
    return None

def save_chat_message_sync(session_id: str, project_id: str, role: str, message: str) -> bool:
    s_db = get_sync_mongo_db()
    if s_db is not None:
        try:
            msg_obj = {
                "role": role,
                "message": message,
            }
            s_db.chat_sessions.update_one(
                {"session_id": str(session_id)},
                {
                    "$set": {"project_id": str(project_id)},
                    "$push": {"messages": msg_obj}
                },
                upsert=True
            )
            return True
        except Exception as e:
            logger.error(f"Failed to save chat message in MongoDB: {e}")
    return False

