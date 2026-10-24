# Contributing to FrontierAGI Academy

## Adding a Blog Post

1. **Copy the template**
   ```bash
   cp blog/_template.html blog/your-post-slug.html
   ```

2. **Edit the HTML** — update every `<!-- CHANGE: -->` marker:
   - `<title>` tag
   - `.blog-post-tag` (emoji + category labels)
   - `<h1 class="blog-post-title">`
   - Author name + initials in `.blog-card-author-avatar`
   - Date and read time in `.blog-post-meta`
   - Post body inside `.blog-post-body`

3. **Add to the manifest** — open `blog/index.json` and prepend a new entry to the `"posts"` array:
   ```json
   {
     "slug": "your-post-slug",
     "title": "Your Post Title",
     "excerpt": "One or two sentence summary shown on the blog card.",
     "author": "Your Name",
     "authorInitials": "YN",
     "date": "2026-06-22",
     "readTime": "5 min",
     "tags": ["Tag1", "Tag2"],
     "emoji": "🧠",
     "featured": false
   }
   ```
   Set `"featured": true` to pin the post at the top (only one post at a time).

4. **Commit and push**
   ```bash
   git add blog/your-post-slug.html blog/index.json
   git commit -m "Blog: add post — Your Post Title"
   git push
   ```

---

## Adding a New Sub-Page

1. **Copy an existing page** from `pages/` as your starting point:
   ```bash
   cp pages/india-ai.html pages/your-new-page.html
   ```

2. **Set correct paths** at the top of the file:
   ```html
   <link rel="stylesheet" href="../styles.css" />
   ...
   <script src="../app.js"></script>
   ```

3. **Add it to the nav (if it belongs there)** — edit `partials/nav.html` once, using `{{PAGES}}your-new-page.html`. Do not edit the `<!-- NAV:START -->…<!-- NAV:END -->` block inside any page; it is regenerated.

   Then run the build, which re-inserts the nav and SEO tags into every page, updates `sitemap.xml` and `README.md`, and fails on broken internal links:
   ```bash
   python3 scripts/build.py
   ```

4. **Commit and push**
   ```bash
   git add blog/your-post-slug.html blog/index.json
   git commit -m "Blog: add post — Your Post Title"
   git push
   ```

---

## Adding a New Sub-Page

1. **Copy an existing page** from `pages/` as your starting point:
   ```bash
   cp pages/india-ai.html pages/your-new-page.html
   ```

2. **Set correct paths** at the top of the file:
   ```html
   <link rel="stylesheet" href="../styles.css" />
   ...
   <script src="../app.js"></script>
   ```

3. **Update the nav panels** — add a link to the new page in every HTML file that has nav panels. The easiest way is a small Python script:
   ```python
   import os, glob

   # Example: add to the Explore panel
   OLD = '<a href="llm-engineering.html" class="panel-btn">⚙️ LLM Engineering</a>'
   NEW = OLD + '\n        <a href="your-new-page.html" class="panel-btn">🆕 New Page</a>'

   files = ['index.html'] + glob.glob('pages/*.html') + glob.glob('blog/*.html')
   for f in files:
       c = open(f).read()
       if OLD in c:
           open(f, 'w').write(c.replace(OLD, NEW))
   ```
   Remember path differences:
   - In `index.html`: use `pages/your-new-page.html`
   - In `pages/*.html`: use `your-new-page.html`
   - In `blog/*.html`: use `../pages/your-new-page.html`

4. **Commit and push**
   ```bash
   git add -A pages partials sitemap.xml README.md
   git commit -m "Add: Your New Page title"
   git push
   ```

---

## File Structure Quick Reference

```
FrontierAGI-Academy/
├── index.html          ← Home (root only)
├── styles.css          ← All CSS
├── app.js              ← All JS
├── pages/              ← All sub-pages
├── blog/               ← Blog posts + index.json manifest
├── docs/               ← This file + architecture notes
└── CLAUDE.md           ← AI agent context (do not delete)
```

## Path Rules

| You're editing... | Link to index | Link to pages/foo | Link to blog/post |
|---|---|---|---|
| `index.html` | — | `pages/foo.html` | `blog/post.html` |
| `pages/*.html` | `../index.html` | `foo.html` | `../blog/post.html` |
| `blog/*.html` | `../index.html` | `../pages/foo.html` | `post.html` |
