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
    dti = Column(Float)
    installment = Column(Float)
    fico_score = Column(Integer)
    tot_cur_bal = Column(Float)
    revol_util = Column(Float)
    emp_length = Column(Integer)
    home_ownership = Column(String(30))
    inq_last_6mths = Column(Integer)
    delinq_2yrs = Column(Integer)
    pct_tl_nvr_dlq = Column(Float)
    open_acc = Column(Integer)
    total_acc = Column(Integer)
    bc_util = Column(Float)
    avg_cur_bal = Column(Float)
    acc_open_past_24mths = Column(Integer)
    grade = Column(String(5))
    sub_grade = Column(String(10))
    purpose = Column(String(100))
    verification_status = Column(String(50))
    credit_history_years = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    user = relationship("User", back_populates="applications")
    prediction = relationship("Prediction", back_populates="application", uselist=False, cascade="all, delete-orphan")

   


class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True)

    application_id = Column(Integer, ForeignKey("credit_applications.id", ondelete="CASCADE"), nullable=False, unique=True)

    default_probability = Column(Float)
    credit_score = Column(Integer)
    risk_level = Column(String(20))

    top_factors = Column(JSON)

    model_version = Column(String(50))

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

    application = relationship("CreditApplication", back_populates="prediction")