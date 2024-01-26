from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from db import SessionLocal, Exam

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 資格リストのデータ
Exams = [
    {"ID": "FE00", "NAME": "基本情報技術者試験"},
    {"ID": "OR00", "NAME": "Java SE Bronze"}
]

@app.get("/list")
def get_exam_list(token:str,db: Session = Depends(get_db)):
    ename = db.query(Exam).all()
    return ename

@app.get("/{ID}")
def get_exam_item(ID:str,token:str,db: Session = Depends(get_db)):
    exam_info = db.query(Exam).get(ID)
    return exam_info


@app.post("/add")
def add_exam_item(ID:str,NAME:str,token:str,db: Session = Depends(get_db)):
    new_item = Exam(exam_id=ID,exam_name=NAME)
    if(ID == None or NAME == None):
        return {"message": "Exam added successfully", "exam": {"ID": "FE00", "NAME": "基本情報技術者試験"}}
    else:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return{"追加処理成功": new_item}