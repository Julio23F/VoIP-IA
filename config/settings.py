# === CLÉS API ===
ELEVENLABS_API_KEY = ""
GROQ_API_KEY = ""

# === ELEVENLABS ===
VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
# TTS_MODEL = "eleven_turbo_v2_5"
TTS_MODEL = "eleven_multilingual_v2"
STT_MODEL = "scribe_v1"
OUTPUT_FORMAT = "mp3_44100_128"

# === GROQ ===
LLM_MODEL = "llama-3.1-8b-instant"
MAX_TOKENS = 150
TEMPERATURE = 0.7

# === AUDIO ===
SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 30         # durée chunk VAD en ms
SILENCE_DURATION_MS = 800      # silence avant fin de parole
VAD_AGGRESSIVENESS = 2         # 0 à 3 (3 = très agressif)

# === PROMPT SYSTÈME ===
SYSTEM_PROMPT = """Tu es un assistant vocal francophone.
Règles IMPORTANTES :
- Réponds en maximum 2-3 phrases courtes
- Pas de listes, pas de bullet points
- Pas de symboles spéciaux (*, #, -, etc.)
- Langage naturel et conversationnel
- Réponds UNIQUEMENT en français"""
