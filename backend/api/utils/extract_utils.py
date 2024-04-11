import os
from typing import List
from dotenv import load_dotenv
import logging
from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader
from llama_index.core.program import LLMTextCompletionProgram
from api.data_models import response_models
import csv

logging.basicConfig(level=logging.INFO)
load_dotenv()

api_key = os.getenv("LLAMA_CLOUD_API_KEY")

parser = LlamaParse(
    api_key=api_key,
    result_type="markdown"  # "markdown" and "text" are available
)

#file_extractor = {".pdf": parser}

async def return_csv_column_names(file_location: str) -> List:
    """returns the column names of the csv file"""
    logging.info(f"Reading columns from {file_location} initiated...")
    with open(file_location, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
    logging.info(f"Reading column names for {file_location} successful...")
    return header

async def read_file(file_location: str, extension: str) -> List:
    directory = os.path.dirname(os.path.abspath(file_location))
    logging.info(f"Reading file from directory: {directory}")
    print("Extension: ", extension)
    reader = SimpleDirectoryReader(directory, file_extractor={extension: parser})
    documents = await reader.aload_data(show_progress=True, num_workers=1)
    print(documents)
    return documents

prompt_template_str = """\
Extract all relevant information from {document_text}. Return a null value if a property cannot be found.\
"""
# prompt_template_str = """\
#         Restrict your answer to only the following information:
#         ----------------
#         {document_text}
#         ----------------\
#         """

async def create_data_model(document: dict, data_model) -> dict:
    logging.info(f"Creating data model for: {document}")

    program = LLMTextCompletionProgram.from_defaults(
        output_cls=data_model,
        prompt_template_str=prompt_template_str,
        verbose=True
    )

    result = program(document_text=document.text)
    return result

prompt_template_str_mapping = """\
Map the following columns to {data_model}: {header}. Return a null value if a property cannot be found.\
"""

async def create_mapping_model(header: List, data_model) -> dict:
    logging.info(f"Creating mapping model for: {header}")

    program = LLMTextCompletionProgram.from_defaults(
        output_cls=data_model,
        prompt_template_str=prompt_template_str_mapping,
        verbose=True
    )

    result = program(data_model=data_model, header=header)
    return result

async def create_document_metadata(document: dict, ) -> dict:
    logging.info(f"Creating file metadata for: {document}")
    
    program = LLMTextCompletionProgram.from_defaults(
        output_cls = response_models.DocumentMetadata,
        prompt_template_str = prompt_template_str,
        verbose = True
    )

    result = program(document_text=document.text)
    return result