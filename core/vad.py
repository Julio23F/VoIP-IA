import pyaudio
import numpy as np
from config.settings import SAMPLE_RATE, SILENCE_DURATION_MS

CHUNK_DURATION_MS = 30
ENERGY_THRESHOLD = 2000  # ajuste si nécessaire

def enregistrer_avec_vad() -> bytes:
    chunk_samples = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
    max_silence_chunks = int(SILENCE_DURATION_MS / CHUNK_DURATION_MS)

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=chunk_samples
    )

    frames = []
    silence_count = 0
    speaking = False

    print("🎤 En attente de voix...")

    try:
        while True:
            frame = stream.read(chunk_samples, exception_on_overflow=False)

            # Calculer énergie du chunk
            audio_np = np.frombuffer(frame, dtype=np.int16)
            energy = np.abs(audio_np).mean()

            is_speech = energy > ENERGY_THRESHOLD

            if is_speech:
                if not speaking:
                    print(f"🗣️  Parole détectée (énergie: {energy:.0f})")
                speaking = True
                silence_count = 0
                frames.append(frame)

            elif speaking:
                silence_count += 1
                frames.append(frame)

                if silence_count >= max_silence_chunks:
                    print("🔇 Fin de parole détectée")
                    break

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

    return b''.join(frames)