/* DilsAI config: expõe ASK_URL global ANTES do script principal */
window.API_BASE = "http://127.0.0.1:8000";
window.ASK_URL  = window.API_BASE + "/ask";
console.log("[DilsAI] CONFIG ASK_URL =", window.ASK_URL);
