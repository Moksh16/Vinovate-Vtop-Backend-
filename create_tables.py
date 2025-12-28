from vtop.models import Users
from vtop.models import FFCS
from vtop.models import Faculty 
from vtop.models import Parent
from vtop.models import Student
from vtop.models import Faculty_subject
from vtop.models import Marks
from vtop.models import Attendance
from vtop.models import reval
from vtop.models import selected_slots
from vtop.db import Base,engine
print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Tables created successfully.")