import pyaudio
import numpy as np

SAMPLE_RATE = 16000
CHUNK = 480

p = pyaudio.PyAudio()
stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    frames_per_buffer=CHUNK
)

print("🎤 Parle pour voir ton niveau d'énergie (Ctrl+C pour arrêter)")

try:
    while True:
        frame = stream.read(CHUNK, exception_on_overflow=False)
        audio_np = np.frombuffer(frame, dtype=np.int16)
        energy = np.abs(audio_np).mean()
        barre = "█" * int(energy / 50)
        print(f"\rÉnergie: {energy:6.0f} {barre[:40]}", end="", flush=True)
except KeyboardInterrupt:
    pass
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()