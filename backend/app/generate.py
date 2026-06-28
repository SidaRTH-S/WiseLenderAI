import random

from app.db.database import SessionLocal
from app.db.models import CreditApplication


def create_application(db):

    annual_inc = random.randint(200000, 2000000)

    loan_amnt = random.randint(
        10000,
        min(500000, int(annual_inc * 0.4))
    )

    installment = round(
        loan_amnt / random.randint(12, 60),
        2
    )

    monthly_income = annual_inc / 12

    application = CreditApplication(
        user_id=random.choice([1, 3, 6]),

        loan_amnt=loan_amnt,
        annual_inc=annual_inc,

        dti=round(
            installment / monthly_income * 100,
            2
        ),

        installment=installment,

        fico_score=random.randint(580, 850),

        tot_cur_bal=random.randint(
            1000,
            annual_inc
        ),

        revol_util=round(
            random.uniform(5, 95),
            2
        ),

        emp_length=random.randint(0, 25),

        home_ownership=random.choice([
            "RENT",
            "OWN",
            "MORTGAGE"
        ]),

        inq_last_6mths=random.randint(0, 6),

        delinq_2yrs=random.randint(0, 3),

        pct_tl_nvr_dlq=round(
            random.uniform(70, 100),
            2
        ),

        open_acc=random.randint(1, 15),

        total_acc=random.randint(5, 40),

        bc_util=round(
            random.uniform(5, 95),
            2
        ),

        avg_cur_bal=random.randint(
            1000,
            100000
        ),

        acc_open_past_24mths=random.randint(0, 8),

        grade=random.choice([
            "A",
            "B",
            "C",
            "D",
            "E"
        ]),

        sub_grade=random.choice([
            "A1", "A2",
            "B1", "B2",
            "C1", "C2",
            "D1", "D2"
        ]),

        purpose=random.choice([
            "debt_consolidation",
            "medical",
            "education",
            "home_improvement"
        ]),

        verification_status=random.choice([
            "Verified",
            "Source Verified",
            "Not Verified"
        ]),

        credit_history_years=round(
            random.uniform(1, 25),
            1
        )
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


if __name__ == "__main__":

    db = SessionLocal()

    try:
        app = create_application(db)

        print(
            f"Application created:"
            f"\nID={app.id}"
            f"\nUSER_ID={app.user_id}"
        )

    finally:
        db.close()