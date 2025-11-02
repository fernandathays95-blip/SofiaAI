import json
import os
import random
import socket

# --- Leitura de arquivos ---

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

    resposta = ""
    termos = [k for k, _ in conhecidas]
    tipos = [detectar_tipo(v) for _, v in conhecidas]

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

# --- Funções de memória ---

def carregar_memoria(arquivo):
    if os.path.exists(arquivo):
        with open(arquivo, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_memoria(memoria, arquivo):
    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

def aprender_palavra(memoria, arquivo):
    termo = input("Nova palavra: ").strip().lower()
    significado = input(f"O que significa '{termo}'? ").strip()
    memoria[termo] = significado
    salvar_memoria(memoria, arquivo)
    print(f"✅ Aprendi '{termo}' = {significado}")

# --- Servidor Local ---

def iniciar_servidor():
    config = carregar_json("server_api.json")
    palavras = carregar_palavras(config["arquivo_palavras"])
    memoria = carregar_memoria(config["arquivo_memoria"])
    porta = config.get("porta", 5050)

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind(("localhost", porta))
    servidor.listen(1)
    print(f"🤖 {config['nome_ia']} ouvindo na porta {porta}...")

    while True:
        conn, addr = servidor.accept()
        data = conn.recv(4096).decode("utf-8").strip()
        if not data:
            conn.close()
            continue

        if data == "sair":
            conn.send("IA: Até logo!".encode("utf-8"))
            conn.close()
            break

        resposta = gerar_resposta(data, palavras, memoria, config)
        conn.send(resposta.encode("utf-8"))
        conn.close()

if __name__ == "__main__":
    iniciar_servidor()
