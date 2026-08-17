# House News

The studio's editorial publication. Intelligence, tools, and infrastructure - written like a magazine, not a feed.

Published by Propagation House. Built on the Propagation House layout (Acumin Pro + Playfair Display, olive/military-green palette on paper-cream).

---

## Directory Structure

```
house-news/
+-- index.html                  # Front page - the magazine
+-- assets/
|   +-- fonts/                  # Acumin Pro (OTF) + Playfair Display (TTF)
|   +-- css/
|   |   +-- shared.css          # Shared branding/layout (extracted from inline styles)
|   +-- images/                 # Hero visuals, generated art per article
+-- articles/                   # Published articles (live HTML)
+-- drafts/                     # Work-in-progress before publishing
+-- templates/
|   +-- article-template.html   # Blank article scaffold with branding pre-wired
+-- content/
|   +-- articles.json           # Registry: title, date, category, author, status, filename, summary
|   +-- topics.json             # Topic manifest - what we hunt for, not what we poll
+-- README.md                   # This file
+-- archive/                    # Old versions and backups
```

## Editorial Architecture

House News replaces the old RSS-firehose intelligence feed with a **topic-driven** model. Instead of polling 18 sources for thousands of headlines a day, we define the trends we care about and hunt for them directly.

### The Three Lenses

Every article is framed through one of three lenses:

- **Intelligence** - Core technical shifts in the AI substrate. Models, agents, research breakthroughs. The Architect's view.
- **Tools** - Immediate tool updates, workflow optimizations, creative software releases. The Shovel's view.
- **Infrastructure** - Semiconductors, compute, data centers, power, supply chain, geopolitics. The Gardener's view.

A fourth non-intelligence lens exists for studio voice:
- **Studio** - Plants, music, the workbench. The house speaking for itself.

### Topics (defined in `content/topics.json`)

1. **ai_agents** (intelligence, weekly) - Gemini, agentic enterprise, agent frameworks, DeepMind
2. **semiconductors** (infrastructure, weekly) - TSMC, H200/H100, chip geopolitics, data center power
3. **robotics_autonomy** (intelligence, weekly) - Humanoid, driverless freight, Unitree/Boston Dynamics, embodied AI
4. **generative_design** (tools, biweekly) - WebGL, generative UI, AI design tools, shader art
5. **regulatory_geopolitical** (intelligence, weekly) - Export controls, FDA, EU AI Act, chip sovereignty
6. **security_infrastructure** (infrastructure, biweekly) - Breaches, AI infra attacks, supply chain

### Primary Sources (trimmed from 18 to 9)

- research.google/blog
- blogs.nvidia.com
- Microsoft Research Blog
- arxiv.org/cs.LG (filtered to specific tracks)
- MIT Technology Review
- Ars Technica
- Wired
- codrops.com
- creativebloq.com

## Workflow

### Adding a new article

1. **Scan**: For each topic in `topics.json`, run the `search_queries` through `web_search`. Cross-reference hits against `primary_sources` for full reads.
2. **Decide**: Pick 1-3 stories per topic worth a full article.
3. **Draft**: Copy `templates/article-template.html` into `drafts/<slug>.html`. Write the article. Use the lens to frame it.
4. **Review**: Read it. If it holds, promote.
5. **Publish**: Move `drafts/<slug>.html` to `articles/<slug>.html`. Update `content/articles.json` (add to `published` array). Link from `index.html`.
6. **Archive**: Anything superseded goes to `archive/` with a note in `articles.json`.

### Article conventions

- **Filename**: kebab-case, no date prefix (date lives in `articles.json` and the byline)
- **Fonts**: Acumin Pro (body, sans), Playfair Display (headlines, serif). Both loaded via `@font-face` from `assets/fonts/`.
- **Palette**: `--ink:#1a1d12`, `--paper:#f5f2e6`, `--accent:#4b5320` (olive/military green), `--rule:#c8c3ad`, `--muted:#6b6e5a`
- **CSS**: Articles currently use inline `<style>` blocks (legacy from signal-magazine). New articles should link `assets/css/shared.css` and add only article-specific styles inline. Migration of existing articles to shared.css is ongoing.
- **Visuals**: SVG diagrams preferred over raster. See `archive/composure-viz-v2.html` for examples (channel maps, session state diagrams). CSS gradient placeholders acceptable for drafts.
- **Byline**: "By The Studio" unless a specific author is called for. Always include date and read time.
- **Tags**: Lowercase, hyphenated. Stored in the article footer.

### Index page (`index.html`)

The front page is static HTML, not generated. When an article is published:
- Add it to the appropriate section (Front Grid, Feature, Opinion, or Rail)
- Update the "Most Read" rail if it's getting traction
- Update the ticker if it's a headline-worthy dispatch
- Update the volume/issue number in the footer

## Migration Notes (from signal-magazine)

- `signal-magazine/` is preserved as the prototype. Do not delete.
- All article HTML files were copied here and renamed to clean slugs.
- The composure article exists in multiple versions in `archive/`. The published version (`articles/composure.html`) is the latest text-complete version. The SVG visualizations from `archive/composure-viz-v2.html` should be merged into the published version when time permits.
- Backups of the original index and composure article are in `archive/`.

## RSS Skill Integration

The `rss-intelligence-check` skill (at `C:\Users\Bl0ck\Substrate\skills\rss-intelligence-check.md`) should be updated to:
1. Read `content/topics.json` instead of the old `intelligence_feed.md` source list
2. Run topic-based `web_search` queries instead of polling RSS feeds
3. Output article drafts to `drafts/` instead of a markdown briefing file

That skill update is a separate task.

## Maintenance

- **Weekly**: Run the topic scan, draft 3-6 articles, promote the best 1-3
- **Monthly**: Review `topics.json` - add emerging trends, retire stale queries
- **Quarterly**: Review source list - promote new primary sources, demote ones that have gone noisy
- **Ongoing**: Migrate inline article CSS to `shared.css` as articles are touched
