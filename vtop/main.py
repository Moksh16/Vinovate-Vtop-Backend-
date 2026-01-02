from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from sqlalchemy import func
from typing import Optional
from random import randrange
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from . import models
from .db import get_db  # assuming you have a get_db dependency
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="Login")
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

class user(BaseModel):
    name: str
    password: str
    role: str

class SelectSubjectRequest(BaseModel):
    subject_id: int


@app.get('/marks')
def see_marks_grade(db: Session = Depends(get_db)):
    marks = db.query(models.Marks).all()
    return {"Your marks ": marks}


@app.post("/select-subject-ffcs")
def ffcs_selection(request: SelectSubjectRequest, db: Session = Depends(get_db)):
    subject_row = db.query(models.FFCS).filter(models.FFCS.id == request.subject_id).first()

    if not subject_row:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject = subject_row.subject
    credits = subject_row.credits
    slot = subject_row.slot
    faculty_name = subject_row.faculty_name

    # check whether we have already selected that subject
    if db.query(models.selected_slots).filter(models.selected_slots.subject == subject).first():
        raise HTTPException(status_code=404, detail="You already have that subject in your list")
    
    # check if the slot is already occupied
    if db.query(models.selected_slots).filter(models.selected_slots.slot == slot).first():
        raise HTTPException(status_code=400, detail="Slot already occupied")
    
    # check total credits
    total_credits = db.query(models.selected_slots).with_entities(
        func.coalesce(func.sum(models.selected_slots.credits), 0)
    ).scalar()

    if total_credits + credits > 27:
        raise HTTPException(status_code=400, detail="Credit limit exceeded")
    total_credits += credits

    # insert the new subject
    new_slot = models.selected_slots(
        subject=subject,
        credits=int(credits),
        slot=slot,
        faculty_name=faculty_name
    )
    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)

    return {
        "message": "selected successfully",
        "subject": subject,
        "slot": slot,
        "faculty_name": faculty_name,
        "total_credits": total_credits
    }


@app.get('/attendance')
def see_attendance(db: Session = Depends(get_db)):
    attendance = db.query(models.Attendance).all()
    return {"Your attendance: ": attendance}


@app.get('/selected-slots')
def slots_selected(db: Session = Depends(get_db)):
    slots = db.query(models.selected_slots).all()
    total_credits = db.query(models.selected_slots).with_entities(
        func.coalesce(func.sum(models.selected_slots.credits), 0)
    ).scalar()
    return {"your slots": slots, "totalCredits": total_credits}

