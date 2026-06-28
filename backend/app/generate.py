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
        dti=round(installment / monthly_income * 100, 2),
        installment=installment,
        tot_cur_bal=random.randint(1000, annual_inc),
        revol_util=round(random.uniform(5, 95), 2),
        emp_length=random.randint(0, 25),
        home_ownership=random.choice(["RENT", "OWN", "MORTGAGE"]),
        open_acc=random.randint(1, 15),
        total_acc=random.randint(5, 40),
        bc_util=round(random.uniform(5, 95), 2),
        avg_cur_bal=random.randint(1000, 100000),
        purpose=random.choice([
            "debt_consolidation", "credit_card", "home_improvement", "house", 
            "car", "major_purchase", "medical", "moving", "vacation", 
            "wedding", "small_business", "educational", "renewable_energy", "other"
        ]),
        verification_status=random.choice(["Verified", "Source Verified", "Not Verified"]),
        
        FLAG_MOBIL=random.choice([0, 1]),
        FLAG_PHONE=random.choice([0, 1]),
        FLAG_WORK_PHONE=random.choice([0, 1]),
        FLAG_CONT_MOBILE=random.choice([0, 1]),
        FLAG_EMAIL=random.choice([0, 1]),
        DAYS_EMPLOYED=random.randint(-10000, 0),
        FLAG_OWN_REALTY=random.choice(["Y", "N"]),
        NAME_HOUSING_TYPE=random.choice(["House / apartment", "With parents", "Municipal apartment", "Rented apartment", "Office apartment", "Co-op apartment"]),
        CNT_CHILDREN=random.randint(0, 5),
        CNT_FAM_MEMBERS=random.randint(1, 7),
        NAME_FAMILY_STATUS=random.choice(["Married", "Single / not married", "Civil marriage", "Separated", "Widow"]),
        DAYS_REGISTRATION=random.randint(-20000, 0),
        DAYS_ID_PUBLISH=random.randint(-10000, 0),
        DAYS_LAST_PHONE_CHANGE=random.randint(-4000, 0),
        REG_REGION_NOT_WORK_REGION=random.choice([0, 1]),
        REG_CITY_NOT_WORK_CITY=random.choice([0, 1]),
        LIVE_CITY_NOT_WORK_CITY=random.choice([0, 1]),
        NAME_EDUCATION_TYPE=random.choice(["Higher education", "Secondary / secondary special", "Incomplete higher", "Lower secondary", "Academic degree"]),
        NAME_INCOME_TYPE=random.choice(["Working", "Commercial associate", "Pensioner", "State servant", "Student"]),
        OCCUPATION_TYPE=random.choice(["Laborers", "Core staff", "Accountants", "Managers", "Drivers", "Sales staff"]),
        ORGANIZATION_TYPE=random.choice(["Business Entity Type 3", "School", "Government", "Medicine", "Self-employed"]),
        REGION_RATING_CLIENT=random.choice([1, 2, 3])
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