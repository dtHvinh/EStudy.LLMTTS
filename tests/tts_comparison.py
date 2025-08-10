"""
Performance comparison between Piper TTS and Coqui TTS
"""

import time
import numpy as np
from piper import PiperVoice
from TTS.api import TTS
import torch


def benchmark_piper_vs_coqui():
    """
    Compare performance and streaming capabilities
    """
    print("TTS Performance Comparison: Piper vs Coqui")
    print("=" * 60)

    test_texts = [
        "Hello, this is a short test.",
        "This is a medium length sentence that should take a bit more time to synthesize completely.",
        "This is a much longer text that we will use to test the performance and streaming capabilities of both TTS systems. It contains multiple sentences and should give us a good idea of how each system handles longer content generation and whether streaming provides any benefits.",
    ]

    # Initialize both systems
    print("Initializing TTS systems...")

    # Piper
    VOICE_PATH = (
        r"D:\dev\AI\Voices\en_US-hfc_female-medium\en_US-hfc_female-medium.onnx"
    )
    try:
        piper_voice = PiperVoice.load(VOICE_PATH)
        piper_available = True
        print("✅ Piper TTS loaded successfully")
    except Exception as e:
        print(f"❌ Piper TTS failed to load: {e}")
        piper_available = False

    # Coqui
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        coqui_tts = TTS(
            model_name="tts_models/en/ljspeech/fast_pitch", progress_bar=False
        ).to(device)
        coqui_available = True
        print(f"✅ Coqui TTS loaded successfully on {device}")
    except Exception as e:
        print(f"❌ Coqui TTS failed to load: {e}")
        coqui_available = False

    print("\n" + "=" * 60)

    for i, text in enumerate(test_texts, 1):
        print(f"\nTest {i}: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print(f"Text length: {len(text)} characters")
        print("-" * 40)

        # Test Piper TTS
        if piper_available:
            print("🎵 Piper TTS:")
            test_piper_performance(piper_voice, text)

        # Test Coqui TTS
        if coqui_available:
            print("🎵 Coqui TTS:")
            test_coqui_performance(coqui_tts, text)

        print()


def test_piper_performance(voice, text):
    """Test Piper TTS performance and streaming"""
    try:
        # Measure synthesis time
        start_time = time.time()
        tts_gen = voice.synthesize(text)

        chunks = []
        chunk_count = 0
        first_chunk_time = None

        for chunk in tts_gen:
            if first_chunk_time is None:
                first_chunk_time = time.time() - start_time
            chunks.append(chunk.audio_int16_bytes)
            chunk_count += 1

        total_time = time.time() - start_time

        # Calculate total audio length
        total_audio_bytes = sum(len(chunk) for chunk in chunks)
        total_audio_samples = total_audio_bytes // 2  # int16 = 2 bytes per sample
        audio_duration = total_audio_samples / 22050  # Piper typically uses 22050 Hz

        print(f"  ⏱️  First chunk: {first_chunk_time:.3f}s")
        print(f"  ⏱️  Total time: {total_time:.3f}s")
        print(f"  🔊 Audio duration: {audio_duration:.3f}s")
        print(f"  📊 Real-time factor: {total_time/audio_duration:.2f}x")
        print(f"  📦 Chunks generated: {chunk_count}")
        print(f"  💾 Total audio bytes: {total_audio_bytes:,}")
        print(f"  ✨ Streaming: Yes (native)")

    except Exception as e:
        print(f"  ❌ Error: {e}")


def test_coqui_performance(tts, text):
    """Test Coqui TTS performance"""
    try:
        # Measure synthesis time
        start_time = time.time()
        wav = tts.tts(text=text)
        synthesis_time = time.time() - start_time

        # Convert to audio info
        wav_array = np.array(wav)
        audio_duration = len(wav_array) / tts.synthesizer.output_sample_rate

        # Simulate chunking
        wav_int16 = np.clip(wav_array * 32767, -32768, 32767).astype(np.int16)
        wav_bytes = wav_int16.tobytes()

        chunk_size = 4096
        chunk_count = len(wav_bytes) // chunk_size + (
            1 if len(wav_bytes) % chunk_size else 0
        )

        print(f"  ⏱️  First chunk: {synthesis_time:.3f}s (full synthesis required)")
        print(f"  ⏱️  Total time: {synthesis_time:.3f}s")
        print(f"  🔊 Audio duration: {audio_duration:.3f}s")
        print(f"  📊 Real-time factor: {synthesis_time/audio_duration:.2f}x")
        print(f"  📦 Chunks after synthesis: {chunk_count}")
        print(f"  💾 Total audio bytes: {len(wav_bytes):,}")
        print(f"  ✨ Streaming: No (post-synthesis chunking)")

        # Test sentence-by-sentence approach
        sentences = text.split(". ")
        if len(sentences) > 1:
            start_time = time.time()
            first_sentence_time = None
            total_sentence_duration = 0

            for sentence in sentences:
                if sentence.strip():
                    sentence_start = time.time()
                    sentence_wav = tts.tts(text=sentence.strip() + ".")
                    sentence_time = time.time() - sentence_start

                    if first_sentence_time is None:
                        first_sentence_time = sentence_time

                    sentence_duration = (
                        len(np.array(sentence_wav)) / tts.synthesizer.output_sample_rate
                    )
                    total_sentence_duration += sentence_duration

            total_sentence_time = time.time() - start_time

            print(f"  📝 Sentence-by-sentence approach:")
            print(f"     ⏱️  First sentence: {first_sentence_time:.3f}s")
            print(f"     ⏱️  Total time: {total_sentence_time:.3f}s")
            print(f"     📊 RTF: {total_sentence_time/total_sentence_duration:.2f}x")

    except Exception as e:
        print(f"  ❌ Error: {e}")


def streaming_latency_analysis():
    """
    Analyze the latency implications of each approach
    """
    print("\n" + "=" * 60)
    print("STREAMING LATENCY ANALYSIS")
    print("=" * 60)

    analysis = """
    📊 LATENCY COMPARISON:
    
    Piper TTS (Streaming):
    ✅ Time to first audio: ~0.1-0.5 seconds
    ✅ Progressive audio delivery during synthesis
    ✅ Can start playback immediately when first chunk arrives
    ✅ Memory efficient (processes chunks as generated)
    ✅ Better user experience for long texts
    
    Coqui TTS (Traditional):
    ❌ Time to first audio: Full synthesis time (1-10+ seconds)
    ❌ All audio generated before any can be played
    ❌ Higher memory usage (full audio in memory)
    ❌ Poor user experience for long texts
    
    Coqui TTS (Sentence-by-sentence):
    🟡 Time to first audio: First sentence synthesis time
    🟡 Progressive delivery by sentences
    🟡 Better than full synthesis, worse than Piper
    🟡 Multiple model inference calls (slower overall)
    
    📈 RECOMMENDATIONS:
    
    1. Use Piper TTS for:
       - Real-time applications
       - Voice assistants
       - Interactive chat systems
       - Long-form content
    
    2. Use Coqui TTS for:
       - High-quality voice generation
       - Voice cloning/customization
       - Batch processing
       - When latency is not critical
       - Multi-language support
    
    3. Hybrid approach:
       - Use Piper for real-time responses
       - Use Coqui for high-quality offline generation
       - Pre-generate common responses with Coqui
    """

    print(analysis)


if __name__ == "__main__":
    benchmark_piper_vs_coqui()
    streaming_latency_analysis()
