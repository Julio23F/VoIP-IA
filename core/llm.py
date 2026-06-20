import json
import requests
from config.settings import GROQ_API_KEY, LLM_MODEL, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT

# Historique de conversation
conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def demander_groq_stream(texte: str):
    """
    Envoie le texte à Groq et retourne les tokens
    au fur et à mesure (générateur)
    """
    conversation.append({"role": "user", "content": texte})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": LLM_MODEL,
            "messages": conversation,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": True
        },
        stream=True
    )

    reponse_complete = ""

    for line in response.iter_lines():
        if line and line != b"data: [DONE]":
            data = line.decode().replace("data: ", "")
            try:
                token = json.loads(data)["choices"][0]["delta"].get("content", "")
                if token:
                    reponse_complete += token
                    yield token  # on retourne token par token
            except Exception:
                pass

    # Sauvegarder dans l'historique
    conversation.append({
        "role": "assistant",
        "content": reponse_complete
    })

def reset_conversation():
    """Remet la conversation à zéro"""
    global conversation
    conversation = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]