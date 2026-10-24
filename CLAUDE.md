# FrontierAGI Academy — Claude Agent Context

## Project Type
Static educational website. No framework, no backend — one small Python script (`scripts/build.py`, see below) keeps shared markup in sync.
All pages are plain HTML/CSS/JS served as files.

## File Structure
```
FrontierAGI-Academy/
├── index.html              ← Home page (stays in root, always) — AGI research/progress hub
├── styles.css              ← All CSS (single file)
├── app.js                  ← All JS (single file)
├── pages/                  ← All sub-pages live here
│   ├── blog.html
│   ├── frontier-model-learning.html  ← the interactive mode-based LLM course (formerly index.html)
│   ├── frontier-timeline.html
│   ├── future-frontier.html
│   ├── llm-engineering.html
│   ├── ai-news.html
│   ├── india-ai.html
│   ├── china-ai.html
│   └── usa-ai.html
├── blog/                   ← Blog posts + manifest
│   ├── index.json          ← Post manifest (source of truth for all blog UI)
│   ├── _template.html      ← Copy this to create a new post
│   └── [slug].html         ← Individual post files
└── docs/
    └── CONTRIBUTING.md     ← How to add pages and posts
```

**Note (Sep 2026 restructure):** `index.html` used to BE the interactive mode-based LLM course.
That entire experience moved to `pages/frontier-model-learning.html` unchanged, and `index.html` is
now a separate AGI-research/progress homepage (hero, latest blog signal, the 3 startup lanes, deep
investigations, researcher's path, explore links). The navbar's "Learning Mode" panel and every
`?mode=X` link across the site point at `pages/frontier-model-learning.html`, not `index.html`.

## Path Rules (critical)
| File location | styles.css | app.js | index.html (homepage) | frontier-model-learning.html | Other pages |
|---|---|---|---|---|---|
| `index.html` (root) | `styles.css` | `app.js` | — | `pages/frontier-model-learning.html` | `pages/foo.html` |
| `pages/*.html` | `../styles.css` | `../app.js` | `../index.html` | `frontier-model-learning.html` (same dir) | `foo.html` (same dir) |
| `blog/*.html` | `../styles.css` | `../app.js` | `../index.html` | `../pages/frontier-model-learning.html` | `../pages/foo.html` |

## Navbar Architecture
Two-ribbon fixed navbar:
- Ribbon 1 (`.navbar-brand`, 46px): indigo gradient, logo only
- Ribbon 2 (`.navbar-main`, 48px): white, 4 tab buttons + 1 direct link
- Total navbar height: **94px** — all pages set `padding-top: 94px` on first element after nav

Nav tabs open slide-down panels (`.nav-panel`) — NOT CSS hover dropdowns.
Panel JS lives in `app.js`: `initNavPanels()`, `closeAllNavPanels()`.
Backdrop (`#navBackdrop`) closes panels on click.

### Nav panels inserted after `</nav>` in every HTML file:
```html
<div class="nav-backdrop" id="navBackdrop"></div>
<div class="nav-panel-wrap" id="navPanelWrap">
  <div class="nav-panel" id="navPanel-mode">...</div>
  <div class="nav-panel" id="navPanel-explore">...</div>
  <div class="nav-panel" id="navPanel-ecosystems">...</div>
  <div class="nav-panel" id="navPanel-blog">...</div>
</div>
```

## Learning Modes
8 modes: layman, graduate, researcher, team, startup, investor, founder, agentmode.
- Live on `pages/frontier-model-learning.html`: mode buttons use `onclick="setMode('mode')"` with `id="modeBtn_mode"`
- Everywhere else, mode links point AT that file: `href="../pages/frontier-model-learning.html?mode=X"` (from `blog/*.html`) or `href="frontier-model-learning.html?mode=X"` (from `pages/*.html`)
- Mode state persisted via `sessionStorage('llm-mode')`
- URL param `?mode=X` read on load in `app.js`

## Blog System
- Manifest: `blog/index.json` — add entry here to publish a post
- Template: `blog/_template.html` — copy and fill in
- Nav Recent Posts: `loadBlogNavPosts()` in `app.js` — reads manifest, populates `#blogNavMenu`
- Blog listing page: `pages/blog.html` — reads manifest, renders cards

### blog/index.json schema:
```json
{
  "slug": "post-slug",
  "title": "Post Title",
  "excerpt": "One-two sentence summary.",
  "author": "Author Name",
  "authorInitials": "AN",
  "date": "2026-06-22",
  "readTime": "5 min",
  "tags": ["Tag1", "Tag2"],
  "emoji": "🧠",
  "featured": false
}
```
Only one post should have `"featured": true` at a time.

## CSS Conventions
- All CSS in `styles.css` — append new sections at the bottom with a banner comment
- CSS variables in `:root`: `--accent`, `--accent2`, `--accent3`, `--text`, `--border`, `--bg-card`, etc.
- Light theme only (no dark mode toggle)
- Mobile breakpoint at `768px`

## Adding a New Page
1. Copy an existing page from `pages/` as your template
2. Place the new file in `pages/`
3. If it belongs in the nav, edit `partials/nav.html` (never the generated block inside pages), then run `python3 scripts/build.py`
4. Paths: use `../styles.css`, `../app.js`, `../index.html` at top

## Build Step (`scripts/build.py`)
Still no framework — one Python script keeps shared markup in sync. Run it after ANY change (new post, manifest edit, nav edit):
```bash
python3 scripts/build.py          # rewrites generated blocks, sitemap.xml, robots.txt, 404.html, README table
python3 scripts/build.py --check  # what CI runs: fails if anything is stale or an internal link/anchor is broken
```
- Nav source of truth: `partials/nav.html` (`{{ROOT}}`/`{{PAGES}}`/`{{BLOG}}` path prefixes, `{{ACTIVE_x}}` tab markers). Pages hold it between `<!-- NAV:START -->`/`<!-- NAV:END -->` — never hand-edit that block.
- SEO block (`<!-- SEO:START -->…<!-- SEO:END -->`) after `<title>`: description, canonical, Open Graph, Twitter card. Blog posts take title/excerpt/date from `blog/index.json`; other pages use their first intro paragraph.
- Social preview image: `assets/og-default.png`.
- Series footer (`<!-- SERIES:START -->…<!-- SERIES:END -->`, before `</main>` in every post): prev/next links. A series = one homepage spotlight grid, in card order, so adding a card to the right grid on `index.html` is all it takes — build.py picks it up.
- `blog/series.json` (generated): every series with its short label, icon and ordered slugs. `pages/blog.html` builds its sidebar categories and card labels from it. Manifest `tags` are no longer used for navigation.
- Homepage "· N Articles" counts on spotlight tags are kept in sync automatically.
- `pages/idea-map.html`: the 3D "AI Idea Map" (dependency-free canvas renderer; reachable from the nav and the "See it in 3D" button, no longer on the homepage). Its data `blog/idea-graph.json` is generated by build.py from every `ar-card` in `blog/ai-research-*-papers.html` plus the hand-curated `data/idea-map.json` (research area per card, lineage links `[from, to, kind?]`, short labels, guided tours, and `core`: the ~120 key ideas shown by `idea-map.html?view=core`, the 3D map's `?embed=1` mode, and the default view of `idea-flow.html`). When a new "AI Research in YEAR" article is added, give each new card an area in `nodeArea` and at least one link — `--check` fails on unknown or unassigned cards.
- `pages/idea-flow.html` ("AI Idea Flow"): vertical SVG metro map, 2026 at the top down to 1950 (time flows upward) — one column per research area, one bubble per paper card (radius = number of cards built directly on it), curved flows origin → target, canvas particle streams down each line, interchange rings where parents come from 2+ areas, and a click-to-open family tree (bottom sheet on phones; phones default to 3 lines with a pick-up-to-3 chooser). `idea-flow.html?embed=1` is a chrome-free mode used by the homepage iframe in the AI Research Progress section. It reads the same `blog/idea-graph.json` as the 3D map (default view = all cards; the "Key ideas" toggle shows the `core` list bridged), so there is no extra data to maintain.
- `pages/lab-updates.html` ("Frontier Lab Updates"): every release/announcement from 13 frontier labs, Oct 2021 → Sep 2026, newest first. Source of truth: `data/lab-updates.json` (`labs`, `types`, `items` with `date` as `YYYY-MM-DD` or `YYYY-MM`, `lab`, `type`, `title`, `summary`, `facts`, `source`, `flagship`). build.py renders the cards into the page (`<!-- LABITEMS -->`), plus the homepage ticker strip (`<!-- LABSTRIP -->`, inside the hero) and the "Latest from the Labs" section (`<!-- LABLATEST -->`). To add an announcement: add one item with an https source, then run the build; `--check` rejects unknown labs/types, bad or out-of-range dates, missing sources and duplicate ids.
- `pages/rsi-evolution.html` ("RSI Evolution Map"): loop-anatomy explorer + three views (autonomy staircase L1–L5, "what gets rewritten" by 10 object families, research-vs-industry timeline). Data `data/rsi-papers.json` (522 papers, 14 industry cases) is generated by `python3 scripts/import_awesome_rsi.py` from the CC0 Awesome-RSI catalog (theseus-labs-rsi/awesome-rsi, survey arXiv:2609.11873) — keep the attribution box; `build.py --check` runs `validate_rsi()` on it. Post-cutoff months undercount because of the catalog's screening; industry figures are organisation-reported.
- `pages/start-here.html`: hand-curated reading tracks (new to AI / research / building). Update when a better entry point is published.

## Git Branch
Active development branch: `claude/trusting-mendel-u9s1oh`
Remote: `gopalakrbiec-ui/Claude_Project_3_LLM` (also mirrors to `gopalakrbiec-ui/FrontierAGI-Academy`)
