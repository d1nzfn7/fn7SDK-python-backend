"""Test endpoints for FN7 SDK."""
import logging
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from fastapi.responses import Response
from pydantic import BaseModel, Field
from app.utils.auth import extract_jwt_token
from app.sdk_manager import get_sdk

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/test", tags=["test"])


# Request/Response Models
class GetDataRequest(BaseModel):
    """Request model for getting data."""
    doc_type: str = Field(..., description="Document type/collection name")
    doc_id: str = Field(..., description="Document ID")


class CreateDataRequest(BaseModel):
    """Request model for creating data."""
    doc_type: str = Field(..., description="Document type/collection name")
    doc_id: str = Field(..., description="Document ID")
    data: Dict[str, Any] = Field(..., description="Data to create")


class UpdateDataRequest(BaseModel):
    """Request model for updating data."""
    doc_type: str = Field(..., description="Document type/collection name")
    doc_id: str = Field(..., description="Document ID")
    data: Dict[str, Any] = Field(..., description="Data to update")


class DeleteDataRequest(BaseModel):
    """Request model for deleting data."""
    doc_type: str = Field(..., description="Document type/collection name")
    doc_id: str = Field(..., description="Document ID")


class SearchDataRequest(BaseModel):
    """Request model for searching data."""
    doc_type: str = Field(..., description="Document type/collection name")
    query_constraints: Optional[Dict[str, Any]] = Field(default={}, description="Query constraints")
    limit: Optional[int] = Field(default=10, ge=1, le=100, description="Limit results")
    order_by: Optional[str] = Field(default=None, description="Order by field")


class GetStorageRequest(BaseModel):
    """Request model for getting file from storage."""
    folder_name: str = Field(..., description="Folder name in storage")
    file_name: str = Field(..., description="File name")
    app_name: Optional[str] = Field(default=None, description="Application name")


class GetBlobStorageRequest(BaseModel):
    """Request model for getting file blob from storage."""
    folder_name: str = Field(..., description="Folder name in storage")
    file_name: str = Field(..., description="File name")
    app_name: Optional[str] = Field(default=None, description="Application name")


@router.post("/get", summary="Get data from Firebase")
async def test_get_data(
    request: GetDataRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to get data from Firebase using FN7 SDK.

    Example:
    {
        "doc_type": "Users",
        "doc_id": "user123"
    }
    """
    try:
        logger.info(f"Getting data: {request.doc_type}/{request.doc_id}")
        sdk = get_sdk()
        data = sdk.get_firebase_data(request.doc_type, request.doc_id, jwt_token)

        if data is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Document not found: {request.doc_type}/{request.doc_id}"
            )

        return {
            "success": True,
            "doc_type": request.doc_type,
            "doc_id": request.doc_id,
            "data": data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get data: {str(e)}"
        )


@router.post("/create", summary="Create data in Firebase")
async def test_create_data(
    request: CreateDataRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to create data in Firebase using FN7 SDK.

    Example:
    {
        "doc_type": "Chats",
        "doc_id": "chat456",
        "data": {"message": "Hello", "user": "user123"}
    }
    """
    try:
        logger.info(f"Creating data: {request.doc_type}/{request.doc_id}")
        sdk = get_sdk()
        result = sdk.create_firebase_data(request.doc_type, request.doc_id, request.data, jwt_token)

        return {
            "success": True,
            "doc_type": request.doc_type,
            "doc_id": request.doc_id,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error creating data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create data: {str(e)}"
        )


@router.post("/update", summary="Update data in Firebase")
async def test_update_data(
    request: UpdateDataRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to update data in Firebase using FN7 SDK.

    Example:
    {
        "doc_type": "Chats",
        "doc_id": "chat456",
        "data": {"message": "Updated message"}
    }
    """
    try:
        logger.info(f"Updating data: {request.doc_type}/{request.doc_id}")
        sdk = get_sdk()
        result = sdk.update_firebase_data(request.doc_type, request.doc_id, request.data, jwt_token)

        return {
            "success": True,
            "doc_type": request.doc_type,
            "doc_id": request.doc_id,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error updating data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update data: {str(e)}"
        )


@router.post("/delete", summary="Delete data from Firebase")
async def test_delete_data(
    request: DeleteDataRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to delete data from Firebase using FN7 SDK.

    Example:
    {
        "doc_type": "Chats",
        "doc_id": "chat456"
    }
    """
    try:
        logger.info(f"Deleting data: {request.doc_type}/{request.doc_id}")
        sdk = get_sdk()
        sdk.delete_firebase_data(request.doc_type, request.doc_id, jwt_token)

        return {
            "success": True,
            "doc_type": request.doc_type,
            "doc_id": request.doc_id,
            "message": "Document deleted successfully"
        }
    except Exception as e:
        logger.error(f"Error deleting data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete data: {str(e)}"
        )


@router.post("/search", summary="Search data in Firebase")
async def test_search_data(
    request: SearchDataRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to search data in Firebase using FN7 SDK.

    Example:
    {
        "doc_type": "Chats",
        "query_constraints": {},
        "limit": 10,
        "order_by": null
    }
    """
    try:
        logger.info(f"Searching data: {request.doc_type}")
        sdk = get_sdk()
        results = sdk.search_firebase_data(
            query_constraints=request.query_constraints,
            limit=request.limit,
            order_by=request.order_by,
            jwt_token=jwt_token
        )

        return {
            "success": True,
            "doc_type": request.doc_type,
            "count": len(results) if results else 0,
            "results": results or []
        }
    except Exception as e:
        logger.error(f"Error searching data: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search data: {str(e)}"
        )


@router.post("/storage/upload", summary="Upload files to Firebase Storage")
async def test_upload_storage(
    files: List[UploadFile] = File(..., description="Files to upload"),
    folder: str = Form(..., description="Folder name in storage"),
    app_name: Optional[str] = Form(default=None, description="Application name"),
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to upload files to Firebase Storage using FN7 SDK.

    Uploads one or more files to the specified folder.
    """
    try:
        logger.info(f"Uploading {len(files)} file(s) to folder: {folder}")
        logger.info(f"App name: {app_name}")
        logger.info(f"JWT token: {jwt_token}")
        sdk = get_sdk()

        # Read file contents
        filenames = []
        file_contents = []

        for file in files:
            content = await file.read()
            filenames.append(file.filename)
            file_contents.append(content)
            logger.info(f"Prepared file: {file.filename} ({len(content)} bytes)")

        # Upload files
        result = sdk.upload_to_storage(
            filenames=filenames,
            files=file_contents,
            jwt_token=jwt_token,
            folder=folder,
            app_name=app_name
        )

        return {
            "success": True,
            "folder": folder,
            "app_name": app_name,
            "files_uploaded": filenames,
            "result": result
        }
    except Exception as e:
        logger.error(f"Error uploading files: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to upload files: {str(e)}"
        )


@router.post("/storage/get-url", summary="Get file URL from Firebase Storage")
async def test_get_storage_url(
    request: GetStorageRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to get file URL from Firebase Storage using FN7 SDK.

    Example:
    {
        "folder_name": "uploads",
        "file_name": "document.pdf",
        "app_name": "myapp"
    }
    """
    try:
        logger.info(f"Getting file URL: {request.folder_name}/{request.file_name}")
        sdk = get_sdk()
        url = sdk.get_from_storage(
            folder_name=request.folder_name,
            file_name=request.file_name,
            jwt_token=jwt_token,
            app_name=request.app_name
        )

        return {
            "success": True,
            "folder_name": request.folder_name,
            "file_name": request.file_name,
            "app_name": request.app_name,
            "url": url
        }
    except Exception as e:
        logger.error(f"Error getting file URL: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file URL: {str(e)}"
        )


@router.post("/storage/get-blob", summary="Get file blob from Firebase Storage")
async def test_get_storage_blob(
    request: GetBlobStorageRequest,
    jwt_token: str = Depends(extract_jwt_token),
):
    """
    Test endpoint to get file bytes/blob from Firebase Storage using FN7 SDK.

    Returns the file content as bytes.

    Example:
    {
        "folder_name": "uploads",
        "file_name": "document.pdf",
        "app_name": "myapp"
    }
    """
    try:
        logger.info(f"Getting file blob: {request.folder_name}/{request.file_name}")
        sdk = get_sdk()
        blob = sdk.get_blob_from_storage(
            folder_name=request.folder_name,
            file_name=request.file_name,
            jwt_token=jwt_token,
            app_name=request.app_name
        )

        # Determine content type (basic detection)
        content_type = "application/octet-stream"
        if request.file_name.endswith(('.jpg', '.jpeg')):
            content_type = "image/jpeg"
        elif request.file_name.endswith('.png'):
            content_type = "image/png"
        elif request.file_name.endswith('.pdf'):
            content_type = "application/pdf"
        elif request.file_name.endswith('.txt'):
            content_type = "text/plain"
        elif request.file_name.endswith('.json'):
            content_type = "application/json"

        return Response(
            content=blob,
            media_type=content_type,
            headers={
                "Content-Disposition": f'inline; filename="{request.file_name}"'
            }
        )
    except Exception as e:
        logger.error(f"Error getting file blob: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get file blob: {str(e)}"
        )

