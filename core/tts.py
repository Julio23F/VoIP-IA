from elevenlabs.client import ElevenLabs
from elevenlabs import stream
from config.settings import (
    ELEVENLABS_API_KEY,
    VOICE_ID,
    TTS_MODEL,
    OUTPUT_FORMAT
)

client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def parler(texte: str):
    """
    Synthétise le texte en audio et joue immédiatement
    via streaming ElevenLabs
    """
    if not texte.strip():
        return

    print(f"🤖 Assistant : {texte}")

    try:
        audio_stream = client.text_to_speech.stream(
            text=texte,
            voice_id=VOICE_ID,
            model_id=TTS_MODEL,
            output_format=OUTPUT_FORMAT,
            optimize_streaming_latency=4,
        )
        stream(audio_stream)

    except Exception as e:
        print(f"❌ Erreur TTS : {e}")