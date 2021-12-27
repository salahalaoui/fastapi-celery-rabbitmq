import os
from .auth import get_current_user
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Body, status
from fastapi.responses import JSONResponse
from ..schema import User, TaskResult, Task
from ..models import ModelUser
from uuid import uuid4 as uuid
from .auth import create_jwt_token

from celery import current_app as current_celery_app
from app.celery_app.tasks import create_task
from app.celery_app.celery_utils import get_task_info
from typing import Optional

from ..config import settings
router = APIRouter(
    prefix="/analysis",
    tags=["analysis"],
    responses={404: {"description": "Not found"}},
)

TASKS = {
    'create_task': 'create_task'
}

def check_file_format(file: UploadFile= File(...)):

    type_is_valid = settings.ACCEPTED_FILE_TYPES.get(file.content_type)

    if not type_is_valid:
        raise HTTPException(status_code=400, detail=f"file format {file.content_type} not accepted")

    return file

@router.post("/", response_model=Task, status_code=status.HTTP_202_ACCEPTED)
async def postTask(file: UploadFile = Depends(check_file_format), current_user: ModelUser = Depends(get_current_user)):
    """
    receives a file, and sends a positive response to the consumer as soon as possible. After the response is sent, the system perform the text
    analysis.
    """
    id = str(uuid())

    # https://stackoverflow.com/questions/63580229/how-to-save-uploadfile-in-fastapi
    # https://github.com/encode/starlette/issues/446
    file_location_full_path = os.path.join(
        settings.UPLOADS_DEFAULT_DEST,
        f'{id}_{file.filename}'
    )

    with open(file_location_full_path, "wb+") as file_object:
        file_object.write(file.file.read())

    task_id = create_task.apply_async(kwargs = {
            "file_location": file_location_full_path,
            "original_filename": file.filename,
            "mime_type": file.content_type
        },
        task_id=id
    )

    return Task(task_id=str(task_id))

async def check_task_exists(task_id: str):

    task = current_celery_app.backend.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task ID not found.")

    return task_id

@router.get("/{task_id}")
async def getTaskResults(task_id: str = Depends(check_task_exists), current_user: ModelUser = Depends(get_current_user)):

    return TaskResult(
        **get_task_info(task_id)
    )

