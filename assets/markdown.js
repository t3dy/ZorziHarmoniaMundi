/* Shared block-based markdown renderer.
   Replaces the old regex-chain parser that wrapped headings in <p> tags
   and converted every newline to <br>, producing huge vertical gaps. */

function mdEscape(s) {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
}

function mdInline(s) {
  return mdEscape(s)
    .replace(/&lt;cite&gt;([\s\S]+?)&lt;\/cite&gt;/g, '<cite>$1</cite>')
    .replace(/\*\*\*(.+?)\*\*\*/g, '<strong><em>$1</em></strong>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>');
}

function mdSlug(s) {
  return s.toLowerCase()
    .replace(/<[^>]+>/g, '')
    .replace(/[^a-z0-9\s-]/g, '')
    .trim()
    .replace(/\s+/g, '-')
    .slice(0, 60);
}

function mdToHtml(md, opts) {
  opts = opts || {};
  const lines = md.split('\n');
  const out = [];
  let para = [];

  function flushPara() {
    if (para.length) {
      out.push('<p>' + mdInline(para.join(' ')) + '</p>');
      para = [];
    }
  }

  for (const raw of lines) {
    const line = raw.trimEnd();
    if (!line.trim()) { flushPara(); continue; }
    let m;
    if ((m = line.match(/^###\s+(.+)/))) {
      flushPara();
      const inner = mdInline(m[1]);
      out.push('<h3 id="' + mdSlug(m[1]) + '">' + inner + '</h3>');
    } else if ((m = line.match(/^##\s+(.+)/))) {
      flushPara();
      const inner = mdInline(m[1]);
      out.push('<h2 id="' + mdSlug(m[1]) + '">' + inner + '</h2>');
    } else if ((m = line.match(/^#\s+(.+)/))) {
      flushPara();
      const inner = mdInline(m[1]);
      // Skip the top-level title if the page header already shows it
      if (!opts.skipH1) out.push('<h1>' + inner + '</h1>');
    } else if (/^---+$/.test(line)) {
      flushPara();
      out.push('<hr>');
    } else if ((m = line.match(/^>+\s?(.*)/))) {
      flushPara();
      const content = mdInline(m[1]);
      if (out.length && /<\/blockquote>$/.test(out[out.length - 1])) {
        out[out.length - 1] = out[out.length - 1]
          .replace(/<\/blockquote>$/, '<br>' + content + '</blockquote>');
      } else {
        out.push('<blockquote>' + content + '</blockquote>');
      }
    } else {
      para.push(line);
    }
  }
  flushPara();

  let html = out.join('\n');
  // A citation paragraph immediately after a blockquote flows inline with it
  html = html.replace(/<\/blockquote>\s*<p>(<cite>[\s\S]*?<\/cite>)<\/p>/g, ' $1</blockquote>');
  return html;
}

/* ── Quality-of-life helpers ─────────────────────────────── */

function installProgressBar() {
  const bar = document.createElement('div');
  bar.className = 'progress-bar';
  document.body.appendChild(bar);
  function update() {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    bar.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  }
  document.addEventListener('scroll', update, { passive: true });
  update();
}

function installBackToTop() {
  const btn = document.createElement('button');
  btn.className = 'back-to-top';
  btn.setAttribute('aria-label', 'Back to top');
  btn.innerHTML = '&#8593;';
  btn.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  document.body.appendChild(btn);
  function toggle() {
    btn.classList.toggle('visible', window.scrollY > 600);
  }
  document.addEventListener('scroll', toggle, { passive: true });
  toggle();
}

/* Arrow-key navigation between prev/next links inside .chunk-nav */
function installKeyboardNav() {
  document.addEventListener('keydown', (e) => {
    if (e.target.matches('input, textarea, select')) return;
    if (e.key !== 'ArrowLeft' && e.key !== 'ArrowRight') return;
    const nav = document.querySelector('.chunk-nav');
    if (!nav) return;
    const links = nav.querySelectorAll('a');
    const target = e.key === 'ArrowLeft' ? links[0] : links[links.length - 1];
    if (target && target.href) window.location.href = target.href;
  });
}

/* Build a TOC from rendered h2 headings and track the active section */
function buildToc(bodyEl, tocListEl) {
  const heads = bodyEl.querySelectorAll('h2');
  tocListEl.innerHTML = '';
  heads.forEach((h) => {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = '#' + h.id;
    a.textContent = h.textContent;
    li.appendChild(a);
    tocListEl.appendChild(li);
  });
  if (!('IntersectionObserver' in window)) return;
  const links = tocListEl.querySelectorAll('a');
  const byId = {};
  links.forEach((a) => { byId[a.getAttribute('href').slice(1)] = a; });
  const obs = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (en.isIntersecting) {
        links.forEach((a) => a.classList.remove('active'));
        const a = byId[en.target.id];
        if (a) a.classList.add('active');
      }
    });
  }, { rootMargin: '0px 0px -75% 0px' });
  heads.forEach((h) => obs.observe(h));
}
