from fastapi import APIRouter, File, UploadFile
from backend.api.utils.file_utils import save_uploaded_files, save_uploaded_file, read_file
from backend.api.data_models import models
from typing import List
from llama_index.core.program import LLMTextCompletionProgram
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

@router.post("/upload/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    save_paths = await save_uploaded_files(files)
    return {"file_paths": save_paths}

@router.post("/extract/")
async def extract_data_model(file: UploadFile = File(...)):
    file_location = await save_uploaded_file(file)
    document = await read_file(file_location)
    print(len(document))
    document_text = document[0].text

    prompt_template_str = """\
    Extract all relevant information from {file_text}. Return "NULL" if a property cannot be found.\
    """

    program = LLMTextCompletionProgram.from_defaults(
        output_cls = models.CapitalCall,
        prompt_template_str = prompt_template_str,
        verbose = False
    )

    result = program(file_text=document_text)
    print(result)

    return result