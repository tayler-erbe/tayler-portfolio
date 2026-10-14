# Site design system

Every page on taylererbe.com loads one stylesheet, `assets/site.css`. It holds the tokens (colours, type, spacing, radii, shadows) and the shared components (nav, footer, page header, section, cards, metric tiles, tables, callouts, code, buttons, tags, back link). A page's own `<style>` block may only hold layout that is unique to that page, and it may only use tokens.

The look is the home page's: a dark theme, a cyan accent, square corners, Barlow Condensed for display type, DM Sans for text and DM Mono for labels and data. There is no light theme.

## Rules

1. **No raw colours on a page.** Use `var(--token)`. A colour that has no token gets a token in `site.css` first. This applies to `<style>`, `style=""`, SVG `fill`/`stroke`/`stop-color` attributes and styles built by scripts.
2. **No font names on a page.** Use `var(--font-display)`, `var(--font-body)`, `var(--font-mono)` or `var(--font-heading)`. Fonts are loaded once, by `site.css`; pages do not link Google Fonts.
3. **No page-level tokens.** `:root { --x: ... }` belongs in `site.css` only.
4. **Same chrome everywhere.** Every page has the shared nav (`nav.site-nav`) and footer (`footer.site-footer`), both linking to the portfolio, `skyrule.html` and `resume.pdf`. Every page except the home page ends with the back link.
5. **Reuse before inventing.** Use a shared component when one fits. A page-specific class is fine for a one-off layout (a chart legend, a search demo), styled with tokens.
6. **Restyling never changes text.** Markup and classes only; prose goes through the Qwen writer and Tayler's approval.
7. **Run the check before committing:** `python tools/check_style.py` must print "All N pages pass".

## Tokens

### Colour

| Token | Value | Use |
|---|---|---|
| `--bg` | #080b10 | Page background |
| `--surface` | #0f1318 | Cards, tiles, alternate sections |
| `--surface2` | #161c24 | Raised cards, callouts, hover state of a tile |
| `--surface3` | #1f2230 | Hover state of a raised card |
| `--border` | #1e2530 | Every hairline and 1px grid gap |
| `--nav-bg` | rgba(8,11,16,.88) | Nav and sub-nav background (with blur) |
| `--white` | #eef3f8 | Headings, emphasised figures |
| `--text` | #d8e2ed | Body text, values, `strong` inside muted text |
| `--muted` | #6b7c91 | Prose paragraphs, secondary text |
| `--muted2` | #3a4556 | Captions, step numbers, footer text |
| `--ink` | #0b0c0f | Text on an accent-filled button |
| `--accent` | #5bc8dc | Primary: links, big figures, active state, focus ring |
| `--accent-hover` | #82d9e8 | Hover of accent links and the primary button |
| `--accent2` | #3a8fc4 | Secondary: eyebrows, section tags, tag outlines |
| `--accent3` | #c07a6e | Warm: caution, challenger, personal-project tags |
| `--accent-dim`, `--accent-faint` | cyan at 12% / 8% | Tinted backgrounds, link underlines |
| `--green`, `--green-bg` | #5dbf8a | Active, pass, winner |
| `--blue`, `--blue-bg` | #3a8fc4 | Status hue (same as accent2) |
| `--coral`, `--coral-bg` | #c07a6e | Status hue (same as accent3) |
| `--warm` | #e07a3d | Personal-project highlight (Legacy, Skyrule card) |
| `--gold`, `--slate`, `--violet`, `--lilac` | | Single-page highlight hues kept from existing pages |
| `--viz-*` | 21 hues | Chart and diagram series only, never UI chrome |
| `--paper`, `--navy`, `--rust` | | The Legacy app preview illustration only |

### Type

| Token | Value | Use |
|---|---|---|
| `--font-display` | Barlow Condensed | Page titles, section titles, big figures; usually uppercase, weight 700-800 |
| `--font-body` | DM Sans | Paragraphs and UI text |
| `--font-mono` | DM Mono | Labels, eyebrows, tags, tables' first column, code, data |
| `--font-heading` | = `--font-display` | Card and entry titles (project cards, experience entries, chart titles) and the former serif accents (Legacy's italic lines). Barlow Condensed by Founder decision, 14 Oct |
| `--text-2xs` .. `--text-2xl` | 0.65rem .. clamp(2.8rem, 5vw, 5rem) | Tags and meta labels (2xs), mono labels (xs), card body (sm), prose (base), hero description (md), card titles (lg), section titles (xl), page title (2xl) |
| `--leading-tight / -normal / -prose` | 1.0 / 1.6 / 1.8 | Display type / UI / paragraphs |
| `--tracking-label`, `--tracking-eyebrow` | 0.08em / 0.15em | Mono uppercase labels / hero eyebrow |

### Spacing, radii, shadows, motion

| Token | Value | Use |
|---|---|---|
| `--space-1` .. `--space-8` | 0.25, 0.5, 0.75, 1, 1.5, 2, 3, 4.5rem | All gaps and padding in components |
| `--gutter` | 3rem, 1.5rem under 860px, 1.25rem under 480px | Page side padding |
| `--nav-h` | 4.25rem (3.5rem on phones) | Fixed nav height; page headers clear it |
| `--content-max` | 1080px | Reading width for `.wrap` pages |
| `--measure` | 60ch | Longest line of body text, about 75 characters (Founder, 14 Oct). Applies to paragraphs and list items in sections and headers, step and stage bodies, cautions and takeaways. Tables, charts, code, key-value lists and grids stay full width |
| `--radius` | 0 | Cards, tiles, buttons, tables: the look is square |
| `--radius-sm` | 2px | Inline code, small pills |
| `--radius-round` | 50% | Dots and avatars only |
| `--shadow-glow` | 0 0 6px currentColor | Live status dot |
| `--focus-ring` | 2px solid accent | Every `:focus-visible` outline |
| `--dur` | 0.2s | Hover transitions |

## Components

| Component | Markup | Use |
|---|---|---|
| **Site nav** | `nav.site-nav > a.nav-logo + ul.site-nav-links > li > a` | Same seven links on every page; `li.nav-secondary` items hide under 900px so Projects, Skyrule and Resume stay visible on phones. Mark the current page with `aria-current="page"` |
| **Sub-nav** | `nav.subnav > ul > li > a` or `div.subnav` | Under the site nav, sticky: in-page section links or a page status (badge plus link). Long evaluation pages only |
| **Page header** | `.hero > .hero-eyebrow + h1 (span/em = accent line) + p.hero-desc + .hero-meta > .meta-item > .meta-label + .meta-value` | Top of every project page. Optional `.toc` (`a > .toc-num + .toc-name`) and `.hero-stats` under it. The home page adds `.hero-home` for its two-column layout |
| **Section** | `section > .section-header > .section-tag + h2.section-title + .section-line`, optional `p.section-lede` | Every content section. Tag reads `NN / Name`; title is display type, uppercase; `em` or `span` in the title takes the accent |
| **Prose** | `.prose > p` | Running text: muted, 1.8 leading, capped at `--measure`; `strong` lifts to `--text`; links underline |
| **Stat strip** | `.stat-strip > .stat-item > .stat-big + .stat-desc` | Full-width row of 4 figures under a page header (`.stat-strip-5` for five) |
| **Stat cards** | `.hero-stats > .stat-card > .stat-icon + .stat-num + .stat-label + .stat-sub` | Labelled tiles. Add `.hero-stats-4` for four across and `.hero-stats-figures` when the values are numbers |
| **Results strip** | `.results-strip > .result-cell > .result-num + .result-label` | Figures inside a section (`.results-strip-4` for four) |
| **Card** | `.card`, `.insight-box` (`.insight-box-title`, `p`) in `.insight-grid` | A boxed point. Insight boxes sit two across |
| **Comparison card** | `.method-grid > .method-card(.winner/.challenger) > .method-header > .method-name + .method-badge`, then `.metric-row > .metric-label + .metric-value(.good/.warn)` | Side-by-side options with measured values |
| **Callout** | `.callout > .callout-label + p`; variants `.callout-good`, `.callout-warn`, `.callout-info`; `.warn` for a caution note; `.takeaway` for a one-line conclusion | Emphasis that sits beside the prose |
| **Steps** | `.pipeline > .pipeline-step > .step-num + div > .step-title + .step-body` | Numbered process |
| **Stages** | `.stage > .stage-head > .stage-id + .stage-name` + `.stage-body` | Documented pipeline stages |
| **Key-value list** | `.kv > .k + .v` pairs | Labelled facts, timelines |
| **Tags** | `.tag-row > span.tag(.tag-accent/.tag-warm/.tag-green)` | Technology chips. One tag style site-wide (the old `.chip` classes became `.tag`) |
| **Badge / status** | `.badge(.badge-green/.badge-warn/.badge-blue)`, `.status > .status-dot` | Short state labels |
| **Tables** | `table.dt` (`td.num` for figures) or `table.cat-table` | Data tables: mono uppercase headers, hairline rows. Under 760px every table scrolls inside its own box |
| **Code** | inline `code`; block `.code-block > pre` with `.code-comment`, `.code-keyword` | Code and file trees |
| **Figure** | `.chart-wrap` + `.chart-caption`; `figure.shot` with `figcaption` | Charts and screenshots |
| **Buttons** | `a.btn-primary`, `a.btn-ghost` | Calls to action. One primary per group |
| **Back link** | `.back-section > a.back-link` | End of every page except the home page, above the footer |
| **Site footer** | `footer.site-footer > .site-footer-meta > p` + `ul.site-footer-links` | Page's own footer lines on the left; Portfolio, Skyrule, Resume (PDF), GitHub, LinkedIn on the right |
| **Helpers** | `.link`, `.label`, `.mono`, `.text-accent`, `.text-muted` ... | Small text treatments that replace repeated inline styles |

## Responsive and accessibility

- Breakpoints: 900px (nav collapses to its primary links), 860px (grids go to one column, gutters shrink), 760px (section header wraps, tables scroll), 480px (phone: tiles stack, nav tightens). Every page is checked at 400px with no horizontal page scroll.
- Focus: every focusable element shows the accent ring on keyboard focus.
- Motion: the hero fade-in and hover transitions switch off under `prefers-reduced-motion`.

## Checking

`python tools/check_style.py` fails if any page uses a raw hex colour or a named font family outside `site.css`, defines its own tokens, misses the shared stylesheet, nav or footer, or has a broken local link or anchor.
