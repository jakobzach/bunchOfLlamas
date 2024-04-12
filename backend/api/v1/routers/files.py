from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Query
from api.utils.upload_utils import save_uploaded_files, save_uploaded_file, delete_file
from api.utils.extract_utils import read_file,create_document_metadata,create_data_model, return_csv_column_names, create_mapping_model
from api.data_models.response_models import FileMetadata, ModelCategory, CapitalCall, ConvertibleLoanAgreement, ExtractResponse, MappingResponse, MappingCategory, InvestmentColumns
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
async def extract_data_model(file: UploadFile = File(..., description="Currently, only the following file types are supported: ['.pdf', '.xml.doc', '.docx', '.pptx', '.rtf', '.pages', '.key', '.epub']"), category: ModelCategory = None):
    logging.info(f"/extract for {file.filename} initiated...")

    file_metadata = FileMetadata(fileName=file.filename, contentType=file.content_type, extension="."+file.filename.split(".")[-1], size=file.size)

    file_location = await save_uploaded_file(file)
    logging.info(f"File upload for {file.filename} successful...")

    document = await read_file(file_location, file_metadata.extension)
    logging.info(f"Reading text for {file.filename} successful...")
    print(len(document))

    await delete_file(file_location)
    logging.info(f"File deletion for {file.filename} successful...")

    document_metadata = await create_document_metadata(document=document[0])
    logging.info(f"Reading document metadata for {file.filename} successful...")

    category_to_data_model = {
        ModelCategory.CapitalCall: CapitalCall,
        ModelCategory.CLA: ConvertibleLoanAgreement
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

@router.post("/map-columns/", response_model=MappingResponse, description="Map columns of a csv to a pre-defined data model.")
async def map_columns(file: UploadFile = File(..., description="Only csv files are supported."), category: MappingCategory = Query(..., description="The category for mapping.")):
    logging.info(f"/map-columns for {file.filename} initiated...")
    file_metadata = FileMetadata(fileName=file.filename, contentType=file.content_type, extension="."+file.filename.split(".")[-1], size=file.size)

    if not file_metadata.extension == ".csv":
        raise HTTPException(status_code=400, detail="File must be a csv file")

    file_location = await save_uploaded_file(file)
    logging.info(f"File upload for {file.filename} successful...")

    columns = await return_csv_column_names(file_location)

    await delete_file(file_location)
    logging.info(f"File deletion for {file.filename} successful...")

    category_to_data_model = {
        MappingCategory.Investment: InvestmentColumns
        }
    data_model = category_to_data_model.get(category)

    data = await create_mapping_model(header=columns, data_model=data_model)

    response = MappingResponse(
        fileMetadata = file_metadata,
        data = data
    )

    return response