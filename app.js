/* ══════════════════════════════════════════════════════
   LLM Academy — JavaScript
   ══════════════════════════════════════════════════════ */

/* ── Mode toggle ── */
let currentMode = 'layman';

const MODE_LABELS = {
  layman:     "Layman's Guide",
  graduate:   'Graduate Mode',
  researcher: 'Researcher Mode',
  team:       'Team Mode',
  startup:    'Startup Mode',
  investor:   "Investor's Perspective",
  founder:    "Founder's Perspective",
  agentmode:  'Agentic AI Mode',
};

function setMode(mode) {
  currentMode = mode;

  // Update hero title label with fade
  const lbl = document.getElementById('modeLabel');
  if (lbl) {
    lbl.style.opacity = '0';
    setTimeout(() => {
      lbl.textContent = MODE_LABELS[mode] || mode;
      // Swap gradient color per mode
      const gradients = {
        layman:     'linear-gradient(135deg,#4f46e5,#7c3aed)',
        graduate:   'linear-gradient(135deg,#7c3aed,#0891b2)',
        researcher: 'linear-gradient(135deg,#d97706,#dc2626)',
        team:       'linear-gradient(135deg,#059669,#0891b2)',
        startup:    'linear-gradient(135deg,#f97316,#ec4899)',
        investor:   'linear-gradient(135deg,#16a34a,#0891b2)',
        founder:    'linear-gradient(135deg,#d97706,#7c3aed)',
        agentmode:  'linear-gradient(135deg,#06b6d4,#6366f1)',
      };
      lbl.style.backgroundImage = gradients[mode] || gradients.layman;
      lbl.style.webkitBackgroundClip = 'text';
      lbl.style.backgroundClip = 'text';
      lbl.style.opacity = '1';
    }, 150);
  }

  // Support both old hero btn IDs and new navbar dropdown btn IDs
  const btnLayman   = document.getElementById('btnLayman')   || document.getElementById('modeBtn_layman');
  const btnGrad     = document.getElementById('btnGrad')     || document.getElementById('modeBtn_graduate');
  const btnResearch = document.getElementById('btnResearch') || document.getElementById('modeBtn_researcher');
  const btnTeam     = document.getElementById('btnTeam')     || document.getElementById('modeBtn_team');
  const btnStartup  = document.getElementById('btnStartup')  || document.getElementById('modeBtn_startup');
  const btnInvestor = document.getElementById('btnInvestor') || document.getElementById('modeBtn_investor');
  const btnFounder  = document.getElementById('btnFounder')  || document.getElementById('modeBtn_founder');
  const btnAgentMode= document.getElementById('btnAgentMode')|| document.getElementById('modeBtn_agentmode');

  // Reset all mode buttons (both old and new selectors)
  document.querySelectorAll('.mode-btn, .mode-panel-btn').forEach(b => b.classList.remove('active', 'mode-active'));
  [btnLayman, btnGrad, btnResearch, btnTeam, btnStartup, btnInvestor, btnFounder, btnAgentMode].forEach(b => b && b.classList.remove('active'));

  // Hide ALL mode content
  document.querySelectorAll('.layman-text, .grad-text, .researcher-text, .team-text, .startup-text, .investor-text, .founder-text, .agentmode-text')
    .forEach(el => el.classList.add('hidden'));

  // Hide special sections
  const gradSection     = document.getElementById('graduate-roadmap');
  const resSection      = document.getElementById('research-landscape');
  const teamSection     = document.getElementById('team-coordination');
  const startupSection  = document.getElementById('startup-journey');
  const investorSection = document.getElementById('investor-journey');
  const founderSection   = document.getElementById('founder-journey');
  const agentmodeSection = document.getElementById('agentmode-journey');
  const navTeam          = document.getElementById('navTeam');
  const navGrad          = document.getElementById('navGrad');
  const navResearch      = document.getElementById('navResearch');
  const navStartup       = document.getElementById('navStartup');
  const navInvestor      = document.getElementById('navInvestor');
  const navFounder       = document.getElementById('navFounder');
  const navAgentMode     = document.getElementById('navAgentMode');
  if (gradSection)           gradSection.classList.add('hidden');
  if (resSection)            resSection.classList.add('hidden');
  if (teamSection)           teamSection.classList.add('hidden');
  if (startupSection)        startupSection.classList.add('hidden');
  if (investorSection)       investorSection.classList.add('hidden');
  if (founderSection)        founderSection.classList.add('hidden');
  if (agentmodeSection)      agentmodeSection.classList.add('hidden');
  if (navTeam)          navTeam.classList.add('hidden');
  if (navGrad)          navGrad.classList.add('hidden');
  if (navResearch)      navResearch.classList.add('hidden');
  if (navStartup)       navStartup.classList.add('hidden');
  if (navInvestor)      navInvestor.classList.add('hidden');
  if (navFounder)       navFounder.classList.add('hidden');
  if (navAgentMode)     navAgentMode.classList.add('hidden');

  if (mode === 'layman') {
    btnLayman.classList.add('active');
    document.querySelectorAll('.layman-text').forEach(el => el.classList.remove('hidden'));

  } else if (mode === 'graduate') {
    btnGrad.classList.add('active');
    document.querySelectorAll('.grad-text').forEach(el => el.classList.remove('hidden'));
    if (gradSection) gradSection.classList.remove('hidden');
    if (navGrad)     navGrad.classList.remove('hidden');

  } else if (mode === 'researcher') {
    btnResearch.classList.add('active');
    document.querySelectorAll('.researcher-text, .grad-text').forEach(el => el.classList.remove('hidden'));
    if (resSection)  resSection.classList.remove('hidden');
    if (navResearch) navResearch.classList.remove('hidden');
    // Re-trigger paper timeline animations
    setTimeout(() => {
      document.querySelectorAll('.pt-item').forEach(el => {
        el.style.animation = 'none';
        void el.offsetWidth;
        el.style.animation = '';
      });
    }, 50);

  } else if (mode === 'team') {
    btnTeam.classList.add('active');
    document.querySelectorAll('.team-text').forEach(el => el.classList.remove('hidden'));
    if (teamSection) teamSection.classList.remove('hidden');
    if (navTeam)     navTeam.classList.remove('hidden');
    // Re-trigger gantt bar animations
    setTimeout(() => {
      document.querySelectorAll('.gantt-bar').forEach(el => {
        el.style.animation = 'none';
        void el.offsetWidth;
        el.style.animation = '';
      });
    }, 50);

  } else if (mode === 'startup') {
    btnStartup.classList.add('active');
    document.querySelectorAll('.startup-text').forEach(el => el.classList.remove('hidden'));
    if (startupSection) startupSection.classList.remove('hidden');
    if (navStartup)     navStartup.classList.remove('hidden');
    // Activate first infra tab if not already done
    setTimeout(() => {
      const firstItab = document.querySelector('.itab');
      if (firstItab && !document.querySelector('.itab.active')) {
        firstItab.classList.add('active');
      }
    }, 50);

  } else if (mode === 'investor') {
    btnInvestor.classList.add('active');
    document.querySelectorAll('.investor-text').forEach(el => el.classList.remove('hidden'));
    if (investorSection) investorSection.classList.remove('hidden');
    if (navInvestor)     navInvestor.classList.remove('hidden');

  } else if (mode === 'founder') {
    btnFounder.classList.add('active');
    document.querySelectorAll('.founder-text').forEach(el => el.classList.remove('hidden'));
    if (founderSection) founderSection.classList.remove('hidden');
    if (navFounder)     navFounder.classList.remove('hidden');

  } else if (mode === 'agentmode') {
    btnAgentMode.classList.add('active');
    document.querySelectorAll('.agentmode-text').forEach(el => el.classList.remove('hidden'));
    if (agentmodeSection) agentmodeSection.classList.remove('hidden');
    if (navAgentMode)     navAgentMode.classList.remove('hidden');
  }

  // Persist
  sessionStorage.setItem('llm-mode', mode);
}

/* ── Infrastructure tabs (startup mode) ── */
function showInfra(tab) {
  document.querySelectorAll('.infra-content').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.itab').forEach(el => el.classList.remove('active'));
  const pane = document.getElementById(`ic-${tab}`);
  if (pane) pane.classList.remove('hidden');
  const btn = document.querySelector(`.itab[onclick*="'${tab}'"]`);
  if (btn) btn.classList.add('active');
}

/* ── Reading tabs ── */
function showReading(tab) {
  document.querySelectorAll('.reading-content').forEach(el => el.classList.add('hidden'));
  document.querySelectorAll('.rtab').forEach(el => el.classList.remove('active'));
  const content = document.getElementById(`rc-${tab}`);
  if (content) content.classList.remove('hidden');
  event.target.classList.add('active');
}

/* ── Stage accordion ── */
function toggleStage(btn) {
  const card = btn.closest('.stage-card');
  const body = card.querySelector('.stage-body');
  const isOpen = body.classList.contains('open');

  // Close all
  document.querySelectorAll('.stage-body').forEach(b => b.classList.remove('open'));
  document.querySelectorAll('.stage-toggle').forEach(t => t.classList.remove('open'));

  if (!isOpen) {
    body.classList.add('open');
    btn.classList.add('open');

    // Trigger animations inside
    body.querySelectorAll('.bench-fill').forEach(el => {
      el.style.animation = 'none';
      void el.offsetWidth;
      el.style.animation = '';
    });
    body.querySelectorAll('.loss-line').forEach(el => {
      el.style.animation = 'none';
      void el.offsetWidth;
      el.style.animation = 'drawLine 3s ease forwards';
    });
  }
}

/* ── Stars ── */
function createStars() {
  const container = document.getElementById('stars');
  if (!container) return;
  const count = 150;
  for (let i = 0; i < count; i++) {
    const star = document.createElement('div');
    star.className = 'star';
    star.style.cssText = `
      left: ${Math.random() * 100}%;
      top:  ${Math.random() * 100}%;
      --d:  ${2 + Math.random() * 4}s;
      --del:${Math.random() * 4}s;
      --op: ${0.3 + Math.random() * 0.7};
      width: ${1 + Math.random() * 2}px;
      height: ${1 + Math.random() * 2}px;
    `;
    container.appendChild(star);
  }
}

/* ── Neural network canvas animation ── */
function initNeuralCanvas() {
  const wrapper = document.getElementById('neuralCanvas');
  if (!wrapper) return;

  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;opacity:0.25;';
  wrapper.appendChild(canvas);

  const ctx = canvas.getContext('2d');
  let nodes = [];
  let connections = [];
  let W, H;

  function resize() {
    W = canvas.width  = wrapper.offsetWidth;
    H = canvas.height = wrapper.offsetHeight;
    buildGraph();
  }

  function buildGraph() {
    nodes = [];
    connections = [];
    const layers = [4, 6, 6, 5, 3];
    const layerGap = W / (layers.length + 1);

    layers.forEach((count, li) => {
      const x = layerGap * (li + 1);
      const nodeGap = H / (count + 1);
      for (let ni = 0; ni < count; ni++) {
        nodes.push({ x, y: nodeGap * (ni + 1), r: 4, pulse: Math.random() * Math.PI * 2 });
      }
    });

    // Connect adjacent layers
    let offset = 0;
    for (let li = 0; li < layers.length - 1; li++) {
      for (let a = 0; a < layers[li]; a++) {
        for (let b = 0; b < layers[li + 1]; b++) {
          connections.push({ a: offset + a, b: offset + layers[li] + b, pulse: Math.random() });
        }
      }
      offset += layers[li];
    }
  }

  let frame = 0;
  function draw() {
    ctx.clearRect(0, 0, W, H);
    frame++;
    const t = frame / 60;

    // Draw connections
    connections.forEach(c => {
      const na = nodes[c.a], nb = nodes[c.b];
      const alpha = 0.05 + 0.08 * Math.sin(t * 2 + c.pulse * 10);
      ctx.strokeStyle = `rgba(99,102,241,${alpha})`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(na.x, na.y);
      ctx.lineTo(nb.x, nb.y);
      ctx.stroke();
    });

    // Draw signal pulses
    if (frame % 8 === 0) {
      connections.forEach(c => {
        if (Math.random() < 0.02) {
          c.activePulse = 0;
        }
      });
    }
    connections.forEach(c => {
      if (c.activePulse !== undefined) {
        c.activePulse += 0.04;
        if (c.activePulse >= 1) { delete c.activePulse; return; }
        const na = nodes[c.a], nb = nodes[c.b];
        const px = na.x + (nb.x - na.x) * c.activePulse;
        const py = na.y + (nb.y - na.y) * c.activePulse;
        const grad = ctx.createRadialGradient(px, py, 0, px, py, 6);
        grad.addColorStop(0, 'rgba(99,102,241,0.8)');
        grad.addColorStop(1, 'rgba(99,102,241,0)');
        ctx.fillStyle = grad;
        ctx.beginPath();
        ctx.arc(px, py, 6, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // Draw nodes
    nodes.forEach(n => {
      n.pulse += 0.03;
      const brightness = 0.3 + 0.3 * Math.sin(n.pulse);
      ctx.fillStyle = `rgba(99,102,241,${brightness})`;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
      ctx.fill();

      const glow = ctx.createRadialGradient(n.x, n.y, 0, n.x, n.y, n.r * 3);
      glow.addColorStop(0, `rgba(99,102,241,${brightness * 0.5})`);
      glow.addColorStop(1, 'rgba(99,102,241,0)');
      ctx.fillStyle = glow;
      ctx.beginPath();
      ctx.arc(n.x, n.y, n.r * 3, 0, Math.PI * 2);
      ctx.fill();
    });

    requestAnimationFrame(draw);
  }

  window.addEventListener('resize', resize);
  resize();
  draw();
}

/* ── Scroll reveal ── */
function initScrollReveal() {
  const items = document.querySelectorAll('.stage-card, .resource-card, .roadmap-phase, .resource-link');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.animation = 'fadeInUp 0.5s ease both';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  items.forEach(item => {
    item.style.opacity = '0';
    observer.observe(item);
  });
}

/* ── Slide-down nav panels ── */
function closeAllNavPanels() {
  document.querySelectorAll('.nav-panel.open').forEach(p => p.classList.remove('open'));
  document.querySelectorAll('.nav-tab.active').forEach(t => {
    t.classList.remove('active');
    const ch = t.querySelector('.nav-chevron');
    if (ch) ch.style.transform = '';
  });
  const bd = document.getElementById('navBackdrop');
  if (bd) bd.classList.remove('open');
}

function initNavPanels() {
  const backdrop = document.getElementById('navBackdrop');

  document.querySelectorAll('.nav-tab').forEach(tab => {
    tab.addEventListener('click', e => {
      e.stopPropagation();
      const panel = document.getElementById('navPanel-' + tab.dataset.panel);
      const isOpen = panel && panel.classList.contains('open');
      closeAllNavPanels();
      if (!isOpen && panel) {
        panel.classList.add('open');
        tab.classList.add('active');
        const ch = tab.querySelector('.nav-chevron');
        if (ch) ch.style.transform = 'rotate(180deg)';
        if (backdrop) backdrop.classList.add('open');
      }
    });
  });

  if (backdrop) backdrop.addEventListener('click', closeAllNavPanels);
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeAllNavPanels(); });
}

/* ── Smooth navbar hide/show on scroll ── */
function initNavbar() {
  let lastY = 0;
  const nav = document.querySelector('.navbar');
  const wrap = document.getElementById('navPanelWrap');
  window.addEventListener('scroll', () => {
    const y = window.scrollY;
    if (y > lastY && y > 120) {
      closeAllNavPanels();
      nav.style.transform = 'translateY(-100%)';
      nav.style.transition = 'transform 0.3s ease';
      if (wrap) { wrap.style.transform = 'translateY(-100%)'; wrap.style.transition = 'transform 0.3s ease'; }
    } else {
      nav.style.transform = '';
      if (wrap) wrap.style.transform = '';
    }
    lastY = y;
  });
}

/* ── Add SVG gradient for loss chart ── */
function addSvgDefs() {
  const svgs = document.querySelectorAll('.loss-svg');
  svgs.forEach(svg => {
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    defs.innerHTML = `
      <linearGradient id="lossGrad" x1="0" y1="0" x2="1" y2="0">
        <stop offset="0%" stop-color="#6366f1"/>
        <stop offset="100%" stop-color="#06b6d4"/>
      </linearGradient>
    `;
    svg.prepend(defs);
  });
}

/* ── Typing animation for tokenizer ── */
function initTypingDemo() {
  const phrases = [
    "Hello, I love building AI systems!",
    "The transformer architecture changed everything.",
    "Training on trillions of tokens requires patience.",
    "Large language models can write code and poetry."
  ];
  let pi = 0;
  const inp = document.getElementById('tokenInput');
  if (!inp) return;

  const tokenColors = ['#ff6b6b','#ffa07a','#ffd700','#90ee90','#87ceeb','#dda0dd','#f0e68c','#ff8c69','#00ced1','#da70d6'];

  setInterval(() => {
    pi = (pi + 1) % phrases.length;
    inp.textContent = phrases[pi];
    const out = document.getElementById('tokenOutput');
    if (!out) return;
    out.innerHTML = '';
    const words = phrases[pi].split(' ');
    words.forEach((w, i) => {
      const span = document.createElement('span');
      span.className = 'tok';
      span.style.setProperty('--c', tokenColors[i % tokenColors.length]);
      span.textContent = w;
      out.appendChild(span);
    });
  }, 3000);
}

/* ── Blog nav panel population ── */
async function loadBlogNavPosts() {
  const menu = document.getElementById('blogNavMenu');
  if (!menu) return;
  const path = window.location.pathname;
  const isBlogPost = path.includes('/blog/');   // blog/slug.html
  const isPage     = path.includes('/pages/');  // pages/foo.html
  const jsonPath   = isBlogPost || isPage ? '../blog/index.json' : 'blog/index.json';
  try {
    const r = await fetch(jsonPath);
    if (!r.ok) return;
    const data = await r.json();
    (data.posts || []).slice(0, 4).forEach(p => {
      const a = document.createElement('a');
      a.href = isBlogPost ? `${p.slug}.html`
             : isPage     ? `../blog/${p.slug}.html`
             :               `blog/${p.slug}.html`;
      a.className = 'panel-btn';
      a.textContent = `${p.emoji || '📝'} ${p.title}`;
      a.style.cssText = 'font-size:0.82rem;white-space:normal;line-height:1.3;';
      menu.appendChild(a);
    });
  } catch (_) {}
}

/* ── Article on-page nav: convert the horizontal pill bar into a left sidebar ── */
function initArticleSidebarNav() {
  // Every in-article section nav: the shared .agi-section-nav plus the per-article variants
  // (xx-section-nav, fde-nav, sk-nav, sb-nav, phase-nav, fr-toc).
  // Articles without a section nav: build one from their headings (h2[id], or h2 inside section[id])
  const wrap0 = document.querySelector('.blog-post-wrap');
  if (wrap0 && !wrap0.querySelector('.agi-section-nav, [class$="-section-nav"], .fde-nav, .sk-nav, .sb-nav, .phase-nav, .fr-toc')) {
    const heads = Array.from(wrap0.querySelectorAll('h2')).map(h => {
      let id = h.id || (h.closest('section[id]') || {}).id;
      if (!id) {
        id = 'sec-' + h.textContent.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 48);
        if (!id || document.getElementById(id)) return null;
        h.id = id; h.style.scrollMarginTop = '110px';
      }
      return [id, h.textContent.trim()];
    }).filter(Boolean).filter((x, i, arr) => arr.findIndex(y => y[0] === x[0]) === i);
    if (heads.length >= 4) {
      const first = document.getElementById(heads[0][0]);
      let anchor = first;
      while (anchor && anchor.parentNode !== wrap0) anchor = anchor.parentNode;
      if (anchor) {
        const auto = document.createElement('div');
        auto.className = 'agi-section-nav';
        heads.forEach(([id, t]) => { const l = document.createElement('a'); l.href = '#' + id; l.textContent = t; auto.appendChild(l); });
        wrap0.insertBefore(auto, anchor);
      }
    }
  }
  const secNav = document.querySelector('.blog-post-wrap .agi-section-nav, .blog-post-wrap [class$="-section-nav"], .blog-post-wrap .fde-nav, .blog-post-wrap .sk-nav, .blog-post-wrap .sb-nav, .blog-post-wrap .phase-nav, .blog-post-wrap .fr-toc');
  const wrap = document.querySelector('.blog-post-wrap');
  if (!secNav || !wrap) return;

  const links = Array.from(secNav.querySelectorAll('a[href^="#"]'));
  if (links.length < 3) return; // not worth a sidebar for a very short nav

  // Mark where the old nav sat so we can splice the new layout in at the same spot
  const placeholder = document.createElement('div');
  secNav.parentNode.insertBefore(placeholder, secNav);

  // Everything that came after the nav is the article body — move it under the sidebar
  const main = document.createElement('div');
  main.className = 'blog-article-main';
  let node = secNav.nextSibling;
  while (node) {
    const next = node.nextSibling;
    main.appendChild(node);
    node = next;
  }

  const sidebar = document.createElement('aside');
  sidebar.className = 'blog-article-sidebar';
  sidebar.innerHTML = '<div class="blog-article-sidebar-title">📑 On This Page</div><nav class="blog-article-sidebar-nav"></nav>';
  const navEl = sidebar.querySelector('.blog-article-sidebar-nav');
  links.forEach(a => {
    const link = document.createElement('a');
    link.href = a.getAttribute('href');
    link.textContent = Array.from(a.childNodes).map(n => n.textContent.trim()).filter(Boolean).join(' ');
    navEl.appendChild(link);
  });

  const toggleBtn = document.createElement('button');
  toggleBtn.type = 'button';
  toggleBtn.className = 'blog-article-toggle-btn';
  toggleBtn.textContent = '☰ Contents';
  toggleBtn.onclick = () => sidebar.classList.toggle('is-collapsed');

  const layout = document.createElement('div');
  layout.className = 'blog-article-layout';
  layout.appendChild(sidebar);
  layout.appendChild(main);

  placeholder.replaceWith(toggleBtn, layout);
  secNav.remove();

  // Highlight the section currently in view
  const navLinks = Array.from(navEl.querySelectorAll('a'));
  const targets = links.map(a => {
    try { return document.querySelector(a.getAttribute('href')); } catch (_) { return null; }
  });
  function onScroll() {
    let idx = 0;
    const pos = window.scrollY + 160;
    targets.forEach((t, i) => { if (t && t.offsetTop <= pos) idx = i; });
    navLinks.forEach((l, i) => l.classList.toggle('is-active', i === idx));
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // On small screens, collapse the sidebar automatically after a jump
  navLinks.forEach(l => l.addEventListener('click', () => {
    if (window.matchMedia('(max-width: 900px)').matches) sidebar.classList.add('is-collapsed');
  }));
}

/* ── Init ── */

/* ── Reading history + "Latest from the Academy" personal panel ──────────────
   Stored only in this browser (localStorage); everything degrades silently. */
const FA_READ = 'fa-read', FA_KNOWN = 'fa-known', FA_NEW = 'fa-new';
function faGet(store, k, d) { try { const v = store.getItem(k); return v ? JSON.parse(v) : d; } catch (_) { return d; } }
function faSet(store, k, v) { try { store.setItem(k, JSON.stringify(v)); } catch (_) {} }
function faReadList() { return faGet(localStorage, FA_READ, []); }

function recordArticleVisit() {
  const m = window.location.pathname.match(/\/blog\/([^\/]+)\.html$/);
  if (!m || m[1].startsWith('_')) return;
  const list = faReadList().filter(x => x.s !== m[1]);
  list.unshift({ s: m[1], t: Date.now() });
  faSet(localStorage, FA_READ, list.slice(0, 60));
}

async function initLatestThreads() {
  const root = document.getElementById('latestThreads');
  if (!root) return;
  const read = faReadList(), readSet = new Set(read.map(x => x.s));
  root.querySelectorAll('.lt-dot').forEach(d => { if (readSet.has(d.dataset.slug)) d.classList.add('is-read'); });
  let posts, series;
  try {
    const [a, b] = await Promise.all([fetch('blog/index.json'), fetch('blog/series.json')]);
    posts = (await a.json()).posts || []; series = (await b.json()).series || [];
  } catch (_) { return; }
  const bySlug = {}; posts.forEach(p => { bySlug[p.slug] = p; });
  // "New since your last visit": compare with the posts this browser saw last time (kept for the session)
  let fresh = faGet(sessionStorage, FA_NEW, null);
  if (!fresh) {
    const known = faGet(localStorage, FA_KNOWN, null);
    fresh = known ? posts.map(p => p.slug).filter(s => !known.includes(s)) : [];
    faSet(sessionStorage, FA_NEW, fresh);
    faSet(localStorage, FA_KNOWN, posts.map(p => p.slug));
  }
  root.querySelectorAll('.lt-card').forEach(c => {
    if (fresh.includes(c.dataset.slug) && !readSet.has(c.dataset.slug)) { c.classList.add('is-new'); const b = c.querySelector('.lt-new'); if (b) b.hidden = false; }
  });
  const esc = s => String(s).replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  const link = (slug, text) => '<a href=\x22blog/' + slug + '.html\x22>' + esc(text) + '</a>';
  const boxes = [];
  const unreadNew = fresh.filter(s => bySlug[s] && !readSet.has(s));
  if (unreadNew.length) boxes.push('<div class="lt-pbox"><b class="h">🆕 ' + unreadNew.length + ' new since your last visit</b>' + unreadNew.slice(0, 4).map(s => '<div>' + link(s, bySlug[s].title) + '</div>').join('') + '</div>');
  // Continue your thread: the most recently read post whose series still has an unread next part
  for (const r of read) {
    const ser = series.find(x => x.slugs.includes(r.s));
    if (!ser) continue;
    const next = ser.slugs.slice(ser.slugs.indexOf(r.s) + 1).find(s => bySlug[s] && !readSet.has(s));
    if (next) { boxes.push('<div class="lt-pbox"><b class="h">▶ Continue your thread · ' + esc(ser.icon + ' ' + ser.short) + '</b>Next: ' + link(next, bySlug[next].title) + '<div style="font-size:.74rem;color:#64748b;margin-top:4px">You read ' + ser.slugs.filter(s => readSet.has(s)).length + ' of ' + ser.slugs.length + ' in this series.</div></div>'); break; }
  }
  const trail = read.filter(r => bySlug[r.s]).slice(0, 6);
  if (trail.length) boxes.push('<div class="lt-pbox"><b class="h">👣 Your reading trail</b><div class="lt-chips">' + trail.map((r, i) => (i ? '<i>←</i>' : '') + link(r.s, bySlug[r.s].title)).join('') + '</div></div>');
  const panel = document.getElementById('ltPersonal');
  if (panel && boxes.length) { panel.innerHTML = boxes.join(''); panel.hidden = false; }
}

// ── Maestro films: a small scene player for documentary-style animated diagrams ──
// MoFilm(el, {title, scenes:[{t, cap, dur, render(p, S) -> svg string, counters(p) -> [[label, value]]}]})
// p runs 0..1 within a scene. Elements with data-def="..." show a plain-English definition when tapped.
window.MoFilm = function (el, cfg) {
  const W = cfg.w || 480, H = cfg.h || 300, sc = cfg.scenes;
  let i = 0, t0 = 0, el0 = 0, playing = false, raf = 0, last = 0;
  el.classList.add('mf'); if (cfg.scenes.length === 1) el.classList.add('mf-one');
  el.innerHTML = '<div class="mf-top"><b>🎬 ' + cfg.title + '</b><span class="mf-sim">animated diagram · numbers from this article&#39;s scripts</span></div>' +
    '<div class="mf-stage"><svg viewBox="0 0 ' + W + ' ' + H + '" role="img"></svg><div class="mf-def" hidden></div></div>' +
    '<div class="mf-cap"><span class="mf-n"></span><b class="mf-t"></b><span class="mf-c"></span></div><div class="mf-ctr"></div>' +
    '<div class="mf-ctl"><button type="button" data-a="prev" aria-label="Previous scene">⏮</button><button type="button" data-a="play" class="mf-play" aria-label="Play or pause">▶</button><button type="button" data-a="next" aria-label="Next scene">⏭</button>' +
    '<div class="mf-dots">' + sc.map((s, k) => '<button type="button" data-k="' + k + '" title="' + s.t.replace(/"/g, '') + '"></button>').join('') + '</div></div>';
  const svg = el.querySelector('svg'), def = el.querySelector('.mf-def');
  function frame(now) {
    const s = sc[i], d = s.dur || 7000;
    let p = playing ? Math.min(1, el0 + (now - t0) / d) : el0;
    if (!playing || now - last > 33) {
      last = now;
      svg.innerHTML = s.render(p, { W: W, H: H, now: now });
      el.querySelector('.mf-ctr').innerHTML = (s.counters ? s.counters(p) : []).map(c => '<span><i>' + c[0] + '</i><b>' + c[1] + '</b></span>').join('');
    }
    if (playing && p >= 1) { if (i < sc.length - 1) { go(i + 1, true); return; } playing = false; el.querySelector('.mf-play').textContent = '↺'; }
    if (playing) raf = requestAnimationFrame(frame);
  }
  function go(k, keep) {
    i = Math.max(0, Math.min(sc.length - 1, k)); el0 = 0; t0 = performance.now(); def.hidden = true;
    el.querySelector('.mf-n').textContent = sc.length === 1 ? (cfg.label || '') : 'Scene ' + (i + 1) + ' of ' + sc.length;
    el.querySelector('.mf-t').textContent = sc[i].t; el.querySelector('.mf-c').innerHTML = sc[i].cap;
    el.querySelectorAll('.mf-dots button').forEach((b, j) => b.className = j === i ? 'on' : j < i ? 'done' : '');
    cancelAnimationFrame(raf); if (playing || keep) { playing = true; raf = requestAnimationFrame(frame); } else frame(performance.now());
  }
  function toggle() {
    if (playing) { el0 = Math.min(1, el0 + (performance.now() - t0) / (sc[i].dur || 7000)); playing = false; cancelAnimationFrame(raf); el.querySelector('.mf-play').textContent = '▶'; }
    else { if (i === sc.length - 1 && el0 >= 1) { go(0, true); } else { playing = true; t0 = performance.now(); raf = requestAnimationFrame(frame); } el.querySelector('.mf-play').textContent = '⏸'; }
  }
  el.querySelector('.mf-ctl').addEventListener('click', e => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.k !== undefined) go(+b.dataset.k, playing);
    else if (b.dataset.a === 'play') toggle();
    else if (b.dataset.a === 'prev') go(i - 1, playing);
    else if (b.dataset.a === 'next') go(i + 1, playing);
  });
  svg.addEventListener('click', e => {
    const g = e.target.closest('[data-def]'); if (!g) { def.hidden = true; return; }
    def.innerHTML = g.getAttribute('data-def'); def.hidden = false;
  });
  go(0, false);
  // start when scrolled into view, once
  if ('IntersectionObserver' in window && cfg.autoplay !== false) {
    const io = new IntersectionObserver(es => { if (es[0].isIntersecting && !playing && i === 0 && el0 === 0) { toggle(); io.disconnect(); } }, { threshold: 0.6 });
    io.observe(el);
  }
};

// Drawing helpers shared by scene scripts, and a placer that puts one player after each section heading.
window.MoSvg = {
  T: function (x, y, s, o) { o = o || {}; return '<text x="' + x + '" y="' + y + '" font-size="' + (o.size || 14) + '" fill="' + (o.fill || '#0f172a') + '" text-anchor="' + (o.a || 'middle') + '" font-weight="' + (o.w || 600) + '"' + (o.op != null ? ' opacity="' + o.op + '"' : '') + '>' + s + '</text>'; },
  R: function (x, y, w, h, f, o) { o = o || {}; return '<rect x="' + x + '" y="' + y + '" width="' + Math.max(0, w) + '" height="' + Math.max(0, h) + '" rx="' + (o.rx == null ? 6 : o.rx) + '" fill="' + f + '"' + (o.s ? ' stroke="' + o.s + '" stroke-width="' + (o.sw || 1.5) + '"' : '') + (o.op != null ? ' opacity="' + o.op + '"' : '') + '/>'; },
  G: function (def, inner) { return '<g data-def="' + def + '">' + inner + '</g>'; },
  cl: function (v) { return Math.max(0, Math.min(1, v)); },
  ease: function (v) { v = Math.max(0, Math.min(1, v)); return v * v * (3 - 2 * v); },
  path: function (pts) { return pts.map(function (p, i) { return (i ? 'L' : 'M') + p[0].toFixed(1) + ' ' + p[1].toFixed(1); }).join(' '); }
};
window.MoScenes = function (part, list) {
  if (!window.MoFilm) return;
  list.forEach(function (it, k) {
    var h = document.getElementById(it.place); if (!h) return;
    var box = document.createElement('div'); box.id = 'scene' + part + '-' + (k + 1);
    var after = h; while (after.nextElementSibling && after.nextElementSibling.id && after.nextElementSibling.id.indexOf('scene' + part + '-') === 0) after = after.nextElementSibling;
    after.after(box);
    MoFilm(box, { title: it.scene.t, label: 'Animated scene · Part ' + part, scenes: [it.scene] });
  });
};
// The recurring "cluster" character: 1,024 GPUs as 128 nodes x 8 GPUs.
// colour(node, gpu) -> fill; returns an SVG group string.
window.MoCluster = function (x, y, w, colour, opts) {
  opts = opts || {};
  const cols = 16, rows = 8, gap = 3, nw = (w - gap * (cols - 1)) / cols, gw = (nw - 4) / 4, nh = gw * 2 + 6;
  let s = '<g data-def="' + (opts.def || 'The whole cluster: 128 servers (nodes), each with 8 GPUs = 1,024 GPUs. Each small square is one GPU.') + '">';
  for (let n = 0; n < 128; n++) {
    const cx = x + (n % cols) * (nw + gap), cy = y + Math.floor(n / cols) * (nh + gap);
    s += '<rect x="' + cx.toFixed(1) + '" y="' + cy.toFixed(1) + '" width="' + nw.toFixed(1) + '" height="' + nh.toFixed(1) + '" rx="2" fill="#f1f5f9" stroke="' + (opts.stroke ? opts.stroke(n) : '#cbd5e1') + '" stroke-width="' + (opts.stroke ? 1.6 : 0.6) + '"/>';
    for (let g = 0; g < 8; g++) s += '<rect x="' + (cx + 2 + (g % 4) * gw).toFixed(1) + '" y="' + (cy + 2 + Math.floor(g / 4) * (gw + 2)).toFixed(1) + '" width="' + (gw - 1).toFixed(1) + '" height="' + (gw - 1).toFixed(1) + '" rx="1" fill="' + colour(n, g) + '"/>';
  }
  return s + '</g>';
};

// ── Article reader: browser text-to-speech for every blog article ──
function initArticleReader() {
  if (!/\/blog\/[^/]+\.html$/.test(location.pathname) || !('speechSynthesis' in window)) return;
  const root = document.querySelector('.blog-post-wrap') || document.querySelector('main');
  if (!root) return;
  const SKIP = 'nav, pre, code, table, svg, script, style, button, select, .mo-code, .mo-out, .blog-breadcrumb, [class*="section-nav"], .ar-reader, .ar-bar, .series-nav, [aria-hidden="true"]';
  const els = [...root.querySelectorAll('h1, h2, h3, h4, p, li, dd, blockquote')].filter(el => !el.closest(SKIP) && !(el.tagName !== 'LI' && el.closest('li')));
  const items = [];
  els.forEach(el => {
    const c = el.cloneNode(true);
    c.querySelectorAll('ul, ol, pre, code, svg, button').forEach(x => x.remove());
    const t = c.textContent.replace(/\s+/g, ' ').trim();
    if (t.length < 3) return;
    const parts = t.match(/[^.!?]+[.!?]*["”)]*\s*/g) || [t];
    let buf = '';
    parts.forEach(p => { if ((buf + p).length > 220 && buf) { items.push({ el, text: buf.trim() }); buf = ''; } buf += p; });
    if (buf.trim()) items.push({ el, text: buf.trim() });
  });
  if (items.length < 3) return;
  const words = items.reduce((n, i) => n + i.text.split(' ').length, 0);
  const synth = window.speechSynthesis;
  let idx = 0, playing = false, rate = parseFloat(localStorage.getItem('ar-rate') || '1'), voice = null;

  const pill = document.createElement('div');
  pill.className = 'ar-reader';
  pill.innerHTML = '<button type="button" class="ar-listen">🔊 Listen to this article</button><span>~' + Math.max(1, Math.round(words / 160)) + ' min · read aloud by your browser</span>';
  const anchor = root.querySelector('.blog-meta-row') || root.querySelector('h1');
  if (anchor) anchor.after(pill); else root.prepend(pill);

  const bar = document.createElement('div');
  bar.className = 'ar-bar'; bar.hidden = true;
  bar.innerHTML = '<button type="button" data-a="prev" title="Previous">⏮</button><button type="button" data-a="play" class="ar-main" title="Play / pause">⏸</button><button type="button" data-a="next" title="Next">⏭</button>' +
    '<select data-a="rate" title="Speed">' + [0.75, 1, 1.25, 1.5, 1.75, 2].map(r => '<option value="' + r + '"' + (r === rate ? ' selected' : '') + '>' + r + '×</option>').join('') + '</select>' +
    '<select data-a="voice" title="Voice" class="ar-voice"></select><span class="ar-prog"></span><button type="button" data-a="stop" title="Stop">✕</button>';
  document.body.appendChild(bar);
  const vSel = bar.querySelector('[data-a="voice"]');
  function loadVoices() {
    const vs = synth.getVoices().filter(v => /^en/i.test(v.lang));
    if (!vs.length) return;
    const saved = localStorage.getItem('ar-voice');
    vSel.innerHTML = vs.map(v => '<option value="' + v.name.replace(/"/g, '') + '">' + v.name.replace(/</g, '') + ' (' + v.lang + ')</option>').join('');
    voice = vs.find(v => v.name === saved) || vs.find(v => v.default) || vs[0];
    vSel.value = voice.name.replace(/"/g, '');
  }
  loadVoices(); synth.onvoiceschanged = loadVoices;

  function mark() {
    root.querySelectorAll('.ar-now').forEach(e => e.classList.remove('ar-now'));
    const it = items[idx]; if (!it) return;
    it.el.classList.add('ar-now');
    const r = it.el.getBoundingClientRect();
    if (r.top < 100 || r.bottom > innerHeight - 90) it.el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    bar.querySelector('.ar-prog').textContent = Math.round(idx / items.length * 100) + '%';
  }
  function speak() {
    synth.cancel();
    if (idx >= items.length) { stop(); return; }
    const u = new SpeechSynthesisUtterance(items[idx].text);
    u.rate = rate; if (voice) u.voice = voice;
    u.onend = () => { if (playing) { idx++; speak(); } };
    mark(); synth.speak(u);
  }
  function play() { playing = true; bar.hidden = false; bar.querySelector('.ar-main').textContent = '⏸'; speak(); }
  function pause() { playing = false; synth.cancel(); bar.querySelector('.ar-main').textContent = '▶'; }
  function stop() { pause(); bar.hidden = true; root.querySelectorAll('.ar-now').forEach(e => e.classList.remove('ar-now')); }
  pill.querySelector('.ar-listen').addEventListener('click', () => { if (playing) pause(); else play(); });
  bar.addEventListener('click', e => {
    const a = e.target.closest('button') && e.target.closest('button').dataset.a;
    if (a === 'play') playing ? pause() : play();
    else if (a === 'prev') { idx = Math.max(0, idx - 1); if (playing) speak(); else mark(); }
    else if (a === 'next') { idx = Math.min(items.length - 1, idx + 1); if (playing) speak(); else mark(); }
    else if (a === 'stop') stop();
  });
  bar.querySelector('[data-a="rate"]').addEventListener('change', e => { rate = +e.target.value; try { localStorage.setItem('ar-rate', rate); } catch (x) {} if (playing) speak(); });
  vSel.addEventListener('change', () => { voice = synth.getVoices().find(v => v.name.replace(/"/g, '') === vSel.value) || voice; try { localStorage.setItem('ar-voice', voice.name); } catch (x) {} if (playing) speak(); });
  // click any paragraph while the bar is open to start reading from there
  root.addEventListener('dblclick', e => { const i = items.findIndex(it => it.el.contains(e.target)); if (i >= 0 && !bar.hidden) { idx = i; play(); } });
  window.addEventListener('pagehide', () => synth.cancel());
}

document.addEventListener('DOMContentLoaded', () => {
  recordArticleVisit();
  initLatestThreads();
  createStars();
  initNeuralCanvas();
  initScrollReveal();
  initNavbar();
  initNavPanels();
  addSvgDefs();
  initTypingDemo();

  // Read ?mode= URL param (used when navigating from other pages via Learning Mode dropdown)
  const urlMode = new URLSearchParams(window.location.search).get('mode');
  if (urlMode && MODE_LABELS[urlMode]) {
    setMode(urlMode);
  } else {
    // Restore last mode from session
    const saved = sessionStorage.getItem('llm-mode');
    if (saved) setMode(saved);
  }

  // Open first stage by default
  const firstToggle = document.querySelector('.stage-toggle');
  if (firstToggle) toggleStage(firstToggle);

  // Populate blog nav dropdown
  loadBlogNavPosts();

  // Convert an article's on-page section nav into a left sidebar, if present
  initArticleSidebarNav();

  // Listen button: read the article aloud with the browser's speech engine
  initArticleReader();
});
