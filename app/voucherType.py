from fastapi import FastAPI,Depends
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
voucherTypes = [
    {"ID": "FESG", "NAME": "FE/SG受験バウチャー"},
    {"ID": "OR00", "NAME": "Oracle認定資格ピアソンVUE 配信監督なし試験用"}
]

@app.get("/list")
def get_voucher_type_list(token:str,db: Session = Depends(get_db)):
    vname = db.query(VoucherType).all()
    return vname

@app.get("/{ID}")
def get_voucher_type_item(ID:str,token:str,db: Session = Depends(get_db)):
    Voucher_Info = db.query(VoucherType).get(ID)
    if(Voucher_Info is None):
        return{}
    else:
        return Voucher_Info

@app.post("/add")
def get_voucherType_item(ID:str,NAME:str,token:str, db: Session = Depends(get_db)):
    new_item = VoucherType(voucher_id=ID,voucher_name=NAME)
    if(ID is None or NAME is None):
        #kuuhakutoosanaisyorituika
        return {"message": "voucherType was not added successfully", "voucherType": {{"ID": new_item.voucher_id, "NAME":new_item.voucher_name}}}
    else:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return{"追加処理成功!!!!!": new_item}
    
	