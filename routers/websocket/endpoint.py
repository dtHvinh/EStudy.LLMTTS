from fastapi import APIRouter, WebSocket, Request, WebSocketDisconnect
from piper import PiperVoice
from helper.prompt_loader import load_prompt_to_messages
from helper.prompt_loader import set_prompt_to_messages
from openai import OpenAI
import logging
from managers.websocket_manager import manager
import constants.symbol as const
import os
import http.client
import json
import ssl

websocket_router = APIRouter()

VOICE_PATH = r"D:\dev\AI\Voices\en_US-hfc_female-medium\en_US-hfc_female-medium.onnx"
voice = PiperVoice.load(VOICE_PATH)


def get_conversation_context(conversation_id: str) -> str:
    conn = http.client.HTTPSConnection(
        "localhost", 7185, context=ssl._create_unverified_context()
    )
    conn.request("GET", f"/api/ai/conversations/{conversation_id}")
    response = conn.getresponse()
    response_body = response.read()
    conversation_details = json.loads(response_body.decode("utf-8"))
    context = conversation_details.get("context", "")
    conn.close()
    return context


def save_assistant_conversation_message(conversation_id: str, message: str):
    conn = http.client.HTTPSConnection(
        "localhost", 7185, context=ssl._create_unverified_context()
    )
    headers = {"Content-Type": "application/json"}
    payload = json.dumps({"isUserMessage": False, "message": message})
    conn.request(
        "POST", f"/api/ai/conversations/{conversation_id}/messages", payload, headers
    )
    response = conn.getresponse()
    if response.status != 200:
        logging.error(f"Failed to save message: {response.status} {response.reason}")
    conn.close()


@websocket_router.websocket("/ws/chat/{conversation_id}")
async def voicechat_endpoint(websocket: WebSocket, conversation_id: str):
    await websocket.accept()
    manager.add_connection(conversation_id, websocket)

    context = get_conversation_context(conversation_id)

    try:
        while True:
            payload = await websocket.receive_json()
            messages = payload.get("messages", [])

            if not messages:
                await websocket.close(
                    code=4000, reason="Missing 'messages' in JSON body"
                )
                return

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=(
                    set_prompt_to_messages(messages, context)
                    if context is not None
                    else load_prompt_to_messages(messages, "Lexa")
                ),
            )

            output_text = response.choices[0].message.content

            save_assistant_conversation_message(conversation_id, output_text)

            tts_gen = voice.synthesize(output_text)

            await websocket.send_text(output_text)

            for chunk in tts_gen:
                await websocket.send_bytes(chunk.audio_int16_bytes)

            await websocket.send_text(const.VOICE_STREAM_END)

    except WebSocketDisconnect:
        await manager.close_connection(conversation_id)
