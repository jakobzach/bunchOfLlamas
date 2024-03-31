from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LLAMA_CLOUD_API_KEY")

from llama_parse import LlamaParse
from llama_index.core import SimpleDirectoryReader

parser = LlamaParse(
    api_key=api_key,
    result_type="markdown"  # "markdown" and "text" are available
)

def read_file():
    file_extractor = {".pdf": parser}
    print("searching for file...")
    reader = SimpleDirectoryReader(input_dir=os.path.dirname(os.path.abspath("tests/testfiles/Capital Call 1 - Valentina Pape - 13251239173529.pdf")), file_extractor=file_extractor)
    print("file found...") 
    documents = reader.load_data(show_progress=True, num_workers=1)
    return documents
