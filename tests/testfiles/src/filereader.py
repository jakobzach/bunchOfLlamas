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
    reader = SimpleDirectoryReader("/Users/jakobzacherl/Library/Mobile Documents/com~apple~CloudDocs/bunch/bunchOfLlamas/testfiles", file_extractor=file_extractor)
    documents = reader.load_data(show_progress=True, num_workers=1)
    return documents
