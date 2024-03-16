# Define Pydantic class for data validation
from pydantic import BaseModel

class Companies(BaseModel):
    name: str