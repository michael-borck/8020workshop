# 8020workshop.com

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
