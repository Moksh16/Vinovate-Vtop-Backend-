from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import time
from sqlalchemy.orm import Session
from passlib.context import CryptContext
oauth_2_scheme = OAuth2PasswordBearer(tokenUrl="Login")
password_hasher = CryptContext(schemes=["bcrypt"], deprecated="auto")



while True:
    try:
        conn = psycopg2.connect(host='localhost',database='vinovate',user='postgres',password='moksh', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connection established")
        break
    except Exception as error:
        print("Connection to server failed")
        print("error,",error)
        time.sleep(2)

app = FastAPI()

class user(BaseModel):
    name: str
    password: str
    role: str




class SelectSubjectRequest(BaseModel):
    subject_id: int


@app.get('/marks')
def see_marks_grade():
    cursor.execute("""select * from marks""")
    marks = cursor.fetchall()
    return {"Your marks ": marks}


@app.post("/select-subject-ffcs")
def ffcs_selection(request: SelectSubjectRequest):
    cursor.execute("""SELECT subject, credits, slot, faculty_name FROM "FFCS" WHERE id = %s""",(request.subject_id,))
    subject_row = cursor.fetchone()
    # to check the subject is in the original ffcs list or not
    if not subject_row:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    subject = subject_row["subject"]
    credits = subject_row["credits"]
    slot = subject_row["slot"]
    faculty_name = subject_row["faculty_name"]

    # to check whether we have already selected that subject or not
    cursor.execute("""select * from "Selected_slots" where subject = %s""",(subject,))

    if cursor.fetchone():
        raise HTTPException(status_code=404, detail = "You already have that subject in your list")
    
    # to dheck we already have selected that slot or not
    cursor.execute("""SELECT 1 FROM "Selected_slots" WHERE slot = %s""",(slot,))

    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Slot already occupied")
    
    # to check our credits are fulfilled or not
    # to check our credits are fulfilled or not
    cursor.execute(
    """SELECT COALESCE(SUM(credits), 0) AS total_credits
       FROM "Selected_slots";"""
)

    row = cursor.fetchone()
    total_credits = row["total_credits"]


    if total_credits + credits > 27:
        raise HTTPException(status_code=400, detail="Credit limit exceeded")
    total_credits +=credits
    

    # it all conditions are satisfied, additing the required subject into our selected list
    cursor.execute("""INSERT INTO "Selected_slots" (subject,credits, slot, faculty_name) VALUES (%s, %s, %s, %s)""",
        (subject,int(credits), slot, faculty_name))
    conn.commit()

    return {
        "message": "selected successfully",
        "subject": subject,
        "slot": slot,
        "faculty_name": faculty_name,
        "total_credits": total_credits
    }
                
@app.get('/attendance')
def see_attendance():
    cursor.execute("""select * from attendance""")
    attendance = cursor.fetchall()
    return {"Your attendance: ": attendance}

@app.get('/selected-slots')
def slots_selected():
    cursor.execute("""select * from "Selected_slots" """)
    slots = cursor.fetchall()
    cursor.execute(
    """SELECT COALESCE(SUM(credits), 0) AS total_credits
       FROM "Selected_slots";"""
)
    row = cursor.fetchone()
    total_credits = row["total_credits"]
    return{"your slots": slots}, {"totalCredits": total_credits}