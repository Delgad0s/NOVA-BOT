import os
import openai
import json

# Cargar API Key directamente de variables de entorno
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Cargar memoria inicial
with open("nova_memoria.json", "r", encoding="utf-8") as f:
    contexto_nova = json.load(f)["contexto"]

def preguntar_a_nova(pregunta):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres NOVA, un analista macroeconómico profesional, preciso, frío, estratégico y directo."},
            {"role": "user", "content": contexto_nova + "\n\nUsuario: " + pregunta + "\n\nNOVA:"}
        ],
        temperature=0.2,
        max_tokens=800
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("Bienvenido a tu consola NOVA-JARVIS. Escribe 'salir' para terminar.\n")
    while True:
        pregunta = input("Tú: ")
        if pregunta.lower() in ["salir", "exit", "quit"]:
            break
        respuesta = preguntar_a_nova(pregunta)
        print("\nNOVA:", respuesta + "\n")
