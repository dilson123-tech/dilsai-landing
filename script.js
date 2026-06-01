console.log("[DilsAI Estudos] script carregado");

// ===== Ambiente / API =====
const DILSAI_IS_LOCAL =
  location.hostname === "127.0.0.1" ||
  location.hostname === "localhost";

const DILSAI_PROD_API =
  window.DILSAI_API_BASE ||
  window.API_BASE ||
  "https://dilsai-api.onrender.com";

window.API_BASE = DILSAI_IS_LOCAL
  ? "http://127.0.0.1:8091"
  : DILSAI_PROD_API;

window.ASK_URL = `${window.API_BASE}/api/v1/chat`;

console.log("[DilsAI Estudos] Ambiente:", DILSAI_IS_LOCAL ? "LOCAL" : "PRODUÇÃO");
console.log("[DilsAI Estudos] Endpoint:", window.ASK_URL);

// ===== Rodapé =====
const yearEl = document.getElementById("year");
if (yearEl) {
  yearEl.textContent = new Date().getFullYear();
}

// ===== Opções oficiais do backend =====
const DILSAI_LEVELS = [
  { value: "geral", label: "Geral" },
  { value: "fundamental_1", label: "Ensino Fundamental I" },
  { value: "fundamental_2", label: "Ensino Fundamental II" },
  { value: "ensino_medio", label: "Ensino Médio" },
  { value: "tecnico", label: "Curso Técnico" },
  { value: "concurso", label: "Concurso" },
  { value: "universidade", label: "Universidade" },
];

const DILSAI_TOPICS = [
  { value: "geral", label: "Geral" },
  { value: "matematica_logica", label: "Matemática e lógica" },
  { value: "portugues", label: "Português" },
  { value: "redacao", label: "Redação" },
  { value: "programacao", label: "Programação" },
  { value: "informatica", label: "Informática" },
  { value: "direito", label: "Direito" },
  { value: "administracao", label: "Administração" },
  { value: "fisica", label: "Física" },
  { value: "quimica", label: "Química" },
  { value: "biologia", label: "Biologia" },
  { value: "historia", label: "História" },
  { value: "geografia", label: "Geografia" },
  { value: "ingles", label: "Inglês" },
  { value: "filosofia", label: "Filosofia" },
  { value: "sociologia", label: "Sociologia" },
  { value: "engenharia", label: "Engenharia" },
  { value: "saude", label: "Saúde" },
  { value: "humanas", label: "Humanas" },
  { value: "negocios", label: "Negócios" },
];

const DILSAI_MODES = [
  { value: "professor", label: "Modo Professor" },
  { value: "direto", label: "Direto" },
  { value: "resumo", label: "Resumo" },
  { value: "passo_a_passo", label: "Passo a passo" },
  { value: "revisao", label: "Revisão" },
  { value: "simulado", label: "Simulado" },
  { value: "fonte_segura", label: "Fonte segura" },
];

function escapeHtml(value) {
  return String(value || "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function nl2br(value) {
  return escapeHtml(value).replace(/\n/g, "<br>");
}

function getOptionHtml(options) {
  return options
    .map((item) => `<option value="${item.value}">${escapeHtml(item.label)}</option>`)
    .join("");
}

function populateSelectOptions(selectId, options, defaultValue = "geral") {
  const select = document.getElementById(selectId);
  if (!select) return;

  const currentValue = select.value || defaultValue;
  select.innerHTML = getOptionHtml(options);

  const hasCurrentValue = options.some((item) => item.value === currentValue);
  select.value = hasCurrentValue ? currentValue : defaultValue;
}

function populateFullStudyTaxonomyOptions() {
  populateSelectOptions("dilsai-full-level", DILSAI_LEVELS, "geral");
  populateSelectOptions("dilsai-full-topic", DILSAI_TOPICS, "geral");
  populateSelectOptions("dilsai-full-mode", DILSAI_MODES, "professor");
}


function normalizeDilsAILevel(level) {
  const normalized = String(level || "geral").trim();

  const levelMap = {
    geral: "geral",
    fundamental_1: "fundamental_1",
    fundamental_i: "fundamental_1",
    fundamental_2: "fundamental_2",
    fundamental_ii: "fundamental_2",
    ensino_medio: "ensino_medio",
    medio: "ensino_medio",
    médio: "ensino_medio",
    tecnico: "tecnico",
    técnico: "tecnico",
    concurso: "concurso",
    universidade: "universidade",
  };

  return levelMap[normalized] || "geral";
}

function normalizeDilsAITopic(topic) {
  const normalized = String(topic || "geral").trim();

  const topicMap = {
    geral: "geral",
    matematica: "matematica_logica",
    matemática: "matematica_logica",
    matematica_logica: "matematica_logica",
    portugues: "portugues",
    português: "portugues",
    redacao: "redacao",
    redação: "redacao",
    programacao: "programacao",
    programação: "programacao",
    informatica: "informatica",
    informática: "informatica",
    direito: "direito",
    administracao: "administracao",
    administração: "administracao",
    fisica: "fisica",
    física: "fisica",
    quimica: "quimica",
    química: "quimica",
    biologia: "biologia",
    historia: "historia",
    história: "historia",
    geografia: "geografia",
    ingles: "ingles",
    inglês: "ingles",
    filosofia: "filosofia",
    sociologia: "sociologia",
    engenharia: "engenharia",
    saude: "saude",
    saúde: "saude",
    humanas: "humanas",
    negocios: "negocios",
    negócios: "negocios",
  };

  return topicMap[normalized] || "geral";
}

function normalizeDilsAIMode(mode) {
  const normalized = String(mode || "professor").trim();

  const modeMap = {
    direto: "direto",
    professor: "professor",
    resumo: "resumo",
    passo_a_passo: "passo_a_passo",
    revisao: "revisao",
    revisão: "revisao",
    simulado: "simulado",
    fonte_segura: "fonte_segura",
  };

  return modeMap[normalized] || "professor";
}


async function askDilsAI({ message, userName, level, topic, mode, context }) {
  const payload = {
    user_name: userName || "Aluno",
    message,
    level: normalizeDilsAILevel(level || "geral"),
    topic: normalizeDilsAITopic(topic || "geral"),
    mode: normalizeDilsAIMode(mode || "professor"),
  };

  if (context && context.trim()) {
    payload.context = context.trim();
  }

  const response = await fetch(window.ASK_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    const text = await response.text().catch(() => "");
    throw new Error(`API ${response.status}${text ? ` — ${text.slice(0, 160)}` : ""}`);
  }

  return response.json();
}

function ensureChatShell() {
  let chat = document.getElementById("dilsai-chatbox");

  if (!chat) {
    chat = document.createElement("div");
    chat.id = "dilsai-chatbox";
    document.body.appendChild(chat);
  }

  chat.style.display = chat.style.display || "none";
  chat.style.position = "fixed";
  chat.style.right = "20px";
  chat.style.bottom = "84px";
  chat.style.width = "min(390px, calc(100vw - 32px))";
  chat.style.maxHeight = "min(620px, calc(100vh - 120px))";
  chat.style.background = "#ffffff";
  chat.style.borderRadius = "18px";
  chat.style.boxShadow = "0 18px 48px rgba(0,0,0,.26)";
  chat.style.overflow = "hidden";
  chat.style.zIndex = "2147483647";
  chat.style.flexDirection = "column";
  chat.style.border = "1px solid rgba(0,0,0,.08)";
  chat.style.fontFamily = "Arial, sans-serif";

  chat.innerHTML = `
    <header style="background:#08111f;color:#fff;padding:12px 14px;display:flex;align-items:center;gap:10px;">
      <div style="font-weight:800;line-height:1.2;">
        <div>DilsAI Estudos</div>
        <small style="font-weight:400;color:#cbd5e1;">IA de estudos com modo e tema</small>
      </div>
      <button id="dilsai-close" type="button" aria-label="Fechar chat" style="margin-left:auto;background:rgba(255,255,255,.12);border:0;color:#fff;border-radius:10px;width:32px;height:32px;cursor:pointer;font-size:18px;">×</button>
    </header>

    <section style="padding:12px;background:#f8fafc;border-bottom:1px solid #e5e7eb;display:grid;gap:8px;">
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;">
        <label style="font-size:12px;color:#475569;font-weight:700;">
          Tema
          <select id="dilsai-topic" style="width:100%;margin-top:4px;padding:8px;border:1px solid #cbd5e1;border-radius:10px;background:#fff;">
            ${getOptionHtml(DILSAI_TOPICS)}
          </select>
        </label>

        <label style="font-size:12px;color:#475569;font-weight:700;">
          Modo
          <select id="dilsai-mode" style="width:100%;margin-top:4px;padding:8px;border:1px solid #cbd5e1;border-radius:10px;background:#fff;">
            ${getOptionHtml(DILSAI_MODES)}
          </select>
        </label>
      </div>

      <details id="dilsai-context-details" style="font-size:12px;color:#475569;">
        <summary style="cursor:pointer;font-weight:700;">Adicionar contexto/material para resposta precisa</summary>
        <textarea id="dilsai-context" rows="4" placeholder="Cole aqui trecho de apostila, aula, PDF ou material..." style="width:100%;margin-top:8px;padding:8px;border:1px solid #cbd5e1;border-radius:10px;resize:vertical;font-family:Arial,sans-serif;"></textarea>
      </details>
    </section>

    <div id="dilsai-chat-messages" style="flex:1;padding:12px;overflow:auto;background:#ffffff;min-height:220px;"></div>

    <div id="dilsai-typing" style="display:none;padding:0 12px 8px;color:#64748b;font-size:12px;">
      DilsAI está pensando...
    </div>

    <form id="dilsai-chat-form" style="display:flex;gap:8px;padding:12px;border-top:1px solid #e5e7eb;background:#f8fafc;">
      <input id="dilsai-chat-input" type="text" placeholder="Digite sua dúvida de estudo..." autocomplete="off" style="flex:1;padding:11px;border:1px solid #cbd5e1;border-radius:12px;outline:none;" />
      <button type="submit" style="background:#0077ff;color:#fff;border:0;border-radius:12px;padding:0 14px;font-weight:700;cursor:pointer;">Enviar</button>
    </form>
  `;

  document.getElementById("dilsai-close")?.addEventListener("click", () => toggleChat(false));

  return chat;
}

function ensureLauncher() {
  let launcher =
    document.getElementById("dilsai-launcher") ||
    document.getElementById("dilsai-fab");

  if (!launcher) {
    launcher = document.createElement("button");
    launcher.id = "dilsai-launcher";
    launcher.type = "button";
    launcher.textContent = "💬";
    document.body.appendChild(launcher);
  }

  launcher.setAttribute("aria-label", "Abrir chat DilsAI Estudos");
  launcher.title = "Falar com DilsAI Estudos";
  launcher.style.position = "fixed";
  launcher.style.right = "20px";
  launcher.style.bottom = "20px";
  launcher.style.width = "54px";
  launcher.style.height = "54px";
  launcher.style.borderRadius = "50%";
  launcher.style.border = "0";
  launcher.style.background = "#0077ff";
  launcher.style.color = "#fff";
  launcher.style.fontSize = "22px";
  launcher.style.cursor = "pointer";
  launcher.style.zIndex = "2147483647";
  launcher.style.boxShadow = "0 14px 30px rgba(0,0,0,.25)";

  launcher.onclick = (event) => {
    event.preventDefault();
    toggleChat();
  };

  return launcher;
}

function addMessage(role, text, meta = "") {
  const messages = document.getElementById("dilsai-chat-messages");
  if (!messages) return;

  const isUser = role === "user";
  const row = document.createElement("div");
  row.style.margin = "8px 0";
  row.style.display = "flex";
  row.style.justifyContent = isUser ? "flex-end" : "flex-start";

  const bubble = document.createElement("div");
  bubble.style.maxWidth = "88%";
  bubble.style.padding = "10px 12px";
  bubble.style.borderRadius = isUser ? "14px 14px 2px 14px" : "14px 14px 14px 2px";
  bubble.style.background = isUser ? "#e8f0ff" : "#f1f5f9";
  bubble.style.color = "#0f172a";
  bubble.style.fontSize = "14px";
  bubble.style.lineHeight = "1.45";
  bubble.innerHTML = `
    <strong style="display:block;margin-bottom:4px;">${isUser ? "Você" : "DilsAI"}</strong>
    <div>${nl2br(text)}</div>
    ${meta ? `<small style="display:block;margin-top:6px;color:#64748b;">${escapeHtml(meta)}</small>` : ""}
  `;

  row.appendChild(bubble);
  messages.appendChild(row);
  messages.scrollTop = messages.scrollHeight;
}

function setTyping(isTyping) {
  const typing = document.getElementById("dilsai-typing");
  if (typing) {
    typing.style.display = isTyping ? "block" : "none";
  }
}

function toggleChat(force) {
  const chat = ensureChatShell();
  ensureLauncher();

  const isVisible = chat.style.display !== "none";
  const next = typeof force === "boolean" ? force : !isVisible;

  chat.style.display = next ? "flex" : "none";

  if (next) {
    const input = document.getElementById("dilsai-chat-input");
    const messages = document.getElementById("dilsai-chat-messages");

    if (messages && !messages.dataset.welcome) {
      addMessage(
        "ai",
        "Olá! Eu sou o DilsAI Estudos. Escolha um tema, um modo e mande sua dúvida. Para resposta mais precisa, cole o material no campo de contexto.",
        "Precisão acima de resposta bonita."
      );
      messages.dataset.welcome = "1";
    }

    setTimeout(() => input?.focus(), 50);
  }
}

async function handleChatSubmit(event) {
  event.preventDefault();

  const input = document.getElementById("dilsai-chat-input");
  const topic = normalizeDilsAITopic(document.getElementById("dilsai-topic")?.value || "geral");
  const mode = document.getElementById("dilsai-mode")?.value || "professor";
  const context = document.getElementById("dilsai-context")?.value || "";
  const message = (input?.value || "").trim();

  if (!message) return;

  addMessage("user", message, `${topic} • ${mode}`);
  input.value = "";
  setTyping(true);

  try {
    const data = await askDilsAI({
      message,
      userName: "Aluno",
      topic,
      mode,
      context,
    });

    const metaParts = [];
    if (data.topic) metaParts.push(`Tema: ${data.topic}`);
    if (data.mode) metaParts.push(`Modo: ${data.mode}`);
    if (data.confidence) metaParts.push(`Confiança: ${data.confidence}`);
    if (data.safety_notice) metaParts.push(data.safety_notice);

    addMessage("ai", data.response || "(sem resposta)", metaParts.join(" • "));
  } catch (error) {
    addMessage(
      "ai",
      `Não consegui falar com a API agora. Verifique se o backend está rodando em ${window.API_BASE}. Erro: ${error.message}`,
      "Falha de conexão"
    );
  } finally {
    setTyping(false);
  }
}

function bindChatEvents() {
  ensureChatShell();
  ensureLauncher();

  document.addEventListener("submit", (event) => {
    if (event.target && event.target.id === "dilsai-chat-form") {
      handleChatSubmit(event);
    }
  });

  document.addEventListener(
    "click",
    (event) => {
      const element = event.target.closest("[data-ask], a, button");
      if (!element) return;

      const text = (element.textContent || "").trim().toLowerCase();

      if (element.hasAttribute("data-ask") || text === "experimente agora") {
        event.preventDefault();
        toggleChat(true);
      }
    },
    true
  );

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      toggleChat(false);
    }
  });

  console.log("[DilsAI Estudos] chat oficial ligado");
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bindChatEvents);
} else {
  bindChatEvents();
}

// === DilsAI Estudos — Full Page Chat Layout V1 ===
const DILSAI_FULL_PAGE_CHAT_V1 = true;

function getFullStudyElements() {
  return {
    section: document.getElementById("dilsai-study-app"),
    messages: document.getElementById("dilsai-full-messages"),
    form: document.getElementById("dilsai-full-chat-form"),
    input: document.getElementById("dilsai-full-input"),
    level: document.getElementById("dilsai-full-level"),
    topic: document.getElementById("dilsai-full-topic"),
    mode: document.getElementById("dilsai-full-mode"),
    context: document.getElementById("dilsai-full-context"),
  };
}

function getSelectLabel(select) {
  if (!select) return "";
  return select.options[select.selectedIndex]?.text || select.value || "";
}

function addFullStudyMessage(role, text, meta) {
  const { messages } = getFullStudyElements();
  if (!messages) return;

  const bubble = document.createElement("div");
  bubble.className = `study-app__message study-app__message--${role === "user" ? "user" : "assistant"}`;

  if (meta) {
    const metaNode = document.createElement("span");
    metaNode.className = "study-app__message-meta";
    metaNode.textContent = meta;
    bubble.appendChild(metaNode);
  }

  const textNode = document.createElement("div");
  textNode.textContent = text;
  bubble.appendChild(textNode);

  messages.appendChild(bubble);
  messages.scrollTop = messages.scrollHeight;
}

function ensureFullStudyWelcome() {
  const { messages } = getFullStudyElements();
  if (!messages || messages.dataset.welcome === "1") return;

  addFullStudyMessage(
    "assistant",
    "Olá! Eu sou o Professor DilsAI. Escolha o nível, a matéria e o modo. Se a pergunta depender de apostila, questão, PDF ou regra específica, cole o material no campo de contexto para eu responder com mais precisão.",
    "Bem-vindo"
  );

  messages.dataset.welcome = "1";
}

function openFullStudyChat() {
  const { section, input } = getFullStudyElements();
  ensureFullStudyWelcome();

  if (section) {
    section.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  setTimeout(() => input?.focus(), 250);
}

function clearFullStudyChat() {
  const { messages } = getFullStudyElements();
  if (!messages) return;
  messages.innerHTML = "";
  messages.dataset.welcome = "";
  ensureFullStudyWelcome();
}

async function handleFullStudySubmit(event) {
  event.preventDefault();

  const { input, level, topic, mode, context, form } = getFullStudyElements();
  const message = (input?.value || "").trim();

  if (!message) return;

  const selectedLevel = normalizeDilsAILevel(level?.value || "geral");
  const selectedTopic = normalizeDilsAITopic(topic?.value || "geral");
  const selectedMode = normalizeDilsAIMode(mode?.value || "professor");
  const levelLabel = getSelectLabel(level);
  const topicLabel = getSelectLabel(topic);
  const modeLabel = getSelectLabel(mode);
  const rawContext = (context?.value || "").trim();

  const enrichedContext = [
    `Nível de estudo selecionado: ${levelLabel || selectedLevel}.`,
    rawContext ? `Material/contexto enviado pelo usuário:\n${rawContext}` : "",
  ].filter(Boolean).join("\n\n");

  addFullStudyMessage("user", message, `${levelLabel} • ${topicLabel} • ${modeLabel}`);

  if (input) input.value = "";

  const submitButton = form?.querySelector("button[type='submit']");
  if (submitButton) {
    submitButton.disabled = true;
    submitButton.textContent = "Pensando...";
  }

  addFullStudyMessage(
    "assistant",
    "Analisando sua dúvida com foco em precisão. Um segundo...",
    "DilsAI"
  );

  try {
    const data = await askDilsAI({
      message,
      userName: "Dilson",
      level: selectedLevel,
      topic: selectedTopic,
      mode: selectedMode,
      context: enrichedContext,
    });

    const { messages } = getFullStudyElements();
    const lastMessage = messages?.lastElementChild;
    if (lastMessage?.classList.contains("study-app__message--assistant")) {
      lastMessage.remove();
    }

    const metaParts = [];
    if (data.topic) metaParts.push(`Tema: ${data.topic}`);
    if (data.mode) metaParts.push(`Modo: ${data.mode}`);
    if (data.used_context) metaParts.push("Usou contexto");

    addFullStudyMessage(
      "assistant",
      data.answer || data.response || "Recebi, mas a API não retornou resposta.",
      metaParts.join(" • ") || "DilsAI"
    );
  } catch (error) {
    const { messages } = getFullStudyElements();
    const lastMessage = messages?.lastElementChild;
    if (lastMessage?.classList.contains("study-app__message--assistant")) {
      lastMessage.remove();
    }

    addFullStudyMessage(
      "assistant",
      `Não consegui falar com a API agora. Verifique se o backend está rodando em ${window.API_BASE}. Erro: ${error.message}`,
      "Erro de conexão"
    );
  } finally {
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.textContent = "Enviar";
    }
  }
}

function bindFullStudyChatEvents() {
  populateFullStudyTaxonomyOptions();
  ensureFullStudyWelcome();

  document.addEventListener("click", (event) => {
    const openButton = event.target.closest("[data-open-study-chat]");
    if (openButton) {
      event.preventDefault();
      openFullStudyChat();
      return;
    }

    const clearButton = event.target.closest("[data-clear-study-chat]");
    if (clearButton) {
      event.preventDefault();
      clearFullStudyChat();
    }
  });

  document.addEventListener("submit", (event) => {
    if (event.target && event.target.id === "dilsai-full-chat-form") {
      handleFullStudySubmit(event);
    }
  });

  document.addEventListener("keydown", (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
      const active = document.activeElement;
      if (active && active.id === "dilsai-full-input") {
        const { form } = getFullStudyElements();
        form?.requestSubmit();
      }
    }
  });

  console.log("[DilsAI Estudos] tela cheia ligada");
}

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", bindFullStudyChatEvents);
} else {
  bindFullStudyChatEvents();
}

