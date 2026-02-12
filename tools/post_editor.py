#!/usr/bin/env python3
"""TUI Blog Post Editor with AI-assisted editing."""

import json
import os
import re
import subprocess
from datetime import date
from pathlib import Path

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import Screen
from textual.widgets import (
    Button,
    Footer,
    Header,
    Input,
    Label,
    ListItem,
    ListView,
    Select,
    Static,
    TextArea,
)

# Paths relative to project root (resolve to absolute path first)
PROJECT_ROOT = Path(__file__).resolve().parent.parent
TAGMETA_PATH = PROJECT_ROOT / "data" / "tagmeta.json"
POSTS_PATH = PROJECT_ROOT / "content" / "posts"


def load_tags() -> dict:
    """Load tags from tagmeta.json."""
    if TAGMETA_PATH.exists():
        with open(TAGMETA_PATH) as f:
            return json.load(f)
    return {}


def save_tags(tags: dict) -> None:
    """Save tags to tagmeta.json."""
    with open(TAGMETA_PATH, "w") as f:
        json.dump(tags, f, indent=2)
        f.write("\n")


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[-\s]+", "-", text)
    return text.strip("-")


def load_post(filepath: Path) -> dict:
    """Load a post file and parse frontmatter."""
    content = filepath.read_text()

    # Parse YAML frontmatter
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            frontmatter_text = parts[1].strip()
            body = parts[2].strip()

            # Simple YAML parsing
            frontmatter = {}
            for line in frontmatter_text.split("\n"):
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()
                    # Handle quoted strings
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    # Handle tags array
                    if key == "tags" and value.startswith("["):
                        try:
                            value = json.loads(value)
                        except json.JSONDecodeError:
                            value = []
                    frontmatter[key] = value

            return {
                "title": frontmatter.get("title", ""),
                "date": frontmatter.get("date", str(date.today())),
                "tags": frontmatter.get("tags", []),
                "content": body,
                "filepath": filepath,
            }

    return {
        "title": filepath.stem,
        "date": str(date.today()),
        "tags": [],
        "content": content,
        "filepath": filepath,
    }


def get_anthropic_client():
    """Get Anthropic client or raise error."""
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("anthropic package not installed")

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY not set")

    return anthropic.Anthropic(api_key=api_key)


def ai_improve(content: str) -> str:
    """Light touch editing - grammar, clarity, preserve length and voice."""
    client = get_anthropic_client()

    system_prompt = """You are an editor for "The 80-20 Workshop" blog.
Style: direct, practical, personal. No corporate speak.

Your task: LIGHT editing only.
- Fix grammar and typos
- Improve clarity where genuinely unclear
- Keep the same length - don't shorten or expand
- Preserve the author's voice and style
- Keep technical details intact

Return ONLY the edited text. No comments."""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": content}],
    )
    return message.content[0].text


def ai_generate(intro: str, title: str = "") -> str:
    """Expand an intro/outline into a full blog post."""
    client = get_anthropic_client()

    system_prompt = """You are a writer for "The 80-20 Workshop" blog.
Philosophy: 80% of the result with 20% of the effort - that's plenty.

Style guide:
- Direct and personal ("I did X" not "one might do X")
- Practical and hands-on
- Short paragraphs, punchy sentences
- Include specific details (prices, part numbers, settings)
- No fluff, no filler, no "in this post I will..."
- Conversational but not chatty

Take the intro/outline and expand into a complete blog post.
Keep it focused - aim for 200-400 words unless the topic needs more.
Return ONLY the post content. No meta-commentary."""

    context = f"Title: {title}\n\n" if title else ""
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=4096,
        system=system_prompt,
        messages=[{"role": "user", "content": f"{context}Expand this into a full post:\n\n{intro}"}],
    )
    return message.content[0].text


def ai_suggest_tags(content: str, existing_tags: dict) -> list[str]:
    """Suggest tags for content from existing tags or propose new ones."""
    client = get_anthropic_client()

    tag_list = "\n".join(f"- {tag}: {info['description']}" for tag, info in existing_tags.items())

    system_prompt = f"""You suggest tags for blog posts.

Available tags:
{tag_list}

Rules:
1. Suggest 1-3 tags that fit the content
2. Prefer existing tags when they fit well
3. Only suggest a NEW tag if nothing existing fits
4. For new tags, format as: newtag: description

Return ONLY a JSON array of strings, nothing else.
Example: ["printing", "klipper"]"""

    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=256,
        system=system_prompt,
        messages=[{"role": "user", "content": content}],
    )

    try:
        response = message.content[0].text
        # Find JSON array in response using regex
        match = re.search(r'\[.*?\]', response, re.DOTALL)
        if match:
            return json.loads(match.group())
        return []
    except (json.JSONDecodeError, IndexError):
        return []


class SelectedTags(Static):
    """Display selected tags."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.tags: list[str] = []

    def update_tags(self, tags: list[str]) -> None:
        self.tags = tags
        if tags:
            self.update(f"Selected: {', '.join(tags)}")
        else:
            self.update("No tags selected")


class MenuScreen(Screen):
    """Opening menu screen."""

    CSS = """
    MenuScreen {
        align: center middle;
    }

    #menu-container {
        width: 40;
        height: auto;
        padding: 2 4;
        border: solid $primary;
        background: $surface;
    }

    #menu-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 2;
    }

    #menu-container Button {
        width: 100%;
        margin: 1 0;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        with Vertical(id="menu-container"):
            yield Static("80-20 Post Editor", id="menu-title")
            yield Button("New Post", id="new-post-btn", variant="primary")
            yield Button("Edit Post", id="edit-post-btn", variant="default")
            yield Button("Exit", id="exit-btn", variant="error")
        yield Footer()

    @on(Button.Pressed, "#new-post-btn")
    def new_post(self) -> None:
        self.app.push_screen(EditorScreen())

    @on(Button.Pressed, "#edit-post-btn")
    def edit_post(self) -> None:
        self.app.push_screen(PostPickerScreen())

    @on(Button.Pressed, "#exit-btn")
    def exit_app(self) -> None:
        self.app.exit()


class PostListItem(ListItem):
    """ListItem that stores a post path."""

    def __init__(self, post_path: Path, title: str) -> None:
        super().__init__()
        self.post_path = post_path
        self._title = title

    def compose(self) -> ComposeResult:
        yield Static(f"{self._title} ({self.post_path.name})")


class PostPickerScreen(Screen):
    """Screen to pick an existing post to edit."""

    CSS = """
    PostPickerScreen {
        align: center middle;
    }

    #picker-container {
        width: 70;
        height: auto;
        max-height: 80%;
        padding: 1 2;
        border: solid $primary;
        background: $surface;
    }

    #picker-title {
        text-align: center;
        text-style: bold;
        margin-bottom: 1;
    }

    #post-list {
        height: auto;
        max-height: 20;
    }

    #cancel-btn {
        margin-top: 1;
        width: 100%;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()

        # Build list items during compose
        posts = sorted(POSTS_PATH.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
        items = []
        for post_path in posts:
            post_data = load_post(post_path)
            items.append(PostListItem(post_path, post_data["title"]))

        with Vertical(id="picker-container"):
            yield Static("Select Post to Edit", id="picker-title")
            yield ListView(*items, id="post-list")
            yield Button("Cancel", id="cancel-btn", variant="error")

        yield Footer()

    @on(ListView.Selected, "#post-list")
    def post_selected(self, event: ListView.Selected) -> None:
        """Open selected post in editor."""
        if isinstance(event.item, PostListItem):
            self.app.pop_screen()
            self.app.push_screen(EditorScreen(event.item.post_path))

    @on(Button.Pressed, "#cancel-btn")
    def cancel(self) -> None:
        self.app.pop_screen()


class EditorScreen(Screen):
    """Main editor screen."""

    CSS = """
    #title-row, #date-row, #tag-row {
        height: 3;
        margin: 0 1;
    }

    #title-row Label, #date-row Label, #tag-row Label {
        width: 8;
        padding: 1 0;
    }

    #title-input {
        width: 1fr;
    }

    #date-input {
        width: 20;
    }

    #tag-select {
        width: 25;
    }

    #add-tag-btn, #ai-tags-btn {
        width: 10;
        margin-left: 1;
    }

    #clear-tags-btn {
        width: 8;
        margin-left: 1;
    }

    #selected-tags {
        margin: 0 1;
        height: 2;
        color: $text-muted;
    }

    #content-area {
        height: 1fr;
        margin: 1;
    }

    #button-row {
        height: 3;
        margin: 0 1;
        align: center middle;
    }

    #button-row Button {
        margin: 0 1;
    }

    #status {
        height: 1;
        margin: 0 1;
        color: $success;
    }

    #new-tag-container {
        height: 4;
        margin: 0 1;
        display: none;
    }

    #new-tag-container.visible {
        display: block;
    }

    #new-tag-input, #new-tag-desc {
        width: 1fr;
        margin-right: 1;
    }
    """

    BINDINGS = [
        Binding("ctrl+s", "save", "Save"),
        Binding("ctrl+p", "publish", "Publish"),
        Binding("ctrl+i", "do_improve", "AI Improve"),
        Binding("ctrl+g", "do_generate", "AI Generate"),
        Binding("ctrl+t", "do_suggest_tags", "AI Tags"),
        Binding("escape", "close", "Close"),
    ]

    def __init__(self, post_path: Path = None):
        super().__init__()
        self.post_path = post_path  # None for new post
        self.all_tags = load_tags()
        self.selected_tags: list[str] = []
        self.post_data = None

    def compose(self) -> ComposeResult:
        yield Header()

        with Vertical():
            # Title row
            with Horizontal(id="title-row"):
                yield Label("Title:")
                yield Input(placeholder="Post title", id="title-input")

            # Date row
            with Horizontal(id="date-row"):
                yield Label("Date:")
                yield Input(value=str(date.today()), id="date-input")

            # Tag row
            with Horizontal(id="tag-row"):
                yield Label("Tags:")
                tag_options = [(tag, tag) for tag in sorted(self.all_tags.keys())]
                yield Select(tag_options, prompt="Select tag", id="tag-select")
                yield Button("+ Add", id="add-tag-btn", variant="default")
                yield Button("AI Tags", id="ai-tags-btn", variant="primary")
                yield Button("Clear", id="clear-tags-btn", variant="warning")

            # Selected tags display
            yield SelectedTags(id="selected-tags")

            # New tag input (hidden by default)
            with Horizontal(id="new-tag-container"):
                yield Input(placeholder="Tag name", id="new-tag-input")
                yield Input(placeholder="Description", id="new-tag-desc")
                yield Button("Create", id="create-tag-btn", variant="success")
                yield Button("Cancel", id="cancel-tag-btn", variant="error")

            # Main content area
            yield TextArea(id="content-area")

            # Button row
            with Horizontal(id="button-row"):
                yield Button("AI Generate", id="generate-btn", variant="warning")
                yield Button("AI Improve", id="improve-btn", variant="primary")
                yield Button("Save", id="save-btn", variant="success")
                yield Button("Publish", id="publish-btn", variant="primary")
                yield Button("Close", id="close-btn", variant="default")

            # Status bar
            yield Static("", id="status")

        yield Footer()

    def on_mount(self) -> None:
        """Load post data if editing existing post."""
        if self.post_path:
            self.post_data = load_post(self.post_path)
            self.query_one("#title-input", Input).value = self.post_data["title"]
            self.query_one("#date-input", Input).value = str(self.post_data["date"])
            self.query_one("#content-area", TextArea).text = self.post_data["content"]

            if isinstance(self.post_data["tags"], list):
                self.selected_tags = self.post_data["tags"]
            self.update_selected_tags_display()
            self.set_status(f"Editing: {self.post_path.name}")

    def update_selected_tags_display(self) -> None:
        """Update the selected tags display."""
        widget = self.query_one("#selected-tags", SelectedTags)
        widget.update_tags(self.selected_tags)

    @on(Select.Changed, "#tag-select")
    def tag_selected(self, event: Select.Changed) -> None:
        """Handle tag selection."""
        if event.value and event.value != Select.BLANK:
            tag = str(event.value)
            if tag not in self.selected_tags:
                self.selected_tags.append(tag)
                self.update_selected_tags_display()
            # Reset select to prompt
            self.query_one("#tag-select", Select).value = Select.BLANK

    @on(Button.Pressed, "#clear-tags-btn")
    def clear_tags(self) -> None:
        """Clear all selected tags."""
        self.selected_tags = []
        self.update_selected_tags_display()

    @on(Button.Pressed, "#add-tag-btn")
    def show_add_tag(self) -> None:
        """Show the add tag inputs."""
        container = self.query_one("#new-tag-container")
        container.add_class("visible")
        self.query_one("#new-tag-input", Input).focus()

    @on(Button.Pressed, "#cancel-tag-btn")
    def hide_add_tag(self) -> None:
        """Hide the add tag inputs."""
        container = self.query_one("#new-tag-container")
        container.remove_class("visible")
        self.query_one("#new-tag-input", Input).value = ""
        self.query_one("#new-tag-desc", Input).value = ""

    @on(Button.Pressed, "#create-tag-btn")
    def create_tag(self) -> None:
        """Create a new tag."""
        name = self.query_one("#new-tag-input", Input).value.strip().lower()
        desc = self.query_one("#new-tag-desc", Input).value.strip()

        if not name:
            self.set_status("Tag name required", error=True)
            return

        if name in self.all_tags:
            self.set_status(f"Tag '{name}' already exists", error=True)
            return

        # Add to tags
        self.all_tags[name] = {"description": desc or f"Posts about {name}"}
        save_tags(self.all_tags)

        # Update select options
        tag_select = self.query_one("#tag-select", Select)
        tag_options = [(tag, tag) for tag in sorted(self.all_tags.keys())]
        tag_select.set_options(tag_options)

        # Select the new tag
        self.selected_tags.append(name)
        self.update_selected_tags_display()

        # Hide inputs
        self.hide_add_tag()
        self.set_status(f"Created tag: {name}")

    @on(Button.Pressed, "#ai-tags-btn")
    def action_do_suggest_tags(self) -> None:
        """Suggest tags using AI."""
        self.do_suggest_tags_work()

    @work(thread=True)
    def do_suggest_tags_work(self) -> None:
        """Background worker for tag suggestion."""
        content = self.query_one("#content-area", TextArea).text
        title = self.query_one("#title-input", Input).value

        if not content.strip() and not title.strip():
            self.app.call_from_thread(self.set_status, "Need content or title for tag suggestions", True)
            return

        self.app.call_from_thread(self.set_status, "Suggesting tags...")

        try:
            suggestions = ai_suggest_tags(f"Title: {title}\n\n{content}", self.all_tags)
            self.app.call_from_thread(self.apply_tag_suggestions, suggestions)
        except RuntimeError as e:
            self.app.call_from_thread(self.set_status, str(e), True)

    def apply_tag_suggestions(self, suggestions: list[str]) -> None:
        """Apply suggested tags."""
        if not suggestions:
            self.set_status("AI returned no tag suggestions")
            return

        added = []
        already_selected = []

        for suggestion in suggestions:
            if ":" in suggestion and suggestion.split(":")[0].strip().lower() not in self.all_tags:
                # New tag with description
                parts = suggestion.split(":", 1)
                tag_name = parts[0].strip().lower()
                tag_desc = parts[1].strip() if len(parts) > 1 else f"Posts about {tag_name}"

                self.all_tags[tag_name] = {"description": tag_desc}
                save_tags(self.all_tags)

                # Update select
                tag_select = self.query_one("#tag-select", Select)
                tag_options = [(tag, tag) for tag in sorted(self.all_tags.keys())]
                tag_select.set_options(tag_options)

                if tag_name not in self.selected_tags:
                    self.selected_tags.append(tag_name)
                    added.append(f"{tag_name} (new)")
            else:
                # Existing tag
                tag_name = suggestion.split(":")[0].strip().lower()
                if tag_name in self.all_tags:
                    if tag_name not in self.selected_tags:
                        self.selected_tags.append(tag_name)
                        added.append(tag_name)
                    else:
                        already_selected.append(tag_name)

        self.update_selected_tags_display()
        if added:
            self.set_status(f"Added tags: {', '.join(added)}")
        elif already_selected:
            self.set_status(f"Suggested tags already selected: {', '.join(already_selected)}")
        else:
            self.set_status(f"AI suggested: {suggestions} (no matches)")

    @on(Button.Pressed, "#improve-btn")
    def action_do_improve(self) -> None:
        """Light touch AI editing."""
        self.do_improve_work()

    @work(thread=True)
    def do_improve_work(self) -> None:
        """Background worker for improvement."""
        content = self.query_one("#content-area", TextArea).text
        if not content.strip():
            self.app.call_from_thread(self.set_status, "Nothing to improve", True)
            return

        self.app.call_from_thread(self.set_status, "Improving...")

        try:
            improved = ai_improve(content)
            self.app.call_from_thread(self.apply_content, improved, "Content improved!")
        except RuntimeError as e:
            self.app.call_from_thread(self.set_status, str(e), True)

    @on(Button.Pressed, "#generate-btn")
    def action_do_generate(self) -> None:
        """Expand intro into full post."""
        self.do_generate_work()

    @work(thread=True)
    def do_generate_work(self) -> None:
        """Background worker for generation."""
        content = self.query_one("#content-area", TextArea).text
        title = self.query_one("#title-input", Input).value

        if not content.strip():
            self.app.call_from_thread(self.set_status, "Write an intro or outline first", True)
            return

        self.app.call_from_thread(self.set_status, "Generating...")

        try:
            generated = ai_generate(content, title)
            self.app.call_from_thread(self.apply_content, generated, "Post generated!")
        except RuntimeError as e:
            self.app.call_from_thread(self.set_status, str(e), True)

    def apply_content(self, content: str, message: str) -> None:
        """Apply new content and show message."""
        self.query_one("#content-area", TextArea).text = content
        self.set_status(message)

    @on(Button.Pressed, "#save-btn")
    def action_save(self) -> None:
        """Save the post."""
        title = self.query_one("#title-input", Input).value.strip()
        post_date = self.query_one("#date-input", Input).value.strip()
        content = self.query_one("#content-area", TextArea).text.strip()

        if not title:
            self.set_status("Title required", error=True)
            return

        if not content:
            self.set_status("Content required", error=True)
            return

        # Use existing filepath or generate new one
        if self.post_path:
            filepath = self.post_path
        else:
            slug = slugify(title)
            filepath = POSTS_PATH / f"{slug}.md"
            self.post_path = filepath  # Remember for subsequent saves

        # Build frontmatter
        tags_yaml = json.dumps(self.selected_tags) if self.selected_tags else "[]"
        frontmatter = f'''---
title: "{title}"
date: {post_date}
tags: {tags_yaml}
---

{content}
'''

        # Save file
        POSTS_PATH.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(frontmatter)

        self.set_status(f"Saved: {filepath.name}")
        return True  # Indicate success

    @on(Button.Pressed, "#publish-btn")
    def action_publish(self) -> None:
        """Save and publish (git add, commit, push)."""
        self.do_publish_work()

    @work(thread=True)
    def do_publish_work(self) -> None:
        """Background worker for publishing."""
        title = self.query_one("#title-input", Input).value.strip()
        post_date = self.query_one("#date-input", Input).value.strip()
        content = self.query_one("#content-area", TextArea).text.strip()

        if not title or not content:
            self.app.call_from_thread(self.set_status, "Title and content required", True)
            return

        # Determine filepath
        if self.post_path:
            filepath = self.post_path
            is_new = False
        else:
            slug = slugify(title)
            filepath = POSTS_PATH / f"{slug}.md"
            is_new = True

        # Build and save
        tags_yaml = json.dumps(self.selected_tags) if self.selected_tags else "[]"
        frontmatter = f'''---
title: "{title}"
date: {post_date}
tags: {tags_yaml}
---

{content}
'''
        POSTS_PATH.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            f.write(frontmatter)

        self.post_path = filepath  # Remember for subsequent saves
        self.app.call_from_thread(self.set_status, "Saved, publishing...")

        # Git operations
        try:
            # git add
            subprocess.run(
                ["git", "add", str(filepath)],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
            )

            # git commit
            action = "Add" if is_new else "Update"
            commit_msg = f"{action} post: {title}"
            subprocess.run(
                ["git", "commit", "-m", commit_msg],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
            )

            # git push
            subprocess.run(
                ["git", "push"],
                cwd=PROJECT_ROOT,
                check=True,
                capture_output=True,
            )

            self.app.call_from_thread(self.set_status, f"Published: {filepath.name}")

        except subprocess.CalledProcessError as e:
            error_msg = e.stderr.decode() if e.stderr else str(e)
            self.app.call_from_thread(self.set_status, f"Git error: {error_msg[:50]}", True)

    @on(Button.Pressed, "#close-btn")
    def action_close(self) -> None:
        """Close editor and return to menu."""
        self.app.pop_screen()

    def set_status(self, message: str, error: bool = False) -> None:
        """Update status bar."""
        status = self.query_one("#status", Static)
        status.update(message)
        status.styles.color = "red" if error else "green"


class PostEditor(App):
    """TUI for editing blog posts."""

    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
    ]

    def on_mount(self) -> None:
        """Show menu on startup."""
        self.push_screen(MenuScreen())


if __name__ == "__main__":
    app = PostEditor()
    app.run()
