---
title: "One YAML File, Six Resumes, and an API"
date: 2026-03-05
tags: ["coding", "80-20"]
---

I got tired of maintaining several versions of my resume. Every format, whether PDF, website or portfolio, had its own copy of the same information, and they drifted out of sync. So I over-engineered the problem once so I would never have to think about it again.

### The source of truth

Everything lives in a single YAML file: work history, skills, education, projects. One file, one place to update. Change a job title or add a project and every output picks it up.

The core engine uses Quarto to generate PDF, HTML and presentation formats from that YAML source. The formats are where most of the work went.

### The formats

- **Quarto Academic.** Clean LaTeX-typeset personal website and portfolio. The formal one.
- **Magazine.** A magazine-style layout with page transitions, built in vanilla JavaScript and CSS. Flip through it like a publication.
- **Word Cloud.** A word cloud built from the same data.
- **Quest.** An 8-bit card game version. Not the one I send to recruiters, but people do play it.
- **Blog.** Jekyll-powered resume with articles, running on GitHub Pages.
- **Standard.** PDF and HTML via Quarto. The one I send to recruiters.

### The API

The same YAML file feeds a FastAPI backend, so the resume is accessible programmatically. Code can query it. LLMs can access it via MCP. If someone, or something, wants to know what I have worked on, there is an endpoint for it.

### The 80-20 take

The upfront investment was real. Now updating my resume across six formats and a live API means editing one file. I do the work once and let automation repeat it.

This is plain text infrastructure in practice. See [Plain Text Is Forever](/posts/plain-text-is-forever/) for the philosophy.
