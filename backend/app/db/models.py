from datetime import datetime
from sqlalchemy.orm import relationship
from app.db.database import Base

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    DateTime,
    ForeignKey,
    text,
    TIMESTAMP,
    JSON
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100), nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=True)
    password = Column(String, nullable=False)
    consent_given = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    documents = relationship("UploadedDocument", back_populates="user", cascade="all, delete-orphan")
    applications = relationship("CreditApplication", back_populates="user", cascade="all, delete-orphan")



class UploadedDocument(Base):
    __tablename__ = "uploaded_documents"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    document_type = Column(String(50), nullable=False)
    # BANK_STATEMENT
    # PHONE_BILL
    # QUESTIONNAIRE

    file_name = Column(String(255), nullable=False)
    file_path = Column(String, nullable=False)
    uploaded_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user = relationship("User", back_populates="documents")

class CreditApplication(Base):
    __tablename__ = "credit_applications"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
  
    loan_amnt = Column(Float)
    annual_inc = Column(Float)
    installment = Column(Float)
    dti = Column(Float)
    tot_cur_bal = Column(Float)
    avg_cur_bal = Column(Float)
    open_acc = Column(Integer)
    total_acc = Column(Integer)
    emp_length = Column(Integer)
    revol_util = Column(Float)
    bc_util = Column(Float)
    home_ownership = Column(String(30))
    purpose = Column(String(100))
    verification_status = Column(String(50))
    
    FLAG_MOBIL = Column(Integer)
    FLAG_PHONE = Column(Integer)
    FLAG_WORK_PHONE = Column(Integer)
    FLAG_CONT_MOBILE = Column(Integer)
    FLAG_EMAIL = Column(Integer)
    DAYS_EMPLOYED = Column(Integer)
    FLAG_OWN_REALTY = Column(String(5))
    NAME_HOUSING_TYPE = Column(String(50))
    CNT_CHILDREN = Column(Integer)
    CNT_FAM_MEMBERS = Column(Integer)
    NAME_FAMILY_STATUS = Column(String(50))
    DAYS_REGISTRATION = Column(Integer)
    DAYS_ID_PUBLISH = Column(Integer)
    DAYS_LAST_PHONE_CHANGE = Column(Integer)
    REG_REGION_NOT_WORK_REGION = Column(Integer)
    REG_CITY_NOT_WORK_CITY = Column(Integer)
    LIVE_CITY_NOT_WORK_CITY = Column(Integer)
    NAME_EDUCATION_TYPE = Column(String(100))
    NAME_INCOME_TYPE = Column(String(100))
    OCCUPATION_TYPE = Column(String(100))
    ORGANIZATION_TYPE = Column(String(100))
    REGION_RATING_CLIENT = Column(Integer)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User", back_populates="applications")
    prediction = relationship("Prediction", back_populates="application", uselist=False, cascade="all, delete-orphan")

   


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("credit_applications.id", ondelete="CASCADE"), nullable=False, unique=True)
    financial_index = Column(Float)
    behavioral_index = Column(Float)
    digital_trust_index = Column(Float)
    meta_index = Column(Float)
    alternative_credit_score = Column(Integer)
    financial_default_probability = Column(Float)
    behavioral_default_probability = Column(Float)
    digital_default_probability = Column(Float)
    overall_default_probability = Column(Float)
    risk_level = Column(String(20))
    financial_shap_explanations = Column(JSON)
    behavioral_shap_explanations = Column(JSON)
    digital_trust_shap_explanations = Column(JSON)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    application = relationship("CreditApplication", back_populates="prediction")