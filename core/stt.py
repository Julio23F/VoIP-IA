from elevenlabs.client import ElevenLabs
from config.settings import ELEVENLABS_API_KEY, STT_MODEL
from utils.audio import bytes_vers_wav_bytes

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def transcrire(audio_bytes: bytes, sample_rate: int) -> str:
    """
    Transcrit l'audio en texte via ElevenLabs STT
    """
    print("📝 Transcription en cours...")

    wav_buffer = bytes_vers_wav_bytes(audio_bytes, sample_rate)

    try:
        result = client.speech_to_text.convert(
            file=("audio.wav", wav_buffer, "audio/wav"),
            model_id=STT_MODEL,
            language_code="fr"
        )
        texte = result.text.strip()
        print(f"👤 Transcrit : {texte}")
        return texte

    except Exception as e:
        print(f"❌ Erreur STT : {e}")
        return ""