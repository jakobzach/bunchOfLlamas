# Define Pydantic class for data validation
from pydantic import BaseModel, Field, validator, ValidationError
from typing_extensions import Annotated
from typing import List, Optional, Any
from enum import Enum

import datetime

class ModelCategory(Enum):
    """Enum for metadata categories."""
    CapitalCall = "CapitalCall"
    LPA = "LimitedPartnershipAgreement"
    EquityRound = "EquityRound"
    CLA = "ConvertibleLoanAgreement"
    SHA = "ShareholderAgreement"
    GeneralInformation = "GeneralInformation"
    Other = "Other"

class MappingCategory(Enum):
    """Enum for categories of mapped columns."""
    Investment = "Investment"

class Sector(Enum):
    """Enum for economic sectors/industries."""
    Aerospace = "Aerospace"
    Agriculture = "Agriculture"
    AI_ML = "Artificial Intelligence & Machine Learning"
    AR_VR = "Augmented & Virtual Reality"
    Beauty = "Beauty & Personal Care"
    Biotech = "Biotechnology & Life Sciences"
    Blockchain_Crypto = "Blockchain & Cryptocurrency"
    Cloud_DevOps = "Cloud Computing & DevOps"
    Construction_RealEstate = "Construction & Real Estate"
    Cybersecurity = "Cybersecurity"
    DataAnalytics_BigData = "Data Analytics & Big Data"
    DigitalMedia_Entertainment = "Digital Media & Entertainment"
    ECommerce_Retail = "E-commerce & Retail"
    Education = "Education"
    Energy = "Energy"
    FinancialServices = "Financial Services"
    Food_Beverages = "Food & Beverages"
    Gaming_ESports = "Gaming & eSports"
    Healthtech_MedicalDevices = "Healthtech & Medical Devices"
    HR_Workforce = "HR & Workforce"
    Insurance = "Insurance"
    IoT = "Internet of Things (IoT)"
    Manufacturing = "Manufacturing"
    Mobility = "Mobility"
    Nutrition_Wellness = "Nutrition & Wellness"
    Pharmaceuticals_DrugDevelopment = "Pharmaceuticals & Drug Development"
    Robotics_Automation = "Robotics & Automation"
    Semiconductors_Microchips = "Semiconductors & Microchips"
    SupplyChain_Logistics = "Supply Chain & Logistics"
    Sustainability = "Sustainability"
    Other = "Other"

class BusinessModel(Enum):
    """Enum for business models."""
    Advertisement = "Advertisement"
    Affiliate = "Affiliate"
    Licensing = "Licensing"
    Marketplace = "Marketplace"
    OneTimeSales = "One-Time Sales"
    PayPerUse = "Pay-Per-Use"
    SaaS = "Software-as-a-Service (SaaS)"
    Subscription = "Subscription"
    Other = "Other"

class InvestmentType(Enum):
    """Enum for investment types."""
    Company = "Company"
    Fund = "Fund"
    Token = "Token"

class DocumentMetadata(BaseModel):
    """Metadata of a document."""
    category: ModelCategory = Field(..., description="Unique category in this text chunk. ")
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
    type: ModelCategory = Field(..., description="Unique category for this text chunk.")

class GeneralCompanyInfo(DocumentData):
    """Data model for a company (primarily a startup) or alternative asset."""
    companyName: str = Field(..., description="Name of company or alternative asset being invested into.")
    companyDescription: Optional[str] = Field(None, description="Description of company or alternative asset being invested into.")
    website: Optional[str] = Field(None, description="Website of company or alternative asset being invested into.")
    currency: Optional[Annotated[str, Field(max_length=3, min_length=3)]] = Field(None, description="Currency of company or alternative asset being invested into.")
    type: Optional[InvestmentType] = Field(None, description="Type of company or alternative asset being invested into.")
    sector: Optional[Sector] = Field(None, description="Sector of company or alternative asset being invested into.")
    businessModel: Optional[str] = Field(None, description="Business model of company or alternative asset being invested into.")
    primaryOperatingCountry: Optional[str] = Field(None, description="Primary operating country of company or alternative asset being invested into.")
    otherOperatingCountries: Optional[List[str]] = Field(None, description="Other operating countries of company or alternative asset being invested into.")
    founders: Optional[List[str]] = Field(None, description="List of first and last names of founders of the company or alternative asset being invested into.")
    
class RecurrencyFrequency(Enum):
    """Enum for recurrency frequency."""
    Yearly = "Yearly"
    Quarterly = "Quarterly"
    Monthly = "Monthly"
    Weekly = "Weekly"
    Daily = "Daily"

class RecurrentRevenue(BaseModel):
    """Data model for recurrent revenue."""
    amount: float = Field(..., description="Amount of recurrent revenue.")
    recurrencyFrequency: RecurrencyFrequency = Field(..., description="Recurrency frequency of recurrent revenue. Default is yearly.")

class Revenue(BaseModel):
    """Data model for revenue. Has to have either oneTimeRevenue or recurrentRevenue and can have both."""
    currency: Annotated[str, Field(max_length=3, min_length=3)] = Field(..., description="Currency of revenue. Default is EUR.")
    recurrentRevenue: Optional[RecurrentRevenue] = Field(None, description="Recurrent revenue.")
    oneTimeRevenue: Optional[float] = Field(None, description="One-time revenue.")

class OperationalKPIs(DocumentData):
    """Data model for a startup's operational KPIs based on a periodical update."""
    date: datetime.datetime = Field(None, description="Date of update.")
    revenue: Optional[Revenue] = Field(None, description="Revenue. How much money is being generated at time of update.")
    cashBalance: Optional[float] = Field(None, description="Cash balance. How much money is available at time of update.")
    monthlyBurn: Optional[float] = Field(None, description="Monthly burn. How much money is being spent per month (= negative cashflow).")
    ftes: Optional[float] = Field(None, description="FTEs. How many full-time employees are in the company at time of update.")

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
    extension: str
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

class InvestmentColumns(BaseModel):
    """Mapping of columns of a csv to a data model."""
    companyName: Optional[str] = Field(None, description="Name of a column header for a company or alternative asset being invested into.")
    currency: Optional[str] = Field(None, description="Name of a column header for a currency.")
    type: Optional[str] = Field(None, description="Name of a column header for a type of company or alternative asset being invested into.")
    sector: Optional[str] = Field(None, description="Name of a column header for a sector of company or alternative asset being invested into.")
    businessModel: Optional[str] = Field(None, description="Name of a column header for a business model of company or alternative asset being invested into.")
    website: Optional[str] = Field(None, description="Name of a column header for a website of company or alternative asset being invested into.")

class MappingResponse(BaseModel):
    """Data model for a mapping response."""
    fileMetadata: FileMetadata
    data: Any

    class Config:
        schema_extra = {
            "fileMetadata": {
                "fileName": "Capital Call 1 - Valentina Pape - 13251239173529.pdf",
                "contentType": "application/pdf",
                "size": 240428
            },
            "data": {}
        }