from filereader import read_file
from llama_index.core.program import LLMTextCompletionProgram
from llama_index.program.openai import OpenAIPydanticProgram
import models

def main():
    document = read_file()
    document_text = document[0].text
    #print(document[0].text)

    prompt_template_str = """\
    Extract all relevant information from {file_text}. Return "NULL" if a property cannot be found.\
    """
    program = LLMTextCompletionProgram.from_defaults(
        output_cls = models.CapitalCall,
        prompt_template_str = prompt_template_str,
        verbose = False
    )

    result = program(file_text=document_text)

    return result

if __name__ == "__main__":
    output = main()

    print(output.json())