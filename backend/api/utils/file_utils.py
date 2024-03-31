import os
from fastapi import UploadFile
from typing import List
from dotenv import load_dotenv
import logging
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader


logging.basicConfig(level=logging.INFO)
load_dotenv()

api_key = os.getenv("LLAMA_CLOUD_API_KEY")

parser = LlamaParse(
    api_key=api_key,
    result_type="markdown"  # "markdown" and "text" are available
)

async def read_file(file_location):
    file_extractor = {".pdf": parser}
    directory = os.path.dirname(os.path.abspath(file_location))
    logging.info(f"Reading file from directory: {directory}")
    reader = SimpleDirectoryReader(directory, file_extractor=file_extractor)
    document = await reader.aload_data(show_progress=True, num_workers=1)
    print(document)
    return document

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