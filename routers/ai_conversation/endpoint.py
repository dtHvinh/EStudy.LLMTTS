from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import StreamingResponse
from piper import PiperVoice
from ollama import chat
from helper.prompt_loader import load_prompt_to_messages

ai_convo_router = APIRouter()

# Load the Piper voice model
VOICE_PATH = r"D:\dev\AI\Voices\en_US-hfc_female-medium\en_US-hfc_female-medium.onnx"
voice = PiperVoice.load(VOICE_PATH)


@ai_convo_router.post(
    "/voice_chat",
    description="Chat endpoint for AI conversations",
    summary="Chat with AI",
)
async def voicechat_endpoint(request: Request):
    payload = await request.json()
    messages = payload.get("messages", [])
    if not messages:
        raise HTTPException(status_code=400, detail="Missing 'messages' in JSON body")

    response = chat(
        "llama3.2:1b", messages=load_prompt_to_messages(messages, "RealPerson")
    )

    tts_gen = voice.synthesize(response.message.content)

    def generate():
        for chunk in tts_gen:
            yield chunk.audio_int16_bytes

    return StreamingResponse(
        generate(),
        media_type="audio/L16",
        headers={"Transfer-Encoding": "chunked"},
    )
