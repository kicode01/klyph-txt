/**
 * Klyph Ambient Companion HUD Client
 * Reactive, Local-First, 100% Deterministic NLP Bridge
 */

let clipboardWatcherActive = false;
let watcherInterval = null;
let lastClipboardText = "";
let debounceTimer = null;
let currentInspectionData = null;
let broadcastChannel = null;

// Initialize BroadcastChannel for cross-window synchronization
try {
  broadcastChannel = new BroadcastChannel('klyph_companion');
  broadcastChannel.onmessage = (event) => {
    if (event.data && event.data.type === 'SYNC_TEXT') {
      const inputEl = document.getElementById('hud-input');
      if (inputEl && event.data.text && inputEl.value !== event.data.text) {
        inputEl.value = event.data.text;
        triggerInspection();
      }
    }
  };
} catch (e) {
  console.warn('BroadcastChannel not supported in this environment');
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  setupEventListeners();

  // Check URL query parameters or localStorage for preloaded text
  const urlParams = new URLSearchParams(window.location.search);
  const queryText = urlParams.get('text');
  const pendingText = localStorage.getItem('klyph_pending_hud_text') || localStorage.getItem('openquill_pending_hud_text');

  const inputEl = document.getElementById('hud-input');
  if (queryText) {
    inputEl.value = queryText;
    triggerInspection();
  } else if (pendingText) {
    inputEl.value = pendingText;
    localStorage.removeItem('klyph_pending_hud_text');
    localStorage.removeItem('openquill_pending_hud_text');
    triggerInspection();
  } else {
    // Attempt one automatic clipboard read if permission already granted
    attemptSilentClipboardRead();
  }
});

// ------------------------------------------------------------
// Theme Toggle & Sync
// ------------------------------------------------------------
function updateDynamicFavicon(theme) {
  const isPaper = theme === 'paper';
  const iconFile = isPaper ? 'icon-light.svg' : 'icon-dark.svg';
  const timestamp = Date.now();
  const iconHref = `${iconFile}?v=${timestamp}`;

  try {
    const existingIcons = document.querySelectorAll("link[rel='icon'], link[rel='shortcut icon']");
    existingIcons.forEach(el => el.remove());

    const newFavicon = document.createElement('link');
    newFavicon.rel = 'icon';
    newFavicon.type = 'image/svg+xml';
    newFavicon.href = iconHref;
    document.head.appendChild(newFavicon);
  } catch (e) {
    console.warn('Favicon update error in HUD:', e);
  }

  const hudLogo = document.querySelector('.hud-logo');
  if (hudLogo) {
    hudLogo.src = iconFile;
  }
}

function initTheme() {
  const saved = localStorage.getItem('klyph_theme') || localStorage.getItem('openquill_theme') || 'slate';
  document.documentElement.setAttribute('data-theme', saved);
  updateDynamicFavicon(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'slate' ? 'paper' : 'slate';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('klyph_theme', next);
  updateDynamicFavicon(next);
}

// ------------------------------------------------------------
// Event Listeners & Keyboard Hotkeys
// ------------------------------------------------------------
function setupEventListeners() {
  const inputEl = document.getElementById('hud-input');
  if (inputEl) {
    inputEl.addEventListener('input', () => {
      triggerInspection();
    });
  }

  // Window Focus: check clipboard if watcher is active
  window.addEventListener('focus', () => {
    if (clipboardWatcherActive) {
      checkClipboardOnce();
    }
  });

  // Global Keyboard Shortcuts
  window.addEventListener('keydown', (e) => {
    // Esc: clear text
    if (e.key === 'Escape') {
      const input = document.getElementById('hud-input');
      if (input && input.value) {
        input.value = '';
        triggerInspection();
        showToast('Input cleared', 'info');
      }
      return;
    }

    // If typing in textarea, only handle specific keys
    const isTextarea = document.activeElement && document.activeElement.id === 'hud-input';

    if (e.key === 'Enter' && (e.ctrlKey || !isTextarea)) {
      e.preventDefault();
      applyQuickFixAndCopy();
    } else if (!isTextarea) {
      if (e.key.toLowerCase() === 'h') {
        e.preventDefault();
        applyHumanizeAndCopy();
      } else if (e.key.toLowerCase() === 'o') {
        e.preventDefault();
        openFullStudio();
      } else if (e.key.toLowerCase() === 'w') {
        e.preventDefault();
        toggleClipboardWatcher();
      }
    }
  });
}

// ------------------------------------------------------------
// View Switcher (Input vs Precision Diff)
// ------------------------------------------------------------
function switchHUDView(viewName) {
  const tabEditor = document.getElementById('tab-btn-editor');
  const tabDiff = document.getElementById('tab-btn-diff');
  const viewEditor = document.getElementById('hud-view-editor');
  const viewDiff = document.getElementById('hud-view-diff');

  if (viewName === 'editor') {
    tabEditor.classList.add('active');
    tabDiff.classList.remove('active');
    viewEditor.classList.add('active');
    viewDiff.classList.remove('active');
    document.getElementById('hud-input').focus();
  } else {
    tabDiff.classList.add('active');
    tabEditor.classList.remove('active');
    viewDiff.classList.add('active');
    viewEditor.classList.remove('active');
  }
}

// ------------------------------------------------------------
// Real-Time Inspection Pipeline
// ------------------------------------------------------------
function triggerInspection() {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    runInspection();
  }, 240);
}

async function runInspection() {
  const text = document.getElementById('hud-input').value.trim();
  
  if (!text) {
    resetHUDMetrics();
    return;
  }

  try {
    const res = await fetch('/api/companion/inspect', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    if (!res.ok) throw new Error('Companion inspection failed');
    const data = await res.json();
    currentInspectionData = data;
    renderHUDMetrics(data);
  } catch (err) {
    console.warn('Backend inspection unavailable, falling back to Client Neuro Engine:', err);
    if (window.clientNeuroEngine) {
      const clientData = window.clientNeuroEngine.inspectDocument(text);
      currentInspectionData = clientData;
      renderHUDMetrics(clientData);
    } else {
      console.error('Inspection error:', err);
    }
  }
}

function renderHUDMetrics(data) {
  // 1. Score Circle & Track
  const scoreValEl = document.getElementById('hud-score-value');
  const scoreTitleEl = document.getElementById('hud-score-title');
  const scoreFillEl = document.getElementById('hud-score-fill');

  const score = data.quality_score;
  scoreValEl.textContent = score;
  scoreFillEl.style.width = `${Math.max(5, score)}%`;

  let scoreColor = 'var(--color-emerald)';
  let title = 'Writing Pristine';
  if (score < 70) {
    scoreColor = 'var(--color-correctness)';
    title = 'Needs Polishing';
  } else if (score < 90) {
    scoreColor = 'var(--color-amber)';
    title = 'Good Quality';
  }

  scoreValEl.style.color = scoreColor;
  scoreFillEl.style.backgroundColor = scoreColor;
  scoreTitleEl.textContent = title;

  // 2. AI Spectrum Badge
  const aiBadgeEl = document.getElementById('hud-ai-badge');
  const aiLabelEl = document.getElementById('hud-ai-label');
  if (data.ai_probability > 45) {
    aiBadgeEl.style.color = 'var(--color-amber)';
    aiBadgeEl.style.borderColor = 'var(--color-amber)';
    aiBadgeEl.style.backgroundColor = 'var(--color-amber-bg)';
    aiLabelEl.textContent = `${Math.round(data.ai_probability)}% AI-Signal`;
  } else {
    aiBadgeEl.style.color = 'var(--color-emerald)';
    aiBadgeEl.style.borderColor = 'var(--color-emerald)';
    aiBadgeEl.style.backgroundColor = 'var(--color-emerald-bg)';
    aiLabelEl.textContent = `${Math.round(data.human_probability)}% Human`;
  }

  // 3. Telemetry Ribbon
  document.getElementById('hud-issues-count').textContent = `${data.total_issues} Issues`;
  document.getElementById('hud-habits-count').textContent = `${data.habit_clusters_count} Habits`;
  document.getElementById('hud-words-count').textContent = `${data.word_count} Words`;
  document.getElementById('hud-reading-time').textContent = `${data.reading_time_seconds}s read`;

  // 4. Diff View & Badge
  const diffCountEl = document.getElementById('hud-diff-count');
  const diffBoxEl = document.getElementById('hud-diff-box');

  if (data.total_issues > 0 && data.diff_html) {
    diffCountEl.textContent = data.total_issues;
    diffCountEl.style.display = 'inline-flex';
    diffBoxEl.innerHTML = data.diff_html;
  } else {
    diffCountEl.style.display = 'none';
    diffBoxEl.innerHTML = '<span class="diff-placeholder">No corrections needed. Input text is clear and accurate.</span>';
  }

  // 5. Habits Bar
  const habitsBarEl = document.getElementById('hud-habits-bar');
  const habitsListEl = document.getElementById('hud-habits-list');
  if (data.top_habits && data.top_habits.length > 0) {
    habitsBarEl.style.display = 'flex';
    habitsListEl.innerHTML = data.top_habits.map(h => `
      <span class="habit-tag" title="${h.category}: ${h.title}">
        <span>${h.title}</span>
        <strong>(${h.count})</strong>
      </span>
    `).join('');
  } else {
    habitsBarEl.style.display = 'none';
  }
}

function resetHUDMetrics() {
  document.getElementById('hud-score-value').textContent = '100';
  document.getElementById('hud-score-title').textContent = 'Writing Pristine';
  document.getElementById('hud-score-fill').style.width = '100%';
  document.getElementById('hud-score-fill').style.backgroundColor = 'var(--color-emerald)';
  document.getElementById('hud-score-value').style.color = 'var(--color-emerald)';

  document.getElementById('hud-ai-label').textContent = '100% Human';
  document.getElementById('hud-issues-count').textContent = '0 Issues';
  document.getElementById('hud-habits-count').textContent = '0 Habits';
  document.getElementById('hud-words-count').textContent = '0 Words';
  document.getElementById('hud-reading-time').textContent = '0s read';

  document.getElementById('hud-diff-count').style.display = 'none';
  document.getElementById('hud-diff-box').innerHTML = '<span class="diff-placeholder">No corrections needed. Input text is clear and accurate.</span>';
  document.getElementById('hud-habits-bar').style.display = 'none';
}

// ------------------------------------------------------------
// Clipboard Bridge & Watcher
// ------------------------------------------------------------
function toggleClipboardWatcher() {
  clipboardWatcherActive = !clipboardWatcherActive;
  const btn = document.getElementById('btn-watch-clipboard');
  const label = document.getElementById('watcher-label');

  if (clipboardWatcherActive) {
    btn.classList.add('active');
    label.textContent = 'Clipboard: ON';
    startClipboardPolling();
    checkClipboardOnce();
    showToast('Clipboard watcher enabled', 'info');
  } else {
    btn.classList.remove('active');
    label.textContent = 'Clipboard: Off';
    stopClipboardPolling();
    showToast('Clipboard watcher paused', 'info');
  }
}

function startClipboardPolling() {
  stopClipboardPolling();
  watcherInterval = setInterval(() => {
    checkClipboardOnce();
  }, 1400);
}

function stopClipboardPolling() {
  if (watcherInterval) {
    clearInterval(watcherInterval);
    watcherInterval = null;
  }
}

async function checkClipboardOnce() {
  try {
    if (!navigator.clipboard || !navigator.clipboard.readText) return;
    const text = await navigator.clipboard.readText();
    if (text && text.trim() && text !== lastClipboardText) {
      lastClipboardText = text;
      const inputEl = document.getElementById('hud-input');
      inputEl.value = text;
      triggerInspection();
      showToast('Detected text from clipboard', 'info');
    }
  } catch (e) {
    // User denied clipboard permission or window not focused
  }
}

async function attemptSilentClipboardRead() {
  try {
    if (navigator.clipboard && navigator.clipboard.readText) {
      const text = await navigator.clipboard.readText();
      if (text && text.trim().length > 3) {
        lastClipboardText = text;
        document.getElementById('hud-input').value = text;
        triggerInspection();
      }
    }
  } catch (e) {
    // Normal browser security restriction when not user-invoked
  }
}

async function pasteFromClipboard() {
  try {
    const text = await navigator.clipboard.readText();
    if (text) {
      lastClipboardText = text;
      const input = document.getElementById('hud-input');
      input.value = text;
      triggerInspection();
      showToast('Pasted from clipboard', 'info');
    }
  } catch (err) {
    showToast('Clipboard access denied. Press Ctrl+V directly in box.', 'error');
  }
}

// ------------------------------------------------------------
// Action 1: Fix All & Copy
// ------------------------------------------------------------
async function applyQuickFixAndCopy() {
  const inputEl = document.getElementById('hud-input');
  const text = inputEl.value.trim();
  if (!text) {
    showToast('Please enter text to fix', 'error');
    return;
  }

  const btn = document.getElementById('btn-hud-fix-all');
  btn.style.transform = 'scale(0.95)';
  setTimeout(() => btn.style.transform = '', 150);

  try {
    const res = await fetch('/api/companion/quick-fix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    if (!res.ok) throw new Error('Quick fix failed');
    const data = await res.json();

    const fixed = data.fixed_text;
    inputEl.value = fixed;
    lastClipboardText = fixed;

    // Write back to system clipboard
    await navigator.clipboard.writeText(fixed);

    // Sync with main window if active
    if (broadcastChannel) {
      broadcastChannel.postMessage({ type: 'SYNC_TEXT', text: fixed });
    }

    triggerInspection();
    showToast(`✓ Fixed ${data.count_fixed} items & copied to clipboard!`, 'success');
  } catch (err) {
    console.warn('Backend quick-fix unavailable, applying Client-Side Neurosymbolic fix:', err);
    if (window.clientNeuroEngine) {
      const fixed = window.clientNeuroEngine.applyLexicalTransforms(text);
      inputEl.value = fixed;
      lastClipboardText = fixed;
      await navigator.clipboard.writeText(fixed);
      if (broadcastChannel) {
        broadcastChannel.postMessage({ type: 'SYNC_TEXT', text: fixed });
      }
      triggerInspection();
      showToast('✓ Client Neuro-Fix applied & copied ($0.00)', 'success');
    } else {
      console.error('Quick fix error:', err);
      showToast('Error applying quick fix', 'error');
    }
  }
}

// ------------------------------------------------------------
// Action 2: De-AI Humanize & Copy
// ------------------------------------------------------------
async function applyHumanizeAndCopy() {
  const inputEl = document.getElementById('hud-input');
  const text = inputEl.value.trim();
  if (!text) {
    showToast('Please enter text to humanize', 'error');
    return;
  }

  const btn = document.getElementById('btn-hud-humanize');
  btn.style.transform = 'scale(0.95)';
  setTimeout(() => btn.style.transform = '', 150);

  try {
    const res = await fetch('/api/humanize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: text })
    });

    if (!res.ok) throw new Error('Humanize failed');
    const data = await res.json();

    const humanized = data.humanized_text;
    inputEl.value = humanized;
    lastClipboardText = humanized;

    // Write back to clipboard
    await navigator.clipboard.writeText(humanized);

    if (broadcastChannel) {
      broadcastChannel.postMessage({ type: 'SYNC_TEXT', text: humanized });
    }

    triggerInspection();
    showToast(`✓ De-AI humanized & copied to clipboard!`, 'success');
  } catch (err) {
    console.warn('Backend humanize unavailable, applying Client-Side Neurosymbolic de-AI:', err);
    if (window.clientNeuroEngine) {
      let humanized = window.clientNeuroEngine.applyLexicalTransforms(text);
      humanized = window.clientNeuroEngine.transposeClause(humanized);
      inputEl.value = humanized;
      lastClipboardText = humanized;
      await navigator.clipboard.writeText(humanized);
      if (broadcastChannel) {
        broadcastChannel.postMessage({ type: 'SYNC_TEXT', text: humanized });
      }
      triggerInspection();
      showToast('✓ Client De-AI applied & copied ($0.00)', 'success');
    } else {
      console.error('Humanize error:', err);
      showToast('Error applying humanizer', 'error');
    }
  }
}

// ------------------------------------------------------------
// Action 3: Open in Full Studio
// ------------------------------------------------------------
function openFullStudio() {
  const text = document.getElementById('hud-input').value;
  if (text) {
    localStorage.setItem('klyph_pending_import', text);
  }

  if (window.opener && !window.opener.closed) {
    window.opener.focus();
    if (text && window.opener.loadExternalText) {
      window.opener.loadExternalText(text);
    }
  } else {
    window.open('/', '_blank');
  }

  showToast('Opened Studio in browser', 'info');
}

// ------------------------------------------------------------
// Toast Notification System
// ------------------------------------------------------------
let toastTimer = null;
function showToast(message, type = 'success') {
  const toastEl = document.getElementById('hud-toast');
  const msgEl = document.getElementById('hud-toast-msg');
  const iconEl = document.getElementById('hud-toast-icon');

  if (!toastEl) return;

  clearTimeout(toastTimer);
  msgEl.textContent = message;

  if (type === 'success') {
    iconEl.textContent = '✓';
    toastEl.style.borderColor = 'var(--color-emerald)';
    toastEl.style.color = 'var(--color-emerald)';
  } else if (type === 'error') {
    iconEl.textContent = '✕';
    toastEl.style.borderColor = 'var(--color-correctness)';
    toastEl.style.color = 'var(--color-correctness)';
  } else {
    iconEl.textContent = 'ℹ';
    toastEl.style.borderColor = 'var(--color-accent)';
    toastEl.style.color = 'var(--color-accent)';
  }

  toastEl.style.display = 'flex';
  toastTimer = setTimeout(() => {
    toastEl.style.display = 'none';
  }, 2200);
}
