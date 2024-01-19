from fastapi import FastAPI
import db

app = FastAPI()

# 商品リストのデータ
voucherTypes = [
    {"ID": "FESG", "NAME": "FE/SG受験バウチャー"},
    {"ID": "OR00", "NAME": "Oracle認定資格ピアソンVUE 配信監督なし試験用"}
]

@app.get("/list")
def get_voucher_type_list(token:str):
    vname = db.query(db.VoucherType).all()
    return vname

@app.get("/{ID}")
def get_voucher_type_item(ID:str,token:str):
    if ID == "FESG":
        return voucherTypes[0]
    elif ID == "OR00":
        return voucherTypes[1]
    else:
        return {}

@app.post("/add")
def get_voucherType_item(ID:str,NAME:str,token:str):
    if(ID == None or NAME == None):
        return {"message": "voucherType was not added successfully", "voucherType": {}}
    else:
        db.VoucherType.voucher_id.add(ID)
        db.VoucherType.voucher_name.add(NAME)
        return{"追加処理成功!!!!!":(ID,NAME)}
    
	