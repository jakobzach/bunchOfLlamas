from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from backend.api.utils.upload_utils import save_uploaded_files, save_uploaded_file
from backend.api.utils.extract_utils import read_file,create_document_metadata,create_data_model
from backend.api.data_models.response_models import FileMetadata,Category, CapitalCall, ConvertibleLoanAgreement, ExtractResponse
from typing import List
from dotenv import load_dotenv
import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

router = APIRouter()

@router.post("/upload/")
async def upload_multiple_files(files: List[UploadFile] = File(...)):
    saved_paths = await save_uploaded_files(files)
    return {"file_paths": saved_paths}

@router.post("/extract/", response_model=ExtractResponse, description="Extract a pre-defined data model from a file.")
async def extract_data_model(file: UploadFile = File(...), category: Category = None):
    logging.info(f"Extracting data for {file.filename} initiated...")

    file_metadata = FileMetadata(fileName=file.filename, contentType=file.content_type, size=file.size)

    file_location = await save_uploaded_file(file)
    logging.info(f"File upload for {file.filename} successful...")

    document = await read_file(file_location)
    logging.info(f"Reading text for {file.filename} successful...")
    print(len(document))

    document_metadata = await create_document_metadata(document=document[0])
    logging.info(f"Reading document metadata for {file.filename} successful...")

    category_to_data_model = {
        Category.CapitalCall: CapitalCall,
        Category.CLA: ConvertibleLoanAgreement,
    }
    category = category or document_metadata.category
    data_model = category_to_data_model.get(category)
    data = await create_data_model(document=document[0], data_model=data_model)

    response = ExtractResponse(
        fileMetadata = file_metadata,
        documentMetadata = document_metadata,
        data = data
    )

    return response

    ## code from  before moving data extraction to models into extract_utils 
    # document_text = document[0].text

    # prompt_template_str = """\
    # Extract all relevant information from {file_text}. Return "NULL" if a property cannot be found.\
    # """

    # program = LLMTextCompletionProgram.from_defaults(
    #     output_cls = CapitalCall,
    #     prompt_template_str = prompt_template_str,
    #     verbose = False
    # )

    # result = program(file_text=document_text)
    # print(result)

    # return result