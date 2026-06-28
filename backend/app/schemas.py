from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List
from enum import Enum


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    phone: int

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(UserBase):
    id: int
    consent_given: bool = False
    model_config = ConfigDict(from_attributes=True)

class GiveConsent(BaseModel):
    consent_given: bool

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None

class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class ModelResponse(BaseModel):
    default_probability: float
    credit_score: int
    risk_level: RiskLevel
    top_factors: List[str]

class ModelInput(BaseModel):
    loan_amnt: float
    annual_inc: float
    dti: float
    installment: float
    fico_score: int
    tot_cur_bal: float
    revol_util: float
    emp_length: int
    home_ownership: str
    inq_last_6mths: int
    delinq_2yrs: int
    pct_tl_nvr_dlq: float
    open_acc: int
    total_acc: int
    bc_util: float
    avg_cur_bal: float
    acc_open_past_24mths: int
    grade: str
    sub_grade: str
    purpose: str
    verification_status: str
    credit_history_years: float