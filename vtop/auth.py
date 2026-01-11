from fastapi import Depends,APIRouter,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

from . import models, oauth2, schemas, db,utils
router = APIRouter(prefix="/login")


@router.post('/login')
def login(user_credentials:schemas.UserLogin,db:Session= Depends(db.get_db)):
    user = db.query(models.Users).filter(models.Users.email== user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found. Invalid credentails")
    if not utils.verify_password(user_credentials.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Password invalid")
    
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}