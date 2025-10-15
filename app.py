# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.ai_conversation.endpoint import ai_convo_router
from routers.websocket.endpoint import websocket_router
from routers.test.endpoint import test_router
from dotenv import load_dotenv

load_dotenv(".env")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def start():
    app = FastAPI()
    app.include_router(ai_convo_router)
    return app


app.include_router(websocket_router)
app.include_router(test_router)

app.mount("/api", start())
