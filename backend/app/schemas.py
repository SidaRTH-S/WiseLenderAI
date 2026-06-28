from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
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
    financial_index: float
    behavioral_index: float
    digital_trust_index: float
    meta_index: float
    alternative_credit_score: int
    financial_default_probability: float
    behavioral_default_probability: float
    digital_default_probability: float
    overall_default_probability: float
    risk_level: RiskLevel
    financial_shap_explanations: Dict[str, Any]
    behavioral_shap_explanations: Dict[str, Any]
    digital_trust_shap_explanations: Dict[str, Any]

class ModelInput(BaseModel):
    loan_amnt: float
    annual_inc: float
    installment: float
    dti: float
    tot_cur_bal: float
    avg_cur_bal: float
    open_acc: int
    total_acc: int
    emp_length: int
    revol_util: float
    bc_util: float
    home_ownership: str
    purpose: str
    verification_status: str

    FLAG_MOBIL: int
    FLAG_PHONE: int
    FLAG_WORK_PHONE: int
    FLAG_CONT_MOBILE: int
    FLAG_EMAIL: int
    DAYS_EMPLOYED: int
    FLAG_OWN_REALTY: str
    NAME_HOUSING_TYPE: str
    CNT_CHILDREN: int
    CNT_FAM_MEMBERS: int
    NAME_FAMILY_STATUS: str
    DAYS_REGISTRATION: int
    DAYS_ID_PUBLISH: int
    DAYS_LAST_PHONE_CHANGE: int
    REG_REGION_NOT_WORK_REGION: int
    REG_CITY_NOT_WORK_CITY: int
    LIVE_CITY_NOT_WORK_CITY: int
    NAME_EDUCATION_TYPE: str
    NAME_INCOME_TYPE: str
    OCCUPATION_TYPE: str
    ORGANIZATION_TYPE: str
    REGION_RATING_CLIENT: int

class CreditApplicationOut(ModelInput):
    id: int
    user_id: int
    created_at: datetime
    prediction: Optional[ModelResponse] = None
    model_config = ConfigDict(from_attributes=True)