from flask import Flask, render_template, request, jsonify
import json
import os
import random

# --- Funções de arquivo ---

def carregar_json(caminho):
    if os.path.exists(caminho):
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def carregar_palavras(arquivo):
    palavras = {}
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            for linha in f:
                if ":" in linha:
                    termo, info = linha.strip().split(":", 1)
                    palavras[termo.strip().lower()] = info.strip()
    return palavras

def carregar_memoria(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_memoria(memoria, arquivo):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

# --- Funções de IA ---

def detectar_tipo(info):
    info = info.lower()
    if "verbo" in info: return "verbo"
    if "substantivo" in info: return "substantivo"
    if "adjetivo" in info: return "adjetivo"
    return "outro"

def gerar_resposta(frase, palavras, memoria, config):
    entrada = frase.lower().split()
    conhecidas = []
    desconhecidas = []

    for p in entrada:
        if p in palavras:
            conhecidas.append((p, palavras[p]))
        elif p in memoria:
            conhecidas.append((p, memoria[p]))
        else:
            desconhecidas.append(p)

    if not conhecidas:
        return "Não conheço essas palavras. Quer me ensinar o que significam?"

    termos = [k for k, _ in conhecidas]
    tipos = [detectar_tipo(v) for _, v in conhecidas]
    resposta = ""

    if "verbo" in tipos:
        v = termos[tipos.index("verbo")]
        resposta = random.choice([
            f"Você gosta de {v}?",
            f"Eu também sei {v}, mas de outro jeito.",
            f"Interessante falar sobre {v}."
        ])
    elif "substantivo" in tipos:
        s = termos[tipos.index("substantivo")]
        resposta = random.choice([
            f"Gosto de falar sobre {s}.",
            f"{s} é algo interessante.",
            f"Você tem um {s}?"
        ])
    elif "adjetivo" in tipos:
        a = termos[tipos.index("adjetivo")]
        resposta = random.choice([
            f"É bom ser {a}.",
            f"Por que você se sente {a}?",
            f"Conheço pessoas que são muito {a}."
        ])
    else:
        resposta = random.choice([
            "Gostei do que você disse.",
            "Interessante o seu comentário.",
            "Faz sentido o que você falou."
        ])

    if desconhecidas and config.get("modo_aprendizado"):
        resposta += f" (Não conheço: {', '.join(desconhecidas)})"

    return resposta

# --- Flask Web ---

app = Flask(__name__)

config = carregar_json("server_api.json")
palavras = carregar_palavras(config["arquivo_palavras"])
memoria = carregar_memoria(config["arquivo_memoria"])

@app.route("/")
def index():
    return render_template("chat.html", nome_ia=config["nome_ia"])

@app.route("/mensagem", methods=["POST"])
def mensagem():
    global memoria
    dados = request.get_json()
    texto = dados.get("texto", "")
    resposta = gerar_resposta(texto, palavras, memoria, config)
    return jsonify({"resposta": resposta})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=config.get("porta", 8080))
