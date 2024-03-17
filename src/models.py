# Define Pydantic class for data validation
from pydantic import BaseModel, ValidationError
import datetime

class LegalEntity(BaseModel):
    name: str

class Ownership():
    committedAmount: float
    numberOfShares: int
    shareNumberOfSharesAcquired: str

class Round(BaseModel):
    name: str
    date: datetime.datetime
    totalRoundSize: float
    sharePrice: float
    otherInvestors: set[str]

class Equity(BaseModel):
    name: str
    totalNumberofShares: float

class CLA(BaseModel):
    name: str
    amount: float