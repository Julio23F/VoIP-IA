# 🎙️ Assistant Vocal IA — VoIP + ElevenLabs + Groq

Assistant vocal intelligent capable de comprendre la parole, raisonner et répondre
naturellement en français, avec une latence optimisée grâce au streaming.

---

## Architecture du pipeline

```
Micro
  ↓
VAD (détection fin de parole)
  ↓
ElevenLabs STT (transcription)
  ↓
Groq LLM — llama-3.1-8b-instant (streaming token par token)
  ↓
ElevenLabs TTS — turbo (streaming phrase par phrase)
  ↓
Haut-parleur
```

---

## Stack technique

| Brique | Service | Rôle |
|--------|---------|------|
| Détection parole | VAD énergie | Arrêt automatique à la fin de la phrase |
| Transcription | ElevenLabs Scribe v1 | Voix → Texte (STT) |
| Intelligence | Groq `llama-3.1-8b-instant` | Génération de réponse |
| Synthèse vocale | ElevenLabs `eleven_turbo_v2_5` | Texte → Voix naturelle |

---

## Fonctionnalités

- 🎤 Détection automatique de fin de parole sans durée fixe
- 🌊 Streaming Groq + TTS pour une latence minimale (~500-700ms)
- 🇫🇷 Entièrement en français
- 💬 Historique de conversation maintenu entre les échanges
- 💰 100% gratuit via quotas API
- 🧪 Mode texte pour tester Groq sans micro

---

## Structure du projet

```
VoIP/
│
├── config/
│   └── settings.py
│
├── core/
│   ├── vad.py
│   ├── stt.py
│   ├── llm.py
│   └── tts.py
│
├── pipeline/
│   └── assistant.py
│
├── utils/
│   └── audio.py
│
├── env/                    # environnement virtuel Python (non versionné)
│
├── main.py
├── test_chat.py
├── requirements.txt
└── README.md
```

---

## Description de chaque fichier

### `main.py`
Point d'entrée du projet.
Lance simplement la boucle principale de l'assistant vocal.

```python
from pipeline.assistant import run

if __name__ == "__main__":
    run()
```

---

### `config/settings.py`
Centralise toutes les configurations du projet :
- Clés API (ElevenLabs, Groq)
- Paramètres audio (sample rate, durée silence, seuil énergie)
- Paramètres LLM (modèle, max tokens, température)
- Prompt système de l'assistant

---

### `core/vad.py`
**Voice Activity Detection** — Détection de fin de parole.

- Écoute en continu le microphone chunk par chunk (30ms)
- Calcule l'énergie du signal audio à chaque chunk
- Démarre l'enregistrement dès que la voix est détectée
- S'arrête automatiquement après 800ms de silence
- Retourne les bytes audio bruts prêts pour la transcription

> Remplace un enregistrement à durée fixe (ex: 5 secondes) par
> une détection intelligente — gain majeur sur la latence ressentie.

---

### `core/stt.py`
**Speech To Text** — Transcription via ElevenLabs.

- Reçoit les bytes audio bruts depuis `vad.py`
- Les convertit en format WAV via `utils/audio.py`
- Envoie au modèle `scribe_v1` d'ElevenLabs avec `language_code="fr"`
- Retourne le texte transcrit

---

### `core/llm.py`
**Large Language Model** — Cerveau de l'assistant via Groq.

- Maintient l'historique complet de la conversation
- Envoie le texte transcrit à `llama-3.1-8b-instant` sur Groq
- Utilise le **streaming** : retourne les tokens un par un via un générateur
- Sauvegarde la réponse complète dans l'historique après génération
- Expose `reset_conversation()` pour remettre à zéro si besoin

---

### `core/tts.py`
**Text To Speech** — Synthèse vocale via ElevenLabs.

- Reçoit un texte (phrase courte) et le synthétise immédiatement
- Utilise le modèle `eleven_turbo_v2_5` pour une latence minimale
- Active `optimize_streaming_latency=4` pour jouer l'audio
  sans attendre la génération complète
- Joue l'audio directement sur le haut-parleur via `stream()`

---

### `pipeline/assistant.py`
**Orchestrateur principal** — Assemble toutes les briques.

Boucle principale :
1. `vad.py` → écoute et détecte la fin de parole
2. `stt.py` → transcrit l'audio en texte
3. Vérifie les mots de fin (`au revoir`, `stop`, etc.)
4. `llm.py` → génère la réponse en streaming token par token
5. `phrases_depuis_stream()` → regroupe les tokens en phrases complètes
6. `tts.py` → joue chaque phrase dès qu'elle est prête

> Le streaming LLM → TTS phrase par phrase est le cœur
> de l'optimisation latence : on commence à parler avant
> que Groq ait fini de générer la réponse complète.

---

### `utils/audio.py`
Utilitaires de conversion audio.

- `numpy_vers_wav_bytes()` : convertit un tableau numpy en buffer WAV
- `bytes_vers_wav_bytes()` : convertit des bytes bruts en buffer WAV
- `sauvegarder_wav()` : sauvegarde un fichier WAV sur disque (debug)

---

### `test_chat.py`
**Mode texte** — Permet de tester Groq sans micro ni audio.

- Chat en terminal avec l'assistant
- Conserve l'historique de conversation
- Utilise les mêmes paramètres que l'assistant vocal
- Utile pour valider le prompt et les réponses du LLM

---

## Installation

```bash
# Cloner le projet
git clone https://github.com/ton-user/voip-ai-assistant.git
cd voip-ai-assistant

# Créer l'environnement virtuel
python3 -m venv env
source env/bin/activate

# Dépendances système
sudo apt install portaudio19-dev -y

# Dépendances Python
pip3 install -r requirements.txt
```

---

## Configuration

Dans `config/settings.py`, renseigne tes clés API :

```python
ELEVENLABS_API_KEY = "ta_clé_elevenlabs"
GROQ_API_KEY       = "ta_clé_groq"
```

---

## Utilisation

```bash
# Activer l'environnement virtuel
source env/bin/activate

# Lancer l'assistant vocal
python3 main.py

# Tester le LLM en mode texte
python3 test_chat.py
```

---

## Prérequis

- Python 3.10+
- Microphone fonctionnel
- Compte gratuit [ElevenLabs](https://elevenlabs.io)
- Compte gratuit [Groq](https://groq.com)