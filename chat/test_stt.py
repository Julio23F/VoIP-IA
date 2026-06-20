# import sounddevice as sd
# import numpy as np
# import io
# import wave
# from elevenlabs.client import ElevenLabs

# client = ElevenLabs(api_key="sk_36e0cea917fcd892e5b90902b7ce226f2615b18e1196f2b0")

# def enregistrer_voix(duree=5, sample_rate=16000):
#     """Enregistre la voix pendant duree secondes"""
#     print("🎤 Parlez...")
#     audio = sd.rec(
#         int(duree * sample_rate),
#         samplerate=sample_rate,
#         channels=1,
#         dtype=np.int16
#     )
#     sd.wait()
#     print("✅ Enregistrement terminé")
#     return audio, sample_rate

# def audio_vers_wav_bytes(audio, sample_rate):
#     """Convertit l'audio numpy en bytes WAV"""
#     buffer = io.BytesIO()
#     with wave.open(buffer, 'wb') as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(2)
#         wf.setframerate(sample_rate)
#         wf.writeframes(audio.tobytes())
#     buffer.seek(0)
#     return buffer

# def transcrire(audio, sample_rate):
#     """Transcrit l'audio en texte via ElevenLabs"""
#     wav_bytes = audio_vers_wav_bytes(audio, sample_rate)
#     result = client.speech_to_text.convert(
#         file=("audio.wav", wav_bytes, "audio/wav"),
#         model_id="scribe_v1",
#         language_code="fr"
#     )
#     return result.text


# /********************** ///////// **********************/

# import sounddevice as sd
# import numpy as np
# import wave
# import io

# def enregistrer_voix(duree=5, sample_rate=16000):
#     print("🎤 Parlez maintenant...")
#     audio = sd.rec(
#         int(duree * sample_rate),
#         samplerate=sample_rate,
#         channels=1,
#         dtype=np.int16
#     )
#     sd.wait()
#     print("✅ Enregistrement terminé")
#     return audio, sample_rate

# def sauvegarder_wav(audio, sample_rate, fichier="test_micro.wav"):
#     with wave.open(fichier, 'wb') as wf:
#         wf.setnchannels(1)
#         wf.setsampwidth(2)
#         wf.setframerate(sample_rate)
#         wf.writeframes(audio.tobytes())
#     print(f"✅ Fichier sauvegardé : {fichier}")

# # Test
# audio, sample_rate = enregistrer_voix(duree=5)
# sauvegarder_wav(audio, sample_rate)


# /********************** ///////// **********************/
from elevenlabs.client import ElevenLabs

elevenlabs = ElevenLabs(
    api_key="sk_36e0cea917fcd892e5b90902b7ce226f2615b18e1196f2b0"
)

with open("./voice_preview_nicolas.mp3", "rb") as audio_file:
    transcription = elevenlabs.speech_to_text.convert(
        file=audio_file,
        model_id="scribe_v1",
        tag_audio_events=True,
        language_code="fr",
        diarize=True
    )

print(transcription.text)