import json
import os
import random
from colorama import Fore, Style

ARQ_PALAVRAS = "all_names.txt"
ARQ_MEMORIA = "memoria.json"

# --- FUNÇÕES DE ARQUIVO ---

def carregar_palavras():
    palavras = {}
    if os.path.exists(ARQ_PALAVRAS):
        with open(ARQ_PALAVRAS, "r", encoding="utf-8") as f:
            for linha in f:
                if ":" in linha:
                    termo, info = linha.strip().split(":", 1)
                    palavras[termo.strip().lower()] = info.strip()
    return palavras

def carregar_memoria():
    if os.path.exists(ARQ_MEMORIA):
        with open(ARQ_MEMORIA, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def salvar_memoria(memoria):
    with open(ARQ_MEMORIA, "w", encoding="utf-8") as f:
        json.dump(memoria, f, ensure_ascii=False, indent=2)

# --- FUNÇÕES DE LÓGICA ---

def detectar_tipo(info):
    info = info.lower()
    if "verbo" in info: return "verbo"
    if "substantivo" in info: return "substantivo"
    if "adjetivo" in info: return "adjetivo"
    return "outro"

def gerar_resposta(frase, palavras, memoria):
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

    # Se não conhece nada, pede pra ensinar
    if not conhecidas:
        return "Não conheço essas palavras. Quer me ensinar o que significam?"

    # Montar frases naturais
    resposta = ""
    termos = [k for k, _ in conhecidas]
    tipos = [detectar_tipo(v) for _, v in conhecidas]

    if "verbo" in tipos:
        verbo = termos[tipos.index("verbo")]
        resposta = random.choice([
            f"Você gosta de {verbo}?",
            f"Eu também sei {verbo}, mas de outro jeito.",
            f"Interessante falar sobre {verbo}."
        ])
    elif "substantivo" in tipos:
        sub = termos[tipos.index("substantivo")]
        resposta = random.choice([
            f"Gosto de falar sobre {sub}.",
            f"{sub} é algo interessante.",
            f"Você tem um {sub}?"
        ])
    elif "adjetivo" in tipos:
        adj = termos[tipos.index("adjetivo")]
        resposta = random.choice([
            f"É bom ser {adj}.",
            f"Por que você se sente {adj}?",
            f"Conheço pessoas que são muito {adj}."
        ])
    else:
        resposta = random.choice([
            f"Gostei do que você disse.",
            f"Interessante o seu comentário.",
            f"Faz sentido o que você falou."
        ])

    if desconhecidas:
        resposta += f" (Não conheço as palavras: {', '.join(desconhecidas)})"

    return resposta

def aprender(memoria):
    termo = input("Digite a nova palavra: ").strip().lower()
    significado = input(f"O que significa '{termo}'? ").strip()
    memoria[termo] = significado
    salvar_memoria(memoria)
    print(Fore.YELLOW + f"Aprendi que '{termo}' significa: {significado}" + Style.RESET_ALL)

# --- PROGRAMA PRINCIPAL ---

def main():
    print(Fore.CYAN + "🤖 IA Offline em Português — modo conversa natural" + Style.RESET_ALL)
    print("Diga algo! (ou digite 'ensinar' para me ensinar, 'sair' para encerrar)\n")

    palavras = carregar_palavras()
    memoria = carregar_memoria()

    while True:
        frase = input(Fore.GREEN + "Você: " + Style.RESET_ALL)
        if frase.lower() == "sair":
            print(Fore.CYAN + "IA: Até logo!" + Style.RESET_ALL)
            break
        elif frase.lower() == "ensinar":
            aprender(memoria)
        else:
            resposta = gerar_resposta(frase, palavras, memoria)
            print(Fore.MAGENTA + "IA: " + resposta + Style.RESET_ALL)

if __name__ == "__main__":
    main()
