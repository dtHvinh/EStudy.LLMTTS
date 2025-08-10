"""
Coqui TTS Streaming Test
Comparing Coqui TTS streaming capabilities with Piper TTS approach
"""

import torch
from TTS.api import TTS
import io
import numpy as np
import time


def test_coqui_streaming():
    """
    Test Coqui TTS streaming capabilities
    """
    print("Testing Coqui TTS streaming...")

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    try:
        # Using a lightweight model for testing
        tts = TTS(
            model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False
        ).to(device)

        text = "Hello, this is a test of Coqui TTS streaming capabilities. We want to see if we can get audio in chunks like Piper TTS does."

        print(f"Synthesizing: '{text}'")
        start_time = time.time()

        # Method 1: Standard synthesis (non-streaming)
        print("\n--- Method 1: Standard synthesis ---")
        wav = tts.tts(text=text)
        synthesis_time = time.time() - start_time
        print(f"Standard synthesis completed in {synthesis_time:.2f} seconds")
        print(f"Audio shape: {np.array(wav).shape}")
        print(f"Audio sample rate: {tts.synthesizer.output_sample_rate}")

        # Method 2: Chunk the output manually
        print("\n--- Method 2: Manual chunking ---")
        wav_array = np.array(wav)
        chunk_size = 4096  # Similar to what Piper might use
        chunks = []

        for i in range(0, len(wav_array), chunk_size):
            chunk = wav_array[i : i + chunk_size]
            chunks.append(chunk)
            print(f"Chunk {len(chunks)}: {len(chunk)} samples")

        print(f"Total chunks: {len(chunks)}")

        # Method 3: Check if streaming synthesis is available
        print("\n--- Method 3: Streaming capabilities ---")

        # Coqui TTS doesn't have native streaming like Piper, but we can simulate it
        # by synthesizing in smaller segments
        sentences = text.split(". ")
        print(f"Splitting into {len(sentences)} sentences for pseudo-streaming:")

        streaming_chunks = []
        for i, sentence in enumerate(sentences):
            if sentence.strip():
                print(f"Synthesizing sentence {i+1}: '{sentence.strip()}'")
                sentence_wav = tts.tts(text=sentence.strip() + ".")
                streaming_chunks.append(np.array(sentence_wav))

        print(f"Streaming approach created {len(streaming_chunks)} audio segments")

        return True

    except Exception as e:
        print(f"Error with TTS model: {e}")
        print("Trying alternative approach...")
        return test_coqui_alternative()


def test_coqui_alternative():
    """
    Test with a different Coqui TTS model or approach
    """
    try:
        # Try with Tacotron2 model
        tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False)

        text = "Testing alternative Coqui TTS model."
        wav = tts.tts(text=text)

        print("Alternative model working!")
        print(f"Audio shape: {np.array(wav).shape}")

        return True

    except Exception as e:
        print(f"Alternative model also failed: {e}")
        return False


def compare_with_piper_approach():
    """
    Compare Coqui TTS approach with Piper TTS streaming
    """
    print("\n" + "=" * 60)
    print("COMPARISON: Coqui TTS vs Piper TTS")
    print("=" * 60)

    print(
        """
    PIPER TTS (Current implementation):
    ✅ Native streaming support with voice.synthesize() returning iterator
    ✅ Real-time chunk generation with audio_int16_bytes
    ✅ Memory efficient - processes chunks as generated
    ✅ Low latency - can start playing audio before full synthesis
    
    COQUI TTS:
    ❌ No native streaming support in current API
    ✅ Can manually chunk output after full synthesis
    ✅ Can synthesize sentences separately for pseudo-streaming
    ❌ Higher memory usage - full audio generated before chunking
    ❌ Higher latency - full synthesis required before playback
    
    RECOMMENDATIONS:
    1. Keep Piper TTS for real-time streaming applications
    2. Use Coqui TTS for:
       - Better voice quality (if needed)
       - Voice cloning capabilities
       - Multi-language support
       - When real-time streaming is not critical
    
    POTENTIAL WORKAROUNDS for Coqui streaming:
    1. Sentence-by-sentence synthesis
    2. Manual audio chunking after synthesis
    3. Use faster Coqui models to reduce latency
    4. Pre-generate common responses
    """
    )


def demonstrate_websocket_integration():
    """
    Show how to integrate Coqui TTS with WebSocket (like current Piper implementation)
    """
    print("\n" + "=" * 60)
    print("WEBSOCKET INTEGRATION EXAMPLE")
    print("=" * 60)

    websocket_code = """
# For Coqui TTS WebSocket integration (pseudo-code):

@websocket_router.websocket("/ws/chat")
async def voicechat_endpoint_coqui(websocket: WebSocket):
    await websocket.accept()
    
    # Initialize TTS once (expensive operation)
    tts = TTS(model_name="tts_models/en/ljspeech/fast_pitch")
    
    while True:
        payload = await websocket.receive_json()
        messages = payload.get("messages", [])

        # ... OpenAI API call ...
        
        output_text = response.choices[0].message.content
        await websocket.send_text(output_text)

        # Option 1: Full synthesis then chunking
        wav = tts.tts(text=output_text)
        wav_bytes = np.array(wav * 32767, dtype=np.int16).tobytes()
        
        chunk_size = 4096
        for i in range(0, len(wav_bytes), chunk_size):
            chunk = wav_bytes[i:i + chunk_size]
            await websocket.send_bytes(chunk)
        
        # Option 2: Sentence-by-sentence synthesis
        sentences = output_text.split('. ')
        for sentence in sentences:
            if sentence.strip():
                wav = tts.tts(text=sentence.strip() + ".")
                wav_bytes = np.array(wav * 32767, dtype=np.int16).tobytes()
                await websocket.send_bytes(wav_bytes)
        
        await websocket.send_text(const.VOICE_STREAM_END)
"""

    print(websocket_code)


if __name__ == "__main__":
    print("Coqui TTS Streaming Capabilities Test")
    print("=" * 50)

    success = test_coqui_streaming()

    if success:
        compare_with_piper_approach()
        demonstrate_websocket_integration()
    else:
        print("Could not test Coqui TTS. Please check your installation.")
        print("\nTo install Coqui TTS:")
        print("pip install coqui-tts")
