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
    



class ExtractResponse(BaseModel):
    """Data model for an extract response."""
    fileMetadata: dict = Field(..., description="Metadata of the file such as filename, type, etc.")
    documentMetadata: DocumentMetadata
    data: Any