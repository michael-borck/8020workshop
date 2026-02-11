# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/claude-code) when working with code in this repository.

## Project Overview

This is a Hugo-based static website for "The 80-20 Workshop" - a personal blog by Michael Borck focused on projects that embody the 80-20 philosophy: focus on what matters, skip the rest.

## Key Commands

```bash
# Local development server (includes drafts)
hugo server -D

# Build site for production
hugo

# Create a new post
hugo new posts/my-post-title.md
```

## Project Structure

- `hugo.toml` - Main site configuration
- `content/posts/` - Blog posts in markdown
- `content/about.md` - About page
- `themes/8020/` - Custom theme (layouts, CSS, JS)
- `data/tagmeta.json` - Tag descriptions for homepage tooltips

## Theme Architecture

The site uses a custom "8020" theme located in `themes/8020/`:

- `layouts/index.html` - Homepage with interactive tag word cloud
- `layouts/_default/baseof.html` - Base template with header/footer
- `layouts/_default/list.html` - Post listings and taxonomy pages
- `layouts/_default/single.html` - Individual post pages
- `static/css/style.css` - All styling

## Content Guidelines

Posts use YAML front matter:
```yaml
---
title: "Post Title"
date: 2026-02-10
tags: ["tag1", "tag2"]
---
```

Available tags are defined in `data/tagmeta.json` with descriptions that appear as tooltips on the homepage word cloud.

## Deployment

The site deploys to GitHub Pages via GitHub Actions. Push to main branch triggers automatic build and deployment.

Base URL: https://8020workshop.com/
