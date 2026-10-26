# Lessons (state for the authoring loop)

Pitfalls already hit while building this site, and their fixes. Read before building a new page or series; add a line when something new bites.

## Pages and inline JS
- Inside inline `<script>` strings, write `\x22` for double quotes in generated HTML attributes (e.g. `href=\x22…\x22`); `build.py --check` parses `href="' + x + '"` as a broken link. Use `\x27` for apostrophes inside single-quoted JS strings.
- New pages: copy the head from an existing page by finding `</style>` before `</head>` and `<!-- NAV:END -->` **by search, never by line number**. Nav length changes when nav items are added.
- Rewriting a page's intro paragraph: the first `<p>` text also appears in the generated SEO block. Replace inside the hero, not the first match in the file.
- `sed` replacement strings: `&` means "the match". It broke JS once (`'Schedulers & monitoring'`). Use Python for edits containing `&`.

## SVG and canvas figures
- Long SVG labels clip at the viewBox edge. Right-anchor labels near the right edge (`text-anchor="end"`); offset end labels on line charts so they don't overlap.
- Boxes in loop or flow diagrams: size them for the longest label (≥ 7 px per character at 12 px bold), and keep x ≥ half the box width from 0.
- Canvas 3D (`ai-factory-3d.html`):
  - eye-level views need near-plane polygon clipping and subdivided large faces, or painter's sorting breaks;
  - text signs need all four corners in front of the camera, or the affine transform explodes.
- Hide decorative particles in first-person views; they show through walls.

## Testing
- Playwright: scroll the target into view before mouse tests. The page is long and events off-screen do nothing.
- Test pages at 1400 and 390 px and screenshot the key figures, not just the top of the page. Most layout bugs were found in screenshots, not by the overflow check.
- Nav tabs reported as off-screen at 390 px are the site's normal horizontally-scrolling nav, not a bug.

## Content honesty
- The owner finds long paragraphs hard to read: Maestro parts use bullets and sub-bullets and several visuals per part. Write that way from the start.
- Maestro parts must be long and researched (the owner asked twice). Phase 1 first shipped at ~2,500 words and had to be expanded; research then corrected a claim (DGX H100 racks need three power feeds, not A/B). Research before writing, not after.
- Cross-references like "section N" break when sections are added; the Maestro generator links and renumbers them, so write "section N" against the original order or use an anchor link.
- Run article code and paste real output. Two of the most useful findings (hoarded skills hurt; one learning rate does not fit all sizes) came from runs that "failed".
- Code that was not run says "not executed for this article" in its header. Story outcomes go in a `wr-caveat` box starting "Scenario".
- Before calling a gap a gap, check what exists (e.g. `ls blog | grep …` for slugs) to avoid linking to missing articles.

## Environment
- The sandbox has no torch by default. Install it with `pip install --target /tmp/tlib` plus the CUDA wheels it requires, then run with `PYTHONPATH=/tmp/tlib`. `pip` and `python3` may be different Python versions; use `python3 -m pip`.
- The scratchpad is wiped when the session container restarts. Keep anything reusable (article code) in `data/code/<slug>/`.
