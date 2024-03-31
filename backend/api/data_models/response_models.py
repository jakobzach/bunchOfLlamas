# Define Pydantic class for data validation
from pydantic import BaseModel, Field, validator, ValidationError
from typing_extensions import Annotated
from typing import List, Optional, Any
from enum import Enum

import datetime

class Category(Enum):
    """Enum for metadata categories."""
    CapitalCall = "CapitalCall"
    LPA = "LimitedPartnershipAgreement"
    EquityRound = "EquityRound"
    CLA = "ConvertibleLoanAgreement"
    SHA = "ShareholderAgreement"
    Other = "Other"

class DocumentMetadata(BaseModel):
    """Metadata of a document."""
    category: Category = Field(..., description="Unique category in this text chunk. ")
    entities: List[str] = Field(..., description="Unique entities in this text chunk.")
    summary: str = Field(..., description="A concise summary of this text chunk. Maximum of 250 characters.")
    containsFinancials: bool = Field(..., description="Whether the text chunk contains any company performance metrics or financial data.",)

    ## add back in if categories should be extended to be a list
    # @validator('categories')
    # def list_must_not_be_empty(cls, categories):
    #     if len(categories) == 0:
    #         raise ValueError('Category not found.')
    #     return categories
    
#superclass of all document data models
class DocumentData(BaseModel):
    type: Category = Field(..., description="Unique category for this text chunk.")

class CapitalCall(DocumentData):
    """Data model for a single investor's share of a capital call."""
    name: Optional[str] = Field(..., description="Name of investor")
    date: Optional[datetime.datetime] = Field(None, description="Date of issuance of capital call")
    deadline: Optional[datetime.datetime] = Field(None, description="Date of deadline for capital call")
    commitment: Optional[float] = Field(None, description="Investor's share of total commitment")
    equityShare: Optional[Annotated[float, Field(ge=0, le=1)]] = Field(None, description="Investor's percentage share of equity")
    previouscontributionToTarget: Optional[float] = Field(None, description="Investor's share of previous contribution to target")
    contributionToTarget: Optional[float] = Field(None, description="Investor's share of contribution to target")
    organizationalExpenses: Optional[float] = Field(None, description="Investor's share of organizational expenses")
    liquidityBuffer: Optional[float] = Field(None, description="Investor's share of liquidity buffer")
    bunchFee: Optional[float] = Field(None, description="Investor's share of Bunch fee")
    adjustmentsFromPreviousCapitalCalls: Optional[float] = Field(None, description="Investor's share of adjustments from previous capital calls")
    totalCapitalCalled: Optional[float] = Field(None, description="Investor's share of total capital called")
    outstandingCommitmentToTarget: Optional[float] = Field(None, description="Investor's share of outstanding commitment to target")
    currency: Optional[str] = Field(None)

class ConvertibleLoanAgreement(DocumentData):
    """Data model for the details of a convertible loan agreement."""
    date: datetime.datetime = Field(...,description="Date of the agreement")
    loanAmount: float = Field(...,description="Total amount of the loan")
    currency: str = Field(...,description="Currency of the loan")
    interestRate: float = Field(...,description="Interest rate of the loan")
    valuationCap: float = Field(...,description="Maximum post-money valuation for which the loan converts to shares")
    valuationDiscount: float = Field(...,description="Discount on the post-money valuation for which the loan converts to shares")
    

class FileMetadata(BaseModel):
    """Data model for a file metadata."""
    fileName: str
    contentType: str
    size: int

    class Config:
        schema_extra = {
            "fileName": "Capital Call 1 - Valentina Pape - 13251239173529.pdf",
            "contentType": "application/pdf",
            "size": 240428
        }

class ExtractResponse(BaseModel):
    """Data model for an extract response."""
    fileMetadata: FileMetadata
    documentMetadata: DocumentMetadata
    data: Any

    class Config:
        schema_extra = {
            "fileMetadata": {
                "fileName": "Capital Call 1 - Valentina Pape - 13251239173529.pdf",
                "contentType": "application/pdf",
                "size": 240428
            },
            "documentMetadata": {
                "category": "CapitalCall",
                "entities": [
                    "Cherry Fund IV GmbH & Co. KG",
                    "Valentina Pape"
                ],
                "summary": "Capital Call 1 for Cherry Fund IV GmbH & Co. KG with details of funds to be transferred by Valentina Pape.",
                "containsFinancials": True
            },
            "data": {
                "type": "CapitalCall",
                "name": "Valentina Pape",
                "date": "2023-10-19T00:00:00",
                "deadline": "2023-11-19T00:00:00",
                "commitment": 500000.0,
                "equityShare": 0.02,
                "previouscontributionToTarget": 0.0,
                "contributionToTarget": 99880.0,
                "organizationalExpenses": 20.0,
                "liquidityBuffer": 0.0,
                "bunchFee": 100.0,
                "adjustmentsFromPreviousCapitalCalls": 0.0,
                "totalCapitalCalled": 100000.0,
                "outstandingCommitmentToTarget": 40000.0,
                "currency": "EUR"
            }
        }
