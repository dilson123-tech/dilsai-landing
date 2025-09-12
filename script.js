console.log("[DilsAI] SCRIPT.JS CARREGADO");

// ===== Detecta ambiente =====
const isLocal = location.hostname === "127.0.0.1" || location.hostname === "localhost";

// Se tiver API pública, troca aqui ↓
const PROD_API = "https://dilsai-api.onrender.com"; // depois ajusta com sua URL real

// Base da API
window.API_BASE = isLocal ? "http://127.0.0.1:8000" : PROD_API;
window.ASK_URL  = window.API_BASE + "/chat";

console.log("[DilsAI] Ambiente:", isLocal ? "LOCAL" : "PRODUÇÃO");
console.log("[DilsAI] window.ASK_URL =", window.ASK_URL);

// Atualiza ano no rodapé
document.getElementById("year").textContent = new Date().getFullYear();

// ========= Função de chamada =========
async function askDilsAI(question) {
  try {
    const res = await fetch(window.ASK_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: question, user_name: "Usuário" })
    });
    if (!res.ok) throw new Error("API " + res.status);
    const { response } = await res.json();
    alert("🤖 " + answer);
  } catch (e) {
    alert("❌ Erro: " + e.message + "\nEndpoint: " + window.ASK_URL);
  }
}

// ========= Delegação CTA =========
document.addEventListener("click", (e) => {
  const el = e.target.closest("[data-ask], a, button");
  if (!el) return;
  const txt = (el.textContent || "").trim().toLowerCase();
  if (el.hasAttribute("data-ask") || txt === "experimente agora") {
    e.preventDefault();
    const q = window.prompt("Faça sua pergunta para o DilsAI:");
    if (q) askDilsAI(q);
  }
}, true);

console.log("[DilsAI] CTA ativo ✅");

// ===== DilsAI Chat – bootstrap =====
(function () {
  if (window.DILSAI_CHATBOUND) return;
  window.DILSAI_CHATBOUND = true;

  const chat = document.getElementById('dilsai-chatbox');
  const msgs = document.getElementById('dilsai-chat-messages');
  const form = document.getElementById('dilsai-chat-form');
  const input = document.getElementById('dilsai-chat-input');
  const launcher = document.getElementById('dilsai-launcher');

  if (!chat || !msgs || !form || !input) {
    console.warn('[DilsAI] chatbox HTML não encontrado.');
    return;
  }

  // helpers
  function openChat() {
    chat.style.display = 'flex';
    setTimeout(() => input.focus(), 50);
  }
  function closeChat() {
    chat.style.display = 'none';
  }
  function addMsg(role, text) {
    const li = document.createElement('div');
    li.style.margin = '8px 0';
    li.style.lineHeight = '1.4';
    li.innerHTML =
      role === 'me'
        ? `<div style="text-align:right"><span style="display:inline-block;background:#eef5ff;color:#0b4880;padding:8px 10px;border-radius:10px 10px 0 10px;max-width:92%">${text}</span></div>`
        : `<div style="text-align:left"><span style="display:inline-block;background:#f6f7f8;color:#222;padding:8px 10px;border-radius:10px 10px 10px 0;max-width:92%">${text}</span></div>`;
    msgs.appendChild(li);
    msgs.scrollTop = msgs.scrollHeight;
  }

  // abre chat pelo botão flutuante
  if (launcher) {
    launcher.addEventListener('click', () => {
      const isOpen = chat.style.display !== 'none' && chat.style.display !== '';
      if (isOpen) { closeChat(); } else { openChat(); }
    });
  }

  // fecha com ESC
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeChat();
  });

  // envia mensagem ao backend
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const q = (input.value || '').trim();
    if (!q) return;
    addMsg('me', q);
    input.value = '';
    try {
      const r = await fetch(window.ASK_URL, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ question: q })
      });
      if (!r.ok) throw new Error('API ' + r.status);
      const { response } = await r.json();
      addMsg('ai', answer || '(sem resposta)');
    } catch (err) {
      addMsg('ai', '❌ Erro: ' + err.message);
    }
  });

  // também abre o chat quando clicar em "Experimente agora" ou qualquer [data-ask]
  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-ask], a, button');
    if (!el) return;
    const txt = (el.textContent || '').trim().toLowerCase();
    if (el.hasAttribute('data-ask') || txt === 'experimente agora') {
      e.preventDefault();
      openChat();
    }
  }, true);

  console.log('[DilsAI] Chat ligado ✅');
})();
/* === DilsAI: Chatbox minimal (FAB abre/fecha) === */
(function(){
  const FAB_ID='dilsai-fab';
  const BOX_ID='dilsai-chatbox';

  // helper p/ criar nó a partir de HTML
  function h(html){
    const t=document.createElement('template');
    t.innerHTML=html.trim();
    return t.content.firstChild;
  }

  // cria o chatbox uma vez
  function ensureChatbox(){
    if (document.getElementById(BOX_ID)) return;

    const box=h(`
      <div id="${BOX_ID}" style="display:none">
        <header>💬 DilsAI
          <button type="button" id="${BOX_ID}-close"
            aria-label="Fechar"
            style="margin-left:auto;background:none;border:none;color:#fff;font-size:18px;cursor:pointer">×</button>
        </header>
        <div id="dilsai-chat-messages" style="padding:8px;overflow:auto;flex:1"></div>
        <form><input type="text" placeholder="Digite sua mensagem..." autocomplete="off"/>
              <button type="submit">Enviar</button></form>
      </div>
    `);
    document.body.appendChild(box);

    const msgs = box.querySelector('#dilsai-chat-messages');
    const form = box.querySelector('form');
    const input = box.querySelector('input');
    const close = box.querySelector(`#${BOX_ID}-close`);

    function push(who, text){
      const bubble = h(`<div style="margin:6px 0;display:flex;${who==='you'?'justify-content:flex-end':''}">
        <div style="max-width:75%;padding:8px 10px;border-radius:12px;${who==='you'?'background:#e8f0fe;':'background:#f5f5f5;'}">${text}</div>
      </div>`);
      msgs.appendChild(bubble);
      msgs.scrollTop = msgs.scrollHeight;
    }

    form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const q=(input.value||'').trim();
      if(!q) return;
      push('you', q);
      input.value='';
      try{
        const r = await fetch(window.ASK_URL, {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ question: q })
        });
        if(!r.ok) throw new Error('API '+r.status);
        const { response } = await r.json();
        push('bot', answer);
      }catch(err){
        push('bot', 'Erro: '+err.message);
      }
    });

    close.addEventListener('click', ()=>{ box.style.display='none'; });
  }

  function toggle(){
    const box = document.getElementById(BOX_ID);
    if(!box){ ensureChatbox(); return toggle(); }
    const st = getComputedStyle(box).display;
    box.style.display = st==='none' ? 'flex' : 'none';
  }

  // evita que cliques dentro do chat disparem outros handlers globais
  document.addEventListener('click', (e)=>{
    if (e.target.closest('#'+BOX_ID)) e.stopPropagation();
  }, true);

  // abre/fecha ao clicar no FAB
  document.addEventListener('click', (e)=>{
    if (e.target.closest('#'+FAB_ID)) { e.preventDefault(); toggle(); }
  }, true);
})();
/* Força FAB de chat (garantia) */
(function(){
  const id = 'dilsai-fab';
  if(document.getElementById(id)) return;
  const btn = document.createElement('button');
  btn.id = id;
  btn.innerHTML = '💬';
  Object.assign(btn.style, {
    position:'fixed', bottom:'20px', right:'20px',
    width:'48px', height:'48px', borderRadius:'50%',
    border:'none', background:'#0077ff', color:'#fff',
    fontSize:'20px', cursor:'pointer', zIndex:99999,
    boxShadow:'0 4px 12px rgba(0,0,0,0.2)'
  });
  document.body.appendChild(btn);
})();
/* === DilsAI Chat (Parte 1): FAB + Chatbox ================================ */
(function(){
  const LOG = (...a)=>console.log('[DilsAI Chat/P1]', ...a);

  // --- garante FAB ---
  function ensureFab(){
    let fab = document.getElementById('dilsai-fab');
    if (!fab) {
      fab = document.createElement('button');
      fab.id = 'dilsai-fab';
      fab.type = 'button';
      fab.innerHTML = '💬';
      Object.assign(fab.style, {
        position:'fixed', bottom:'20px', right:'20px',
        width:'48px', height:'48px', borderRadius:'50%',
        border:'none', background:'#0077ff', color:'#fff',
        fontSize:'20px', cursor:'pointer', zIndex: 2147483647,
        boxShadow:'0 4px 12px rgba(0,0,0,.2)'
      });
      document.body.appendChild(fab);
      LOG('FAB criado');
    } else {
      LOG('FAB já existe');
    }
    return fab;
  }

  // --- garante Chatbox ---
  function ensureChatbox(){
    let box = document.getElementById('dilsai-chatbox');
    if (!box) {
      box = document.createElement('div');
      box.id = 'dilsai-chatbox';
      box.style.display = 'none';
      box.innerHTML = `
        <header style="background:#0077ff;color:#fff;padding:8px 12px;">💬 DilsAI</header>
        <div id="dilsai-chat-messages" style="flex:1;padding:10px;overflow:auto;"></div>
        <form id="dilsai-chat-form" style="display:flex;border-top:1px solid #ddd;">
          <input id="dilsai-chat-input" placeholder="Digite..." style="flex:1;padding:8px;border:none;"/>
          <button type="submit" style="background:#0077ff;color:#fff;border:none;padding:0 12px;">Enviar</button>
        </form>
      `;
      Object.assign(box.style, {
        position:'fixed', bottom:'80px', right:'20px', width:'360px', maxHeight:'480px',
        background:'#fff', borderRadius:'12px', boxShadow:'0 8px 24px rgba(0,0,0,.2)',
        display:'none', zIndex: 2147483647, overflow:'hidden', fontFamily:'sans-serif'
      });
      document.body.appendChild(box);
      LOG('Chatbox criado');
    } else {
      LOG('Chatbox já existe');
    }
    return box;
  }

  window.DilsAIEnsure = { fab: ensureFab, chat: ensureChatbox };
})();
/* === DilsAI Chat (Parte 2): Toggle + API + Bind ========================== */
(function(){
  const LOG = (...a)=>console.log('[DilsAI Chat/P2]', ...a);

  function pushMsg(who, text){
    const wrap = document.getElementById('dilsai-chat-messages');
    if (!wrap) return;
    const line = document.createElement('div');
    line.style.margin = '6px 0';
    line.innerHTML = `<strong>${who}:</strong> ${text}`;
    wrap.appendChild(line);
    wrap.scrollTop = wrap.scrollHeight;
  }

  function toggleChat(force){
    const box = window.DilsAIEnsure.chat();
    const wantOpen = (typeof force === 'boolean') ? force : (box.style.display === 'none');
    box.style.display = wantOpen ? 'flex' : 'none';
    box.style.flexDirection = 'column';
    LOG('toggleChat ->', wantOpen ? 'abriu' : 'fechou');
  }

  function bind(){
    const fab = window.DilsAIEnsure.fab();
    fab.addEventListener('click', () => toggleChat());

    // enviar mensagens
    document.getElementById('dilsai-chat-form')?.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const input = document.getElementById('dilsai-chat-input');
      const msg = (input.value||'').trim();
      if (!msg) return;
      pushMsg('Você', msg);
      input.value = '';
      try {
        const r = await fetch(window.ASK_URL, {
          method:'POST', headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ question: msg })
        });
        if (!r.ok) throw new Error('API ' + r.status);
        const { response } = await r.json();
        pushMsg('DilsAI', answer);
      } catch(err){ pushMsg('DilsAI','Erro: '+err.message); }
    });

    LOG('Listeners prontos');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bind);
  } else {
    bind();
  }
})();
/* === DilsAI Chat • HOTFIX (parte 1/3: cria FAB + chat) === */
(function(){
  const LOG = (...a)=>console.log('[DilsAI Chat/Hotfix]', ...a);

  window.__dilsaiEnsureFab = function(){
    let fab = document.getElementById('dilsai-fab');
    if (!fab) {
      fab = document.createElement('button');
      fab.id = 'dilsai-fab';
      fab.type = 'button';
      fab.textContent = '��';
      Object.assign(fab.style, {
        position:'fixed', bottom:'20px', right:'20px',
        width:'48px', height:'48px', borderRadius:'50%',
        border:'none', background:'#0077ff', color:'#fff',
        fontSize:'20px', cursor:'pointer', zIndex:2147483647,
        boxShadow:'0 4px 12px rgba(0,0,0,.2)'
      });
      document.body.appendChild(fab);
      LOG('FAB criado');
    }
    return fab;
  };

  window.__dilsaiEnsureChat = function(){
    let box = document.getElementById('dilsai-chatbox');
    if (!box) {
      box = document.createElement('div');
      box.id = 'dilsai-chatbox';
      Object.assign(box.style, {
        position:'fixed', bottom:'80px', right:'20px',
        width:'360px', maxHeight:'480px',
        background:'#fff', borderRadius:'12px',
        boxShadow:'0 8px 24px rgba(0,0,0,.2)',
        display:'none', zIndex:2147483647, overflow:'hidden',
        fontFamily:'sans-serif'
      });
      box.innerHTML = `
        <header style="background:#0077ff;color:#fff;padding:8px 12px;">💬 DilsAI</header>
        <div id="dilsai-chat-messages" style="flex:1;padding:10px;overflow:auto;"></div>
        <form id="dilsai-chat-form" style="display:flex;border-top:1px solid #ddd;">
          <input id="dilsai-chat-input" placeholder="Digite..." style="flex:1;padding:8px;border:none;outline:none;"/>
          <button type="submit" style="background:#0077ff;color:#fff;border:none;padding:0 12px;cursor:pointer;">Enviar</button>
        </form>
      `;
      document.body.appendChild(box);
      LOG('Chatbox criado');
    }
    return box;
  };
  window.__dilsaiToggleChat = function(){
    const box = window.__dilsaiEnsureChat();
    const show = (box.style.display === 'none' || !box.style.display);
    box.style.display = show ? 'block' : 'none';
    console.log('[DilsAI Chat/Hotfix] toggleChat ->', show ? 'abriu' : 'fechou');
  };

  function __bindDilsai(){
    const fab = window.__dilsaiEnsureFab();
    fab.onclick = null; // limpa handlers antigos
    fab.addEventListener('click', (e)=>{ e.preventDefault(); window.__dilsaiToggleChat(); });

    // submit do chat (funciona mesmo se criado depois)
    document.addEventListener('submit', async (e)=>{
      const f = e.target;
      if (f && f.id === 'dilsai-chat-form') {
        e.preventDefault();
        const input = document.getElementById('dilsai-chat-input');
        const msg = (input?.value||'').trim();
        if (!msg) return;
        const out = document.getElementById('dilsai-chat-messages');
        const me = document.createElement('div');
        me.innerHTML = `<strong>Você:</strong> ${msg}`;
        out.appendChild(me); out.scrollTop = out.scrollHeight; input.value = '';
        try {
          const r = await fetch(window.ASK_URL, {
            method:'POST', headers:{'Content-Type':'application/json'},
            body: JSON.stringify({ question: msg })
          });
          if (!r.ok) throw new Error('API ' + r.status);
          const { response } = await r.json();
          const ai = document.createElement('div');
          ai.innerHTML = `<strong>DilsAI:</strong> ${answer}`;
          out.appendChild(ai); out.scrollTop = out.scrollHeight;
        } catch(err){
          const ai = document.createElement('div');
          ai.innerHTML = `<strong>DilsAI:</strong> Erro: ${err.message}`;
          out.appendChild(ai); out.scrollTop = out.scrollHeight;
        }
      }
    });

    console.log('[DilsAI Chat/Hotfix] listeners prontos');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', __bindDilsai);
  } else {
    __bindDilsai();
  }
})();
/* === DilsAI Chat • auto-scroll === */
(function(){
  const box = document.getElementById('dilsai-chat-messages');
  if(!box) return;
  const observer = new MutationObserver(()=>{ box.scrollTop = box.scrollHeight; });
  observer.observe(box,{childList:true});
})();

// ===== DilsAI: bind no chatbox =====
(function(){
  const form = document.querySelector('#dilsai-chatbox form');
  const input = document.querySelector('#dilsai-chat-input');
  const messages = document.querySelector('#dilsai-chat-messages');

  if(!form) return;
  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const q = input.value.trim();
    if(!q) return;
    input.value = "";

    // mostra mensagem do usuário
    const userMsg = document.createElement('div');
    userMsg.textContent = "👤 " + q;
    messages.appendChild(userMsg);

    try {
      const res = await fetch(window.ASK_URL, {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({ question: q })
      });
      const data = await res.json();

      const botMsg = document.createElement('div');
      botMsg.textContent = "🤖 " + (data.answer || "[sem resposta]");
      messages.appendChild(botMsg);

      messages.scrollTop = messages.scrollHeight;
    } catch(err) {
      const errMsg = document.createElement('div');
      errMsg.textContent = "⚠️ Erro: " + err.message;
      messages.appendChild(errMsg);
    }
  });
})();

(()=> {
// === DilsAI Chat+ (helpers) START ===
(()=> {
  const STORE_KEY='dilsai.chat.v1';
  const $ = (sel,p=document)=>p.querySelector(sel);

  function scrollEnd(){
    const box = $('#dilsai-chat-messages');
    if (box) box.scrollTop = box.scrollHeight;
  }

  function showTyping(on){
    const t = $('#dilsai-typing');
    if (!t) return;
    t.classList.toggle('on', !!on);
    scrollEnd();
  }

  function loadHistory(){
    try { return JSON.parse(localStorage.getItem(STORE_KEY) || '[]'); }
    catch { return []; }
  }
  function saveHistory(list){
    try { localStorage.setItem(STORE_KEY, JSON.stringify(list.slice(-50))); }
    catch {}
  }

  function appendMessage(role, text){
    const box = $('#dilsai-chat-messages');
    if (!box) return;
    const div = document.createElement('div');
    div.className = 'dilsai-msg ' + (role==='me' ? 'dilsai-me' : 'dilsai-bot');
    div.textContent = text;
    box.appendChild(div);
    const hist = loadHistory(); hist.push({role, text, at: Date.now()}); saveHistory(hist);
    scrollEnd();
  }

  function mountTyping(){
    const box = $('#dilsai-chat-messages');
    if (box && !$('#dilsai-typing')) {
      const t = document.createElement('div');
      t.id = 'dilsai-typing';
      t.textContent = 'DilsAI está digitando…';
      box.appendChild(t);
    }
  }

  function renderHistory(){
    const box = $('#dilsai-chat-messages');
    if (!box) return;
    loadHistory().forEach(m => appendMessage(m.role, m.text));
  }

  function patchForm(){
    const form  = $('#dilsai-chat-form');
    const input = $('#dilsai-chat-input');
    if (!form || !input) return;

    form.onsubmit = async (e) => {
      e.preventDefault();
      const msg = (input.value||'').trim();
      if (!msg) return;

      appendMessage('me', msg);
      input.value='';

      try{
        showTyping(true);
        const r = await fetch(window.ASK_URL, {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ question: msg })
        });
        const data = await r.json();
        appendMessage('bot', data.answer || '[sem resposta]');
      } catch(err){
        appendMessage('bot', 'Erro: ' + (err?.message || err));
      } finally {
        showTyping(false);
      }
    };
  }

  function init(){
    const box = $('#dilsai-chat-messages');
    if (!box) { setTimeout(init, 300); return; } // espera o chat montar
    mountTyping();
    renderHistory();
    patchForm();
    scrollEnd();
    console.log('[DilsAI] chat UX plus ativo');
  }

  if (document.readyState==='loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})(); // === DilsAI Chat+ END ===
// === DilsAI: FAB + montagem garantida do chat ===
(() => {
  const $ = (s,p=document)=>p.querySelector(s);

  function ensureChatBox(){
    if ($('#dilsai-chatbox')) return;
    const box=document.createElement('div');
    box.id='dilsai-chatbox';
    box.style.display='none';
    box.innerHTML = `
      <div id="dilsai-chatbox-header">DilsAI Chat
        <button id="dilsai-close" aria-label="Fechar" style="float:right;background:transparent;border:none;color:#fff;cursor:pointer">×</button>
      </div>
      <div id="dilsai-chat-messages" class="dilsai-chat-messages"></div>
      <div id="dilsai-typing" style="display:none;padding:8px 10px;color:#666;font-size:12px">DilsAI está digitando…</div>
      <form id="dilsai-chat-form">
        <input id="dilsai-chat-input" placeholder="Digite sua mensagem..." autocomplete="off"/>
        <button type="submit">Enviar</button>
      </form>
    `;
    document.body.appendChild(box);
    // fechar pelo X
    $('#dilsai-close').addEventListener('click', () => toggleChat(false));
  }

  function ensureFab(){
    if ($('#dilsai-fab')) return;
    const fab=document.createElement('button');
    fab.id='dilsai-fab';
    fab.title='Abrir chat do DilsAI';
    fab.innerHTML='💬';
    Object.assign(fab.style, {
      position:'fixed', right:'20px', bottom:'20px',
      width:'48px', height:'48px', borderRadius:'50%',
      background:'#0077ff', color:'#fff', border:'none',
      boxShadow:'0 10px 20px rgba(0,0,0,.2)', cursor:'pointer',
      zIndex: 2147483647, fontSize:'20px', lineHeight:'48px'
    });
    fab.addEventListener('click', () => toggleChat());
    document.body.appendChild(fab);
  }

  function toggleChat(force){
    ensureChatBox();
    const box = $('#dilsai-chatbox');
    const showing = box.style.display !== 'none';
    const next = (typeof force === 'boolean') ? force : !showing;
    box.style.display = next ? 'flex' : 'none';
    if (next) { $('#dilsai-chat-input')?.focus(); }
  }

  // expõe pra outros blocos se precisarem
  window.__dilsaiToggleChat = toggleChat;

  function initFab(){
    ensureChatBox();
    ensureFab();
  }
  if (document.readyState === 'loading'){
    document.addEventListener('DOMContentLoaded', initFab);
  } else {
    initFab();
  }
})();

// === DilsAI: bootstrap mínimo do FAB + montar chat + capturar CTA ===
(() => {
  const $ = (s,p=document)=>p.querySelector(s);

  function ensureChat(){
    if ($('#dilsai-chatbox')) return;
    const box = document.createElement('div');
    box.id = 'dilsai-chatbox';
    box.style.display = 'none';
    box.innerHTML = `
      <div id="dilsai-chatbox-header" style="background:#0077ff;color:#fff;padding:10px 12px;font-weight:600">
        DilsAI Chat
        <button id="dilsai-close" aria-label="Fechar" style="float:right;background:transparent;border:none;color:#fff;cursor:pointer">×</button>
      </div>
      <div id="dilsai-chat-messages" class="dilsai-chat-messages"></div>
      <div id="dilsai-typing" style="display:none;padding:8px 10px;color:#666;font-size:12px">DilsAI está digitando…</div>
      <form id="dilsai-chat-form">
        <input id="dilsai-chat-input" placeholder="Digite sua mensagem..." autocomplete="off"/>
        <button type="submit">Enviar</button>
      </form>
    `;
    document.body.appendChild(box);
    $('#dilsai-close')?.addEventListener('click', () => toggleChat(false));
  }

  function ensureFab(){
    if ($('#dilsai-fab')) return;
    const fab = document.createElement('button');
    fab.id = 'dilsai-fab';
    fab.title = 'Abrir chat do DilsAI';
    fab.innerHTML = '💬';
    Object.assign(fab.style, {
      position:'fixed', right:'20px', bottom:'20px',
      width:'48px', height:'48px', borderRadius:'50%',
      background:'#0077ff', color:'#fff', border:'none',
      boxShadow:'0 12px 24px rgba(0,0,0,.22)', cursor:'pointer',
      zIndex: 2147483647, fontSize:'20px', lineHeight:'48px'
    });
    fab.addEventListener('click', () => toggleChat());
    document.body.appendChild(fab);
  }

  function toggleChat(force){
    ensureChat();
    const box = $('#dilsai-chatbox');
    const showing = box.style.display !== 'none';
    const next = (typeof force==='boolean') ? force : !showing;
    box.style.display = next ? 'flex' : 'none';
    if (next) $('#dilsai-chat-input')?.focus();
  }
  window.__dilsaiToggleChat = toggleChat;

  // CTA: qualquer [data-ask] ou texto "Experimente agora"
  document.addEventListener('click', (e) => {
    const el = e.target.closest('[data-ask],a,button');
    if (!el) return;
    const txt = (el.textContent||'').trim().toLowerCase();
    if (el.hasAttribute('data-ask') || txt === 'experimente agora') {
      e.preventDefault();
      toggleChat(true);
    }
  }, true);

  function init(){ ensureChat(); ensureFab(); console.log('[DilsAI] bootstrap ativo'); }
  (document.readyState==='loading')
    ? document.addEventListener('DOMContentLoaded', init)
    : init();
})();
