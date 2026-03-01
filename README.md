# 8020workshop.com

<!-- BADGES:START -->
[![automated-deployment](https://img.shields.io/badge/-automated--deployment-blue?style=flat-square)](https://github.com/topics/automated-deployment) [![blog](https://img.shields.io/badge/-blog-blue?style=flat-square)](https://github.com/topics/blog) [![css](https://img.shields.io/badge/-css-1572b6?style=flat-square)](https://github.com/topics/css) [![custom-theme](https://img.shields.io/badge/-custom--theme-blue?style=flat-square)](https://github.com/topics/custom-theme) [![github-pages](https://img.shields.io/badge/-github--pages-blue?style=flat-square)](https://github.com/topics/github-pages) [![html](https://img.shields.io/badge/-html-e34f26?style=flat-square)](https://github.com/topics/html) [![hugo](https://img.shields.io/badge/-hugo-blue?style=flat-square)](https://github.com/topics/hugo) [![personal-website](https://img.shields.io/badge/-personal--website-blue?style=flat-square)](https://github.com/topics/personal-website) [![static-site](https://img.shields.io/badge/-static--site-blue?style=flat-square)](https://github.com/topics/static-site) [![website](https://img.shields.io/badge/-website-2196f3?style=flat-square)](https://github.com/topics/website)
<!-- BADGES:END -->

Personal site for The 80-20 Workshop. Built with [Hugo](https://gohugo.io/) and a custom theme.

## Local development

```bash
hugo server -D
```

## New post

```bash
hugo new posts/my-post-title.md
```

Edit the file, remove `draft: true` when ready to publish.

## Deploy

Push to `main` branch. GitHub Actions builds and deploys to GitHub Pages automatically.

## Tag descriptions

Edit `data/tagmeta.json` to add tooltip descriptions for tags on the homepage word cloud.
