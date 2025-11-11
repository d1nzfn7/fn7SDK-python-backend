"""Pydantic models for request/response validation."""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# Sync Function Models
class UserProfileRequest(BaseModel):
    """Request model for user profile sync endpoint."""
    user_id: str = Field(..., description="User ID to fetch profile for")


# Async Function Models
class CreateTaskRequest(BaseModel):
    """Request model for async task creation."""
    task_id: str = Field(..., description="Unique task ID")
    title: str = Field(..., description="Task title")
    description: Optional[str] = Field(None, description="Task description")


class CreateTaskResponse(BaseModel):
    """Response model for async task creation."""
    success: bool = Field(..., description="Whether task creation was successful")
    task_id: str = Field(..., description="Created task ID")
    message: str = Field(..., description="Status message")


# Stream Function Models
class TaskStreamResponse(BaseModel):
    """Response model for task stream."""
    data: Dict[str, Any] = Field(..., description="Task data")
    timestamp: str = Field(..., description="Timestamp of the update")


# Long Running Function Models
class ProcessDocumentsRequest(BaseModel):
    """Request model for long-running document processing."""
    document_ids: List[str] = Field(..., description="List of document IDs to process")
    operation: str = Field(..., description="Operation to perform on documents")


class ProcessDocumentsResponse(BaseModel):
    """Response model for long-running document processing."""
    job_id: str = Field(..., description="Job ID for tracking progress")
    message: str = Field(..., description="Status message")


class JobStatusResponse(BaseModel):
    """Response model for job status check."""
    job_id: str = Field(..., description="Job ID")
    status: str = Field(..., description="Job status: pending, processing, completed, failed")
    progress: int = Field(..., ge=0, le=100, description="Progress percentage (0-100)")
    message: Optional[str] = Field(None, description="Status message")
    result: Optional[Dict[str, Any]] = Field(None, description="Job result if completed")


# Error Response Models
class ErrorResponse(BaseModel):
    """Error response model."""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Error details")

