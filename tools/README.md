# TUI Blog Post Editor

A terminal-based editor for writing blog posts with AI-assisted editing.

## Setup

```bash
cd tools
pip install -r requirements.txt
```

## Usage

```bash
# Set your API key
export ANTHROPIC_API_KEY="your-key-here"

# Run the editor
python post_editor.py
```

## Workflow

1. **Opening menu** - Choose "New Post", "Edit Post", or "Exit"
2. **Edit Post** - Shows list of existing posts (sorted by most recent)
3. **Editor** - Write/edit content, select tags, use AI features
4. **Save** - Save iteratively as you work
5. **Close** - Return to menu

## AI Features

### AI Generate (Ctrl+G)
Write an intro sentence or outline, then click "AI Generate" to expand into a full post.
- Uses title for context
- Follows 80-20 style: direct, practical, no fluff
- Aims for 200-400 words

### AI Improve (Ctrl+I)
Light touch editing on existing content:
- Fixes grammar and typos
- Improves clarity
- Preserves length and voice
- Keeps technical details intact

### AI Tags (Ctrl+T)
Suggests 1-3 tags based on content:
- Prefers existing tags when they fit
- Can create new tags with descriptions
- Automatically adds suggested tags to selection

## Text Editing

Standard editing keys work in the content area:
- `Ctrl+C` / `Ctrl+V` - Copy/Paste
- `Ctrl+X` - Cut
- `Ctrl+A` - Select all
- `Delete` / `Backspace` - Delete text

## Keyboard Shortcuts

- `Ctrl+S` - Save post
- `Ctrl+P` - Publish (save + git add/commit/push)
- `Ctrl+G` - AI Generate (expand intro)
- `Ctrl+I` - AI Improve (light editing)
- `Ctrl+T` - AI Tags (suggest tags)
- `Escape` - Close (return to menu)
- `Ctrl+Q` - Quit application
- `Tab` - Navigate between fields

## Publishing

The **Publish** button (or `Ctrl+P`) saves the post and runs:
```bash
git add content/posts/your-post.md
git commit -m "Add post: Your Post Title"  # or "Update post:" for edits
git push
```

The site auto-deploys via GitHub Actions after push.

## AI Prompts

The AI prompts are tuned for the 80-20 Workshop style:

**Generate** - "Direct and personal, practical and hands-on, short paragraphs, punchy sentences, include specific details, no fluff"

**Improve** - "Light editing only, fix grammar/typos, improve clarity where unclear, keep same length, preserve author's voice"

**Tags** - Prefers existing tags, only suggests new if nothing fits
