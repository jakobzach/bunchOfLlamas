import os
from fastapi import UploadFile
from typing import List
import logging

logging.basicConfig(level=logging.INFO)    

async def save_uploaded_files(upload_files: List[UploadFile]) -> List[str]:
    save_paths = []
    for upload_file in upload_files:
        file_location = f"app/uploaded_files/{upload_file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(await upload_file.read())
        save_paths.append(file_location)
    return save_paths

async def save_uploaded_file(upload_file: UploadFile) -> str:
    file_location = f"app/uploaded_files/{upload_file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb+") as file_object:
        file_object.write(await upload_file.read())
        print("Successfully saved file at: " + file_location)
    return file_location