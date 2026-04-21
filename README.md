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

## Updating the wiki

All changes to the documentation **must go through a branch and a pull request** — never commit directly to `master`. This applies whether the update accompanies a code change or is a standalone wiki improvement.

### Workflow

1. **Create a branch** from the latest `master`:

   ```bash
   git checkout master && git pull
   git checkout -b wiki/<short-description>
   ```

   Use the `wiki/` prefix for documentation-only branches (e.g. `wiki/fix-starwall-howto`, `wiki/add-gpu-instructions`). If the documentation update is part of a code change, use whatever branch naming convention the code repository follows.

2. **Make your edits.** Add or modify the relevant Markdown files under `docs/`. Preview locally with `bundle exec jekyll serve --baseurl /doc_repo` to verify formatting, navigation order, and links.

3. **Commit and push:**

   ```bash
   git add docs/
   git commit -m "docs: <what changed>"
   git push -u origin wiki/<short-description>
   ```

4. **Open a pull request** on GitHub targeting `master`. In the PR description, briefly explain what was changed and why. Request a review from at least one other contributor if the change is non-trivial.

5. **Once approved, merge the PR.** The GitHub Pages workflow will automatically rebuild and deploy the site.

### Guidelines

- Keep each PR focused: one topic or section per pull request. This makes reviews faster and reduces the risk of merge conflicts.
- Always check that your changes render correctly locally before pushing. Pay attention to front matter fields (`parent`, `grand_parent`, `nav_order`) since mistakes there can break the navigation sidebar.

---

## Collaborative editing session

During the collaborative session, multiple people edit the wiki simultaneously. Because GitHub **does not support** real-time co-editing of the same file, coordination is essential to avoid merge conflicts.

### Before the session

1. **Assign sections to breakout rooms.** Each breakout room should be responsible for a distinct set of pages so that no two rooms edit the same file at the same time. An example could be the following:

   | Breakout room | Section path | Example pages |
   |---|---|---|
   | Room A | `docs/compiling/` | Getting Started guides, Input Parameters, Diagnostics |
   | Room B | `docs/physics/` | Base Fluid Models, Model Extensions, Notation |
   | Room C | `docs/numerics/` | Spatial Discretization, Grids, Solver |
   | Room D | `docs/howto/` (first half) | Getting Started howtos, Grid setup, Energy conservation |
   | Room E | `docs/howto/` (second half) | Particles, Stellarator, Controller module |
   | Room F | `docs/code_development/`, `docs/machines/` | Development Workflow, Regression Tests, Machine pages |

   The key rule is: **one file should only be edited by one room.**

2. **Pre-create branches.** Before the session starts, create one branch per breakout room so participants can get going immediately:

   ```bash
   git checkout master && git pull
   git checkout -b docs/compiling/
   git push -u origin docs/compiling/
   ```

   Repeat for each room.

### During the session

- Each room clones the repo.
- Participants within the same room can coordinate freely (pair-editing, splitting sub-pages among themselves) since they are all on the same branch and working on the same set of files.

### After the session

1. Each room **opens a pull request** from its branch to `master`.
2. Since rooms worked on disjoint files, PRs should merge cleanly without conflicts.

### Tips

- Prefer many small commits over one large commit.
- Use the local preview (`bundle exec jekyll serve`) to catch rendering issues before pushing.
- If you need to add a new section landing page (with `has_children: true`), coordinate with the session organizer since it may affect the global navigation.

---

## Deployment

Pushing to `master` automatically builds and deploys the site to GitHub Pages via the workflow in `.github/workflows/pages.yml`. No manual step needed.

To trigger a deployment without a code change, go to **Actions → Deploy to GitHub Pages → Run workflow**.

