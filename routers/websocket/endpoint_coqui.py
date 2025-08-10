from fastapi import APIRouter, WebSocket
from TTS.api import TTS
from helper.prompt_loader import load_prompt_to_messages
from openai import OpenAI
from dotenv import load_dotenv
import logging
import constants.symbol as const
import os
import numpy as np
import asyncio
import torch

websocket_router_coqui = APIRouter()

# Global TTS instance to avoid reloading on each request
_tts_instance = None


def get_tts_instance():
    """Get or create TTS instance"""
    global _tts_instance
    if _tts_instance is None:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        _tts_instance = TTS(
            model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False
        ).to(device)
        logging.info(f"Coqui TTS initialized on {device}")
    return _tts_instance


@websocket_router_coqui.websocket("/ws/chat/coqui")
async def voicechat_endpoint_coqui(websocket: WebSocket):
    """
    WebSocket endpoint using Coqui TTS with pseudo-streaming
    """
    await websocket.accept()

    # Initialize TTS once per connection
    try:
        tts = get_tts_instance()
    except Exception as e:
        await websocket.close(code=4001, reason=f"TTS initialization failed: {str(e)}")
        return

    while True:
        try:
            payload = await websocket.receive_json()
            messages = payload.get("messages", [])

            if not messages:
                await websocket.close(
                    code=4000, reason="Missing 'messages' in JSON body"
                )
                return

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=load_prompt_to_messages(messages, "Lexa"),
            )

            output_text = response.choices[0].message.content
            await websocket.send_text(output_text)

            await synthesize_and_stream_coqui(websocket, tts, output_text)

            await websocket.send_text(const.VOICE_STREAM_END)

        except Exception as e:
            logging.error(f"Error in Coqui WebSocket endpoint: {e}")
            await websocket.close(code=4002, reason=f"Processing error: {str(e)}")
            break


async def synthesize_and_stream_coqui(websocket: WebSocket, tts: TTS, text: str):
    """
    Synthesize text with Coqui TTS and stream to websocket

    Args:
        websocket: WebSocket connection
        tts: TTS instance
        text: Text to synthesize
        method: "full" (synthesize all then chunk) or "sentences" (sentence by sentence)
    """
    try:
        await stream_full_then_chunk(websocket, tts, text)
    except Exception as e:
        logging.error(f"TTS synthesis error: {e}")
        # Fallback to text if TTS fails
        await websocket.send_text(f"[TTS Error: {str(e)}]")


async def stream_full_then_chunk(websocket: WebSocket, tts: TTS, text: str):
    """
    Synthesize full text then chunk the output
    """
    # Synthesize entire text
    wav = tts.tts(text=text)

    # Convert to int16 bytes
    wav_array = np.array(wav)
    wav_int16 = np.clip(wav_array * 32767, -32768, 32767).astype(np.int16)
    wav_bytes = wav_int16.tobytes()

    # Send in chunks (similar to Piper chunk size)
    chunk_size = 4096
    for i in range(0, len(wav_bytes), chunk_size):
        chunk = wav_bytes[i : i + chunk_size]
        await websocket.send_bytes(chunk)
        # Small delay to simulate streaming behavior
        await asyncio.sleep(0.01)


# Alternative implementation with async synthesis
async def voicechat_endpoint_coqui_async(websocket: WebSocket):
    """
    Alternative implementation using asyncio for non-blocking synthesis
    """
    await websocket.accept()

    while True:
        try:
            payload = await websocket.receive_json()
            messages = payload.get("messages", [])

            if not messages:
                await websocket.close(
                    code=4000, reason="Missing 'messages' in JSON body"
                )
                return

            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
            response = client.chat.completions.create(
                model="gpt-4.1-nano",
                messages=load_prompt_to_messages(messages, "Lexa"),
            )

            output_text = response.choices[0].message.content
            await websocket.send_text(output_text)

            # Run TTS in executor to avoid blocking
            loop = asyncio.get_event_loop()
            tts = get_tts_instance()

            # Synthesize in background thread
            wav = await loop.run_in_executor(None, tts.tts, output_text)

            # Stream the result
            wav_array = np.array(wav)
            wav_int16 = np.clip(wav_array * 32767, -32768, 32767).astype(np.int16)
            wav_bytes = wav_int16.tobytes()

            chunk_size = 4096
            for i in range(0, len(wav_bytes), chunk_size):
                chunk = wav_bytes[i : i + chunk_size]
                await websocket.send_bytes(chunk)

            await websocket.send_text(const.VOICE_STREAM_END)

        except Exception as e:
            logging.error(f"Error in async Coqui WebSocket endpoint: {e}")
            await websocket.close(code=4002, reason=f"Processing error: {str(e)}")
            break
