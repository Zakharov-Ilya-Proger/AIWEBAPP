import json

import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
import firebase_admin
from firebase_admin import credentials, firestore

from app.send_to_AI import send_to_gpt
from settings import settings

app = FastAPI()

firebase_credentials = settings.FIREBASE_CREDENTIALS
cred = credentials.Certificate(json.loads(firebase_credentials))
firebase_admin.initialize_app(cred)
db = firestore.client()

app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_headers=["*"]
                   )

@app.middleware("http")
async def block_ips(request: Request, call_next):
    client_ip = str(request.client.host)
    if client_ip != settings.ALLOWED_USER_IP:
        return JSONResponse(
            status_code=403,
            content={"message": "Доступ запрещен"},
        )
    response = await call_next(request)
    return response


@app.get("/")
async def root():
    return {"message": "Darova Zaebal"}


@app.get("/question/{userid}")
async def get_question(userid: str):
    user_doc = db.collection('user_session').document(userid).get()
    response = await send_to_gpt(user_doc.to_dict()['prompt'], user_doc.to_dict()['lang'])
    if isinstance(response, HTTPException):
        raise response
    return {'message': response}
