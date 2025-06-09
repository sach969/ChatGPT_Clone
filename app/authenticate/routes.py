from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas, database
from app.authenticate.hashing import hash_password, verify_password
from app.authenticate.jwt import create_access_token

router = APIRouter(prefix="/auth")
 
def get_db():
    db = database.sessionlocal()
    try:
        yield db 
    finally:                                                                                                                                                            
        db.close()

@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
  
    db_user = models.User(username=user.username, hashed_password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    return {"msg": "User created"}

@router.post("/login")
def login(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token({"sub": str(db_user.id)})
    return schemas.Token(access_token=token, token_type="bearer")