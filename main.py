from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel
# Writen in the FastAPI Documentation that if we have a optinal parameter we must include this Optional

# TODO routers

# Api object this will initialize our api
app = FastAPI()

# Course Class inharates from base model
class Course(BaseModel):
    course_name: str
    grade: int
    credit: float
    course_type: Optional[str] = None # Required, Choice, Entrepreneurship, Multidisciplinary
    year: Optional[str]        = None # A, B, C
    semester: Optional[str]    = None # A, B, S

class UpdateCourse(BaseModel):
    course_name: Optional[str] = None
    grade: Optional[int]       = None
    credit: Optional[float]    = None
    course_type: Optional[str] = None # Required, Choice, Entrepreneurship, Multidisciplinary
    year: Optional[str]        = None # A, B, C
    semester: Optional[str]    = None # A, B, S

class StudentInfo(BaseModel):
    name:     str
    username: str

grade_Sheet = {}

#check
@app.get('/')
def home():
    return "Welcome to the GArithmetics app! 😊"

# Register
@app.post('/new_user')
async def addaccount(user: StudentInfo):
    data = {"name": user.name, "username": user.username}
    #response = user_DB(data) #no db yet
    return ("The account was created succesfully!")

# Login will be add when after the DB

# The Create end point
@app.post('/create-course/{course_id}')
def create_course(course_id: int, course: Course):
    if course_id in grade_Sheet:
        return {"Error": "Course ID already exists."}

    grade_Sheet[course_id] = {"course_name": course.course_name, "grade": course.grade, "credit": course.credit, 
    "course_type": course.course_type, "year": course.year, "semester": course.semester}
    #grade_Sheet[course_id] = course
    return grade_Sheet[course_id]

# View end point get by id
@app.get('/get-course/{course_id}')
def get_course(course_id: int = Path(None, description="The ID of the course you'd like to view")):
    return grade_Sheet[course_id]

# View end point get by id all courses
# TODO response model 
@app.get('/get-all-courses')
def get_all_courses():
    # from db order by semester, oreder by year.
    return grade_Sheet

# Query parameter get by name
@app.get('/get-by-course-name')
def get_course(course_name : Optional[str] = None):
    for course_id in grade_Sheet:
        if grade_Sheet[course_id]["course_name"] == course_name:
            return grade_Sheet[course_id]
    return {"Data": "Not found"}
# TODO testing python

# Update the course
@app.put('/update-course/{course_id}')
def update_course(course_id: int, course: UpdateCourse):
    if course_id not in grade_Sheet:
        return {"Error" : "Course ID does not exist."}

    if course.course_name != None:
        grade_Sheet[course_id]["course_name"] = course.course_name

    if course.grade != None:
        grade_Sheet[course_id]["grade"] = course.grade

    if course.credit != None:
        grade_Sheet[course_id]["credit"] = course.credit

    if course.course_type != None:
        grade_Sheet[course_id]["course_type"] = course.course_type
    
    if course.year != None:
        grade_Sheet[course_id]["year"] = course.year

    if course.semester != None:
        grade_Sheet[course_id]["semester"] = course.semester

    #grade_Sheet[course_id] = course
    #grade_Sheet[course_id].update(course)
    return grade_Sheet[course_id]

# Deleting Course
@app.delete('/delete-course')
def delete_course(course_id: int = Query(None, description="The ID of the course to delete")):
    if course_id not in grade_Sheet:
        return {"Error": "ID does not exist"}
    del grade_Sheet[course_id]

# Averege Score
@app.get('/score')
def calc_score():
    grades = 0.0
    totalCredits = 0.0
    cretidsNeeded = 119.5
    coursestook = 0
    for course_id in grade_Sheet:
        grades += grade_Sheet[course_id]["grade"] * grade_Sheet[course_id]["credit"]
        totalCredits += grade_Sheet[course_id]["credit"]
        coursestook += 1

    #if 0 == totalCredits:
    #    return 

    return { 
        "Amount of courses took": coursestook,
        "GPA":               round(grades/totalCredits, 2),
        "Credits":           totalCredits,
        "Credits Remaining": cretidsNeeded - totalCredits
        } 
# returns Avg Grade and Total credits  

# python -m uvicorn main:app --reload
