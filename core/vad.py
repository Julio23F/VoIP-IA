import pyaudio
import webrtcvad
from config.settings import (
    SAMPLE_RATE,
    CHUNK_DURATION_MS,
    SILENCE_DURATION_MS,
    VAD_AGGRESSIVENESS
)

def enregistrer_avec_vad() -> bytes:
    """
    Enregistre la voix et s'arrête automatiquement
    après SILENCE_DURATION_MS ms de silence
    """
    vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

    # Taille d'un chunk en samples
    chunk_samples = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)
    chunk_bytes = chunk_samples * 2  # int16 = 2 bytes

    # Nombre de chunks silence avant d'arrêter
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

            # Vérifier si c'est de la voix
            try:
                is_speech = vad.is_speech(frame, SAMPLE_RATE)
            except Exception:
                is_speech = False

            if is_speech:
                if not speaking:
                    print("🗣️  Parole détectée...")
                speaking = True
                silence_count = 0
                frames.append(frame)

            elif speaking:
                # On est en train de parler mais silence détecté
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