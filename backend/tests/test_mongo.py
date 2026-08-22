import pytest
import uuid
from backend.db import mongo

def test_mongo_graceful_fallback():
    """Verify that mongo helper functions gracefully handle offline MongoDB without raising unhandled exceptions."""
    assert isinstance(mongo.is_mongo_available(), bool)
    
    # Verify sync helpers do not raise exceptions when MongoDB is unavailable
    res_doc = mongo.save_document_content_sync(
        document_id=str(uuid.uuid4()),
        project_id=str(uuid.uuid4()),
        raw_text="Sample policy text",
        metadata={"test": True}
    )
    assert isinstance(res_doc, bool)

    res_report = mongo.save_analysis_report_sync(
        analysis_id=str(uuid.uuid4()),
        document_id=str(uuid.uuid4()),
        framework="GDPR",
        findings=[{"rule": "GDPR-1", "severity": "High"}],
        scores={"overall_score": 85.0}
    )
    assert isinstance(res_report, bool)

    res_chat = mongo.save_chat_message_sync(
        session_id=str(uuid.uuid4()),
        project_id=str(uuid.uuid4()),
        role="user",
        message="Hello assistant"
    )
    assert isinstance(res_chat, bool)
