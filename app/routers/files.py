from fastapi import APIRouter, File, UploadFile
from ..utils.file_utils import save_uploaded_files
from typing import List

router = APIRouter()

@router.post("/upload/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    save_paths = await save_uploaded_files(files)
    return {"file_paths": save_paths}
