from fastapi import FastAPI
import datetime
import voucherType
from sqlalchemy.orm import Session
from db import SessionLocal, VoucherType

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
    return vouchers

@app.get("/{ID}")
def get_voucher_item(ID:str,token:str,db: Session = Depends(get_db)):
    
    if ID == "FESG":
        return vouchers[0]
    elif ID == "OR00":
        return vouchers[1]
    else:
        return {}
    

@app.post("/add")
def add_voucher_item(ID:str,DATE:str,token:str,db: Session = Depends(get_db)):
    DATE = datetime.datetime.strptime(DATE, "%Y-%m-%d")
    new_items = vouchers(voucher_id=ID,limit_date=DATE)
    if(ID is None or DATE is None):
        #kuuhakutoosanaisyorituika
        return {"message": "voucherType was not added successfully", "voucher":  {{"ID": "FESG" , "DATE": "2024/06/20"}}}
    else:
        db.add(new_items)
        db.commit()
        db.refresh(new_items)
        return{"追加処理成功!!!!!": new_items}
	