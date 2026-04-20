# JOREK Wiki

Documentation site for the [JOREK](https://www.jorek.eu) project, built with [Jekyll](https://jekyllrb.com) and the [Just the Docs](https://just-the-docs.com) theme.

**Live site:** https://lukethewalker.github.io/doc_repo

---

## Local development

**Prerequisites:** Ruby ≥ 3.1, Bundler (`gem install bundler`)

```bash
git clone https://github.com/LukeTheWalker/doc_repo.git
cd doc_repo
bundle install
bundle exec jekyll serve --baseurl /doc_repo
```

Then open http://localhost:4000/doc_repo/

> **Note:** the first build downloads the remote Just the Docs theme and may take ~30 s.

---

## Adding content

Each page under `docs/` is a Markdown file with a small YAML front matter block:

```yaml
---
title: "My Page"
nav_order: 5
parent: "Section Name"        # omit for top-level pages
grand_parent: "Parent Name"   # level-3 pages only
layout: default
render_with_liquid: false
---

Page content goes here.
```

Section landing pages (e.g. `cat_physics.md`) have `has_children: true` and `nav_fold: true` — edit those to rename a section.

---

## Deployment

Pushing to `master` automatically builds and deploys the site to GitHub Pages via the workflow in `.github/workflows/pages.yml`. No manual step needed.

To trigger a deployment without a code change, go to **Actions → Deploy to GitHub Pages → Run workflow**.
