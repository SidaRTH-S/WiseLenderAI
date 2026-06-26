from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import models
from app.schemas import UserCreate, UserOut, GiveConsent
from app.utils import hash_password
from app.core.oauth2 import get_current_user


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/", status_code=201, response_model = UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    
    user.password = hash_password(user.password)

    new_user = models.User(**user.model_dump())
    db.add(new_user)      
    db.commit()           
    db.refresh(new_user) 
    return new_user

@router.patch("/giveconsent/{id}", status_code=200, response_model=UserOut)
def give_consent(id: int, payload: GiveConsent, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):    
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {id} not found")
    
    user.consent_given = payload.consent_given
    
    db.commit()
    db.refresh(user)

    return user