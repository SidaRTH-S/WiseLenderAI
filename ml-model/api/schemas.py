from pydantic import BaseModel


class LoanApplication(BaseModel):

    loan_amnt: float
    annual_inc: float
    dti: float

    installment: float

    fico_score: float

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