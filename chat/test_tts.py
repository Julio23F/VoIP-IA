from elevenlabs.client import ElevenLabs
from elevenlabs import stream

client = ElevenLabs(
    api_key="sk_36e0cea917fcd892e5b90902b7ce226f2615b18e1196f2b0"
)

def parler(texte):
    audio_stream = client.text_to_speech.stream(
        text=texte,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
        optimize_streaming_latency=4,  # 0 à 4, plus c'est haut plus c'est rapide
    )
    stream(audio_stream)

# Test
parler("Vous recherchez une voix narrative pour un audiobook, une story ou tout autre projet audio, choisissez ma voix.")