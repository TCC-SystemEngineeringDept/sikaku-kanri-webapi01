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

    if len(ename) == 0:
        return {}

    # 返却用のリストに変換して返却
    return_list = []
    for r in ename:
        return_list.append({"ID": r.exam_id, "NAME": r.exam_name})

    return return_list

@app.get("/{ID}")
def get_exam_item(ID:str,token:str,db: Session = Depends(get_db)):
    exam_info = db.query(Exam).get(ID)
    if(exam_info is None):
        return {}
    else:
        return {"ID": exam_info.exam_id, "NAME": exam_info.exam_name}
    
    

    


@app.post("/add")
def add_exam_item(ID:str,NAME:str,token:str,db: Session = Depends(get_db)):
    new_item = Exam(exam_id=ID,exam_name=NAME)
    if(ID is None or NAME is None):
        return {"message": "Exam added successfully", "exam": {"ID": "FE00", "NAME": "基本情報技術者試験"}}
    else:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return{"追加処理成功": new_item}