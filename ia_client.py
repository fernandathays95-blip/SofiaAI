import socket
import json
from colorama import Fore, Style

# Carregar config
with open("server_api.json", "r", encoding="utf-8") as f:
    config = json.load(f)

HOST = "localhost"
PORT = config.get("porta", 5050)

print(Fore.CYAN + f"Conectando à IA {config['nome_ia']} na porta {PORT}..." + Style.RESET_ALL)
print("Digite 'sair' para encerrar.\n")

while True:
    msg = input(Fore.GREEN + "Você: " + Style.RESET_ALL)
    if not msg:
        continue

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.send(msg.encode("utf-8"))

    resposta = s.recv(4096).decode("utf-8")
    print(Fore.MAGENTA + f"{config['nome_ia']}: {resposta}" + Style.RESET_ALL)
    s.close()

    if msg.lower() == "sair":
        break
