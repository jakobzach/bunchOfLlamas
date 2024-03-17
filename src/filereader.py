from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("LLAMAINDEX_KEY")


from llama_parse import LlamaParse
from llama_index.core.program import LLMTextCompletionProgram
import models

prompt_template_str = """\
List all financing rounds for {legal_entity}. \
"""

rounds = LLMTextCompletionProgram.from_defaults(
    output_cls = models.LegalEntity,
    prompt_template_str = prompt_template_str,
    verbose = True,
)