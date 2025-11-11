"""JWT token extraction utilities."""
import logging
from typing import Optional
from fastapi import Header, HTTPException, status

logger = logging.getLogger(__name__)


def extract_jwt_token(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract JWT token from Authorization header.

    The token is sent directly in the Authorization header without any prefix.

    Args:
        authorization: Authorization header value (token directly)

    Returns:
        JWT token string

    Raises:
        HTTPException: If token is missing or invalid
    """
    if not authorization:
        logger.warning("Authorization header missing")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is required"
        )

    token = authorization.strip()

    if not token:
        logger.warning("JWT token is empty")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="JWT token is required"
        )

    return token

