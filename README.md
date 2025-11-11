# FN7 Backend Server

Python backend server using the **FN7 SDK for Python** package. This server provides test endpoints for Firebase operations with security rules enforcement.

## Features

- **FastAPI** web framework with async support
- **Firebase CRUD operations**: Get, Create, Update, Delete, Search
- **Firebase Storage operations**: Upload files, Get file URL, Get file blob
- JWT token authentication
- Comprehensive error handling and logging
- Health check endpoint

## Installation

### Prerequisites

- Python 3.8+
- Firebase service account credentials

### Setup

1. **Clone or navigate to the project directory**

2. **Install dependencies**:

```bash
pip install --index-url http://localhost:8083/simple fn7-sdk
pip install -r requirements.txt
```

3. **Configure environment variables**:

Copy `.env.example` to `.env` and fill in the required values:

```bash
cp .env.example .env
```

Edit `.env` with your Firebase credentials:

```env
# Option 1: Path to Firebase service account JSON file
FIREBASE_SERVICE_ACCOUNT_PATH=/path/to/service-account.json

# Option 2: OR use JSON string (alternative to PATH)
# FIREBASE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}

# Optional: Firebase Storage bucket
FIREBASE_STORAGE_BUCKET=your-storage-bucket.appspot.com

# Server port (default: 8000)
PORT=8000

# Log level (default: INFO)
LOG_LEVEL=INFO
```

## Running the Server

### Development Mode

```bash
uvicorn app.main:app --reload --port 8000
```

Or using Python directly:

```bash
python -m app.main
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

The server will be available at `http://localhost:8000`

## API Endpoints

### Health Check

```bash
curl http://localhost:8000/health
```

Returns server health status.

### Firebase CRUD Operations

#### Get Data

```bash
curl -X POST http://localhost:8000/api/test/get \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type": "Users",
    "doc_id": "user123"
  }'
```

#### Create Data

```bash
curl -X POST http://localhost:8000/api/test/create \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type": "Chats",
    "doc_id": "chat456",
    "data": {"message": "Hello", "user": "user123"}
  }'
```

#### Update Data

```bash
curl -X POST http://localhost:8000/api/test/update \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type": "Chats",
    "doc_id": "chat456",
    "data": {"message": "Updated message"}
  }'
```

#### Delete Data

```bash
curl -X POST http://localhost:8000/api/test/delete \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type": "Chats",
    "doc_id": "chat456"
  }'
```

#### Search Data

```bash
curl -X POST http://localhost:8000/api/test/search \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "doc_type": "Chats",
    "query_constraints": {},
    "limit": 10,
    "order_by": null
  }'
```

### Firebase Storage Operations

#### Upload Files

**Single file:**
```bash
curl -X POST http://localhost:8000/api/test/storage/upload \
  -H "Authorization: your-jwt-token-here" \
  -F "files=@/path/to/your/file.pdf" \
  -F "folder=uploads" \
  -F "app_name=myapp"
```

**Multiple files:**
```bash
curl -X POST http://localhost:8000/api/test/storage/upload \
  -H "Authorization: your-jwt-token-here" \
  -F "files=@/path/to/file1.pdf" \
  -F "files=@/path/to/file2.jpg" \
  -F "folder=uploads" \
  -F "app_name=myapp"
```

**Without app_name (optional):**
```bash
curl -X POST http://localhost:8000/api/test/storage/upload \
  -H "Authorization: your-jwt-token-here" \
  -F "files=@/path/to/your/file.pdf" \
  -F "folder=uploads"
```

#### Get File URL

```bash
curl -X POST http://localhost:8000/api/test/storage/get-url \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_name": "uploads",
    "file_name": "document.pdf",
    "app_name": "myapp"
  }'
```

**Without app_name:**
```bash
curl -X POST http://localhost:8000/api/test/storage/get-url \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_name": "uploads",
    "file_name": "document.pdf"
  }'
```

#### Get File Blob (Download)

```bash
curl -X POST http://localhost:8000/api/test/storage/get-blob \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_name": "uploads",
    "file_name": "document.pdf",
    "app_name": "myapp"
  }' \
  --output downloaded-file.pdf
```

**Without app_name:**
```bash
curl -X POST http://localhost:8000/api/test/storage/get-blob \
  -H "Authorization: your-jwt-token-here" \
  -H "Content-Type: application/json" \
  -d '{
    "folder_name": "uploads",
    "file_name": "document.pdf"
  }' \
  --output downloaded-file.pdf
```

## Project Structure

```
backend-server/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app initialization
│   ├── config.py               # Configuration and environment variables
│   ├── firebase_init.py        # Firebase Admin SDK initialization
│   ├── sdk_manager.py          # FN7 SDK singleton manager
│   ├── routes/
│   │   ├── __init__.py
│   │   └── test.py             # Test endpoints for FN7 SDK
│   ├── utils/
│   │   ├── __init__.py
│   │   └── auth.py             # JWT token extraction utilities
│   └── models/
│       ├── __init__.py
│       └── schemas.py          # Pydantic models for request/response
├── requirements.txt
├── .env.example
├── README.md
└── .gitignore
```

## Authentication

All endpoints require a JWT token in the `Authorization` header:

- Format: `<token>` (token sent directly, no Bearer prefix)
- The token is extracted and passed to all FN7 SDK method calls
- Invalid or missing tokens will return a 401 Unauthorized response

## Error Handling

The server includes comprehensive error handling:

- **401 Unauthorized**: Missing or invalid JWT token
- **404 Not Found**: Resource not found (user, job, etc.)
- **500 Internal Server Error**: Server-side errors

Error responses follow this format:

```json
{
  "error": "Error message",
  "detail": "Detailed error information"
}
```

## Logging

The server uses Python's `logging` module with configurable log levels:

- Set `LOG_LEVEL` in `.env` (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Logs include timestamps, log levels, and detailed error information
- All requests, errors, and important operations are logged

## Development

### Running Tests

```bash
# Add your test commands here
pytest
```

### Code Quality

```bash
# Format code
black app/

# Lint code
flake8 app/
```

## Security Notes

- The SDK implements all Firebase security rules in code
- All operations are validated before execution
- JWT tokens are required for all operations
- Never commit `.env` files or service account credentials to version control

## Troubleshooting

### Firebase Initialization Errors

- Ensure `FIREBASE_SERVICE_ACCOUNT_PATH` or `FIREBASE_SERVICE_ACCOUNT_JSON` is set correctly
- Verify the service account JSON file exists and is valid
- Check that the service account has the necessary Firebase permissions

### JWT Token Errors

- Ensure the JWT token is valid and not expired
- Verify the token includes required claims (user_id, org_hkey, application_id, etc.)
- Check that the token is properly formatted in the Authorization header

### Port Already in Use

- Change the `PORT` in `.env` to a different port
- Or stop the process using the current port

## License

[Add your license information here]

## Support

For issues related to the FN7 SDK, refer to the SDK documentation.
For server-specific issues, check the logs or open an issue in the repository.

