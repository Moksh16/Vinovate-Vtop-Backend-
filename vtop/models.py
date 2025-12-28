from .db import Base
from sqlalchemy import Column, Integer, String,Boolean,DateTime,ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import Enum

class Users(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True)
    role = Column(
        Enum("Student", "Parent", "Faculty", "Admin", name="role_enum"),
        nullable=False
    )
    username = Column(String, unique=True,nullable=False)
    password_hash = Column(String, nullable=False)


class FFCS(Base):
    __tablename__ = "FFCS"

    id = Column(Integer, primary_key=True)
    subject = Column(String,nullable=False)
    credits = Column(Integer,nullable=False)
    slot = Column(Enum("A1+TA1", "B1/TB1", "C1/TC1", "D1/TD1", "E1/TE1","F1/TF1","G1/TG1", name="slot_enum"),nullable=False)
    faculty_name = Column(String, nullable=False)

class Student(Base):
    __tablename__ = "Student"

    registration_number = Column(String, primary_key=True)
    name = Column(String,nullable=False)
    parent_id = Column(String,nullable=False)


class Faculty(Base):
    __tablename__ = "Faculty"

    registration_number = Column(String, primary_key=True)
    name = Column(String,nullable=False)
    department = Column(String, nullable=False)


class Parent(Base):
    __tablename__ = "Parent"
    name = Column(String, nullable=False)
    id = Column(Integer,primary_key=True, nullable=False)
    child_id = Column(String,ForeignKey("Student.registration_number"),nullable=False)


class Faculty_subject(Base):
    __tablename__ = "faculty_subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String,nullable=False)
    Subject = Column(String,nullable=False)




class Marks(Base):
    __tablename__ = "marks"

    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False)
    marks = Column(Integer, nullable=False)
    grade = Column(String, nullable=True)


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=False)
    subect = Column(DateTime)
    present = Column(Boolean, nullable=False)
    
class reval(Base):
    __tablename__ = "Revaluation"
    id = Column(Integer, primary_key=True)
    student_regno = Column(String, nullable=False)
    subject = Column(String, nullable=False)
    enrollment_status = Column(Enum("PENDING", "APPROVED", "REJECTED", name="reeval_status_enum"), default="PENDING")


class selected_slots(Base):
    __tablename__ = "Selected_slots"
    id = Column(Integer, primary_key=True)
    subject = Column(String, nullable=False,unique=True)
    faculty_name = Column(String,nullable=False,unique=True)
    credits = Column(Integer,nullable=False)
    slot = Column(Enum("A1+TA1", "B1/TB1", "C1/TC1", "D1/TD1", "E1/TE1","F1/TF1","G1/TG1", name="slot_enum"),unique=True)
