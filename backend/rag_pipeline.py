<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>RAG Document Q&A</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;1,9..144,300&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet"/>

<style>
  :root {
    --bg: #0c0d0f;
    --bg2: #141518;
    --bg3: #1c1e23;
    --border: rgba(255,255,255,0.07);
    --border2: rgba(255,255,255,0.14);
    --text: #e8e9ec;
    --muted: #7a7d87;
    --accent: #5b8cf7;
    --accent2: #3ecf8e;
    --accent3: #f5a623;
    --danger: #f56565;
    --font-serif: 'Fraunces', Georgia, serif;
    --font-sans: 'DM Sans', sans-serif;
    --font-mono: 'DM Mono', monospace;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    color: var(--text);
    font-family: var(--font-sans);
    font-size: 15px;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
  }

  /* ── Header ── */
  header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 18px 32px;
    border-bottom: 1px solid var(--border);
    background: var(--bg);
    position: sticky; top: 0; z-index: 50;
    backdrop-filter: blur(12px);
  }

  .logo {
    font-family: var(--font-serif);
    font-size: 22px;
    font-weight: 600;
    letter-spacing: -0.5px;
    color: var(--text);
  }
  .logo span { color: var(--accent); }

  .status-dot {
    display: flex; align-items: center; gap: 7px;
    font-size: 12px; color: var(--muted);
    font-family: var(--font-mono);
  }
  .dot {
    width: 7px; height: 7px; border-radius: 50%;
    background: var(--muted);
    transition: background 0.3s;
  }
  .dot.ready { background: var(--accent2); box-shadow: 0 0 8px var(--accent2); }

  /* ── Layout ── */
  .app {
    display: grid;
    grid-template-columns: 320px 1fr;
    flex: 1;
    height: calc(100vh - 62px);
  }

  /* ── Sidebar ── */
  .sidebar {
    border-right: 1px solid var(--border);
    display: flex;
    flex-direction: column;
    overflow: hidden;
    background: var(--bg2);
  }

  .sidebar-section {
    padding: 20px;
    border-bottom: 1px solid var(--border);
  }

  .section-label {
    font-size: 10px;
    font-family: var(--font-mono);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
  }

  /* API Key */
  .api-input-wrap { position: relative; }
  .api-input {
    width: 100%;
    background: var(--bg3);
    border: 1px solid var(--border2);
    border-radius: 8px;
    color: var(--text);
    font-family: var(--font-mono);
    font-size: 12px;
    padding: 10px 12px;
    outline: none;
    transition: border-color 0.2s;
  }
  .api-input:focus { border-color: var(--accent); }
  .api-input::placeholder { color: var(--muted); }

  .btn {
    display: inline-flex; align-items: center; justify-content: center;
    gap: 6px;
    background: var(--accent);
    color: #fff;
    border: none;
    border-radius: 8px;
    padding: 9px 16px;
    font-family: var(--font-sans);
    font-size: 13px;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s, transform 0.1s;
    width: 100%;
    margin-top: 8px;
  }
  .btn:hover { opacity: 0.88; }
  .btn:active { transform: scale(0.98); }
  .btn.secondary {
    background: var(--bg3);
    color: var(--text);
    border: 1px solid var(--border2);
  }
  .btn.danger { background: transparent; color: var(--danger); border: 1px solid var(--danger); }
  .btn:disabled { opacity: 0.35; cursor: not-allowed; }

  /* Upload Zone */
  .drop-zone {
    border: 1.5px dashed var(--border2);
    border-radius: 10px;
    padding: 24px 16px;
    text-align: center;
    cursor: pointer;
    transition: border-color 0.2s, background 0.2s;
    background: var(--bg3);
    position: relative;
  }
  .drop-zone:hover, .drop-zone.drag { border-color: var(--accent); background: rgba(91,140,247,0.06); }
  .drop-zone input[type=file] { position: absolute; inset: 0; opacity: 0; cursor: pointer; }
  .drop-icon { font-size: 26px; margin-bottom: 8px; }
  .drop-label { font-size: 13px; color: var(--muted); line-height: 1.5; }
  .drop-label strong { color: var(--accent); font-weight: 500; }
  .drop-types { font-size: 10px; color: var(--muted); margin-top: 6px; font-family: var(--font-mono); }

  /* File list */
  .file-list {
    flex: 1;
    overflow-y: auto;
    padding: 16px 20px;
  }
  .file-item {
    display: flex; align-items: center; gap: 10px;
    padding: 9px 10px;
    border-radius: 7px;
    border: 1px solid var(--border);
    background: var(--bg3);
    margin-bottom: 7px;
    animation: slideIn 0.25s ease;
  }
  @keyframes slideIn {
    from { opacity: 0; transform: translateY(-6px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .file-icon {
    font-size: 18px;
    width: 28px; text-align: center;
    flex-shrink: 0;
  }
  .file-info { flex: 1; min-width: 0; }
  .file-name {
    font-size: 12px; font-weight: 500;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  }
  .file-meta { font-size: 10px; color: var(--muted); font-family: var(--font-mono); margin-top: 1px; }
  .file-badge {
    font-size: 10px; font-family: var(--font-mono);
    padding: 2px 7px; border-radius: 20px;
    background: rgba(62,207,142,0.12); color: var(--accent2);
    flex-shrink: 0;
  }
  .file-badge.indexing { background: rgba(245,166,35,0.12); color: var(--accent3); }
  .file-badge.error { background: rgba(245,101,101,0.12); color: var(--danger); }

  .stats-bar {
    padding: 14px 20px;
    border-top: 1px solid var(--border);
    display: flex; gap: 16px;
    font-size: 11px; font-family: var(--font-mono);
    color: var(--muted);
  }
  .stat-num { color: var(--accent); font-weight: 500; }

  /* ── Chat Area ── */
  .chat-area {
    display: flex;
    flex-direction: column;
    background: var(--bg);
  }

  .messages {
    flex: 1;
    overflow-y: auto;
    padding: 32px 48px;
    display: flex;
    flex-direction: column;
    gap: 24px;
  }

  .empty-state {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    color: var(--muted);
    gap: 12px;
    padding: 48px;
  }
  .empty-icon { font-size: 40px; opacity: 0.5; }
  .empty-title { font-family: var(--font-serif); font-size: 22px; color: var(--text); font-weight: 300; }
  .empty-sub { font-size: 14px; line-height: 1.6; max-width: 380px; }

  .msg { display: flex; gap: 14px; max-width: 820px; animation: fadeUp 0.3s ease; }
  @keyframes fadeUp {
    from { opacity: 0; transform: translateY(10px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .msg.user { align-self: flex-end; flex-direction: row-reverse; }

  .msg-avatar {
    width: 34px; height: 34px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px; flex-shrink: 0; margin-top: 2px;
  }
  .msg.ai .msg-avatar   { background: rgba(91,140,247,0.15); color: var(--accent); border: 1px solid rgba(91,140,247,0.25); }
  .msg.user .msg-avatar { background: rgba(62,207,142,0.15); color: var(--accent2); border: 1px solid rgba(62,207,142,0.25); }

  .msg-bubble {
    background: var(--bg2);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 18px;
    font-size: 14px;
    line-height: 1.7;
    max-width: 680px;
  }
  .msg.user .msg-bubble {
    background: rgba(91,140,247,0.1);
    border-color: rgba(91,140,247,0.2);
  }
  .msg-bubble p { margin-bottom: 8px; }
  .msg-bubble p:last-child { margin-bottom: 0; }

  .sources {
    margin-top: 12px;
    padding-top: 12px;
    border-top: 1px solid var(--border);
    display: flex;
    flex-wrap: wrap;
    gap: 6px;
  }
  .source-chip {
    font-size: 11px; font-family: var(--font-mono);
    padding: 4px 10px; border-radius: 20px;
    background: var(--bg3); border: 1px solid var(--border2);
    color: var(--muted);
    display: flex; align-items: center; gap: 5px;
  }
  .source-chip .src-icon { font-size: 12px; }
  .source-snippet {
    font-size: 11px; color: var(--muted);
    margin-top: 6px; font-style: italic;
    line-height: 1.5;
    padding-left: 8px; border-left: 2px solid var(--border2);
  }

  .thinking {
    display: flex; align-items: center; gap: 8px;
    color: var(--muted); font-size: 13px;
    font-family: var(--font-mono);
  }
  .dots span {
    display: inline-block; width: 5px; height: 5px;
    border-radius: 50%; background: var(--accent);
    animation: bounce 1.2s ease-in-out infinite;
    margin-right: 3px;
  }
  .dots span:nth-child(2) { animation-delay: 0.2s; }
  .dots span:nth-child(3) { animation-delay: 0.4s; }
  @keyframes bounce {
    0%, 80%, 100% { transform: translateY(0); opacity: 0.3; }
    40% { transform: translateY(-5px); opacity: 1; }
  }

  /* ── Input Bar ── */
  .input-bar {
    padding: 20px 32px 24px;
    border-top: 1px solid var(--border);
    background: var(--bg);
  }
  .input-wrap {
    display: flex; gap: 10px;
    background: var(--bg2);
    border: 1px solid var(--border2);
    border-radius: 12px;
    padding: 8px 10px;
    transition: border-color 0.2s;
    align-items: flex-end;
  }
  .input-wrap:focus-within { border-color: var(--accent); }

  textarea {
    flex: 1;
    background: transparent;
    border: none;
    outline: none;
    color: var(--text);
    font-family: var(--font-sans);
    font-size: 14px;
    line-height: 1.6;
    resize: none;
    min-height: 40px;
    max-height: 160px;
    padding: 4px 6px;
    overflow-y: auto;
  }
  textarea::placeholder { color: var(--muted); }

  .send-btn {
    background: var(--accent);
    border: none; color: #fff;
    width: 36px; height: 36px;
    border-radius: 8px;
    cursor: pointer;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    transition: opacity 0.2s, transform 0.1s;
    font-size: 16px;
  }
  .send-btn:hover { opacity: 0.88; }
  .send-btn:active { transform: scale(0.95); }
  .send-btn:disabled { opacity: 0.3; cursor: not-allowed; }

  .input-hint {
    font-size: 11px; color: var(--muted);
    text-align: center; margin-top: 8px;
    font-family: var(--font-mono);
  }

  /* ── Toast ── */
  .toast {
    position: fixed; bottom: 28px; right: 28px;
    background: var(--bg2); border: 1px solid var(--border2);
    border-radius: 10px; padding: 12px 18px;
    font-size: 13px; z-index: 100;
    display: flex; align-items: center; gap: 10px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.4);
    animation: toastIn 0.3s ease;
    max-width: 340px;
  }
  @keyframes toastIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
  }
  .toast.success { border-color: rgba(62,207,142,0.3); }
  .toast.error   { border-color: rgba(245,101,101,0.3); }
  .toast-icon { font-size: 16px; }

  /* Scrollbar */
  ::-webkit-scrollbar { width: 4px; }
  ::-webkit-scrollbar-track { background: transparent; }
  ::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 2px; }

  /* Notification area */
  #notification { display: none; }
</style>
</head>
<body>

<header>
  <div class="logo">RAG <span>Q&A</span></div>
  <div class="status-dot">
    <div class="dot" id="statusDot"></div>
    <span id="statusText">not initialized</span>
  </div>
</header>

<div class="app">

  <!-- ── Sidebar ── -->
  <aside class="sidebar">

    <div class="sidebar-section">
      <div class="section-label">Groq API Key (Free)</div>
      <div class="api-input-wrap">
        <input type="password" class="api-input" id="apiKey" placeholder="gsk_..."/>
      </div>
      <button class="btn" id="initBtn" onclick="initPipeline()">Initialize Pipeline</button>
    </div>

    <div class="sidebar-section">
      <div class="section-label">Upload Documents</div>
      <div class="drop-zone" id="dropZone">
        <input type="file" id="fileInput" multiple
          accept=".pdf,.txt,.docx,.doc,.csv,.html,.htm,.pptx,.ppt,.xlsx,.xls,.md"
          onchange="handleFiles(this.files)"/>
        <div class="drop-icon">📂</div>
        <div class="drop-label"><strong>Click to upload</strong> or drag & drop</div>
        <div class="drop-types">PDF · DOCX · TXT · CSV · PPTX · XLSX · HTML · MD</div>
      </div>
    </div>

    <div class="file-list" id="fileList">
      <div style="font-size:12px;color:var(--muted);text-align:center;padding:20px 0;">
        No documents indexed yet
      </div>
    </div>

    <div class="stats-bar">
      <span>Files: <span class="stat-num" id="statFiles">0</span></span>
      <span>Chunks: <span class="stat-num" id="statChunks">0</span></span>
      <button class="btn danger" style="width:auto;padding:4px 12px;font-size:11px;" onclick="resetPipeline()">Reset</button>
    </div>

  </aside>

  <!-- ── Chat ── -->
  <main class="chat-area">
    <div class="messages" id="messages">
      <div class="empty-state" id="emptyState">
        <div class="empty-icon">🔍</div>
        <div class="empty-title">Ask anything about your documents</div>
        <div class="empty-sub">
          Initialize the pipeline with your OpenAI key, upload your files, then start asking questions.
        </div>
      </div>
    </div>

    <div class="input-bar">
      <div class="input-wrap">
        <textarea id="questionInput" placeholder="Ask a question about your documents…" rows="1"
          onkeydown="handleKey(event)" oninput="autoResize(this)"></textarea>
        <button class="send-btn" id="sendBtn" onclick="sendQuery()" disabled title="Send">➤</button>
      </div>
      <div class="input-hint">Enter to send · Shift+Enter for new line</div>
    </div>
  </main>

</div>

<script>
const API = 'http://localhost:8000';
let initialized = false;
let indexedFiles = [];

// ── Auto resize textarea ──
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 160) + 'px';
}

// ── Key handler ──
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendQuery();
  }
}

// ── Init Pipeline ──
async function initPipeline() {
  const key = document.getElementById('apiKey').value.trim();
  if (!key) return showToast('Enter your OpenAI API key', 'error');

  const btn = document.getElementById('initBtn');
  btn.disabled = true;
  btn.textContent = 'Initializing…';

  try {
    const res = await fetch(`${API}/init`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ groq_api_key: key })
    });
    if (!res.ok) throw new Error(await res.text());

    initialized = true;
    setStatus(true);
    document.getElementById('sendBtn').disabled = false;
    showToast('Pipeline ready!', 'success');
    btn.textContent = '✓ Initialized';
  } catch (e) {
    showToast('Init failed: ' + e.message, 'error');
    btn.textContent = 'Initialize Pipeline';
    btn.disabled = false;
  }
}

// ── Handle file uploads ──
async function handleFiles(files) {
  if (!initialized) return showToast('Initialize the pipeline first', 'error');
  for (const file of files) {
    await uploadFile(file);
  }
  await refreshStats();
}

async function uploadFile(file) {
  const id = addFileCard(file.name, 'indexing');
  const formData = new FormData();
  formData.append('file', file);

  try {
    const res = await fetch(`${API}/upload`, { method: 'POST', body: formData });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Upload failed');
    updateFileCard(id, 'indexed', data.chunks + ' chunks');
    indexedFiles.push(file.name);
  } catch (e) {
    updateFileCard(id, 'error', e.message);
    showToast(`Error: ${e.message}`, 'error');
  }
}

function addFileCard(name, status) {
  const list = document.getElementById('fileList');
  const emptyMsg = list.querySelector('div');
  if (emptyMsg && emptyMsg.textContent.includes('No documents')) emptyMsg.remove();

  const id = 'f_' + Date.now();
  const icon = getFileIcon(name);
  const card = document.createElement('div');
  card.className = 'file-item'; card.id = id;
  card.innerHTML = `
    <div class="file-icon">${icon}</div>
    <div class="file-info">
      <div class="file-name">${name}</div>
      <div class="file-meta" id="${id}_meta">uploading…</div>
    </div>
    <span class="file-badge indexing" id="${id}_badge">⟳</span>
  `;
  list.appendChild(card);
  return id;
}

function updateFileCard(id, status, meta) {
  const badge = document.getElementById(id + '_badge');
  const metaEl = document.getElementById(id + '_meta');
  if (!badge) return;
  badge.className = 'file-badge ' + (status === 'indexed' ? '' : status);
  badge.textContent = status === 'indexed' ? '✓' : status === 'error' ? '✗' : '⟳';
  if (metaEl) metaEl.textContent = meta || '';
}

function getFileIcon(name) {
  const ext = name.split('.').pop().toLowerCase();
  const map = { pdf:'📄', docx:'📝', doc:'📝', txt:'📃', csv:'📊', xlsx:'📊', xls:'📊',
    pptx:'📑', ppt:'📑', html:'🌐', htm:'🌐', md:'📋' };
  return map[ext] || '📁';
}

async function refreshStats() {
  if (!initialized) return;
  try {
    const res = await fetch(`${API}/stats`);
    const data = await res.json();
    document.getElementById('statFiles').textContent = data.indexed_files?.length || 0;
    document.getElementById('statChunks').textContent = data.total_chunks || 0;
  } catch {}
}

// ── Send Query ──
async function sendQuery() {
  const input = document.getElementById('questionInput');
  const q = input.value.trim();
  if (!q || !initialized) return;

  input.value = '';
  input.style.height = '40px';

  hideEmpty();
  appendMessage('user', q);

  const thinkId = appendThinking();
  document.getElementById('sendBtn').disabled = true;

  try {
    const res = await fetch(`${API}/query`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: q })
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail);

    removeThinking(thinkId);
    appendMessage('ai', data.answer, data.sources);
  } catch (e) {
    removeThinking(thinkId);
    appendMessage('ai', '⚠ ' + (e.message || 'Query failed'), []);
  } finally {
    document.getElementById('sendBtn').disabled = false;
  }
}

function appendMessage(role, text, sources) {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = `msg ${role}`;

  const avatar = role === 'ai' ? '🤖' : '👤';
  let sourcesHTML = '';

  if (sources && sources.length > 0) {
    const chips = sources.map(s => `
      <span class="source-chip">
        <span class="src-icon">${getFileIcon(s.source)}</span>
        ${s.source}${s.page != null ? ' p.' + (s.page+1) : ''}
      </span>
    `).join('');
    const snippet = sources[0]?.snippet
      ? `<div class="source-snippet">"${sources[0].snippet.substring(0, 120)}…"</div>` : '';
    sourcesHTML = `<div class="sources">${chips}${snippet}</div>`;
  }

  div.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-bubble">
      <p>${text.replace(/\n/g, '<br/>')}</p>
      ${sourcesHTML}
    </div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}

function appendThinking() {
  const msgs = document.getElementById('messages');
  const id = 'think_' + Date.now();
  const div = document.createElement('div');
  div.className = 'msg ai'; div.id = id;
  div.innerHTML = `
    <div class="msg-avatar">🤖</div>
    <div class="msg-bubble">
      <div class="thinking">
        <div class="dots">
          <span></span><span></span><span></span>
        </div>
        Thinking…
      </div>
    </div>
  `;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
  return id;
}

function removeThinking(id) {
  document.getElementById(id)?.remove();
}

function hideEmpty() {
  document.getElementById('emptyState')?.remove();
}

// ── Reset ──
async function resetPipeline() {
  if (!initialized) return;
  if (!confirm('Clear all indexed documents and conversation history?')) return;
  await fetch(`${API}/reset`, { method: 'POST' });
  indexedFiles = [];
  document.getElementById('fileList').innerHTML = `
    <div style="font-size:12px;color:var(--muted);text-align:center;padding:20px 0;">
      No documents indexed yet
    </div>`;
  document.getElementById('messages').innerHTML = `
    <div class="empty-state" id="emptyState">
      <div class="empty-icon">🔍</div>
      <div class="empty-title">Ask anything about your documents</div>
      <div class="empty-sub">Upload files and start asking questions.</div>
    </div>`;
  document.getElementById('statFiles').textContent = '0';
  document.getElementById('statChunks').textContent = '0';
  showToast('Pipeline reset', 'success');
}

// ── Status ──
function setStatus(ready) {
  const dot = document.getElementById('statusDot');
  const txt = document.getElementById('statusText');
  dot.className = 'dot' + (ready ? ' ready' : '');
  txt.textContent = ready ? 'pipeline ready' : 'not initialized';
}

// ── Toast ──
function showToast(msg, type='') {
  const icon = type === 'success' ? '✓' : type === 'error' ? '✗' : 'ℹ';
  const t = document.createElement('div');
  t.className = `toast ${type}`;
  t.innerHTML = `<span class="toast-icon">${icon}</span>${msg}`;
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 3500);
}

// ── Drag & drop ──
const dz = document.getElementById('dropZone');
dz.addEventListener('dragover', e => { e.preventDefault(); dz.classList.add('drag'); });
dz.addEventListener('dragleave', () => dz.classList.remove('drag'));
dz.addEventListener('drop', e => {
  e.preventDefault(); dz.classList.remove('drag');
  handleFiles(e.dataTransfer.files);
});
</script>
</body>
</html>
