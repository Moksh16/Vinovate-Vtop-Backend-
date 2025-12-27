from fastapi import FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session




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

subjects = [

    {
        "math":{
            "teachers": [
                {"name": "animesh", "slot":"A2"},
                {"name":"Abdul Haq", "slot":"A1"}
                ],
                "credits": 5
            }   
        }
        ]



#backend for students

marks_and_grade = [{'Physics':
                    {"marks":35,"grades":'A'}
                    }]
subject_info = {}
attendance={"Physics":"80%", "Chemistry":"55%"}
total_credits=0
@app.get('/marks')
def see_marks_grade():
    return marks_and_grade

    
def max_credits(max,credits):
    total_credits += credits
    if total_credits>max:
        total_credits-= credits
        return False
    else:
        return True

@app.post('/ffcs')
def add_slot(subject_name, teacher_name, slot):

    for subject in subjects:

        if subject_name in subject:

            teachers = subject[subject_name]["teachers"]

            for teacher in teachers:

                if teacher["name"] == teacher_name and teacher["slot"] == slot:

                    
                    credit= subject[subject_name]['credits']
                    credit_outcome =max_credits(27,credit)
                    if credit_outcome==False:
                        return {"Credit limit reached"}
                    subject.append({"Subject": subject_name,"Professor":teacher_name})

                    return {"Course Successfully added"}
                else:

                    return {"Your slots are clashing, try with some other slot"}
                
@app.get('/attendance')
def see_attendance():
    return attendance