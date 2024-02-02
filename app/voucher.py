from fastapi import FastAPI,Depends
import datetime
import voucherType
from sqlalchemy.orm import Session
from db import SessionLocal, Voucher,VoucherType

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 商品リストのデータ
vouchers = [
    {"ID": "FESG", "NAME": "FE/SG受験バウチャー", "DATE": "2024/06/20"},
    {"ID": "OR00", "NAME": "Oracle認定資格ピアソンVUE 配信監督なし試験用", "DATE": "2023/12/25"}
]

@app.get("/list")
def get_voucher_list(token:str,db: Session = Depends(get_db)):
    joined_table = db.query(Voucher, Voucher.voucher_id, VoucherType.voucher_name, Voucher.limit_date).join(VoucherType,Voucher.voucher_id == VoucherType.voucher_id).all()
    
    # 返却用のリストに変換して返却
    return_list = []
    for r in joined_table:
        return_list.append({"ID": r.voucher_id, "NAME": r.voucher_name, "DATE": f"{r.limit_date:%Y/%m/%d}"})
    return return_list

@app.get("/{ID}")
def get_voucher_item(ID:str,token:str,db: Session = Depends(get_db)):
    joined_table = db.query(Voucher, Voucher.exam_id, VoucherType.exam_name, Voucher.limit_date).join(Exam, Sikaku.exam_id == Exam.exam_id).filter(Sikaku.exam_id == ID).all()

    if len(joined_table) == 0:
        return {}
    else:
        # 返却用のリストに変換して返却
        return_list = []
        for r in joined_table:
            return_list.append({"ID": r.exam_id, "NAME": r.exam_name, "DATE": f"{r.passed_date:%Y/%m/%d}"})
        return return_list
    
@app.post("/add")
def add_voucher_item(ID: str,DATE:str,token:str,db: Session = Depends(get_db)):
    DATE = datetime.datetime.strptime(DATE, "%Y/%m/%d")
    new_items = Voucher(voucher_id=ID, user_id="001", limit_date=DATE)
    if(ID is None or DATE is None):
        #kuuhakutoosanaisyorituika
        return {"message": "voucherType was not added successfully", "voucher":  {{"ID": new_items.voucher_id, "DATE": new_items.limit_date}}}
    else:
        db.add(new_items)
        db.commit()
        db.refresh(new_items)
        return{"追加処理成功!!!!!": new_items}
	