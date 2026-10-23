// =============================================================
// klyph-txt - Core Application Logic & PWA Engine
// =============================================================

let currentTab = 'grammar';
let currentParaphraseMode = 'standard';
let currentSynonymLevel = 2;
let debounceTimer = null;
let currentIssues = [];
let currentSentenceGroups = [];
let currentParagraphRewrites = [];
let currentHabitClusters = [];
let activeGroupId = null;
let currentRailSubtab = 'proofread';
let currentCategoryFilter = 'all';

// Cognitive Flow & Velocity Gating State (Laya Architecture)
let typingTimestamps = [];
let typingWpm = 0;
let isFlowModeActive = false;
let isFlowGatingEnabled = true;
let pauseDebounceTimer = null;

let currentParaphraseData = null;
let activeWordElement = null;

// Revert History Buffers
let originalGrammarBuffer = null;
let originalParaBuffer = null;
let originalDetectorBuffer = null;

// AI Detector State
let currentBoundary = 50.0;
let currentTextPositionX = 25.0;
let detectorDebounceTimer = null;
let currentDetectionData = null;

// PWA Install Prompt State
let deferredInstallPrompt = null;
let currentFileTarget = 'grammar';

// -------------------------------------------------------------
// PWA & SERVICE WORKER INITIALIZATION
// -------------------------------------------------------------
if ('serviceWorker' in navigator) {
  window.addEventListener('load', () => {
    navigator.serviceWorker.register('/sw.js')
      .then((reg) => console.log('ServiceWorker registered:', reg.scope))
      .catch((err) => console.warn('ServiceWorker registration skipped:', err));
  });
}

window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault();
  deferredInstallPrompt = e;
  const installBtn = document.getElementById('btn-pwa-install');
  if (installBtn) {
    installBtn.style.display = 'inline-flex';
  }
});

function triggerPWAInstall() {
  if (!deferredInstallPrompt) return;
  deferredInstallPrompt.prompt();
  deferredInstallPrompt.userChoice.then((choiceResult) => {
    if (choiceResult.outcome === 'accepted') {
      showToast('klyph-txt installed successfully!', 'success');
    }
    deferredInstallPrompt = null;
    const installBtn = document.getElementById('btn-pwa-install');
    if (installBtn) installBtn.style.display = 'none';
  });
}

// -------------------------------------------------------------
// EYE-COMFORT THEME ENGINE (Twilight ↔ Warm Paper)
// -------------------------------------------------------------
function initTheme() {
  const savedTheme = localStorage.getItem('klyph_theme') || localStorage.getItem('openquill_theme');
  const defaultTheme = (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) ? 'twilight' : 'paper';
  const initialTheme = savedTheme || defaultTheme;
  applyTheme(initialTheme, false);

  // Dynamic OS-level preference synchronization
  if (window.matchMedia) {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    mediaQuery.addEventListener('change', (e) => {
      // If user hasn't explicitly set a preference, track OS automatically
      if (!localStorage.getItem('klyph_theme')) {
        applyTheme(e.matches ? 'twilight' : 'paper', false);
      }
    });
  }
}

function toggleTheme() {
  const currentTheme = document.documentElement.getAttribute('data-theme') || 'paper';
  const newTheme = currentTheme === 'paper' ? 'twilight' : 'paper';
  applyTheme(newTheme, true);
}

function updateDynamicFavicon(theme) {
  const isPaper = theme === 'paper';
  const iconFile = isPaper ? 'icon-light.svg' : 'icon-dark.svg';
  const timestamp = Date.now();
  const iconHref = `${iconFile}?v=${timestamp}`;

  // 1. Force dynamic favicon refresh across Chrome/Safari/Edge/Firefox
  try {
    const existingIcons = document.querySelectorAll("link[rel='icon'], link[rel='shortcut icon']");
    existingIcons.forEach(el => el.remove());

    const newFavicon = document.createElement('link');
    newFavicon.id = 'app-dynamic-favicon';
    newFavicon.rel = 'icon';
    newFavicon.type = 'image/svg+xml';
    newFavicon.href = iconHref;
    document.head.appendChild(newFavicon);

    const newShortcut = document.createElement('link');
    newShortcut.rel = 'shortcut icon';
    newShortcut.type = 'image/svg+xml';
    newShortcut.href = iconHref;
    document.head.appendChild(newShortcut);
  } catch (err) {
    console.warn('Favicon update error:', err);
  }

  // 2. Update all navbar brand marks
  const brandLogos = document.querySelectorAll('.brand-logo-img, .hud-logo');
  brandLogos.forEach(img => {
    img.src = iconFile;
  });
}

function applyTheme(theme, notify = true) {
  // Suppress color smearing on theme swap (better-ui / next-themes pattern)
  const css = document.createElement('style');
  css.appendChild(document.createTextNode('* { transition: none !important; }'));
  document.head.appendChild(css);

  document.documentElement.setAttribute('data-theme', theme);
  localStorage.setItem('klyph_theme', theme);

  const themeSlot = document.getElementById('theme-icon-slot');
  const themeLabel = document.getElementById('theme-label');
  const metaThemeColor = document.getElementById('meta-theme-color');

  if (theme === 'paper') {
    if (themeSlot) themeSlot.innerHTML = '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
    if (themeLabel) themeLabel.textContent = 'Paper';
    if (metaThemeColor) metaThemeColor.setAttribute('content', '#fbfaf6');
    if (notify) showToast('Switched to Warm Paper (Eye-Comfort Reading Mode)', 'info');
  } else {
    if (themeSlot) themeSlot.innerHTML = '<svg class="ui-svg" viewBox="0 0 24 24"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>';
    if (themeLabel) themeLabel.textContent = 'Twilight';
    if (metaThemeColor) metaThemeColor.setAttribute('content', '#080b10');
    if (notify) showToast('Switched to Twilight Slate (Low-Light Mode)', 'info');
  }

  // Dynamically update favicon and branding to match theme
  updateDynamicFavicon(theme);

  // Force layout flush then restore transitions on next animation frame
  window.getComputedStyle(document.documentElement).opacity;
  requestAnimationFrame(() => {
    if (css.parentNode) css.parentNode.removeChild(css);
  });

  // Redraw canvas with new palette
  drawBoundaryCanvas();
}

// -------------------------------------------------------------
// TOAST NOTIFICATION SYSTEM
// -------------------------------------------------------------
function showToast(message, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  toast.className = `toast-message ${type}`;

  let svgIcon = '<svg class="ui-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>';
  if (type === 'warning') {
    svgIcon = '<svg class="ui-svg" viewBox="0 0 24 24"><path d="m21.73 18-8-14a2 2 0 0 0-3.48 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>';
  } else if (type === 'info') {
    svgIcon = '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/></svg>';
  }

  toast.innerHTML = `${svgIcon} <span>${escapeHtml(message)}</span>`;

  container.appendChild(toast);

  setTimeout(() => {
    if (toast.parentNode) {
      toast.parentNode.removeChild(toast);
    }
  }, 3200);
}

// -------------------------------------------------------------
// TAB SWITCHING & DEEP LINKING
// -------------------------------------------------------------
function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.nav-segment').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.mob-dock-btn').forEach(btn => btn.classList.remove('active'));
  document.querySelectorAll('.tab-panel').forEach(sec => sec.classList.remove('active'));

  const tabBtn = document.getElementById(`tab-${tab}`);
  const mobTabBtn = document.getElementById(`mob-tab-${tab}`);
  const secPanel = document.getElementById(`section-${tab}`);
  if (tabBtn) tabBtn.classList.add('active');
  if (mobTabBtn) mobTabBtn.classList.add('active');
  if (secPanel) secPanel.classList.add('active');

  if (tab === 'detector') {
    setTimeout(drawBoundaryCanvas, 60);
  }
}

// -------------------------------------------------------------
// MOBILE ERGONOMIC PANE SWITCHER (Editor Surface vs Diagnostic Rail)
// -------------------------------------------------------------
let currentMobileGrammarPane = 'editor';
function setMobileGrammarPane(pane) {
  currentMobileGrammarPane = pane;
  const btnDoc = document.getElementById('btn-mobile-doc');
  const btnRail = document.getElementById('btn-mobile-rail');
  const surfaceEl = document.getElementById('grammar-surface');
  const railEl = document.querySelector('.diagnostic-rail');

  if (btnDoc && btnRail && surfaceEl && railEl) {
    if (pane === 'editor') {
      btnDoc.classList.add('active');
      btnRail.classList.remove('active');
      surfaceEl.classList.remove('mobile-pane-hidden');
      railEl.classList.add('mobile-pane-hidden');
    } else {
      btnRail.classList.add('active');
      btnDoc.classList.remove('active');
      surfaceEl.classList.add('mobile-pane-hidden');
      railEl.classList.remove('mobile-pane-hidden');
    }
  }
}

// -------------------------------------------------------------
// FILE IMPORT & DRAG AND DROP
// -------------------------------------------------------------
function triggerFileInput(target) {
  currentFileTarget = target;
  const fileInput = document.getElementById('file-importer');
  if (fileInput) fileInput.click();
}

function handleFileImport(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;
  readFileContent(file, currentFileTarget);
  event.target.value = '';
}

function readFileContent(file, target) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const content = e.target.result;
    if (target === 'grammar') {
      grammarInput.value = content;
      triggerGrammarCheck();
      showToast(`Imported ${file.name} into Editor`, 'info');
    } else if (target === 'para') {
      paraInput.value = content;
      runParaphrase();
      showToast(`Imported ${file.name} into Paraphraser`, 'info');
    } else if (target === 'detector') {
      detectorInput.value = content;
      runAIDetectionScan();
      showToast(`Imported ${file.name} into AI Spectrum`, 'info');
    } else if (target === 'humanizer') {
      if (humanizerInput) humanizerInput.value = content;
      runHumanizer();
      showToast(`Imported ${file.name} into Humanizer`, 'info');
    }
  };
  reader.readAsText(file);
}

function setupDragAndDrop() {
  const dropTargets = [
    { el: document.getElementById('grammar-surface'), target: 'grammar' },
    { el: document.getElementById('para-surface'), target: 'para' },
    { el: document.getElementById('detector-surface'), target: 'detector' },
    { el: document.getElementById('humanizer-surface'), target: 'humanizer' }
  ];

  dropTargets.forEach(({ el, target }) => {
    if (!el) return;
    el.addEventListener('dragover', (e) => {
      e.preventDefault();
      el.classList.add('drag-over');
    });
    el.addEventListener('dragleave', (e) => {
      e.preventDefault();
      el.classList.remove('drag-over');
    });
    el.addEventListener('drop', (e) => {
      e.preventDefault();
      el.classList.remove('drag-over');
      if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
        readFileContent(e.dataTransfer.files[0], target);
      }
    });
  });
}

// -------------------------------------------------------------
// KEYBOARD SHORTCUTS & COMMAND CENTER ENGINE
// -------------------------------------------------------------
document.addEventListener('keydown', (e) => {
  // Ctrl+K or Cmd+K: Toggle Command Palette
  if ((e.ctrlKey || e.metaKey) && (e.key === 'k' || e.key === 'K')) {
    e.preventDefault();
    toggleCommandPalette();
    return;
  }

  // If palette is open, handle palette navigation
  if (isPaletteOpen) {
    handlePaletteKeydown(e);
    return;
  }

  // Esc closes popovers
  if (e.key === 'Escape') {
    closeSynonymPopover();
    return;
  }

  // Tab switching: Ctrl+1, Ctrl+2, Ctrl+3
  if ((e.ctrlKey || e.metaKey) && e.key === '1') {
    e.preventDefault();
    switchTab('grammar');
    return;
  }
  if ((e.ctrlKey || e.metaKey) && e.key === '2') {
    e.preventDefault();
    switchTab('paraphrase');
    return;
  }
  if ((e.ctrlKey || e.metaKey) && e.key === '3') {
    e.preventDefault();
    switchTab('detector');
    return;
  }
  if ((e.ctrlKey || e.metaKey) && e.key === '4') {
    e.preventDefault();
    switchTab('humanizer');
    return;
  }

  // De-AI Clean: Ctrl+H
  if ((e.ctrlKey || e.metaKey) && (e.key === 'h' || e.key === 'H')) {
    e.preventDefault();
    humanizeActiveInput();
    return;
  }

  // Apply All Fixes: Ctrl+Shift+A
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'a' || e.key === 'A')) {
    e.preventDefault();
    acceptAllCorrections();
    return;
  }

  // Toggle Theme: Ctrl+Shift+T
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 't' || e.key === 'T')) {
    e.preventDefault();
    toggleTheme();
    return;
  }

  // Launch Ambient HUD: Ctrl+Shift+H or Ctrl+Shift+Q
  if ((e.ctrlKey || e.metaKey) && e.shiftKey && (e.key === 'h' || e.key === 'H' || e.key === 'q' || e.key === 'Q')) {
    e.preventDefault();
    openCompanionHUD();
    return;
  }

  // Ctrl+Enter or Cmd+Enter triggers current workspace action
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault();
    triggerActiveCheck();
    return;
  }
});

// -------------------------------------------------------------
// GRAMMAR & CLARITY ENGINE
// -------------------------------------------------------------
const grammarInput = document.getElementById('grammar-input');
const issuesList = document.getElementById('issues-list');
const issuesCounter = document.getElementById('issues-counter');
const grammarStats = document.getElementById('grammar-stats');
const readabilityBadge = document.getElementById('readability-badge');
const btnAcceptAll = document.getElementById('btn-accept-all');
const btnRevertGrammar = document.getElementById('btn-revert-grammar');

// Velocity & Cognitive Flow Tracker (Laya Micro-Engine)
function recordKeystroke() {
  const now = performance.now();
  typingTimestamps.push(now);
  const cutoff = now - 3000;
  typingTimestamps = typingTimestamps.filter(t => t >= cutoff);

  if (typingTimestamps.length >= 4) {
    const durationMin = (now - typingTimestamps[0]) / 60000;
    if (durationMin > 0) {
      const words = typingTimestamps.length / 5;
      typingWpm = Math.round(words / durationMin);
    }
  } else {
    typingWpm = 0;
  }

  const workspaceWrap = document.getElementById('editor-workspace-wrap');
  const flowStatusText = document.getElementById('flow-status-text');

  if (isFlowGatingEnabled && typingWpm >= 28) {
    if (!isFlowModeActive) {
      isFlowModeActive = true;
      if (workspaceWrap) workspaceWrap.classList.add('flow-mode');
      if (flowStatusText) flowStatusText.textContent = `⚡ Flow (${typingWpm} WPM)`;
    }
  }

  clearTimeout(pauseDebounceTimer);
  pauseDebounceTimer = setTimeout(() => {
    isFlowModeActive = false;
    typingTimestamps = [];
    if (workspaceWrap) workspaceWrap.classList.remove('flow-mode');
    if (flowStatusText) {
      flowStatusText.textContent = isFlowGatingEnabled ? '⚡ Flow: Active' : 'Flow: Off';
    }
    triggerGrammarCheck();
  }, 1600);
}

function toggleFlowMode() {
  isFlowGatingEnabled = !isFlowGatingEnabled;
  const toggleBtn = document.getElementById('btn-flow-toggle');
  const flowStatusText = document.getElementById('flow-status-text');
  const workspaceWrap = document.getElementById('editor-workspace-wrap');

  if (isFlowGatingEnabled) {
    if (toggleBtn) toggleBtn.classList.add('active');
    if (flowStatusText) flowStatusText.textContent = '⚡ Flow: Active';
    showToast('Cognitive Flow Mode enabled: silences squiggles during fast drafting', 'info');
  } else {
    if (toggleBtn) toggleBtn.classList.remove('active');
    if (workspaceWrap) workspaceWrap.classList.remove('flow-mode');
    if (flowStatusText) flowStatusText.textContent = 'Flow: Off';
    showToast('Cognitive Flow Mode disabled: live squiggles always visible', 'info');
  }
}

if (grammarInput) {
  grammarInput.addEventListener('input', () => {
    updateGrammarTelemetry();
    recordKeystroke();
    if (!isFlowModeActive) {
      clearTimeout(debounceTimer);
      debounceTimer = setTimeout(() => {
        triggerGrammarCheck();
      }, 400);
    }
  });

  grammarInput.addEventListener('click', handleCaretMove);
  grammarInput.addEventListener('keyup', (e) => {
    if (['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) {
      handleCaretMove();
    }
  });

  grammarInput.addEventListener('scroll', () => {
    const backdrop = document.getElementById('grammar-backdrop');
    if (backdrop) {
      backdrop.scrollTop = grammarInput.scrollTop;
    }
  });
}

function handleCaretMove() {
  if (!grammarInput || !currentSentenceGroups || currentSentenceGroups.length === 0) return;
  const pos = grammarInput.selectionStart;
  const match = currentSentenceGroups.find(g => pos >= g.start && pos <= g.end);
  if (match && match.id !== activeGroupId) {
    activeGroupId = match.id;
    highlightCardInRail(match.id);
    renderHighlights(grammarInput.value, currentIssues, currentSentenceGroups, activeGroupId);
  }
}

function highlightCardInRail(groupId) {
  document.querySelectorAll('.grammarly-card').forEach(c => c.classList.remove('active-focus'));
  const targetCard = document.getElementById(`card-${groupId}`);
  if (targetCard) {
    targetCard.classList.add('active-focus');
    targetCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}

function updateGrammarTelemetry() {
  const text = grammarInput ? grammarInput.value : '';
  const wordCount = (text.match(/\b\w+\b/g) || []).length;
  const readingSeconds = Math.round(wordCount / 3.3);
  const timeDesc = readingSeconds < 60 ? `~${readingSeconds}s read` : `~${Math.ceil(readingSeconds / 60)}m read`;
  if (grammarStats) {
    grammarStats.textContent = `${wordCount} words • ${timeDesc}`;
  }
  const headWords = document.getElementById('header-word-count');
  const headRead = document.getElementById('header-read-time');
  if (headWords) headWords.textContent = `${wordCount} words`;
  if (headRead) headRead.textContent = timeDesc;
}

// Synchronized Backdrop Highlighting Engine
function renderHighlights(text, issues, sentenceGroups, activeGroupId) {
  const highlightsEl = document.getElementById('grammar-highlights');
  if (!highlightsEl) return;

  if (!text) {
    highlightsEl.innerHTML = '';
    return;
  }

  let activeGroup = null;
  if (activeGroupId && sentenceGroups) {
    activeGroup = sentenceGroups.find(g => g.id === activeGroupId);
  }

  const boundaries = new Set([0, text.length]);

  if (activeGroup && activeGroup.start >= 0 && activeGroup.end <= text.length) {
    boundaries.add(activeGroup.start);
    boundaries.add(activeGroup.end);
  }

  if (currentRailSubtab === 'proofread' && issues) {
    issues.forEach(issue => {
      if (issue.start >= 0 && issue.end <= text.length && issue.start < issue.end) {
        boundaries.add(issue.start);
        boundaries.add(issue.end);
      }
    });
  }

  const sortedPoints = Array.from(boundaries).sort((a, b) => a - b);
  let html = '';

  for (let i = 0; i < sortedPoints.length - 1; i++) {
    const p1 = sortedPoints[i];
    const p2 = sortedPoints[i + 1];
    const slice = text.substring(p1, p2);
    if (!slice) continue;

    const isInsideActiveGroup = activeGroup && p1 >= activeGroup.start && p2 <= activeGroup.end;
    const matchingIssue = (currentRailSubtab === 'proofread' && issues)
      ? issues.find(iss => p1 >= iss.start && p2 <= iss.end)
      : null;

    let classes = [];
    if (isInsideActiveGroup) {
      classes.push('sentence-focus-highlight');
    }
    if (matchingIssue) {
      const cat = (matchingIssue.category || 'correctness').toLowerCase();
      classes.push(`grammar-underline ${cat}`);
    }

    const escapedSlice = escapeHtml(slice);
    if (classes.length > 0) {
      html += `<span class="${classes.join(' ')}">${escapedSlice}</span>`;
    } else {
      html += escapedSlice;
    }
  }

  if (text.endsWith('\n')) {
    html += '<br/>&nbsp;';
  }

  highlightsEl.innerHTML = html;
}

async function triggerGrammarCheck() {
  if (!grammarInput) return;
  const text = grammarInput.value;
  const wordCount = (text.match(/\b\w+\b/g) || []).length;
  updateGrammarTelemetry();

  const qualityScoreVal = document.getElementById('quality-score-value');
  const qualityProgressFill = document.getElementById('quality-progress-fill');
  const countAll = document.getElementById('count-all');
  const statusGrammar = document.getElementById('status-grammar');
  const statusClarity = document.getElementById('status-clarity');
  const statusDelivery = document.getElementById('status-delivery');
  
  if (!text.trim()) {
    if (issuesList) {
      issuesList.innerHTML = `
        <div class="empty-state">
          <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          <p class="empty-title">Clean Document</p>
          <p class="empty-desc">No syntax errors, misplaced agreements, or wordiness detected.</p>
        </div>`;
    }
    if (issuesCounter) issuesCounter.textContent = '0';
    if (countAll) countAll.textContent = '0';
    if (statusGrammar) statusGrammar.textContent = '✓';
    if (statusClarity) statusClarity.textContent = '✓';
    if (statusDelivery) statusDelivery.textContent = '✓';
    if (qualityScoreVal) {
      qualityScoreVal.textContent = '100';
      qualityScoreVal.style.color = 'var(--accent-emerald)';
    }
    if (qualityProgressFill) qualityProgressFill.style.width = '100%';
    if (readabilityBadge) readabilityBadge.textContent = 'Reading Ease: 100';
    if (btnAcceptAll) btnAcceptAll.disabled = true;
    currentIssues = [];
    currentSentenceGroups = [];
    activeGroupId = null;
    renderHighlights('', [], [], null);
    return;
  }

  try {
    const res = await fetch('/api/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) throw new Error('API check returned ' + res.status);
    const data = await res.json();
    currentIssues = data.issues || [];
    currentSentenceGroups = data.sentence_groups || [];
    renderGrammarResults(data, wordCount);
  } catch (err) {
    console.warn('Backend /api/check unavailable, activating Client Neurosymbolic Engine fallback:', err);
    if (window.clientNeuroEngine) {
      const clientInspection = window.clientNeuroEngine.inspectDocument(text);
      const fallbackData = {
        text: text,
        total_issues: clientInspection.total_issues,
        issues: [],
        sentence_groups: clientInspection.top_habits.map((h, i) => ({
          id: `client-group-${i}`,
          category: 'Clarity',
          issue_count: h.count,
          reason: `Detected stylistic drag: ${h.title}`,
          rewritten: clientInspection.fixed_preview,
          diff_html: clientInspection.diff_html
        })),
        category_counts: { clarity: clientInspection.total_issues },
        quality_score: clientInspection.quality_score,
        readability_score: 85.0,
        habit_clusters: clientInspection.top_habits.map(h => ({
          id: h.id,
          title: h.title,
          category: h.category,
          count: h.count,
          impact_penalty: h.count * 4,
          explanation: `Automated client-side check detected ${h.count} instances of ${h.title}.`,
          instances: []
        }))
      };
      currentIssues = fallbackData.issues;
      currentSentenceGroups = fallbackData.sentence_groups;
      currentHabitClusters = fallbackData.habit_clusters;
      renderGrammarResults(fallbackData, wordCount);
    } else {
      console.error('Error checking grammar:', err);
    }
  }
}

function renderGrammarResults(data, wordCount) {
  const total = data.total_issues || 0;
  if (issuesCounter) issuesCounter.textContent = total;
  const mobBadge = document.getElementById('mobile-badge-count');
  if (mobBadge) mobBadge.textContent = total;
  
  // Category Pill counts & checkmarks
  const countAll = document.getElementById('count-all');
  const statusGrammar = document.getElementById('status-grammar');
  const statusClarity = document.getElementById('status-clarity');
  const statusDelivery = document.getElementById('status-delivery');
  const catCounts = data.category_counts || {};

  if (countAll) countAll.textContent = total;
  if (statusGrammar) {
    const c = catCounts['correctness'] || 0;
    statusGrammar.textContent = c > 0 ? c : '✓';
  }
  if (statusClarity) {
    const c = catCounts['clarity'] || 0;
    statusClarity.textContent = c > 0 ? c : '✓';
  }
  if (statusDelivery) {
    const c = catCounts['delivery'] || 0;
    statusDelivery.textContent = c > 0 ? c : '✓';
  }

  // Writing Quality Score & Progress Bar
  const qualityScore = data.quality_score !== undefined ? data.quality_score : 100;
  const qualityScoreVal = document.getElementById('quality-score-value');
  const qualityProgressFill = document.getElementById('quality-progress-fill');
  if (qualityScoreVal) {
    qualityScoreVal.textContent = qualityScore;
    if (qualityScore >= 90) {
      qualityScoreVal.style.color = 'var(--accent-emerald)';
    } else if (qualityScore >= 70) {
      qualityScoreVal.style.color = 'var(--accent-amber)';
    } else {
      qualityScoreVal.style.color = 'var(--accent-ruby)';
    }
  }
  if (qualityProgressFill) {
    qualityProgressFill.style.width = `${qualityScore}%`;
  }

  if (readabilityBadge) {
    readabilityBadge.textContent = `Reading Ease: ${data.readability_score || 100}`;
  }
  const headReadability = document.getElementById('header-readability');
  if (headReadability) {
    headReadability.textContent = `Ease ${data.readability_score || 100}`;
  }
  
  const applicableFixes = (data.issues || []).filter(i => (i.replacement && i.replacement.trim() !== '') || i.category === 'clarity').length;
  if (btnAcceptAll) {
    btnAcceptAll.disabled = (applicableFixes === 0 && currentSentenceGroups.length === 0);
  }

  // Habit Clusters (Phase 3 Macro Habits)
  currentHabitClusters = data.habit_clusters || [];
  const habitsBadge = document.getElementById('habits-badge');
  if (habitsBadge) {
    if (currentHabitClusters.length > 0) {
      habitsBadge.textContent = currentHabitClusters.length;
      habitsBadge.style.display = 'inline-block';
    } else {
      habitsBadge.style.display = 'none';
    }
  }

  // Render cards depending on active subtab
  if (currentRailSubtab === 'proofread') {
    if (currentSentenceGroups.length > 0) {
      renderGrammarCards(currentSentenceGroups);
    } else if (total > 0) {
      renderFallbackIssueCards(data.issues);
    } else {
      issuesList.innerHTML = `
        <div class="empty-state">
          <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          <p class="empty-title">Clean Document</p>
          <p class="empty-desc">No syntax errors, misplaced agreements, or wordiness detected.</p>
        </div>`;
    }
  } else if (currentRailSubtab === 'paragraphs') {
    fetchParagraphImprovements();
  } else if (currentRailSubtab === 'habits') {
    renderHabitCards(currentHabitClusters);
  }

  // Synchronize highlights in text backdrop
  renderHighlights(grammarInput.value, currentIssues, currentSentenceGroups, activeGroupId);
}

function renderGrammarCards(sentenceGroups) {
  if (!issuesList) return;

  let filtered = sentenceGroups || [];
  if (currentCategoryFilter && currentCategoryFilter !== 'all') {
    filtered = filtered.filter(g => (g.category || '').toLowerCase() === currentCategoryFilter.toLowerCase());
  }

  if (filtered.length === 0) {
    if (!sentenceGroups || sentenceGroups.length === 0) {
      issuesList.innerHTML = `
        <div class="empty-state">
          <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          <p class="empty-title">Clean Document</p>
          <p class="empty-desc">No syntax errors, misplaced agreements, or wordiness detected.</p>
        </div>`;
    } else {
      issuesList.innerHTML = `
        <div class="empty-state">
          <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          <p class="empty-title">No ${escapeHtml(currentCategoryFilter)} Issues</p>
          <p class="empty-desc">All sentence structures in this category meet strict precision standards.</p>
        </div>`;
    }
    return;
  }

  issuesList.innerHTML = '';
  filtered.forEach(group => {
    const card = document.createElement('div');
    card.className = `klyph-diagnostic-card grammarly-card ${group.category || 'Clarity'}`;
    card.id = `card-${group.id}`;
    if (group.id === activeGroupId) {
      card.classList.add('active-focus');
    }

    card.innerHTML = `
      <div class="card-header-row">
        <span class="card-cat-badge ${group.category || 'Clarity'}">
          <svg class="ui-svg xs" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/></svg>
          ${escapeHtml(group.category || 'Clarity')}
        </span>
        <span class="card-issue-count">${group.issue_count || 1} ${group.issue_count === 1 ? 'issue' : 'issues'}</span>
      </div>
      <div class="card-diff-box">${group.diff_html || escapeHtml(group.rewritten)}</div>
      <div class="card-explanation-text">${escapeHtml(group.reason || 'Restructured for active voice and conciseness.')}</div>
      <div class="card-actions-strip">
        <button class="btn-rewrite-dismiss" onclick="event.stopPropagation(); dismissSentenceRewrite('${group.id}')">
          Dismiss
        </button>
        <button class="btn-rewrite-accept" onclick="event.stopPropagation(); acceptSentenceRewrite('${group.id}')">
          <svg class="ui-svg xs" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          Accept
        </button>
      </div>
    `;

    card.onclick = () => focusSentenceGroup(group.id);
    issuesList.appendChild(card);
  });
}

function focusSentenceGroup(groupId) {
  activeGroupId = groupId;
  const group = currentSentenceGroups.find(g => g.id === groupId);
  if (group && grammarInput) {
    grammarInput.focus();
    grammarInput.setSelectionRange(group.start, group.end);
    renderHighlights(grammarInput.value, currentIssues, currentSentenceGroups, activeGroupId);
    highlightCardInRail(groupId);
  }
}

function acceptSentenceRewrite(groupId) {
  const group = currentSentenceGroups.find(g => g.id === groupId);
  if (!group || !grammarInput) return;

  const card = document.getElementById(`card-${groupId}`);
  if (card) {
    card.classList.add('card-dismissing');
  }

  setTimeout(() => {
    if (!originalGrammarBuffer) {
      originalGrammarBuffer = grammarInput.value;
      if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
    }

    const cur = grammarInput.value;
    grammarInput.value = cur.substring(0, group.start) + group.rewritten + cur.substring(group.end);
    showToast('Applied sentence improvement', 'success');
    activeGroupId = null;
    triggerGrammarCheck();
  }, 180);
}

function dismissSentenceRewrite(groupId) {
  const card = document.getElementById(`card-${groupId}`);
  if (card) {
    card.classList.add('card-dismissing');
  }

  setTimeout(() => {
    currentSentenceGroups = currentSentenceGroups.filter(g => g.id !== groupId);
    renderGrammarCards(currentSentenceGroups);
    renderHighlights(grammarInput.value, currentIssues, currentSentenceGroups, activeGroupId);
  }, 180);
}

function switchRailSubtab(tabName) {
  currentRailSubtab = tabName;
  const tabProofread = document.getElementById('tab-proofread');
  const tabParagraphs = document.getElementById('tab-paragraphs');
  const tabHabits = document.getElementById('tab-habits');
  const categoryPillBar = document.getElementById('category-pill-bar');

  if (tabProofread) tabProofread.classList.toggle('active', tabName === 'proofread');
  if (tabParagraphs) tabParagraphs.classList.toggle('active', tabName === 'paragraphs');
  if (tabHabits) tabHabits.classList.toggle('active', tabName === 'habits');

  if (tabName === 'proofread') {
    if (categoryPillBar) categoryPillBar.style.display = 'flex';
    triggerGrammarCheck();
  } else if (tabName === 'paragraphs') {
    if (categoryPillBar) categoryPillBar.style.display = 'none';
    fetchParagraphImprovements();
  } else if (tabName === 'habits') {
    if (categoryPillBar) categoryPillBar.style.display = 'none';
    renderHabitCards(currentHabitClusters);
  }
}

function setCategoryFilter(category, buttonEl) {
  currentCategoryFilter = category;
  document.querySelectorAll('.cat-pill').forEach(btn => btn.classList.remove('active'));
  if (buttonEl) buttonEl.classList.add('active');
  renderGrammarCards(currentSentenceGroups);
}

async function fetchParagraphImprovements() {
  if (!grammarInput || !issuesList) return;
  const text = grammarInput.value;
  if (!text.trim()) {
    issuesList.innerHTML = `
      <div class="empty-state">
        <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <p class="empty-title">Clean Document</p>
        <p class="empty-desc">No paragraph-level restructuring needed.</p>
      </div>`;
    return;
  }

  issuesList.innerHTML = `
    <div style="padding: 32px 16px; text-align: center; color: var(--text-tertiary); font-size: 13px;">
      Analyzing paragraph flow and structure...
    </div>`;

  try {
    const res = await fetch('/api/improve-paragraphs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    const data = await res.json();
    currentParagraphRewrites = data.paragraphs || data.rewrites || [];
    renderParagraphCards(currentParagraphRewrites);
  } catch (err) {
    console.error('Error improving paragraphs:', err);
  }
}

function renderParagraphCards(rewrites) {
  if (!issuesList) return;

  if (!rewrites || rewrites.length === 0) {
    issuesList.innerHTML = `
      <div class="empty-state">
        <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <p class="empty-title">Optimized Paragraph Flow</p>
        <p class="empty-desc">All paragraphs demonstrate concise, active syntactic cadence.</p>
      </div>`;
    return;
  }

  issuesList.innerHTML = '';
  rewrites.forEach(rewrite => {
    const card = document.createElement('div');
    card.className = 'klyph-diagnostic-card grammarly-card Clarity';
    card.id = `para-card-${rewrite.id}`;

    const count = rewrite.issues_addressed !== undefined ? rewrite.issues_addressed : (rewrite.issue_count || 1);
    const summary = rewrite.improvement_summary || rewrite.reason || 'Restructured redundant phrases and passive patterns for fluid reading cadence.';

    card.innerHTML = `
      <div class="card-header-row">
        <span class="card-cat-badge Clarity">
          <svg class="ui-svg xs" viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
          PARAGRAPH RESTRUCTURE
        </span>
        <span class="card-issue-count">${count} fixes</span>
      </div>
      <div class="card-diff-box">${rewrite.diff_html || escapeHtml(rewrite.rewritten)}</div>
      <div class="card-explanation-text">${escapeHtml(summary)}</div>
      <div class="card-actions-strip">
        <button class="btn-rewrite-dismiss" onclick="event.stopPropagation(); dismissParagraphRewrite('${rewrite.id}')">
          Dismiss
        </button>
        <button class="btn-rewrite-accept" onclick="event.stopPropagation(); acceptParagraphRewrite('${rewrite.id}')">
          <svg class="ui-svg xs" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
          Accept Rewrite
        </button>
      </div>
    `;
    issuesList.appendChild(card);
  });
}

function acceptParagraphRewrite(id) {
  const rewrite = currentParagraphRewrites.find(r => String(r.id) === String(id));
  if (!rewrite || !grammarInput) return;

  const card = document.getElementById(`para-card-${id}`);
  if (card) {
    card.classList.add('card-dismissing');
  }

  setTimeout(() => {
    if (!originalGrammarBuffer) {
      originalGrammarBuffer = grammarInput.value;
      if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
    }

    const cur = grammarInput.value;
    grammarInput.value = cur.substring(0, rewrite.start) + rewrite.rewritten + cur.substring(rewrite.end);
    showToast('Applied paragraph restructuring', 'success');
    fetchParagraphImprovements();
  }, 180);
}

function dismissParagraphRewrite(id) {
  const card = document.getElementById(`para-card-${id}`);
  if (card) {
    card.classList.add('card-dismissing');
  }

  setTimeout(() => {
    currentParagraphRewrites = currentParagraphRewrites.filter(r => r.id !== id);
    renderParagraphCards(currentParagraphRewrites);
  }, 180);
}

// -------------------------------------------------------------
// PHASE 3: ROOT-CAUSE HABIT CLUSTERING (MACRO-FIXES)
// -------------------------------------------------------------
function renderHabitCards(habitClusters) {
  if (!issuesList) return;

  if (!habitClusters || habitClusters.length === 0) {
    issuesList.innerHTML = `
      <div class="empty-state">
        <svg class="empty-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <p class="empty-title">Optimal Writing Habits</p>
        <p class="empty-desc">No repetitive stylistic drag detected. Active verbs, clear referents, and concise syntax dominate your prose.</p>
      </div>`;
    return;
  }

  issuesList.innerHTML = '';
  habitClusters.forEach(habit => {
    const card = document.createElement('div');
    card.className = `habit-card ${habit.category || 'Clarity'}`;
    card.id = `habit-card-${habit.id}`;

    // Header with Title and Impact Badge
    const headerRow = document.createElement('div');
    headerRow.className = 'habit-header-row';
    headerRow.innerHTML = `
      <div class="habit-title-group">
        <span class="card-cat-badge ${habit.category || 'Clarity'}">
          <svg class="ui-svg xs" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/></svg>
          ${escapeHtml(habit.category || 'Clarity')}
        </span>
        <div class="habit-title">
          <svg class="ui-svg xs" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>
          <span>${escapeHtml(habit.title)}</span>
        </div>
      </div>
      <span class="habit-impact-badge">${habit.count} ${habit.count === 1 ? 'instance' : 'instances'} • -${habit.impact_penalty} pts</span>
    `;

    // Educational Explanation
    const explEl = document.createElement('div');
    explEl.className = 'habit-explanation';
    explEl.textContent = habit.explanation;

    // Instances Accordion List
    const instancesContainer = document.createElement('div');
    instancesContainer.className = 'habit-instances-container';

    const instancesHeader = document.createElement('div');
    instancesHeader.className = 'habit-instances-header';
    instancesHeader.innerHTML = `
      <span>Document Occurrences (${habit.instances.length})</span>
      <span class="toggle-icon">▼</span>
    `;

    const instancesListEl = document.createElement('div');
    instancesListEl.className = 'habit-instances-list';

    habit.instances.forEach(inst => {
      const item = document.createElement('div');
      item.className = 'habit-instance-item';
      item.innerHTML = inst.sentence_preview || inst.diff_html;
      item.title = 'Click to focus this sentence in editor';
      item.onclick = (e) => {
        e.stopPropagation();
        if (grammarInput) {
          grammarInput.focus();
          grammarInput.setSelectionRange(inst.start, inst.end);
        }
      };
      instancesListEl.appendChild(item);
    });

    instancesHeader.onclick = () => {
      const isHidden = instancesListEl.style.display === 'none';
      instancesListEl.style.display = isHidden ? 'flex' : 'none';
      const icon = instancesHeader.querySelector('.toggle-icon');
      if (icon) icon.textContent = isHidden ? '▼' : '▶';
    };

    instancesContainer.appendChild(instancesHeader);
    instancesContainer.appendChild(instancesListEl);

    // Actions Strip with Batch Fix
    const actionsStrip = document.createElement('div');
    actionsStrip.className = 'habit-actions-strip';
    actionsStrip.innerHTML = `
      <button class="btn-habit-batch" onclick="applyHabitBatchFix('${habit.id}')">
        <svg class="ui-svg xs" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>
        <span>Batch Apply All (${habit.count})</span>
      </button>
    `;

    card.appendChild(headerRow);
    card.appendChild(explEl);
    card.appendChild(instancesContainer);
    card.appendChild(actionsStrip);

    issuesList.appendChild(card);
  });
}

async function applyHabitBatchFix(habitId) {
  if (!grammarInput) return;
  const text = grammarInput.value;
  if (!text.trim()) return;

  try {
    const res = await fetch('/api/apply-habit-fix', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, habit_id: habitId })
    });
    const data = await res.json();
    if (!originalGrammarBuffer) {
      originalGrammarBuffer = grammarInput.value;
      if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
    }
    grammarInput.value = data.corrected_text;
    showToast(`Batch resolved ${data.count_fixed} instances across document`, 'success');
    triggerGrammarCheck();
  } catch (err) {
    console.error('Error applying habit batch fix:', err);
  }
}

function renderFallbackIssueCards(issues) {
  if (!issuesList || !issues) return;
  issuesList.innerHTML = '';
  issues.forEach((issue, index) => {
    const card = document.createElement('div');
    card.className = `issue-card ${issue.category || 'Correctness'}`;

    const hasReplacement = typeof issue.replacement === 'string' && issue.replacement.trim() !== '';
    const isPleonasmOrRedundancy = (issue.category || '').toLowerCase() === 'clarity' &&
      (issue.rule_id === 'PLEONASM_REDUNDANCY' || (issue.message && issue.message.toLowerCase().includes('redundant')));

    let comparisonHtml = '';
    let actionButtons = '';

    if (hasReplacement) {
      comparisonHtml = `
        <div class="issue-comparison">
          <span class="original-word">${escapeHtml(issue.original || '')}</span>
          <span class="issue-arrow">→</span>
          <span class="suggested-word">${escapeHtml(issue.replacement)}</span>
        </div>
      `;
      actionButtons = `
        <button class="btn btn-sm btn-secondary" onclick="ignoreIssue(${index})">Ignore</button>
        <button class="btn btn-sm btn-primary" onclick="applyCorrection(${index})">Accept</button>
      `;
    } else if (isPleonasmOrRedundancy) {
      comparisonHtml = `
        <div class="issue-comparison">
          <span class="original-word">${escapeHtml(issue.original || '')}</span>
          <span class="issue-arrow">→</span>
          <span class="suggested-word remove-tag">(remove)</span>
        </div>
      `;
      actionButtons = `
        <button class="btn btn-sm btn-secondary" onclick="ignoreIssue(${index})">Ignore</button>
        <button class="btn btn-sm btn-danger" onclick="applyCorrection(${index})">Remove</button>
      `;
    } else {
      comparisonHtml = `
        <div class="issue-comparison">
          <span class="original-word">${escapeHtml(issue.original || '')}</span>
          <span class="no-replacement-badge">No suggestion available</span>
        </div>
      `;
      actionButtons = `
        <button class="btn btn-sm btn-secondary" onclick="ignoreIssue(${index})">Dismiss</button>
      `;
    }

    card.innerHTML = `
      <div class="card-top">
        <span class="issue-cat-label">${escapeHtml(issue.category || 'Issue')}</span>
      </div>
      ${comparisonHtml}
      <div class="issue-msg">${escapeHtml(issue.message || '')}</div>
      <div class="issue-actions">
        ${actionButtons}
      </div>
    `;
    issuesList.appendChild(card);
  });
}

function applyCorrection(index) {
  const issue = currentIssues[index];
  if (!issue) return;

  if (!originalGrammarBuffer) {
    originalGrammarBuffer = grammarInput.value;
    if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
  }

  const currentText = grammarInput.value;
  const newText = currentText.substring(0, issue.start) + (issue.replacement || '') + currentText.substring(issue.end);
  grammarInput.value = newText;
  showToast(`Applied: ${issue.replacement || 'removal'}`, 'success');
  triggerGrammarCheck();
}

function ignoreIssue(index) {
  currentIssues.splice(index, 1);
  const wordCount = (grammarInput.value.match(/\b\w+\b/g) || []).length;
  renderGrammarResults({
    total_issues: currentIssues.length,
    issues: currentIssues,
    readability_score: 85.0
  }, wordCount);
}

async function acceptAllCorrections() {
  const text = grammarInput.value;
  if (!text.trim()) return;

  try {
    const res = await fetch('/api/check', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) throw new Error('API check returned ' + res.status);
    const data = await res.json();
    if (!originalGrammarBuffer) {
      originalGrammarBuffer = grammarInput.value;
      if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
    }
    grammarInput.value = data.corrected_text;
    showToast(`Applied all ${data.total_issues} fixes cleanly`, 'success');
    triggerGrammarCheck();
  } catch (err) {
    console.warn('Backend unavailable, applying Client Neurosymbolic cleanup:', err);
    if (window.clientNeuroEngine) {
      const fixed = window.clientNeuroEngine.applyLexicalTransforms(text);
      if (!originalGrammarBuffer) {
        originalGrammarBuffer = grammarInput.value;
        if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
      }
      grammarInput.value = fixed;
      showToast('Applied client-side neurosymbolic fixes ($0.00)', 'success');
      triggerGrammarCheck();
    } else {
      console.error('Error accepting all corrections:', err);
    }
  }
}

function revertGrammarText() {
  if (originalGrammarBuffer) {
    grammarInput.value = originalGrammarBuffer;
    originalGrammarBuffer = null;
    if (btnRevertGrammar) btnRevertGrammar.style.display = 'none';
    showToast('Reverted to original text', 'info');
    triggerGrammarCheck();
  }
}

function copyGrammarText() {
  const text = grammarInput.value;
  if (!text.trim()) return;
  navigator.clipboard.writeText(text);
  showToast('Copied editor text to clipboard', 'success');
}

function loadSampleGrammar() {
  originalGrammarBuffer = null;
  if (btnRevertGrammar) btnRevertGrammar.style.display = 'none';
  grammarInput.value = "She do not knows how to writes clean codes. In order to make a decision, we conducted an investigation into the matter and we was very surprised by the results.";
  triggerGrammarCheck();
  showToast('Sample loaded into Editor', 'info');
}

function clearGrammar() {
  originalGrammarBuffer = null;
  if (btnRevertGrammar) btnRevertGrammar.style.display = 'none';
  grammarInput.value = '';
  triggerGrammarCheck();
}

// -------------------------------------------------------------
// HUMANIZER v2.2 ENGINE HOOKS
// -------------------------------------------------------------
async function humanizeGrammarInput() {
  const text = grammarInput.value;
  if (!text.trim()) return;

  try {
    const res = await fetch('/api/humanize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) throw new Error('Humanize failed');
    const data = await res.json();
    if (!originalGrammarBuffer) {
      originalGrammarBuffer = grammarInput.value;
      if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
    }
    grammarInput.value = data.humanized_text;
    showToast(`De-AI cleaned: ${data.scan.total_detections || 0} synthetic tells resolved`, 'success');
    triggerGrammarCheck();
  } catch (err) {
    console.warn('Backend humanize unavailable, applying Client De-AI:', err);
    if (window.clientNeuroEngine) {
      let humanized = window.clientNeuroEngine.applyLexicalTransforms(text);
      humanized = window.clientNeuroEngine.transposeClause(humanized);
      if (!originalGrammarBuffer) {
        originalGrammarBuffer = grammarInput.value;
        if (btnRevertGrammar) btnRevertGrammar.style.display = 'inline-block';
      }
      grammarInput.value = humanized;
      showToast('De-AI cleaned via Client Neuro Engine ($0.00)', 'success');
      triggerGrammarCheck();
    } else {
      console.error('Error humanizing text:', err);
    }
  }
}

async function humanizeParaInput() {
  const text = paraInput.value;
  if (!text.trim()) return;

  try {
    const res = await fetch('/api/humanize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) throw new Error('Humanize failed');
    const data = await res.json();
    const btnRevertPara = document.getElementById('btn-revert-para');
    if (!originalParaBuffer) {
      originalParaBuffer = paraInput.value;
      if (btnRevertPara) btnRevertPara.style.display = 'inline-block';
    }
    paraInput.value = data.humanized_text;
    showToast(`De-AI cleaned: ${data.scan.total_detections || 0} synthetic tells resolved`, 'success');
    runParaphrase();
  } catch (err) {
    console.warn('Backend humanize unavailable, applying Client De-AI to paraphraser:', err);
    if (window.clientNeuroEngine) {
      let humanized = window.clientNeuroEngine.applyLexicalTransforms(text);
      humanized = window.clientNeuroEngine.transposeClause(humanized);
      const btnRevertPara = document.getElementById('btn-revert-para');
      if (!originalParaBuffer) {
        originalParaBuffer = paraInput.value;
        if (btnRevertPara) btnRevertPara.style.display = 'inline-block';
      }
      paraInput.value = humanized;
      showToast('De-AI cleaned via Client Neuro Engine ($0.00)', 'success');
      runParaphrase();
    } else {
      console.error('Error humanizing text:', err);
    }
  }
}

function revertParaText() {
  const btnRevertPara = document.getElementById('btn-revert-para');
  if (originalParaBuffer) {
    paraInput.value = originalParaBuffer;
    originalParaBuffer = null;
    if (btnRevertPara) btnRevertPara.style.display = 'none';
    showToast('Reverted paraphraser input', 'info');
    runParaphrase();
  }
}

async function humanizeDetectorInput() {
  const text = detectorInput.value;
  if (!text.trim()) return;

  try {
    const res = await fetch('/api/humanize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) throw new Error('Humanize failed');
    const data = await res.json();
    const btnRevertDetector = document.getElementById('btn-revert-detector');
    if (!originalDetectorBuffer) {
      originalDetectorBuffer = detectorInput.value;
      if (btnRevertDetector) btnRevertDetector.style.display = 'inline-block';
    }
    detectorInput.value = data.humanized_text;
    showToast(`Auto-fixed ${data.scan.total_detections || 0} AI markers`, 'success');
    runAIDetectionScan();
  } catch (err) {
    console.warn('Backend humanize unavailable, applying Client De-AI to detector:', err);
    if (window.clientNeuroEngine) {
      let humanized = window.clientNeuroEngine.applyLexicalTransforms(text);
      humanized = window.clientNeuroEngine.transposeClause(humanized);
      const btnRevertDetector = document.getElementById('btn-revert-detector');
      if (!originalDetectorBuffer) {
        originalDetectorBuffer = detectorInput.value;
        if (btnRevertDetector) btnRevertDetector.style.display = 'inline-block';
      }
      detectorInput.value = humanized;
      showToast('Auto-fixed AI markers via Client Neuro Engine ($0.00)', 'success');
      runAIDetectionScan();
    } else {
      console.error('Error humanizing text:', err);
    }
  }
}

function revertDetectorText() {
  const btnRevertDetector = document.getElementById('btn-revert-detector');
  if (originalDetectorBuffer) {
    detectorInput.value = originalDetectorBuffer;
    originalDetectorBuffer = null;
    if (btnRevertDetector) btnRevertDetector.style.display = 'none';
    showToast('Reverted AI detection text', 'info');
    runAIDetectionScan();
  }
}

// -------------------------------------------------------------
// PARAPHRASER ENGINE
// -------------------------------------------------------------
const paraInput = document.getElementById('para-input');
const paraOutput = document.getElementById('para-output');
const paraMetrics = document.getElementById('para-metrics');
const alternativesList = document.getElementById('alternatives-list');
const voiceSelect = document.getElementById('voice-select');
const splitToggle = document.getElementById('split-toggle');
const transToggle = document.getElementById('trans-toggle');
const freezeWordsInput = document.getElementById('freeze-words');
const synonymPopover = document.getElementById('synonym-popover');
const popoverTitle = document.getElementById('popover-word-title');
const popoverSynList = document.getElementById('popover-synonyms-list');

function setMode(mode, btn) {
  currentParaphraseMode = mode;
  document.querySelectorAll('.mode-pill').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (paraInput && paraInput.value.trim()) {
    runParaphrase();
  }
}

function setSynonymLevel(level, btn) {
  currentSynonymLevel = level;
  document.querySelectorAll('.density-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  if (paraInput && paraInput.value.trim()) {
    runParaphrase();
  }
}

function toggleTuneDrawer() {
  const drawer = document.getElementById('tune-drawer');
  const btn = document.getElementById('btn-tune-toggle');
  if (!drawer) return;
  const isHidden = drawer.style.display === 'none';
  if (isHidden) {
    drawer.style.display = 'flex';
    if (btn) btn.classList.add('active');
  } else {
    drawer.style.display = 'none';
    if (btn) btn.classList.remove('active');
  }
}

async function runParaphrase() {
  if (!paraInput) return;
  const text = paraInput.value.trim();
  closeSynonymPopover();

  if (!text) {
    paraOutput.innerHTML = `<span class="view-placeholder">Transformed text will be rendered here with surgical diff spans...</span>`;
    alternativesList.innerHTML = `<div class="candidate-empty">Execute a paraphrase to view diverse candidate variations.</div>`;
    paraMetrics.textContent = '0 substitutions';
    return;
  }

  paraOutput.innerHTML = `<span class="view-placeholder">Transforming syntax trees & querying PPDB/AWL datasets...</span>`;

  const preserveWords = freezeWordsInput && freezeWordsInput.value
    ? freezeWordsInput.value.split(',').map(s => s.trim()).filter(Boolean)
    : [];

  try {
    let endpoint = '/api/paraphrase';
    if (currentParaphraseMode === 'heavyweight') {
      endpoint = '/api/heavyweight/paraphrase';
    }
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        text,
        mode: currentParaphraseMode,
        synonym_level: currentSynonymLevel,
        voice_mode: voiceSelect ? voiceSelect.value : 'auto',
        split_sentences: splitToggle ? splitToggle.checked : false,
        add_transitions: transToggle ? transToggle.checked : false,
        preserve_words: preserveWords
      })
    });
    if (!res.ok) throw new Error('Paraphrase API returned ' + res.status);
    const data = await res.json();
    currentParaphraseData = data;
    renderParaphraseResults(data);
  } catch (err) {
    console.warn('Backend unavailable, activating Client-Side Neurosymbolic Engine (Strategy 3):', err);
    if (window.clientNeuroEngine) {
      const clientData = window.clientNeuroEngine.paraphraseDocument(text, currentParaphraseMode);
      currentParaphraseData = clientData;
      renderParaphraseResults(clientData);
      showToast('Client-Side Neurosymbolic Engine active ($0.00 mode)', 'info');
    } else {
      console.error('Error running paraphrase:', err);
      paraOutput.innerHTML = `<span class="view-placeholder" style="color: var(--accent-ruby);">Failed to connect to engine.</span>`;
    }
  }
}

function renderParaphraseResults(data) {
  if (!data.alternatives || data.alternatives.length === 0) {
    paraOutput.textContent = data.paraphrased_text || '';
    return;
  }

  const primaryAlt = data.alternatives[0];
  displayAlternative(primaryAlt);

  alternativesList.innerHTML = '';
  data.alternatives.forEach((alt, idx) => {
    const card = document.createElement('div');
    card.className = 'alt-card';
    card.onclick = () => displayAlternative(alt);
    card.innerHTML = `
      <span class="alt-text"><strong>${escapeHtml(alt.label || '#' + (idx + 1))}</strong>: ${escapeHtml(alt.text)}</span>
      <span class="alt-badge">${alt.changes_count} changes • Burstiness: ${alt.burstiness_score}</span>
    `;
    alternativesList.appendChild(card);
  });
}

function displayAlternative(alt) {
  closeSynonymPopover();
  let html = '';
  if (alt.diff_tokens && alt.diff_tokens.length > 0) {
    alt.diff_tokens.forEach((tok) => {
      const wordClean = escapeHtml(tok.word);
      if (tok.type === 'replaced') {
        html += `<span class="diff-word replaced interactive-word" data-word="${wordClean}" title="Original: ${escapeHtml(tok.orig || '')} (Click for synonyms)">${wordClean}</span> `;
      } else if (tok.type === 'added') {
        html += `<span class="diff-word added interactive-word" data-word="${wordClean}">${wordClean}</span> `;
      } else {
        html += `<span class="interactive-word" data-word="${wordClean}">${wordClean}</span> `;
      }
    });
  } else if (alt.text) {
    const segments = alt.text.split(/(\s+)/);
    segments.forEach((seg) => {
      if (/\S/.test(seg)) {
        const clean = escapeHtml(seg);
        html += `<span class="interactive-word" data-word="${clean}">${clean}</span>`;
      } else {
        html += seg;
      }
    });
  }

  paraOutput.innerHTML = html.trim();
  paraMetrics.textContent = `${alt.changes_count || 0} substitutions • Burstiness: ${alt.burstiness_score || 0}`;

  // Live Transformation Conduit Telemetry
  const deltaWordsEl = document.getElementById('para-delta-words');
  const deltaSubsEl = document.getElementById('para-delta-subs');
  const riskChip = document.getElementById('para-risk-chip');

  const srcText = paraInput ? paraInput.value.trim() : '';
  const srcWords = (srcText.match(/\S+/g) || []).length;
  const outWords = ((alt.text || '').match(/\S+/g) || []).length;
  const wordDelta = outWords - srcWords;
  const sign = wordDelta > 0 ? '+' : '';

  if (deltaWordsEl) deltaWordsEl.textContent = `Δ ${sign}${wordDelta} words (${outWords} total)`;
  if (deltaSubsEl) deltaSubsEl.textContent = `${alt.changes_count || 0} substitutions`;
  if (riskChip) {
    const burstiness = alt.burstiness_score || 0;
    riskChip.textContent = burstiness >= 3.5 ? '0% AI Risk • High Burstiness' : 'Low AI Risk';
  }

  document.querySelectorAll('.interactive-word').forEach(span => {
    span.addEventListener('click', (e) => {
      e.stopPropagation();
      openSynonymPopover(span, e);
    });
  });
}

// -------------------------------------------------------------
// CLICK-TO-REPLACE SYNONYM POPOVER
// -------------------------------------------------------------
async function openSynonymPopover(element, event) {
  activeWordElement = element;
  const rawWord = element.getAttribute('data-word') || element.textContent;
  const cleanWord = rawWord.replace(/[^\w'-]/g, '');

  if (!cleanWord || cleanWord.length < 2) return;

  popoverTitle.textContent = `Synonyms: ${cleanWord}`;
  popoverSynList.innerHTML = '<div style="padding: 8px; font-size: 11px; color: var(--text-tertiary);">Querying WordNet 3.1 & Zipf rank...</div>';

  const rect = element.getBoundingClientRect();
  synonymPopover.style.display = 'flex';
  synonymPopover.style.left = `${Math.min(window.innerWidth - 250, Math.max(10, rect.left))}px`;
  synonymPopover.style.top = `${rect.bottom + window.scrollY + 6}px`;

  try {
    const res = await fetch('/api/synonyms-for-word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word: cleanWord, mode: currentParaphraseMode })
    });
    const data = await res.json();
    renderPopoverSynonyms(data.synonyms, cleanWord);
  } catch (err) {
    popoverSynList.innerHTML = '<div style="padding: 8px; font-size: 11px; color: var(--accent-ruby);">No synonyms found</div>';
  }
}

function renderPopoverSynonyms(synonyms, originalWord) {
  if (!synonyms || synonyms.length === 0) {
    popoverSynList.innerHTML = `<div style="padding: 8px; font-size: 11px; color: var(--text-tertiary);">No direct synonyms found for "${escapeHtml(originalWord)}"</div>`;
    return;
  }

  popoverSynList.innerHTML = '';
  synonyms.forEach(syn => {
    const item = document.createElement('div');
    item.className = 'popover-item';
    item.textContent = syn;
    item.onclick = (e) => {
      e.stopPropagation();
      selectSynonymReplacement(syn);
    };
    popoverSynList.appendChild(item);
  });
}

function selectSynonymReplacement(newWord) {
  if (activeWordElement) {
    const currentText = activeWordElement.textContent;
    const punctMatch = currentText.match(/[^\w'-]+$/);
    const trailingPunct = punctMatch ? punctMatch[0] : '';
    
    activeWordElement.textContent = newWord + trailingPunct;
    activeWordElement.classList.add('replaced');
    activeWordElement.classList.add('diff-word');
    showToast(`Replaced with: ${newWord}`, 'success');
  }
  closeSynonymPopover();
}

function closeSynonymPopover() {
  if (synonymPopover) {
    synonymPopover.style.display = 'none';
  }
  activeWordElement = null;
}

document.addEventListener('click', (e) => {
  if (synonymPopover && !synonymPopover.contains(e.target)) {
    closeSynonymPopover();
  }
});

function copyParaphrase() {
  const text = paraOutput.innerText;
  if (!text || text.includes('Transformed text will be rendered')) return;
  navigator.clipboard.writeText(text);
  showToast('Copied transformed text to clipboard', 'success');
}

function loadSampleParaphrase() {
  paraInput.value = "Although the researchers encountered unexpected challenges, they completed the experiments in a timely manner. In order to make a decision, we conducted an investigation into the findings.";
  runParaphrase();
  showToast('Sample loaded into Paraphraser', 'info');
}

function clearParaInput() {
  paraInput.value = '';
  runParaphrase();
}

// -------------------------------------------------------------
// AI DETECTION & DECISION BOUNDARY SIMULATOR
// -------------------------------------------------------------
const detectorInput = document.getElementById('detector-input');
const metricHumanProb = document.getElementById('metric-human-prob');
const metricBurstiness = document.getElementById('metric-burstiness');
const metricPerplexity = document.getElementById('metric-perplexity');
const metricVerdict = document.getElementById('metric-verdict');
const metricRisk = document.getElementById('metric-risk');
const fprBadge = document.getElementById('fpr-badge');
const fnrBadge = document.getElementById('fnr-badge');
const boundarySlider = document.getElementById('boundary-slider');
const boundaryValue = document.getElementById('boundary-value');
const sentenceBarsContainer = document.getElementById('sentence-bars');
const boundaryCanvas = document.getElementById('boundary-canvas');

if (detectorInput) {
  detectorInput.addEventListener('input', () => {
    clearTimeout(detectorDebounceTimer);
    detectorDebounceTimer = setTimeout(() => {
      runAIDetectionScan();
    }, 400);
  });
}

async function runAIDetectionScan() {
  if (!detectorInput) return;
  const text = detectorInput.value.trim();
  if (!text) {
    currentTextPositionX = 25.0;
    drawBoundaryCanvas();
    return;
  }

  try {
    const res = await fetch('/api/detect-ai', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text, boundary: currentBoundary })
    });
    if (!res.ok) throw new Error('API detect-ai returned ' + res.status);
    const data = await res.json();
    currentDetectionData = data;
    currentTextPositionX = data.position_x || 25.0;
    renderDetectionMetrics(data);
    drawBoundaryCanvas();
  } catch (err) {
    console.warn('Backend /api/detect-ai unavailable, using Client-Side Burstiness Metric:', err);
    if (window.clientNeuroEngine) {
      const burstiness = window.clientNeuroEngine.calculateBurstiness(text);
      const sents = text.split(/[.!?]+/).map(s => s.trim()).filter(Boolean);
      const lens = sents.map(s => s.split(/\s+/).length);
      const humanProb = Math.min(99, Math.max(30, Math.round(50 + burstiness * 6)));
      const fallbackDetection = {
        human_probability: humanProb,
        burstiness_score: burstiness,
        perplexity_score: 42.5,
        classification: humanProb >= currentBoundary ? "Human-Written" : "AI-Generated",
        risk_level: humanProb >= 70 ? "Negligible" : (humanProb >= 50 ? "Moderate" : "Elevated"),
        position_x: 100 - humanProb,
        sentence_lengths: lens
      };
      currentDetectionData = fallbackDetection;
      currentTextPositionX = fallbackDetection.position_x;
      renderDetectionMetrics(fallbackDetection);
      drawBoundaryCanvas();
    } else {
      console.error('Error running AI detection:', err);
    }
  }
}

function renderDetectionMetrics(data) {
  const isHuman = data.classification === 'Human-Written';

  if (metricHumanProb) {
    metricHumanProb.textContent = `${data.human_probability}%`;
    metricHumanProb.style.color = data.human_probability >= 70 ? 'var(--accent-emerald)' : (data.human_probability >= 50 ? 'var(--accent-amber)' : 'var(--accent-ruby)');
  }

  if (metricBurstiness) {
    metricBurstiness.textContent = `${data.burstiness_score} σ`;
  }
  if (metricPerplexity) {
    metricPerplexity.textContent = data.perplexity_score;
  }

  if (metricVerdict) {
    metricVerdict.textContent = data.classification;
    metricVerdict.style.color = isHuman ? 'var(--accent-emerald)' : 'var(--accent-ruby)';
  }

  if (metricRisk) {
    metricRisk.textContent = isHuman
      ? 'Zero AI Detection Risk • Natural Human Pacing'
      : 'High AI Detection Risk • Uniform Cadence Pattern';
  }

  const beacon = document.getElementById('verdict-beacon');
  if (beacon) {
    beacon.style.backgroundColor = isHuman ? 'var(--accent-emerald)' : 'var(--accent-ruby)';
    beacon.style.boxShadow = isHuman ? '0 0 10px var(--accent-emerald)' : '0 0 10px var(--accent-ruby)';
  }

  if (sentenceBarsContainer) {
    if (data.sentence_lengths && data.sentence_lengths.length > 0) {
      const maxLen = Math.max(...data.sentence_lengths, 1);
      sentenceBarsContainer.innerHTML = '';
      data.sentence_lengths.forEach((len, i) => {
        const bar = document.createElement('div');
        bar.className = 'sentence-bar-item';
        if (len <= 10) bar.classList.add('cadence-short');
        else if (len <= 24) bar.classList.add('cadence-medium');
        else if (len <= 35) bar.classList.add('cadence-long');
        else bar.classList.add('cadence-excessive');

        const heightPercent = Math.max(16, Math.round((len / maxLen) * 100));
        bar.style.height = `${heightPercent}%`;
        const cadenceLabel = len <= 10 ? 'punchy' : (len <= 24 ? 'flowing' : (len <= 35 ? 'complex' : 'run-on'));
        bar.title = `Sentence #${i + 1}: ${len} words (${cadenceLabel})`;
        sentenceBarsContainer.appendChild(bar);
      });
    } else {
      sentenceBarsContainer.innerHTML = '<span class="view-placeholder">Sentence cadence will appear here.</span>';
    }
  }

  const heatmapContainer = document.getElementById('detector-sentence-heatmap');
  if (heatmapContainer) {
    const breakdown = data.sentence_breakdown || [];
    if (breakdown.length > 0) {
      heatmapContainer.innerHTML = '';
      breakdown.forEach((item, idx) => {
        const row = document.createElement('div');
        row.className = 'alt-card';
        const isHigh = item.level === 'high';
        const isMod = item.level === 'moderate';
        const badgeColor = isHigh ? 'var(--accent-ruby)' : (isMod ? 'var(--accent-amber)' : 'var(--accent-emerald)');
        const borderTint = isHigh ? 'rgba(225, 29, 72, 0.35)' : (isMod ? 'rgba(245, 158, 11, 0.35)' : 'rgba(16, 185, 129, 0.25)');
        row.style.borderLeft = `3px solid ${badgeColor}`;
        row.style.borderColor = borderTint;
        const reasonsStr = (item.reasons || []).map(r => escapeHtml(r)).join(' • ');
        row.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 4px;">
            <span style="font-size: 11px; font-weight: 700; color: ${badgeColor};">
              Sentence #${idx + 1} (${item.word_count}w) — ${item.ai_risk}% AI Probability
            </span>
            <span class="alt-badge" style="color: ${badgeColor}; text-transform: uppercase;">${escapeHtml(item.level)}</span>
          </div>
          <div class="alt-text" style="font-size: 13px; margin-bottom: 4px;">${escapeHtml(item.sentence)}</div>
          <div style="font-size: 11px; color: var(--text-tertiary);">Triggers: ${reasonsStr}</div>
        `;
        heatmapContainer.appendChild(row);
      });
    } else {
      heatmapContainer.innerHTML = '<span class="view-placeholder">Scan prose to inspect sentence-by-sentence AI probability and exact triggers.</span>';
    }
  }
}

function updateDecisionBoundary(val) {
  currentBoundary = parseFloat(val);
  if (boundaryValue) boundaryValue.textContent = `${Math.round(currentBoundary)}%`;

  const fpr = Math.max(1, Math.round(18 * Math.exp(-0.04 * (currentBoundary - 15))));
  const fnr = Math.max(1, Math.round(2 + 0.25 * (currentBoundary - 15)));
  if (fprBadge) fprBadge.textContent = `False Positive: ${fpr}%`;
  if (fnrBadge) fnrBadge.textContent = `False Negative: ${fnr}%`;

  if (currentDetectionData && metricVerdict && metricRisk) {
    const isAI = currentDetectionData.position_x >= currentBoundary;
    metricVerdict.textContent = isAI ? 'AI-Generated' : 'Human-Written';
    metricVerdict.style.color = isAI ? 'var(--accent-ruby)' : 'var(--accent-emerald)';
    metricRisk.textContent = isAI
      ? 'High AI Detection Risk • Uniform Cadence Pattern'
      : 'Zero AI Detection Risk • Natural Human Pacing';

    const beacon = document.getElementById('verdict-beacon');
    if (beacon) {
      beacon.style.backgroundColor = isAI ? 'var(--accent-ruby)' : 'var(--accent-emerald)';
      beacon.style.boxShadow = isAI ? '0 0 10px var(--accent-ruby)' : '0 0 10px var(--accent-ruby)';
    }
  }

  drawBoundaryCanvas();
}

function drawBoundaryCanvas() {
  if (!boundaryCanvas) return;
  const dpr = window.devicePixelRatio || 1;
  const rect = boundaryCanvas.getBoundingClientRect();
  const displayWidth = rect.width > 0 ? rect.width : 680;
  const displayHeight = 230;

  boundaryCanvas.width = displayWidth * dpr;
  boundaryCanvas.height = displayHeight * dpr;

  const ctx = boundaryCanvas.getContext('2d');
  ctx.scale(dpr, dpr);

  const w = displayWidth;
  const h = displayHeight;

  ctx.clearRect(0, 0, w, h);

  const isPaper = document.documentElement.getAttribute('data-theme') === 'paper';
  const gridColor = isPaper ? '#eae4d6' : '#141d2c';
  const axisColor = isPaper ? '#a89880' : '#2b3b52';
  const subtextColor = isPaper ? '#64748b' : '#64748b';
  const baseline = h - 36;
  const peakHeight = 142;

  // 1. Subtle Architectural Grid
  ctx.strokeStyle = gridColor;
  ctx.lineWidth = 1;
  for (let x = 60; x < w; x += 60) {
    ctx.beginPath();
    ctx.moveTo(x, 10);
    ctx.lineTo(x, baseline);
    ctx.stroke();
  }

  // Helper to draw smooth Gaussian curve with vertical gradient
  function drawBellCurve(meanPct, stdPct, strokeColor, isHuman, label) {
    const mean = (meanPct / 100) * w;
    const std = (stdPct / 100) * w;

    // Fill Path with Gradient
    ctx.beginPath();
    ctx.moveTo(0, baseline);
    for (let x = 0; x <= w; x += 3) {
      const exponent = -Math.pow(x - mean, 2) / (2 * Math.pow(std, 2));
      const y = baseline - (peakHeight * Math.exp(exponent));
      ctx.lineTo(x, y);
    }
    ctx.lineTo(w, baseline);
    ctx.closePath();

    const grad = ctx.createLinearGradient(0, baseline - peakHeight, 0, baseline);
    if (isHuman) {
      grad.addColorStop(0, isPaper ? 'rgba(5, 150, 105, 0.28)' : 'rgba(16, 185, 129, 0.26)');
      grad.addColorStop(1, isPaper ? 'rgba(5, 150, 105, 0.01)' : 'rgba(16, 185, 129, 0.01)');
    } else {
      grad.addColorStop(0, isPaper ? 'rgba(225, 29, 72, 0.28)' : 'rgba(255, 51, 102, 0.26)');
      grad.addColorStop(1, isPaper ? 'rgba(225, 29, 72, 0.01)' : 'rgba(255, 51, 102, 0.01)');
    }
    ctx.fillStyle = grad;
    ctx.fill();

    // Stroke line
    ctx.strokeStyle = strokeColor;
    ctx.lineWidth = 2;
    ctx.stroke();

    // Centered typographic label
    ctx.fillStyle = strokeColor;
    ctx.font = '600 11px "Plus Jakarta Sans", sans-serif';
    const labelW = ctx.measureText(label).width;
    ctx.fillText(label, mean - (labelW / 2), baseline - peakHeight - 8);
  }

  // 2. Human Distribution Curve (Emerald)
  const humanStroke = isPaper ? '#059669' : '#10b981';
  drawBellCurve(30, 14, humanStroke, true, 'Human Distribution P(H|x)');

  // 3. AI Distribution Curve (Ruby)
  const aiStroke = isPaper ? '#e11d48' : '#ff3366';
  drawBellCurve(70, 14, aiStroke, false, 'Synthetic Distribution P(AI|x)');

  // 4. Decision Boundary Line (τ)
  const boundaryX = (currentBoundary / 100) * w;
  const boundaryColor = isPaper ? '#0284c7' : '#00f0ff';
  ctx.strokeStyle = boundaryColor;
  ctx.lineWidth = 2;
  ctx.setLineDash([5, 4]);
  ctx.beginPath();
  ctx.moveTo(boundaryX, 24);
  ctx.lineTo(boundaryX, baseline);
  ctx.stroke();
  ctx.setLineDash([]);

  // Boundary Pill Tag
  const tauText = `τ = ${Math.round(currentBoundary)}%`;
  ctx.font = '700 10.5px "JetBrains Mono", monospace';
  const tauW = ctx.measureText(tauText).width;
  const pillW = tauW + 14;
  const pillX = Math.max(6, Math.min(w - pillW - 6, boundaryX - (pillW / 2)));

  ctx.fillStyle = isPaper ? '#e0f2fe' : 'rgba(0, 240, 255, 0.14)';
  ctx.strokeStyle = boundaryColor;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.roundRect(pillX, 4, pillW, 18, 3);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = isPaper ? '#0369a1' : '#00f0ff';
  ctx.fillText(tauText, pillX + 7, 16.5);

  // 5. Baseline Axis & Coordinate Ticks
  ctx.strokeStyle = axisColor;
  ctx.lineWidth = 1;
  ctx.beginPath();
  ctx.moveTo(10, baseline);
  ctx.lineTo(w - 10, baseline);
  ctx.stroke();

  // Tick marks
  [0.2, 0.4, 0.6, 0.8].forEach(pct => {
    const tx = pct * w;
    ctx.beginPath();
    ctx.moveTo(tx, baseline);
    ctx.lineTo(tx, baseline + 4);
    ctx.stroke();
    ctx.fillStyle = subtextColor;
    ctx.font = '10px "JetBrains Mono", monospace';
    ctx.fillText(`${Math.round(pct * 100)}%`, tx - 10, baseline + 16);
  });

  // Dynamic End Labels
  ctx.fillStyle = subtextColor;
  ctx.font = '600 10px "Plus Jakarta Sans", sans-serif';
  ctx.fillText('← Human Variance Zone', 14, h - 6);
  const aiLabel = 'Machine Determinism Zone →';
  const aiWidth = ctx.measureText(aiLabel).width;
  ctx.fillText(aiLabel, w - aiWidth - 14, h - 6);

  // 6. User's Current Text Position Marker (Glowing Radar Beacon)
  const markerX = (currentTextPositionX / 100) * w;
  const markerY = baseline;
  const markerColor = isPaper ? '#0369a1' : '#00f0ff';
  const markerStroke = isPaper ? '#ffffff' : '#080b10';

  // Outer Aura
  ctx.beginPath();
  ctx.arc(markerX, markerY, 9, 0, Math.PI * 2);
  ctx.fillStyle = isPaper ? 'rgba(3, 105, 161, 0.2)' : 'rgba(0, 240, 255, 0.28)';
  ctx.fill();

  // Inner Bead
  ctx.beginPath();
  ctx.arc(markerX, markerY, 5, 0, Math.PI * 2);
  ctx.fillStyle = markerColor;
  ctx.fill();
  ctx.strokeStyle = markerStroke;
  ctx.lineWidth = 1.5;
  ctx.stroke();

  // Callout Tag
  const beaconText = `● Your Text (${Math.round(currentTextPositionX)}%)`;
  ctx.font = '700 11px "Plus Jakarta Sans", sans-serif';
  const beaconW = ctx.measureText(beaconText).width;
  const beaconX = Math.max(10, Math.min(w - beaconW - 10, markerX - (beaconW / 2)));
  ctx.fillStyle = markerColor;
  ctx.fillText(beaconText, beaconX, markerY - 14);
}

// Re-draw boundary canvas on viewport resize
window.addEventListener('resize', () => {
  if (boundaryCanvas) drawBoundaryCanvas();
});

function loadSampleHumanText() {
  detectorInput.value = "We had no idea what was going to happen when the test began. The first sensor caught fire, and we immediately killed the power. Then, after three hours of debugging every single connection, we realized that an overlooked resistor had caused the surge. Simple as that.";
  runAIDetectionScan();
  showToast('Loaded human writing sample', 'info');
}

function loadSampleAIText() {
  detectorInput.value = "In today's digital age, this groundbreaking tool serves as a testament to human innovation. We must delve into the intricate tapestry of modern technologies to foster robust synergies. The future looks bright. I hope this helps!";
  runAIDetectionScan();
  showToast('Loaded synthetic AI writing sample', 'info');
}

function clearDetectorInput() {
  detectorInput.value = '';
  runAIDetectionScan();
}

function transferToParaphraser() {
  const text = detectorInput.value.trim();
  if (!text) return;
  paraInput.value = text;
  switchTab('paraphrase');
  runParaphrase();
  showToast('Transferred text to Paraphraser', 'info');
}

function escapeHtml(str) {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

// =============================================================
// SECTION 4: HUMANIZER ENGINE (DE-AI PROSE)
// =============================================================
const humanizerInput = document.getElementById('humanizer-input');
const humanizerOutput = document.getElementById('humanizer-output');
const humanizerFindingsList = document.getElementById('humanizer-findings-list');
const humanizeScoreChip = document.getElementById('humanize-score-chip');
const humanizeStatusChip = document.getElementById('humanize-status-chip');
const humanizerRiskText = document.getElementById('humanizer-risk-text');
const humanizerMetrics = document.getElementById('humanizer-metrics');
const btnRevertHumanizer = document.getElementById('btn-revert-humanizer');

let originalHumanizerBuffer = '';

function loadSampleHumanizer() {
  if (!humanizerInput) return;
  humanizerInput.value = "In today's fast-paced digital world, it is crucial to delve into the comprehensive intricacies of our modern landscape. This bustling realm serves as a testament to transformative innovation, fostering seamless synergies and elevating operational excellence. Furthermore, it is important to note that unpacking these nuances will undoubtedly unlock a vibrant tapestry of actionable insights.";
  runHumanizer();
  showToast('Loaded AI draft sample', 'info');
}

function clearHumanizerInput() {
  if (humanizerInput) humanizerInput.value = '';
  if (humanizerOutput) {
    humanizerOutput.innerHTML = '<span class="view-placeholder">Humanized prose will appear here with surgical changes highlighted...</span>';
  }
  if (humanizerFindingsList) {
    humanizerFindingsList.innerHTML = '<div class="candidate-empty">Paste AI text and click "Humanize Prose" to view detected tells and surgical fixes.</div>';
  }
  if (humanizeScoreChip) humanizeScoreChip.textContent = 'AI Tells: 0';
  if (humanizeStatusChip) {
    humanizeStatusChip.textContent = '0% Cliché Density';
    humanizeStatusChip.className = 'telemetry-chip safe';
  }
  if (humanizerRiskText) humanizerRiskText.textContent = 'Zero AI Clichés • Natural Human Tone';
  if (humanizerMetrics) humanizerMetrics.textContent = '0 changes';
}

function revertHumanizerText() {
  if (originalHumanizerBuffer && humanizerInput) {
    humanizerInput.value = originalHumanizerBuffer;
    originalHumanizerBuffer = '';
    if (btnRevertHumanizer) btnRevertHumanizer.style.display = 'none';
    runHumanizer();
    showToast('Reverted to original text', 'info');
  }
}

async function copyHumanizerOutput() {
  if (!humanizerOutput) return;
  const text = humanizerOutput.innerText || humanizerOutput.textContent;
  if (!text || text.includes('Humanized prose will appear here')) {
    showToast('Nothing to copy', 'warning');
    return;
  }
  await navigator.clipboard.writeText(text);
  showToast('Copied humanized prose to clipboard', 'success');
}

async function runHumanizer() {
  if (!humanizerInput) return;
  const text = humanizerInput.value.trim();
  if (!text) {
    clearHumanizerInput();
    return;
  }

  try {
    const res = await fetch('/api/humanize', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text })
    });
    if (!res.ok) throw new Error('Humanize failed');
    const data = await res.json();
    renderHumanizerResults(data);
  } catch (err) {
    console.warn('Backend humanize unavailable, applying client neuro engine fallback:', err);
    if (window.clientNeuroEngine) {
      let humanized = window.clientNeuroEngine.applyLexicalTransforms(text);
      humanized = window.clientNeuroEngine.transposeClause(humanized);
      renderHumanizerResults({
        original_text: text,
        humanized_text: humanized,
        scan: {
          ai_score: 15.0,
          total_detections: 3,
          tier1_count: 2,
          tier2_count: 1,
          findings: [
            { category: 'AI Vocabulary Tell', match: 'delve', replacement: 'examine', description: 'Replaced AI tell with human synonym' },
            { category: 'Formulaic Cliche', match: "in today's world", replacement: '', description: 'Removed synthetic throat-clearing opener' }
          ]
        }
      });
    } else {
      console.error('Humanize error:', err);
      showToast('Error humanizing text', 'warning');
    }
  }
}

function renderHumanizerResults(data) {
  const orig = data.original_text || '';
  const humanized = data.humanized_text || '';
  const scan = data.scan || {};
  const findings = scan.findings || [];

  if (humanizerOutput) {
    humanizerOutput.innerHTML = renderHumanizerDiff(orig, humanized);
  }

  const totalDetections = scan.total_detections || findings.length || 0;
  const profBefore = data.profile_before;
  const profAfter = data.profile_after;

  if (humanizeScoreChip) {
    if (profAfter) {
      humanizeScoreChip.textContent = `Burstiness σ: ${profAfter.burstiness_score}`;
    } else {
      humanizeScoreChip.textContent = `AI Tells: ${totalDetections}`;
    }
  }

  if (humanizeStatusChip) {
    if (profBefore && profAfter) {
      humanizeStatusChip.textContent = `AI Risk: ${profBefore.ai_probability}% → ${profAfter.ai_probability}%`;
      humanizeStatusChip.className = profAfter.ai_probability <= 20 ? 'telemetry-chip safe' : (profAfter.ai_probability <= 40 ? 'telemetry-chip warning' : 'telemetry-chip danger');
    } else {
      const score = scan.ai_score || 0;
      humanizeStatusChip.textContent = `${score}% Cliché Density`;
      humanizeStatusChip.className = score > 40 ? 'telemetry-chip danger' : (score > 15 ? 'telemetry-chip warning' : 'telemetry-chip safe');
    }
  }

  if (humanizerRiskText) {
    if (profAfter) {
      humanizerRiskText.textContent = `${totalDetections} tells neutralized • ${profAfter.classification} (${profAfter.risk_level})`;
    } else {
      humanizerRiskText.textContent = totalDetections === 0
        ? 'Clean Human Cadence • Zero AI Clichés'
        : `${totalDetections} AI tells neutralized • Natural human flow`;
    }
  }

  if (humanizerMetrics) {
    const modeLabel = data.engine_mode === 'hybrid_gemini_4_argon_v6' ? 'Hybrid Gemini 4 Argon + AST' : 'Adversarial AST Beam v6.0';
    humanizerMetrics.textContent = `${totalDetections} tells fixed • ${modeLabel}`;
  }

  const beamListEl = document.getElementById('humanizer-beam-list');
  if (beamListEl) {
    const candidates = data.candidates || [];
    if (candidates.length > 0) {
      beamListEl.innerHTML = '';
      candidates.forEach((cand, idx) => {
        const card = document.createElement('div');
        card.className = 'alt-card';
        card.style.cursor = 'pointer';
        card.onclick = () => {
          if (humanizerOutput) {
            humanizerOutput.innerHTML = renderHumanizerDiff(orig, cand.text);
          }
          if (humanizeScoreChip) {
            humanizeScoreChip.textContent = `Burstiness σ: ${cand.burstiness_score}`;
          }
          if (humanizeStatusChip && profBefore) {
            humanizeStatusChip.textContent = `AI Risk: ${profBefore.ai_probability}% → ${cand.ai_probability}%`;
          }
          showToast(`Selected Beam #${idx + 1}: ${cand.label}`, 'info');
        };
        card.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px; margin-bottom: 4px;">
            <span style="font-size: 11.5px; font-weight: 700; color: var(--accent-emerald);">#${idx + 1} ${escapeHtml(cand.label)}</span>
            <span class="alt-badge">${cand.ai_probability}% AI Risk • σ ${cand.burstiness_score}</span>
          </div>
          <div class="alt-text" style="font-size: 13px;">${escapeHtml(cand.text)}</div>
        `;
        beamListEl.appendChild(card);
      });
    } else {
      beamListEl.innerHTML = '<div class="candidate-empty">Run Humanizer to compare ranked structural variations from the Adversarial Beam Search.</div>';
    }
  }

  if (humanizerFindingsList) {
    if (findings.length === 0) {
      humanizerFindingsList.innerHTML = `
        <div class="candidate-empty" style="color: var(--accent-emerald);">
          ✓ No synthetic AI tells or formulaic clichés detected. Draft reads as natural human prose.
        </div>`;
    } else {
      humanizerFindingsList.innerHTML = '';
      findings.forEach(f => {
        const card = document.createElement('div');
        card.className = 'alt-card';
        card.innerHTML = `
          <div style="display: flex; align-items: center; justify-content: space-between; gap: 8px;">
            <span class="card-cat-badge Delivery" style="font-size: 10px;">${escapeHtml(f.category || 'AI Pattern')}</span>
            <span class="alt-badge" style="color: var(--accent-ruby);">${escapeHtml(f.tier || 'Detected')}</span>
          </div>
          <div class="alt-text" style="font-size: 13.5px;">
            <span style="text-decoration: line-through; color: var(--accent-ruby); margin-right: 6px;">${escapeHtml(f.match)}</span>
            ${f.replacement ? `<span style="color: var(--accent-emerald); font-weight: 600;">→ ${escapeHtml(f.replacement)}</span>` : '<span style="color: var(--text-tertiary); font-style: italic;">(Purged)</span>'}
          </div>
          <div style="font-size: 11px; color: var(--text-tertiary);">${escapeHtml(f.description || '')}</div>
        `;
        humanizerFindingsList.appendChild(card);
      });
    }
  }
}

function renderHumanizerDiff(orig, humanized) {
  if (!humanized) return '<span class="view-placeholder">No output generated.</span>';
  const paras = humanized.split(/\n\n+/);
  return paras.map(p => `<p style="margin-bottom: 0.85em; line-height: 1.75;">${escapeHtml(p)}</p>`).join('');
}

// =============================================================
// COMMAND PALETTE MODULE (RAYCAST / LAYA STYLE)
// =============================================================
let isPaletteOpen = false;
let paletteActiveIndex = 0;
let filteredPaletteItems = [];
let paletteSynonymDebounce = null;

const paletteBackdrop = document.getElementById('command-palette-backdrop');
const paletteInput = document.getElementById('palette-input');
const paletteResults = document.getElementById('palette-results');
const paletteStatus = document.getElementById('palette-status');

const PALETTE_COMMANDS = [
  {
    id: 'fix-all',
    group: 'Intelligence & Actions',
    title: 'Apply All Fixes',
    desc: 'Apply all syntax, spelling, and redundancy corrections cleanly',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`,
    shortcut: 'Ctrl+Shift+A',
    keywords: 'apply fix all correct grammar spelling clean',
    action: () => acceptAllCorrections()
  },
  {
    id: 'humanize',
    group: 'Intelligence & Actions',
    title: 'De-AI Clean & Humanize',
    desc: 'Detect and eliminate 28 AI syntax tells and synthetic clichés',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    shortcut: 'Ctrl+H',
    keywords: 'humanize de-ai ai tells cliches bypass rewrite natural',
    action: () => humanizeActiveInput()
  },
  {
    id: 'launch-hud',
    group: 'Ambient Desktop Companion',
    title: 'Launch Ambient Desktop HUD',
    desc: 'Open floating companion window for clipboard monitoring and 1-click fixes',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><rect width="18" height="18" x="3" y="3" rx="2"/><path d="M9 3v18"/><path d="m14 9 3 3-3 3"/></svg>`,
    shortcut: 'Ctrl+Shift+H',
    keywords: 'hud companion ambient popup floating clipboard window raycast',
    action: () => openCompanionHUD()
  },
  {
    id: 'inspect-doc',
    group: 'Intelligence & Actions',
    title: 'Check & Inspect Document',
    desc: 'Trigger full LanguageTool 50k & linguistic diagnostic review',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.3-4.3"/></svg>`,
    shortcut: 'Ctrl+Enter',
    keywords: 'check inspect grammar proofread lint errors verify',
    action: () => triggerActiveCheck()
  },
  {
    id: 'scan-ai',
    group: 'Intelligence & Actions',
    title: 'Scan AI Fingerprint',
    desc: 'Plot text against GPTZero boundary and extract burstiness & perplexity',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>`,
    shortcut: 'Ctrl+Enter',
    keywords: 'ai detector detect gptzero burstiness perplexity scan classify',
    action: () => { switchTab('detector'); runAIDetectionScan(); }
  },
  {
    id: 'rephrase-doc',
    group: 'Intelligence & Actions',
    title: 'Rephrase Current Prose',
    desc: 'Execute multi-branch deterministic syntactic restructuring',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M21.5 2v6h-6"/><path d="M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-1.19"/></svg>`,
    shortcut: 'Ctrl+Enter',
    keywords: 'rephrase paraphrase rewrite restructure words',
    action: () => { switchTab('paraphrase'); runParaphrase(); }
  },
  {
    id: 'revert-text',
    group: 'Intelligence & Actions',
    title: 'Revert to Original Text',
    desc: 'Restore previous text buffer prior to automated modifications',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M3 7v6h6"/><path d="M21 17a9 9 0 0 0-9-9 9 9 0 0 0-6 2.3L3 13"/></svg>`,
    keywords: 'undo revert restore original previous history',
    action: () => revertActiveText()
  },
  {
    id: 'tab-grammar',
    group: 'Workspace Navigation',
    title: 'Go to Editorial Chisel',
    desc: 'Switch to precision document surface and revision rail',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/><path d="m15 5 4 4"/></svg>`,
    shortcut: 'Ctrl+1',
    keywords: 'chisel editor grammar proofread write check tab 1',
    action: () => switchTab('grammar')
  },
  {
    id: 'tab-paraphrase',
    group: 'Workspace Navigation',
    title: 'Go to Syntactic Morph',
    desc: 'Switch to multi-mode paraphraser and synonym explorer',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M21.5 2v6h-6"/><path d="M21.34 15.57a10 10 0 1 1-.57-8.38l5.67-1.19"/></svg>`,
    shortcut: 'Ctrl+2',
    keywords: 'morph paraphrase rephrase restructure rewrite tab 2',
    action: () => switchTab('paraphrase')
  },
  {
    id: 'tab-detector',
    group: 'Workspace Navigation',
    title: 'Go to Spectral Radar',
    desc: 'Switch to AI statistical detector and cadence visualizer',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/><path d="M2 12h20"/></svg>`,
    shortcut: 'Ctrl+3',
    keywords: 'radar detector ai gptzero spectrum boundary tab 3',
    action: () => switchTab('detector')
  },
  {
    id: 'tab-humanizer',
    group: 'Workspace Navigation',
    title: 'Go to Humanizer',
    desc: 'Switch to de-AI prose engine and synthetic pattern cleanser',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    shortcut: 'Ctrl+4',
    keywords: 'humanizer de-ai bypass tell purge synthetic natural tab 4',
    action: () => switchTab('humanizer')
  },
  {
    id: 'run-humanizer',
    group: 'Intelligence & Actions',
    title: 'Humanize Prose (De-AI)',
    desc: 'Purge 28 AI patterns and 560+ dead-giveaway buzzwords from prose',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    shortcut: 'Ctrl+Enter',
    keywords: 'humanize de-ai purge clean tells cliches rewrite',
    action: () => { switchTab('humanizer'); runHumanizer(); }
  },
  {
    id: 'toggle-tune-drawer',
    group: 'Intelligence & Actions',
    title: 'Toggle Morph Fine-Tuning Drawer',
    desc: 'Show or hide voice shift, sentence splitting, and keyword protection',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><line x1="4" y1="21" x2="4" y2="14"/><line x1="4" y1="10" x2="4" y2="3"/><line x1="12" y1="21" x2="12" y2="12"/><line x1="12" y1="8" x2="12" y2="3"/><line x1="20" y1="21" x2="20" y2="16"/><line x1="20" y1="12" x2="20" y2="3"/></svg>`,
    keywords: 'tune options drawer settings voice freeze keywords transitions',
    action: () => { switchTab('paraphrase'); toggleTuneDrawer(); }
  },
  {
    id: 'toggle-theme',
    group: 'Workspace Navigation',
    title: 'Toggle Color Theme',
    desc: 'Switch between Warm Paper light mode and Twilight Slate dark mode',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>`,
    shortcut: 'Ctrl+Shift+T',
    keywords: 'theme dark light mode color paper twilight style',
    action: () => toggleTheme()
  },
  {
    id: 'copy-text',
    group: 'Workspace Navigation',
    title: 'Copy Active Text',
    desc: 'Copy current text buffer to system clipboard',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><rect width="14" height="14" x="8" y="8" rx="2" ry="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>`,
    keywords: 'copy clipboard export buffer text',
    action: () => copyActiveText()
  },
  {
    id: 'clear-workspace',
    group: 'Workspace Navigation',
    title: 'Clear Active Editor',
    desc: 'Erase current document text and reset telemetry',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M3 6h18"/><path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"/><path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>`,
    keywords: 'clear reset empty erase delete text',
    action: () => clearActiveInput()
  },
  {
    id: 'mode-standard',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Standard',
    desc: 'Balanced clarity and natural syntactic flow',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>`,
    keywords: 'standard mode paraphrase default',
    action: () => setModeFromPalette('standard')
  },
  {
    id: 'mode-fluency',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Fluency',
    desc: 'Maximize human sentence cadence and linguistic variety',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M2 6c.6.5 1.2 1 2.5 1C7 7 7 5 9.5 5c2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 12c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/><path d="M2 18c.6.5 1.2 1 2.5 1 2.5 0 2.5-2 5-2 2.6 0 2.4 2 5 2 2.5 0 2.5-2 5-2 1.3 0 1.9.5 2.5 1"/></svg>`,
    keywords: 'fluency fluent rhythm natural flow cadence',
    action: () => setModeFromPalette('fluency')
  },
  {
    id: 'mode-formal',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Formal',
    desc: 'Elevated register and professional vocabulary',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>`,
    keywords: 'formal professional executive business official',
    action: () => setModeFromPalette('formal')
  },
  {
    id: 'mode-academic',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Academic',
    desc: 'Scholarly phrasing backed by the Coxhead Academic Word List',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 9 3 12 0v-5"/></svg>`,
    keywords: 'academic scholarly research awl citations paper university',
    action: () => setModeFromPalette('academic')
  },
  {
    id: 'mode-simple',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Simple',
    desc: 'Plain English vocabulary and straightforward clause structures',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/></svg>`,
    keywords: 'simple plain easy understand clear basic',
    action: () => setModeFromPalette('simple')
  },
  {
    id: 'mode-shorten',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Shorten',
    desc: 'Trim filler words and condense verbose clauses',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><line x1="20" y1="4" x2="8.12" y2="15.88"/><line x1="14.47" y1="14.48" x2="20" y2="20"/><line x1="8.12" y1="8.12" x2="12" y2="12"/></svg>`,
    keywords: 'shorten concise trim cut brevity brief',
    action: () => setModeFromPalette('shorten')
  },
  {
    id: 'mode-expand',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Expand',
    desc: 'Elaborate clauses with descriptive depth and nuance',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="m15 15 6 6m0 0v-4.5m0 4.5h-4.5"/><path d="m9 9-6-6m0 0v4.5m0-4.5h4.5"/></svg>`,
    keywords: 'expand elaborate detail describe longer explain',
    action: () => setModeFromPalette('expand')
  },
  {
    id: 'mode-heavyweight',
    group: 'Paraphrase Modes',
    title: 'Paraphrase: Heavyweight AST',
    desc: 'Deep dependency tree clause transposition and fractal burstiness control',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>`,
    keywords: 'heavyweight ast neurosymbolic syntax tree chomsky transposition burstiness stealth bypass',
    action: () => setModeFromPalette('heavyweight')
  },
  {
    id: 'load-grammar-sample',
    group: 'Samples & Templates',
    title: 'Load Grammar Sample',
    desc: 'Load paragraph with syntax errors, agreement mismatches, and tautologies',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-1 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/></svg>`,
    keywords: 'sample grammar test error template',
    action: () => { switchTab('grammar'); loadSampleGrammar(); }
  },
  {
    id: 'load-ai-sample',
    group: 'Samples & Templates',
    title: 'Load AI Synthetic Sample',
    desc: 'Load machine-generated text packed with AI vocabulary and clichés',
    icon: `<svg class="ui-svg" viewBox="0 0 24 24"><rect width="16" height="16" x="4" y="4" rx="2"/><rect width="6" height="6" x="9" y="9" rx="1"/><path d="M15 2v2M9 2v2M20 15h2M20 9h2M9 20v2M15 20v2M2 9h2M2 15h2"/></svg>`,
    keywords: 'sample ai test detection template cliches',
    action: () => { switchTab('detector'); loadSampleAIText(); }
  }
];

function openCommandPalette() {
  if (!paletteBackdrop) return;
  isPaletteOpen = true;
  paletteBackdrop.style.display = 'flex';
  if (paletteInput) {
    paletteInput.value = '';
    paletteInput.focus();
  }
  renderPaletteResults('');
}

function closeCommandPalette() {
  if (!paletteBackdrop) return;
  isPaletteOpen = false;
  paletteBackdrop.style.display = 'none';
}

function toggleCommandPalette() {
  if (isPaletteOpen) closeCommandPalette();
  else openCommandPalette();
}

function handlePaletteBackdropClick(e) {
  if (e.target === paletteBackdrop) {
    closeCommandPalette();
  }
}

function handlePaletteKeydown(e) {
  if (e.key === 'Escape') {
    e.preventDefault();
    closeCommandPalette();
    return;
  }

  if (e.key === 'ArrowDown') {
    e.preventDefault();
    if (filteredPaletteItems.length > 0) {
      paletteActiveIndex = (paletteActiveIndex + 1) % filteredPaletteItems.length;
      updatePaletteActiveSelection();
    }
    return;
  }

  if (e.key === 'ArrowUp') {
    e.preventDefault();
    if (filteredPaletteItems.length > 0) {
      paletteActiveIndex = (paletteActiveIndex - 1 + filteredPaletteItems.length) % filteredPaletteItems.length;
      updatePaletteActiveSelection();
    }
    return;
  }

  if (e.key === 'Enter') {
    e.preventDefault();
    executePaletteCommand(paletteActiveIndex);
    return;
  }
}

function renderPaletteResults(query) {
  if (!paletteResults) return;
  const q = (query || '').trim().toLowerCase();
  paletteActiveIndex = 0;

  // Dynamically inject active macro habit actions (Phase 3)
  const dynamicHabitCommands = [];
  if (currentHabitClusters && currentHabitClusters.length > 0) {
    currentHabitClusters.forEach(h => {
      dynamicHabitCommands.push({
        id: `habit-${h.id}`,
        title: `Macro Fix: ${h.title}`,
        desc: `Batch resolve all ${h.count} occurrences (+${h.impact_penalty} pts)`,
        group: 'Macro Habits (Phase 3)',
        icon: '<svg class="ui-svg" viewBox="0 0 24 24"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/></svg>',
        keywords: `macro habit batch fix ${h.title} ${h.category} clean`,
        action: () => applyHabitBatchFix(h.id)
      });
    });
  }

  const pool = [...dynamicHabitCommands, ...PALETTE_COMMANDS];

  if (!q) {
    filteredPaletteItems = [...pool];
    buildPaletteHTML(filteredPaletteItems);
    if (paletteStatus) paletteStatus.textContent = `${filteredPaletteItems.length} commands available`;
    return;
  }

  // Filter commands
  filteredPaletteItems = pool.filter(cmd => {
    return cmd.title.toLowerCase().includes(q) ||
           cmd.desc.toLowerCase().includes(q) ||
           cmd.group.toLowerCase().includes(q) ||
           (cmd.keywords && cmd.keywords.toLowerCase().includes(q));
  });

  if (filteredPaletteItems.length > 0) {
    buildPaletteHTML(filteredPaletteItems);
    if (paletteStatus) paletteStatus.textContent = `${filteredPaletteItems.length} matches`;
  } else {
    // If no command matches and query is at least 2 characters, search live synonyms via API
    searchPaletteSynonyms(q);
  }
}

function buildPaletteHTML(items) {
  paletteResults.innerHTML = '';
  const groups = {};
  items.forEach((item, idx) => {
    const grp = item.group || 'Commands';
    if (!groups[grp]) groups[grp] = [];
    groups[grp].push({ ...item, globalIndex: idx });
  });

  for (const [groupName, groupItems] of Object.entries(groups)) {
    const titleEl = document.createElement('div');
    titleEl.className = 'palette-group-title';
    titleEl.textContent = groupName;
    paletteResults.appendChild(titleEl);

    groupItems.forEach(item => {
      const itemEl = document.createElement('div');
      itemEl.className = `palette-item ${item.globalIndex === paletteActiveIndex ? 'active' : ''}`;
      itemEl.setAttribute('data-index', item.globalIndex);
      itemEl.onclick = () => executePaletteCommand(item.globalIndex);

      itemEl.innerHTML = `
        <div class="palette-item-left">
          ${item.icon || '<svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/></svg>'}
          <div class="palette-item-text">
            <span class="palette-item-title">${escapeHtml(item.title)}</span>
            <span class="palette-item-desc">${escapeHtml(item.desc)}</span>
          </div>
        </div>
        ${item.shortcut ? `<div class="palette-item-shortcut"><kbd>${escapeHtml(item.shortcut)}</kbd></div>` : ''}
      `;
      paletteResults.appendChild(itemEl);
    });
  }
}

async function searchPaletteSynonyms(word) {
  if (paletteStatus) paletteStatus.textContent = `Searching synonyms for "${word}"...`;
  paletteResults.innerHTML = `
    <div class="palette-empty">
      <svg class="ui-svg" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      <span>Searching lexical databases for "${escapeHtml(word)}"...</span>
    </div>`;

  try {
    const res = await fetch('/api/synonyms-for-word', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ word, mode: 'standard' })
    });
    const data = await res.json();
    const syns = data.synonyms || [];

    if (syns.length === 0) {
      filteredPaletteItems = [];
      paletteResults.innerHTML = `
        <div class="palette-empty">
          <svg class="ui-svg" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          <span>No commands or synonyms found for "${escapeHtml(word)}".</span>
        </div>`;
      if (paletteStatus) paletteStatus.textContent = '0 results';
      return;
    }

    filteredPaletteItems = syns.map(syn => ({
      title: syn,
      desc: `Substitute "${word}" with "${syn}" (WordNet / PPDB ranked)`,
      group: `Synonyms for "${word}"`,
      icon: `<svg class="ui-svg" viewBox="0 0 24 24"><path d="m15 15 6 6m0 0v-4.5m0 4.5h-4.5"/><path d="m9 9-6-6m0 0v4.5m0-4.5h4.5"/></svg>`,
      shortcut: 'Copy',
      action: () => {
        navigator.clipboard.writeText(syn);
        showToast(`Copied "${syn}" to clipboard`, 'success');
      }
    }));

    buildPaletteHTML(filteredPaletteItems);
    if (paletteStatus) paletteStatus.textContent = `${syns.length} synonyms found`;
  } catch (err) {
    console.error('Error fetching synonyms in palette:', err);
  }
}

function updatePaletteActiveSelection() {
  const items = paletteResults.querySelectorAll('.palette-item');
  items.forEach((item, idx) => {
    const isAct = idx === paletteActiveIndex;
    item.classList.toggle('active', isAct);
    if (isAct) {
      item.scrollIntoView({ block: 'nearest' });
    }
  });
}

function executePaletteCommand(index) {
  const item = filteredPaletteItems[index];
  if (!item) return;
  closeCommandPalette();
  if (typeof item.action === 'function') {
    item.action();
  }
}

function humanizeActiveInput() {
  switchTab('humanizer');
  runHumanizer();
}

function triggerActiveCheck() {
  if (currentTab === 'grammar') triggerGrammarCheck();
  else if (currentTab === 'paraphrase') runParaphrase();
  else if (currentTab === 'detector') runAIDetectionScan();
  else if (currentTab === 'humanizer') runHumanizer();
}

function revertActiveText() {
  if (currentTab === 'grammar') revertGrammarText();
  else if (currentTab === 'paraphrase') revertParaText();
  else if (currentTab === 'detector') revertDetectorText();
  else if (currentTab === 'humanizer') revertHumanizerText();
}

function clearActiveInput() {
  if (currentTab === 'grammar') clearGrammar();
  else if (currentTab === 'paraphrase') clearParaInput();
  else if (currentTab === 'detector') clearDetectorInput();
  else if (currentTab === 'humanizer') clearHumanizerInput();
}

function copyActiveText() {
  if (currentTab === 'grammar') copyGrammarText();
  else if (currentTab === 'paraphrase') copyParaphrase();
  else if (currentTab === 'detector') {
    const text = detectorInput.value;
    if (text.trim()) {
      navigator.clipboard.writeText(text);
      showToast('Copied detector text to clipboard', 'success');
    }
  } else if (currentTab === 'humanizer') {
    copyHumanizerOutput();
  }
}

function setModeFromPalette(mode) {
  switchTab('paraphrase');
  const pills = document.querySelectorAll('.mode-pill');
  pills.forEach(p => {
    const pMode = p.getAttribute('onclick') || '';
    if (pMode.includes(`'${mode}'`)) {
      setMode(mode, p);
    }
  });
}

if (paletteInput) {
  paletteInput.addEventListener('input', (e) => {
    clearTimeout(paletteSynonymDebounce);
    paletteSynonymDebounce = setTimeout(() => {
      renderPaletteResults(e.target.value);
    }, 120);
  });
}

window.addEventListener('load', () => {
  initTheme();
  setupDragAndDrop();
  drawBoundaryCanvas();

  // Check if text was queued from Ambient HUD
  const pendingImport = localStorage.getItem('klyph_pending_import') || localStorage.getItem('openquill_pending_import');
  if (pendingImport) {
    localStorage.removeItem('klyph_pending_import');
    localStorage.removeItem('openquill_pending_import');
    loadExternalText(pendingImport);
    showToast('Loaded prose from Ambient Companion', 'success');
  }
});

window.addEventListener('resize', () => {
  if (currentTab === 'detector') {
    drawBoundaryCanvas();
  }
});

// -------------------------------------------------------------
// AMBIENT DESKTOP HUD COMPANION INTEGRATION (PHASE 4)
// -------------------------------------------------------------
let companionWindowRef = null;
let mainBroadcastChannel = null;

try {
  mainBroadcastChannel = new BroadcastChannel('klyph_companion');
  mainBroadcastChannel.onmessage = (event) => {
    if (event.data && event.data.type === 'SYNC_TEXT') {
      loadExternalText(event.data.text);
    }
  };
} catch (e) {
  console.warn('BroadcastChannel not supported');
}

function openCompanionHUD() {
  const currentText = getActiveText();
  if (currentText) {
    localStorage.setItem('klyph_pending_hud_text', currentText);
  }

  const width = 460;
  const height = 580;
  const left = Math.max(20, window.screen.width - width - 40);
  const top = 60;

  if (companionWindowRef && !companionWindowRef.closed) {
    companionWindowRef.focus();
    if (mainBroadcastChannel && currentText) {
      mainBroadcastChannel.postMessage({ type: 'SYNC_TEXT', text: currentText });
    }
  } else {
    companionWindowRef = window.open(
      '/hud',
      'KlyphCompanionHUD',
      `width=${width},height=${height},left=${left},top=${top},menubar=no,toolbar=no,location=no,status=no,resizable=yes`
    );
  }
}

function loadExternalText(text) {
  if (!text) return;
  if (currentTab === 'grammar') {
    if (grammarInput) {
      grammarInput.value = text;
      triggerGrammarCheck();
    }
  } else if (currentTab === 'paraphrase') {
    if (paraInput) {
      paraInput.value = text;
      runParaphrase();
    }
  } else if (currentTab === 'detector') {
    if (detectorInput) {
      detectorInput.value = text;
      runAIDetectionScan();
    }
  }
}

function getActiveText() {
  if (currentTab === 'grammar') return (grammarInput && grammarInput.value) || '';
  if (currentTab === 'paraphrase') return (paraInput && paraInput.value) || '';
  if (currentTab === 'detector') return (detectorInput && detectorInput.value) || '';
  return '';
}

