from fastapi import Depends, APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.utils import PDF_OPERATIONS
import os, base64
# from db.database import fetch_prompts, insert_result_pdf, update_prompt, insert_prompt, delete_prompt

router = APIRouter(tags=["Do not look at this now"], responses={404: {"description": "Not found"}})

@router.post("/upload_file", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def upload_document(request: Request):
    data = await request.json()

    try:
        PDF_OPERATIONS(data['base64']).create_embeddings()
        return JSONResponse(status_code=200, content={"status_code": 200, "message": "Data has been extracted from PDF and Embeddings has been saved in DB!!"})
    except Exception as e:
        print(e)
        return JSONResponse(status_code=401, content={"status_code": 401, "message": "Error while data extraction."})


@router.post("/ask_question", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def ques_ask(request: Request):
    data = await request.json()

    response = PDF_OPERATIONS(data['prompt']).ask_question()
    # try:
    #     response = PDF_OPERATIONS(data['prompt']).ask_question()
    #     return JSONResponse(status_code=200, content={"status_code": 200, "response": response})
    # except Exception as e:
    #     print(e)
    #     return JSONResponse(status_code=401, content={"status_code": 401, "message": "Error while data extraction."})
    

@router.get("/", responses={200: {"headers": {"Access-Control-Allow-Origin": "*"}}})
async def root():
    try:
        return JSONResponse(status_code=200, content={"status_code": 200, "message": "App is working !!"})
    except Exception as e:
        # raise HTTPException
        return JSONResponse(status_code=401, content={"status_code": 401, "message": str(e)})