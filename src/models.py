# Define Pydantic class for data validation
from pydantic import BaseModel, Field, ValidationError
from typing_extensions import Annotated
import datetime

class CapitalCall(BaseModel):
    """Data model for a single investor's share of a capital call."""
    name: str = Field(...,description="Name of investor")
    date: datetime.datetime = Field(...,description="Date of issuance of capital call")
    deadline: datetime.datetime = Field(...,description="Date of deadline for capital call")
    commitment: float = Field(...,description="Investor's share of total commitment")
    equityShare: Annotated[float, Field(ge=0,le=1)] = Field(...,description="Investor's percentage share of equity")
    previouscontributionToTarget: float = Field(...,description="Investor's share of previous contribution to target")
    contributionToTarget: float = Field(...,description="Investor's share of contribution to target")
    organizationalExpenses: float = Field(...,description="Investor's share of organizational expenses")
    liquidityBuffer: float = Field(...,description="Investor's share of liquidity buffer")
    bunchFee: float = Field(...,description="Investor's share of Bunch fee")
    adjustmentsFromPreviousCapitalCalls: float = Field(...,description="Investor's share of adjustments from previous capital calls")
    totalCapitalCalled: float = Field(...,description="Investor's share of total capital called")
    outstandingCommitmentToTarget: float = Field(...,description="Investor's share of outstanding commitment to target")
    currency: str

    def shareOfTotalGoingToTarget(self, totalCapitalCalled, contributionToTarget):
        return contributionToTarget/totalCapitalCalled

class LegalEntity(BaseModel):
    name: str

class Ownership(BaseModel):
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