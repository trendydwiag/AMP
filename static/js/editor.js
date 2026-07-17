/**
 * Kabulhaden CMS - Rich Text Editor
 * Uses Toast UI Editor for WYSIWYG editing
 */
document.addEventListener('DOMContentLoaded', function() {
    const editorContainer = document.getElementById('editor-container');
    if (!editorContainer) return;

    // Toast UI Editor CDN
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = 'https://uicdn.toast.com/editor/latest/toastui-editor.min.css';
    document.head.appendChild(cssLink);

    const script = document.createElement('script');
    script.src = 'https://uicdn.toast.com/editor/latest/toastui-editor-all.min.js';
    script.onload = function() {
        initEditor();
    };
    document.head.appendChild(script);

    function initEditor() {
        const contentField = document.getElementById('article-content');
        const initialContent = contentField ? contentField.value : '';

        const editor = new toastui.Editor({
            el: editorContainer,
            height: '500px',
            initialEditType: 'wysiwyg',
            previewStyle: 'vertical',
            usageStatistics: false,
            language: 'id',
            toolbarItems: [
                'heading', 'bold', 'italic', 'strike',
                'divider',
                'hr', 'quote',
                'divider',
                'ul', 'ol', 'task', 'indent', 'outdent',
                'divider',
                'table', 'link', 'divider',
                'code', 'codeblock'
            ],
            customHTMLSanitizer: function(html) {
                return html;
            }
        });

        editor.setMarkdown(initialContent);

        // Sync editor content to hidden textarea
        editor.on('change', function() {
            if (contentField) {
                contentField.value = editor.getHTML();
            }
            updateWordCount(editor.getMarkdown());
        });

        // Word count display
        function updateWordCount(text) {
            const words = text.trim().split(/\s+/).filter(w => w).length;
            const readTime = Math.max(1, Math.ceil(words / 200));
            const counter = document.getElementById('word-count-display');
            if (counter) {
                counter.textContent = `${words} kata · ${readTime} menit baca`;
            }
        }

        updateWordCount(initialContent);

        // Store editor reference globally for autosave
        window.cmsEditor = editor;
    }
});

/**
 * Markdown Preview
 */
function showMarkdownPreview(content, elementId) {
    const previewEl = document.getElementById(elementId);
    if (!previewEl || !window.marked) return;
    previewEl.innerHTML = marked.parse(content);
}

/**
 * Autosave with debounce
 */
let autosaveTimer = null;
function setupAutosave(articleId, csrfToken) {
    const editor = window.cmsEditor;
    if (!editor) return;

    editor.on('change', function() {
        clearTimeout(autosaveTimer);
        autosaveTimer = setTimeout(function() {
            const statusEl = document.getElementById('autosave-status');
            if (statusEl) statusEl.textContent = 'Menyimpan...';

            fetch(`/berita/cms/artikel/${articleId}/autosave/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken,
                    'X-Requested-With': 'XMLHttpRequest',
                },
                body: JSON.stringify({
                    content: editor.getHTML(),
                    title: document.querySelector('[name="title"]')?.value || '',
                    excerpt: document.querySelector('[name="excerpt"]')?.value || '',
                })
            })
            .then(r => r.json())
            .then(data => {
                if (statusEl) {
                    statusEl.textContent = `Tersimpan ${new Date(data.saved_at).toLocaleTimeString('id-ID')}`;
                    statusEl.classList.add('text-green-600');
                    setTimeout(() => statusEl.classList.remove('text-green-600'), 2000);
                }
            })
            .catch(() => {
                if (statusEl) statusEl.textContent = 'Gagal menyimpan';
            });
        }, 3000);
    });
}
