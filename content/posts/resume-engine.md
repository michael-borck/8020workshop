---
title: "One YAML File, Six Resumes, and an API"
date: 2026-03-05
tags: ["coding", "80-20"]
---

I got tired of maintaining multiple versions of my resume. Every format — PDF, website, portfolio — had its own copy of the same information, and they'd inevitably drift out of sync. So I did what any reasonable person would do: I over-engineered the problem once so I'd never have to think about it again.

### The Source of Truth

Everything lives in a single YAML file. Work history, skills, education, projects — one file, one place to update. Change a job title or add a new project, and every output format picks it up automatically.

The core engine uses Quarto to generate PDF, HTML, and presentation formats from that YAML source. But the formats are where it gets interesting.

### The Formats

- **Quarto Academic** — Clean LaTeX-typeset personal website and portfolio. The "serious" version.
- **Magazine** — Interactive magazine-style layout with page transitions. Vanilla JavaScript and CSS, no frameworks. Flip through it like a publication.
- **Word Cloud** — Interactive word cloud visualisation with responsive design. A visual snapshot of what I do, weighted by experience.
- **Quest** — An 8-bit card game that turns the resume into an explorable adventure. Because if someone's going to spend time reading my CV, they might as well have fun doing it.
- **Blog** — Jekyll-powered resume with articles, running on GitHub Pages.
- **Standard** — PDF and HTML via Quarto. The one you'd actually send to a recruiter.

### The API

The same YAML file also feeds a FastAPI backend, so the resume is accessible programmatically. Code can query it. LLMs can access it via MCP. If someone — or something — wants to know what I've worked on, there's an endpoint for that.

### The 80-20 Take

The upfront investment was real. But now, updating my resume across six formats and a live API means editing one file. That's the 80-20 principle applied to maintenance: do the work once, in the right place, and let automation handle the rest.
