# Editor Guide

> How to use the Kabulhaden CMS content editor effectively.

## Overview

The Kabulhaden CMS editor provides a rich editing experience for creating and managing
articles, podcast episodes, and broadcast episodes. The editor supports multiple content
formats, autosave, SEO tools, and real-time preview.

## Rich Text Editor

### Toast UI Editor

The CMS uses **Toast UI Editor** for WYSIWYG content editing. It provides:

- Visual (rich text) editing mode
- Markdown editing mode
- Split-view mode (edit + preview side by side)
- Image embedding and upload
- Table creation and editing
- Code block syntax highlighting

### Switching Between Modes

The editor supports three content formats (defined in `utils/choices.py`):

```python
class ContentFormat(models.TextChoices):
    RICH_TEXT = 'RICH_TEXT', 'Rich Text'
    MARKDOWN = 'MARKDOWN', 'Markdown'
    HTML = 'HTML', 'HTML'
```

- **Rich Text** — Visual WYSIWYG editing (default for new content)
- **Markdown** — Direct Markdown syntax editing
- **HTML** — Raw HTML editing (advanced users only)

### Editor Toolbar

| Button | Function | Keyboard Shortcut |
|--------|----------|-------------------|
| Bold | Toggle bold text | `Ctrl+B` |
| Italic | Toggle italic text | `Ctrl+I` |
| Strikethrough | Toggle strikethrough | — |
| Heading (H1–H3) | Insert heading | — |
| Quote | Insert blockquote | — |
| Code | Inline code | — |
| Code Block | Fenced code block | — |
| Bullet List | Unordered list | — |
| Numbered List | Ordered list | — |
| Task List | Checkbox list | — |
| Link | Insert hyperlink | `Ctrl+K` |
| Image | Insert image | — |
| Table | Insert table | — |
| HR | Horizontal rule | — |

## Markdown Support

### Syntax Reference

```markdown
# Heading 1
## Heading 2
### Heading 3

**Bold text**
*Italic text*
~~Strikethrough~~

> Blockquote

- Unordered list item
1. Ordered list item

- [x] Task list item (checked)
- [ ] Task list item (unchecked)

[Link text](https://example.com)
![Image alt text](image-url.jpg)

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |

`inline code`

```python
# Code block with syntax highlighting
def hello():
    print("Hello, Kabulhaden!")
```
```

### Markdown Tips

- Use `##` for section headings in article body
- Use `>` for highlighted quotes or pull quotes
- Use code blocks for technical content
- Keep paragraphs short for mobile readability
- Use task lists for checklists in show notes

## Autosave Behavior

The CMS implements **automatic content saving** to prevent data loss.

### Configuration

| Parameter | Value |
|-----------|-------|
| Debounce interval | 3 seconds |
| Trigger | After content change (idle period) |
| Method | POST to autosave endpoint |
| Visual indicator | Save status shown in editor |

### How It Works

```
User types → 3-second idle → Auto-POST to /autosave/ → Server saves draft
```

### Autosave Endpoint

- **Articles:** `POST /berita/cms/artikel/<uuid>/autosave/`
- The endpoint accepts partial data (content, title, etc.)
- Creates or updates a draft version
- Returns JSON status response

### What Gets Autosaved

- Content body (text/HTML)
- Title
- Excerpt (if applicable)
- Current status remains `DRAFT`

### What Does NOT Get Autosaved

- Status changes (requires explicit workflow action)
- Published state changes
- SEO metadata (saved on form submit)
- Tags and categories (saved on form submit)

### Tips

- Don't rely solely on autosave — use the Save button for important changes
- Autosave only works for DRAFT content
- Check the save indicator in the editor toolbar
- Network issues may delay autosave — the editor queues changes

## Preview Mode

### Live Preview

The editor offers a split-view mode:

1. **Edit mode** (default) — Full-width editor
2. **Split mode** — Editor on left, preview on right
3. **Preview mode** — Full-width preview of rendered content

### Preview Features

- Renders Markdown to HTML in real-time
- Shows heading structure and formatting
- Displays embedded images at full size
- Applies the same CSS as the public website
- Updates as you type (debounced)

### Preview Triggers

- Toggle via editor mode button
- Keyboard shortcut: `Ctrl+Shift+P`
- Preview auto-refreshes on content changes

## Media Embedding

### Image Insertion

1. Click the Image button in toolbar (or `Ctrl+Shift+I`)
2. Options:
   - **Upload** — Select from local files
   - **URL** — Paste external image URL
   - **Media Library** — Browse existing uploads

### Image Best Practices

| Requirement | Recommendation |
|------------|----------------|
| Format | JPEG for photos, PNG for graphics, WebP preferred |
| Max size | 2MB recommended |
| Dimensions | 1200×630px for featured images (OG ratio) |
| Alt text | Always provide descriptive alt text |
| Caption | Use caption for attribution |

### Audio Embedding (Podcast Episodes)

- Upload via the audio file field on podcast episode forms
- Supported formats: MP3, WAV, OGG, M4A
- File is stored at `podcast/episodes/audio/`
- Duration should be entered in seconds

### Video Embedding (Broadcast Episodes)

- Upload via the recording video field on episode forms
- Supported formats: MP4, WebM
- File is stored at `broadcast/episode/video/`

## Word Count and Reading Time

### Automatic Calculation

For Articles, the CMS automatically calculates:

```python
# apps/news/models.py — line 115
def _calculate_word_count(self):
    text = re.sub(r'<[^>]+>', ' ', self.content or '')
    words = text.split()
    return len(words)

def _calculate_reading_time(self):
    words = self._calculate_word_count()
    minutes = max(1, words // 200)
    return minutes
```

### Display

| Metric | Displayed In |
|--------|-------------|
| Word count | Article detail view, list view |
| Reading time | Article detail view (e.g., "5 min read") |

### Calculation Rules

- HTML tags are stripped before counting
- Words are split by whitespace
- Reading time: 200 words per minute (minimum 1 minute)
- Updated on every save

### Content Length Guidelines

| Content Type | Recommended Length |
|-------------|-------------------|
| Short article | 300–600 words |
| Standard article | 600–1200 words |
| Long-form article | 1200–3000 words |
| Podcast episode notes | 100–300 words |
| Show description | 150–250 words |

## SEO Scoring

The CMS provides a real-time SEO score for each piece of content.

### Scoring Algorithm

Points are awarded for the following criteria:

| Criterion | Points | Optimal |
|-----------|--------|---------|
| Has meta title | 20 | Yes |
| Title length 30–60 chars | 10 | Yes |
| Has meta description | 20 | Yes |
| Description length 120–160 chars | 10 | Yes |
| Has OG title | 10 | Yes |
| Has OG description | 10 | Yes |
| Has OG image | 10 | Yes |
| Has keywords | 10 | Yes |
| **Total** | **100** | |

### Grade Scale

| Score | Grade | Color | Action |
|-------|-------|-------|--------|
| 90–100 | A | Green | Excellent — no changes needed |
| 70–89 | B | Blue | Good — minor improvements possible |
| 50–69 | C | Yellow | Fair — consider improvements |
| 30–49 | D | Orange | Poor — significant improvements needed |
| 0–29 | F | Red | Critical — major SEO issues |

### SEO Tips

1. **Title** — Include primary keyword, keep 30–60 characters
2. **Description** — Compelling summary, 120–160 characters
3. **OG Image** — Use 1200×630px image for social sharing
4. **Keywords** — Use 3–5 relevant keywords, comma-separated
5. **Canonical URL** — Set for duplicate or syndicated content

## Content Editing Workflow

### Creating New Content

1. Navigate to the content type list (e.g., Articles)
2. Click "Tambah" (Add) button
3. Fill in the required fields:
   - **Title** — Descriptive, keyword-rich
   - **Content** — Main body in chosen format
   - **Category** — Select from existing categories
   - **Tags** — Add relevant tags
4. The editor auto-saves your draft
5. Preview your content before submitting

### Editing Existing Content

1. Navigate to the content detail or list page
2. Click the edit button (pencil icon)
3. Make your changes
4. Click "Simpan" (Save) to persist changes
5. Or click "Kirim ke Review" to submit for approval

### Submitting for Review

1. Ensure content is complete
2. Click "Kirim ke Review" (Submit for Review)
3. Status changes from DRAFT → PENDING_REVIEW
4. An editor will review and approve/reject

### Publishing

1. After approval, click "Terbitkan" (Publish)
2. Or schedule for future publication
3. Content goes live on the public website

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+K` | Insert link |
| `Ctrl+B` | Bold |
| `Ctrl+I` | Italic |
| `Ctrl+Shift+P` | Toggle preview |
| `Ctrl+S` | Manual save |
| `Cmd+K` | Open search (global) |
| `Cmd+D` | Toggle dark mode |
| `[` | Toggle sidebar |
| `Esc` | Close modal/panel |

## Mobile Editing

The CMS editor is responsive and works on mobile devices:

- Touch-friendly toolbar buttons
- Simplified mobile layout
- Bottom navigation bar on mobile
- Quick actions FAB for common operations
- Swipe gestures for sidebar navigation

## Content Formatting Tips

### Paragraphs

- Use double line breaks between paragraphs
- Keep paragraphs to 3–4 sentences maximum
- Use subheadings every 200–300 words

### Lists

- Use bullet lists for non-sequential items
- Use numbered lists for step-by-step instructions
- Keep list items parallel in structure

### Emphasis

- **Bold** for key terms and important information
- *Italic* for titles, foreign words, and emphasis
- Use blockquotes for pull quotes or notable statements

### Links

- Use descriptive link text (not "click here")
- Link to relevant internal content when possible
- Open external links in new tabs

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| Autosave not working | Check network connection; refresh page |
| Image not uploading | Verify file size (<2MB) and format |
| Preview not updating | Toggle preview mode off/on |
| Content not saving | Check required fields; try manual save |
| SEO score not calculating | Ensure SEO fields are filled |
