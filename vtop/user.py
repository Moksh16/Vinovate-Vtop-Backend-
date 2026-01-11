from fastapi import FastAPI, Response,status,HTTPException, Depends, APIRouter
from . import utils,schemas,models
from sqlalchemy.orm import Session
from . import db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate , db: Session = Depends(db.get_db)):

    hashed_password = utils.hash(user.password[:72])
    user.password = hashed_password
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/{id}', response_model=schemas.UserOut)
def get_current_user(id:int,db : Session = Depends(db.get_db)):
    users = db.query(models.Users.id).filter(models.Users.id == id).first()

    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with {id} not found")
    return users