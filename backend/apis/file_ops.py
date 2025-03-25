from fastapi import Depends, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from db.database import pdf_db_connect
from sqlalchemy.orm import Session
from models.model import Insert_PDF_Record, Model_Resp

router = APIRouter(tags=["Do not look at this now"], responses={404: {"description": "Not found"}})

@router.get("/get_all_files", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}}, response_model=Model_Resp)
async def upload_document(db: Session = Depends(pdf_db_connect)):
    try:
        records = db.query(Insert_PDF_Record).all()

        return JSONResponse(status_code=200, content={"status_code": 200, "details": jsonable_encoder(records)})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Error while data extraction from DB.")
    

@router.get("/")
async def index():
    return JSONResponse(status_code=200, content={"status_code": 200, "message": "App is working good !!"})