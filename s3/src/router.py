from fastapi import APIRouter
from fastapi import Request, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse, StreamingResponse
from botocore.exceptions import ClientError
import uuid
from src.settings import settings
from src.s3 import s3
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix='', tags=['main'])


@router.post("/upload")
async def upload(request: Request, file_name: str = None, domain: str = "main", file: UploadFile = File(...)):
    try:
        file_content = await file.read()
        if domain == "main":
            bucket = settings.S3_BUCKET_NAME
        if not file_name:
            file_name = file.filename
        key = f"{uuid.uuid4()}_{file_name}"

        content_type = file.content_type
        s3.put_object(Bucket=bucket, Key=key, Body=file_content, StorageClass='STANDARD', ContentType=content_type)
        link = f"{request.base_url}get/{domain}/{key}"

        return JSONResponse(content={"link": link})

    except ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to upload file to S3: {e}")


@router.get("/get/{domain}/{key}")
async def get(domain: str, key: str):
    try:
        if domain == 'main':
            bucket = settings.S3_BUCKET_NAME
        response = s3.get_object(Bucket=bucket, Key=key)
        file_stream = response["Body"].iter_chunks(chunk_size=8192)

        headers = {
            "Content-Disposition": f"attachment; filename={key.split('_', 1)[-1]}",
            "Content-Type": "application/octet-stream",
        }
        return StreamingResponse(file_stream, headers=headers)
    except ClientError as e:
        raise HTTPException(
            status_code=404, detail=f"Failed to get photo from S3: {e}")
