from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router as api_router
from api.ws import websocket_endpoint
from fastapi import WebSocket
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Matma API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Later do not foget to restrict this at frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_router)
@app.websocket("/ws")
async def ws(websocket: WebSocket):
    await websocket_endpoint(websocket)
