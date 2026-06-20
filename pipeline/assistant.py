from core.vad import enregistrer_avec_vad
from core.stt import transcrire
from core.llm import demander_groq_stream
from core.tts import parler
from config.settings import SAMPLE_RATE

MOTS_FIN = ["au revoir", "merci au revoir", "bye", "stop", "quitter", "terminer"]

def phrases_depuis_stream(token_generator):
    """
    Regroupe les tokens en phrases complètes
    et les retourne dès qu'une phrase est prête
    """
    buffer = ""
    for token in token_generator:
        buffer += token
        # Dès qu'on a une ponctuation forte → phrase complète
        if any(buffer.rstrip().endswith(p) for p in [".", "!", "?", "..."]):
            yield buffer.strip()
            buffer = ""
    # Reste éventuel sans ponctuation
    if buffer.strip():
        yield buffer.strip()

def run():
    """Boucle principale de l'assistant vocal"""
    print("🚀 Assistant vocal démarré\n")

    # Message d'accueil
    parler("Bonjour, je suis votre assistant vocal. Comment puis-je vous aider ?")

    while True:
        try:
            # 1. Enregistrer avec VAD
            audio_bytes = enregistrer_avec_vad()

            # 2. Transcrire
            texte_utilisateur = transcrire(audio_bytes, SAMPLE_RATE)

            if not texte_utilisateur:
                parler("Je n'ai pas bien entendu, pouvez-vous répéter ?")
                continue

            # 3. Vérifier fin de conversation
            if any(mot in texte_utilisateur.lower() for mot in MOTS_FIN):
                parler("Au revoir, bonne journée !")
                break

            # 4. LLM streaming → TTS phrase par phrase
            token_generator = demander_groq_stream(texte_utilisateur)

            for phrase in phrases_depuis_stream(token_generator):
                parler(phrase)  # joue chaque phrase dès qu'elle est prête

        except KeyboardInterrupt:
            print("\n👋 Arrêt demandé")
            parler("Au revoir !")
            break

        except Exception as e:
            print(f"❌ Erreur : {e}")
            continue