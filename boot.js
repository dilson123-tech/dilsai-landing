(() => {
  /* helpers */
  const $ = (q,root=document) => root.querySelector(q);

  function ensureFab(){
    let fab = $('#dilsai-fab');
    if (!fab){
      fab = document.createElement('button');
      fab.id = 'dilsai-fab';
      fab.title = 'Falar com a DilsAI';
      fab.innerHTML = '💬';
      document.body.appendChild(fab);
    }
    return fab;
  }

  function ensureBox(){
    let box = $('#dilsai-chatbox');
    if (!box){
      box = document.createElement('div');
      box.id = 'dilsai-chatbox';
      box.innerHTML = `
        <div id="dilsai-chatbox-header"
             style="background:#0077ff;color:#fff;padding:10px 12px;font-weight:600;border-radius:12px 12px 0 0">
          DilsAI Chat
        </div>
        <div id="dilsai-chat-messages"
             style="flex:1; overflow:auto; padding:10px; background:#fff"></div>
        <form id="dilsai-chat-form" style="display:flex; gap:8px; padding:10px; border-top:1px solid #e6e6ef">
          <input id="dilsai-chat-input" placeholder="Digite sua mensagem..." style="flex:1; outline:none; border:1px solid #e2e8f0; border-radius:8px; padding:8px 10px">
          <button type="submit" style="background:#0077ff;color:#fff;border:none;border-radius:8px;padding:0 12px">Enviar</button>
        </form>`;
      document.body.appendChild(box);
    }
    return box;
  }

  function toggleChat(force){
    const box = ensureBox();
    const show = (typeof force==='boolean') ? force : (box.style.display==='none' || !box.style.display);
    box.style.display = show ? 'flex' : 'none';
    if (show) $('#dilsai-chat-input')?.focus();
  }
  /* wire: FAB */
  function bindFab(){
    const fab = ensureFab();
    fab.onclick = (e)=>{ e.preventDefault(); toggleChat(); };
  }

  /* wire: CTA “Experimente agora” e [data-ask] */
  function bindCTA(){
    document.addEventListener('click', (e)=>{
      const el = e.target.closest('[data-ask],a,button'); if (!el) return;
      const txt = (el.textContent||'').trim().toLowerCase();
      if (el.hasAttribute('data-ask') || txt === 'experimente agora'){
        e.preventDefault();
        toggleChat(true);
      }
    }, true); /* capture para vencer scroll de anchor */
  }

  /* chat form -> chama API */
  function bindForm(){
    const form = $('#dilsai-chat-form'); if (!form) return;
    const input = $('#dilsai-chat-input');
    const msgs  = $('#dilsai-chat-messages');

    const append = (who, text) => {
      const div = document.createElement('div');
      div.style.margin = '6px 0';
      div.style.whiteSpace = 'pre-wrap';
      div.innerHTML = who === 'me'
        ? `<div style="background:#f1f5f9;border-radius:8px;padding:8px 10px;display:inline-block">${text}</div>`
        : `<div style="background:#eef6ff;border-radius:8px;padding:8px 10px;display:inline-block">${text}</div>`;
      msgs.appendChild(div);
      msgs.scrollTop = msgs.scrollHeight;
    };

    form.onsubmit = async (ev)=>{
      ev.preventDefault();
      const q = (input.value||'').trim();
      if (!q) return;
      append('me', q);
      input.value = '';

      try{
        const res = await fetch(window.ASK_URL, {
          method:'POST',
          headers:{'Content-Type':'application/json'},
          body: JSON.stringify({ question: q })
        });
        if (!res.ok) throw new Error('API '+res.status);
        const { answer } = await res.json();
        append('bot', answer || '[sem resposta]');
      }catch(err){
        append('bot', 'Erro: '+ (err?.message || err));
      }
    };
  }
  function init(){
    ensureFab();
    ensureBox();
    bindFab();
    bindCTA();
    bindForm();
    console.log('[DilsAI] boot minimal ativo');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
