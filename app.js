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
  const secNav = document.querySelector('.agi-section-nav');
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
    link.textContent = a.textContent.trim();
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
document.addEventListener('DOMContentLoaded', () => {
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
});
