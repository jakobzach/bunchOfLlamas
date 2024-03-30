from pydantic import BaseModel
from typing import List

from llama_index.program.openai import OpenAIPydanticProgram

class Song(BaseModel):
    title: str
    length_seconds: int


class Album(BaseModel):
    name: str
    artist: str
    songs: List[Song]

prompt_template_str = """\
Generate an example album, with an artist and a list of songs. \
Using the movie {movie_name} as inspiration.\
"""
program = OpenAIPydanticProgram.from_defaults(
    output_cls=Album, prompt_template_str=prompt_template_str, verbose=True
)

output = program(
    movie_name="The Shining", description="Data model for an album."
)