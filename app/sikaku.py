import datetime
from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from db import SessionLocal, Sikaku, Exam

app = FastAPI()

# 資格リストのデータ
Passed = [
    {"ID": "FE00", "NAME": "基本情報技術者試験", "DATE": "2022/06/18"},
    {"ID": "OR00", "NAME": "Java SE Bronze", "DATE": "2023/02/20"}
]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/list")
def get_passed_list(token:str, db: Session = Depends(get_db)):
    joined_table = db.query(Sikaku, Sikaku.exam_id, Exam.exam_name, Sikaku.passed_date).join(Exam, Sikaku.exam_id == Exam.exam_id).all()
    if len(joined_table) == 0:
        return {}

    # 返却用のリストに変換して返却
    return_list = []
    for r in joined_table:
        return_list.append({"ID": r.exam_id, "NAME": r.exam_name, "DATE": f"{r.passed_date:%Y/%m/%d}"})

    return return_list

@app.get("/{ID}")
def get_passed_item(ID:str,token:str, db: Session = Depends(get_db)):
    joined_table = db.query(Sikaku, Sikaku.exam_id, Exam.exam_name, Sikaku.passed_date).join(Exam, Sikaku.exam_id == Exam.exam_id).filter(Sikaku.exam_id == ID).all()

    if len(joined_table) == 0:
        return {}
    else:
        jt = joined_table
        return {"ID": jt[0].exam_id, "NAME": jt[0].exam_name, "DATE": f"{jt[0].passed_date:%Y/%m/%d}"}


@app.post("/add")
def add_passed_item(ID:str, DATE:str, token:str, db: Session = Depends(get_db)):
    DATE = datetime.datetime.strptime(DATE, "%Y/%m/%d")
    new_item = Sikaku(exam_id=ID, user_id="001", passed_date=DATE)
    if (ID is None or DATE is None):
        return {"message": "Passed was not added successfully", "sikaku": {{"ID": new_item.exam_id, "DATE": new_item.passed_date},}}
    else:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return {"追加処理成功": new_item}