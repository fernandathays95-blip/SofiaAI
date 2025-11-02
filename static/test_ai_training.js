/**
 * test_ai_training.js
 * Script de teste e treino automático da IA offline
 * Conecta no endpoint /mensagem do Flask
 */

const frasesDeTreino = [
  "oi",
  "gosto de andar",
  "computador",
  "estou feliz",
  "triste",
  "casa",
  "adoro programar",
  "você é legal",
  "ensinar",
  "adeus"
];

let indice = 0;

// Função para enviar uma mensagem
async function enviarMensagem(texto) {
  const resposta = await fetch("/mensagem", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({texto})
  });

  const dados = await resposta.json();
  console.log(`👤 ${texto}`);
  console.log(`🤖 ${dados.resposta}\n`);
}

// Executa automaticamente o teste
async function iniciarTreino() {
  console.log("=== Iniciando teste de treinamento da IA ===");
  for (const frase of frasesDeTreino) {
    await enviarMensagem(frase);
    await new Promise(r => setTimeout(r, 500)); // aguarda meio segundo entre mensagens
  }
  console.log("=== Teste finalizado ===");
}

// Inicia automaticamente ao carregar o script
window.addEventListener("load", iniciarTreino);
