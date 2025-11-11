"""Firebase Admin SDK initialization."""
import json
import logging
import os
import firebase_admin
from firebase_admin import credentials
from app.config import settings

logger = logging.getLogger(__name__)


def initialize_firebase() -> None:
    """Initialize Firebase Admin SDK with credentials from environment variables."""
    try:
        # Check if Firebase is already initialized
        if firebase_admin._apps:
            logger.info("Firebase Admin SDK already initialized")
            return

        cred = None
        service_account_path = None

        # Option 1: From file path
        if settings.FIREBASE_SERVICE_ACCOUNT_PATH:
            service_account_path = settings.FIREBASE_SERVICE_ACCOUNT_PATH
            # Convert to absolute path for GOOGLE_APPLICATION_CREDENTIALS
            if not os.path.isabs(service_account_path):
                service_account_path = os.path.abspath(service_account_path)

            logger.info(f"Initializing Firebase from file: {service_account_path}")
            cred = credentials.Certificate(service_account_path)

            # Set GOOGLE_APPLICATION_CREDENTIALS so gRPC calls use the service account
            # This ensures the FN7 SDK uses the correct credentials instead of falling back to ADC
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = service_account_path
            logger.info(f"Set GOOGLE_APPLICATION_CREDENTIALS to: {service_account_path}")

        # Option 2: From JSON string
        elif settings.FIREBASE_SERVICE_ACCOUNT_JSON:
            logger.info("Initializing Firebase from JSON string")
            service_account_dict = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_JSON)
            cred = credentials.Certificate(service_account_dict)

            # For JSON string, we can't set GOOGLE_APPLICATION_CREDENTIALS directly
            # The credentials object should be sufficient, but if issues persist,
            # consider writing to a temp file and setting the env var

        else:
            raise ValueError(
                "Firebase credentials not found. Set either FIREBASE_SERVICE_ACCOUNT_PATH "
                "or FIREBASE_SERVICE_ACCOUNT_JSON environment variable."
            )

        # Initialize Firebase Admin SDK
        firebase_admin.initialize_app(cred)
        logger.info("Firebase Admin SDK initialized successfully")

    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {str(e)}")
        raise

