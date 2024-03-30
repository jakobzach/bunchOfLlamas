import os
from fastapi import UploadFile
from typing import List
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("LLAMA_CLOUD_API_KEY")


from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

parser = LlamaParse(
    api_key=api_key,
    result_type="markdown"  # "markdown" and "text" are available
)

async def read_file():
    file_extractor = {".pdf": parser}
    reader = SimpleDirectoryReader("/Users/jakobzacherl/Library/Mobile Documents/com~apple~CloudDocs/bunch/bunchOfLlamas/testfiles", file_extractor=file_extractor)
    documents = reader.load_data(show_progress=True, num_workers=1)
    return documents

async def save_uploaded_files(upload_files: List[UploadFile]) -> List[str]:
    save_paths = []
    for upload_file in upload_files:
        file_location = f"uploaded_files/{upload_file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb+") as file_object:
            file_object.write(await upload_file.read())
        save_paths.append(file_location)
    return save_paths