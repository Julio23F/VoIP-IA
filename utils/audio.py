import io
import wave
import numpy as np

def numpy_vers_wav_bytes(audio: np.ndarray, sample_rate: int) -> io.BytesIO:
    """Convertit un tableau numpy en bytes WAV"""
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # int16 = 2 bytes
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    buffer.seek(0)
    return buffer

def bytes_vers_wav_bytes(raw_bytes: bytes, sample_rate: int) -> io.BytesIO:
    """Convertit des bytes bruts en bytes WAV"""
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(raw_bytes)
    buffer.seek(0)
    return buffer

def sauvegarder_wav(audio_bytes: bytes, sample_rate: int, fichier: str):
    """Sauvegarde en fichier WAV pour debug"""
    with wave.open(fichier, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_bytes)
    print(f"💾 Sauvegardé : {fichier}")