---
title: "Markdown: Plain Text With Just Enough Structure"
date: 2026-02-14
tags: ["thinking", "80-20", "coding"]
---

*Part of the [Plain Text Is Forever](/posts/plain-text-is-forever/) series.*

Raw `.txt` works fine for quick notes and task lists. But when you need headings, links, code blocks, or emphasis, Markdown gives you all of that without leaving the keyboard. It's readable as-is — no rendering required — and it converts to virtually anything: HTML, DOCX, PDF, slides.

Write once. Render everywhere.

## Just Enough Syntax

The syntax is minimal enough to learn in ten minutes and powerful enough to write entire books. A `#` for a heading. `**` for bold. `-` for a list. `[text](url)` for a link. That covers about 90% of what most people need, most of the time.

And because it's just text with conventions, there's no binary format to corrupt, no version incompatibility to debug, no "please upgrade to access your files" ransom note.

## Readable Without Rendering

This is the part that separates Markdown from every other markup language. An HTML file without a browser is a mess of angle brackets. A LaTeX file without a compiler is barely readable. A Markdown file without *anything* is still a perfectly clear document.

That's the design philosophy: the source *is* the document. Rendering just makes it prettier.

## The Conversion Pipeline

Markdown's real power shows up when you need output in multiple formats. The same `.md` file can become:

- A blog post (Hugo, Jekyll, Astro)
- A PDF (Pandoc, Quarto)
- A slide deck (Marp, reveal.js)
- A Word document (Pandoc)
- An email (most Markdown editors)

One source file, many outputs. No copy-pasting between formats. No reformatting. No "which version is the latest?" confusion.

## Where It Fits in the Stack

Think of it this way: plain text is the foundation. Markdown is plain text with just enough structure to be useful for longer-form writing. You don't *need* Markdown for a quick note or a shopping list — `.txt` is fine for that. But the moment you want sections, links, or code, Markdown earns its keep without adding complexity.

It's the 80-20 of document formats. Minimal syntax, maximum reach.

---

*Next: [The 80/20 of Productivity Tools](/posts/plain-text-8020-productivity/)*
