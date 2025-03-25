from fastapi import Depends, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from services.utils import create_embeddings, ask_question
from db.database import pdf_db_connect, engine
from sqlalchemy.orm import Session
from models.model import Insert_PDF_Record
from models import model
import datetime

router = APIRouter(tags=["Do not look at this now"], responses={404: {"description": "Not found"}})

@router.post("/upload_file", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def upload_document(request: Request, db: Session = Depends(pdf_db_connect)):
    data = await request.json()

    try:
        model.Base.metadata.create_all(bind=engine)
        embedding_id = create_embeddings(data['filename'].replace(" ", "_"), data['base64'])

        pdf_model = Insert_PDF_Record()
        pdf_model.filename = data['filename'].replace(" ", "_")
        pdf_model.embedding_id = embedding_id
        pdf_model.uploaded_on = datetime.datetime.now()

        db.add(pdf_model)
        db.commit()

        return JSONResponse(status_code=200, content={"status_code": 200, "message": "Data has been extracted from PDF and Embeddings has been saved in DB!!"})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Error while data injection in DB.")


@router.post("/ask_question", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def ques_ask(request: Request):
    data = await request.json()

    try:
        del data['uploaded_on']
        response = ask_question(data)
        return JSONResponse(status_code=200, content={"status_code": 200, "response": response})
    except Exception as e:
        print(e)
        raise HTTPException(status_code=401, detail="Error while answering question.")