---
title: "One YAML File, Six Resumes, and an API"
date: 2026-03-05
tags: ["coding", "80-20"]
---

I got tired of maintaining several versions of my resume. Every format, whether PDF, website or portfolio, had its own copy of the same information, and they drifted out of sync. So I over-engineered the problem once so I would never have to think about it again.

### The source of truth

Everything lives in a single YAML file: work history, skills, education, projects. One file, one place to update. Change a job title or add a project and every output picks it up.

The core engine uses Quarto to generate PDF, HTML and presentation formats from that YAML source. The formats are the interesting part.

### The formats

- **Quarto Academic.** Clean LaTeX-typeset personal website and portfolio. The serious version.
- **Magazine.** Interactive magazine-style layout with page transitions. Vanilla JavaScript and CSS, no frameworks. Flip through it like a publication.
- **Word Cloud.** Interactive word cloud visualisation with responsive design. A visual snapshot of what I do, weighted by experience.
- **Quest.** An 8-bit card game that turns the resume into an explorable adventure. If someone is going to spend time reading my CV, they might as well have fun doing it.
- **Blog.** Jekyll-powered resume with articles, running on GitHub Pages.
- **Standard.** PDF and HTML via Quarto. The one you would actually send to a recruiter.

### The API

The same YAML file feeds a FastAPI backend, so the resume is accessible programmatically. Code can query it. LLMs can access it via MCP. If someone, or something, wants to know what I have worked on, there is an endpoint for it.

### The 80-20 take

The upfront investment was real. Now updating my resume across six formats and a live API means editing one file. Do the work once, in the right place, and let automation handle the rest.

This is plain text infrastructure in practice. See [Plain Text Is Forever](/posts/plain-text-is-forever/) for the philosophy.
