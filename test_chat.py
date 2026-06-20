import requests
from config.settings import GROQ_API_KEY, LLM_MODEL, MAX_TOKENS, TEMPERATURE, SYSTEM_PROMPT

conversation = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

def demander_groq(texte: str) -> str:
    conversation.append({"role": "user", "content": texte})

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": LLM_MODEL,
            "messages": conversation,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": False
        }
    )

    reponse = response.json()["choices"][0]["message"]["content"]
    conversation.append({"role": "assistant", "content": reponse})
    return reponse

def main():
    print("💬 Chat avec Groq (tape 'quit' pour quitter)\n")
    print("=" * 50)

    while True:
        texte = input("\n👤 Toi : ").strip()

        if not texte:
            continue

        if texte.lower() in ["quit", "exit", "quitter", "bye"]:
            print("👋 Au revoir !")
            break

        reponse = demander_groq(texte)
        print(f"\n🤖 Groq : {reponse}")

if __name__ == "__main__":
    main()