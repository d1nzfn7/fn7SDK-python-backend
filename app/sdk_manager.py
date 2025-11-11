"""FN7 SDK singleton manager."""
import logging
from typing import Optional
from fn7_sdk import FN7SDK
from app.config import settings

logger = logging.getLogger(__name__)

# Global SDK instance
_sdk_instance: Optional[FN7SDK] = None


def get_sdk() -> FN7SDK:
    """Get or create the singleton FN7 SDK instance."""
    global _sdk_instance

    if _sdk_instance is None:
        logger.info("Initializing FN7 SDK instance")
        _sdk_instance = FN7SDK(storage_bucket_name=settings.FIREBASE_STORAGE_BUCKET)
        logger.info("FN7 SDK instance created successfully")

    return _sdk_instance

